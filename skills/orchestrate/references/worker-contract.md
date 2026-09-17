# Worker contract

Use this template for deliberate or program work. A small read-only assignment
may collapse it to a paragraph only when outcome, scope, proof, and report remain
explicit.

```text
WORK_ID: W-###
ROLE: investigator | designer | implementer | verifier | reviewer | integrator

OUTCOME:
One bounded, falsifiable result.

PARENT_OUTCOME:
Why this unit matters.

READ:
- Exact files, symbols, systems, or evidence sources.

WRITE:
- Exact paths or mutable resources exclusively owned here, or NONE.

EXCLUDED:
- Adjacent areas this worker must not change.

CONTEXT:
- Focused path, symbol, commit, issue, artifact, or runtime pointers.

ACCEPTED_DECISIONS:
- D-###: Decision and relevant constraint, or NONE.

KNOWN_FACTS:
- Evidence-backed starting facts.

ASSUMPTIONS_TO_TEST:
- Assumptions that must not silently become facts, or NONE.

REQUIRES:
- W-### or NONE.

PRODUCES_FOR:
- W-###, final integration, or NONE.

AUTHORITY:
- Exact permitted mutations or external actions. Unlisted actions are excluded.

ACCEPTANCE:
- A-###: Observable predicate.

VERIFY:
- A-###: Exact command or action.
  Expected: Concrete passing signal.

STOP_IF:
- A dependency or decision is stale.
- Required authority is missing.
- Write ownership conflicts.
- Required proof cannot run.
- Additional task-specific conditions.

FORBIDDEN:
- Task-specific prohibited actions, or NONE.

REPORT:
Return the evidence receipt below.
```

## Evidence receipt

```text
WORK_ID: W-###
STATUS: PASS | ISSUES | BLOCKED | INCONCLUSIVE
RESULT:
One-sentence outcome.

EVIDENCE:
- E-###:
  ACCEPTANCE: A-###
  CLAIM:
  BASIS: observed | supported-inference | proposed | unknown
  ACTION_OR_SOURCE:
  OBSERVED_RESULT:
  LOCATION_OR_ARTIFACT:
  FINGERPRINT:

MUTATIONS:
- Exact path or resource and concise change, or NONE.

REJECTED:
- Hypothesis or alternative and counterevidence, or NONE.

UNCERTAINTY:
- Remaining uncovered condition, or NONE.

HANDOFF:
- Integration requirement or exact next action, or NONE.
```

## Calibration

A good brief lets a worker begin without conversation, names a falsifiable
outcome, grants bounded authority, and makes completion decidable.

A bad brief says only “handle the backend,” omits protected behavior, lets
several workers edit the same boundary, or asks for “tests” without the command
and expected signal.

## Work graph JSON

Use this machine-readable form when the graph has several writers or must survive
a checkpoint:

```json
{
  "decisions": [
    {
      "id": "D-001",
      "text": "One owner settles the shared boundary"
    }
  ],
  "units": [
    {
      "id": "W-001",
      "role": "implementer",
      "outcome": "Deliver one bounded vertical behavior",
      "parent_outcome": "Complete the requested feature",
      "read": ["src/"],
      "write": ["src/owned-area/"],
      "excluded": ["src/other-area/"],
      "context": ["AGENTS.md", "src/owned-area/current.ts"],
      "accepted_decisions": ["D-001"],
      "known_facts": ["The current public entry point is run()"],
      "assumptions_to_test": [],
      "requires": [],
      "produces_for": ["final"],
      "authority": "Edit only the declared write scope",
      "acceptance": [
        {
          "id": "A-001",
          "predicate": "The public entry point exposes the requested behavior",
          "verify": {
            "action": "run the focused public-path check",
            "expected": "the expected result is observed"
          }
        }
      ],
      "stop_if": ["The public contract differs from the accepted decision"],
      "forbidden": [],
      "report": "Return an R-Stack evidence receipt"
    }
  ]
}
```

Validate it from the plugin root:

```bash
python3 scripts/check_work_graph.py graph.json
python3 scripts/check_receipt.py receipt.json --graph graph.json
```
