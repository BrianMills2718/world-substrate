## ADDED Requirements

### Requirement: Knock-on chains of any length finish in one moment

The engine SHALL settle a moment's same-moment knock-on effects (`timing: immediately` processes) to the end with no
cap on their number, firing each (process, entity) pair at most once per moment, so every chain and loop ends. Each
knock-on step SHALL name the step that caused it, and a step a failed check stopped SHALL be recorded with its blocker
(the failed check and its value). Each run SHALL record the reaction limit it ran under (`null` for none), and replay
SHALL use the recorded limit; a record that names none ran under the old limit of 32.

Where it is enforced: `src/world_substrate/engine.py` (`Engine.__init__` `reaction_limit`, `_settle`,
`_blocked_steps`, `replay_commands`, `recorded_reaction_limit`), `src/world_substrate/action_authoring.py`
(`CompiledProcessMechanic.near_misses`), `scripts/run_authored_world.py` (`_round_reactions`, `_moments`, the run
record's `reaction_limit`).

Source: Brian, 2026-11-09: "50 things could propagate down a causal chain 100 links deep" (`docs/plans/ai_judge.md`,
Why, R1); build approved by Brian, 2026-11-10: "yes if ti si planned out and you have no quesitons for me". Replay
under the recorded limit: inferred by agent (plan, Agent technical calls; R10), so saved worlds still replay
unchanged.

#### Scenario: Fifty chains of a hundred links finish in one moment

- **WHEN** one move sets off 50 chains of 100 links each
- **THEN** all 5,000 steps happen in that moment with no refusal
- **AND** every step names the step that caused it, and the moment's summary reads 5,000 steps run, 5,000 with a
  cause

#### Scenario: A loop still ends

- **WHEN** a move sets off a ring of 40 things, each knocked by the one before and the first knocked by the last
- **THEN** each (process, thing) pair fires once, the first thing is knocked once more at the end, and the moment
  ends with 40 steps

#### Scenario: A blocked knock-on step is recorded with its blocker

- **WHEN** a 40-step loading line finishes and the next rule, "a loaded truck leaves if it has fuel", finds the
  truck has fuel 0
- **THEN** the truck does not leave, and the round records that step as blocked after step 40 with the failed check
  "the truck has fuel" and its value 0
- **AND** nothing follows from it

#### Scenario: A run saved under the old limit replays under it

- **WHEN** a run recorded before this change, with no reaction limit in its record, was refused for needing more
  than 32 reactions
- **THEN** its replay runs under 32 and is refused the same way, and its run page says "refused: knock-on effects
  did not settle within 32 steps (the limit this run ran under)"
- **AND** a new run of the same world has no limit and runs the whole chain
