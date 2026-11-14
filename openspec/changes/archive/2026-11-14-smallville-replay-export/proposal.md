## Why

Brian chose to use Smallville's own front end for an inhabited scene (2026-11-14, "if it is better then lets just use that"). It replays from `master_movement.json`, which needs tile coordinates the substrate does not have.

## What changes

A tested exporter turns a retained run into that replay file, taking room anchors and walkable tiles from a map. The rules never see a coordinate.

Source: Brian, 2026-11-14 ("yes" to the spike); mechanism inferred by agent.
