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
