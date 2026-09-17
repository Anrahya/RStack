# Shaping

Use when product behavior, domain language, or decision dependencies are unclear.

1. **Contract.** State the problem, affected user or caller, desired outcome,
   protected behavior, and why existing information is insufficient.
2. **Separate.** Invoke `shape`. Divide the unknowns into observable facts and
   genuine product, preference, authority, or irreversible decisions.
3. **Resolve facts.** Invoke `investigate` or `prototype` for facts the system
   can reveal. Pass when no operator question asks them to predict observable
   behavior or feasibility.
4. **Resolve decisions.** Work only the current decision frontier. Give a
   recommendation and consequence with each question. Exercise ordinary, edge,
   failure, retry, and concurrency scenarios where relevant.
5. **Close.** Return settled decisions, precise domain terms, acceptance
   scenarios, explicit deferrals, and the next route. Pass when the behavior is
   unambiguous enough to design or plan; do not implement unless separately
   requested.

