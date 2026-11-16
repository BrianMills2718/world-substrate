## ADDED Requirements

### Requirement: The library is a left rail beside the run
The owner sees their saved worlds in a rail beside the run. The open world lists its runs, with each branch under the run it came from. Choosing a world or run opens it in the same view without calling a model. Worlds can be pinned to the top. Visitors do not get the rail.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md, increment 5).

#### Scenario: the-library-is-a-left-rail-beside-the-run
- **WHEN** the owner has a run open
- **THEN** a rail lists their worlds, the open world's runs and its branches
- **AND** choosing a run opens it in the same view
