# Plan

Use for an implementation plan, specification, ticket breakdown, or phased work
graph.

1. **Contract.** Confirm that the requested outcome, protected behavior, settled
   decisions, authority, and proof are known. Route unresolved requirements
   through Shaping and unresolved boundaries through Design.
2. **Ground.** Inspect the current code and project instructions far enough to
   identify real seams, dependencies, existing checks, and prefactoring that
   would make the change safer. Stay read-only.
3. **Slice.** Define complete vertical units, each small enough for one fresh
   context and independently demoable or verifiable. Give every unit a stable
   identifier, outcome, scope, dependencies, write owner, acceptance claims, and
   exact proof.
4. **Order.** Put shared contracts and blocking work first. Parallelize only
   disjoint units. For a wide mechanical migration that cannot stay green as a
   vertical slice, use expand, migrate in bounded batches, then contract.
5. **Audit.** Map every original acceptance claim to at least one unit and proof.
   Flag unsupported assumptions, write overlap, cycles, and terminal integration
   gaps before presenting the plan.
6. **Close.** Return the work graph, frontier, decision links, per-unit proof,
   integration order, and finish predicate. Persist it only in the project's
   existing tracker or durable task state unless the user requests a document.

