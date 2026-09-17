# Bug fix

1. **Contract.** State the exact symptom, affected surface, protected behavior,
   and passing condition. Partition broad words such as *replacement*,
   *unchanged*, *retry*, or *concurrent* into the distinct state transitions
   they imply; do not let one convenient example stand for the whole contract.
2. **Build the loop.** Produce one red-capable command or repeatable observation
   that exercises the reported symptom. Run it before forming a cause. Tighten it
   toward deterministic, fast, and unattended execution. If no honest loop is
   possible, record what was attempted and limit the result to an inconclusive
   investigation.
3. **Minimize.** Remove inputs, setup, and actors one at a time while retaining
   the symptom. Pass when the remaining scenario is small enough to discriminate
   causes and every retained element is plausibly load-bearing.
4. **Diagnose.** Invoke `investigate`. For a non-obvious cause, rank competing
   falsifiable hypotheses and state each prediction. Use `orchestrate` only when
   hypotheses can be tested independently; do not dispatch competing fixes.
5. **Pin.** Convert the minimal reproduction into a failing regression check at
   the real caller seam when one exists. Build a compact behavior matrix from
   the contract and cover each materially different transition plus an
   unchanged control. When authority depends on equality, a version, or a
   compare-and-set predicate, vary every identity-bearing field independently.
   A shallow test that cannot exhibit the bug is false confidence; record a
   missing seam instead.
6. **Fix.** Invoke `architect` only if ownership or a boundary changes. Make the
   smallest change supported by the surviving mechanism. Remove diagnostic
   instrumentation and discard disproved defenses.
7. **Prove.** Invoke `verify` after the final mutation. Require the regression
   check and the original unminimized surface to pass.
8. **Review and close.** For deliberate risk, invoke `review`. Report the
   root cause, red-then-green evidence, affected revision, cleanup, and remaining
   uncertainty.
