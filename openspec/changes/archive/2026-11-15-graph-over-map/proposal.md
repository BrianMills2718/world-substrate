## Why

Brian, 2026-11-14: "i approve your recommendation" (Decision 4 = C: one graph layer, alone for Waltzman and over the room map for worlds with a layout), after "that whole thing as an overlay over the spatial structure". Slice 1 (PR #413) drew it alone. This slice draws it over the map.

## What Changes

- A replay made with a causal model carries `graph` (the world's graph and each round's lit tries) and `graph_actors` (graph actor to person shown).
- The room-map viewer has a "Show graph" switch: people tagged where they stand, the moves they tried and the things those moves used in boxes left of the map, linked and lit blue (allowed), orange (refused, with the reason) or grey (no move), each said in words; an "every box" tick shows the rest.
