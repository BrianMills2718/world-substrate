## MODIFIED Requirements

### Requirement: What if branches a run from the round on the map
The owner can press "What if…" beside the map to play the same world again from the round the map shows. The original run is kept as it was and drawn beside the branch, which plays live. A round the engine cannot branch greys the button and says why in words. Visitors do not see the button. A saved library run opened for replay is drawn on the map from the catalog, so the owner can branch it.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md, increment 4); lever fallback "same start, a new draw" decided by agent, inferred from the engine.

#### Scenario: what-if-branches-a-run-from-the-round-on-the-map
- **WHEN** the owner presses What if at round 4 of a saved run
- **THEN** a separate run starts from round 4 and plays live on the right of the original
- **AND** a round that cannot be branched shows the button greyed with the reason
