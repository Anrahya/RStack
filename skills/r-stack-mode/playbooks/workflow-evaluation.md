# Workflow evaluation

1. **Decision.** State the proposed behavioral improvement and what evidence
   would justify promotion. Separate script correctness from agent uplift.
2. **Freeze.** Invoke `workflow-eval`. Fix task snapshots, acceptance, holdout
   tests, judge criteria, severe failures, repetitions and resource accounting.
3. **Isolate.** Keep grader/reference artifacts outside candidate access. Use
   matched executor settings and tools. Blind outcome reviewers; disclose that
   candidates may see the identity of their installed workflow.
4. **Run.** Preserve all attempts, outputs, final diffs, actual tool records,
   retries, interventions and cost. Randomize order and avoid carryover memory.
5. **Judge and close.** Run deterministic checks first, then calibrated artifact
   review. Report paired task outcomes, uncertainty, cost per clean completion,
   severe failures and `promote`, `hold`, or `reject`. A smoke suite without model
   runs does not establish workflow superiority.
