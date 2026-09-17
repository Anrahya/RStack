---
name: workflow-eval
description: Compare skills, prompts, playbooks, or engineering workflows with blinded realistic tasks and evidence-based scoring. Use before promoting an R-Stack change or when comparing R-Stack with another workflow.
---

# Workflow evaluation

Measure behavior, not whether an agent repeats the instructions. R-Stack never
selects the executors for an evaluation. Use the configuration supplied by the
operator or harness and hold it constant across the arms being compared.

## Frame

1. State the behavior under test and the decision the result will inform.
2. Choose realistic tasks that expose the suspected failure mode. Read
   [v0 cases](references/v0-cases.md) when evaluating the full workflow; otherwise
   build the smallest case that can discriminate the variants.
3. Define the rubric, severe-failure conditions, resource accounting, and
   promotion threshold before seeing candidate output. Read
   [the scoring contract](references/scoring.md).

## Blind

4. Create one isolated workspace per run. Candidate-visible paths, prompts, and
   files must look like an ordinary project. Do not use words such as evaluation,
   benchmark, rubric, candidate, judge, comparison, or test arm where candidates
   can see them.
5. Give every arm the same organic user request, starting state, tool access,
   time boundary, and harness-supplied executor configuration. Change only the
   workflow variant under study.
6. Do not tell candidates that other runs exist. Do not ask them to enumerate
   instructions or skills they followed.

## Run and judge

7. Run repetitions independently. Preserve outputs, diffs, commands, and
   transcripts under sanitized labels.
8. Run deterministic checks before judgment scoring. A functional failure is not
   rescued by persuasive prose.
9. Give a judge anonymized artifacts, the original request, and the predeclared
   rubric. Hide workflow and executor identities. For paired variants, score both
   in one pass on the same scale.
10. Inspect transcripts for actual actions: sources opened, gates performed,
    mutations made, verification freshness, and skipped steps. Self-report is not
    evidence of process adherence.
11. Read every result yourself. Investigate disagreements between deterministic
    outcomes, judge scores, and coordinator assessment rather than averaging them
    away.

## Decide

Return the task set, frozen conditions, arm labels, deterministic outcomes,
criterion scores, severe failures, resource use, transcript findings,
uncertainty, and one decision:

- **promote:** the threshold passed without a new severe failure;
- **hold:** signal is promising but underpowered or materially ambiguous;
- **reject:** the variant regressed quality or added cost without earned benefit.

Store evaluation artifacts outside product source unless the repository already
has a designated evaluation area.

