---
name: shape
description: Resolve ambiguous engineering intent, domain vocabulary, and dependent product decisions before architecture or implementation. Use when requirements are underspecified, terms conflict, edge behavior is unclear, or several decisions depend on one another.
---

# Shape

Turn ambiguity into decisions without making the operator research the system.
The deliverable is a shaping receipt, not implementation.

1. Restate the problem in your own words. Name the user or caller, the outcome
   they need, the current behavior, and the tension that makes the work nontrivial.
2. Separate known facts, observable unknowns, and genuine decisions. Invoke
   `investigate` or `prototype` for observable unknowns. Do not ask the operator
   to predict code, runtime behavior, feasibility, or performance.
3. Build a decision tree. Put only decisions whose prerequisites are resolved on
   the current frontier. Ask independent frontier questions together; keep
   dependent questions for the next round.
4. Give a recommendation and consequence with every question. Ask for a choice
   only when alternatives express different product intent, risk tolerance, or
   irreversible tradeoffs.
5. Test the emerging shape with concrete scenarios: ordinary use, empty and
   invalid input, retry or interruption, partial failure, concurrency when
   relevant, and the most expensive reversal. Challenge terms that mean
   different things in different scenarios.
6. Record settled decisions with stable identifiers when the work will cross
   sessions or work units. Use the project's existing tracker or canonical
   design document. Keep short-lived decisions in task state; do not create a
   repository document merely to preserve ceremony.
7. Stop when the decision frontier is empty or explicitly deferred and the
   observable acceptance behavior is unambiguous.

Return:

- problem restatement;
- domain terms whose precise meaning matters;
- observed facts with evidence;
- decisions and their identifiers;
- deferred questions and what unlocks them;
- acceptance scenarios;
- recommended next route: `architect`, `plan`, or implementation playbook.

