## ADDED Requirements

### Requirement: Builder additions are listed apart from what was left out

Things the builder added to make a world run (for example a doorway the description does not mention) are listed
under their own heading, "Added to make it run", and never under "Left out of the simulation", which holds only
parts of the description that could not be represented.

Where it is enforced: `added_to_run` returned by `scripts/generate_world_bundle.py`, passed through
`scripts/world_builder_service.py`, shown by `scripts/world_builder_home.html`.

Router heuristic: none (project-specific).

Source: BrianMills2718/world-substrate#241; evidence `evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md`
finding 3; requirement wording inferred by agent.

#### Scenario: The builder adds a doorway

- **WHEN** a build's designer returns `added_to_run: ["A doorway between the office and hangar"]` and `not_modeled: ["before noon"]`
- **THEN** the `/generate-world` result has `added_to_run` equal to the doorway item and `not_modeled` equal to `["before noon"]`
- **AND** the build progress has an "Added to make it run" step listing the doorway and a "Left out of the simulation" step listing only "before noon"

#### Scenario: The page shows two separate lists

- **WHEN** the page renders a result with both lists
- **THEN** "Left out of the simulation" shows only the `not_modeled` items
- **AND** a separate disclosure "Added to make it run" shows only the `added_to_run` items

#### Scenario: Nothing was added

- **WHEN** a result has no `added_to_run` (empty or absent, as for people worlds)
- **THEN** no "Added to make it run" disclosure or progress step appears

## MODIFIED Requirements

### Requirement: Unrepresentable parts are listed

Parts of a description the simulator cannot represent are listed, not dropped silently. Only such parts are listed as
left out; anything the builder added is listed separately (see "Builder additions are listed apart from what was
left out").

Where it is enforced: `not_modeled` from `scripts/generate_world_bundle.py`.

Router heuristic: none (project-specific).

Source: Cold first-visit review, 2026-10-05 ("before noon" disappeared); narrowed by world-substrate#241.

#### Scenario: Part of a description cannot be represented

- **WHEN** a description contains something the simulator cannot represent (for example "before noon")
- **THEN** that part is listed as not modelled
- **AND** it is not dropped silently
