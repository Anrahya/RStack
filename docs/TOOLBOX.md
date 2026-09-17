# The optional R-Stack toolbox

R-Stack has two entry paths. **Mode** runs a verification-driven engineering task.
**Utilities** give focused help with communication, learning, research or development.
Calling a utility does not call the mode. None is an always-on output filter.

## Choose the help you need

| Skill | Use it for |
| --- | --- |
| `bro` | Restate a dense answer plainly, without extra research or workflow steps. |
| `unslop` | Edit identified prose while preserving its meaning, voice and uncertainty. |
| `technical-writing` | Write or review guides, explanations, RFCs and other technical documents. |
| `teach` | Learn a concept, paper or system at the requested level and pace. |
| `how` | Understand a mechanism or trace how a system works. |
| `why` | Investigate causes or documented intent without inventing motivations. |
| `research` | Research a question or compare options using source-aware evidence. |
| `recall` | Recover scoped working or learning context, without resuming the work. |
| `show-me-your-work` | See a public rationale and evidence, or keep a requested decision log. |
| `automate-me` | Draft reusable preferences without installing or activating them automatically. |
| `reflect` | Review a session and suggest useful lessons. Also usable by an existing workflow. |
| `blast-radius` | Examine what a change could break beyond the diff. |
| `typescript-best-practices` | Get scoped TypeScript design or review help. |
| `no-comments` | Remove comment clutter while retaining useful explanations and directives. |
| `tdd` | Use a focused red/green test-first loop for authorized implementation. |
| `create-verification-skill` | Create and exercise a project-specific launch/drive/check recipe. |
| `maintain-verification-skill` | Audit or repair an existing recipe and feature map. |

All seventeen are model-discoverable and user-invocable on hosts supporting the
corresponding skill mechanism. Selection is discretionary: the model may choose
one for the actual request, but no rule requires running a utility on every answer.
`toolbox.json` records the intended separation; it is metadata, not a runtime router.

## Examples

```text
/bro
/unslop this explanation, but keep the technical caveats
/teach entropy assuming undergraduate physics
/how does TCP congestion control work?
/why did this project use a queue here?
/research compare these papers and identify what their experiments establish
/recall where we left off on the caching discussion
/show-me-your-work explain the decision and the evidence behind it
/reflect what made this research session inefficient?
/no-comments review this diff; do not edit it
```

These are conceptual short command names. Actual host syntax can be namespaced.
Claude Code plugin skills use `/r-stack:bro` and `/r-stack:teach`; `$bro` is the
Codex-style skill reference. Cursor exposes the installed plugin's skills and
command wrappers; verify the menu in the actual installed host. Do not assume every
host supports the same unqualified slash command or that two plugins named `bro`
resolve identically. Use the R-Stack-qualified entry when P-stack is also installed.

## A utility inside an engineering session

```text
User: Use R-Stack to fix the persistence bug.
Agent: [works on the authorized engineering task]
User: /bro
Agent: [restates its previous answer, then stops]
User: Continue the fix.
Agent: [returns to the retained engineering task state]
```

The utility turn does not run tests, create receipts or continue implementation.
It also does not erase the task state or permanently switch off R-Stack. A request
that explicitly says "explain this, then continue" authorizes both deliverables.

General learning and research do not require a code repository. Launching the agent
inside one does not transform every question into an engineering assignment.

## What remains required

Truthful sourcing, preserved uncertainty, permissions, privacy and safe handling of
user-owned work still apply. Optional does not mean "ignore evidence". It means no
mandatory workflow ceremony. A mutation-capable utility only edits the authorized
scope; selecting it does not grant permission to commit, publish or deploy.

There is no automatic `unslop` pass, mandatory `how`/`why` chain for `teach`, model
panel, transcript sweep or permanent style change. Larger utilities have local
references; small utilities such as `bro` remain self-contained.

## Validate and try

```bash
python3 scripts/check_toolbox.py
python3 -m unittest discover -s tests -v
```

The checker validates declared invocation policy, paths, adapters and dependency
boundaries. It does not prove that an LLM will obey the text or that a native host
loads it. Use [the interaction cases](../evals/toolbox-cases.json) for live trials
and [the test guide](TOOLBOX-TESTING.md) for what to observe.

Source design and deliberate differences are recorded in
[the provenance notes](TOOLBOX-PROVENANCE.md).
