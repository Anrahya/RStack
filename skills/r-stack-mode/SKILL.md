---
name: r-stack-mode
description: Route non-trivial software work through alignment, evidence, bounded subagents, and fresh verification. Use for engineering investigations, designs, plans, changes, reviews, long runs, and workflow evaluation across projects and agent hosts.
---

# R-Stack mode

R-Stack is the front door for non-trivial engineering work. Read
`../../WORK_PROFILE.md`, the active project's instructions, and any project
overlay those instructions name. The work profile supplies stable preferences.
The project owns architecture, commands, permissions, and delivery policy.

## Align before mutation

Restate the request in your own words. Before editing, write a compact alignment
capsule in the task:

- **Outcome:** the externally meaningful result;
- **Proof:** the observation that would demonstrate it;
- **Observed:** facts already established and their sources;
- **Assumed:** unresolved assumptions that could change the approach;
- **Constraints:** behavior and state that must remain true;
- **Non-goals:** adjacent work intentionally excluded;
- **Decisions:** genuine product or preference choices still open;
- **Route:** selected playbook and rigor level.

Keep empty fields out. Resolve observable facts through source, history, tools,
or a reversible experiment. Ask the operator only for a preference, unavailable
authority, inaccessible evidence, or an irreversible external decision.

## Route to one playbook

Read the matching playbook in full. When several match, use the playbook for the
requested deliverable; a diagnosis request does not silently become a fix.

| Requested deliverable | Playbook |
| --- | --- |
| explanation, audit, comparison, recommendation | [investigation](playbooks/investigation.md) |
| requirement clarification or domain decisions | [shaping](playbooks/shaping.md) |
| architecture or interface decision | [design](playbooks/design.md) |
| implementation plan, spec, or work breakdown | [plan](playbooks/plan.md) |
| reported defect or regression | [bug fix](playbooks/bug-fix.md) |
| new or changed behavior | [feature](playbooks/feature.md) |
| behavior-preserving structural work | [refactor](playbooks/refactor.md) |
| measured speed, memory, or capacity problem | [performance](playbooks/performance.md) |
| disposable empirical decision | [prototype](playbooks/prototype.md) |
| deployment, migration, configuration, live state | [operational change](playbooks/operational-change.md) |
| review of an existing change | [review](playbooks/review.md) |
| interrupted or inherited work | [resume](playbooks/resume.md) |
| operator-away or multi-checkpoint mission | [long run](playbooks/long-run.md) |
| skill, prompt, or workflow comparison | [workflow evaluation](playbooks/workflow-evaluation.md) |

Use explicit deliverable and mutation boundaries first. Otherwise choose the
primary route in this order: read-only investigation, workflow evaluation,
operational mutation, measured performance, established-behavior bug, invariant
refactor, then feature. Shaping, Design, Plan, and Prototype are primary only
when they are the requested deliverable. Resume and Long run modify the selected
primary route and return to its first unmet gate.

Put every numbered playbook step into the active task checklist. A skipped step
remains visible as `skip: <evidence-based reason>`. Do not advance past a phase
whose completion condition is unmet.

## Choose earned rigor

- **Direct:** local, reversible work with a known path. One grounded pass, one
  complete change, and final proof.
- **Deliberate:** uncertain intent, a changed boundary, meaningful blast radius,
  or an expensive reversal. Add independent evidence or alternatives and an
  independent review.
- **Program:** work spans independent units, checkpoints, or an operator absence.
  Add durable unit state, a pilot, evidence receipts, and explicit stop rules.

Rigor follows uncertainty, reversibility, and impact. Fan-out must improve
coverage, elapsed time, or falsification. Do not add ceremony to a task whose
shape and proof are already obvious.

## Invoke capabilities explicitly

Playbooks may call these reusable skills:

- `investigate` traces mechanics, history, and competing explanations;
- `shape` resolves decision dependencies and domain meaning;
- `architect` settles caller usage, state ownership, interfaces, and seams;
- `prototype` answers one observable question with disposable code;
- `orchestrate` creates isolated work units and integrates their receipts;
- `verify` maps acceptance claims to fresh checks on the final artifact;
- `review` independently tests intent, engineering, and proof quality;
- `resume` reconstructs the current state without repeating settled work;
- `reflect` promotes repeated lessons into the narrowest effective control;
- `workflow-eval` compares workflow variants under blinded conditions.

Use the host's native skill mechanism and invoke one named skill at a time. A
load-bearing call is complete only after the target instructions were actually
loaded and its required receipt exists. If the host has no skill mechanism but
the plugin source is readable, read the target `SKILL.md` in full. A bare mention
of a skill name is not execution.

## Orchestration boundary

R-Stack owns work decomposition, role separation, dependencies, write
ownership, brief quality, evidence receipts, synthesis, and integration. It
does not choose or recommend executor configuration. Preserve configuration
provided by the operator or harness. If subagents are unavailable, execute the
same work graph in dependency order and retain the same receipts.

The coordinator owns the final verdict. Agent reports are leads until their
evidence and accepted diffs are checked.

## Completion gate

Before declaring completion:

1. Reconcile every acceptance claim with a verification receipt.
2. Confirm the receipt was produced after the last relevant mutation.
3. Inspect the final diff and current workspace for scope drift.
4. Report `complete`, `inconclusive`, or `blocked` without upgrading uncertainty.

`complete` means the outcome and proof both exist. `inconclusive` means a
named claim remains unproven and delivery depends on the active risk policy.
`blocked` means no safe in-scope path remains without new input or an external
change. Use
[workflow metrics](references/metrics.md) for retrospective analysis, not as a
substitute for the task's acceptance criteria.
