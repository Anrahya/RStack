# Worker contract, schema 2

A direct assignment needs outcome, context pointers, exclusive write scope,
authority, acceptance, proof and stop conditions. Do not fill twenty fields with
`NONE` when a short brief carries the same actionable information.

For work crossing contexts or using captured evidence, freeze the original
acceptance IDs and use this shape. Commands below belong to the supplied runnable
example, not an instruction to substitute them for an application's real checks.

```json
{
  "schema_version": 2,
  "outcome": "Return the stable sorted result without changing the input.",
  "acceptance_ids": ["A-001"],
  "units": [{
    "id": "W-001",
    "role": "implementer",
    "outcome": "Implement stable unique sorting.",
    "authority": "Edit app.py only; no external actions.",
    "context": ["TASK.md", "app.py", "check.py"],
    "stop_if": ["The requested behavior is ambiguous or the declared check cannot run."],
    "write": ["app.py"],
    "requires": [],
    "acceptance": [{
      "id": "A-001",
      "predicate": "The public function sorts unique values without mutating its caller input.",
      "verify": {
        "kind": "execution",
        "action": "Run the public behavior assertions.",
        "expected": "Every public behavior assertion passes.",
        "argv": ["python3", "check.py"]
      }
    }]
  }]
}
```

Every machine-checked unit requires non-empty `context` pointers and `stop_if`
conditions. Optional fields include read scopes, excluded paths, accepted decision
IDs, known facts, assumptions, forbidden actions and
`write_resources` for explicitly named external resources. Use canonical literal
relative POSIX paths: no globs or parent traversal. `.` owns the whole repository.
Case aliases conflict conservatively; symlink write scopes require host-specific
handling. An empty write list means no source write authority.

Dependencies must be acyclic. Overlapping writes require a dependency order and
actual host serialization. `produces_for` names consumers that depend on this
unit; final integration must have its own proof. These checks validate declared
ownership, not actual permissions or resource locks.

A worker returns a schema-2 receipt with a result and evidence tied to its assigned
claims. Execution observations should come from the recorder, not hand-written
success summaries. `PASS` requires current successful proof for every assigned
claim. `FAIL`, `ISSUES`, `BLOCKED` and `INCONCLUSIVE` remain distinct; unresolved
blockers must be named. See [the full evidence contract](../../r-stack-mode/references/evidence-contract.md).

The coordinator inspects the final diff and actual artifacts before acceptance.
It accounts for every dispatched unit and verifies the converged final artifact.
