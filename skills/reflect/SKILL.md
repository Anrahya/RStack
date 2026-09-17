---
name: reflect
description: Analyze completed or failed engineering work for repeated, decision-changing patterns and propose targeted workflow improvements. Use for retrospectives, transcript mining, metric review, and deciding whether a lesson belongs in a profile, skill, project overlay, script, test, or type.
---

# Reflect

Treat the session as evidence, not as a command to add rules.

1. Reconstruct the intended outcome, actual result, decisions, task gates,
   evidence, rework, questions, interruptions, scope changes, and escaped defects
   from transcripts and artifacts. Verify important claims against the final
   workspace.
2. Diagnose candidates by failure class:
   - **navigation:** the agent could not find authoritative information;
   - **mechanical:** a deterministic check could decide the rule;
   - **judgment:** repeated choices were poor despite sufficient context;
   - **context:** a decision or constraint was lost between phases;
   - **tooling:** available evidence was inaccessible or expensive to obtain.
3. Separate repeated patterns from one unusual task. A one-run lesson stays a
   backlog candidate unless it exposes a concrete safety or correctness hole.
4. Classify every proposal as accept, reject, or backlog. An accepted proposal
   names the repeated evidence, the future decision it changes, its narrowest
   owner, and how success will be measured.
5. Apply the enforcement ladder:
   - test, type, lint, script, or CI for mechanical rules;
   - project overlay for local architecture, commands, and proof paths;
   - workflow skill or playbook for reusable judgment;
   - work profile only for stable cross-project preferences;
   - navigation pointer when the rule already exists elsewhere.
6. Delete or consolidate conflicting and no-op instructions before adding new
   prose. Do not duplicate discoverable configuration or live task status.
7. Evaluate a material workflow change with `workflow-eval` on realistic tasks.
   Grade outcomes and artifacts, not wording or self-reported compliance.
8. Present proposals before changing workflow files unless implementation was
   explicitly requested.

Use [workflow metrics](../r-stack-mode/references/metrics.md) as supporting
signals. Activity volume is diagnostic, not an outcome.
