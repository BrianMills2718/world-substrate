## ADDED Requirements

### Requirement: Public room map of a shared run

Source: Brian, 2026-11-14: "build the public one"; word-hiding rule from the public scene's existing rule (a share shows nothing its viewer may not see); mechanism inferred by agent.

The service SHALL return, for a share link, a replay of the shared run on a generated map (never Smallville art or map data). It SHALL withhold the words of reports from callers who are not the owner, and SHALL refuse with a reason when the world declares no layout.

#### Scenario: A visitor opens a share link's room map

- **GIVEN** a shared run of a world whose layout names a room map
- **WHEN** a visitor without the owner password requests the replay
- **THEN** the replay carries the generated grid, every report's chat line reads "(words not shown)", and no private map name appears in it
- **AND** the same request from the owner keeps the words

#### Scenario: A world with no layout has no room map

- **GIVEN** a shared run of a world with no layout
- **WHEN** its replay is requested
- **THEN** the service answers 404 saying the world declares no layout
