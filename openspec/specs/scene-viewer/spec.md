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

### Requirement: Rules overlay

Source: Brian, 2026-11-14: "i approve" (overlay of the world's rules on the map; computer only); tag colours and click-through inferred by agent.

When a replay carries the world's rules, the viewer SHALL offer a switch that shows each rule on the map and marks, for the step shown, the rule each person's attempt met as allowed or refused with the failed check named in words as well as colour. A replay made from a shared run SHALL carry the rules of that run's world; rule text is the world's own definition and carries no report words.

#### Scenario: A refusal shows the rule that caused it

- **GIVEN** a saved run in which a person tries to walk through a closed door
- **WHEN** the replay is exported with the world's causal model
- **THEN** that step records the move rule, refused, with "the door must be open", on that door
- **AND** the later step where the door opens records the open-door rule as allowed

### Requirement: The Builder proposes a layout

Source: Brian, 2026-11-14: "i approve" (Decision 1, layouts yes); mechanism inferred by agent.

After building a world's structure and rules, the Builder SHALL make one optional extra call that places the world's places on a prepared public map, and SHALL attach the result as the world's `layout` only when it passes `validate_layout`. The step SHALL NOT fail the build, SHALL have its own small spending allowance on top of what the build spent (the build uses nearly all of its own), SHALL log why a layout was skipped, and SHALL NOT replace a layout the world already has. A door declared with no halves SHALL be drawn as an always-open doorway.

#### Scenario: A spatial world gets a layout

- **GIVEN** a built world with rooms, doors and people
- **WHEN** the model returns a layout that passes validation
- **THEN** the world's bundle carries it and a share link of a run of that world can show the room map

#### Scenario: A world with no places or a bad layout is built as before

- **GIVEN** a built world with no places, or a reply that fails validation twice
- **WHEN** the step runs
- **THEN** the bundle is returned unchanged and the build succeeds

### Requirement: Any world's actions and doors show

Source: inferred by agent, from the first live Builder-made world (clinic, 2026-11-14) failing to export.

The replay exporter SHALL show every action kind of any world, not only the pump facility's, and SHALL draw a door open from the first step someone walks through it when the world has no action that opens it.

#### Scenario: A clinic world exports

- **GIVEN** a shared run of a Builder-made world whose actions include check-in, unlock-lab-door and examine
- **WHEN** its room-map replay is requested
- **THEN** each action appears in words, and the door two people walk through is open from that round

### Requirement: World graph
Source: Brian, 2026-11-14: "i approve your recommendation" (Decision 4 = C, one whole-system graph layer).
A shared run SHALL be viewable as one graph of everything in its world (who acts, the moves its rules allow, the things and places, the changes it makes by itself) with the chosen round lit, whether or not the world has a layout.

#### Scenario: Waltzman graph carries every box and the round's tries
- **WHEN** the graph of the Waltzman share is built
- **THEN** it has 70 boxes (10 who act, 17 moves, 17 things, 26 by-itself changes), 411 links, and each round lists every actor's try with allowed, refused or no-move

#### Scenario: A refusal keeps its reason and no words
- **WHEN** a round has a refused try
- **THEN** the graph names its reasons and carries no message words

### Requirement: Graph over the map
Source: Brian, 2026-11-14: "i approve your recommendation" (Decision 4 = C, the graph as an overlay over the spatial structure).
A replay of a world with a layout SHALL carry the whole-system graph, and the room-map viewer SHALL draw it over the map for the step shown.

#### Scenario: A refused try shows orange with its reason
- **WHEN** the graph is on at a step where someone's try was refused
- **THEN** their tag, their move and the things it used are orange, and the tag says "refused" with the reason

#### Scenario: The replay carries the graph
- **WHEN** a replay is exported with a causal model
- **THEN** it holds the graph, one lit entry per round, and the graph actor for each person shown

### Requirement: Named rooms and objects
Source: Brian, 2026-11-14: "is it supposed to look like this [Image #4] in the top portion?" and "i approve your recommendation".
A replay of a world with a layout SHALL name each room and show each thing that stands in a laid-out room, and the viewer SHALL draw them.

#### Scenario: The pump facility shows its rooms and its pump
- **WHEN** the pump facility replay is exported
- **THEN** it names Laboratory, Corridor and Control room, puts no name on a wall that has a doorway, and places the prototype pump in the laboratory at least four steps from any doorway

### Requirement: Zoom and pan
Source: Brian, 2026-11-14: "i approve your recommendation" (Decision 4 = C); zoom listed in the goal text of 2026-11-15.
The room-map viewer SHALL let a person zoom into the map with the wheel, move it by dragging, and return to the whole map with one button, with the graph overlay following.

#### Scenario: The viewer wires zoom, pan and reset
- **WHEN** the viewer page is loaded
- **THEN** it has a "Reset view" button and handlers for the wheel and for dragging that refit the map and redraw the graph

### Requirement: Whole network over the map
Source: Brian, 2026-11-16: "ok in the compelte network tba that is what i was tlakign about and i figured thgat couldbe overlaid on the physical map?"
The room-map viewer's graph overlay SHALL offer a whole-network mode that places every graph box on the map (places at their rooms, things in their room, people where they stand, moves and processes in the margin) and draws every link faintly, with the round's tries still lit blue, orange or grey with words.

#### Scenario: The viewer wires the whole-network mode
- **WHEN** the viewer page is loaded for a replay that carries a graph
- **THEN** its graph overlay has a "Whole network" tick that places every box and draws every link

### Requirement: Graph style choice
Source: Brian, 2026-11-16: "can you show me A and B. like have it toggalable maybe?"
The room-map viewer SHALL let a person choose how the whole network is shown: on the map with every link, on the map with links only for a clicked box, or in columns beside the map where clicking a box lights its links and rings it on the map, and SHALL open in a given style from a link.

#### Scenario: The viewer offers the styles and opens one from a link
- **WHEN** the viewer page is loaded for a replay that carries a graph
- **THEN** its graph style choice offers this round only, on the map, on the map with links on click, and beside the map, and a `graph` link parameter opens one of them

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

### Requirement: A running world is drawn on the map as it plays
While a world runs on the World Builder page, the run stage shows the room map with the graph beside it, and the map grows after every finished round. The page asks the service for the room-map replay of the rounds so far; the service rebuilds it from its own run log, saves nothing, and withholds message words from visitors. The viewer, opened for embedding, takes each longer replay, extends its timeline and plays on to the newest round unless the person scrubbed back.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md, increment 2).

#### Scenario: a-running-world-is-drawn-on-the-map-as-it-plays
- **WHEN** a run has finished one or more rounds and the page asks for its live replay
- **THEN** the service answers with the room-map replay of those rounds, saves nothing, and a visitor's copy withholds message words
- **AND** a private catalog run needs the owner
- **AND** the embedded viewer takes a longer replay by message and follows the newest round
