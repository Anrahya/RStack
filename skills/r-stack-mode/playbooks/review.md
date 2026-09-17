# Review

Use when the deliverable is a verdict on an existing change. Stay read-only
unless fixes are separately requested.

1. **Pin.** Resolve the fixed comparison point, exact head or workspace
   fingerprint, intended outcome, acceptance claims, protected behavior, project
   rules, and claimed verification. Fail early on an invalid or empty scope.
2. **Check mechanics.** Run or inspect existing deterministic checks first.
   Record failures directly; do not spend prose review rediscovering what tooling
   already proves.
3. **Split axes.** Invoke `review`. For deliberate risk, use isolated contexts:
   intent review checks requested behavior, scope, and acceptance; engineering
   review checks correctness, failures, ownership, security, cleanup,
   maintainability, and project standards; proof review checks whether evidence
   reaches the changed boundary and is fresh.
4. **Validate findings.** For each candidate issue, establish trigger, execution
   path, consequence, changed cause, and counterevidence. Reviewer agreement is a
   lead, not proof. Do not expose one reviewer's findings to another before both
   finish.
5. **Close.** Return `PASS`, `ISSUES`, or `INCONCLUSIVE`; prioritized
   evidenced findings; dismissed hypotheses; deterministic results; and proof
   gaps. Reviewers do not auto-fix.
