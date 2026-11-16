## ADDED Requirements

### Requirement: Graph over the map
Source: Brian, 2026-11-14: "i approve your recommendation" (Decision 4 = C, the graph as an overlay over the spatial structure).
A replay of a world with a layout SHALL carry the whole-system graph, and the room-map viewer SHALL draw it over the map for the step shown.

#### Scenario: A refused try shows orange with its reason
- **WHEN** the graph is on at a step where someone's try was refused
- **THEN** their tag, their move and the things it used are orange, and the tag says "refused" with the reason

#### Scenario: The replay carries the graph
- **WHEN** a replay is exported with a causal model
- **THEN** it holds the graph, one lit entry per round, and the graph actor for each person shown
