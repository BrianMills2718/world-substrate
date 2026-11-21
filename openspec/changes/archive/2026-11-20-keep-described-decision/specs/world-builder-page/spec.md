## ADDED Requirements

### Requirement: A draft without the described decision is asked again

Source: Brian, 2026-11-20: "continue" (approving the recommended fix for issue #496); finding in `evidence/declared-laws/s4-waltzman-6/TRACE_READ.md`; mechanism inferred by agent.

When a description asks its people to make a shared decision and the draft has no decision, the builder SHALL ask again once, saying which decision is missing, and SHALL note in plain words when the second draft still has none. A draft that has its decision SHALL NOT be asked again for it.

#### Scenario: A draft without the described decision is asked again

- **GIVEN** a description whose people must decide whether to activate a system
- **WHEN** the first draft has no decision
- **THEN** the builder asks again with feedback naming that decision
- **AND** a draft that has its decision is not asked again
