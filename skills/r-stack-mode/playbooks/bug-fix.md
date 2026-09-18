# Bug fix

1. **Contract.** State the reported symptoms, intended behavior, protected behavior
   and success observations before mutation. For several findings, use one short
   checklist with a row per defect; separate file names are not separate defects.
2. **Baseline each defect.** Before applying its corresponding fix, establish
   that defect's failing observation on the reported surface. Preserve the
   starting bytes, inputs and environment needed to repeat it, including relevant
   uncommitted work. One defect's reproduction does not cover another. Batch fixes
   only after every defect in the batch has its own baseline or an explicitly
   disclosed reproduction limitation. A provisional hypothesis may guide the
   probe; it is not yet a confirmed cause.
3. **Diagnose each defect.** Trace the actual mechanism and name the confirming
   observation. Load `investigate` when the cause is uncertain, contested or needs
   deeper tracing; a directly established local cause can be diagnosed inline.
   A reporter's explanation is a hypothesis. Merely reading a skill is not a
   diagnosis. Minimize a scenario only as far as useful and retain the original.
4. **Choose each check.** Prefer maintained tests that reach the changed behavior.
   Where they cannot, use an authorized one-off executable probe or an inspected
   browser interaction, with its coverage and retention limits. No available safe
   check means unverified, not an inferred pass. Load the
   [UI behavior guidance](../references/lenses/ui-ux.md) for changed user-facing
   interactions; add other triggered lenses as needed. Include an unchanged
   control and material behavior partitions. Expected results must not reproduce
   the implementation's logic.
5. **Fix.** Apply the smallest complete change supported by each diagnosis. Invoke
   `architect` only for changed ownership or a consequential boundary. Do not
   widen scope, weaken checks or accumulate defenses for disproved causes.
6. **Prove.** Invoke `verify` after the final relevant mutation. Recheck each
   original scenario, its focused check and the required project gates. Commands
   used as pass/fail checks must fail on failed assertions, missing cases or setup
   failures. Capture tools are optional; meaningful assertions are not optional
   for checks presented as executable gates.
7. **Review and close.** Use the review warranted by risk, label self-review
   honestly and re-verify resulting edits. Report each defect's actual evidence,
   final identity, maintained versus one-off coverage, cleanup and remaining gaps.

## Recover from a missed baseline

If a fix was written first, disclose that ordering. A later comparison against an
exact saved pre-edit artifact is useful reconstructed evidence, not reproduction
performed before editing. Use a separate copy or an authorized isolated worktree;
do not restore files with `git checkout --`, `git restore` or a reset over user
work. `HEAD` is not the starting state unless that equivalence was checked. If no
faithful pre-edit artifact exists, state the limit. Recovery does not erase the
ordering miss, and the final relevant state still needs verification.
