# Replacement spike: Mesa (constrained-handoff)

Executed 2026-10-05, Mesa 3.5.1, Python 3.12.3, zero provider spend. Run from the repo root:

```
PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.12 --with mesa --with networkx \
  python spikes/replacement-2026-10/mesa/run_spike.py      # exit 0, "RESULT: PASS failures=0"
```

Files: `v1_compose.py` (Mesa model/agents over the Engine), `v2_native.py` (rules hand-written in Mesa), `run_spike.py` (checks).

## Observed
Variant 1 (compose: Mesa loop + DataCollector, World Substrate Engine as sole consequence authority):
- `refused approval ... actor=bo status=precondition_failed failed=['Prerequisite A is healthy'] cause=c00003 rule=coordination.action.approve event=e00003`
- `gate reaches ready -- mesa steps=7`; `final event count equals reference -- mesa=7 reference=7`
- `material_dict sha256 equals reference -- a80b5bf8bbe366cd98dc9d7154a95d21c9d1bfa4940e326fdc45f786552e4848` (both)
- event log equals the `run_native_coordination()` log except the controller label; `Engine.replay()` ok, 7 steps
- DataCollector table: gate `blocked` x6 then `ready`, approval_count 0,0,0,0,1,2,2, event_count 1..7

Variant 2 (replace: same rules as Mesa agent methods, no Engine): gate reaches `ready`, bad approval refused with `['Prerequisite A is healthy']`, final components equal the Engine run. Governed properties, each exercised by code:

| property | native Mesa | WS Engine |
|---|---|---|
| atomic commit/refusal (defect raises after first write) | LACKING: `approved=True` persisted, count 0 | world hash unchanged (exception propagates; no refusal event is recorded for a raising rule) |
| declared write scope (approve also zeroes link-health) | LACKING: write lands, link-health=0 | `scope_violation`, world unchanged |
| recorded cause | LACKING: state and DataCollector carry none | gate `last_cause_event_id=e00007`, rule finalize, cause c00007, bearer dev, 19 checks |
| rules-as-data, compiler-checkable | LACKING: rule is 11 lines of Python; a proposal would need `exec` | compiler rejects LLM-style bad effect: `effects[2] names unknown participant 'ghost'` |
| exact replay of a recorded run | LACKING: same-seed re-execution is identical, but there is no command log to replay/verify | `Engine.replay()` ok, event_match=True |

Glue LOC (non-blank, non-comment): compose 70, native port 109 (and the port only gets the five properties above by re-writing the Engine).

## What Mesa replaced (variant 1)
Agent objects and registry (`AgentSet`), activation (`model.agents.do("step")`), step clock (`model.steps`), seeded RNG (`rng=`), per-step tabular data collection (`DataCollector` -> pandas).

## What it could not
Anything in the governed-rules layer: discovery of available/blocked actions, validation, atomic commit or refusal, write-scope enforcement, causal events, replay, compiler-checked rules-as-data. Mesa has no transaction or provenance concept; its state is whatever agent code mutates.

## Friction
- `pip`/`uv --with mesa` alone fails at `import mesa` (`ModuleNotFoundError: networkx`); needs `--with networkx` (or `mesa[network]`). Pulls numpy/pandas/scipy.
- `Model.step()` does not activate agents; the subclass must call `self.agents.do("step")`. `seed=` is deprecated for `rng=` (FutureWarning).
- For a turn-scripted world Mesa's activation adds nothing beyond a loop: each agent fires on a step index we assign. Mesa's value (spaces, random activation, batch sweeps) is not exercised by this world.

## Verdict: compose
Mesa can own the outer loop and per-step data collection over the Engine with exact parity (same hash, events, replay) for 70 lines of glue; replacing the Engine with Mesa loses all five governed properties, so not adopt. Compose is optional, not a reason to delete World Substrate's loop: the existing fixture already drives the Engine with a plain Python loop.

Wrong when: a World Substrate world needs spatial grids/networks, stochastic activation, or parameter sweeps (Mesa `batch_run`) and the native loop would have to grow them, then compose becomes the default host; or if any Mesa release ships transactional state with write scopes and per-mutation provenance (re-run this spike's P1-P5 against it).
