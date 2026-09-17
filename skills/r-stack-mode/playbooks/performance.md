# Performance

1. **Contract.** Define one user-relevant metric, workload, environment, units,
   correctness guardrails, and success threshold.
2. **Freeze the harness.** Record the exact command, inputs, warmup, repetitions,
   noise or variance, environment, and tree fingerprint. Capture the baseline
   before changing code.
3. **Diagnose.** Invoke `investigate` and profile the measured path. Generate
   causal hypotheses from traces or measurements rather than code appearance.
   Independent analysis lanes may inspect different artifacts; benchmark
   execution and mutations stay serialized.
4. **Climb.** Change one causal variable at a time. Measure with the frozen
   harness. Keep a change only when it improves the target without violating
   guardrails; revert non-wins before the next attempt.
5. **Redesign when earned.** Invoke `architect` if the measured cause requires
   changed ownership or a boundary. Rebaseline only when the approved design
   changes the workload itself, and preserve the original comparison.
6. **Prove and close.** Invoke `verify` on the final tree with correctness
   checks and the performance measurement. Report values, units, variance,
   environment, baseline and final fingerprints, retained changes, rejected
   hypotheses, and limits.
