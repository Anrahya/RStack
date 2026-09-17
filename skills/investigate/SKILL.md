---
name: investigate
description: Establish how a system behaves or whether an engineering claim is supported using source, history, execution and falsifiable alternatives. Use for root-cause grounding, audits, comparisons and technical research before consequential decisions.
---

# Investigate

Stay read-only unless the task separately authorizes a bounded experiment or
implementation. Define the question and the observation that distinguishes the
plausible answers. A diagnosis embedded in the request is one hypothesis.

For software behavior, trace the caller or event through input validation,
authoritative state, control flow, side effects, failures and recovery to the
observable result. Inspect actual callers, tests, configuration and runtime
where they can contradict the apparent path. Filenames are navigation, not a
runtime model.

For state, retries or concurrency, identify ownership and the important state
transitions. Inspect the exact equality, identity, version or compare-and-set
predicate. Vary each identity-bearing field independently, with an unchanged
control; one aggregate example may conceal an omitted field.

Inspect history when the reason for a constraint matters. Current code proves
mechanics, not the motivation for its own design. Separate contemporaneous
intent evidence from a present-day interpretation.

For an external technical comparison or research answer, load the
[research lens](../r-stack-mode/references/lenses/research.md). Do not force a
caller trace onto a literature question. Open the primary source, pin its date
or version and inspect contrary evidence before accepting a consequential claim.

Prefer a small probe with a clear prediction over more unfocused reading.
Generate competing explanations only when a real uncertainty remains. A narrow
question does not need a panel; independent read-only lanes must cover genuinely
different sources, subsystems or hypotheses.

Return the answer, traced evidence, rejected explanations and counterevidence,
observed facts versus supported inferences, source gaps, and the next
observation that would change the conclusion. A failed search is not evidence
that a thing does not exist. Stop when the decision's evidence threshold is met,
not when every available source has been read.
