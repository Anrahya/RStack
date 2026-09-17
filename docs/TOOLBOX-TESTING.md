# Toolbox validation and live trials

The local tests establish packaging invariants and behavior of the decision-log
helper and upgrade applicator. They do not execute an LLM or simulate genuine skill
selection. No model compliance, learning effectiveness or research quality result is
claimed from string checks.

## Local checks

```bash
python3 scripts/check_toolbox.py
python3 -m unittest discover -s tests -v
python3 scripts/check_portability.py
```

When validating the distribution overlay without a complete source checkout, use
`check_portability.py --root payload --retained-manifest manifest.json` from the
bundle root. That explicitly acknowledges retained files rather than inventing them.
Run the ordinary full-package command after applying to the actual checkout.

## Live interaction trials

`evals/toolbox-cases.json` contains 31 unrun scenarios, covering all seventeen
utilities, explicit and implicit selection, an active-mode interruption, general
knowledge without a repository, unavailable evidence, privacy and mutation scope.

For each trial, record host/version, executor configuration, loaded skill name,
user prompt, output, actual tool calls, files changed and whether the expected
boundary held. Run important cases both in a fresh conversation and in an active
R-Stack engineering session. Check the actual transcript rather than trusting the
agent's statement that it did not start a mode.

Start with `bro-active-mode`, `teach-physics`, `unslop-uncertainty`, `research-no-access`,
`recall-scope` and `native-menu`. Also test the next engineering turn after `/bro`:
it should resume only when separately requested, with prior state intact.

For native host discovery, verify the R-Stack-qualified menu entry resolves to the
intended skill even with P-stack installed. Do not infer short-name aliases or
plugin loading from JSON/YAML validity alone.

## Pass criteria

The utility answers the actual request, preserves material facts and uncertainty,
uses sources honestly, respects scope and does not invoke mode as a side effect.
No tool calls are needed for an ordinary `/bro` restatement. Mutation-capable
utilities must distinguish an advice/review request from authorization to edit.

Optional selection is not a failure to obey a mandatory process: for a natural
question with no explicit utility, direct competent answering is acceptable too.
When the user explicitly invokes one, verify it was actually loaded.
