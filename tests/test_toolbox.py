"""Static isolation checks and actual local log execution; not LLM compliance tests."""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from check_toolbox import check_toolbox, relative_file

spec = importlib.util.spec_from_file_location('decision_log', ROOT / 'skills/show-me-your-work/scripts/log_decision.py')
log = importlib.util.module_from_spec(spec)
spec.loader.exec_module(log)


class ToolboxPolicyTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'payload'
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns('__pycache__'))
    def catalog(self):
        return json.loads((self.root / 'toolbox.json').read_text())
    def save(self, catalog):
        (self.root / 'toolbox.json').write_text(json.dumps(catalog))
    def modify(self, relative, old, new):
        p = self.root / relative
        p.write_text(p.read_text().replace(old, new))
    def rejects(self, phrase):
        self.assertTrue(any(phrase in x for x in check_toolbox(self.root)), check_toolbox(self.root))
    def test_supplied_toolbox_passes(self):
        self.assertEqual(check_toolbox(self.root), [])
    def test_absent_catalog_rejected(self):
        (self.root / 'toolbox.json').unlink(); self.rejects('unreadable')
    def test_nonobject_catalog_rejected(self):
        self.save([]); self.rejects('must be an object')
    def test_nonlist_entries_rejected(self):
        c=self.catalog(); c['utilities']=None; self.save(c); self.rejects('nonempty list')
    def test_nonobject_entry_rejected(self):
        c=self.catalog(); c['utilities'].append([]); self.save(c); self.rejects('must be an object')
    def test_invalid_effect_does_not_crash(self):
        c=self.catalog(); c['utilities'][0]['effect']=[]; self.save(c); self.rejects('invalid kind')
    def test_boolean_schema_rejected(self):
        c=self.catalog(); c['schema_version']=True; self.save(c); self.rejects('unsupported schema')
    def test_missing_requested_skill_rejected(self):
        c=self.catalog(); c['utilities']=c['utilities'][1:]; self.save(c); self.rejects('missing utility entries')
    def test_duplicate_skill_rejected(self):
        c=self.catalog(); c['utilities'].append(c['utilities'][0]); self.save(c); self.rejects('duplicate utility')
    def test_mode_dependency_rejected(self):
        c=self.catalog(); c['utilities'][0]['dependencies']=['r-stack-mode']; self.save(c); self.rejects('core or missing')
    def test_positive_mode_call_in_body_rejected(self):
        p=self.root/'skills/bro/SKILL.md'; p.write_text(p.read_text()+'\nInvoke `r-stack-mode` before responding.\n')
        self.rejects('positive core workflow invocation')
    def test_optional_core_helper_rejected(self):
        c=self.catalog(); c['utilities'][0]['optional_helpers']=['orchestrate']; self.save(c); self.rejects('core or missing')
    def test_indirect_core_dependency_rejected(self):
        c=self.catalog(); c['utilities'][0]['dependencies']=['unslop']; c['utilities'][1]['dependencies']=['r-stack-mode']; self.save(c); self.rejects('core or missing')
    def test_mandatory_cycle_rejected(self):
        c=self.catalog(); c['utilities'][0]['dependencies']=['unslop']; c['utilities'][1]['dependencies']=['bro']; self.save(c); self.rejects('dependency cycle')
    def test_malformed_dependency_rejected(self):
        c=self.catalog(); c['utilities'][0]['dependencies']=[{}]; self.save(c); self.rejects('list of strings')
    def test_hidden_from_model_rejected(self):
        self.modify('skills/bro/SKILL.md','license: MIT','disable-model-invocation: true\nlicense: MIT'); self.rejects('hidden, sticky')
    def test_sticky_mode_rejected(self):
        self.modify('skills/bro/SKILL.md','license: MIT','mode: true\nlicense: MIT'); self.rejects('hidden, sticky')
    def test_preapproved_permissions_rejected(self):
        self.modify('skills/bro/SKILL.md','license: MIT','allowed-tools: Bash\nlicense: MIT'); self.rejects('permission-granting')
    def test_adapter_implicit_disabled_rejected(self):
        self.modify('skills/bro/agents/openai.yaml','allow_implicit_invocation: true','allow_implicit_invocation: false'); self.rejects('implicit invocation')
    def test_missing_boundary_rejected(self):
        self.modify('skills/bro/SKILL.md','Standalone utility. Do not start or resume R-Stack mode','Run whatever mode is useful'); self.rejects('missing standalone boundary')
    def test_entry_exception_missing_rejected(self):
        self.modify('rules/r-stack-workflow.mdc','## Standalone utility exception','## Something else'); self.rejects('missing entry exception')
    def test_lost_wrapper_boundary_rejected(self):
        self.modify('commands/bro.md','Do not start or resume R-Stack mode','Start the workflow'); self.rejects('command wrapper')
    def test_external_skill_link_rejected(self):
        p=self.root/'skills/bro/SKILL.md'; p.write_text(p.read_text()+'\nRead [mode](../r-stack-mode/SKILL.md).\n'); self.rejects('self-contained')
    def test_missing_reference_rejected(self):
        (self.root/'skills/unslop/references/patterns.md').unlink(); self.rejects('reference does not exist')
    def test_all_utilities_have_interaction_cases(self):
        cases=json.loads((ROOT/'evals/toolbox-cases.json').read_text())['cases']
        covered={name for c in cases for name in c['skills']}
        self.assertTrue({e['name'] for e in self.catalog()['utilities']} <= covered)
    def test_small_bro_has_no_tools_or_dependencies(self):
        text=(ROOT/'skills/bro/SKILL.md').read_text()
        self.assertLess(len(text.split()),250)
        self.assertEqual(self.catalog()['utilities'][0]['dependencies'],[])
        self.assertFalse(list((ROOT/'skills/bro').glob('scripts/*')))
    def test_helper_script_exists_and_executable(self):
        path=ROOT/'skills/show-me-your-work/scripts/log_decision.py'
        self.assertTrue(path.is_file()); self.assertTrue(path.stat().st_mode & 0o111)


class DecisionLogTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name); self.path=self.root/'decisions.tsv'
    def append(self, **overrides):
        fields=dict(phase='research',decision='Retain the interface',why='Caller compatibility',evidence='notes/source.md',result='proposed')
        fields.update(overrides); log.append_decision(self.path,**fields)
    def rows(self):
        with self.path.open(newline='',encoding='utf-8') as f:return list(csv.reader(f,delimiter='\t'))
    def test_creates_header_and_real_row(self):
        self.append(); rows=self.rows(); self.assertEqual(rows[0],list(log.HEADER)); self.assertEqual(len(rows),2)
        self.assertRegex(rows[1][0],r'^\d{4}-\d{2}-\d{2}T'); self.assertEqual(rows[1][-1],'proposed')
    def test_append_preserves_existing_bytes(self):
        self.append(); before=self.path.read_bytes(); self.append(result='confirmed'); self.assertTrue(self.path.read_bytes().startswith(before)); self.assertEqual(len(self.rows()),3)
    def test_multiline_and_tabs_are_single_cell(self):
        self.append(decision='one\tvalue\nwith lines\rhere'); self.assertEqual(self.rows()[1][2],'one value with lines here'); self.assertEqual(len(self.rows()[1]),6)
    def test_formula_prefixes_are_quoted(self):
        for value in ('=1+1','+cmd','-1','@SUM(1)', ' \t=1'):
            self.assertTrue(log.clean_cell(value).startswith("'"))
    def test_empty_field_rejected_before_writes(self):
        with self.assertRaises(ValueError): self.append(why='   ')
        self.assertFalse(self.path.exists()); self.assertFalse(self.path.with_suffix('.tsv.lock').exists())
    def test_nonstring_field_rejected(self):
        with self.assertRaises(ValueError):self.append(result=None)
    def test_existing_lock_prevents_change(self):
        lock=self.path.with_name(self.path.name+'.lock'); lock.write_text('another writer')
        with self.assertRaises(FileExistsError):self.append()
        self.assertEqual(lock.read_text(),'another writer'); self.assertFalse(self.path.exists())
    def test_unknown_header_preserved(self):
        self.path.write_text('my data\n')
        with self.assertRaises(ValueError):self.append()
        self.assertEqual(self.path.read_text(),'my data\n'); self.assertFalse(Path(str(self.path)+'.lock').exists())
    def test_bad_row_preserved(self):
        self.append(); self.path.write_text(self.path.read_text()+'broken\trow\n'); before=self.path.read_bytes()
        with self.assertRaises(ValueError):self.append()
        self.assertEqual(self.path.read_bytes(),before)
    def test_incomplete_final_line_rejected(self):
        self.append(); self.path.write_bytes(self.path.read_bytes().rstrip(b'\n'))
        with self.assertRaises(ValueError):self.append()
    def test_symlink_file_rejected(self):
        target=self.root/'original'; target.write_text('private'); self.path.symlink_to(target)
        with self.assertRaises(ValueError):self.append()
        self.assertEqual(target.read_text(),'private')
    def test_symlink_parent_rejected(self):
        target=self.root/'real'; target.mkdir(); alias=self.root/'alias'; alias.symlink_to(target,target_is_directory=True); self.path=alias/'decisions.tsv'
        with self.assertRaises(ValueError):self.append()
    def test_cli_executes_without_repo(self):
        command=[sys.executable,str(ROOT/'skills/show-me-your-work/scripts/log_decision.py'),str(self.path)]
        for field,value in [('phase','analysis'),('decision','Keep data'),('why','Reproducibility'),('evidence','source.txt'),('result','not tested')]:command.extend(['--'+field,value])
        result=subprocess.run(command,capture_output=True,text=True,cwd=self.root)
        self.assertEqual(result.returncode,0,result.stderr); self.assertEqual(self.rows()[1][-1],'not tested')
    def test_invalid_cli_does_not_traceback(self):
        self.path.write_text('foreign data\n')
        result=subprocess.run([sys.executable,str(ROOT/'skills/show-me-your-work/scripts/log_decision.py'),str(self.path),'--phase','a','--decision','b','--why','c','--evidence','d','--result','e'],capture_output=True,text=True)
        self.assertEqual(result.returncode,2); self.assertNotIn('Traceback',result.stderr); self.assertEqual(self.path.read_text(),'foreign data\n')


if __name__=='__main__':unittest.main()
