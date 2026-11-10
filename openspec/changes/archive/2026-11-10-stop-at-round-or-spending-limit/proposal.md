## Why

A World Builder world could stop by itself only once nothing was changing (PR #356, Q12). A visitor could not say
"play 40 rounds" or "spend at most $0.40 on this run": live play asks for one round at a time and only pauses every
100 rounds to check someone is still watching. Source: Brian, 2026-11-10: "i should be able to stop a world based on
budget or number of rounds or a natural langue stopping potin that the judge assesses once we build him".

## What Changes

- Two optional limits join the per-world "When to stop a run" setting (`run_stop`), each with a checkbox on the
  Create page, off by default: "Stop after N rounds" (`max_rounds`, 1 to 500) and "Stop when this run has spent $X"
  (`max_spend_usd`, $0.01 to $100). They combine with the quiet choice; the run stops at whichever fires first.
- A round limit records `stopped` with `reason: round_limit`. It is not `round_cap`, which only says one request
  played every round it asked for.
- A spending limit uses the cost llm_client recorded for this run's own calls (the number the daily budget ledger is
  settled with), carried across live play's one-round requests as `run_spent_usd`. It is checked before each round,
  so a round under way finishes and the run can go over by up to one round's spending; the run-page line says so.
  It records `reason: budget` with the amount spent.
- "Always run every round" is renamed "Don't stop for being quiet", since a limit can now still stop such a run.
- Pressing Play after a limit stops the run carries on without that limit for the rest of the run, as Play after a
  quiet stop already counts quiet rounds afresh.
- The third condition, a stopping point in plain words that the AI judge assesses, is a requirement in the AI judge
  plan (`docs/plans/ai_judge.md`) and is not built here.
- Worlds and runs saved without the new keys behave exactly as before.

## Impact

- Code: `scripts/run_stop.py`, `scripts/run_authored_world.py`, `scripts/world_builder_service.py`,
  `scripts/world_builder_home.html`.
- Tests: `tests/test_run_stop.py`, `tests/test_world_builder_service.py`, `tests/test_world_builder_home.py`.
- No engine, scheduler or cognition capability (Decision 006): stopping rules over recorded run state and recorded
  cost.
