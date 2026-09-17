# A practical technical-writing guide

## Structure by purpose

| Purpose | Useful order | Common mistake |
| --- | --- | --- |
| Tutorial | Outcome, prerequisites, small working steps, expected observations. | Large conceptual detours before the first working step. |
| How-to | Goal, conditions, ordered actions, checks, failure recovery. | Explaining the entire system before answering the task. |
| Reference | Named subject, exact behavior, inputs, outputs, errors, limits. | Unsupported certainty or mixing current and historical versions. |
| Explanation | Question, definition, mechanism, example, implications, limits. | A file inventory presented as understanding. |
| RFC | Decision, constraints, alternatives, proposal, risks, rollout and validation. | A preferred solution before establishing the actual problem. |
| Change summary | Intent, externally visible effect, important implementation choices, actual validation. | A transcript or every changed line repeated in prose. |

## Sentence checks

Name the actor when it matters. Keep "only", "not" and conditions next to what they
qualify. Break noun piles into relationships. Use one name per concept. Preserve
articles and verbs. Resolve ambiguous pronouns. Avoid unnecessary idioms for a
broad audience. Use the term the reader actually sees in the product or code.

Short sentences are useful, not a mandatory meter. Longer sentences can retain a
condition or consequence without interrupting the explanation. One document can
contain explanation and a reference section when that serves its reader.

## Evidence checks

Separate verified commands from examples. An illustrative path is not a discovered
path. Record versions for time-sensitive instructions. Source factual claims without
burying every sentence in citation clutter. Do not remove limits or uncertainty to
sound confident. Never imply that code was executed or a source read when it was not.

## Usability checks

Can the reader find the answer? Can they follow a procedure in order? Will they
recognize successful and failed outcomes? Are recovery instructions safe? Are examples
copyable without exposing credentials? Is the document complete for its stated scope?

The structural vocabulary is informed by Diátaxis; sentence guidance draws on the
P-stack adaptation of Google developer style, simplified technical English and
Global English. This guide does not claim compliance with a proprietary standard.
