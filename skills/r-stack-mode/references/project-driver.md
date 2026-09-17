# Build a project-local verification driver

This is optional reusable capability, not a document to generate on every task.
Use the project's existing driver first. Create or repair one only when authorized
and when a missing surface blocks consequential repeated verification.

Inspect the repository for its documented launch command, required fixtures,
ports, authentication, actual user/API/CLI entry points and existing browser or
integration tests. Resolve observable setup facts from the repository. Do not
invent selectors, commands or credentials.

A usable driver states:

1. **Launch:** exact authorized command and isolated instance/data ownership.
2. **Doctor:** read-only evidence of readiness, expected build/version, correct
   target and valid test authentication. A responding unrelated process is not
   your instance.
3. **Drive:** exact stable controls or commands from this application, reaching
   the real feature and its material failure state.
4. **Observe:** independently expected result, visible state and relevant durable
   side effect; evidence locations and environment identity.
5. **Cleanup:** stop only processes and scratch state this run owns. Keep proof
   artifacts. Never kill everything with the same process name.

Use existing accessibility labels, test IDs or public paths rather than brittle
coordinates where possible. Do not make the proof pass by exposing internal
setters that bypass the changed boundary. Mark necessary fixtures and mocks.

Execute the recipe once, including cleanup, and confirm the proof still exists.
An unexecuted recipe is a draft. Record which feature was actually exercised;
executing one mapped feature does not verify every feature. Give maintained
feature maps an owner and recheck them when routes, commands, authentication or
build setup change. Never claim installation or runtime compatibility on a host
that was not exercised.
