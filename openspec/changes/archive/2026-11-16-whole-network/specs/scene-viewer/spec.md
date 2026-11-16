## ADDED Requirements

### Requirement: Whole network over the map
Source: Brian, 2026-11-16: "ok in the compelte network tba that is what i was tlakign about and i figured thgat couldbe overlaid on the physical map?"
The room-map viewer's graph overlay SHALL offer a whole-network mode that places every graph box on the map (places at their rooms, things in their room, people where they stand, moves and processes in the margin) and draws every link faintly, with the round's tries still lit blue, orange or grey with words.

#### Scenario: The viewer wires the whole-network mode
- **WHEN** the viewer page is loaded for a replay that carries a graph
- **THEN** its graph overlay has a "Whole network" tick that places every box and draws every link
