---
name: resume
description: Reconstruct and continue in-flight engineering work from transcripts, summaries, branches, diffs, and verification evidence without repeating completed work. Use after handoff, compaction, interruption, or when taking over an existing workspace.
---

# Resume

Own the resume point. A summary is an index; the workspace and cited artifacts
are current-state evidence.

1. Read the latest summary, checkpoint, or relevant messages first. Inspect the
   branch, status, recent commits, diff, active task state, and cited artifacts.
   Scope transcript or session mining to the active project and topic.
2. Reconstruct and reconcile:
   - original task contract and underlying playbook;
   - current gate;
   - accepted `D-###` decisions;
   - complete, active, failed, and abandoned `W-###` units;
   - valid and stale `E-###` evidence;
   - current write owners;
   - exact tree, worktree, build, or live-state fingerprint;
   - blockers and exact next action.
3. Treat prior reports as navigation. Spot-check the evidence only where state,
   fingerprint, authority, or intent may have diverged.
4. Do not repeat completed investigation, reproduction, implementation, or
   validation merely to rebuild confidence. Re-run only proof made stale by a
   later mutation or external change.
5. Stop or re-ground active work whose assumptions or write ownership no longer
   match the live state.

Return one checkpoint capsule to the already-active router. It continues from the
first unmet gate in the underlying playbook. Keep the capsule in task or
host-provided durable state. Create a repository handoff or status file only when
project policy requires one.
