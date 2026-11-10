## 1. Tests first

- [x] 1.1 `tests/test_run_stop.py`: quiet stop, carried count, every round, finish line, open decision, the recorded
  Waltzman run (stops at round 30 of 46), setting validation, no setting means no change
- [x] 1.2 `tests/test_world_builder_service.py`: the setting is saved with a new world (default 6) and carried
  across one-round `/run` requests
- [x] 1.3 `tests/test_world_builder_home.py`: the Create page control and its default

## 2. Build

- [x] 2.1 `scripts/run_stop.py`: setting, movable fields, state keys, decision status, the check and its sentence
- [x] 2.2 `scripts/run_authored_world.py`: check after each round; `summary.stopped`, `stop_history`
- [x] 2.3 `scripts/world_builder_service.py`: `run_stop` on `/generate-world` and `/run`, logs and shares
- [x] 2.4 `scripts/world_builder_home.html`: the Options control, the request fields and the run-page line

## 3. Record

- [x] 3.1 Q12 resolved in `tools/planning/questions_src.py`; pages rebuilt; roadmap and wiki updated
