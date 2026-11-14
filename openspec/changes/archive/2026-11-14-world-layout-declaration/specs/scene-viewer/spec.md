## ADDED Requirements

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
