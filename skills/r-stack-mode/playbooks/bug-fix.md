# Bug fix

1. **Contract.** State the symptom, original requested behavior, protected
   behavior and acceptance. Partition broad terms such as replacement, retry or
   unchanged into the distinct transitions they imply.
2. **Reproduce.** Establish a repeatable failing observation on the reported
   surface before editing. A provisional hypothesis may guide the probe; do not
   treat it as the cause. Minimize only as far as it improves discrimination.
   Preserve the original scenario. If reproduction is unavailable, state the
   evidence limit rather than manufacture red-then-green proof.
3. **Diagnose.** Invoke `investigate`. Trace the actual boundary and falsify the
   user's suggested cause when evidence contradicts it. For uncertain causes,
   compare predictions and run the most discriminating safe probe.
4. **Pin.** Add or identify a regression check that can expose the defect at the
   actual consumer seam. Include an unchanged control and material behavior
   partitions. Do not write a test whose expected value repeats the implementation.
5. **Fix.** Make the smallest complete change supported by the diagnosis.
   Invoke `architect` only for changed ownership or a consequential boundary.
   After repeated failures without new evidence, re-examine the premise instead
   of accumulating defensive patches.
6. **Prove.** Invoke `verify` after the final mutation. Check both the focused
   regression and the original scenario, plus required project gates. Preserve
   earlier failures as historical support, not current proof.
7. **Review and close.** Use the review warranted by risk. Re-verify any ensuing
   edits. Report root cause, actual failing/passing evidence, final identity and
   any condition that remains unproven.
