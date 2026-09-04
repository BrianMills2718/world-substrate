---
role: audit
status: active
reviewed_through: 2026-09-04
authority_refs:
  - ./m2-give-path-audit.md
  - ../architecture.md
  - ../../roadmap/README.md
---

# M6: a second world, and what "substrate" actually meant

Success criterion 6: a materially different reference world reuses the
semantic, transition, and mechanic-profile contracts. This was the last unmet
criterion and the only test of whether this project has a substrate or one
carefully documented freshwater engine.

The world is a workshop: a worker, a bench, discrete parts, a wrench, and a
chair frame to assemble. It shares no content with Castaway — no liquid, no
temperature, no material, no heat source, no quantity of anything. Its actors
have no health and cannot be harmed.

Evidence: `tests/test_workshop_world.py` (10 tests, 5 of which exercise shared
machinery written before this world existed).

## The prediction, recorded before building

Written into the session before any code: *the substrate will have to change,
the mechanics will not transfer at all, and the engine/assay/policy machinery
will transfer unchanged.* All three held. The interesting part is the shape of
the substrate changes, which was not predicted in detail.

## What transferred with no edits at all

- `World`, `Entity` identity, revision, tick, snapshot and `from_snapshot`
- `Engine.apply`, `Engine.submit`, `Engine.advance`, `discover`, causal events,
  `Check` results, atomic rejection, stale-revision rejection
- `RuleRegistry` and the `ActionRule` / `ProcessRule` protocols
- Write-scope enforcement *as a mechanism* (its binding needed a fix; see below)
- `MechanicPackage`, `MechanicProfile`, installer validation, profile freezing
- All three interaction assays
- `resolve_choice` / `apply_choice` — the policy consequence seam
- **Exact replay**, which worked in the new world with no work whatsoever

That is a real result. The transition kernel, the observability contract, the
authoring contract, the assays and the policy boundary are genuinely
world-independent.

## What had to change in the substrate — four couplings

Each was freshwater content sitting in a neutral-sounding place, and each was
invisible until a second world existed.

**1. `Entity` was a closed set of eleven Castaway components.** A new component
was rejected by `from_dict` and silently dropped by `as_dict`. The architecture
document said "entities remain open to unrelated components"; the code said
otherwise. Fixed with an open typed-component registry: a world pack registers
its dataclasses and refers to them by name, so components stay typed rather
than becoming the untyped property bag the roadmap warns about. Entities with
no registered components serialise byte-identically, so every pinned M1
receipt and donor comparison is unchanged.

**2. `Engine.observe()` required `ActorState`.** Being able to *see* required
having health and hydration. Now it requires a location, which is what
observing actually needs.

**3. Write-scope enforcement bound placeholders through a hardcoded Castaway
vocabulary** — `vessel`, `source`, `target`, `destination`, `recipient`. The
workshop's `item`, `part` and `assembly` bound to nothing, so a correctly
declared write looked out of scope and `pick_up` was rejected as a
`scope_violation`. It now asks the world which of an envelope's values name
entities, which is both more general and tighter than a hand-listed vocabulary.

**4. `policy.present()` read `actor.health` and `actor.hydration` directly** and
crashed on a world whose actors are not survivors. It now renders whatever
components an entity actually has.

Two of these four were code written earlier in this same session, by the same
author, in modules named for their general purpose. That is the honest lesson:
generality is not established by naming something neutrally, and a single world
cannot reveal what a second one immediately does.

## What transferred: none of the mechanics

Not one of the eleven Castaway rules was reusable, and the reason for the most
plausible candidate is specific rather than aesthetic. `take` and `give` look
like general possession mechanics, but `mechanisms/ownership.py::_vessel_weight`
computes carrying capacity by dividing `liquid.volume_ml`. They cannot move a
bolt. The workshop needed its own `pick_up`.

This matches the M2 audit's measurement exactly: 2 of 10 `give`/`take` checks
were substrate-universal and 8 were content. That number was recorded as a
completed checklist item eight days ago; it was the most predictive thing in
the repository.

## The answer to the question

**The machinery is a substrate. The content is not, and never claimed to be.**

Roughly: everything that moves state around, records it, validates it, refuses
it, replays it, installs it, assays it, or exposes it to a policy transferred.
Everything that decides *what happens* was rewritten from nothing. Four seams
between those two categories were mislabelled and are now fixed.

A second world took one session. The cost was four substrate fixes and a full
rewrite of the domain rules — which is the correct shape for a substrate, and
would have been an unpleasant surprise at ten worlds instead of two.

## Limits

- One second world, chosen by the same person who built the substrate, and
  deliberately chosen to be maximally different. A domain that is *nearly* like
  Castaway would test different seams and might find worse ones.
- The workshop is small: four mechanics, seven entities, no institutions, no
  autonomous environmental process beyond fatigue and wear.
- No LLM policy has driven the workshop. The seam is verified there; the
  playability is not.
- "Transferred unchanged" means no edit was required, not that the contract is
  optimal for the new world.
