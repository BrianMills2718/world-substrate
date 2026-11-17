## ADDED Requirements

### Requirement: The outcome bar follows the round
For a world with a group decision, the run page shows above the map where the decision stands after the round the map shows: the question, its status, support and conditional counts against the number needed, each position counted, meetings held and the deadline meeting. It changes when the round slider moves and is absent for a world with no group decision.

Source: Brian, 2026-11-17: "on decision 2 i apprbe yourr ecommendatino"

#### Scenario: the-outcome-bar-follows-the-round
- **WHEN** a run of a world with a group decision is open and the round slider moves from round 1 to a later round
- **THEN** the bar shows the counts after that round
- **AND** a world with no group decision shows no bar
