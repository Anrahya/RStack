# Reach the application for verification

Choose per claim, not once for the whole task. Existing maintained tests may
reach some behavior and miss another boundary. These are three valid paths:

| Available capability | Action |
| --- | --- |
| Maintained tests reach the changed behavior | Use or extend them and run required gates. |
| Tests cannot reach it, but an authorized browser or one-off probe can | Exercise that boundary, capture the result and state retention limits. |
| No safe available capability reaches it | Keep the claim unverified; do not replace it with an easier proxy. |

Do not add a project dependency or maintained framework merely because one task
needs a browser. Conversely, do not claim a one-off check satisfies a project's
mandatory maintained-test policy. Creating or repairing reusable tooling requires
appropriate task authority. Ordinary authorized scratch work does not require
ceremonial reapproval.

## Common lifecycle for maintained and one-off drivers

1. **Launch or attach:** resolve the existing documented command and tools; name
   the instance, profile/data, port and ownership. Reuse host browser control when
   available. Preserve user-owned sessions; do not attach to unrelated browsers.
2. **Check readiness:** verify the expected app/build, URL, available feature and
   test authentication. HTTP 200 or a listening port alone is insufficient.
3. **Drive:** use actual app controls and inputs. Include materially different
   transitions and an unchanged control. Do not bypass the changed boundary.
4. **Assert and capture:** compare independent expected values; required failures,
   missing cases and setup errors must fail executable gates. Capture inspected
   actions separately from executable tests. Record tool/browser versions,
   viewport, inputs, environment and evidence path. A new gate needs a failing
   control before its pass is trusted.
5. **Cleanup or handoff:** stop only owned scratch resources and confirm evidence
   survives. Never kill everything with the same process name. Preserve a
   user-owned persistent controller; an intentionally retained owned session
   needs explicit lifetime and next owner. Do not delete authentication state.

One-off scripts stay in an authorized scratch/evidence area, not unsolicited
product source. Record resolved dependencies and paths; do not depend silently
on an evictable package cache. State which claims lack a maintained regression
check and how long their script/evidence will remain. Current proof and future
regression protection are separate facts.

## Persistent browser control

See [browser setup](../../../docs/BROWSER-SETUP.md) for host-side installation
choices and session hygiene. A CLI daemon or MCP browser can remain alive across
steps. Surviving process restart additionally needs supported state/profile
persistence; surviving a cloud sandbox reset needs retained storage. Those are
not equivalent guarantees. Use one writer per session and verify the current page
again after a disconnect or navigation change.

## Maintained project drivers

When repeated work justifies a maintained recipe, derive its launch, readiness,
selectors, expected values and cleanup from the actual application. Provide no
invented commands or credentials. Give the feature map an owner. Run the recipe
end to end once and preserve its evidence; until then it is a draft. Verifying
one mapped feature does not verify all features. Recheck it after changes to
routes, authentication, dependencies or build setup.
