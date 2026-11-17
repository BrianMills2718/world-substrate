## ADDED Requirements

### Requirement: The map frame shows the whole viewer
On the run page the frame holding the room map and graph is as tall as the viewer inside it (up to 3,200 px), so the round slider and the graph are visible without scrolling inside the frame.

Source: Brian, 2026-11-17: "the display isnt working did you even tes thits?"

#### Scenario: the-map-frame-shows-the-whole-viewer
- **WHEN** the embedded viewer renders a world whose viewer is taller than the frame's old fixed height
- **THEN** the viewer reports its height to the page and the page makes the frame that tall
- **AND** the round slider is inside the visible frame
