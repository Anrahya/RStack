# Recipe structure

This is an authoring skeleton, not an executable recipe. Fill it from the project
and remove all unresolved placeholders before calling the output operational.

## Skill metadata

Name the actual app. Describe when its recipe is useful. List genuine runtime
requirements. Do not make it an always-on mode or grant additional tool permissions.

## Launch

Exact command, working directory, isolated ports/data directory, required secret
names without values, readiness signal, process owner and build/revision identity.

## Doctor

Confirm target identity, readiness, authentication and expected data before driving.
A listening port alone does not prove it is the intended instance. Recheck after
surprising failures; relaunch only the instance the run owns when necessary.

## Drive

Exercise the real entry point with stable selectors, API calls, terminal input or
public functions. State input and expected observation. Do not bypass the changed
behavior through internal setters or a mock of the very component being verified.

## Evidence

Capture action and result, not only a final screenshot. Include externally visible
side effects and persistence read-back where relevant. Record the actual revision,
inputs, environment and observation; store outside throwaway cleanup directories.

## Cleanup

Stop exact owned processes and remove exact run-created scratch state. Handle failed
iterations. Preserve evidence and user data. Document leftover state honestly.

## Feature map

Index only source-grounded features. Each entry states the user's route, input,
expected result, critical states, prerequisites, evidence location and which paths
have actually been exercised. Do not label unexercised paths as verified.
