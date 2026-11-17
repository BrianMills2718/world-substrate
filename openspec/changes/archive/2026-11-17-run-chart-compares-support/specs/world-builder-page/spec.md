## ADDED Requirements

### Requirement: The run chart compares support by round
For a branch of a world with a group decision, the run page shows a chart of the number of groups supporting it by round for the original run and the branch, with the number needed and the fork round marked. The two lines differ by style and are named in words, not colour alone. The branch line starts at the original's value at the fork round.

Source: Brian, 2026-11-17: "on decision 2 i apprbe yourr ecommendatino"

#### Scenario: the-run-chart-compares-support-by-round
- **WHEN** a saved branch of a world with a group decision is open
- **THEN** a chart shows the original and the branch by round, with the fork round marked
- **AND** a run that is not a branch shows no chart
