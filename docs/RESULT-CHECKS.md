# Make JSON probe results affect the command exit

Prefer assertions in the real test or browser driver. This optional helper only
bridges a structured case report to a failing command; it does not establish that
a reported observation happened, reaches the right boundary, or matches the final
source. A report written by the model is still model-authored.

```json
{
  "schema_version": 1,
  "cases": [
    {"id": "wheel", "status": "PASS", "expected": "User zoom survives resize",
     "observed": "Browser assertion passed at the stated viewport"},
    {"id": "pan", "status": "FAIL", "expected": "User pan survives resize",
     "observed": "Offset reset after the breakpoint transition"}
  ]
}
```

```bash
python3 /path/to/RStack/scripts/assert_results.py results.json --require wheel pan
```

This example must exit 1. Fix the application, rerun the actual probe and then
check the newly produced results. Do not change `FAIL` to `PASS` by hand to close
the task. `--require` comes from the original acceptance contract, not the subset
of cases that happened to run. Exact case coverage is enforced; missing cases,
extra uncontracted cases, FAIL, BLOCKED and NOT_RUN prevent exit 0. Malformed JSON,
duplicate keys/IDs, unsupported fields and invalid types produce exit 2.

A producer must itself fail on exceptions. With a shell, do not hide the producer's
exit status behind `tee`, `|| true` or a following successful command. Keep pipeline
failure propagation enabled where applicable. A stale existing report is not proof
of a new run; use a fresh run directory and preserve the producer's status.

When testing the helper, assert the expected status: 0 for valid complete reports,
1 for scenario/coverage failure, 2 for invalid input. A crash is not a successful
negative test. For browser-native assertions, use the host's supported tool and
inspect its assertion result/error, not merely a successful RPC transport.

The browser example under `examples/browser-check` exercises real wheel, pointer,
resize and keyboard input against a synthetic fixture. It provides an intentionally
broken control. It is not a regression test for the user's application.
