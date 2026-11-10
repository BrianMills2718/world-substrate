## 1. Tests first

- [x] 1.1 `tests/test_run_stop.py`: round limit, spending limit from a faked recorded cost, whichever fires first,
  carried spending across one-round requests, a limit already reached plays no round, setting validation, old
  settings unchanged
- [x] 1.2 `tests/test_world_builder_service.py`: limits saved with a new world; `/run` carries `run_spent_usd` and
  stops on the spending limit using `_trace_cost`
- [x] 1.3 `tests/test_world_builder_home.py`: the two checkboxes, off by default, and the request fields

## 2. Build

- [x] 2.1 `scripts/run_stop.py`: `max_rounds`, `max_spend_usd`, `limit_check` and the run-page lines
- [x] 2.2 `scripts/run_authored_world.py`: check before the first round and after each round; `run_spent_usd`
- [x] 2.3 `scripts/world_builder_service.py`: `run_spent_usd` on `/run`, recorded cost from `_trace_cost`, run log
- [x] 2.4 `scripts/world_builder_home.html`: the controls, `activeStop`, `stopHere`

## 3. Record

- [x] 3.1 AI judge plan gains the plain-words stopping point; planning pages rebuilt; roadmap and wiki updated
