#!/usr/bin/env python3
"""Check declared work-graph consistency. This is not a scheduler or sandbox."""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

WORK_ID = re.compile(r"W-[0-9]{3,}\Z")
ACCEPTANCE_ID = re.compile(r"A-[0-9]{3,}\Z")
DECISION_ID = re.compile(r"D-[0-9]{3,}\Z")
KINDS = {"execution", "inspection", "judgment"}
EXECUTOR_KEYS = {"model", "models", "model_name", "reasoning_effort", "pricing"}


def nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def strings(value: Any) -> bool:
    return isinstance(value, list) and all(nonempty(x) for x in value)


def identifier(value: Any, pattern: re.Pattern[str]) -> bool:
    return isinstance(value, str) and pattern.fullmatch(value) is not None


def normalize_path(value: str) -> str:
    """Conservative, portable ownership paths; no globs or parent traversal."""
    if not nonempty(value) or value != value.strip():
        raise ValueError("ownership path must be non-empty without surrounding whitespace")
    if any(x in value for x in ('\\', '\0', '*', '?', '[', ']', ':')):
        raise ValueError("ownership paths must be literal relative POSIX paths")
    p = PurePosixPath(value)
    if p.is_absolute() or value.startswith('~') or '..' in p.parts:
        raise ValueError("absolute paths, home expansion and parent traversal are forbidden")
    return str(p)


def path_conflict(left: str, right: str) -> bool:
    # Case folding intentionally serializes case-only aliases even on Linux.
    a, b = normalize_path(left).casefold(), normalize_path(right).casefold()
    return a == '.' or b == '.' or a == b or a.startswith(b + '/') or b.startswith(a + '/')


def transitive_dependencies(units: dict[str, dict[str, Any]], work_id: str) -> set[str]:
    found: set[str] = set()
    frontier = list(units[work_id]['requires'])
    while frontier:
        item = frontier.pop()
        if item in found or item not in units:
            continue
        found.add(item)
        frontier.extend(units[item]['requires'])
    return found


def check_graph(graph: Any, repo_root: Path | None = None) -> list[str]:
    if not isinstance(graph, dict):
        return ['$: graph must be an object']
    errors: list[str] = []
    def err(where: str, message: str) -> None:
        errors.append(f'{where}: {message}')
    if type(graph.get('schema_version')) is not int or graph['schema_version'] != 2:
        err('$', 'schema_version must be 2; see skills/r-stack-mode/references/evidence-contract.md for migration')
    if not nonempty(graph.get('outcome')):
        err('$', 'outcome must name the original requested result')
    declared = graph.get('acceptance_ids')
    if not isinstance(declared, list) or not declared or not all(identifier(x, ACCEPTANCE_ID) for x in declared):
        err('$', 'acceptance_ids must be a non-empty list of A-### identifiers')
        declared = []
    elif len(set(declared)) != len(declared):
        err('$', 'duplicate acceptance_ids')
    for key in EXECUTOR_KEYS.intersection(graph):
        err('$', f'executor configuration {key!r} belongs to the host')
    raw_units = graph.get('units')
    if not isinstance(raw_units, list) or not raw_units:
        return errors + ['$: units must be a non-empty list']
    units: dict[str, dict[str, Any]] = {}
    owners: dict[str, str] = {}
    decision_ids: set[str] = set()
    decisions = graph.get('decisions', [])
    if not isinstance(decisions, list):
        err('$', 'decisions must be a list')
        decisions = []
    for i, d in enumerate(decisions):
        if not isinstance(d, dict) or not identifier(d.get('id'), DECISION_ID) or not nonempty(d.get('text')):
            err(f'$.decisions[{i}]', 'decision needs D-### id and text')
            continue
        if d['id'] in decision_ids:
            err('$.decisions', f'duplicate decision {d["id"]}')
        decision_ids.add(d['id'])
    for i, raw in enumerate(raw_units):
        where = f'$.units[{i}]'
        if not isinstance(raw, dict) or not identifier(raw.get('id'), WORK_ID):
            err(where, 'unit must be an object with W-### id')
            continue
        wid = raw['id']
        if wid in units:
            err(where, f'duplicate work id {wid}')
            continue
        unit = dict(raw)
        units[wid] = unit
        for key in EXECUTOR_KEYS.intersection(raw):
            err(where, f'executor configuration {key!r} belongs to the host')
        if 'role' in raw and not nonempty(raw['role']):
            err(where, 'role must be a non-empty string when supplied')
        for field in ('outcome', 'authority'):
            if not nonempty(raw.get(field)):
                err(where, f'{field} must be non-empty')
        for field in ('write', 'requires'):
            if not strings(raw.get(field)):
                err(where, f'{field} must be a list of non-empty strings; use [] for none')
                unit[field] = []
        for field in ('context', 'stop_if'):
            if not strings(raw.get(field)) or not raw[field]:
                err(where, f'{field} must be a non-empty list of actionable strings')
                unit[field] = []
        for field in ('read', 'excluded', 'accepted_decisions', 'produces_for', 'write_resources', 'known_facts', 'assumptions_to_test', 'forbidden'):
            if not strings(raw.get(field, [])):
                err(where, f'{field} must be a list of non-empty strings')
                unit[field] = []
        for field in ('write', 'excluded'):
            clean: list[str] = []
            for value in unit.get(field, []):
                try:
                    normalized = normalize_path(value)
                    clean.append(normalized)
                    if repo_root is not None:
                        root = repo_root.resolve()
                        candidate = root / normalized
                        # Symlink aliases are rejected rather than pretending to lock their targets.
                        while candidate != root:
                            if candidate.is_symlink():
                                raise ValueError('symlink ownership needs a host-resolved canonical scope')
                            candidate = candidate.parent
                except ValueError as exc:
                    err(where, f'{field} {value!r}: {exc}')
            unit[field] = clean
        for a in unit['write']:
            for b in unit.get('excluded', []):
                if path_conflict(a, b):
                    err(where, f'write scope {a!r} overlaps excluded scope {b!r}')
        if raw.get('role') in ('investigator', 'reviewer', 'verifier') and (unit['write'] or unit.get('write_resources')):
            err(where, 'read-only role cannot own source or external mutations')
        acceptance = raw.get('acceptance')
        if not isinstance(acceptance, list) or not acceptance:
            err(where, 'acceptance must be a non-empty list')
            continue
        for j, claim in enumerate(acceptance):
            cw = f'{where}.acceptance[{j}]'
            if not isinstance(claim, dict) or not identifier(claim.get('id'), ACCEPTANCE_ID):
                err(cw, 'claim must have an A-### id')
                continue
            aid = claim['id']
            if aid in owners:
                err(cw, f'{aid} already owned by {owners[aid]}')
            owners[aid] = wid
            if not nonempty(claim.get('predicate')):
                err(cw, 'predicate must be non-empty')
            verify = claim.get('verify')
            if not isinstance(verify, dict):
                err(cw, 'verify must be an object')
                continue
            kind = verify.get('kind')
            if not isinstance(kind, str) or kind not in KINDS:
                err(cw, f'verify.kind must be one of {sorted(KINDS)}')
            for field in ('action', 'expected'):
                if not nonempty(verify.get(field)):
                    err(cw, f'verify.{field} must be non-empty')
            if kind == 'execution' and (not strings(verify.get('argv')) or not verify['argv']):
                err(cw, 'execution proof requires exact non-empty verify.argv; no shell interpolation')
    for wid, unit in units.items():
        for dependency in unit['requires']:
            if dependency not in units:
                err(wid, f'unknown dependency {dependency}')
        for decision in unit.get('accepted_decisions', []):
            if decision not in decision_ids:
                err(wid, f'unknown decision {decision}')
    dependencies = {wid: transitive_dependencies(units, wid) for wid in units}
    for wid, deps in dependencies.items():
        if wid in deps:
            err(wid, 'dependency cycle detected')
        for consumer in units[wid].get('produces_for', []):
            if consumer == 'final':
                continue
            if consumer not in units or wid not in dependencies.get(consumer, set()):
                err(wid, f'consumer {consumer!r} must depend on this producer')
    ids = sorted(units)
    for i, left in enumerate(ids):
        for right in ids[i + 1:]:
            if left in dependencies[right] or right in dependencies[left]:
                continue
            for a in units[left]['write']:
                for b in units[right]['write']:
                    if path_conflict(a, b):
                        err('$.units', f'unordered write conflict: {left}:{a} / {right}:{b}')
            shared = set(units[left].get('write_resources', [])) & set(units[right].get('write_resources', []))
            if shared:
                err('$.units', f'unordered external-resource conflict: {sorted(shared)}')
    if set(declared) != set(owners):
        err('$', f'contract coverage mismatch: unassigned={sorted(set(declared)-set(owners))}, undeclared={sorted(set(owners)-set(declared))}')
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('graph', type=Path)
    parser.add_argument('--repo', type=Path, help='also reject existing symlink ownership aliases')
    args = parser.parse_args()
    try:
        graph = json.loads(args.graph.read_text(encoding='utf-8'))
        errors = check_graph(graph, args.repo)
    except (OSError, UnicodeError, ValueError) as exc:
        print(f'graph input is unreadable: {exc}', file=sys.stderr)
        return 2
    if errors:
        print('work graph rejected:\n' + '\n'.join(f'- {e}' for e in errors))
        return 1
    print('work graph consistent; actual authority, locking and scheduling remain host responsibilities')
    return 0


if __name__ == '__main__':
    sys.exit(main())
