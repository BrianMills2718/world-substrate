---
description: "Knock-on effects that declare timing 'immediately' run to the end inside the one existing commit; this is rule semantics, not the engine capability Decision 006 forbids."
---

# Decision 009: Same-moment knock-on effects are rule semantics, not new engine capability

Governs: src/world_substrate/engine.py, docs/plans/open_attempt.md

**Status:** accepted
**Date:** 2026-10-26
**Decided by:** Brian, in session 2026-10-26: "i approve", answering open question Q27 with its recommendation.
**Related:** [Decision 006](006-governed-rules-layer-scope.md), [open_attempt.md](../plans/open_attempt.md) Piece 2

## Question

Decision 006 and AGENTS.md say not to add engine, scheduler, renderer or cognition capability of World
Substrate's own. Slice S2 runs processes that declare `timing: immediately` again and again inside one commit
until nothing more is due (a ramification fixpoint, as in C+ and the Event Calculus), which changes
`engine.py`. Does that count as the forbidden capability?

## Decision

No. The fixpoint is allowed as rule semantics, under these bounds:

- it runs inside `Engine.apply`'s existing atomic commit and adds no clock, loop over time, or scheduler;
- it is capped at 32 reactions per moment, and the whole moment is refused when the cap is passed;
- only processes that declare timing `immediately` use it; every other process keeps running once per round.

## Why

Hosting the chain on Concordia or Mesa steps would split one moment across steps, so a glass would fall in one
round and break in the next: the behaviour this slice exists to fix. Loops over time stay with Concordia or
Mesa as Decision 006 says.
