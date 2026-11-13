## ADDED Requirements

### Requirement: Actor-authored report exposure

Source: Brian's approved I0/I1 goal, 2026-11-12; integration-2 findings 2 and 7.

The existing action language SHALL support append_report from an actor's string argument into an existing participant's string_list. It SHALL append one immutable exposure record, recording actual sender, recipient, content, event, revision and direct delivered channel. It SHALL leave originating claim lineage undeclared unless actually known; it SHALL NOT infer independent corroboration, belief, stance, assent or technical truth. The compiler SHALL derive both read and write authority on the appended field. Autonomous processes SHALL NOT use this operation.

#### Scenario: An action appends one report record to a participants list

- **WHEN** an actor submits a valid report and then another actor reports to the same recipient
- **THEN** the earlier entry remains unchanged and both entries identify their actual senders and delivery events
- **AND** invalid content, invalid target or insufficient scope is refused atomically with inspectable evidence
