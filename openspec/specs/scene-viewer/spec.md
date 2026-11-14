# scene-viewer Specification

## Purpose
Export a retained run as a replay a Smallville-style tile-map viewer can play, without putting coordinates in the rules.

## Requirements

### Requirement: Smallville replay export

Source: Brian's 2026-11-14 viewer decision; mechanism inferred by agent.

A retained run SHALL be exportable as a Smallville replay (`master_movement.json` and `meta.json`) from the run's recorded rounds and a map that names each room's walkable tiles. Each person's walk SHALL follow a path over the map's walkable tiles, at most one tile per step. A refused attempt SHALL leave the person in place and be labelled with the refusing check's reason, and a delivered report SHALL appear as the sender's chat line. An unreachable room SHALL fail the export with an error.

#### Scenario: A refused walk, a walk through a doorway and a report

- **GIVEN** a run in which a person is refused at a closed door, then walks to another room, then sends a report
- **WHEN** it is exported on a map with a doorway between the rooms
- **THEN** the refused step keeps the person's tile and names the reason
- **AND** the walk crosses the doorway one tile per step and the report appears once as a chat line

#### Scenario: An unreachable room fails loudly

- **WHEN** the map has no walkable path between two rooms
- **THEN** the export raises an error naming the missing path

### Requirement: Static replay viewer

Source: Brian's 2026-11-14 choice of option A; mechanism inferred by agent.

The viewer SHALL play an exported replay from static files with no server. It SHALL draw each door closed or open from the replay's door changes, show a refused attempt with its reason and a delivered report as readable text from the sender, place people sharing a room on different tiles, and fit the facility to the viewport at desktop and 390px widths. The map art SHALL NOT be committed; a setup script copies it from a local clone.

#### Scenario: Refusal at a closed door, then the door opens

- **GIVEN** an exported run in which a person is refused at a closed door and later opens it
- **WHEN** the viewer shows the refused step and then the later step
- **THEN** the door is drawn closed with the refusal reason shown, and later drawn open

#### Scenario: A report shows its words

- **WHEN** the viewer shows the step where one person reports to another
- **THEN** the sender's words appear as text above the sender and in the people panel

### Requirement: World layout declaration

Source: Brian, 2026-11-14: "the world building part is going to have to declare locations and stuff that work with the map presumably", "i approve c then b then a"; mechanism inferred by agent.

A world's authoring bundle MAY declare a `layout`: a prepared map id, a map slot for each place, the two places each door joins with the entity halves that open together, and each person's starting place and optional sprite. A layout SHALL be refused, naming the reason, when its map is not prepared, a place names an unknown slot, two places share a slot, a door joins places whose slots the map does not connect, a person or place is not declared, or laid-out places are not all joined by doors. A world without a layout SHALL still validate. The replay export SHALL take rooms, doors, people, labels and sprites from the layout alone, and the same story SHALL export on any prepared map whose slots connect the same way.

#### Scenario: A layout that cannot be drawn is refused

- **WHEN** a bundle's door joins two places whose map slots are not connected
- **THEN** validation fails and names the door, both places and the map

#### Scenario: The same story on a second map

- **GIVEN** the pump facility layout on the Ville dorm map
- **WHEN** the layout names the Oak Hill College map instead
- **THEN** it validates and exports, with the rooms and sprites of that map

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

### Requirement: Public generated map

Source: Brian, 2026-11-14: "build the public one"; mechanism inferred by agent.

A prepared map MAY be generated from code instead of read from Smallville's data: a hub room with up to four rooms off it, each joined to the hub by a two-tile door gap, drawn with CC0 tiles committed to the repository. A replay on such a map SHALL carry its tile grid and need no Smallville file; the viewer SHALL draw it with the committed sheet, doors, furniture, people and text as it does for Smallville's map.

#### Scenario: A story exports and draws with no private art

- **GIVEN** a world whose layout names a generated map
- **WHEN** a saved run is exported with no Smallville clone present
- **THEN** every walk crosses a two-tile doorway one tile per step and the replay carries the grid the viewer draws

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

### Requirement: Rules overlay

Source: Brian, 2026-11-14: "i approve" (overlay of the world's rules on the map; computer only); tag colours and click-through inferred by agent.

When a replay carries the world's rules, the viewer SHALL offer a switch that shows each rule on the map and marks, for the step shown, the rule each person's attempt met as allowed or refused with the failed check named in words as well as colour. A replay made from a shared run SHALL carry the rules of that run's world; rule text is the world's own definition and carries no report words.

#### Scenario: A refusal shows the rule that caused it

- **GIVEN** a saved run in which a person tries to walk through a closed door
- **WHEN** the replay is exported with the world's causal model
- **THEN** that step records the move rule, refused, with "the door must be open", on that door
- **AND** the later step where the door opens records the open-door rule as allowed
