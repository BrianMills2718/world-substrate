---
description: "Knock-on effects that declare timing 'immediately' run to the end inside the one existing commit; this is rule semantics, not the engine capability Decision 006 forbids."
---

# Decision 009: Same-moment knock-on effects are rule semantics, not new engine capability

Governs: src/world_substrate/engine.py, docs/plans/open_attempt.md

Source: Brian, 2026-10-26, "i approve", answering Q27 with its recommendation; November 10 amendment approval quoted under Amended below.

**Status:** accepted
**Date:** 2026-10-26
**Decided by:** Brian, in session 2026-10-26: "i approve", answering open question Q27 with its recommendation.
**Amended:** 2026-11-10, by the AI judge plan's slice J0 ([ai_judge.md](../plans/ai_judge.md), Agent technical
calls): the 32-reaction cap is removed. Build approved by Brian, 2026-11-10: "yes if ti si planned out and you have
no quesitons for me".
**Related:** [Decision 006](006-governed-rules-layer-scope.md), [open_attempt.md](../plans/open_attempt.md) Piece 2

## Question

Decision 006 and AGENTS.md say not to add engine, scheduler, renderer or cognition capability of World
Substrate's own. Slice S2 runs processes that declare `timing: immediately` again and again inside one commit
until nothing more is due (a ramification fixpoint, as in C+ and the Event Calculus), which changes
`engine.py`. Does that count as the forbidden capability?

## Decision

No. The fixpoint is allowed as rule semantics, under these bounds:

- it runs inside `Engine.apply`'s existing atomic commit and adds no clock, loop over time, or scheduler;
- each (process, entity) pair fires at most once per moment, so the number of such pairs bounds every chain and
  loop; new runs have no other cap (amended 2026-11-10; until then a moment was capped at 32 reactions and refused
  whole past it);
- each run records the reaction limit it ran under, and replay uses it: a record that names none ran under 32, so
  runs saved before the amendment replay unchanged;
- only processes that declare timing `immediately` use it; every other process keeps running once per round.

## Why

Hosting the chain on Concordia or Mesa steps would split one moment across steps, so a glass would fall in one
round and break in the next: the behaviour this slice exists to fix. Loops over time stay with Concordia or
Mesa as Decision 006 says.

## Amendment, 2026-11-10: no cap

Brian, 2026-11-09: "50 things could propagate down a causal chain 100 links deep". That is 5,000 steps in one
moment; the cap of 32 refused it whole. The cap was never what ended loops: a (process, entity) pair already fires
at most once per moment (`Engine._settle`), and that bound is finite: no effect a rule can declare creates an entity,
so a moment has at most (number of immediate processes) × (number of entities) steps. If a rule kind that creates
entities is ever added, this bound must be revisited in the same change. So J0 removed the cap for new runs
(`Engine(reaction_limit=None)`, `src/world_substrate/engine.py`), kept the once-per-pair rule, and wrote the limit
each run ran under into its record (`reaction_limit`, `null` for none). A refusal is part of a run's recorded
commands, so replaying an old run with no cap would change its outcome; old records therefore replay under 32
(`recorded_reaction_limit`, `LEGACY_REACTION_LIMIT`). Evidence: `tests/test_knock_on_unbounded.py` and the saved runs
under `evidence/ai-judge/j0/` (50 chains of 100 links in one moment; a loop of 40 that ends; a run refused at 32
before J0 and the same world run through since). Time, measured: the 5,000-step moment takes about 26 s of CPU
on the local machine (`tests/test_knock_on_unbounded.py`, 2026-11-10, run under other load); a world that size is
far past any World Builder world built so far.
