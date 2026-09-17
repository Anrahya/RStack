#!/usr/bin/env python3
"""Tiny executable mechanism fixtures; NOT evidence of model capability uplift.

Keep this evaluator and its reference fixes outside candidate access. Grading
executes candidate code and needs the host's sandbox for untrusted candidates.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import tempfile
import textwrap

CASES = {
    'tenant-boundary': {
        'request': 'Fix document access so a signed-in actor can read only their own document. Preserve the owner success path and the missing-document result. Keep the public function signature.',
        'bug': "def read_document(actor, document):\n    if document is None:\n        return None\n    return document['text'] if actor else None\n",
        'reference': "def read_document(actor, document):\n    if document is None or actor is None or actor != document['owner']:\n        return None\n    return document['text']\n",
        'checks': "d={'owner':'alice','text':'private'}; assert m.read_document('alice',d)=='private'; assert m.read_document('bob',d) is None; assert m.read_document(None,d) is None; assert m.read_document('alice',None) is None",
    },
    'identity-partition': {
        'request': 'Events with the same identifier in different accounts must not suppress one another. Duplicates within one account must still apply once. Preserve the return value and mutate only the provided seen set.',
        'bug': "def apply_event(seen, account, event_id):\n    if event_id in seen:\n        return False\n    seen.add(event_id)\n    return True\n",
        'reference': "def apply_event(seen, account, event_id):\n    key=(account,event_id)\n    if key in seen:\n        return False\n    seen.add(key)\n    return True\n",
        'checks': "s=set(); assert m.apply_event(s,'a',7); assert not m.apply_event(s,'a',7); assert m.apply_event(s,'b',7); assert m.apply_event(s,'a',8); assert not m.apply_event(s,'b',7)",
    },
    'independent-oracle': {
        'request': 'Parse optional feature flags. None uses the supplied default. Accept booleans and the strings true/false after trimming and ignoring case. Reject other strings and non-boolean non-string values with ValueError. Keep the public function signature.',
        'bug': "def parse_flag(value, default=False):\n    return default if value is None else bool(value)\n",
        'reference': "def parse_flag(value, default=False):\n    if value is None:\n        return default\n    if isinstance(value,bool):\n        return value\n    if isinstance(value,str) and value.strip().lower() in ('true','false'):\n        return value.strip().lower() == 'true'\n    raise ValueError('invalid flag')\n",
        'checks': "assert m.parse_flag(None,True) is True; assert m.parse_flag(False) is False; assert m.parse_flag(' FALSE ') is False; assert m.parse_flag('TrUe') is True\nfor bad in ('0','',0,1,[],{}):\n    try: m.parse_flag(bad)\n    except ValueError: pass\n    else: raise AssertionError('invalid flag accepted')",
    },
    'restart-persistence': {
        'request': 'set_value(path, key, value) must survive a fresh Python process. read_value(path, key) returns None for a missing store or key. Preserve unrelated keys; support JSON-compatible values. Work only on the caller-supplied store path.',
        'bug': "_values={}\ndef set_value(path,key,value):\n    _values[key]=value\ndef read_value(path,key):\n    return _values.get(key)\n",
        'reference': "import json\nfrom pathlib import Path\ndef _read(path):\n    p=Path(path)\n    return json.loads(p.read_text()) if p.exists() else {}\ndef set_value(path,key,value):\n    data=_read(path);data[key]=value;Path(path).write_text(json.dumps(data))\ndef read_value(path,key):\n    return _read(path).get(key)\n",
        'checks': None,
    },
}


def prepare(case: str, destination: Path, reference: bool = False) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    record = CASES[case]
    (destination/'TASK.md').write_text(record['request']+'\n',encoding='utf-8')
    (destination/'app.py').write_text(record['reference' if reference else 'bug'],encoding='utf-8')


def tree_snapshot(root: Path, allowed: Path) -> dict[str, tuple]:
    """Capture final state without following symlinks; exclude only the store file."""
    snapshot={}
    for path in sorted(root.rglob('*')):
        if path == allowed:
            continue
        relative=path.relative_to(root).as_posix();info=path.lstat();mode=info.st_mode & 0o7777
        if path.is_symlink():
            snapshot[relative]=('symlink',mode,os.readlink(path))
        elif path.is_dir():
            snapshot[relative]=('directory',mode)
        elif path.is_file():
            snapshot[relative]=('file',mode,hashlib.sha256(path.read_bytes()).hexdigest())
        else:
            snapshot[relative]=('other',mode)
    return snapshot


def grade(case: str, candidate: Path) -> dict:
    # No shell expansion. Candidate code is still arbitrary code, not sandboxed here.
    load = "import importlib.util,sys;from pathlib import Path;spec=importlib.util.spec_from_file_location('candidate',sys.argv[1]);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)\n"
    checks = CASES[case]['checks']
    scripts = [checks] if checks is not None else [
        "p=sys.argv[2];assert m.read_value(p,'missing') is None;m.set_value(p,'a',{'value':3});m.set_value(p,'b',0)",
        "p=sys.argv[2];assert m.read_value(p,'a')=={'value':3};assert m.read_value(p,'b')==0;assert m.read_value(p,'missing') is None",
    ]
    results=[]
    with tempfile.TemporaryDirectory(prefix='r-stack-smoke-sandbox-') as tmp, tempfile.TemporaryDirectory(prefix='r-stack-smoke-markers-') as marker_tmp:
        sandbox=Path(tmp);isolated=sandbox/'candidate';work=sandbox/'work';store=sandbox/'store.json'
        source=candidate/'app.py'
        if not source.is_file() or source.is_symlink():
            raise ValueError('candidate app.py must be a regular file')
        shutil.copytree(candidate,isolated,symlinks=True);work.mkdir()
        baseline=tree_snapshot(sandbox,store)
        for index,assertions in enumerate(scripts):
            marker=Path(marker_tmp)/f'{index}.done';token=secrets.token_hex(32)
            guarded=("_RStackSystemExit=SystemExit\ntry:\n"+
                     textwrap.indent(load+assertions,'    ')+
                     "\nexcept _RStackSystemExit as exc:\n    raise RuntimeError('candidate terminated before assertions completed') from exc\n"+
                     f"Path({str(marker)!r}).write_text({token!r},encoding='utf-8')\n")
            try:
                result=subprocess.run([sys.executable,'-I','-B','-c',guarded,
                                       str((isolated/'app.py').resolve()),str(store)],
                                      cwd=work,capture_output=True,text=True,timeout=5)
                completed=marker.is_file() and marker.read_text(encoding='utf-8') == token
                final=tree_snapshot(sandbox,store)
                unexpected=sorted(key for key in set(baseline)|set(final) if baseline.get(key) != final.get(key))
                if store.exists() and (store.is_symlink() or not store.is_file()):
                    unexpected.append('store.json is not a regular file')
                results.append({'exit_code':result.returncode,'completed_assertions':completed,
                                'unexpected_workspace_mutations':unexpected,'stderr':result.stderr[-2000:]})
            except subprocess.TimeoutExpired:
                results.append({'exit_code':None,'completed_assertions':False,
                                'unexpected_workspace_mutations':[],'stderr':'candidate timed out'})
    return {'case':case,'passed':all(r['exit_code']==0 and r['completed_assertions'] and not r['unexpected_workspace_mutations'] for r in results),'observations':results}


def self_test() -> list[dict]:
    observations=[]
    with tempfile.TemporaryDirectory(prefix='r-stack-fixtures-') as tmp:
        root=Path(tmp)
        for name in CASES:
            broken=root/(name+'-broken');correct=root/(name+'-reference')
            prepare(name,broken);prepare(name,correct,True)
            red=grade(name,broken);green=grade(name,correct)
            if red['passed'] or not green['passed']:
                raise AssertionError(f'fixture failed its negative/positive controls: {name}')
            observations.append({'case':name,'buggy_rejected':True,'reference_accepted':True,'live_model_run':False})
    return observations


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('self-test')
    for command in ('prepare','grade'):
        c=sub.add_parser(command);c.add_argument('case',choices=CASES);c.add_argument('directory',type=Path)
    a=p.parse_args()
    try:
        if a.command=='self-test':result=self_test()
        elif a.command=='prepare':prepare(a.case,a.directory);result={'prepared':str(a.directory),'contains_reference_fix':False}
        else:
            result=grade(a.case,a.directory);print(json.dumps(result,indent=2));return 0 if result['passed'] else 1
    except (OSError,ValueError,AssertionError) as exc:
        print(f'smoke operation failed: {exc}',file=sys.stderr);return 2
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':sys.exit(main())
