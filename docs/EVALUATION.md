# Does R-Stack improve a capable, cheaper agent?

## Release status

This release contains tested evidence machinery and proposed workflow changes.
It does not contain live model-uplift results. Mechanical test success establishes
that particular code paths behave as asserted, not that an agent will select the
right route, write an adequate oracle, produce better designs or obey the workflow.

The primary experiment is: **holding the task, executor and tools constant, does
R-Stack increase clean completion enough to justify its additional cost?** A
second experiment asks whether that operating point competes with a frontier
executor at a comparable cost or latency budget. These are different claims.

## Arms and controls

Start with three arms under one exact candidate executor configuration:

| Arm | Workflow |
| --- | --- |
| A | Host baseline with normal project instructions, no R-Stack |
| B | Pinned R-Stack 0.1.0 |
| C | This 0.2.0-rc.1 candidate |

Then add a frontier executor with the host baseline and, separately, with the
revision. This prevents attributing all improvements to a workflow that the
frontier executor could use too. A native P-stack arm with its default mixed
executors is a useful product comparison but not an isolated workflow ablation.
Compare a single-executor adaptation separately and disclose the adaptation.

Pin provider, exact checkpoint or resolved model version, quantization when
relevant, tool access, reasoning setting, sampling, context limits, parallelism,
starting revision, dependencies and initial user request. Record all available
limits and observed actual resource use. An endpoint alias may change its model;
a family label such as Llama is not a reproducible configuration.

Keep project instructions and baseline tools in all arms. Do not starve the
control arm of the browser or tests just because R-Stack needs them. Do not lend
only the candidate arm a stronger judge or investigator without accounting for
that intervention. Keep per-run memories and artifacts isolated.

## Task selection

Use recent real work with frozen starting states and evaluator-held acceptance.
A useful pilot is 12–20 varied tasks with independent repeated attempts; three
repeats per task are diagnostic, not a statistical guarantee. Expand held-out
task diversity before making general superiority or non-inferiority claims.
Choose sample size from the required effect, observed variance and severity
budget, not a ritual fixed number.

Cover at least these families in a broader study:

| Family | Failure exposed | Independent check |
| --- | --- | --- |
| Misleading bug diagnosis | Anchoring and premature repair | Original reproducer plus semantic siblings |
| Persistent feature | Success response without durability | Public read-back after restart |
| Cross-tenant access | Authentication mistaken for authorization | Owner succeeds; other actor is denied |
| Retry/concurrency | Identity and lifecycle blind spots | Duplicate, changed-field and reordered cases |
| Refactor | Untested public behavior changes | Characterization or differential replay |
| Performance | Uncontrolled workload or noisy victory | Frozen workload, repetitions and correctness guards |
| UI feature | Good screenshot, broken user flow | Browser task completion and state matrix |
| Visual direction/parity | Uncalibrated taste or baseline tampering | Frozen references, rubric and rendered comparison |
| Migration/release | Wrong artifact or irreversible state loss | Data reconciliation, exact identity, recovery rehearsal |
| External research | Stale sources or mismatched benchmarks | Claim/source audit with conflicting-date examples |
| Interrupted work | Stale proof and unnecessary repetition | Seeded summary, actual diff and altered evidence |
| Missing tool/authority | Fabricated completion or unsafe bypass | Deliberately unavailable dependency and honest outcome |

The four bundled `evals/smoke.py` cases are intentionally small mechanism
controls. Their buggy implementations must fail and reference fixes must pass.
They are not representative of top-ten model difficulty, and their public
availability makes them unsuitable as a hidden capability benchmark. The
persistence fixture does not claim crash-atomicity or concurrency safety.

## Candidate and judge isolation

Candidates see the ordinary user request, project and permitted tools. Graders,
reference fixes, hidden tests and other arms' outputs must be inaccessible through
actual host permissions. A sibling directory alone is not an isolation boundary.
The smoke grader executes arbitrary candidate Python; use a disposable sandbox
for anything untrusted. Do not run a stranger's patch on a privileged host.

The candidate may recognize named skills. Do not claim full workflow blinding.
Instead blind the outcome reviewer to executor and arm identity, randomize
presentation order, and use paired artifact comparisons with balanced ordering.
Preserve raw artifacts and rationale for disagreements; do not let a favorable
LLM score overrule a deterministic failure.

Calibrate subjective criteria with concrete examples. UI judgments should score
fit to the brief, information hierarchy, coherence, craft and task usability—not
whether a design matches the reviewer's favorite palette. Separate visual
judgment from functional and accessibility checks. Review scope and needless
complexity as well as apparent polish.

## Metrics and uncertainty

**Primary:** clean completion of every frozen required acceptance with no severe
failure. Count fabricated proof, unauthorized/destructive action, known acceptance
failure reported as complete, changed holdout tests, and stale proof represented
as current separately as severe failures.

**Efficiency:** total cost of every attempt, retry, planning step, reviewer and
abandoned branch divided by clean completions. Report zero successful runs as
undefined cost per success, not zero. Include latency and user interventions.
Fixed-cost and fixed-latency comparisons are separate operating curves; a cheaper
per-token model is not necessarily cheaper per accepted change.

**Diagnostics:** actual sources opened, surface exercised, invalidated evidence,
route/lens selection, recovery changes and excessive work. Invocation counts or
verbose receipts are not outcome metrics. Do not let an agent define a smaller
acceptance denominator after seeing its result.

Use paired task-level differences and uncertainty that respects repeated runs
within tasks. A task-cluster bootstrap is one option when enough diverse tasks
exist; document its assumptions and limitations. Do not treat dozens of attempts
at one problem as dozens of independent problem types. Rare severe failures need
specific examination even when the average improves.

`evals/summarize.py` checks paired records and computes descriptive counts and
costs. It intentionally does not compute a promotion decision, confidence
interval, or universal ranking. Input records contain `task`, `run`, `arm`,
`clean`, `severe_failure`, `cost` (number or null) and `currency` for known costs.
Store costs in one currency with the conversion basis outside the raw results.

## Promotion and ablation

Predeclare the minimum useful quality gain or non-inferiority margin, acceptable
cost/latency change and severe-failure rule. There is no universally correct
margin. Use **promote** only when the held-out evidence meets those criteria;
**hold** when promising but underpowered or ambiguous; **reject** when outcomes
regress or added cost earns no benefit.

Test components independently: compact contract/context, project driver, capture
gate, domain lens, stalled-attempt recovery, and risk-triggered review. Remove
components that no longer help a newer executor. Curated examples are hypotheses
to evaluate, not automatically good because they were written by an agent.

Record the complete manifest and retain the unsuccessful runs. A release can
pass all script tests and still remain on hold for its claimed model uplift.
