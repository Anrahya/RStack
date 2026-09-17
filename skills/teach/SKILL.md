---
name: teach
description: "Help the user understand a concept, paper, system or change at their current level. Use for teach me, explain intuitively, or walk me through it."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: read-only
---

# Teach

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Teach the topic, not your process. This skill works for physics, mathematics,
computing, papers, history and other knowledge work; a repository is not required.

Infer the learner's starting point and purpose from the conversation. Respect an
explicit level such as undergraduate physics. Start from what they already know,
not from a scripted beginner lesson. Ask a short question only when a missing detail
would change the explanation; otherwise pick a reasonable starting point and proceed.

## Build a mental model

Begin with the concrete answer or a plain definition. Explain the problem the idea
solves, the mechanism, and one worked example. Show how the parts interact rather
than enumerating labels or functions. Use an analogy only when it maps correctly,
and state where it breaks. Distinguish a motivating intuition from a proof.

For quantitative topics, define symbols, keep units, work through the important
steps, and check limiting cases when useful. Do not skip the very step the learner
is trying to understand. For a proof, state its assumptions and the logical bridge;
do not substitute a story for an argument.

Use small diagrams or a progressively expanded picture when they reduce confusion.
Text diagrams are acceptable. Rendered images require an actual available tool;
do not claim to have drawn or inspected something you have not. Do not generate
three diagrams automatically because a topic has three parts.

## Ground only what needs grounding

Read a named paper, provided chapter or specific code before claiming to explain
its content. Use available sources for current, disputed or unfamiliar factual
claims; cite them where they matter. For stable concepts, explain directly unless
research is requested or needed. A missing source must be disclosed rather than
replaced with a guessed account. `how`, `why` and `research` are optional helpers,
not a mandatory chain or reason to repeat evidence already read.

## Match the interaction

For a conversational question, give a complete first layer and let the user steer
the next one. For an explicitly requested thorough lesson, deliver the full lesson
in this response; do not hide the requested material behind repeated "continue?"
gates. Never force quizzes, recap rituals or condescending pacing. Offer exercises
only when asked or when they clearly serve a requested study plan.

Return the explanation itself. Keep uncertainty, source limits and unresolved
questions intact. Do not turn learning into code changes, a project plan or a mode.
