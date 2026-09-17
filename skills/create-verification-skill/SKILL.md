---
name: create-verification-skill
description: "Build a project-local recipe that launches, drives and checks the real application. Invoke when that durable recipe is requested or approved."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: scoped-write
---

# Create a verification skill

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Create a repeatable project-local verification skill, not a new workflow engine.
An advice-only request returns advice. Creating files requires authorization for
that output; existing explicit authorization does not need another approval ritual.

## Discover the actual project

Read project instructions and existing verification recipes. Determine the real
consumer-facing surface: browser, CLI/TUI, desktop, mobile, API, library or pipeline.
Find the documented launch/build command, dependencies, ports, seeds, authentication,
readiness signal, programmatic driver and observable result. Prefer the existing
harness. Do not assume a browser, framework, host directory or executable exists.

Identify how to isolate the instance and its data. Verify that a target belongs to
this run before driving it or cleaning it up. Do not silently borrow production
credentials, touch real customers, install paid services, or launch a second writer
against shared state. A dry-run label is not evidence of which effects it skips.

## Write the smallest usable recipe

Choose the host/project-approved skill location. Name the app and triggers. Include
Launch, Doctor, Drive, Evidence and Cleanup sections, with exact observed commands
and readiness checks. Document relevant input, expected result, state read-back,
run identity and evidence location. Store no secrets. Generated helpers must be
executable, documented and restricted to the requested scope.

Use [the recipe skeleton](references/recipe.md) as a structure, not a file to ship
with placeholders. Seed a feature-map index and a few grounded feature entries.
Each names how a user reaches the feature, how the driver exercises it, the
observable result, important alternative states and known prerequisites. Mark
coverage that was discovered from source versus actually exercised.

## Run the recipe before calling it working

Execute launch, doctor, one mapped feature, evidence capture and cleanup end to end
using a safe target. Recheck that the evidence survives cleanup. Clean up owned
processes even after failures. Do not kill by a broad process name or delete shared
state. Fix and retest the recipe within scope; report product defects separately.

If a needed capability is unavailable, return a clearly labeled draft with the
specific untested step. Running one feature validates the recipe for that feature,
not the entire map. Return location, demonstrated path, evidence and limits. No
automatic commit, PR, deployment, auto-enablement or mode activation.
