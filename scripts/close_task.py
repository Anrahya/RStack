#!/usr/bin/env python3
"""Assemble explicitly selected observations and test the completion predicate."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

from check_receipt import check_receipt, EVIDENCE_ID
from evidence_io import canonical_json_sha256, safe_artifact, workspace_fingerprint, write_json


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('graph', type=Path)
    p.add_argument('--work', required=True)
    p.add_argument('--result', required=True)
    p.add_argument('--repo', type=Path, required=True)
    p.add_argument('--evidence-root', type=Path, required=True)
    p.add_argument('--ids', nargs='+', required=True, help='explicit E-### ids, never implicit latest-run selection')
    p.add_argument('--output', type=Path, required=True, help='new receipt file outside the repository')
    a = p.parse_args()
    try:
        repo = a.repo.resolve(strict=True)
        output = a.output.resolve()
        if output == repo or repo in output.parents:
            raise ValueError('receipt output must be outside the repository')
        if len(a.ids) != len(set(a.ids)) or not all(EVIDENCE_ID.fullmatch(eid) for eid in a.ids):
            raise ValueError('ids must be unique E-### identifiers')
        graph = json.loads(a.graph.read_text(encoding='utf-8'))
        evidence = [json.loads(safe_artifact(a.evidence_root, f'{eid}/evidence.json').read_text(encoding='utf-8')) for eid in a.ids]
        fingerprint = workspace_fingerprint(repo)
        receipt = {'schema_version': 2, 'contract_hash': canonical_json_sha256(graph),
                   'work_id': a.work, 'status': 'PASS', 'result': a.result,
                   'evidence': evidence, 'uncertainty': []}
        errors = check_receipt(receipt, graph, fingerprint, a.evidence_root)
        if workspace_fingerprint(repo) != fingerprint:
            errors.append('workspace changed during close')
        if errors:
            receipt['status'] = 'INCONCLUSIVE'
            receipt['result'] = 'Requested completion was not accepted.'
            receipt['uncertainty'] = errors
        output.parent.mkdir(parents=True, exist_ok=True)
        write_json(output, receipt)
    except (OSError, ValueError, UnicodeError, subprocess.SubprocessError) as exc:
        print(f'close failed: {exc}', file=sys.stderr)
        return 2
    if errors:
        print('completion rejected:\n' + '\n'.join('- ' + e for e in errors))
        return 1
    print('completion evidence consistent; semantic adequacy and independent review are not certified')
    return 0


if __name__ == '__main__':
    sys.exit(main())
