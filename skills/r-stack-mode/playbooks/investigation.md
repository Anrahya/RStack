# Investigation

Use for a read-only explanation, audit, comparison, diagnosis, or recommendation.

1. **Contract.** State the exact question, relevant scope, evidence that could
   answer it, and the fact that mutation is excluded. Pass when the requested
   deliverable cannot be confused with implementation.
2. **Ground.** Invoke `investigate`. Trace current mechanics before historical
   motivation unless the question is explicitly historical. For a broad system,
   use independent read-only lanes for distinct subsystems or evidence sources.
   Pass when the caller or external event is traced through state, side effects,
   failures, recovery, and observable output.
3. **Challenge.** Treat any explanation embedded in the request as a hypothesis.
   Seek callers, tests, runtime observations, history, and primary sources that
   could disprove it. Resolve conflicting reports with a discriminating check,
   not a vote.
4. **Synthesize.** Mark consequential claims as observed, supported inference,
   proposed, or unknown. Include searched sources that returned no evidence and
   any inaccessible source that limits confidence.
5. **Close.** Return the answer, traced path, rejected hypotheses with
   counterevidence, relevant locations, and remaining uncertainty. If the
   evidence cannot answer the question, return `inconclusive`; do not silently
   cross into code changes.

