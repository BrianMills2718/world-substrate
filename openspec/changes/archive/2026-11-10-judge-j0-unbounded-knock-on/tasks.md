## 1. Engine

- [x] 1.1 `Engine(reaction_limit=None)`; `LEGACY_REACTION_LIMIT = 32`; `recorded_reaction_limit(record)`
- [x] 1.2 `replay_commands(..., reaction_limit=32)` default; `replay()` passes the engine's own limit
- [x] 1.3 Reaction events carry `reaction_wave` and `reaction_steps` (`it`, `caused_by`, `via`)
- [x] 1.4 Blocked steps recorded (`CompiledProcessMechanic.near_misses`, `blocked_reactions`)

## 2. Runs and the run page

- [x] 2.1 Run record carries `reaction_limit`; rounds carry `knock_on`, steps and blocked steps
- [x] 2.2 Run page: moment summary line, step-to-cause links, blocked step in orange, old-limit refusal wording
- [x] 2.3 Share links mark refused world changes (new shares when made; older ones from the run log when opened)

## 3. Tests, evidence, docs

- [x] 3.1 `tests/test_knock_on_unbounded.py` (fifty chains, loop, blocked step, old-limit replay, share)
- [x] 3.2 Saved runs under `evidence/ai-judge/j0/` with `TRACE_READ.md`
- [x] 3.3 Decision 009 amended; arc42, ODD and the system model updated
