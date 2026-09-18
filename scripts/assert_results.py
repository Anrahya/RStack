#!/usr/bin/env python3
"""Validate a declared case set and propagate failed observations to the exit status.

This checks reporting, not observation authenticity, source freshness or test adequacy.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

CASE_ID = re.compile(r'[A-Za-z0-9][A-Za-z0-9_.-]{0,79}\Z')
STATUSES = ('PASS', 'FAIL', 'BLOCKED', 'NOT_RUN')
MAX_BYTES = 2 * 1024 * 1024


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def reject_constant(value: str) -> None:
    raise ValueError(f'non-JSON numeric constant: {value}')


def load(path: Path) -> object:
    with path.open('rb') as stream:
        content = stream.read(MAX_BYTES + 1)
    if len(content) > MAX_BYTES:
        raise ValueError('result file exceeds 2 MiB; keep full logs in separate artifacts')
    return json.loads(content.decode('utf-8'), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)


def check(document: object, required: list[str]) -> tuple[int, list[str]]:
    if (not isinstance(required, list) or not required or any(not isinstance(x, str) or not CASE_ID.fullmatch(x) for x in required)
            or len(set(required)) != len(required)):
        return 2, ['--require needs distinct, valid case IDs from the acceptance contract']
    if not isinstance(document, dict) or type(document.get('schema_version')) is not int or document['schema_version'] != 1:
        return 2, ['results must be a schema_version 1 object']
    if set(document) != {'schema_version', 'cases'}:
        return 2, ['result keys must be exactly schema_version and cases']
    cases = document.get('cases')
    if not isinstance(cases, list):
        return 2, ['cases must be a list']
    observed: dict[str, str] = {}
    for index, case in enumerate(cases):
        if not isinstance(case, dict) or set(case) != {'id', 'status', 'expected', 'observed'}:
            return 2, [f'cases[{index}] must contain id, status, expected and observed']
        name = case['id']
        if not isinstance(name, str) or not CASE_ID.fullmatch(name) or name in observed:
            return 2, [f'cases[{index}] has an invalid or duplicate id']
        status = case['status']
        if not isinstance(status, str) or status not in STATUSES:
            return 2, [f'{name}: invalid status; use {STATUSES}']
        if any(not isinstance(case[f], str) or not case[f].strip() for f in ('expected', 'observed')):
            return 2, [f'{name}: expected and observed must be nonempty strings']
        observed[name] = status
    errors = []
    for name in required:
        if name not in observed:
            errors.append(f'{name}: required case did not run')
        elif observed[name] != 'PASS':
            errors.append(f'{name}: {observed[name]}')
    for name in sorted(set(observed) - set(required)):
        errors.append(f'{name}: unexpected case; reconcile the required-case contract')
    return (1, errors) if errors else (0, [f'{len(required)} required case reports are PASS; inspect their evidence separately'])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('results', type=Path)
    parser.add_argument('--require', required=True, nargs='+')
    args = parser.parse_args()
    try:
        status, messages = check(load(args.results), args.require)
    except (OSError, ValueError, UnicodeError, RecursionError) as exc:
        print(f'result input invalid: {exc}', file=sys.stderr)
        return 2
    print('\n'.join(messages), file=sys.stderr if status else sys.stdout)
    return status


if __name__ == '__main__':
    sys.exit(main())
