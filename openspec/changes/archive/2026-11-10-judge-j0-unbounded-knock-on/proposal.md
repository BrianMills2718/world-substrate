## Why

A moment's knock-on effects stopped at 32 reactions: a longer chain was refused whole and nothing changed. Brian's
worlds need far more: "50 things could propagate down a causal chain 100 links deep" (Brian, 2026-11-09, the AI
judge plan's Why). Each (process, entity) pair already fires at most once per moment, so a chain cannot loop without
a cap; the bound is the finite number of such pairs. Slice J0 of `docs/plans/ai_judge.md`, approved for building by
Brian on 2026-11-10 ("yes if ti si planned out and you have no quesitons for me").

## What Changes

- New runs have no reaction cap (`Engine(reaction_limit=None)`); once per (process, entity) pair per moment still
  ends every chain and loop.
- Each run records the limit it ran under (`reaction_limit` in the run record, `null` for none); replay uses the
  recorded value, and a record that names none ran under the old cap of 32 (`recorded_reaction_limit`), so runs
  saved before this change replay unchanged.
- Each knock-on step names its cause: a reaction event carries `reaction_steps` (`it`, `caused_by`, `via`) and its
  wave.
- A step a failed check stopped is recorded with its blocker (`blocked_reactions`: the rule, the thing, the event it
  came after, the failed check and its value).
- The run page shows each moment's summary line ("N steps run, M with a cause, no refusal"), opens each step to the
  step that caused it, shows a blocked step in orange, and words an old refusal "refused: knock-on effects did not
  settle within 32 steps (the limit this run ran under)". A share link made before this change reads that refusal
  from the run log when opened.
- Decision 009 is amended in the same pull request.

## Impact

- Code: `src/world_substrate/engine.py`, `src/world_substrate/action_authoring.py`, `src/world_substrate/model.py`
  (faster entity copies, so 5,000 steps fit one request), `scripts/run_authored_world.py`,
  `scripts/world_builder_service.py`, `scripts/world_builder_home.html`.
- Tests: `tests/test_knock_on_unbounded.py`, `tests/knock_on_worlds.py`, `tests/test_open_attempt.py` (its refusal
  test runs against the recorded limit), `tests/test_system_model.py`.
- Docs: `docs/decisions/009-same-moment-knock-on-effects.md`, `docs/architecture/arc42.md`, `docs/model/ODD.md`,
  `docs/model/world_substrate_model.toml`.
