# Design

Use when the requested deliverable is an architecture, interface, or ownership
decision rather than production implementation.

1. **Contract.** State the decision, consumers, constraints, reversibility, and
   evidence that would distinguish a good design.
2. **Ground.** Invoke `investigate` across every affected boundary. If intent or
   domain behavior is unsettled, invoke `shape`. Pass when fixed constraints and
   open decisions are separated.
3. **Sketch usage.** Invoke `architect`. Write caller or user usage first, then
   derive data shapes, ownership, lifecycle, errors, cancellation, retry
   behavior, module boundaries, and the highest useful test seam.
4. **Explore.** For a consequential fork, produce at least two structurally
   distinct complete candidates under one predeclared rubric. Keep them isolated.
   Invoke `prototype` for questions observation can settle.
5. **Select.** Compare correctness, state ownership, boundary clarity, invalid
   states, migration cost, reader load, reversibility, and proof. Synthesize only
   compatible strengths; do not average contradictory designs.
6. **Close.** Return the selected usage sketch, core data shape, ownership map,
   failure behavior, module/API surface, test seam, migration implication, and
   rejected alternatives. No production code is required unless requested.

