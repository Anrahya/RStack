---
name: review
description: Independently try to falsify an engineering change against its intent, project rules, callers, and real behavior. Use for elevated-risk changes, contested designs, pre-delivery review, or explicit requests for skeptical code review.
---

# Review

Review the final diff and surrounding system. Do not reward complexity or produce
findings to fill a quota.

## Pin scope and evidence

Resolve the fixed comparison point, exact head or workspace fingerprint,
original outcome, acceptance claims, protected behavior, project rules, and
claimed proof. Inspect the full diff and relevant callers. Fail early when the
base is invalid or the requested diff is empty.

Run or inspect existing deterministic checks first. Report their failures
directly; do not restate mechanically enforced rules as speculative prose.

## Separate review axes

For deliberate work, use fresh isolated contexts so one axis does not prime the
others:

- **Intent:** requested outcome, acceptance coverage, protected behavior, scope,
  caller-visible semantics, and unrequested behavior.
- **Engineering:** correctness, ownership, state transitions, failure and
  recovery, concurrency, authority, security, cleanup, maintainability, project
  standards, and tests.
- **Proof:** whether claimed evidence exercises the changed boundary, asserts the
  relevant result, matches the final fingerprint, and covers negative paths.

Do not reveal one reviewer's findings to another before both finish. The harness
supplies executor configuration.

## Prove or dismiss findings

For each candidate issue, establish:

1. the triggering input or state;
2. the execution path;
3. the observable consequence;
4. why the reviewed change introduced or failed to prevent it;
5. validation, recovery, tests, or caller behavior that could disprove it.

Agreement among reviewers increases attention, not truth. The coordinator checks
the cited path and evidence, deduplicates related findings, and classifies each as
blocking, actionable, consider, pre-existing, or dismissed. Challenge proposed
remedies; when the safe fix is not established, describe the behavior that must
change.

Return `PASS`, `ISSUES`, or `INCONCLUSIVE`, followed by deterministic
results, separate axis findings, evidence, dismissals, and proof gaps. A clean
review is valid. Do not edit unless the user separately requested fixes.
