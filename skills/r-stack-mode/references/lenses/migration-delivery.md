# Migration and delivery

Pin the source and target versions, affected data, compatibility obligations,
exact environment, authority and recovery boundary. Distinguish local working
code, a built artifact, a tested release and the deployed version.

For risky data or schema changes, inspect real shape and invariants before the
migration. Use representative malformed, missing, duplicate and legacy inputs.
Rehearse on an approved snapshot or isolated fixture. Verify counts and semantic
invariants after transformation, not merely command exit. A backup is not a
recovery proof until a restore path has been exercised or its untested status is
explicit. Destructive data loss may not be reversible by deploying old code.

When compatibility requires it, expand the new representation, migrate bounded
units, then remove the old form after its consumers are gone. Do not keep
throwaway compatibility forever; do not remove it before its obligation ends.

Before release, verify the exact built artifact and requested delivery boundary.
Opening a pull request does not authorize merging; green CI does not authorize
production deployment. A rebase, regenerated build or relevant configuration
change may invalidate prior evidence.

For authorized deployment, use the project's staged rollout and health criteria.
Observe the actual target after the final mutation, including durable effects
and recovery signals. Stop on ambiguous target identity, conflicting writers or
unknown outcomes. Report what was delivered, what was only proposed, rollback
limits and the final evidence identity.
