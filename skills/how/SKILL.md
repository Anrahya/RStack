---
name: how
description: "Explain how a concept, mechanism, system or code path works. Use for how does this work, walkthroughs, or understanding ownership and flow."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: read-only
---

# How

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Answer the mechanism question at the depth requested. This applies to general
knowledge as well as software. Do not assume a codebase is involved.

For a concept, identify the inputs or starting conditions, interacting parts,
rules, intermediate states and observable result. Use a concrete example. Explain
causal steps rather than substituting a list of terms. Include the failure or
limiting case that makes the model more accurate when relevant.

For code, find the real entry point and consumer. Trace validation, state ownership,
transformations, side effects, failure, cancellation or retry, and the externally
observable result. Inspect surrounding callers, configuration and tests where they
can contradict the apparent path. Verify library versions when behavior depends on
them. File names and function signatures are navigation, not an execution model.

Use current authoritative sources when the topic is time-sensitive or unfamiliar,
and open any specifically named source. Explain stable known concepts directly when
additional research would not help. Mark a code path as statically traced versus
actually executed. Do not invent runtime observations.

Work directly for a small question. For a broad question, independent read-only
angles can help if the host supports them and the user-authorized scope permits
them. Do not require a subagent, switch executors, or manufacture independence in
one context. Keep the final explanation coherent rather than pasting worker reports.

Return the answer first, followed by the flow, a useful example and material gotchas.
Use paths and symbols as supporting pointers, not as the explanation itself. A
question about historical intent belongs to `why`; a broader lesson may benefit
from `teach`, but neither is automatically invoked. No production edits.
