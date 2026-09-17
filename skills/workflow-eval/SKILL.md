---
name: workflow-eval
description: Test whether a workflow improves delivered outcomes under matched task, tool and resource conditions. Use before promoting instruction changes or making claims that R-Stack improves a model's engineering capability.
---

# Workflow evaluation

Read [the evaluation protocol](../../docs/EVALUATION.md). Distinguish tests of
R-Stack's own scripts from trials of an agent using R-Stack. Neither a valid
receipt nor an attractive demonstration establishes model uplift.

Freeze representative tasks, starting revisions, original acceptance criteria,
protected holdout checks, severe-failure rules and resource accounting before
running candidate variants. Compare the same supplied executor configuration
with and without the workflow first. Changing the executor at the same time
changes the question.

Use isolated workspaces and independent repetitions. Randomize run order. Keep
reference implementations and holdout grading outside candidate access, using
actual filesystem or tool permissions rather than an instruction not to look.
Do not imply perfect candidate blinding when named workflow files are visible.
Blind outcome reviewers to variant and executor identity; balance presentation
order and inspect disagreements rather than averaging them away.

Run deterministic checks before subjective scoring. Judge the actual artifact
and exercised behavior, not a polished report. Calibrate UI/UX or maintainability
judgments with concrete examples and the user's priorities. A known severe
failure cannot be rescued by a high mean aesthetic score.

Record every attempt, failure, retry, human intervention and available cost.
Compare clean completion, severe failures and total cost per clean completion.
Report uncertainty over tasks, not an artificially large sample made by treating
repeats of one task as unrelated new tasks.

Return `promote`, `hold`, or `reject` against the predeclared criterion, with
per-task results, artifacts, uncertainty and limits. Three runs of a few tiny
fixtures are smoke tests, not a universal superiority claim. Ablate unnecessary
components instead of assuming every additional step improves the system.
