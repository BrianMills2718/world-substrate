## ADDED Requirements

### Requirement: A what-if branch can change one group's brief
When the owner branches a run at a finished round, they may name one group and write one sentence; the branch's groups play on with that sentence added to that group's own brief, and the branch says which group was changed and what it was told. No other group's brief and no rule changes, and the original run is unchanged.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md, canonical example: "branches with one change").

#### Scenario: a-what-if-branch-can-change-one-groups-brief
- **WHEN** the owner picks the legal group, writes "Its data-sharing concern was settled last week", and presses What if from round 2
- **THEN** the branch's first round runs with that sentence added to the legal group's brief only
- **AND** the branch label names the legal group and the sentence, and the original run is unchanged
