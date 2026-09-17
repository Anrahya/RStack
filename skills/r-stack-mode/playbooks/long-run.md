# Long run

1. **Mission.** State the underlying route, countable finish predicate, authority,
   protected state, checkpoints, resource limits supplied by the host, stop
   conditions and delivery boundary. Duration is not a finish predicate.
2. **Recover.** Invoke `resume` for inherited work. Preserve contract, accepted
   decisions, current units, artifact identities, valid/stale evidence, owners,
   blockers and next action in existing durable task state.
3. **Choose execution.** Use serial execution for dependent work. Invoke
   `orchestrate` only for genuinely independent units; pilot a novel repeated
   contract before scaling it. Operator absence is not permission for unsafe
   parallel writes or new external actions.
4. **Run and re-ground.** Verify bounded units and retain the best supported
   artifact. Stop repeating a failed premise without new evidence. Reconcile
   unknown external outcomes before retrying side effects. At checkpoints,
   re-evaluate the actual finish predicate instead of redefining completion.
5. **Close.** Invoke `verify` on the final artifact and review as required.
   Account for every unit, failed attempt and gap. If unfinished, return an exact
   checkpoint and first unmet gate, never an implied future background result.
