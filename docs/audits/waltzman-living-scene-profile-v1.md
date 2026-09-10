# Waltzman Living Scene v1 composition evidence

Status: implemented for Company Planning #220.

## Authority boundary

`reference_worlds/waltzman/living-scene-v1.json` contains only presentation choices and exact bindings to retained canonical state/events. Resident positions, zones, text glyphs, styling, and layout are illustrative. Resident names/roles/organizations, commitment stance, resource quantities, safeguard state, activity timing, institution counts/status, package state, event order, and information delivery come from the retained World Substrate projections.

The generic runtime contains no Waltzman resident names, entity IDs, or rule branches. The two small generic additions made during composition are reusable: state-to-style tokens and rendering canonical labels through ordinary profile bindings. Neither changes canonical world state or event semantics.

## Retained inputs

- `evidence/waltzman/demo-baseline-v0.json`
- `evidence/waltzman/demo-intervention-v0.json`
- `reference_worlds/waltzman/living-scene-v1.json`

## Retained render evidence

- `evidence/renders/waltzman-living-baseline-v1.html`
- `evidence/renders/waltzman-living-intervention-v1.html`
- `evidence/renders/waltzman-living-v1-initial.png`
- `evidence/renders/waltzman-living-v1-blocked.png`
- `evidence/renders/waltzman-living-v1-intervention.png`
- `evidence/renders/waltzman-living-v1-ready.png`

The four checkpoints correspond to initial state, retained baseline blocked at event `e00021`, stabilization package applied at `e00022`, and recovered ready at `e00028`. No provider/model call or simulation rerun is needed to generate these presentation artifacts.
