# Evidence schemas and trust boundary

`check_work_graph.py` defines schema 2 graph validation. Original acceptance IDs
are declared at root, then assigned exactly once across units. Each claim has a
predicate and `verify` object: `kind` (`execution`, `inspection`, `judgment`),
`action`, `expected`, and exact `argv` for execution. Commands are argument lists,
not implicitly shell-expanded strings. A shell command is allowed only by
explicitly selecting an authorized shell executable and reviewing its script.
Each machine-checked unit also has non-empty `context` pointers and `stop_if`
conditions so a cross-context worker knows what to read and when to stop.

A receipt is an object containing `schema_version: 2`, `work_id`, `status`,
`result`, the canonical graph `contract_hash`, and an `evidence` list. Optional string lists are `mutations`, `rejected`,
`uncertainty` and `handoff`. Omission means the recorder did not collect that
information. `BLOCKED` and `INCONCLUSIVE` require explicit uncertainty.

Each evidence item contains:

```json
{
  "id": "E-001",
  "acceptance": "A-001",
  "claim": "The exact assigned predicate.",
  "basis": "observed",
  "outcome": "PASS",
  "purpose": "proof",
  "action_or_source": "The exact assigned verification action.",
  "expected_result": "The exact assigned expected signal.",
  "observed_result": "The observed result, not an intended action.",
  "fingerprint": "The observed artifact identity.",
  "contract_hash": "The canonical SHA-256 of the graph that authorized this proof.",
  "artifact": {"path": "E-001/run.json", "sha256": "a full SHA-256 digest"},
  "limitations": ["The observation's actual coverage boundary."],
  "supports": []
}
```

This shape illustration is not a valid runnable receipt: the values must come
from the actual frozen contract and captured artifact. The recorder creates valid
execution records automatically. `purpose: support` marks historical context and
cannot close a claim; it may retain its historical identity as context. Proposed
and unknown bases never close a claim. Supported inference is limited to judgment
and needs distinct successful observed items bound to the same current contract;
historical evidence from another contract cannot contribute to closure.

Execution `run.json` records the contract hash, outcome, command, working directory, start/end, elapsed time,
normal completion, exit status, timeout/failure, before/after fingerprints and
hashed stdout/stderr. Inspection and judgment records instead name contract hash,
identity, outcome, origin, observation and hashed attachments. Their observation
must exactly match the receipt item. Their attachments may be captured
screenshots or source excerpts; the validator does not interpret their semantics.

Treat results as consistency evidence, not cryptographic attestations. A trusted
host must freeze the contract and protect checks, recorder, artifacts and gate
from candidate mutation to claim independent enforcement. There is no runtime
scheduler, filesystem sandbox, environment lock, signature or hosted evaluator in
this release. Review the code before installing it in a trusted control path.
