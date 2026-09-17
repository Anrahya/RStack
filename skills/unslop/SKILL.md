---
name: unslop
description: "Edit supplied writing to remove filler, vague claims and mannered AI prose while preserving meaning and the requested tone."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: scoped-edit
---

# Unslop

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Edit the text the user supplied or identified. Use the preceding answer when that
is the clear target. This is an editing operation, not an instruction to rewrite
every future response or every file in the repository.

## Edit in place of the bad pattern

Read [the pattern guide](references/patterns.md) when the text needs more than a
small cleanup. Cut empty framing, inflated vocabulary, formulaic contrasts,
repetitive summaries, flattering openings and decorative formatting. Replace an
abstract claim with its existing concrete mechanism or measurement, not an invented
one. Keep a useful technical word when it is the precise word for this audience.

Preserve the intended voice, substance, structure where requested, citations,
numbers, units, dates, qualifications and uncertainty. Do not convert "may" to
"will" or "not tested" to "works". A citation is not proof that you opened it.
Do not invent attribution to fix "experts say"; flag it or preserve it as explicitly
unsupported. Distinguish an editor's correction from a new factual claim.

Prefer natural punctuation and varied sentence lengths over rigid word bans.
Do not remove every dash or colon, force a word limit, erase personality, or turn
complete sentences into clipped fragments. Follow an explicitly requested house
style, including stricter punctuation preferences, when supplied.

Read the revision once for meaning loss and once for awkwardness. Return the edited
text, not a lecture about slop. Flag only substantive ambiguities or apparent factual
errors that cannot be fixed honestly from the provided material. Editing a named
file is allowed only when requested; otherwise return the revision in chat.
