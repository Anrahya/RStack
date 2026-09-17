# Workflow metrics

Track these per completed task in the task system or existing analytics. Do not
create repository status files solely for measurement. Establish rolling
baselines before setting numeric targets unless correctness requires 100%.

| Metric | Definition | Desired signal |
| --- | --- | --- |
| Acceptance-evidence coverage | Acceptance claims with a valid evidence receipt / acceptance claims | 100% |
| Contract-partition coverage | Materially distinct behavior classes named by the contract with fresh evidence / identified classes | 100% for changed behavior |
| Baseline-first rate | Bugs, refactors, and performance tasks with evidence before mutation / eligible tasks | 100% |
| Real-path proof rate | Behavior changes exercised through the affected boundary or user surface / behavior changes | 100%, with inconclusive separate |
| Proof-overclaim rate | Completion claims whose stated coverage exceeds the exercised contract partitions / completion claims | Zero |
| Stale-proof rate | Completion claims relying on evidence older than the final relevant mutation / completion claims | Zero |
| Wrong-scope mutation rate | Mutations outside accepted scope / mutations | Zero |
| Avoidable-question rate | Operator questions answerable with available evidence or a safe probe / questions | Zero |
| Receipt acceptance rate | Agent receipts whose cited evidence survives coordinator checking / receipts reviewed | Trend upward |
| Resume duplication rate | Completed work unnecessarily repeated after resume / inherited completed work | Zero |
| Escaped defects | Reverts, reopened fixes, or regressions attributable to completed work | Trend downward by severity |
| Clean completion rate | Tasks passing all mandatory acceptance checks without a severe workflow failure / eligible tasks | Trend upward |

Track elapsed time, tool calls, task turns, executor runs, and available token or
cost data as efficiency guardrails. Do not optimize them ahead of clean
completion.

For every miss, classify the cause as framing, grounding, design, implementation,
verification, review, or continuity. A metric matters only when it changes a
future decision.
