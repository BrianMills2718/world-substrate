## ADDED Requirements

### Requirement: A narrow embed shows the map alone
When the viewer is embedded in a window narrower than 700 px, the graph does not open by itself; the map shows alone and the Show graph button opens the graph on request.

Source: Brian, 2026-11-17: "the display isnt working did you even tes thits?"

#### Scenario: a-narrow-embed-shows-the-map-alone
- **WHEN** the run page embeds the viewer with the graph requested and the window is 390 px wide
- **THEN** the map is shown without the graph
- **AND** the Show graph button is available
