# Review

1. **Pin.** Identify the original request, valid comparison point, final artifact,
   protected behavior and claimed proof. An empty diff can be a valid no-op;
   establish whether the requested state already holds.
2. **Check.** Run or inspect deterministic checks before speculative review.
3. **Challenge.** Invoke `review`. Separate intent, engineering and proof
   questions. Record actual review provenance; a serial second pass is not an
   independent reviewer. Do not leak a preferred verdict into separate reviews.
4. **Validate.** Establish trigger, execution path, consequence and counterevidence
   for each issue. Resolve disagreement through observations rather than votes.
5. **Close.** Return `PASS`, `ISSUES`, or `INCONCLUSIVE`, supported findings,
   dismissals and proof gaps. Stay read-only unless fixes were authorized; edits
   made during a fix reopen affected verification.
