# Evidence contract, schema 2

## What is and is not guaranteed

Instruction mode works through ordinary agent tools. It expresses obligations but
cannot force the agent to obey them. Capture mode uses local Python scripts to
record execution and check consistency. Enforcement mode exists only when the
host independently invokes a protected completion gate and rejects bypasses.
This release does not install host-specific stop hooks or a new agent runtime.

The scripts check declared coverage, a canonical graph hash, typed results, each
closing fingerprint, command identity, normal completion and captured file hashes. They cannot prove
that acceptance was correctly interpreted or that assertions are sufficient.
An agent able to rewrite the contract, checks, logs and validator can forge a
self-consistent story. For independent assurance, the host or CI must own those
objects and run outside the candidate's write authority. Hashes are not signatures.

The repository snapshot includes HEAD (or an unborn-branch marker), the index,
tracked files and non-ignored untracked files, content and modes. It excludes
ignored files and external state, does not follow symlink targets, and rejects
submodules. It is not a lock or an environment snapshot. Serialize mutations;
identify builds, services, dependencies and deployed targets separately. Checks
that generate non-ignored files will invalidate their own snapshot: arrange
legitimate outputs outside source, never ignore source merely to hide mutations.

## Minimal recorded execution

Use one schema-2 graph even for a single recorded unit. For a fully runnable
example, see `examples/recorded-check/` at the plugin root. The graph freezes the
original acceptance IDs, required context and stop conditions, and each unit's
predicate, verification kind, action,
expected signal and exact command argument list. The command must actually assert
the expected behavior; a zero exit from `echo` is not meaningful correctness.

From the plugin root, with project and evidence paths chosen by the operator:

```bash
python3 scripts/check_work_graph.py "$GRAPH" --repo "$PROJECT"
python3 scripts/run_check.py "$GRAPH" --work W-001 --acceptance A-001 \
  --id E-001 --repo "$PROJECT" --evidence-root "$EVIDENCE"
python3 scripts/close_task.py "$GRAPH" --work W-001 \
  --ids E-001 --result 'The required behavior passed its declared check.' \
  --repo "$PROJECT" --evidence-root "$EVIDENCE" --output "$RECEIPT"
python3 scripts/check_receipt.py "$RECEIPT" --graph "$GRAPH" \
  --repo "$PROJECT" --evidence-root "$EVIDENCE"
```

Evidence and receipt output must be outside the project. `run_check.py` supports
one execution claim per invocation and creates a new `E-###` directory containing
stdout, stderr, `run.json` and `evidence.json`. Each record and closing evidence
item carries the canonical graph SHA-256; changing the graph invalidates it.
Reuse of an identifier is rejected.
The timeout and log limit are operational limits, not a security sandbox. POSIX
process groups are cleaned up; detached processes and Windows descendant cleanup
need host isolation. Do not run untrusted commands without the host's sandbox.

`close_task.py` assembles only the explicitly selected observations for one unit.
A failed or stale observation produces `INCONCLUSIVE`, not a false PASS. For a
multi-unit graph, validate each receipt and perform a separately declared final
integration unit. The tool does not attribute source edits or certify review.
Omitted `mutations` means not collected, not that no edits occurred.

## Non-execution evidence

`inspection` and `judgment` claims are supported by the validator, but are not
captured by the command runner. Their JSON observation record must name `kind`,
`work_id`, `acceptance`, `evidence_id`, `fingerprint`, `contract_hash`, `outcome`,
`origin` (`tool`, `human`, or `agent`), `observation`, and non-empty `attachments`
with relative paths and SHA-256 hashes. Their receipt item has the same identity,
outcome, observation, predicate, action and expected result as the graph. Keep
inference references in `supports`, pointing to distinct successful observed
evidence bound to the same current contract. Historical support from another
contract may remain as context but cannot contribute to closure. See
`docs/EVIDENCE-SCHEMA.md` for the full shape.

An agent-origin design judgment remains an agent judgment, even when attached to
a real screenshot. The validator checks that attachments exist and match their
record; it does not read images, assess taste or verify citation entailment.

## Exit status and compatibility

Validators: `0` means declared checks passed, `1` means valid input was rejected,
`2` means unreadable input or invocation failure. Capture returns `1` for a
recorded failed/inconclusive check. Never treat a traceback as a successful
negative test. `--structure-only` is explicitly a lint, not permission to close.

Schema-1 receipts cannot certify schema-2 completion. Preserve historical records;
create new evidence after migration rather than relabeling old reports.
