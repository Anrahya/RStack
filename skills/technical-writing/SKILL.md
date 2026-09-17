---
name: technical-writing
description: "Write or review documentation, guides, RFCs and explanations for a named reader and purpose. Optional, not a global writing style."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: scoped-edit
---

# Technical writing

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Establish the reader, their task or question, the requested document and known
constraints from the prompt. Do not quiz the user for context already available.
Use the real identifiers, commands and terminology of the subject. General technical
writing does not require a code repository.

## Choose a useful structure

A tutorial leads a learner through something with observable results. A how-to
assumes competence and solves a task. Reference documents facts for lookup.
Explanation develops understanding and tradeoffs. An RFC supports a decision with
constraints, alternatives, a proposal and unresolved risks. PR descriptions explain
intent, changed behavior and the checks actually performed.

Separate those purposes at the section or document level where that helps the
reader; do not fracture a useful document merely to enforce a taxonomy.
Read [the writing guide](references/guide.md) for a substantial document.

## Write and check

Put conditions and hazards before the steps they govern. Give executable examples
and expected observations when supported. Verify commands, paths, counts and code
examples against available sources; distinguish tested examples from illustrative
or unexecuted ones. Never run destructive commands just to validate documentation.

Use direct, natural sentences, stable names and a sensible reading order. Maintain
meaningful uncertainty even in reference material. Preserve citations and quotations.
Do not force tabs, remove all punctuation, ban useful tables, or apply the writer's
preferences over the user's style or project conventions. Use `unslop` only when a
separate editing pass would materially help; it is not a required dependency.

Return the document or requested review. Write files only within the requested
scope. Publication, commits and PR creation are separate authorized actions. If
facts or examples could not be verified, say exactly which ones remain unverified.
