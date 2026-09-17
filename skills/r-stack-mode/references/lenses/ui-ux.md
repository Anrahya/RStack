# UI and UX

## Establish what good means

Name the audience, user task, primary action, existing design language and target
surface. Inspect supplied references and the running product. Separate faithful
reproduction from an original direction: visual similarity and design quality
are different acceptance criteria. Do not replace an approved reference with
an unrelated style because it is easier to implement.

Describe the intended hierarchy, typography, spacing rhythm, density, color
roles, imagery and motion using observable choices. Reuse existing tokens and
components where they fit. For a consequential unresolved direction, compare two
structurally different sketches under the same brief, not three palette swaps.
A clear supplied reference does not need redundant alternatives.

Freeze a small rubric before implementation: task clarity, hierarchy, coherence,
craft and fit to the requested identity. Add positive and negative examples when
available. “Premium,” “beautiful,” or “no slop” alone is not a grading rule.

## Implement the actual experience

Build a complete user path, including applicable loading, empty, error, success,
disabled and destructive-action states. Exercise realistic long content and
narrow viewports. Check keyboard navigation, focus visibility/order, labels,
contrast and reduced-motion behavior where applicable. Check touch and pointer
behavior rather than relying on hover alone. Backend error handling is part of
the experience, not a later cosmetic concern.

## Inspect the rendered result

Launch the real artifact, perform the target actions, and inspect screenshots
at declared viewports. Capture the action and resulting state; inspect console
and network failures as supporting evidence. A rendered page without exercised
controls cannot prove the workflow works. Automated accessibility checks are
useful but do not replace keyboard and task-flow inspection.

For parity, freeze baseline, viewport, fonts, browser version, data and animation
state before the edit. Predeclare tolerances for known nondeterministic rendering;
never relax them after seeing a failure. Investigate meaningful deltas. A zero
pixel delta under one setup neither proves usability nor covers every state.

Separate functional pass/fail from a design judgment and record who or what made
that judgment. Compare revisions against the rubric and preserve the best known
version. Do not keep iterating when the evaluator is only rewarding extra
complexity. Without visual access, report visual quality as unverified.
