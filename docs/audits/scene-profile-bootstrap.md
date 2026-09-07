---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Scene-profile bootstrap experiment

## Question

Can the graphical replay profile be partly generated from represented world
facts and an explicit asset catalog without giving presentation code authority
to invent world state?

## Method

Kitchen and Castaway were used as acceptance fixtures because both already had
working `scene-profile-v0` files and materially different traces.

For each world the bootstrapper received:

- the reference-world model;
- a retained `world-substrate-contested-run/v3` trace;
- `reference_worlds/scene-asset-catalog-v0.json`;
- then, separately, a presentation-only review overlay.

The first pass intentionally omitted the review overlay. It had to infer safe
facts and emit explicit TODOs rather than coordinates or action animation it
could not justify. The second pass applied the review overlay with
`--require-complete`; its core profile was compared structurally with the
existing hand-authored profile and passed through the unchanged generic scene
loader/renderer.

## Result

The bootstrapper safely inferred:

- trace actors and their model entities;
- visual entities referenced by actions or represented ownership/portability;
- asset bindings supplied by the explicit catalog;
- actor-owned initial objects such as Robinson's cup;
- category-backed canonical stations such as burners, orders, the unsafe pool,
  and camp fire;
- Kitchen actor-to-order progress links already present in the world model;
- candidate item/station action fields when trace values consistently named a
  visual entity or station.

It did **not** invent actor homes, station rectangles, entity screen homes, or
ambiguous action-to-motion/state semantics. Those appear as bootstrap TODOs
until a review overlay resolves them.

After review, both assembled profile cores matched the existing profiles
exactly. The per-world review payload was about **64% of the previous Kitchen
profile** and **67% of the previous Castaway profile** by compact JSON size — a
roughly **36% / 33% reduction** in scene-specific review content. The shared
asset catalog is counted as an explicit reusable input, not as inferred world
truth.

The generic renderer was not modified for this experiment. Full verification
passed 222 unit tests plus `scripts/check_project.py`; both assembled profiles
also rendered successfully through the existing loader.

## Boundary preserved

The trace still owns what happened. The world model owns represented entity and
relationship facts. The asset catalog only says how known things may look. The
review overlay only resolves presentation. None of those presentation inputs
may add a causal fact or promote illustrative coordinates into canonical state.

## Limit

This is not yet a greenfield authoring result. Kitchen and Castaway already had
known-good profiles, so their review overlays could be measured against answers
that were already known. The next meaningful test is a real world with no
existing scene profile to copy. A greenfield failure that requires a
world-specific renderer branch should be treated as a portability finding, not
patched around silently.
