## ADDED Requirements

### Requirement: Public generated map

Source: Brian, 2026-11-14: "build the public one"; mechanism inferred by agent.

A prepared map MAY be generated from code instead of read from Smallville's data: a hub room with up to four rooms off it, each joined to the hub by a two-tile door gap, drawn with CC0 tiles committed to the repository. A replay on such a map SHALL carry its tile grid and need no Smallville file; the viewer SHALL draw it with the committed sheet, doors, furniture, people and text as it does for Smallville's map.

#### Scenario: A story exports and draws with no private art

- **GIVEN** a world whose layout names a generated map
- **WHEN** a saved run is exported with no Smallville clone present
- **THEN** every walk crosses a two-tile doorway one tile per step and the replay carries the grid the viewer draws
