#!/usr/bin/env python3
"""Validate receipt consistency and captured artifacts, not semantic truth."""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from check_work_graph import check_graph, nonempty, strings, identifier, WORK_ID, ACCEPTANCE_ID
from evidence_io import canonical_json_sha256, load_verified_artifact, workspace_fingerprint

EVIDENCE_ID = re.compile(r'E-[0-9]{3,}\Z')
HASH = re.compile(r'[a-f0-9]{64}\Z')
STATUSES = {'PASS', 'FAIL', 'ISSUES', 'BLOCKED', 'INCONCLUSIVE'}
BASES = {'observed', 'supported-inference', 'proposed', 'unknown'}


def check_receipt(receipt: Any, graph: Any, expected_fingerprint: str | None,
                  evidence_root: Path | None = None, *, structure_only: bool = False) -> list[str]:
    graph_errors = check_graph(graph)
    errors = [f'graph: {e}' for e in graph_errors]
    expected_contract_hash: str | None = None
    if not graph_errors:
        try:
            expected_contract_hash = canonical_json_sha256(graph)
        except (TypeError, ValueError) as exc:
            errors.append(f'graph: canonical contract hash unavailable: {exc}')
    if not isinstance(receipt, dict):
        return errors + ['$: receipt must be an object']
    def err(where: str, message: str) -> None:
        errors.append(f'{where}: {message}')
    if type(receipt.get('schema_version')) is not int or receipt['schema_version'] != 2:
        err('$', 'schema_version must be 2; legacy receipts cannot certify completion')
    receipt_contract_hash = receipt.get('contract_hash')
    if not identifier(receipt_contract_hash, HASH):
        err('$', 'contract_hash must be the canonical graph SHA-256')
    elif expected_contract_hash is not None and receipt_contract_hash != expected_contract_hash:
        err('$', 'receipt is bound to a different work graph')
    wid, status = receipt.get('work_id'), receipt.get('status')
    if not identifier(wid, WORK_ID):
        err('$', 'work_id must match W-###')
    if not isinstance(status, str) or status not in STATUSES:
        err('$', 'invalid status')
    if not nonempty(receipt.get('result')):
        err('$', 'result must be non-empty')
    for field in ('mutations', 'rejected', 'uncertainty', 'handoff'):
        if not strings(receipt.get(field, [])):
            err('$', f'{field} must be a list of non-empty strings')
    if status in ('INCONCLUSIVE', 'BLOCKED') and not receipt.get('uncertainty'):
        err('$', f'{status} must name its uncertainty or blocker')
    evidence = receipt.get('evidence')
    if not isinstance(evidence, list):
        return errors + ['$: evidence must be a list']
    if errors:
        # Do not traverse a malformed graph or invalid identity.
        return errors
    unit = next((u for u in graph['units'] if u['id'] == wid), None)
    if unit is None:
        return [f'$: work_id {wid!r} not found in graph']
    assigned = {a['id']: a for a in unit['acceptance']}
    if status == 'PASS' and not structure_only:
        if not nonempty(expected_fingerprint):
            err('$', 'closing PASS requires a current independently supplied fingerprint')
        if evidence_root is None:
            err('$', 'closing PASS requires evidence_root; use --structure-only for a lint')
    seen: dict[str, dict[str, Any]] = {}
    covered: set[str] = set()
    for i, e in enumerate(evidence):
        where = f'$.evidence[{i}]'
        if not isinstance(e, dict):
            err(where, 'evidence must be an object'); continue
        eid, aid = e.get('id'), e.get('acceptance')
        if not identifier(eid, EVIDENCE_ID) or eid in seen:
            err(where, 'invalid or duplicate evidence id')
        else:
            seen[eid] = e
        if not identifier(aid, ACCEPTANCE_ID) or aid not in assigned:
            err(where, 'evidence refers to an unassigned acceptance claim'); continue
        for field in ('claim', 'action_or_source', 'expected_result', 'observed_result', 'fingerprint'):
            if not nonempty(e.get(field)):
                err(where, f'{field} must be non-empty')
        evidence_contract_hash = e.get('contract_hash')
        if not identifier(evidence_contract_hash, HASH):
            err(where, 'contract_hash must be a canonical graph SHA-256')
        basis, outcome, purpose = e.get('basis'), e.get('outcome'), e.get('purpose')
        if not isinstance(basis, str) or basis not in BASES:
            err(where, 'invalid basis')
        if not isinstance(outcome, str) or outcome not in ('PASS', 'FAIL', 'INCONCLUSIVE'):
            err(where, 'outcome must be PASS, FAIL or INCONCLUSIVE')
        if not isinstance(purpose, str) or purpose not in ('proof', 'support'):
            err(where, 'purpose must distinguish closing proof from historical support')
        if not strings(e.get('limitations', [])) or not strings(e.get('supports', [])):
            err(where, 'limitations and supports must be string lists')
        artifact = e.get('artifact')
        if not isinstance(artifact, dict) or not nonempty(artifact.get('path')) or not identifier(artifact.get('sha256'), HASH):
            err(where, 'artifact needs a relative path and SHA-256')
        closing = status == 'PASS' and purpose == 'proof'
        verify = assigned[aid]['verify']
        if evidence_contract_hash == expected_contract_hash:
            if e.get('claim') != assigned[aid]['predicate']:
                err(where, 'claim differs from the frozen acceptance predicate')
            if e.get('expected_result') != verify['expected']:
                err(where, 'expected_result differs from the frozen acceptance contract')
            if e.get('action_or_source') != verify['action']:
                err(where, 'action_or_source differs from the frozen acceptance contract')
        if closing:
            covered.add(aid)
            if outcome != 'PASS' or basis in ('proposed', 'unknown'):
                err(where, 'closing proof requires a successful observed or supported result')
            if verify['kind'] != 'judgment' and basis != 'observed':
                err(where, 'execution and inspection require observed evidence')
            if e.get('contract_hash') != expected_contract_hash:
                err(where, 'closing proof is bound to a different work graph')
            if not structure_only and e.get('fingerprint') != expected_fingerprint:
                err(where, 'closing proof is stale; another fresh item cannot substitute for it')
        if evidence_root is not None:
            try:
                path = load_verified_artifact(evidence_root, artifact)
                if closing or basis == 'observed':
                    record = json.loads(path.read_text(encoding='utf-8'))
                    if not isinstance(record, dict):
                        raise ValueError('captured record must be an object')
                    for key, expected in (('work_id', wid), ('acceptance', aid), ('evidence_id', eid),
                                          ('kind', verify['kind']), ('contract_hash', evidence_contract_hash),
                                          ('outcome', outcome)):
                        if record.get(key) != expected:
                            raise ValueError(f'captured {key} mismatch')
                    if verify['kind'] == 'execution':
                        if record.get('argv') != verify['argv']:
                            raise ValueError('executed argv differs from the frozen contract')
                        code, completed = record.get('exit_code'), record.get('completed')
                        timed_out, failure = record.get('timed_out'), record.get('failure')
                        if (code is not None and type(code) is not int) or type(completed) is not bool or type(timed_out) is not bool:
                            raise ValueError('captured execution status has invalid types')
                        if failure is not None and not nonempty(failure):
                            raise ValueError('captured failure must be null or a non-empty string')
                        if failure is None:
                            if not completed or timed_out or type(code) is not int:
                                raise ValueError('captured execution status is internally inconsistent')
                            recorded_outcome = 'PASS' if code == 0 else 'FAIL'
                        else:
                            recorded_outcome = 'INCONCLUSIVE'
                        if recorded_outcome != outcome:
                            raise ValueError('evidence outcome differs from captured execution status')
                        observed = f'exit_code={code}; completed={completed}; failure={failure}'
                        if e.get('observed_result') != observed:
                            raise ValueError('observed_result differs from captured execution status')
                        if record.get('fingerprint_before') != e['fingerprint'] or record.get('fingerprint_after') != e['fingerprint']:
                            raise ValueError('inputs changed during the captured run')
                        for field in ('stdout', 'stderr'):
                            load_verified_artifact(evidence_root, record.get(field))
                    else:
                        if record.get('fingerprint') != e['fingerprint']:
                            raise ValueError('inspection/judgment fingerprint mismatch')
                        if record.get('origin') not in ('tool', 'human', 'agent') or not nonempty(record.get('observation')):
                            raise ValueError('inspection/judgment requires explicit origin and observation')
                        if record.get('observation') != e.get('observed_result'):
                            raise ValueError('observed_result differs from captured observation')
                        attachments = record.get('attachments')
                        if not isinstance(attachments, list) or not attachments:
                            raise ValueError('inspection/judgment needs captured source or visual attachments')
                        for attachment in attachments:
                            load_verified_artifact(evidence_root, attachment)
            except (OSError, ValueError, UnicodeError, TypeError, KeyError) as exc:
                err(where, f'artifact check failed: {exc}')
    for eid, e in seen.items():
        if status == 'PASS' and e.get('purpose') == 'proof' and e.get('basis') == 'supported-inference':
            support_ids = e.get('supports')
            if not strings(support_ids) or not support_ids:
                err(eid, 'supported inference needs observed evidence references')
                continue
            for sid in support_ids:
                support = seen.get(sid)
                if (sid == eid or not support or support.get('basis') != 'observed'
                        or support.get('outcome') != 'PASS'
                        or support.get('contract_hash') != expected_contract_hash):
                    err(eid, f'{sid} is not distinct successful observed support under this contract')
    if status == 'PASS' and set(assigned) - covered:
        err('$', f'PASS lacks closing proof for {sorted(set(assigned) - covered)}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('receipt', type=Path)
    parser.add_argument('--graph', type=Path, required=True)
    parser.add_argument('--repo', type=Path)
    parser.add_argument('--expected-fingerprint', help='host-supplied build/live/snapshot identity; not derived from the receipt')
    parser.add_argument('--evidence-root', type=Path)
    parser.add_argument('--structure-only', action='store_true', help='lint only; does not certify a completion claim')
    args = parser.parse_args()
    if args.repo and args.expected_fingerprint:
        parser.error('choose --repo or --expected-fingerprint, not both')
    try:
        receipt = json.loads(args.receipt.read_text(encoding='utf-8'))
        graph = json.loads(args.graph.read_text(encoding='utf-8'))
        expected = workspace_fingerprint(args.repo) if args.repo else args.expected_fingerprint
        errors = check_receipt(receipt, graph, expected, args.evidence_root, structure_only=args.structure_only)
        if args.repo and workspace_fingerprint(args.repo) != expected:
            errors.append('$: workspace changed while checking evidence')
    except (OSError, ValueError, UnicodeError, subprocess.SubprocessError) as exc:
        print(f'receipt input is unreadable: {exc}', file=sys.stderr)
        return 2
    if errors:
        print('receipt rejected:\n' + '\n'.join('- ' + e for e in errors))
        return 1
    if args.structure_only:
        print('receipt structure valid; NOT completion verification')
    else:
        print(f'receipt evidence consistent ({receipt["status"]}); test adequacy, judgment and provenance trust still require review')
    return 0


if __name__ == '__main__':
    sys.exit(main())
