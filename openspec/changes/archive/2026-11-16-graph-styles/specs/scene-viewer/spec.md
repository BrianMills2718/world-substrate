## ADDED Requirements

### Requirement: Graph style choice
Source: Brian, 2026-11-16: "can you show me A and B. like have it toggalable maybe?"
The room-map viewer SHALL let a person choose how the whole network is shown: on the map with every link, on the map with links only for a clicked box, or in columns beside the map where clicking a box lights its links and rings it on the map, and SHALL open in a given style from a link.

#### Scenario: The viewer offers the styles and opens one from a link
- **WHEN** the viewer page is loaded for a replay that carries a graph
- **THEN** its graph style choice offers this round only, on the map, on the map with links on click, and beside the map, and a `graph` link parameter opens one of them
