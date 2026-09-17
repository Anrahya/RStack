---
name: architect
description: Design caller-facing types, ownership, failure behavior, and module boundaries before implementation. Use when work creates or moves a public, persistence, process, concurrency, authority, or integration boundary, or when a design is expensive to reverse.
---

# Architect

Design from consumer usage and observed constraints, not from a module diagram.

## Ground

Trace every affected boundary with `investigate`. Separate fixed constraints,
accepted product decisions, observable unknowns, and open preferences. Use
`shape` when domain terms or desired behavior remain unsettled.

## Sketch usage before implementation

Write representative caller or user interactions first. Derive:

- the central data shape and illegal states;
- operations and the smallest useful interface;
- state owner, lifecycle, and concurrency;
- validation and authority boundaries;
- failures, cancellation, retry, idempotency, and cleanup;
- dependency direction and module placement;
- migration shape and compatibility obligations;
- the highest seam that can verify behavior deterministically.

Prefer a deep module whose small interface hides consequential behavior. Do not
create an adapter or abstraction for one implementation unless it enforces a
current invariant.

## Explore consequential forks

When two materially different shapes remain viable and reversal is expensive,
declare three to six gradeable criteria before generating alternatives. Produce
at least two complete, structurally distinct candidates in isolated contexts
under identical requirements. Cosmetic variants do not count.

Use `prototype` for behavior, timing, feasibility, interaction, or
compatibility questions an experiment can settle. Candidates receive the task,
not the desired verdict. Compare them on correctness, ownership, boundary
clarity, invalid states, failure behavior, public surface, reader load,
migration cost, reversibility, and proof.

Pick one coherent base. Graft only compatible, evidenced strengths. If candidates
diverge because the contract was underspecified, re-ground instead of averaging.

## Architecture receipt

Return the consumer usage, data shape, ownership map, interface, invariants,
failure and lifecycle behavior, module boundary, test seam, migration path,
selected candidate, rejected alternatives, and unresolved decision.

During implementation, stop and revisit the shape when two or more independent
workarounds defend the same assumption: repeated casts, optional escape hatches,
leaked internal rules, bypass APIs, or duplicated state repair. One legitimate
edge case is not enough.
