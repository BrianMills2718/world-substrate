---
role: audit
status: active
reviewed_through: 2026-09-09
---

# Living Scene embodied renderer first gate

## Question

Can the Living Scene v1 logical frame seam render an inhabited 2D world using
only declarative profile data and canonical retained state, without adding
Waltzman-specific runtime logic or turning animation into simulation authority?

## Implemented slice

`scripts/render_living_scene.py` consumes a retained
`world-substrate-live-projection/v0` bundle plus a
`world-substrate-living-scene/v1` profile. It renders:

- presentation-only zones;
- arbitrary declared actors and actor state labels;
- canonical resource/current/required values;
- duration-bearing activity status;
- institution status and configured counts;
- deterministic participant gathering while a canonical activity is active; and
- exact declared `actor.move_to` presentation operations.

The renderer does not inspect world names, entity categories, or action names to
infer domain behavior. Unknown render metadata remains neutral.

## Authority boundary

All displayed state values arrive through Living Scene read bindings over the
logical frame. Browser movement and gathering alter only presentation
coordinates. Activity state is read from canonical status/start/end fields; a
CSS/JavaScript animation clock cannot complete the activity or change world time.

## Domain-neutral fixture

`tests/fixtures/living_scene/neutral-render-profile-v1.json` and
`neutral-render-projection-v0.json` exercise two actors, one resource, one
duration-bearing activity, and one institution. At retained frame 2 the resource
is below requirement, the activity is active, the actors gather around it, and
the institution is blocked.

Retained browser artifacts:

- `evidence/renders/living-scene-neutral-v1.html`;
- `evidence/renders/living-scene-neutral-v1-desktop.png` at 1200×800; and
- `evidence/renders/living-scene-neutral-v1-mobile.png` at 390×844.

The browser produced only headless-environment DBus/GPU warnings; the page rendered
and screenshots were produced successfully.

## Acceptance boundary

This gate proves reusable embodied presentation primitives only. It does not prove
information-delivery visualization, action refusal feedback, Waltzman composition,
M1 world-story acceptance, or public deployment. Those remain downstream work.
