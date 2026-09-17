# State and integration

Trace the real consumer across each changed boundary. Name authoritative state,
identity, version, ownership and the transition being changed. Distinguish the
process that acknowledges an operation from the durable owner that commits it.

Build only the relevant behavior partitions: ordinary success, invalid input,
unchanged control, replacement/deletion, duplicate delivery, retry, out-of-order
arrival, concurrent update, cancellation, partial failure and restart. Vary each
identity-bearing or compare-and-set field independently. State which ordering
and delivery guarantees actually exist instead of assuming exactly-once effects.

Write a concrete oracle before implementation. For example, after submitting one
event twice and restarting the service, query the public read path and verify
one durable effect; a mock returning success does not prove that invariant.
Test the unhappy boundary as well as the happy helper. Use deterministic
scheduling or controlled faults where practical; one lucky stress run is weak
concurrency evidence.

A network timeout may leave an unknown external outcome. Reconcile against an
idempotency key, durable record or authoritative read before retrying. Do not
blindly repeat a possibly completed payment, deletion or deployment.

After integration, verify the converged artifact and relevant live-state
identity. Report mocks, substituted services, environment differences and failure
conditions not exercised. Repository fingerprints alone do not identify a remote
database, queue, deployed binary or third-party service.
