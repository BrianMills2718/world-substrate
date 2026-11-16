## ADDED Requirements

### Requirement: The draft keeps every named group
When a description names people or groups, the builder checks the draft against it, asks again once for any it left out, and says in plain words how many of the named groups are in the draft and which are not.

Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams" (docs/goals/unified-world-ux.md, increment 6).

#### Scenario: the-draft-keeps-every-named-group
- **WHEN** a description names ten groups and the first draft has four
- **THEN** the builder asks again with the six missing names
- **AND** the draft says how many named groups it holds and lists any still left out
