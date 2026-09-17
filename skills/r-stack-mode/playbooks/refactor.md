# Refactor

1. **Contract.** State the behavior that must not change, the structural problem,
   the expected reduction in reader load or risk, and excluded feature work.
2. **Pin behavior.** Capture a characterization, snapshot, replay, or equivalence
   baseline before moving structure. Compilation alone is not a behavior pin.
3. **Ground and shape.** Invoke `investigate` to map callers, ownership,
   boundaries, and blast radius. Invoke `architect` only when ownership or a
   public boundary changes.
4. **Sequence.** Remove dead weight before adding a shape. Prefer small vertical
   green units. For an unavoidable wide mechanical migration, expand the new
   form, migrate callers in bounded batches, then contract the old form; record
   the blocking edges and final deletion condition.
5. **Execute.** Use `orchestrate` only for disjoint migrations with explicit
   write ownership and integration order. Keep the behavior pin green after each
   accepted unit. Do not preserve throwaway compatibility unless the contract
   requires it.
6. **Prove equivalence.** Invoke `verify` after the final mutation and compare
   the real artifact with the original baseline.
7. **Review and close.** Inspect the complete diff for accidental behavior,
   obsolete callers, duplicate paths, and speculative abstraction. Keep the
   refactor only if it measurably clarifies ownership, invalid states, reader
   load, or operational risk.

