# UI and UX

Load this for changed gestures, resizing, focus, motion, loading/error states,
user flows or visuals. Choose the relevant section. A behavior repair does not
require redesign, a new rubric or alternative visual directions.

## Behavior repair and interaction verification

Read the component's applicable package instructions and preserve locked design
choices. List each changed behavior and its material transitions. Exercise the
original input: wheel and drag are distinct from zoom buttons; keyboard and touch
are not interchangeable with pointer hover. Include an unchanged control where
one can expose an overbroad fix.

For resize/responsive changes, cross the actual breakpoint in both directions
and check retained user state and focus, not just initial page layout. For motion
changes, check pause, reduced-motion preference and hidden/offscreen behavior
where the implementation or project contract makes them relevant. For lifecycle
changes, check unmount, cleanup and pending asynchronous actions at the real
boundary. Test empty, loading, error and success states that the change can affect.
Do not assume all applications implement every condition; explain material gaps.

Use keyboard navigation to inspect focus visibility/order and labels; inspect
narrow layouts for obscured controls. DOM assertions alone do not establish visual
quality. Capture the relevant action and rendered result, view the image when
making a visual claim, and inspect console/network failures as supporting evidence.
A persistent browser controller is a tool, not a test oracle. Distinguish maintained
tests, one-off assertions and inspected interactions in the final coverage.

## New design or changed visual direction

Name the audience, user task, primary action, existing design language and target
surface. Inspect supplied references and the actual product. Separate faithful
reproduction from original design. Do not replace an approved reference with an
unrelated style because it is easier to implement.

Make hierarchy, typography, spacing, density, color roles and motion concrete.
Reuse existing tokens/components. For a consequential unresolved direction, compare
structurally different sketches under one brief; a clear reference does not need
redundant alternatives. Assess task clarity, coherence, craft and fit to the brief,
not vague praise. Build the whole relevant user path, including its error states.

## Visual comparison

For parity, pin the baseline, viewport, fonts, browser, data and animation state.
Declare tolerances for known nondeterminism before seeing the result; do not relax
them to accept a failure. A zero delta in one setup does not prove usability.
Separate functional pass/fail from aesthetic judgment and say who or what made
that judgment. Preserve the best supported revision rather than iterating toward
more complexity. Without visual access, report visual quality as unverified.
