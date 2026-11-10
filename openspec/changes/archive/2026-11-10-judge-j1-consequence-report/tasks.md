## 1. Pass 1

- [x] 1.1 `consequence_report.pass_one`: moves of the person acting and each person named, values of everything named
- [x] 1.2 Interpreter reading gains `names` (prompt 1.3); an unmatched reading keeps them, filtered to the world
- [x] 1.3 Each run records pass 1 on every unmatched attempt's round row (`consequence.pass_one`)

## 2. Pass 2

- [x] 2.1 `with_rule` and `rules_check`: the proposed rule joins copies of the bundle and rules, then `build_engine`
- [x] 2.2 `pass_two`: test run on a copy of the current world; net changes, blockers, chain length, stopping point,
  full chain
- [x] 2.3 `summary` drops the full chain for the judge

## 3. Tests, evidence, docs

- [x] 3.1 `tests/test_consequence_report.py` with the port world and coin rule (`tests/judge_worlds.py`)
- [x] 3.2 Saved runs under `evidence/ai-judge/j1/` with `TRACE_READ.md`
- [x] 3.3 ODD, METAMODEL, the system model and arc42 updated
