---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Workshop scene-profile greenfield proof

## Question

Can the scene-profile bootstrap path produce a useful graphical replay for a
real world that had **no pre-existing scene profile**, without changing the
generic renderer or copying an already-known visual answer?

## Method

Workshop was chosen before any Workshop scene profile existed. A seven-turn,
zero-spend trace was retained by driving the existing Workshop engine through
accepted `pick_up` and `attach` actions: Mira takes the wrench, then attaches
two legs and a seat to `frame-a`. Replaying those commands through a fresh
Workshop engine completes the same chair.

The bootstrapper then received only:

- `reference_worlds/workshop/bench-v0.json`;
- the retained v3-shaped Workshop trace;
- the shared scene asset catalog.

The asset catalog was generalized once, at the reusable seam, to support
category-level entity bindings in addition to direct ids/component values.
Workshop therefore binds `worker`, `tool_kind=wrench`, and `part_kind` values;
the bootstrapper contains no Workshop ids.

## Unreviewed result

Before presentation review the draft correctly inferred:

- Mira as the actor and a worker asset;
- `frame-a` as the canonical assembly/goal station;
- wrench, legs, seat and bracket as visible portable entities;
- `pick_up.item` as an entity field;
- `attach.part` as an entity field and `attach.assembly` as a station field.

It emitted nine TODOs instead of inventing screen geometry or action motion.

## Reviewed result

A presentation-only overlay supplied the actor/station/entity coordinates and
reviewed two action projections. The assembled profile had zero TODOs and
rendered through the **unchanged** `scripts/render_scene_replay.py`.

The compact review payload is 1,620 bytes versus 2,589 bytes for the final
profile core: a **62.6% manual-review fraction**, or about **37.4% less
per-world scene content** than authoring the full profile directly. This is a
true greenfield measurement, unlike the earlier Kitchen/Castaway backfit test.

## Portability finding

The final frame also exposed a generic visual limitation: a station currently
has one `item_anchor`, so multiple attached parts share the same display slot.
That makes the completed chair less legible than the action/relationship trace
it represents. No Workshop-specific renderer branch was added to hide this.

That finding was intentionally retained through the greenfield merge rather than
hidden with Workshop-specific rendering.

## Follow-up closure

The next increment closed it generically. `scene-profile/v0` now lets a station
declare relative `item_layout.slots` with deterministic `grid` or `anchor`
overflow. `frame-a` uses three relative slots, so the final Workshop frame
places `leg-1`, `leg-2`, and `seat-1` at three distinct positions while their
canonical relationship remains `attached_to = frame-a`. The renderer contains
no Workshop ids.

Kitchen and Castaway, which do not opt into `item_layout`, still regenerate
byte-for-byte identically. The extra Workshop slot declaration raises the
current review payload from the original greenfield 1,620 bytes to 1,699 bytes
against a 2,668-byte profile core: **63.7% current manual-review fraction**.
The original 62.6% figure remains the greenfield baseline before the finding was
closed.

The remaining major automation cost at that point was illustrative scene
geometry, not multi-item placement. A subsequent [auto-layout
audit](scene-profile-auto-layout.md) closed most of that geometry review: the
current Workshop review fraction is **50.9%**, with all 12 proposed geometry
paths recorded as presentation-only bootstrap provenance.

## Boundary preserved

All Workshop actions and attachment relationships come from the real engine and
world model. The review overlay controls only illustrative placement. No model
calls, deployment, or publication were used.
