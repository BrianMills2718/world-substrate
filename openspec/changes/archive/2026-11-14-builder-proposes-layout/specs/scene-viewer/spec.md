## ADDED Requirements

### Requirement: The Builder proposes a layout

Source: Brian, 2026-11-14: "i approve" (Decision 1, layouts yes); mechanism inferred by agent.

After building a world's structure and rules, the Builder SHALL make one optional extra call that places the world's places on a prepared public map, and SHALL attach the result as the world's `layout` only when it passes `validate_layout`. The step SHALL NOT fail the build, SHALL NOT run when the build has under one cent of budget left, and SHALL NOT replace a layout the world already has. A door declared with no halves SHALL be drawn as an always-open doorway.

#### Scenario: A spatial world gets a layout

- **GIVEN** a built world with rooms, doors and people
- **WHEN** the model returns a layout that passes validation
- **THEN** the world's bundle carries it and a share link of a run of that world can show the room map

#### Scenario: A world with no places or a bad layout is built as before

- **GIVEN** a built world with no places, or a reply that fails validation twice
- **WHEN** the step runs
- **THEN** the bundle is returned unchanged and the build succeeds
