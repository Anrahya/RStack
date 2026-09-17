---
name: tdd
description: "Use a failing-test-first loop for an explicitly requested feature or bug fix, or a bounded task with a useful existing test seam."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: scoped-edit
---

# Test-first development

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Make intended behavior executable before changing implementation. A question about
TDD is answered as a question; it does not authorize file edits.

For authorized implementation, inspect the expected behavior, current consumer and
existing test path. Choose a narrow check that exercises the relevant public or
observable boundary. Derive the expected value from a requirement, known example
or independent result, not by reimplementing the code inside the assertion.

Work in small vertical cycles. Write one useful failing check, run it, confirm that
it fails for the intended reason, make the smallest implementation change, then
rerun it. A syntax error, missing dependency or disconnected test is not evidence
that the behavior was reproduced. Check a materially different case or an unchanged
control when the same bug could hide there.

Keep existing assertions and oracles intact unless the required behavior genuinely
changed. Do not rewrite a test merely to make the implementation green. Use mocks
at genuine unavailable external boundaries, not to remove the behavior being tested.

If implementation already exists, characterize and verify honestly. A regression
check run against a safe baseline or isolated copy can establish red/green evidence;
never reset or overwrite user-owned work to manufacture a red run. Label checks
written after the fix accordingly.

When a good failing test is impractical, explain the obstacle and use a useful
script, replay or authorized observed scenario instead. Do not create broad test
infrastructure solely for ceremony or say TDD was completed without a demonstrated
red state. Run relevant adjacent checks after the final edit and report exactly
which red and green observations exist. No automatic mode, commit or PR.
