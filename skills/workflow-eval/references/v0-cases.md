# R-Stack v0 evaluation cases

Use small repositories or isolated worktrees whose expected behavior is known to
the evaluator but not disclosed as a rubric to candidates.

## 1. Misleading bug hypothesis

Report a reproducible symptom and include a plausible but wrong cause in the
request. The repository should contain a tight command that can expose the real
cause after investigation.

Checks: reproduces before theorizing, treats the supplied cause as a hypothesis,
finds the real mechanism, produces red-then-green evidence, avoids defensive
changes for rejected causes, and covers semantic siblings of the reported
example rather than only its easiest instance.

## 2. Boundary-crossing feature

Request one small behavior that crosses persistence or a process boundary. Place
an important invariant in project instructions and an adjacent tempting cleanup
outside scope.

Checks: reads project instructions, names the data shape and ownership, delivers
one vertical slice, preserves the invariant, ignores adjacent cleanup, verifies
through the boundary.

## 3. Behavior-preserving refactor

Provide tangled code with passing tests that miss one public behavior. Ask only
for structural simplification.

Checks: pins behavior before editing, subtracts before adding abstraction,
migrates callers coherently, proves equivalence on the public path, introduces no
feature changes.

## 4. Empirical architecture fork

Offer two plausible designs whose deciding property can be measured or exercised
cheaply.

Checks: does not ask the operator for the observable answer, builds a disposable
probe, compares under held conditions, chooses from evidence, keeps experiment
code out of production.

## 5. Parallel work with one shared boundary

Provide several independent changes plus one shared contract. Allow subagents.

Checks: settles the shared contract first, assigns one writer per mutable
surface, uses standalone briefs, integrates in dependency order, verifies the
converged tree, accounts for dropped or inconclusive lanes.

## 6. Interrupted session

Seed a transcript summary, a partially changed workspace, one stale verification
receipt, and one completed unit.

Checks: reconciles summary with live state, does not repeat completed work,
invalidates only stale proof, resumes at the exact next action, preserves scope.

For the initial comparison, run cases 1, 2, and 6. They cover anchoring, boundary
proof, scope, orchestration, and continuity without requiring a large fixture
suite.
