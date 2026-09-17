# Workflow evaluation

Use to compare R-Stack, another workflow, or a proposed instruction change.

1. **Decision.** State the behavior being tested and the promotion decision the
   result will inform. Keep product work outside the evaluation's output scope.
2. **Contract.** Invoke `workflow-eval`. Freeze realistic tasks, starting state,
   deterministic checks, rubric, severe failures, resource accounting, number of
   runs, and promotion threshold before candidates run.
3. **Blind.** Create isolated organic-looking workspaces and prompts. Hold
   harness-supplied executor configuration, tools, and task conditions constant.
   Hide workflow identity, other runs, and the rubric from candidates.
4. **Run.** Execute independent repetitions. Preserve transcripts, diffs,
   commands, and artifacts under sanitized labels.
5. **Judge.** Run deterministic checks, then score anonymized outputs. Verify
   process behavior from transcripts and artifacts rather than self-report.
6. **Close.** Return per-arm outcomes, severe failures, criterion scores,
   resource use, uncertainty, and `promote`, `hold`, or `reject`. A single
   run is diagnostic evidence, not broad validation.
