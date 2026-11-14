## Why

Brian, 2026-11-14: "i approve" (the Builder writes a room layout for new worlds, so live share links can show the room map and rules overlay). Until now only the pump example carried a layout.

## What Changes

- After a world is built, one small optional call (`scripts/layout_proposal.py`, measured $0.0002) places its places on a prepared public map, or answers null when the world has no places. The local validator judges it; a layout that fails after one repair is dropped and the world is built as before. It never fails a build and stays inside the build's budget.
- A door with no `halves` is a doorway that is always open (worlds where people just walk between places).
