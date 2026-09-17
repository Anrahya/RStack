---
name: show-me-your-work
description: "Explain decisions and evidence, or keep an explicitly requested decision log. A reviewable rationale, not a hidden reasoning transcript."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: scoped-write
---

# Show me your work

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Give a concise account of the important decisions, alternatives considered,
observations, calculations and checks that support the result. This is a public
rationale grounded in artifacts, not private chain-of-thought or a reconstructed
internal monologue. Do not invent discarded approaches or experiments.

A request to explain a decision returns that explanation in chat. Create a TSV
only when a log or durable trail is requested. A request to keep logging applies
to the named task until finished or stopped; it does not activate any mode or
start an unattended agent loop.

For a log, use one canonical location chosen from the user's request or established
task scratch area. Record one consequential decision or checkpoint per row, not
every tool call. Use the helper and schema in [the log guide](references/log-guide.md).
It records timestamps and protects TSV cells against common spreadsheet formula
prefixes. Keep credentials and unrelated private context out of the trail.

A mistaken row is superseded by a new row, not silently rewritten. Reconstructed
entries must say they were reconstructed; do not backdate them as contemporaneous.
Follow important evidence pointers before handoff. A pointer is not proof of what
it names. Do not demand another model, auto-commit a log, or publish the transcript.

Return the rationale or log location and important unresolved evidence gaps. A
second check in the same context must not be represented as independent review.
