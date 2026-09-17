---
name: investigate
description: Establish how a software system behaves and why it has its current shape using source, history, runtime evidence, and falsifiable hypotheses. Use for engineering investigations, audits, explanations, root-cause grounding, and consequential "are we sure" questions.
---

# Investigate

Own the answer. Stay read-only unless the active playbook separately authorizes
implementation.

## Frame the evidence question

Pin the question to entry points, callers, symbols, boundaries, runtime symptoms,
artifacts, or commits. State what observation would distinguish the plausible
answers. Treat a cause or design explanation embedded in the request as one
hypothesis, not privileged truth.

For a narrow question, investigate directly. For a broad subsystem, split two to
four independent read-only lanes by subsystem, evidence source, or falsifiable
hypothesis, then synthesize. Do not split one serial trace into artificial lanes.

## Trace mechanics

Start at the caller or external event and follow:

1. input and boundary validation;
2. central data shape and state owner;
3. control flow and side effects;
4. failure, cancellation, retry, and recovery;
5. persisted or externally observable result.

File names and type names are navigation, not a runtime model. Inspect callers,
tests, configuration, and actual execution where they can contradict the
apparent path.

For stateful, retry, or concurrency defects, name the authoritative state at
each phase and write the smallest transition table that distinguishes no
change, deletion, replacement, conflict, and failure where applicable. Inspect
the actual equality, identity, version, or compare-and-set predicate. Vary each
field that predicate should recognize independently; aggregate examples often
hide one omitted identity field.

## Establish intent

Use history only where current behavior cannot explain why a constraint exists.
Inspect substantive commits, review discussion, issues, documentation, incident
evidence, and available operational records. Code proves mechanics; it does not
prove its own motivation.

Record searched sources that returned nothing and sources that were unavailable.
A missing source is an evidence gap, not a negative result.

## Falsify and observe

Write competing explanations with the prediction each makes. Prefer the probe
that eliminates the most plausible explanations. Change one observed variable at
a time. Run safe instrumentation or a reversible experiment when static evidence
cannot settle an observable fact.

## Investigation receipt

Return:

- question and interpretation;
- traced mechanics with precise evidence pointers;
- intent evidence, separated from present-day inference;
- supported explanation and basis: observed, supported inference, or unknown;
- rejected hypotheses and counterevidence;
- contradictions and source gaps;
- implications, gotchas, and the next discriminating action.

A confident narrative without a traced path and falsification attempt is not
completion.
