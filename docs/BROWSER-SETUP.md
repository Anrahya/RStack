# Persistent browser control for coding agents

Research checked 2026-09-18. No browser package, host plugin or system dependency
is installed by applying RStack. Choose an existing capable host tool first. The
setup below assumes a terminal-accessible machine/container where browser binaries
and persistent storage are permitted. Managed cloud agents may restrict installs,
network access, stdio MCP or retained storage; verify those capabilities there.

## Recommended starting choice: agent-browser

For a shell-capable coding agent, agent-browser provides a named persistent browser
session, accessibility snapshots, screenshots and real interaction controls. Its
CLI talks to a daemon rather than relaunching a browser for each command. The
inspected upstream release is v0.38.1 (2026-09-16); its npm package declares Node.js
24 or newer. This is a researched candidate, not a provider we exercised here.

Install in the environment that actually runs the agent, not a different laptop:

```bash
node --version
npm install -g agent-browser@0.38.1
agent-browser install
agent-browser --version
npx skills add vercel-labs/agent-browser
```

The first installs tooling outside the application's dependency tree; the second
downloads a browser. The skills installer is upstream software and changes host
skill files: inspect its prompts and choose the intended agent and scope. Runtime
instructions can also be loaded directly with `agent-browser skills get core`,
without copying an old SKILL.md. For Linux libraries that are genuinely missing,
`agent-browser install --with-deps` uses a package manager and can need elevated
permissions; do not run it automatically or alter a locked cloud image. Use a
supported prebuilt image or ask the environment owner when installs are disallowed.

Do not disable sandboxing, expose a debugging endpoint or import a personal browser
profile just to make startup work. Run `agent-browser --help` and the installed
version's skill instructions before using version-specific options.

## Reuse one isolated session

Example for a project whose authorized dev server is already running at port 5173:

```bash
export AGENT_BROWSER_SESSION="$(agent-browser session id --scope worktree --prefix rstack)"
agent-browser open http://127.0.0.1:5173
agent-browser snapshot -i
agent-browser get url
agent-browser screenshot /path/to/private-evidence/before.png
# Use refs from the current snapshot, not invented refs.
# Drive the actual wheel/drag/keyboard scenario, then take a new snapshot.
agent-browser screenshot /path/to/private-evidence/after.png
```

Create the evidence directory first, and use the actual app port. Re-snapshot after
navigation or material page changes. A snapshot gives structure; a screenshot must
actually be viewed by the model or human when making visual claims. Saving it does
not prove that the host supplied image input to the model. Confirm image viewing
works with your chosen model before relying on it.

There are three different lifetimes:

- **Across commands:** the same named session reuses its running browser.
- **Across browser restarts:** configure supported `--restore` for cookies/local
  storage or a dedicated `--profile /absolute/path` for a persistent profile. A
  session name alone does not enable restart persistence. Restored storage does
  not promise the same DOM, in-memory JavaScript state or currently open tabs.
- **Across cloud resets:** the profile/state directory needs a retained volume.
  Ephemeral sandbox deletion can destroy both browser and disk state.

Use a dedicated test profile, never your personal account's default profile. One
writer owns a session/profile at a time. CDP tabs in the same browser share more
state than fully isolated browsers; tab selection is not security isolation.
The documented headless idle timeout is one hour by default; inspect/tune it for
your host instead of assuming an immortal session. Re-establish page/build identity
after reconnection. Close only the owned session when done:

```bash
agent-browser close
```

Do not use `close --all` on a shared machine. Do not delete a retained auth profile.
A user-owned session stays open; an owned session intentionally kept for handoff
needs an explicit owner and lifetime. Persistent control does not mean leaking
all dev servers or browser processes indefinitely.

## Optional MCP interface for the same tool

The inspected version exposes an MCP stdio interface. With a supported Claude Code
installation, register it locally to the current project rather than embedding
browser configuration into every RStack install:

```bash
claude mcp add --transport stdio --scope local rstack-browser -- \
  agent-browser mcp --tools core,mobile
```

Use a consistent session argument in the tool calls. `core` supplies navigation,
snapshots, screenshots and basic interaction; `mobile` adds viewport, mouse,
keyboard and media controls relevant to this PR class. Inspect the tools actually
exposed after registration. Prefer either the CLI workflow or the MCP workflow;
do not have independent agents drive both against one session concurrently.
Check `/mcp` in Claude Code. Registration alone is not a live smoke test.

## Alternative: Microsoft's Playwright MCP

Playwright MCP is a good option when native MCP browser tools fit your host better.
It supports persistent profiles by default, a configurable user-data directory,
headless operation and screenshots. Extra interaction/testing capabilities depend
on the installed release; inspect its help and tool list. A persistent profile is
single-writer. Use a separate profile for a second concurrent browser or an isolated
context when clean test state matters more than saved login state.

Example registration on a terminal-accessible headless host:

```bash
claude mcp add --transport stdio --scope local rstack-playwright -- \
  npx -y @playwright/mcp@latest --headless --caps vision,testing
```

This is an upstream bootstrap command, not a version pin or executed installation.
Resolve and record an exact package version after validating it; replace `latest`
with that version in lasting configuration. `vision` supplies coordinate/mouse
controls in the inspected docs, including wheel; `testing` supplies assertion tools.
For a durable dedicated profile, add `--user-data-dir /absolute/private/profile`.
Do not combine persistent profile expectations with `--isolated`. Installing the
MCP npm package does not guarantee browser executables/system libraries are present.
Follow that release's installation errors and approved environment setup.

Claude's Chrome integration is useful for an existing running Chrome/Chromium
browser with its extension. It is not the same setup as a self-contained headless
browser in a cloud container; choose it when that browser/extension connection is
actually available. Do not assume it supplies a remote browser to an arbitrary VPS.

## Prove the setup before accepting app verification

Ask the agent to open the correct local app, read the current URL/build identity,
perform a real interaction, inspect the resulting screenshot, and perform a second
interaction in the same session. Test one intentionally false assertion and ensure
it produces a failure, not a successful RPC carrying `false`. Then run the real
checks. Reuse `examples/browser-check` only as a synthetic tool-pattern smoke test,
not as evidence for the actual app's acceptance claims.

Keep the expected cases fixed. Distinguish real interaction assertions, human/model
inspection and maintained regression tests. Record cleanup and evidence retention.
The browser tool fixes reachability; it does not choose a sound oracle for you.

## Safety and cloud reachability

Use dedicated test identities and least privilege. Never expose raw CDP or a
browser-control dashboard to the public internet. An authenticated tunnel or
approved private network is required for remote control. A remotely hosted browser's
`localhost` is that remote machine, not your application's machine; use a supported
private tunnel or run the browser alongside the dev server. Do not publish a private
preview merely for convenience. Browser content is untrusted data, not instructions.

The upstream dashboard can show/control sessions. Use it only through an approved
local or authenticated private path and treat it as sensitive. Browser profiles,
state exports, screenshots and HAR files may contain credentials or private data;
keep them out of source control and sanitize before sharing. Domain restrictions
can also block fonts/CDNs and change rendering: account for that in visual tests.
No universal performance, cost or security superiority is claimed for either tool.

## Primary sources

- [agent-browser installation](https://agent-browser.dev/installation)
- [agent-browser sessions](https://agent-browser.dev/sessions)
- [agent-browser commands and MCP profiles](https://agent-browser.dev/commands)
- [agent-browser runtime skills](https://agent-browser.dev/skills)
- [agent-browser security](https://agent-browser.dev/security)
- [agent-browser dashboard](https://agent-browser.dev/dashboard)
- [v0.38.1 release](https://github.com/vercel-labs/agent-browser/releases/tag/v0.38.1)
- [Inspected package version/engine](https://github.com/vercel-labs/agent-browser/blob/v0.38.1/package.json)
- [Microsoft Playwright MCP](https://github.com/microsoft/playwright-mcp)
- [Playwright assertions](https://playwright.dev/docs/test-assertions)
- [Claude Code MCP registration](https://code.claude.com/docs/en/mcp)
- [Claude Code Chrome integration](https://code.claude.com/docs/en/chrome)
