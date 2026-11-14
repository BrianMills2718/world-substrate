# Inhabited pump facility: place-scoped perception

Source: Brian, 2026-11-13: build a general-purpose simulator for Waltzman-style influence operations in an inhabited, interactive place; first slice a small facility (rooms, corridor, doors, actors, activities, conversations) where a closed door blocks Ari, opening it permits movement, and Bo's observation reflects location and delivered messages while retained memories and global knowledge stay available; replay and a saved-round branch show the same facts. Roadmap "Next: inhabited spatial world" (2026-11-13) recommends this slice. Design inferred by agent.

## Why

Native worlds already have places, doors (boundaries) and rule-governed movement, and the engine's own `observe` filters by colocation. The declared actor-information projection that residents actually read does not: every declared entity is visible from everywhere, so where a person stands changes nothing they perceive. Physical perception, delivered messages, global knowledge and memory must stay distinct for influence modeling.

## What Changes

- A public entity row in `actor_information` may declare `scope: "place"`. It is perceived only from the place it stands in or is. Rows without scope stay known everywhere (identities, the map, delivered reports).
- A declaration that uses a place scope adds to the observation the actor's place, who and what is physically here, and reports delivered to the actor from the actor's own declared report log, wherever the actor is. The prompt context shows these, global knowledge in `world_summary` and `brief`, and optionally retained `memories` as separate inputs.
- A small authored example world (laboratory, corridor, control room, two doors as directed boundary pairs, Ari, Mara, Bo, a pump and delivered reports) and its rules use only existing mechanics.
- The scene bridge shows a door's passable state.

No engine, scheduler, renderer or cognition capability is added. Place topology only: no coordinates, distance, travel time, occlusion, hearing range or pathfinding.

## Evidence

`tests/test_inhabited_facility.py`: a real catalog run with scripted choices (no model call), its replay frames and a saved-round branch; the same facts at the engine, actor-context and scene layers. A live LLM resident run in this world is not part of this change.
