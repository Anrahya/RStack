---
name: why
description: "Explain causes, design rationale or the reasons behind a result. Distinguish documented intent, causal mechanisms and inference."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: read-only
---

# Why

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

First distinguish the question being asked. "Why does gas expand?" asks for a causal
mechanism. "Why did this project choose SQLite?" asks for recorded intent and
constraints. "Why did this measurement change?" asks for competing explanations
and discriminating evidence. Do not require Git history for a physics question.

For a mechanism, state the relevant principles and conditions, explain the causal
chain, and test the explanation against a counterexample or limiting case when
useful. Separate the explanatory model from what the evidence directly establishes.

For a specific decision, locate the concrete artifact and substantive history.
Read design records, original discussions, commits or issues that actually bear on
the question. Present present-day benefits separately from historical motivation:
"this could explain the choice" is not "the authors chose it because". Current
code proves neither intent nor the absence of rejected alternatives.

For an observed change, write the plausible explanations and the observation that
would distinguish them. Test the strongest alternatives with authorized, bounded
sources or probes. Do not invent probabilities or label correlation as causation.

Select relevant evidence sources, not every connected account. Start with the
strongest likely record and expand when a consequential gap remains. A search that
returned nothing differs from a source that was inaccessible or outside scope.
Read [the evidence guide](references/evidence.md) for contested or historical claims.

Return the best supported answer, the evidence, material alternatives and what is
still unknown. Preserve confidence language through any simplification. Stop when
the answer is adequate for the requested depth or state the next discriminating
observation. Do not launch a default seven-source panel or change production state.
