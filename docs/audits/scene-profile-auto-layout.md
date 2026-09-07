---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Scene-profile presentation auto-layout

## Question

After greenfield scene bootstrapping and generic multi-item station slots, can
we remove most hand-authored **geometry** without giving coordinates causal
authority or hard-coding a world into the renderer?

## Method

Workshop remained the greenfield measurement fixture. The existing presentation
review overlay was stripped of:

- Mira's screen home and carrying offsets;
- station rectangles and actor/item anchors;
- loose entity homes.

The bootstrapper gained optional `--auto-layout`. It runs after the review
merge and fills only geometry that is still absent. Therefore explicit review
coordinates always win. The algorithm is deterministic (`role-grid-v0`): actors
receive stable homes, stations occupy role-based source/workstation/surface/goal
zones, anchors are derived from station rectangles, and loose entities are
placed deterministically using reviewed action targets or a source/surface
fallback.

Every generated path is listed under
`bootstrap.auto_layout.proposed_geometry`. The coordinates remain illustrative
presentation data.

## Result

For Workshop, auto-layout proposed 12 geometry paths:

- one actor home;
- two station rectangles;
- two station actor anchors;
- two station item anchors;
- five loose entity homes.

The compiled profile has no bootstrap TODOs and the replay remains legible at
the first and final turns. The explicit chair-part `item_layout` slots still
place both legs and the seat distinctly inside `frame-a`.

The review overlay is now **1,365 compact JSON bytes** against a **2,680-byte
profile core**, a **50.9% manual-review fraction**. Before auto-layout, after
closing the station-slot finding, that fraction was 63.7%. The original
pre-slot greenfield baseline was 62.6%.

Kitchen and Castaway do not use auto-layout in their committed profiles and
continue to regenerate byte-for-byte identically through the same renderer.

## Boundary preserved

Auto-layout is optional. It never changes the world model, trace, mechanics, or
relationships. It only fills missing scene geometry; review overrides are
applied first and are never overwritten. Action motion/state semantics remain
reviewed rather than inferred merely from action names.

## Remaining manual work

At this point Workshop's remaining review payload was mainly human-facing
title/theme copy and `action_visuals`. The subsequent [action-presentation
binding audit](scene-action-presentation-bindings.md) removed the latter from
per-world review: the polished Workshop review fraction is now **34.3%**, and a
zero-review default replay is also retained.
