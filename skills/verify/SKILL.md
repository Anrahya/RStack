---
name: verify
description: Check every acceptance claim against the final relevant artifact through the actual consumer or system boundary. Use after changes, before delivery, or when existing checks might provide proxy or stale evidence.
---

# Verify

## Establish the oracle

Read the original acceptance contract and project gates. For each claim, name
the observable result, independently justified expected value, actual boundary
exercised and a condition the check does not cover. A test derived from the same
implementation can reproduce its mistake. Do not weaken assertions, refresh
baselines or remove a protected check simply to obtain green.

Choose the smallest sufficient proof: a user interaction, public API call,
persistence read-back, restart, captured replay, differential comparison,
measurement or source-supported analysis. Compilation is not runtime proof;
a screenshot is not interaction proof; a successful HTTP response is not durable
storage proof. Load the relevant domain lens for material negative paths.

For a bug, preserve an honest failing observation and recheck the original
scenario after the fix. Do not fabricate a red test when the original failure
cannot be reproduced. For a new guardrail, demonstrate that a representative
violation is rejected, restore the intended state and pass again.

## Make the surface reachable

Prefer an existing project harness. When repeated verification has no reliable
entry point, follow [the project-driver recipe](../r-stack-mode/references/project-driver.md).
A generated driver is a draft until its own launch, readiness, drive, evidence
and cleanup steps have been exercised. Test scaffolding must be identified and
must not bypass the changed production boundary.

## Capture final-state evidence

Identify the final worktree, build, deployed revision or live target. Pin the
inputs and relevant environment. Record the command or action, expected and
observed results, output artifacts, coverage limits and identity after the last
relevant edit. Use native tool records where available.

When using R-Stack's optional Python recorder, follow
[the evidence contract](../r-stack-mode/references/evidence-contract.md).
`--structure-only` validates formatting, never completion. Historical failed
runs are useful support, not proof of the final state. Every required claim needs
its own current successful evidence; one fresh check cannot freshen the others.

## Decide

Check the final diff for scope drift and recheck identity after verification.
Any relevant later mutation requires fresh affected checks and the project's
required final gate. Do not blindly rerun unrelated work; explain reused proof.

Return `PASS`, `FAIL`, or `INCONCLUSIVE`, with the acceptance-to-evidence map and
uncovered conditions. Missing browser, credentials, fixtures or a reproducible
failure must remain visible. A blocked check is not an inferred pass. Semantic
adequacy and aesthetic judgment still require inspection; a receipt hash cannot
establish them.
