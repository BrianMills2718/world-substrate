## ADDED Requirements

### Requirement: A quiet round does not end a run before its stop setting
A saved run that has had a round with nothing accepted and no move open stays continuable and branchable until the world's quiet-rounds stop setting (default 6) has been reached by consecutive such rounds. A world set not to stop for being quiet is never ended by quiet rounds alone.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md; the stop setting is the one Brian approved on the page, "Stop once nothing is changing, after N quiet rounds").

#### Scenario: a-quiet-round-does-not-end-a-run-before-its-stop-setting
- **WHEN** a run with a quiet-rounds setting of 3 has had one or two consecutive quiet rounds
- **THEN** the run can still continue
- **AND** after the third consecutive quiet round the run reports no active moves
