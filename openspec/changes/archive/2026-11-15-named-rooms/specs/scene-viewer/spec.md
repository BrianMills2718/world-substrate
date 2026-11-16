## ADDED Requirements

### Requirement: Named rooms and objects
Source: Brian, 2026-11-14: "is it supposed to look like this [Image #4] in the top portion?" and "i approve your recommendation".
A replay of a world with a layout SHALL name each room and show each thing that stands in a laid-out room, and the viewer SHALL draw them.

#### Scenario: The pump facility shows its rooms and its pump
- **WHEN** the pump facility replay is exported
- **THEN** it names Laboratory, Corridor and Control room, puts no name on a wall that has a doorway, and places the prototype pump in the laboratory at least four steps from any doorway
