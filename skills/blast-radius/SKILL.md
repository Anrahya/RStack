---
name: blast-radius
description: "Assess what a proposed code, API, configuration or schema change could break beyond its diff. Report evidence and untested assumptions."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: read-only
---

# Blast radius

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Stay focused on the named change and its dependents. Inspect the actual diff or
proposal, its comparison point and relevant consumers. An absent diff does not
justify choosing an arbitrary base or pretending a change exists.

Find the assumptions that make the change safe. There may be more than one. Trace
beyond symbol references: serialized data, persisted rows, external consumers,
library behavior at the installed version, feature flags, ordering, retries,
lifecycle and cross-language boundaries. Separate current callers from hypothetical
future ones. Prioritize plausible consequential paths, not a long list of maybes.

For each important risk, establish the triggering state, execution path and
observable consequence. Inspect validation, recovery and caller behavior that could
disprove it. A static trace, an executed check and a running-app reproduction provide
different evidence; label which you actually have. Do not invent probability values.

Use existing safe checks or an authorized isolated probe to challenge the key
assumptions. Do not edit production code, add a permanent test suite, reset a branch
or touch live systems under a review-only request. Missing runtime access leaves an
assumption untested rather than "safe". Use optional independent review only when it
adds a distinct question; neither agreement nor a panel is proof.

Return what changes, the key safety assumptions, evidenced risks, checked-and-cleared
paths and the smallest useful next check. Preserve uncertainty. No automatic fix,
architecture workflow, PR, merge or mandatory prose-cleaning pass.
