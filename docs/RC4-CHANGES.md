# R-Stack 0.2.0-rc.4

This revision responds to the first usage review, not a measured capability uplift.
The source review covered rc.2 on four Renoa UI findings. The repository already
contained rc.3 at `0b03dfb365bdb5a974cc5f09f882ccbbf8c57e4d`; its default-engineering
scope and the canonical evidence hardening are preserved. The RC4 input archive
had SHA-256 `4612fc26c1cf658ac2167db3501692a4ee60c681c17bd593d6350f36435351dd`.
The canonical release applies its reviewed 34-path patch rather than replacing
the repository with the archive's incomplete cumulative payload.

## Host packaging

ZCode is a primary supported host in RC4. The repository now carries a native
`.zcode-plugin/plugin.json` plus a root `marketplace.json`, so the GitHub repository
can be added directly as a ZCode marketplace. The marketplace and all four host
manifests use the same version and are checked together. ZCode, Claude Code and
Codex installations remain host-managed runtime copies; source-tree validation
does not claim a running session has reloaded them.

## Execution changes

Instruction discovery follows actual intended edit paths, root to package, and
repeats when scope expands. The optional finder lists conventional instruction
candidates; it does not read their content or interpret host precedence. Import
and managed-rule discovery remains the host/agent's responsibility.

Direct is the default for bounded work. Additional checks address named risk;
Program organization requires durable coordination. A small request with four
bugs does not become a program because it has four acceptance claims. Receipts,
subagents and extra approval are not mandatory.

Bug fixing loops per defect. Establish each baseline and mechanism before the
corresponding fix, or disclose an actual reproduction limitation. Retrospective
reconstruction remains useful evidence but must be labelled accurately. Preserve
the original dirty worktree instead of resetting the user's files to HEAD.

The ordinary verify skill now owns meaningful command failure, not a buried
optional recorder document. New checks need a known failing control. Printing
`pass: false` and exiting zero is not a passing assertion gate. The optional
case-result helper checks a fixed externally supplied case list and propagates
failed/missing cases. It does not prove those reports are authentic or sufficient.

Current proof is separate from maintained regression protection. Existing tests
can cover one claim while an authorized one-off browser probe covers another.
Missing reachable tooling keeps a claim unverified. A one-off need does not
authorize installing a new project framework. Retention and cleanup are explicit.

UI repairs load interaction, breakpoint, focus and motion checks without requiring
visual redesign. Design/parity work has a separate section. Other domain triggers
remain conditional on the behavior actually changed.

The command is explicitly an alias, the visible contract is short, diagnosis can
be inline when the cause is established, and metrics stay retrospective. The
utility boundary remains: a utility invocation neither starts nor resumes mode.
Existing utilities and evidence schema are preserved; no new global tool hooks.

## Browser tooling

The setup guide compares agent-browser CLI/MCP, Playwright MCP and existing Chrome
integration. It distinguishes a live session, restart state and retained cloud
storage; recommends dedicated profiles and one writer; and explains target identity,
real input, screenshot inspection, failure propagation and cleanup. It includes
opt-in commands, not an automatic browser install or a universal dependency.

A bundled synthetic Playwright Python fixture demonstrates wheel, pan, pause,
keyboard focus and reduced-motion checks, with a deliberately broken resize
control. Optional HTTP mode also checks profile restart. Offline mode excludes
that claim and does not establish app reachability. See the bundle validation
report for what was actually run.

## Limits and next evaluation

The subagent report is secondary evidence. This revision did not replay the raw
Renoa session or retest that PR. Static instruction tests prevent accidental text
regressions; they cannot establish agent compliance. Use the separately supplied
behavioral scenarios in fresh sessions and compare outcomes, costs and trace events.
None of the candidate prompts should see evaluator notes or expected verdicts.

Do not claim that this release makes every agent obey, that a browser was installed
in the user's cloud, or that a receipt hash proves semantic correctness. Native
host loading, live provider integration and model uplift require actual runs.
