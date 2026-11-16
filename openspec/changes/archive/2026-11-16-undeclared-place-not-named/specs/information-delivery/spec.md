## MODIFIED Requirements

### Requirement: Place-scoped perception with distinct inputs

Source: Brian's 2026-11-13 inhabited-facility request; inferred by agent for the mechanism; naming rule corrected after Brian, 2026-11-16: "i agree thatt this 'you are in <room name>' is a violation of the rules".

A declared public entity MAY be scoped to a place. An actor SHALL perceive a place-scoped entity's declared fields only while the entity stands in, or is, the actor's current place. Unscoped declared entities remain known everywhere. When a declaration uses a place scope, the actor's observation SHALL also name the actor's place only when the declaration publishes that place to the actor (an undeclared place's engine label is private existence and SHALL NOT enter the actor's context), list the declared entities physically present with it, and list reports delivered to the actor from its own declared report log regardless of place. The actor's prompt context SHALL present that observation, global knowledge (world summary and the actor's declared brief and knowledge) and any supplied retained memories as separate inputs; delivered reports and memories SHALL NOT be treated as physical perception, and place scope SHALL NOT be treated as a distance, hearing or occlusion model.

#### Scenario: A closed door blocks movement and opening it permits movement

- **GIVEN** a world with a closed directed door between two rooms
- **WHEN** an actor attempts to walk through it
- **THEN** the door's own rule refuses the attempt and the actor stays in the room
- **AND** after the actor opens the door the same attempt is accepted and changes the actor's place

#### Scenario: Observation follows place while reports and knowledge do not

- **GIVEN** an actor in another room from a place-scoped object and a report delivered to that actor
- **WHEN** the actor's context is built
- **THEN** the object's fields are absent and the delivered report is present
- **AND** global knowledge remains present and supplied memories appear only as memories

#### Scenario: Replay and a branch show the same facts

- **WHEN** a run is replayed and a saved round is branched with a different later choice
- **THEN** the replayed scene shows each person's place and each door's state as the rounds recorded them
- **AND** the branch begins from the checkpoint's facts and diverges without changing its parent

#### Scenario: An undeclared room is not named to the person standing in it

- **GIVEN** a place-scoped world whose declaration does not publish the room an actor stands in
- **WHEN** the actor's context is built
- **THEN** the room's name and id are absent, and who else is in the place is still present
