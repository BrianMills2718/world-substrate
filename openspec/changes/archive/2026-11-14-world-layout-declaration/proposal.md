## Why

The Smallville-style viewer showed the pump facility only because its three rooms, two doors and three sprites were chosen by hand inside the exporter. Brian, 2026-11-14: "the world building part is going to have to declare locations and stuff that work with the map presumably", then "i approve c then b then a" (B). A world must declare its own layout so any spatial world gets a map.

## What Changes

- The authoring bundle gains an optional `layout`: a prepared map id, place to map slot, door to the two places it joins (and its entity halves), and each person's starting place and optional sprite.
- Prepared maps (names only, no art) live in `viewer/maps/maps.json`; two exist: the Ville dorm (a common room with four rooms off it) and Oak Hill College (a hallway with a classroom and a library).
- Validation refuses a layout that cannot be drawn. The exporter reads the bundle's layout instead of hand-written configuration and reproduces the earlier replays exactly.
- Not changed: the World Builder's prompts do not yet offer layouts to the model (a later step, needs a deploy).
