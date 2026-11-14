## Why

Brian, 2026-11-14: "build the public one". Slice 1 made the generated map; this slice lets anyone with a share link see the run on it.

## What Changes

- The World Builder service answers `GET /share/<id>/replay` with the run drawn on a generated map. A world whose layout names a private map is drawn on the generated map with the same number of rooms; a world with no layout has no map (404 with the reason). Report words are replaced by "(words not shown)" unless the caller is the owner.
- A public page `/world-builder/room-map/?share=<id>` (the viewer, the CC0 sheet and its licence only) reads that route; the shared-run view links to it.
