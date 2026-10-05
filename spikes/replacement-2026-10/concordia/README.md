# Replacement-first spike: Concordia (gdm-concordia 2.4.0)

This tests whether Concordia can host World Substrate's governed-rules layer on the
constrained-handoff world (the replacement-first gate in `roadmap/README.md`). The run uses no
LLM: Concordia's `NoLanguageModel` is wrapped in a call counter, and the run asserts it stays at 0.

```
PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.12 --with gdm-concordia==2.4.0 \
  python spikes/replacement-2026-10/concordia/run_spike.py      # from the repo root
```

## Observed output (2026-10-05, exit 0)
```
reference run_native_coordination: events=7 material_sha256=a80b5bf8bbe366cd...e4848
v1: bo approve precondition_failed event=e00003 cause=c00003 failed=['Prerequisite A is healthy']
v1: events=7 material_sha256=a80b5bf8bbe366cd...e4848   (equal to the reference)
[PASS] v1 gate ready | [PASS] v2 refusal, gate ready, components = Engine's | [PASS] LLM calls=0
glue_loc {"concordia glue": 62, "shared": 16, "variant 1 glue": 15, "variant 2": 51}
RESULT checks=11 passed=11 failed=0 exit=0
```

## Variant 1: compose (executed)
- **Concordia took over:** the loop (`Sequential.run_loop`) and its entities
  (`EntityAgentWithLogging` driven by the stock `ScriptedActComponent`). It also took over the
  game master (`SwitchAct` with the stock `NextActingInFixedOrder` and `FixedActionSpec`), the
  flow from a proposed event to a resolved one, sending observations to each entity,
  termination polling and the run log.
- **World Substrate kept:** rule compilation, discovery and authority checks, the approval
  threshold, atomic commit or refusal, causal events with cause ids, the terminal predicate and
  material state. The game master's resolution component calls `Engine.discover`/`Engine.submit`
  and only narrates the Engine's verdict. Every Engine event lines up one-to-one with a
  resolution call.

## Variant 2: replace (executed, bounded)
The Engine was removed, and a game-master component interpreted `coordination-causal-v0.json`
itself: selectors, `eq`/`lt`/`gte` checks, `set`/`add` effects, a copy-then-swap commit and the
terminal predicate. It matched the refused approval, the gate reaching `ready`, and the final
entity components. **Concordia contributed nothing to the rules layer.** All 51 lines are our
code. Concordia has no typed rule, check, authority or atomic-commit primitive, and its stock
`EventResolution`/`WorldState` components are built on a `LanguageModel` and prompt it. The
copy still lacks the revision/staleness check, write-scope enforcement, `discover`'s lists of
available and blocked actions, read-path recording, before/after snapshots, compiler validation
and replay hooks: replacing the Engine means rewriting World Substrate inside Concordia.

## Friction
Custom components must implement abstract `get_state`/`set_state` even when stateless; every value is
a string (intents travel as `"<name> <json>"` and are parsed back); a missing component key makes
`SwitchAct` silently fall back to the model ("YOLO case") instead of failing; the install adds 34 packages.

## Verdict: **compose**
Concordia can own the resident and game-master loop with zero divergence (the material sha256
equals the reference), but it cannot hold the governed-rules layer, so the Engine remains the
only consequence authority. Its distinctive value, LLM-resident cognition (memory, prefabs), was
**not** exercised here. Adopt it for the loop only when LLM residents are needed. Scripted runs
keep `run_native_coordination`'s own loop.

**Wrong when:** the first LLM-resident run through this composition needs either of these:
(a) a game-master component that writes state outside `Engine.submit`, or narration in place of
an Engine verdict; or (b) more glue than putting the same residents behind the existing
`CognitionAdapter` (Decision 004). Either outcome turns the verdict into **keep**.
