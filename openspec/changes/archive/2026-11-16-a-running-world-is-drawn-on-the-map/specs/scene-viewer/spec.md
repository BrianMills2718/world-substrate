## ADDED Requirements

### Requirement: A running world is drawn on the map as it plays
While a world runs on the World Builder page, the run stage shows the room map with the graph beside it, and the map grows after every finished round. The page asks the service for the room-map replay of the rounds so far; the service rebuilds it from its own run log, saves nothing, and withholds message words from visitors. The viewer, opened for embedding, takes each longer replay, extends its timeline and plays on to the newest round unless the person scrubbed back.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md, increment 2).

#### Scenario: a-running-world-is-drawn-on-the-map-as-it-plays
- **WHEN** a run has finished one or more rounds and the page asks for its live replay
- **THEN** the service answers with the room-map replay of those rounds, saves nothing, and a visitor's copy withholds message words
- **AND** a private catalog run needs the owner
- **AND** the embedded viewer takes a longer replay by message and follows the newest round
