---
name: typescript-best-practices
description: "Apply focused TypeScript guidance when requested or useful for a bounded change. Not an always-on rule for every TypeScript file."
license: MIT
metadata:
  rstack-kind: utility
  rstack-activation: discretionary
  rstack-lifetime: invocation
  rstack-effect: scoped-edit
---

# TypeScript guidance

Standalone utility. Do not start or resume R-Stack mode, load its work profile,
or add its phase gates, work graph or evidence receipts. Apply only to this request;
return the requested result and stop. Existing permissions and safety rules still apply.

Use the project's installed TypeScript version, configuration, conventions and
existing runtime validation library. Review or edit only the requested scope.
Do not install dependencies, change global compiler flags or rewrite every .ts file
just because this utility is available.

Model variants with discriminated unions when they prevent real invalid states.
Use branded values only where accidental interchange matters. Keep the simplest
type that makes the supported operations safe; do not brand every primitive or
introduce a generic framework for one call site.

Treat untrusted external values as `unknown` and validate at the boundary. Prefer
the repository's existing schema or parsing approach over duplicate declarations.
A TypeScript annotation or assertion does not validate runtime data. User-defined
type guards must check what they claim.

Narrow before asserting. Avoid unjustified `any`, non-null assertions and broad
suppressions, but distinguish `as const`, validated branding and justified framework
interoperability from unsafe casts. Use exhaustiveness checks when adding a variant
must force callers to handle it. `satisfies` checks compatibility without replacing
the expression's inferred type; it is not a runtime validator or a universal
literal-preservation switch.

Derive related types when that avoids drift, but do not couple unrelated concepts
merely because their current shapes match. Match the interface to caller usage.
Respect existing structured logging, cancellation, lifecycle and cleanup policies;
CLI output is not inherently wrong because it uses `console`.

See [patterns](references/patterns.md) for small examples. Type-check changes with
the project's command and run relevant behavior checks when authorized. Do not
claim runtime correctness from a type-check alone. Return the requested advice,
findings or scoped change with the checks actually performed.
