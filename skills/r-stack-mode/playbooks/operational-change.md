# Operational change

Use for deployments, migrations, configuration, credentials, and live state.

1. **Contract.** Inspect current state and state the desired state, health
   predicate, authority, protected resources, recovery boundary, unknown-outcome
   policy, and actions requiring confirmation.
2. **Preflight.** Invoke `investigate` for unknown mechanics or history. Verify
   exact targets and active ownership. Use independent read-only lanes for
   configuration, health, and recovery checks; keep one writer for shared live
   state.
3. **Rehearse.** Use a dry run, staging target, snapshot, or read-only probe when
   it materially reduces risk. Observe what a dry run actually touches and skips
   instead of trusting its label.
4. **Apply.** Execute the smallest ordered mutation. Persist or back up state
   where project policy requires it. Stop on lost identity, conflicting writers,
   missing authority, or an unknown external outcome; do not retry blindly.
5. **Prove.** Invoke `verify` against the live health predicate, durable state,
   and side effects. Check the exact target after the final mutation.
6. **Close.** Report what changed, what remained untouched, evidence, exact live
   identity, cleanup, recovery path, and any unresolved external outcome.

