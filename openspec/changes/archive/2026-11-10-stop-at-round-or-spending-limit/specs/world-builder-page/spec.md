## ADDED Requirements

### Requirement: A run stops at a round or spending limit

A World Builder world's stop setting SHALL also take two optional limits, each off unless the visitor ticks it on
the Create page: stop after N rounds (`max_rounds`, 1 to 500) and stop once this run's AI spending reaches $X
(`max_spend_usd`, $0.01 to $100). They SHALL combine with the quiet choice, and the run SHALL stop at whichever fires
first. Spending SHALL be the cost llm_client recorded for the run's own calls, never an estimate, and SHALL be
checked before each round, so a round under way finishes. A world or run saved without the limits SHALL behave
exactly as before.

Where it is enforced: `scripts/run_stop.py` (`limit_check`), `scripts/run_authored_world.py` (checked before the
first round of a request and after each round), `scripts/world_builder_service.py` (`run_spent_usd` on `/run`,
recorded cost from `_trace_cost`), `scripts/world_builder_home.html` (the Options controls and the run-page line).

Source: Brian, 2026-11-10: "i should be able to stop a world based on budget or number of rounds or a natural langue
stopping potin that the judge assesses once we build him" (the plain-words stopping point waits for the AI judge,
`docs/plans/ai_judge.md`).

#### Scenario: The Create page offers a round and a spending limit

- **WHEN** a visitor opens Options on the Create page
- **THEN** "When to stop a run" also offers "Stop after N rounds" (N = 40 shown) and "Stop when this run has spent
  $X" ($0.50 shown), each with a checkbox that starts unticked
- **AND** a ticked limit is saved in the world's `run_stop` and sent with each of its rounds

#### Scenario: A run stops at the round limit you set

- **WHEN** a world's setting has `max_rounds: N` and round N is played
- **THEN** the run stops at round N and records `stopped` with `reason: round_limit` and a sentence such as
  "Stopped at round 40: the limit of 40 rounds you set."

#### Scenario: A run stops once it has spent its limit

- **WHEN** a world's setting has `max_spend_usd: X` and the cost recorded for the run's calls, carried across live
  play's one-round requests as `run_spent_usd`, reaches X after a round
- **THEN** the run plays no further round and records `stopped` with `reason: budget`, the amount spent and a
  sentence such as "Stopped at round 18: this run had spent $0.41 of its $0.40 limit. A round already under way
  always finishes, so it went a little over."

#### Scenario: Whichever stop fires first wins

- **WHEN** a world's setting combines quiet rounds with a round or spending limit
- **THEN** the run stops at the first round any of them is met, and records that one as the reason

#### Scenario: The stop setting is checked

- **WHEN** a setting has a round limit outside 1 to 500, a spending limit outside $0.01 to $100, or an unknown key
- **THEN** the request is refused before any spend

## MODIFIED Requirements

### Requirement: A run stops once nothing is changing

A World Builder world SHALL carry a stop setting chosen on the Create page and saved with the world: stop once
nothing is changing after N quiet rounds (the default for new worlds, N = 6), or do not stop for being quiet. A run of a
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
  N editable from 1 to 100, and "Don't stop for being quiet"
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

- **WHEN** the setting is "Don't stop for being quiet" (`mode: every_round`) and no limit is set
- **THEN** the run plays every round asked for and records `stopped` with `reason: round_cap`

#### Scenario: A world without the setting runs every round

- **WHEN** a saved world or run has no stop setting
- **THEN** it runs every round and its summary has no `stopped` record, exactly as before
