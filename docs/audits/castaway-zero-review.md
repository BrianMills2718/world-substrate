---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Castaway zero-review scene portability

## Question

Does the zero-review replay path transfer beyond Workshop to a materially
different action/state family without adding Castaway-specific renderer code or
per-world review geometry/action projection?

## Method

The existing no-spend retained Castaway contested trace was used unchanged. It
exercises `fill` and `drink`, an unsafe liquid source, a shared clay pot, two
actors, and Robinson's initially owned metal cup.

The shared scene presentation catalog gained explicit bindings for the exact
`fill` and `drink` action ids:

- `fill` marks the inferred vessel visually `filled`, activates the inferred
  source station, and uses the trace-grounded source field already discovered by
  the bootstrapper;
- `drink` marks the inferred vessel visually `used` and moves the actor toward
  that explicitly referenced vessel.

No projection is inferred from the English spelling of either action. The
bindings have the same placeholder/negative-control rules established by the
Workshop proof.

The bootstrap command used the Castaway world model, retained trace, shared
catalog, and `--auto-layout` with **no review overlay**.

## Result

The generated profile has:

- zero bootstrap TODOs;
- declared action bindings `drink` and `fill`;
- no binding-resolution errors;
- Robinson's initial ownership of `cup-robinson` preserved from the world model;
- `unsafe-pool` and `fire-camp` inferred as canonical source/workstation scenes;
- deterministic homes/anchors for both actors, the clay pot, and the cup;
- visual vessel state that follows accepted commit order (`fill` then `drink`
  yields `used` when drink commits last in the turn).

Retained artifacts:

- `evidence/castaway/scene-profile-zero-review-v0.json`
- `evidence/renders/castaway-zero-review-v0.html`

Real Chrome checks at turns 1 and 8 were legible. The existing polished
`castaway-spatial-replay-v0.html` remains byte-for-byte unchanged. The full gate
also caught and fixed an authority regression: catalog defaults were initially
deep-merged underneath reviewed action rows. Reviewed action projection now
starts from neutral inferred fields and **replaces catalog projection defaults**,
so explicit polish remains authoritative.

## Boundary preserved

The Castaway world/trace owns liquid behavior, ownership, health and accepted
commands. The presentation catalog only determines how already represented
facts/actions look. `fill`/`drink` bindings cannot make an action valid, change
liquid volume, health, ownership, or causal history.

No model calls, deployment, or publication were used.

## Meaning

Zero-review replay generation is now established on **two real worlds with
materially different action families**: Workshop (`pick_up`/`attach`) and
Castaway (`fill`/`drink`). The next portability gate is the Kitchen flagship,
which combines five action kinds, multiple goal stations, shared ownership, item
state progression, and the replicated handoff trace.
