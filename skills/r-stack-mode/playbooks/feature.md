# Feature

1. **Contract.** State the new observable behavior, protected behavior,
   acceptance claims, authority, and smallest complete vertical slice.
2. **Ground.** Invoke `investigate` over the affected path, existing callers,
   project rules, and verification seams. Invoke `shape` when product behavior
   or domain terms remain ambiguous.
3. **Design.** Name the central data shape and its owner. Invoke `architect`
   when the work creates or moves a public, persistence, process, concurrency,
   authority, security, or integration boundary. Invoke `prototype` for an
   observable fork that evidence can settle cheaply.
4. **Slice.** Divide non-atomic work into narrow end-to-end units, not horizontal
   layers. Each unit owns acceptance claims, dependencies, writable scope, and a
   proof that can pass before the next dependent unit begins.
5. **Execute.** Keep an atomic slice local. Invoke `orchestrate` for independent
   reconnaissance, complete design alternatives, or disjoint implementation
   units. Settle shared contracts first and give each mutable surface one writer.
6. **Accept units.** Run each unit's narrow proof and inspect every accepted diff
   and evidence receipt. Reject stale assumptions, hidden scope expansion, and
   reports without checkable evidence.
7. **Prove final state.** Invoke `verify` after the final mutation. Map every
   acceptance claim and protected behavior to fresh evidence on the converged
   tree.
8. **Review and close.** For deliberate risk, invoke `review`. Report the
   behavior delivered, proof, exact revision or fingerprint, tradeoffs, and
   uncovered risk.

