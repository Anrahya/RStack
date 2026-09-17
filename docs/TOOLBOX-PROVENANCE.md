# Toolbox provenance and deliberate differences

Inspected on 17 September 2026. P-stack source is the `pstack/` directory in
`cursor/plugins`, at repository revision `e31650eea443aaea1e84cc15d88c13f40080b275`.
The source files below were read in this conversation through the GitHub connector;
several were already read in the preceding utility discussion. The branch revision
was rechecked before the adaptation. These are adaptations, not byte-identical
copies, and they do not imply upstream review or endorsement.

The original P-stack copyright and MIT notice are retained in
`licenses/pstack-MIT.txt`. Original R-Stack and Matt Pocock notices remain unchanged.
When extracting utilities individually, retain the applicable upstream notice too.

## Read sources and adaptation

Each name links to the inspected upstream skill entry.

| Source skill | Treatment here |
| --- | --- |
| [bro](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/bro/SKILL.md) | Keep the plain-language restatement; explicitly preserve uncertainty and disallow unnecessary tool use. |
| [unslop](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/unslop/SKILL.md) | Keep pattern-based editing, remove global applicability and categorical punctuation bans. |
| [technical-writing](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/technical-writing/SKILL.md) | Retain purpose, reader and clarity guidance; no forced style pipeline or universal tabs. |
| [teach](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/teach/SKILL.md) | Expand to general learning; optional investigation helpers and diagrams, no mandatory chain or forced pacing. |
| [how](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/how/SKILL.md) | Keep mechanism tracing; support non-code topics and direct execution without mandatory delegates. |
| [why](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/why/SKILL.md) | Keep uncertainty and historical intent separation; distinguish scientific mechanism, empirical diagnosis and recorded motivation. |
| [recall](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/recall/SKILL.md) | Keep scoped context reconstruction; remove Cursor transcript paths, default model choices and automatic resumption. |
| [show-me-your-work](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/show-me-your-work/SKILL.md) | Keep public decision evidence; logging only when requested. New Python helper, no mandatory cross-model audit or commits. |
| [automate-me](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/automate-me/SKILL.md) | Keep evidence-backed preference capture; draft or authorized edit, no automatic installation, mode activation or PR. |
| [reflect](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/reflect/SKILL.md) | Adapt existing R-Stack reflect to a standalone-safe retrospective; no fixed panel or automatic tracker writes. |
| [blast-radius](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/blast-radius/SKILL.md) | Keep consequence tracing and evidence levels; multiple safety assumptions, no mandatory arena or production mutations. |
| [typescript-best-practices](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/typescript-best-practices/SKILL.md) | Keep focused type guidance, remove automatic path triggers and absolutist cast/logging rules. Local examples are newly written. |
| [no-comments](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/no-comments/SKILL.md) | Deliberately safer comment review. Keep useful rationale and ambiguous constraints; no automatic Comment Sicko or architecture chain. |
| [tdd](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/tdd/SKILL.md) | Retain practical red/green behavior checks without forcing poor tests or authorizing resets. |
| [create-verification-skill](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/create-verification-skill/SKILL.md) | Retain launch/doctor/drive/evidence/cleanup; host-neutral destination and honest draft status. |
| [maintain-verification-skill](https://github.com/cursor/plugins/blob/e31650eea443aaea1e84cc15d88c13f40080b275/pstack/skills/maintain-verification-skill/SKILL.md) | Retain drift and live-path audit, remove automatic PRs and default per-feature subagents. |

`research` is a new R-Stack utility, informed by the earlier source-aware research
lens and this user's knowledge-work needs. It is not presented as an upstream
P-stack command. Original referenced principle skills and proprietary host prompts
were not copied as unresolved dependencies. Local guides are newly authored,
self-contained adaptations; no external skill is required for the toolbox to load.

## Not imported as extra utilities

`poteto-mode` and `setup-pstack` remain upstream-specific. `architect`, `arena`,
`swarm`, `interrogate` and bespoke workflow synthesis are outside this bounded
utility import and overlap R-Stack's engineering capabilities. `make-bot-ui` is an
integration-specific workflow, not a general knowledge helper. The 23 principle
skills are not installed as 23 additional standing instructions.

## Host-format sources checked

- Agent Skills specification: https://agentskills.io/specification
- Claude Code skill discovery and namespace: https://code.claude.com/docs/en/skills
- OpenAI skill metadata and invocation policy:
  https://developers.openai.com/codex/skills
  (redirects to https://learn.chatgpt.com/docs/build-skills)

The toolbox keeps standard name/description/license/metadata fields and does not
set `disable-model-invocation`, `paths`, sticky-mode flags or permission grants.
The Codex adapters explicitly allow implicit invocation. Host support and namespaced
menus still require a native loading test; format conformity is not that test.
