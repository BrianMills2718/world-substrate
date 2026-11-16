## ADDED Requirements

### Requirement: Zoom and pan
Source: Brian, 2026-11-14: "i approve your recommendation" (Decision 4 = C); zoom listed in the goal text of 2026-11-15.
The room-map viewer SHALL let a person zoom into the map with the wheel, move it by dragging, and return to the whole map with one button, with the graph overlay following.

#### Scenario: The viewer wires zoom, pan and reset
- **WHEN** the viewer page is loaded
- **THEN** it has a "Reset view" button and handlers for the wheel and for dragging that refit the map and redraw the graph
