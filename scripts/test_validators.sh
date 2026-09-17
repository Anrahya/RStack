#!/usr/bin/env bash
set -euo pipefail

script_dir=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
fixture_dir="$script_dir/fixtures"

python3 "$script_dir/check_work_graph.py" "$fixture_dir/valid-graph.json"

if python3 "$script_dir/check_work_graph.py" "$fixture_dir/invalid-graph.json" \
  >/dev/null 2>&1; then
  printf 'invalid graph unexpectedly passed\n' >&2
  exit 1
fi

python3 "$script_dir/check_receipt.py" \
  "$fixture_dir/valid-receipt.json" \
  --graph "$fixture_dir/valid-graph.json" \
  --expected-fingerprint tree-abc

if python3 "$script_dir/check_receipt.py" \
  "$fixture_dir/invalid-receipt.json" \
  --graph "$fixture_dir/valid-graph.json" >/dev/null 2>&1; then
  printf 'invalid receipt unexpectedly passed\n' >&2
  exit 1
fi

printf 'validator negative fixtures rejected as expected\n'
