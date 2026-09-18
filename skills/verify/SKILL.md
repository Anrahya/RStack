---
name: verify
description: "Check every acceptance claim on the final relevant artifact through the real consumer boundary. Distinguish current observations, executable checks and maintained regression coverage."
---

# Verify

## Establish the expected result

Read the original acceptance contract and applicable project gates. For each
claim, name its independently justified expected result, actual boundary and
uncovered conditions. Do not weaken assertions, refresh a baseline or remove a
protected check just to obtain green. A test based on the same implementation can
repeat its mistake. For several defects, account for each separately.

Load [UI behavior guidance](../r-stack-mode/references/lenses/ui-ux.md) for changed
gestures, resizing, focus, motion, loading/error states or visuals. Use its behavior
section for repairs; do not demand new visual directions for an unchanged design.
For durability, concurrency or authorization, load the corresponding
[domain guidance](../r-stack-mode/references/lenses/README.md).

Choose the smallest sufficient observation: public API, user interaction,
persistence read-back, restart, replay, differential comparison or measurement.
Compilation is not runtime proof; a screenshot is not interaction proof; HTTP 200
is not proof of durable storage. Test the actual gesture, not a convenient proxy.
Preserve honest failing evidence for bugs and disclose reconstructed baselines.

## Reach the behavior

Use maintained tests where they reach the changed boundary. A working test suite
may cover only some claims. For the rest, use an authorized one-off script or the
host's existing browser/runtime controller without automatically adding a project
dependency. State the borrowed tooling, its resolved version and reproducibility
limits. A new maintained driver needs scope and policy support, not a blanket
requirement to construct a framework. If no safe capability reaches a claim,
leave that claim unverified. See the [driver recipe](../r-stack-mode/references/project-driver.md).

Before browser work, inspect available tools. Keep one owned browser session
through the interactions; do not rebuild the browser per step. Confirm the target
URL, expected app/build, readiness and test identity; a responding unrelated
process is not the target. Existing host browser tools take precedence over
improvised cache imports. Where browser control is missing, the optional
[browser setup guide](../../docs/BROWSER-SETUP.md) covers agent-browser and
Playwright MCP. No tool is installed merely by reading this skill.

## Make checks fail meaningfully

An executable gate must return failure when a required assertion fails, a required
case did not run or setup failed. Printing JSON with a false result while exiting
successfully is diagnostic output, not an executable pass/fail gate. Such output
can support an honestly labeled inspected observation; it must not be recorded as
a passing test merely because its process exited zero.

Use the test framework's assertions or a thrown assertion in a script. Before
trusting a new gate, demonstrate that a known failing condition makes it fail;
restore the intended state and pass again. A setup crash alone does not prove
that the assertion detects the bug. In MCP, inspect tool errors and assertion
results; transport-level success does not mean the scenario passed.

For small JSON-only probes, the optional
[result checker](../../docs/RESULT-CHECKS.md) can enforce an explicit required-case
set and command failure. It cannot determine whether observations are truthful or
the assertions are adequate. Do not substitute synthetic events, internal setters
or mocks for the changed production boundary without disclosing that limit.

## Capture and close

Pin the final worktree/build or live target and relevant environment. For every
required claim record the action, expected and observed result, artifact location
and coverage boundary. Inspect visual evidence when making visual claims; saving
an image without viewing it is not visual inspection. Record the viewport, browser
and interaction. Keep sensitive profiles, credentials and unrelated page data out
of public evidence.

Every required claim needs its own current successful evidence; one fresh check
cannot freshen the others. A later relevant mutation requires affected checks
again and the project's mandatory final gate. Inspect the final diff for scope
and account for failures without hiding them. Optional Python capture follows
[the evidence contract](../r-stack-mode/references/evidence-contract.md);
`--structure-only` never establishes completion.

Stop only processes and scratch instances created by this run. Do not close a
user-owned persistent browser, kill by process name, or delete a profile to make
a test pass. A deliberately retained session needs an explicit ownership/handoff
and lifetime; otherwise close your session after proof. Confirm evidence survives
cleanup and name temporary retention limits.

Return `PASS`, `FAIL` or `INCONCLUSIVE` with claim-to-evidence coverage. Separately
report maintained regression tests, one-off executable checks and inspected
observations. A one-off pass can prove a current scenario without protecting
future changes. Missing required regression coverage remains a failure when the
project requires it. State review type, cleanup status and unavailable checks;
record consistency, oracle quality and aesthetic judgment are different things.
