---
name: orchestrate
description: Decompose non-trivial engineering work into bounded subagent assignments and integrate their evidence and changes. Use when independent investigation, design, implementation, verification, or review lanes can improve latency or confidence.
---

# Orchestrate

Coordinate independent work without giving away the verdict. R-Stack owns the
work graph, roles, scopes, dependencies, write ownership, selection rules,
receipts, synthesis, and integration. The operator or harness owns executor
configuration. Do not add, change, or recommend it.

## Choose the work shape

Keep an atomic task local when coordination costs more than it returns. Use
subagents for independent evidence, falsifiable hypotheses, complete design
alternatives, disjoint vertical implementation units, or independent
verification and review.

Declare one shape before dispatch:

- **partition:** distinct coverage slices, all required;
- **race:** the same outcome through independent attempts;
- **panel:** independent read-only judgments;
- **pipeline:** dependent units that pass an artifact forward.

For a race or panel, predeclare how the coordinator will select or synthesize the
result. For a partition, declare the complete coverage set. Do not turn a serial
trace into parallel work.

## Build the graph

Use stable identifiers when work crosses contexts:

- `D-###` for a consequential decision;
- `A-###` for an acceptance claim;
- `W-###` for a work unit;
- `E-###` for evidence.

The minimum trace is `A -> W -> E`; link a decision to every acceptance claim
or work unit it constrains. Settle shared decisions and integration contracts
before dependent implementation. A unit is ready only when its dependencies and
accepted decisions are current.

Partition by evidence question, state owner, or observable vertical boundary.
Every mutable path, branch, key, live resource, or external object has one writer
at a time. Overlapping read-only scopes are allowed.

## Write standalone briefs

Every worker brief contains these non-empty fields:

- `WORK_ID` and `ROLE`;
- `OUTCOME` and `PARENT_OUTCOME`;
- `READ`, `WRITE`, and `EXCLUDED` scope;
- focused `CONTEXT` pointers;
- `ACCEPTED_DECISIONS`, `KNOWN_FACTS`, and `ASSUMPTIONS_TO_TEST`;
- `REQUIRES` and `PRODUCES_FOR` dependencies;
- exact mutation `AUTHORITY`;
- independently decidable `ACCEPTANCE` claims;
- an exact `VERIFY` action and expected result per claim;
- `STOP_IF`, task-specific `FORBIDDEN` actions, and `REPORT` shape.

Use `NONE` rather than silently omitting a field. Give workers file, symbol,
commit, issue, or artifact pointers instead of raw transcript dumps. Never leak
the preferred verdict into investigation, design, or review briefs.

Read [the worker contract](references/worker-contract.md) for the canonical
template and receipt. For deliberate or program work, validate saved briefs with
`python3 scripts/check_work_graph.py <graph.json>` from the plugin root before
dispatch.

## Pilot and dispatch

For a large program or repeated novel unit shape, push one representative unit
through brief, execution, receipt, integration, and proof before scaling. Fix the
contract from pilot evidence. A handful of obvious independent units does not
need a ceremonial pilot.

Dispatch all ready independent units together. Refill capacity as units finish
instead of waiting for barrier batches. Treat completion as a queue event; finish
the coordinator's current critical operation before draining results. Stop or
re-ground a unit when its dependency fingerprint or accepted decision changes.

If subagents are unavailable, execute the same graph in dependency order and
produce the same receipts.

## Accept evidence receipts

Each unit returns `PASS`, `ISSUES`, `BLOCKED`, or `INCONCLUSIVE`, plus:

- result;
- one `E-###` entry per acceptance claim with basis, action or source,
  observed result, artifact location, and exact fingerprint;
- mutations made;
- rejected hypotheses or alternatives and counterevidence;
- remaining uncertainty;
- integration requirement or exact next action.

`PASS` is invalid when an acceptance claim lacks evidence. A report is
navigation, not proof. The coordinator opens cited artifacts, checks commands or
observations, and inspects every accepted diff. Resolve disagreement with a
discriminating check or prototype, never a vote.

## Integrate and close

Integrate in dependency order and recheck shared assumptions on the converged
tree. Account for every dispatched unit as accepted, rejected, blocked,
inconclusive, or abandoned. A missing worker is a coverage gap, not permission
to imply completion.

Invoke `verify` on the final artifact and `review` when the active playbook
requires it. The coordinator owns the final claim and reports incomplete lanes,
stale receipts, integration changes, and uncovered risk.
