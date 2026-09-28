---
role: audit
status: implemented-candidate
reviewed_through: 2026-09-10
---

# Waltzman Kitchen-quality living-world v2

## Disposition

The first public Living Scene proved the generic architecture but failed product-owner
visual review because it read as letter tokens and dashboard cards inside dashed
boxes. That artifact remains useful regression evidence; it is not the visual bar.

The v2 candidate uses the same retained baseline/intervention world truth and replaces
only downstream presentation. The target is the product category already demonstrated
by the Kitchen replay: a coherent place with characters, objects, activities, and
visible state changes.

## Composition

`reference_worlds/waltzman/living-scene-v2.json` declares a project-owned illustrated
Coordination Hall. Six residents have distinct project-owned SVG character assets and
persistent work positions. Four prerequisite stations occupy room alcoves; the center
contains the meeting table and coalition core; the stabilization package has a staging
position and a separate delivered position.

The old dashed profile zones remain semantic/presentation anchors but are hidden. The
background owns illustrative architecture. All geometry is presentation-only.

## Retained story

The canonical history is unchanged:

- initial state: six supporters and healthy prerequisites;
- degraded prerequisite events visibly change local station values/status lights;
- retained communications appear transiently between exact source/recipient anchors;
- the canonical meeting active state gathers all six residents around the central table;
- baseline ends blocked at event `e00021`, support 2/6 and conditional 4;
- intervention event `e00022` moves/activates the stabilization package and repairs the
  represented prerequisites through retained changes;
- reassessment proceeds from retained history;
- intervention ends ready at `e00028`, support 6/6 and conditional 0.

## Interaction

The composed branch shell keeps history selection compact and outside the world. The
world itself contains compact transport/scrub controls. Actor/object selection opens a
contextual inspector; nothing is permanently open. Public inspection is limited to
fields already bound into visibility-safe Living Scene frames.

## Asset provenance

All shipped v2 SVGs under `reference_worlds/waltzman/assets-v2/` were authored for this
repository as simple geometric/vector presentation assets. The third-party screenshots
collected in UI-reference research are inspiration only and are not imported, embedded,
or redistributed by the v2 product artifact.

## Evidence

Retained browser evidence under `evidence/renders/` covers initial, information,
meeting-active, blocked, intervention, ready, blocked-mobile, ready-mobile, and a
selection inspector. These are generated from the actual composed branch player.

The Kitchen flagship remains the comparison baseline at
`evidence/renders/kitchen-spatial-replay-v1.html`. The goal is parity of product category
and scene hierarchy, not imitation of Kitchen's art style.
