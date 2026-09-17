# Evaluation case selection

The original six v0 case families remain useful: misleading diagnosis,
boundary-crossing feature, behavior-preserving refactor, empirical architecture
fork, shared-boundary parallel work and interrupted state. They were case
descriptions, not an executable or statistically validated benchmark.

Use `docs/EVALUATION.md` for the expanded held-out evaluation design. The bundled
`evals/smoke.py` creates and grades four small executable mechanism fixtures.
These are wiring and negative-control tests, not a representative difficulty
sample for capable engineering agents. Keep the grader and reference fixes
outside candidate access. No live model results are shipped in this release.
