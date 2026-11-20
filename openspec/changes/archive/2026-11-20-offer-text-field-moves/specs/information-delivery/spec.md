## ADDED Requirements

### Requirement: Generated moves are offered with their text left to the person

Source: Brian, 2026-11-20: "continue" (approving the recommended fix for issue #488); finding in `evidence/declared-laws/s4-waltzman-5/TRACE_READ.md`; mechanism inferred by agent.

A people build SHALL declare a public action form for every generated move whose referent fields can each be bound to a public entity the move's rule accepts there. Fields that are not referents SHALL be left open, and the resident SHALL be asked to state them in its own words. An open field SHALL NOT be a referent field. A move with a referent field that no public entity fits SHALL get no form.

#### Scenario: A move with only text fields is offered with its text left open

- **GIVEN** the saved Waltzman build whose generated moves take only text fields and at most a decision referent
- **WHEN** a country and a concern group are offered moves
- **THEN** every generated move is offered, the decision referent bound and the text fields asked for in the person's own words
- **AND** an open field that names a referent is refused as invalid

#### Scenario: A move whose referent no one can name gets no form

- **GIVEN** a generated move whose rule accepts no public entity for its referent field
- **WHEN** the build declares forms
- **THEN** that move gets no form and the other moves keep theirs
