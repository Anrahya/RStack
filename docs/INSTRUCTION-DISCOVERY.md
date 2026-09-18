# Find instructions for the actual edit scope

Run from anywhere, pointing at the project root and exact planned file paths:

```bash
python3 /path/to/RStack/scripts/find_instructions.py --root /path/to/project \
  surfaces/control-room/src/work.tsx surfaces/control-room/src/agent-map.tsx
```

Paths after `--root` are relative to that root, not the current shell directory.
New and deleted files work because their ancestors still carry instructions.
For an intended directory, pass `--directory surfaces/control-room`; that finds
instructions governing the directory itself, not every nested package. Expand
it to actual file paths before changing files deeper inside. No glob discovery,
content interpretation, mutation, network call or command execution occurs.

Read applicable candidates in context. The list includes conventional directory
instructions and `.claude/rules` / `.cursor/rules` candidates on those ancestors.
Conditional rule files are candidates, not a claim that all their path predicates
match. User/managed instructions, repository-specific names, imports and host
precedence still need host/project inspection. Do not infer that an empty list
means no instructions apply. An outside-root symlink or unreadable path produces
exit 2 rather than a silently incomplete list. Internal symlink aliases are named.

When the edit scope expands, run discovery for the additional paths and read new
applicable instructions. Keep only task-relevant constraints visible in the task,
but do not summarize instructions that were never read.

## Claude Code setup

Claude Code documents automatic `CLAUDE.md` loading and imports, but not automatic
`AGENTS.md` loading. Where the project uses `AGENTS.md`, merge the following into
an existing `CLAUDE.md` or create it when authorized. Do not overwrite existing
instructions or replace a symlink target without inspecting it.

```markdown
@AGENTS.md

For non-trivial engineering work, load the installed RStack r-stack-mode skill
before editing. The r-stack command is an alias of the same workflow.
Read the project instructions governing the files being changed, including
applicable nested AGENTS.md and CLAUDE.md files and referenced package rules.
Standalone utility requests run only that utility and do not start or resume
engineering work unless I explicitly request both deliverables.
```

Use the actual skill identifier exposed by the installed host. Import `AGENTS.md`
only where it exists. Confirm loading with Claude Code's `/context` rather than
assuming that writing a file changed the current session. A plugin's prose saying
"default" cannot load itself into a host that has never discovered it. Instructions
are not enforced configuration; no stop hook is installed by this upgrade.

Source checked 2026-09-18: [Claude Code memory documentation](https://code.claude.com/docs/en/memory).
