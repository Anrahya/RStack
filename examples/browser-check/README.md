# A browser probe with a real failing control

This synthetic fixture illustrates wheel/drag/resize interactions, pause state,
keyboard focus, reduced-motion emulation and dedicated profile reuse across a
browser restart. It does not exercise Renoa or prove a model used RStack correctly.
The sample uses Playwright Python directly, not agent-browser or Playwright MCP.

Requires an existing authorized Python Playwright installation and compatible
Chromium. This example intentionally does not install packages or modify project
dependencies. On a machine with an approved system Chromium:

```bash
python3 examples/browser-check/check.py --browser-executable "$(command -v chromium)" \
  --output /path/to/private-evidence/fixed
python3 examples/browser-check/check.py --browser-executable "$(command -v chromium)" \
  --output /path/to/private-evidence/broken --broken-control
```

Use new output directories for each run; earlier proof is never overwritten.
The fixed fixture should exit 0. The intentionally broken resize handler should
produce failed behavioral assertions and exit 1. Missing browser/dependencies or
setup failure produce exit 2, which is **not** a successful bug-detection result.
Read the actual results to confirm the failures are the expected ones.

```bash
python3 scripts/assert_results.py /path/to/private-evidence/fixed/results.json \
  --require wheel pan pause focus motion profile
```

The same command on `broken/results.json` must exit 1. Read screenshots before
making visual judgments; assertions on focus/CSS alone do not establish overall
visual quality. This script starts only a loopback fixture server, uses a new
temporary synthetic profile, closes its contexts/server and preserves output.
No real accounts, credentials, production app or public preview are involved.

To adapt the pattern to a real app, replace the fixture controls, expected values
and cases with the original acceptance contract and real inputs. Do not carry the
fixture's IDs/assertions over and claim they cover your application.

## Offline fixture mode

When network policy blocks navigation to a local server, do not bypass that policy.
The optional `--offline` mode loads only this bundled synthetic HTML with
`page.set_content` in an empty browser page. It exercises five in-memory controls,
not server reachability, app integration, login or persistent storage:

```bash
python3 examples/browser-check/check.py --offline \
  --browser-executable "$(command -v chromium)" --output /path/to/private-evidence/offline-fixed
python3 examples/browser-check/check.py --offline --broken-control \
  --browser-executable "$(command -v chromium)" --output /path/to/private-evidence/offline-broken
python3 scripts/assert_results.py /path/to/private-evidence/offline-fixed/results.json \
  --require wheel pan pause focus motion
```

Do not include `profile` in the offline case set: that claim is deliberately not
run. The packaging environment blocked localhost navigation, so only this offline
mode was exercised successfully here. A real host must still test its live app,
MCP/CLI connectivity, screenshot delivery to the model and required persistence.
