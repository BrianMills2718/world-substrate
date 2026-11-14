## ADDED Requirements

### Requirement: Offered action forms follow what an actor can perceive

Source: Brian's 2026-11-13 goal; resident-run finding in `evidence/ui/inhabited-facility-20261113/TRACE_READ.md`; mechanism inferred by agent.

A declared public action form SHALL be offered to an actor only when every entity it names is in the actor's observation, except fields the form lists as `unobserved_refs`, and SHALL NOT be offered when a field listed in `not_self` names the actor. A declared entity that is place-scoped SHALL NOT appear in the observation of an actor in another place, whether it is a person or an object.

#### Scenario: An actor is offered what is at hand and not what is elsewhere

- **GIVEN** a facility with doors in two rooms and people in different rooms
- **WHEN** the actor in one room is offered actions
- **THEN** it can open its own door, naming the far side of that door it cannot see
- **AND** it is not offered another room's door, a report to itself, or sight of people in other rooms

### Requirement: Reports and refusals are visible scene effects

Source: Brian's 2026-11-13 goal; inferred by agent.

When a rule appends a report to the recipient's log, the replayed scene SHALL show a message from the sender to the recipient, and when a move is refused it SHALL show the refusing check's reason. These effects SHALL be derived from the recorded events through the existing scene profile and renderer, not drawn from a fixture.

#### Scenario: A real run's report and refusal appear in the replayed scene

- **WHEN** a catalog run in which one person is refused at a closed door and later sends a report is replayed
- **THEN** the refused frame shows the reason and the report frame shows a message from the sender to the recipient
