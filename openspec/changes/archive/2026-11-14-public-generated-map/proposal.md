## Why

Brian, 2026-11-14: "build the public one" (a map view in the public workspace). Smallville's art and map data are private-use, so a public scene needs its own map and CC0 art.

## What Changes

- `scripts/generated_map.py` makes a room map from code (a hub with up to four rooms off it, two-tile door gaps, furniture) with Kenney Tiny Dungeon tiles (CC0, committed under `viewer/smallville/assets-cc0/`).
- Two prepared maps (`public-hub-3`, `public-hub-5`) join `viewer/maps/maps.json`; the viewer draws any replay that carries a `grid` from the CC0 sheet and needs no Smallville files.
- Not in this change: serving it from the service and the public page.
