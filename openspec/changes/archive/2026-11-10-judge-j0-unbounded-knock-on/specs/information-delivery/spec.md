## MODIFIED Requirements

### Requirement: Same-moment reactions cite their cause (current code)

A same-moment knock-on reaction SHALL cite as its hard causal parent the latest event of the same moment it reacts to (`Engine._settle`, `src/world_substrate/engine.py:964`), and each of its steps SHALL name the step that caused it (`reaction_steps`: `it`, `caused_by`, `via`). New runs have no cap on a moment's reactions: each (process, entity) pair fires at most once per moment, so every chain ends. A run recorded with a limit (records made before the AI judge plan's J0 ran under 32, `LEGACY_REACTION_LIMIT`, `engine.py:155`) replays under it, and a moment over that limit, or a reaction that would break a declared law, is refused whole.

Source: Decision 009, Brian, 2026-10-26: "i approve"; the cap removed by the AI judge plan's J0 (Brian, 2026-11-09: "50 things could propagate down a causal chain 100 links deep"; build approved 2026-11-10)

#### Scenario: A reaction names the event it reacts to

- **WHEN** a same-moment knock-on reaction fires
- **THEN** `Engine._settle` records as its hard causal parent the latest event of that moment that changed its entity, else the triggering event (in the glass-chain test, the fall cites the push, the break cites the fall, and the spill and crash-sound each cite the break)

#### Scenario: A knock-on step names the step that caused it

- **WHEN** one move sets off chains of knock-on effects in one moment
- **THEN** each step's record names the step that caused it (`caused_by`) and the linked things it came through (`via`), with no cap on how many steps the moment has

#### Scenario: A moment needs too many reactions

- **WHEN** a run recorded under a limit (32 for runs recorded before J0) has a moment that would need more reactions than that
- **THEN** the whole moment is refused with status `reaction_limit` and the failed check "Knock-on effects settle within 32 reactions"
- **AND** the world is left as it was, with the refusal as the only event added

#### Scenario: A reaction would break a declared law

- **WHEN** a reaction would break a declared law
- **THEN** the whole moment is refused with status `law_breach`
