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
