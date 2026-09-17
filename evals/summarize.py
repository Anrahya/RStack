#!/usr/bin/env python3
"""Descriptive paired summaries only; no invented trials or significance claims."""
from __future__ import annotations
import argparse
import json
import math
from pathlib import Path
import sys


def summarize(rows: list[dict]) -> dict:
    if not isinstance(rows,list) or not rows:
        raise ValueError('results must be a non-empty list')
    arms={};seen=set()
    for row in rows:
        if not isinstance(row,dict):raise ValueError('each result must be an object')
        for key in ('task','run','arm'):
            if not isinstance(row.get(key),str) or not row[key].strip():raise ValueError(f'missing {key}')
        key=(row['task'],row['run'],row['arm'])
        if key in seen:raise ValueError(f'duplicate result: {key}')
        seen.add(key)
        for field in ('clean','severe_failure'):
            if type(row.get(field)) is not bool:raise ValueError(f'{field} must be boolean')
        if row['clean'] and row['severe_failure']:raise ValueError('a severe failure cannot be a clean completion')
        cost=row.get('cost')
        if cost is not None and (type(cost) not in (int,float) or not math.isfinite(cost) or cost<0):raise ValueError('cost must be finite, non-negative or null')
        if cost is not None and (not isinstance(row.get('currency'),str) or not row['currency']):raise ValueError('known cost needs a currency')
        arms.setdefault(row['arm'],[]).append(row)
    pairs=[{(r['task'],r['run']) for r in group} for group in arms.values()]
    if any(keys!=pairs[0] for keys in pairs[1:]):raise ValueError('arms have missing or unmatched task/run pairs')
    currencies={r['currency'] for r in rows if r.get('cost') is not None}
    if len(currencies)>1:raise ValueError('convert costs to one declared currency before aggregation')
    result={}
    for arm,group in sorted(arms.items()):
        successes=sum(r['clean'] for r in group)
        known=all(r.get('cost') is not None for r in group)
        total=sum(r['cost'] for r in group) if known else None
        result[arm]={'attempts':len(group),'distinct_tasks':len({r['task'] for r in group}),'clean_completions':successes,'clean_rate':successes/len(group),'severe_failures':sum(r['severe_failure'] for r in group),'total_cost':total,'cost_per_clean_completion':total/successes if total is not None and successes else None}
    return {'arms':result,'currency':next(iter(currencies),None),'inference':'Descriptive only. Cluster uncertainty by task; no promotion or statistical claim is computed.'}


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('results',type=Path);a=p.parse_args()
    try:result=summarize(json.loads(a.results.read_text(encoding='utf-8')))
    except (OSError,ValueError,TypeError,KeyError) as exc:print(f'results rejected: {exc}',file=sys.stderr);return 2
    print(json.dumps(result,indent=2));return 0


if __name__=='__main__':sys.exit(main())
