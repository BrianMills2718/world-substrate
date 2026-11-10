## Why

A World Builder run went on to whatever round count the visitor's play reached, even after its story was over. The
Waltzman run of 2026-10-23 (`evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md`) played 46 rounds for $0.2371; the
decision was deployed in round 14 and the last concern resolved in round 22, and after that people only put a matter
on the agenda and settled it again. Open question Q12 asked when a run should stop. Source: Brian, 2026-11-10: "on
d1. stop condition should be configurable."

## What Changes

- A per-world setting, "When to stop a run", on the Create page under Options, saved with the world like "Simulate
  as" (`run_stop` on `/generate-world`, returned with the world, kept in the build log and in shared runs):
  "Stop once nothing is changing, after N quiet rounds" (default for new worlds, N = 6, one operating-review period)
  or "Always run every round".
- The run loop (`scripts/run_authored_world.py`, rule in `scripts/run_stop.py`) checks the setting after each round
  and records why the run stopped in its summary: `stopped` with `reason` `quiet_rounds`, `round_cap` or
  `finish_line`, the round, and one plain sentence the run page shows.
- "Nothing is changing" is judged on the fields people's moves can change plus each group decision's status;
  fields only the world's own processes write (clocks) do not count. Without a group decision: N rounds in which no
  person's move changed anything. With one: every decision deployed or rejected, and the state back to what it
  was N rounds earlier.
- A world or run saved without the setting runs every round and records nothing new, so saved worlds, saved runs
  and replays are unchanged.

## Impact

- Code: `scripts/run_stop.py` (new), `scripts/run_authored_world.py`, `scripts/world_builder_service.py`,
  `scripts/world_builder_home.html`.
- Tests: `tests/test_run_stop.py`, `tests/test_world_builder_service.py`, `tests/test_world_builder_home.py`.
- No engine, scheduler or cognition capability (Decision 006): a stopping rule over recorded run state.
