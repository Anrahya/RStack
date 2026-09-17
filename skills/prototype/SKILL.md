---
name: prototype
description: Build a disposable experiment to answer one observable engineering or product decision. Use for uncertain behavior, timing, feasibility, compatibility, interaction, or layout questions when evidence is cheaper than abstract debate.
---

# Prototype

The deliverable is a decision and its evidence. Prototype code is an instrument,
not the production implementation.

1. State the exact question, alternatives, held conditions, observation, and
   decision rule before building.
2. Isolate the experiment from production source in a temporary directory,
   disposable worktree, or explicit experiment area.
3. Build only what is needed to observe the answer. Skip production abstractions,
   compatibility layers, and polish.
4. When comparison matters, hold the workload and environment constant. Change
   only the variable being evaluated.
5. Exercise the matching surface and capture the action plus resulting state,
   output, timing, trace, or screenshot.
6. Repeat enough to distinguish signal from noise when timing or nondeterminism
   matters.
7. Return a decision receipt: question, alternatives, artifact, action,
   observation, decision rule, result, limitation, and recommended direction.
   Remove or clearly quarantine the disposable artifact.

Route the chosen direction back to `architect` for a boundary decision
or the active implementation playbook for production work.
