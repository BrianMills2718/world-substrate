## ADDED Requirements

### Requirement: The designer reports additions apart from unrepresented parts

The structure the designer returns MAY carry a top-level `added_to_run`: short plain strings naming things it added
that the description does not state, so the world can run. `not_modeled` is only for parts of the description that
could not be represented. Neither field SHALL be stored in the validated bundle.

Where it is enforced: contract and parsing in `scripts/generate_world_bundle.py`.

Source: BrianMills2718/world-substrate#241; requirement inferred by agent.

#### Scenario: The contract names both fields

- **WHEN** the designer's prompt is built
- **THEN** the contract describes `added_to_run` and says `not_modeled` must never hold something that was added

#### Scenario: Additions are returned beside the bundle

- **WHEN** the model returns a valid bundle with `added_to_run: ["a doorway"]` and `not_modeled: ["before noon"]` and the caller passes `added_out=[]`
- **THEN** the returned `not_modeled` is `["before noon"]` and `added_out` is `["a doorway"]`
- **AND** the returned bundle has neither key
- **AND** a caller that does not pass `added_out` still gets the unchanged three-part return

#### Scenario: A malformed additions list is repaired

- **WHEN** the model returns `added_to_run` that is not a list of strings
- **THEN** the existing repair loop is used with an error naming `added_to_run`, exactly once per repair

#### Scenario: A redesign keeps earlier additions

- **WHEN** the designer is asked to redesign from a previous structure
- **THEN** the message tells it to return the full `added_to_run` list, keeping earlier items that still hold
