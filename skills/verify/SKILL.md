---
name: verify
description: Prove an engineering outcome against the final workspace using the affected user, delivery, persistence, integration, or performance path. Use after implementation, before handoff, or whenever a passing test may not cover the consequential behavior.
---

# Verify

Derive proof from the task contract and project instructions. Verification is a
claim-to-evidence mapping, not a command dump.

## Pin the artifact

Identify the final tree, worktree content fingerprint, build, deployed revision,
or live-state identity and the last relevant mutation. Earlier checks remain
supporting evidence but cannot prove a later state.

## Build the proof map

Map every `A-###` acceptance claim and protected behavior to the strongest
practical check:

- user or delivery path for observable behavior;
- read-back after persistence;
- retry, duplicate delivery, cancellation, or restart for durable behavior;
- recorded input replay for parsing and migration;
- frozen baseline and final measurement for performance;
- focused tests for local branches, followed by required project gates.

Call code the way its real consumer does and compare against an independently
known result. A helper test cannot prove a boundary it bypasses. Compilation is
not runtime evidence.

For a bug, retain failing-then-passing evidence and rerun the original
unminimized scenario. Reconcile the proof map with the contract's behavior
partitions: require an unchanged control and every materially different
transition, not just the reported example. For a new guardrail, prove it bites:
pass, introduce one representative violation, observe failure, remove the
violation, pass again.

## Drive and capture

Prefer the project's existing harness. If no repeatable path reaches a recurring
consequential surface, create the smallest project-local launch, doctor, drive,
evidence, and cleanup recipe allowed by project policy, then execute it once
before trusting it.

Capture for every claim:

- `E-###` identifier;
- command or action and relevant input;
- expected signal and observed result;
- artifact or evidence location;
- exact fingerprint;
- coverage boundary and uncovered condition.

Clean up only the processes and scratch state created by the run. Preserve proof
artifacts.

## Freshness gate

Recheck the workspace or live identity after validation. Any later mutation
invalidates affected receipts. Rerun only the checks whose inputs changed, plus
the project's required final gate.

Return `PASS`, `FAIL`, or `INCONCLUSIVE` with the proof map. `INCONCLUSIVE`
means a named claim remains unproven; it does not imply the work is safe to
deliver. Never report broader coverage than the evidence demonstrates.
