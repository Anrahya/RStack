# rc.4: source-derived findings and design decisions

## Input evidence and limits

The user's `rstack-usage-review.md` describes one Renoa PR session using rc.2 at
`407671c`. It is a secondary review of a transcript and app checks, not those raw
artifacts. This release does not claim to have rerun Renoa PR #26 or inspected the
raw session. In particular, its inconsistent wording about prompted versus
volunteered disclosure is not used to infer intent or honesty.

The current GitHub branch was checked and had advanced to rc.3 at
`0b03dfb365bdb5a974cc5f09f882ccbbf8c57e4d`. That seven-file change makes engineering
mode default and preserves standalone utilities. This revision retains that change
and is numbered rc.4, not a replacement rc.3. Source:
[rc.3 commit](https://github.com/Anrahya/RStack/commit/0b03dfb365bdb5a974cc5f09f882ccbbf8c57e4d).

## Findings translated into changes

| Review-supported issue | rc.4 change | Evidence boundary |
| --- | --- | --- |
| Nested package instructions missed | Ancestor/path discovery before editing; optional read-only finder | Finder lists candidates; it cannot establish they were read |
| Several fixes treated as one baseline sequence | Per-defect reproduce/diagnose/check before corresponding fixes | Restored baseline remains labeled reconstructed |
| Printed failures with successful exits | Assertions at the boundary; explicit missing-case failure; optional JSON report checker | Truthfulness and adequacy are not schema properties |
| Maintained tests cannot reach all UI behavior | Maintained / one-off / unavailable paths and separate coverage reporting | One-off proof is not future regression protection |
| Overlapping rigor descriptions | Direct default; Deliberate specific checks; Program coordination only | No measured cost reduction claimed |
| Unloaded UI lens | Explicit behavioral triggers and behavior/design split | Missing checks are not proof of actual app defects |
| Skill/command ambiguity | r-stack explicitly an alias of r-stack-mode | Native host naming still requires host testing |
| Recorder omitted | Keep recorder optional at all levels | No forced graph for a small PR |
| Temporary tooling/process lifecycle | Reuse owned sessions; identify target; clean up or explicitly hand off | User-owned sessions and credentials remain untouched |
| Orphaned metrics | Link from evaluation/retrospective documentation | No new required metrics-reading phase |

## Outside research

Claude Code documents `CLAUDE.md` imports, path-scoped rules and instruction limits.
This supports a short host entry snippet plus explicit applicable-file discovery,
not a claim that prose enforces execution. See
[the primary memory documentation](https://code.claude.com/docs/en/memory).

Playwright documents retrying assertions for asynchronous page behavior. Browser
recipes therefore prefer assertions and observable readiness over fixed waits or
simply printing values. See [assertions](https://playwright.dev/docs/test-assertions).

Agent-browser and Playwright MCP both document persistent browser/profile options.
[Browser setup](BROWSER-SETUP.md) separates between-command continuity, restart
state restoration and cloud-disk retention; none implies the others. The setup
commands are researched documentation, not executed host compatibility tests.

## Intentional non-changes

No additional utility skills, mandatory receipt recorder, universal independent
review, automatic dependency install, model selection or auto-commit behavior.
No private-transcript reasoning length is treated as measured cost. Prose status
capitalization is not scored; machine interfaces still enforce their schema.
Real task uplift needs controlled runs of agents using the workflow. Static phrase
checks and helper tests are labeled as such; they are not model trials.
