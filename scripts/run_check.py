#!/usr/bin/env python3
"""Execute one authorized, frozen check and capture its result outside the repo."""
from __future__ import annotations

import argparse
import json
import math
import os
import platform
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from check_work_graph import check_graph
from check_receipt import EVIDENCE_ID
from evidence_io import canonical_json_sha256, sha256_file, workspace_fingerprint, write_json


def terminate(process: subprocess.Popen[bytes]) -> None:
    try:
        if os.name == 'posix':
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
    except ProcessLookupError:
        pass
    process.wait(timeout=10)


def run_check(graph: dict, work_id: str, acceptance: str, evidence_id: str,
              repo: Path, evidence_root: Path, timeout: float = 120.0,
              max_log_bytes: int = 16 * 1024 * 1024) -> dict:
    errors = check_graph(graph, repo)
    if errors:
        raise ValueError('; '.join(errors))
    if not isinstance(evidence_id, str) or not EVIDENCE_ID.fullmatch(evidence_id):
        raise ValueError('evidence id must match E-###')
    if not math.isfinite(timeout) or timeout <= 0 or type(max_log_bytes) is not int or max_log_bytes <= 0:
        raise ValueError('timeout and max_log_bytes must be positive')
    root = repo.resolve(strict=True)
    destination = evidence_root.resolve()
    if destination == root or root in destination.parents:
        raise ValueError('evidence root must be outside the repository')
    unit = next((u for u in graph['units'] if u['id'] == work_id), None)
    if unit is None:
        raise ValueError('unknown work id')
    claim = next((a for a in unit['acceptance'] if a['id'] == acceptance), None)
    if claim is None or claim['verify']['kind'] != 'execution':
        raise ValueError('this runner supports execution claims only')
    verify = claim['verify']
    contract_hash = canonical_json_sha256(graph)
    before = workspace_fingerprint(root)
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / evidence_id
    output.mkdir()  # No overwrite, no reuse of a previous observation.
    start = datetime.now(timezone.utc).isoformat()
    begin = time.monotonic()
    timed_out = False
    failure: str | None = None
    code: int | None = None
    completed = False
    process = None
    with (output / 'stdout.txt').open('xb') as stdout, (output / 'stderr.txt').open('xb') as stderr:
        try:
            process = subprocess.Popen(verify['argv'], cwd=root, stdin=subprocess.DEVNULL,
                                       stdout=stdout, stderr=stderr, shell=False,
                                       start_new_session=os.name == 'posix')
            while process.poll() is None:
                if time.monotonic() - begin > timeout:
                    timed_out = True; failure = 'timeout'; terminate(process); break
                if stdout.tell() + stderr.tell() > max_log_bytes:
                    failure = 'log limit exceeded'; terminate(process); break
                time.sleep(0.02)
            code = process.wait(timeout=10)
            if os.name == 'posix':
                try:
                    os.killpg(process.pid, 0)
                except ProcessLookupError:
                    pass
                else:
                    terminate(process)
                    failure = failure or 'check left a process group alive'
            completed = failure is None
            if stdout.tell() + stderr.tell() > max_log_bytes:
                failure = 'log limit exceeded'; completed = False
        except OSError as exc:
            failure = f'command execution failed: {exc}'
        finally:
            if process is not None and process.poll() is None:
                terminate(process)
    try:
        after = workspace_fingerprint(root)
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        after = None; failure = f'post-run snapshot unavailable: {exc}'
    if before != after:
        failure = failure or 'repository inputs changed during verification'
    status = 'PASS' if completed and code == 0 and not failure else ('INCONCLUSIVE' if failure else 'FAIL')
    record = {
        'schema_version': 2, 'kind': 'execution', 'origin': 'runner',
        'work_id': work_id, 'acceptance': acceptance, 'evidence_id': evidence_id,
        'contract_hash': contract_hash, 'outcome': status,
        'argv': verify['argv'], 'cwd': str(root), 'started_at': start,
        'finished_at': datetime.now(timezone.utc).isoformat(),
        'elapsed_seconds': round(time.monotonic() - begin, 6),
        'exit_code': code, 'completed': completed, 'timed_out': timed_out,
        'failure': failure, 'fingerprint_before': before, 'fingerprint_after': after,
        'environment': {'platform': platform.platform(), 'python': platform.python_version()},
        'stdout': {'path': f'{evidence_id}/stdout.txt', 'sha256': sha256_file(output / 'stdout.txt')},
        'stderr': {'path': f'{evidence_id}/stderr.txt', 'sha256': sha256_file(output / 'stderr.txt')},
    }
    write_json(output / 'run.json', record)
    evidence = {
        'id': evidence_id, 'acceptance': acceptance, 'claim': claim['predicate'],
        'basis': 'observed', 'outcome': status, 'purpose': 'proof',
        'action_or_source': verify['action'], 'expected_result': verify['expected'],
        'observed_result': f'exit_code={code}; completed={completed}; failure={failure}',
        'fingerprint': before, 'contract_hash': contract_hash,
        'artifact': {'path': f'{evidence_id}/run.json', 'sha256': sha256_file(output / 'run.json')},
        'limitations': ['Exit success proves only the assertions implemented by the frozen check.'],
    }
    write_json(output / 'evidence.json', evidence)
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('graph', type=Path)
    parser.add_argument('--work', required=True)
    parser.add_argument('--acceptance', required=True)
    parser.add_argument('--id', required=True)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('--evidence-root', required=True, type=Path)
    parser.add_argument('--timeout', type=float, default=120)
    parser.add_argument('--max-log-bytes', type=int, default=16 * 1024 * 1024)
    args = parser.parse_args()
    try:
        graph = json.loads(args.graph.read_text(encoding='utf-8'))
        evidence = run_check(graph, args.work, args.acceptance, args.id, args.repo,
                             args.evidence_root, args.timeout, args.max_log_bytes)
    except (OSError, ValueError, UnicodeError, subprocess.SubprocessError) as exc:
        print(f'check not recorded: {exc}', file=sys.stderr)
        return 2
    print(json.dumps(evidence, indent=2))
    return 0 if evidence['outcome'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
