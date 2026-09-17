---
name: orchestrate
description: Decompose work into independently verifiable units with explicit dependencies and exclusive write ownership, then integrate actual artifacts. Use when parallel investigation, alternatives, implementation or review earns its coordination cost.
---

# Orchestrate

Keep an atomic task local. Declare the reason for coordination: distinct
coverage, elapsed-time reduction, an independent hypothesis or a consequential
alternative. A serial trace is not made parallel by assigning it several agents.
The host owns executors, capacity, permissions, isolation and resource limits.

Choose **partition** (all coverage slices required), **race** (alternative
attempts with a predeclared selection rule), **panel** (separate read-only
judgments), or **pipeline** (dependent artifacts). A race is not majority voting.

Settle shared decisions and interfaces before downstream writes. Assign each
mutable path or external resource one active writer. Give every unit an outcome,
readable context pointers, write scope, dependencies, authority, acceptance and
proof, plus stop conditions. Add other fields only when they change execution.
For machine-checked graphs use [the worker contract](references/worker-contract.md).
Stable `D-###`, `A-###`, `W-###`, `E-###` identifiers support cross-context state;
a tiny read-only delegation may use an equivalent compact brief.

Before dispatch, check graph consistency with `scripts/check_work_graph.py`.
This validates declarations; it does not acquire locks or enforce permissions.
The host must isolate worktrees/resources or serialize owners. Explicitly bind
all original acceptance claims to units; an omitted requirement is not a smaller
successful task.

Pilot one representative unit before scaling a novel repeated pattern. Skip a
ceremonial pilot for a few obvious independent units. Dispatch only ready work;
stop or re-ground it when accepted decisions or dependency inputs change.
If no subagents are available, execute serially and label review independence
honestly. Do not simulate concurrency or independent judgment in prose.

Accept a worker result only after inspecting its cited artifacts and accepted
diff. Reports are navigation. Record every unit as accepted, rejected, blocked,
inconclusive or abandoned. Missing results are coverage gaps. Integration may
invalidate otherwise valid local checks: run final proof on the converged tree.

The coordinator owns the final verdict. Invoke `verify` and the review required
by the active risk policy. Report rejected attempts, integration changes, stale
evidence and remaining uncovered claims, not merely the number of agents used.
