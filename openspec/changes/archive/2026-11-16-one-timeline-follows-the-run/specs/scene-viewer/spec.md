## ADDED Requirements

### Requirement: One timeline follows the run and the saved panels
The map's timeline is the only round control in the run view. The embedded viewer reports the round it shows to the page and says whether it is the newest; after a person scrubs back it offers a way back to the newest round. For a saved run the page's saved-run panels follow the round the map shows.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md, increment 3).

#### Scenario: one-timeline-follows-the-run-and-the-saved-panels
- **WHEN** a person scrubs the map's timeline to an earlier round
- **THEN** the map says it shows an earlier round and offers a way back to the newest round
- **AND** the page's saved-run panels show that round
