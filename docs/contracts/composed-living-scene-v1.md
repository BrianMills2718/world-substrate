---
role: contract
status: implemented
reviewed_through: 2026-09-10
---

# Composed Living Scene presentation

`render_composed_living_scene.py` is the product-oriented renderer for the existing
`world-substrate-living-scene/v1` logical-frame contract. It does not introduce a
second simulation contract or a second source of world truth.

The older `render_living_scene.py` remains a compatibility/debug renderer. A world
may opt into the composed renderer without changing canonical state, event history,
information delivery, causal ancestry, or simulation timing.

## Authority boundary

The composed renderer may choose or interpolate presentation-only properties:
illustrative background art, actor/object screen position, state styling, idle or
transition animation, event emphasis, responsive layout, labels, and inspector
layout. It may not mutate or infer canonical state.

The renderer consumes only deterministic Living Scene frames. Scrubbing still
reconstructs from the retained initial snapshot plus canonical event deltas.
Activity status and timing, institution state, resource values, commitments, and
information deliveries remain upstream facts.

## Generic presentation primitives

The composed renderer supports reusable world-neutral primitives:

- image/text actor assets with persistent homes and state styling;
- image/text world objects with local status light, meter, and state effects;
- activity gathering around a declared anchor and deterministic return home;
- presentation-only state-dependent object positions;
- exact-event emphasis pulses;
- visibility-safe transient information paths and message bubbles;
- compact play/pause/step/scrub controls;
- selectable actor/entity/activity/institution anchors;
- a contextual inspector populated from already-bound canonical fields;
- desktop/mobile presentation geometry.

A `presentation.emphasize` event operation has no logical effect. It only tells the
renderer which already-declared visual object should receive a transient pulse.

## Product-quality rule

The composed path exists to make the world itself the primary interface. It should
not regress into a persistent grid of cards, graph panels, or evidence tables. A
profile may retain card display as a compatibility fallback, but polished worlds
should use spatial art and local state changes wherever those are sufficient.

World-specific art, labels, positions, and exact rule bindings remain in that
reference world's profile/assets. Generic renderer source must not branch on a
world name, entity id, resident name, or scenario-specific rule id.
