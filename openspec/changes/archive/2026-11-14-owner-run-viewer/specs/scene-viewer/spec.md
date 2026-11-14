## ADDED Requirements

### Requirement: Owner run viewer

Source: Brian, 2026-11-14: "i approve c then b then a" (A), "yes looks good"; mechanism and the local-only placement (art licence) inferred by agent.

The owner SHALL be able to open a saved run in the map viewer with one command that runs on the owner's machine. It SHALL read the run's saved rounds from the service using the owner password (never printed) or from a run-log file, take the world's bundle and layout from the first saved round, export a replay with that layout, and serve the viewer on localhost. It SHALL refuse with a plain message when no saved run belongs to a world that declares a layout. The viewer, its art and the map data SHALL NOT be served from the public site or the personal server.

#### Scenario: A run log is enough

- **GIVEN** a run log whose first round carries the world's bundle with a layout
- **WHEN** the owner command reads it
- **THEN** the replay is identical to the one exported from the bundle file

#### Scenario: No laid-out world

- **WHEN** no saved run belongs to a world with a layout
- **THEN** the command stops and says so
