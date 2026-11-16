## MODIFIED Requirements

### Requirement: Public room map of a shared run

Source: Brian, 2026-11-14: "build the public one"; word-hiding rule from the public scene's existing rule (a share shows nothing its viewer may not see); changed 2026-11-16 by Brian: "my instinct is that ifw e have the capabilities to drwa the maps we should aways have one"; mechanism inferred by agent.

The service SHALL return, for a share link, a replay of the shared run on a generated map (never Smallville art or map data). It SHALL withhold the words of reports from callers who are not the owner, and SHALL refuse with a reason only when the world declares no layout and has no actor to draw.

#### Scenario: A visitor opens a share link's room map

- **GIVEN** a shared run of a world whose layout names a room map
- **WHEN** a visitor without the owner password requests the replay
- **THEN** the replay carries the generated grid, every report's chat line reads "(words not shown)", and no private map name appears in it
- **AND** the same request from the owner keeps the words

#### Scenario: A world with nobody to draw has no room map

- **GIVEN** a shared run of a world with no layout and no actors
- **WHEN** its replay is requested
- **THEN** the service answers 404 saying there is no actor to draw

## ADDED Requirements

### Requirement: Every world has a map

Source: Brian, 2026-11-16: "my instinct is that ifw e have the capabilities to drwa the maps we should aways have one"; "isnt everythgin illsutrative"; layout choice (an office per actor, a meeting room) inferred by agent.

A world that declares no layout SHALL be drawn as one office per actor round a meeting room, without changing the world. People SHALL stay in their offices, go to the meeting room in a round where their move names a meeting, and return afterwards. The replay SHALL say the layout is illustrative.

#### Scenario: A world with no places gets an office for each group and a meeting room

- **GIVEN** a shared run of a world with three actors, a meeting and no places
- **WHEN** its replay is requested
- **THEN** the replay's rooms are one office per actor plus a meeting room, on the generated office map, with an illustrative note

#### Scenario: People stay in their offices and walk to the meeting room only for a meeting

- **GIVEN** a round where two of three actors attend the meeting
- **WHEN** the replay is read
- **THEN** those two stand in the meeting room at the end of that round and the third stays in their office, and everyone is back in their own office after a round with no meeting

#### Scenario: A message to another group shows as a chat line and its words are withheld from visitors

- **GIVEN** a move that sends a message to another actor
- **WHEN** a visitor requests the replay
- **THEN** a chat line shows the message was sent and its words read "(words not shown)"

#### Scenario: The office map connects the meeting room to every office and holds ten

- **WHEN** the office map is built
- **THEN** every office joins the meeting room through a two-tile doorway and every room has space for ten people

#### Scenario: The viewer shows the note that a drawn layout is illustrative

- **WHEN** a replay carries an illustrative note
- **THEN** the viewer shows it under the title

#### Scenario: The old graph page sends visitors to the graph beside the room map

- **WHEN** someone opens an old graph page link
- **THEN** they land in the room-map viewer with the graph beside the map
