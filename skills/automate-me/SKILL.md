---
name: automate-me
description: "Draft reusable preferences or a personal skill from explicit instructions and recurring work patterns. Does not enable a mode or install rules automatically."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: scoped-edit
---

# Automate me

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Turn demonstrated preferences into a small reusable draft. This includes how the
user learns, researches, writes and develops software; it is not limited to coding.

Read the preferences explicitly supplied and relevant history already authorized
for this topic. Scope history access before mining; do not inspect every project
or account. Inspect an existing named skill before proposing to replace it. Do not
load another author's mode as a template for this user's personality.

Distinguish explicit preferences from inferred patterns. A clear current request
is authoritative even if stated once. Inferred habits need repeated evidence and
must not overrule an explicit correction. Preserve context-specific preferences:
a request for a short answer today is not a global ban on thorough explanations.

Propose only non-default rules that change a future decision. For each, retain its
trigger, desired behavior and basis. Point to an existing relevant skill rather
than copying its entire contents. Resolve contradictions and remove redundant rules.
A one-off observation can remain a suggestion rather than a permanent instruction.

Draft a compact SKILL.md with a precise name and description, invocation boundaries,
and any actual supporting references. A personal style or mode draft defaults to
explicit invocation; making it automatic is a separate user choice. Use the host's
actual supported configuration, not guessed file paths or tool names.

Return the draft and genuinely unresolved choices. Write or update the specific
file only when authorized; creating a draft does not authorize global installation,
editing AGENTS.md, changing R-Stack, commits, PRs or permanent memory. Existing
authorization is enough: do not ask for approval again for an explicitly requested
bounded file edit. If the draft is saved, check its syntax and references and report
what was saved versus actually loaded by a host.
