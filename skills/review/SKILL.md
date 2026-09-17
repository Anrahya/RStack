---
name: review
description: Try to falsify a change against its original intent, surrounding system and claimed proof. Use for consequential changes, contested designs, explicit review requests and final delivery checks.
---

# Review

Pin the comparison point and current artifact. Read the original request,
acceptance contract, project constraints, full relevant diff and callers.
An invalid base is a blocker. An empty diff may be a valid no-op: establish
whether the requested state already exists rather than inventing changes.

Run or inspect deterministic checks first. Separate these review questions:

- **Intent:** Does the artifact satisfy the original request without silently
  changing scope, requirements or protected behavior?
- **Engineering:** What input, lifecycle, state, authority or failure condition
  breaks the behavior? Is ownership understandable and unnecessary complexity
  absent?
- **Proof:** Does each check exercise the changed boundary, assert an independent
  expected result and identify the final relevant artifact?

Use fresh contexts for independent axes when the risk warrants their cost and
the host supports them. Record the actual provenance: **self-review**, **fresh
context with the same executor**, **another executor**, **human review**, or
**deterministic check**. Fresh context reduces priming; it does not guarantee
independent errors. Serial role-play is self-review, not an independent panel.

Do not prime reviewers with a preferred verdict or another reviewer's findings.
For each candidate issue establish the trigger, execution path, observable
consequence, relationship to the change, and counterevidence. Agreement is a
lead; resolve disagreements with a discriminating check, not a vote.

Return `PASS`, `ISSUES`, or `INCONCLUSIVE`, provenance, prioritized supported
findings, dismissals and proof gaps. Do not manufacture findings to fill a quota.
A clean review is valid. Do not edit unless fixes were authorized. When a fix
changes the reviewed artifact, reopen the affected verification gate.
