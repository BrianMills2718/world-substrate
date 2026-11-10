## ADDED Requirements

### Requirement: A run stops once nothing is changing

A World Builder world SHALL carry a stop setting chosen on the Create page and saved with the world: stop once
nothing is changing after N quiet rounds (the default for new worlds, N = 6), or always run every round. A run of a
world with the setting SHALL record why it stopped, and the run page SHALL say it in one plain line. A world or run
saved without the setting SHALL run every round and record nothing new.

Where it is enforced: `scripts/run_stop.py` (the rule), `scripts/run_authored_world.py` (checked after each round),
`scripts/world_builder_service.py` (`run_stop` on `/generate-world` and `/run`), `scripts/world_builder_home.html`
(the Options control and the run-page line).

Source: Brian, 2026-11-10: "on d1. stop condition should be configurable." (open question Q12; the default of 6
quiet rounds after the decision is settled is the recommendation he was answering).

#### Scenario: The Create page offers when to stop a run

- **WHEN** a visitor opens Options on the Create page
- **THEN** "When to stop a run" offers "Stop once nothing is changing, after N quiet rounds" with N = 6 selected,
  N editable from 1 to 100, and "Always run every round"
- **AND** the chosen setting is returned with the built world as `run_stop` and sent with each of its rounds

#### Scenario: A run stops after N quiet rounds

- **WHEN** a world without a group decision has N rounds in a row in which no person's move changed anything and
  the fields people's moves can change stayed the same
- **THEN** the run stops at that round and its summary records `stopped` with `reason: quiet_rounds`, the round
  and a sentence such as "Stopped at round 4: nothing had changed for 3 rounds."
- **AND** live play, which asks for one round at a time, carries the count across requests in `stop_history`

#### Scenario: A group decision must be settled

- **WHEN** a world has a group decision
- **THEN** the run stops only once every decision is deployed or rejected and the fields people's moves can change
  are back to what they were N rounds earlier
- **AND** fields only the world's own processes write, such as a meeting countdown, do not count as change

#### Scenario: Always run every round

- **WHEN** the setting is "Always run every round"
- **THEN** the run plays every round asked for and records `stopped` with `reason: round_cap`

#### Scenario: A world without the setting runs every round

- **WHEN** a saved world or run has no stop setting
- **THEN** it runs every round and its summary has no `stopped` record, exactly as before
