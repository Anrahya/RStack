# Worked examples: what the workflow should change

These examples illustrate intended behavior; they are not reports of model trials.

## A retry bug with a tempting partial fix

Request: events sharing an ID across accounts are being dropped. The agent
suspects a cache timeout. A weak response changes the timeout and adds a unit test
with two different IDs. That test never exercises the failure's identity boundary.

A grounded response traces the deduplication key, finds that only event ID is
stored, and predicts that varying account while holding ID fixed will expose the
bug. The small behavior matrix is same account/same ID (one effect), different
account/same ID (two independent effects), and same account/different ID (two
effects). The unchanged control prevents a fix that simply disables deduplication.
If effects are durable, repeat through the public path after restart. A tuple-key
unit test alone cannot prove the persistence adapter preserves that tuple.

## “Make this settings screen feel better”

A weak response changes colors, rounds cards and announces polish after a build.
A useful response first identifies the screen's task and current design language.
It defines an observable direction: one primary action, clear grouping, consistent
control widths, distinguishable help versus labels, and error text adjacent to the
field. An approved reference constrains hierarchy and density, not just palette.

The agent renders desktop and narrow layouts, tabs through controls, attempts an
invalid save and verifies the resulting error and retained input. It inspects the
screenshots against the original brief and reports its visual assessment as a
judgment. Passing a type checker proves none of that experience. An aesthetically
strong revision that hides the save action should not win the comparison.

## “Which engineering model should I use?”

A weak answer copies one leaderboard row from a search snippet and interprets
rank as a complete capability profile. A useful answer resolves exact model,
provider, harness, benchmark version and budget, then checks what was actually
measured. A vendor score and a separate-harness score are not automatically
comparable. The recommendation distinguishes measured evidence from a proposed
local trial and names which result would change the choice.

For this R-Stack release, the correct closing statement is that the mechanical
capture and validation tests passed while agent-quality uplift remains unmeasured.
A fabricated frontier comparison would contradict the workflow's purpose.
