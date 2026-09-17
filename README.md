# R-Stack 0.2.0-rc.3

A host-neutral engineering workflow with an optional toolbox for learning, research,
writing and focused development help. The fourteen engineering routes remain; the
seventeen utility entry points run independently. This release is an **evaluation
candidate**, not a measured claim of model uplift.

## Two independent ways to use it

R-Stack is the default route for engineering work in a repository: bug fixes,
features, refactors, migrations, architecture and design decisions. It stays out
of general chatter, quick questions, teaching and standalone utility requests.

Use `r-stack-mode` for verification-driven engineering. Use `bro`, `teach`, `research`,
`unslop` or another [toolbox skill](docs/TOOLBOX.md) for focused help. A toolbox call
does not start or resume mode, load the work profile, or add workflow receipts.
Utilities are available to the model but optional, not always-on rules.

For a previously active engineering task, a utility turn leaves its state paused.
The next separately requested engineering action can resume it. Ordinary knowledge
questions do not enter mode merely because the agent is running inside a repository.

## Operating principle

Establish the requested outcome and proof. Ground consequential decisions in the
actual project or primary sources. Do the smallest complete work. Verify the final
relevant artifact. State what was not established. Use extra process only when it
addresses a particular uncertainty, risk or coordination need.

Start by asking the host to use the `r-stack-mode` skill. The router reads project
constraints, chooses one primary playbook and adds only relevant capabilities.
The active host retains permissions, executors, resource limits and isolation.
Native skill syntax varies by host; installing files alone does not demonstrate
that the host loaded or invoked them.

## What changed in rc.3

- R-Stack is the default route for engineering work rather than an opt-in one. The
  mode skill, work profile and README now state the boundary: code, configuration,
  data or a documented decision is engineering work; general chatter, quick
  questions, teaching, prose editing and standalone utilities are not.

## What changed in rc.2

- Sixteen new standalone skills, plus a standalone-safe revision of existing `reflect`.
- A dedicated `research` utility and broader general-knowledge `teach`, `how` and `why`.
- An explicit utility exception in the entry rule, router and engineering profile.
- No new mandatory utility phases, model defaults, automatic editing or publishing.
- A tested decision-log helper, static toolbox checks and live interaction cases.

The evidence recorder, receipt semantics and engineering playbooks are unchanged
from rc.1. See [the toolbox guide](docs/TOOLBOX.md) and its validation limits.

## What changed from 0.1

- A smaller contract-first entry path, explicit capability gaps, bounded recovery
  after repeated unproductive attempts, and honest review provenance.
- Six optional lenses: UI/UX, research, state/integration, security,
  migration/delivery and data analysis. No expansion into dozens of default phases.
- Schema-2 graphs and receipts, actual command capture, per-claim final-state
  identity checks, artifact hashes and negative tests for false completion.
- Safer Cursor copying, a portable entry rule, version-consistent package checks,
  executable smoke fixtures and an outcome/cost evaluation protocol.

Read [the evidence contract](skills/r-stack-mode/references/evidence-contract.md),
[worked examples](docs/WORKED-EXAMPLES.md), [evaluation protocol](docs/EVALUATION.md),
and [migration notes](docs/MIGRATION-0.2.md).

## Workflow versus enforcement

**Instruction mode** guides the agent and works with its ordinary tools.
**Capture mode** records real checks and verifies record consistency using the
optional Python scripts. **Host-enforced completion** requires the host or CI to
run a protected gate and refuse unsupported closure. This plugin does not install
universal stop hooks, a scheduler, a sandbox or a new agent loop.

The recorder requires Python 3.10+ and Git for local snapshots. POSIX process
cleanup was exercised in the supplied tests; native Windows descendant handling
and live host loading were not. Inspection and judgment records can preserve
source or screenshot attachments, but the scripts do not judge images or prove
semantic correctness. A malicious or mistaken agent that owns the checks and
records can still produce self-consistent bad evidence.

## Local checks

```bash
python3 -B -m unittest discover -s tests -v
python3 scripts/check_portability.py
python3 scripts/check_toolbox.py
python3 evals/smoke.py self-test
```

The original schema-1 JSON fixtures remain historical examples; they are not the
new test suite and must not be reused to certify schema-2 completion.

The runnable [recorded-check example](examples/recorded-check/README.md) shows the
capture path without any model calls. Evidence tools execute the commands in a
contract: review those commands and use the host's permissions and sandbox.

## Installing the supplied upgrade

The accompanying bundle is a cumulative overlay, not a complete standalone clone.
Its applicator supports the audited 0.1 base and the exact supplied rc.1 files. It
defaults to a dry run, rejects unexpected target edits, and retains recovery copies.
It never commits, pushes or resets your repository. Read the bundle README and review
the proposed file list. Unrecognized revisions require a reviewed port.

For an existing local Cursor plugin copy, `scripts/install-cursor.sh` stages a
replacement, retains the prior copy, and refuses unrecognized targets. Running
it from the installed location does not delete that location. A successful copy
is not a successful native Cursor loading test.

## Provenance

R-Stack remains derived from its existing P-stack and Matt Pocock skill
inspirations. Preserve `UPSTREAM.md`, `LICENSE`, and `licenses/` from the original
repository. This revision adds independent analysis and code; it does not claim
upstream authors reviewed or endorsed it. See `docs/AUDIT-PROVENANCE.md`.
