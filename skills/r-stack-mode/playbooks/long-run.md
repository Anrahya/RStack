# Long run

Use when the operator steps away or the mission spans several checkpoints. Long
run modifies an underlying primary playbook rather than replacing its gates.

1. **Mission contract.** State the underlying route, countable finish predicate,
   authority, protected state, stop conditions, expected checkpoints, and
   delivery boundary. Duration alone is not a finish predicate.
2. **Recover.** Invoke `resume` when inheriting work. Establish durable task
   state with decisions, work units, dependency frontier, write owners, evidence
   receipts, fingerprints, blockers, and exact next action.
3. **Pilot.** Invoke `orchestrate`. Push one representative unit through brief,
   execution, receipt, integration, and final-path proof before scaling a novel
   or repeated unit shape. Correct the contract from pilot evidence.
4. **Run.** Dispatch a rolling set of ready independent units. Treat completions
   as queue events, integrate in dependency order, refill available capacity,
   and stop or re-ground work whose inputs became stale. Account for every
   dispatched unit as accepted, rejected, blocked, or abandoned.
5. **Replan.** At each checkpoint, test the real finish predicate. Preserve
   accepted evidence, discard non-wins, and revise the graph when observed facts
   contradict it. Do not reinterpret the goal to manufacture completion.
6. **Close.** Invoke `verify` on the converged final state and `review` when
   risk warrants it. Report predicate counts, accepted evidence, abandoned work,
   unresolved gates, and the exact resume point if unfinished.

