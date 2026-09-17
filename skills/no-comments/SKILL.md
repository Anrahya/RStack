---
name: no-comments
description: "Review comments for redundancy, staleness and useful rationale. Remove only safe, requested clutter; never enforce zero comments."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: scoped-edit
---

# Comment review

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

The name is a shortcut, not a zero-comments quota. Keep comments that convey
necessary information the code does not. The requested scope and project policy
matter more than a general style preference.

For a review request, report findings without editing. For an explicit comment
cleanup request, inspect the named files or diff and make only the authorized,
behavior-preserving edits. Do not assume the base is main; resolve the actual scope.

Keep license and attribution notices, public API documentation, safety warnings,
non-obvious rationale, protocol constraints, workarounds with their external cause,
generated-file markers, tool directives and justified suppression explanations.
Check what a directive does before removing it. An ambiguous invariant stays until
its meaning is understood; uncertainty is not a reason to delete it.

Remove or propose removal of comments that narrate obvious syntax, repeat the code,
misstate current behavior or contain obsolete temporary notes. A stale warning needs
investigation, not blind deletion. Never edit literals, URLs, regular expressions,
template strings or docstrings using a global "remove comments" regex.

When a comment exposes a design problem, describe the behavior or invariant that
needs attention. Suggest a type, test or clearer name when it genuinely helps,
but do not widen a comment-only task into a refactor or full architecture workflow.
A missing enforcement mechanism does not justify deleting the only explanation.

Check the resulting diff for semantic changes and run applicable project checks
when edits are authorized. Return important removals, retained rationale, unresolved
questions and actual validation. Do not delegate to an unavailable named reviewer,
force a model switch, invent deletion counts or optimize for the fewest comments.
