# Replacement-first spike: PDDL toolchain (2026-10-05)

Can an off-the-shelf PDDL toolchain host or ground the governed-rules layer (constrained-handoff)? Executed, $0 LLM, ~40 s.

## Command (from repo root)

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.12 \
  --with unified-planning==1.3.0 --with up-enhsp==0.1.1 \
  --with up-pyperplan==1.1.0 --with up-fast-downward==0.5.2 \
  python spikes/replacement-2026-10/pddl/run_spike.py      # exit 0 = PASS; needs Java (ENHSP)
```

`run_spike.py` translates the bundle + causal model into a UP problem (no hand-written PDDL) and writes `domain.pddl`/`problem.pddl`.

## Observed output (2026-10-05, exit 0)

```text
== 1. translation: 4 actions, 30 fluents, 19 objects; wrote domain.pddl/problem.pddl; re-parsed OK
== 2. World Substrate reference: 6 accepted, refused attempt #3 bo:approve because ['Prerequisite A is healthy']
   validator verdict, reference plan (6 steps): VALID
   validator verdict, reference plan against re-read .pddl files: VALID
   validator verdict, refused-approval plan (3 steps): INVALID; inapplicable action: approve(bo, handoff_gate, ...)
   failing PDDL precondition(s) mapped to WS check labels: ['Prerequisite A is healthy']
   MATCH: PDDL validator and World Substrate refuse on the same precondition
   planner pyperplan / fast-downward supports: False (numeric fluents); enhsp: True
== 3. planner enhsp: status=SOLVED_SATISFICING plan length=6   # annotation: differs from scripted reference
   intervene(dev) -> communicate(dev->ana) -> approve(ana) -> communicate(dev->bo) -> approve(bo) -> finalize(bo)
   engine replay: 6/6 accepted; terminal reached=True; gate status=ready
== RESULT: PASS (0 failures)
```

## What PDDL tooling can replace or ground

- **Declaration language (ground, not replace):** checks/effects map mechanically onto PDDL2.1 numeric actions.
- **Validation:** `SequentialPlanValidator` reproduced the accept/refuse verdicts, including the failing check.
- **Planning / affordance discovery:** ENHSP finds a goal-reaching plan; useful offline as an authoring reachability check.

## What it could not express (printed by the script, section 4)

- visibility/asymmetric knowledge (`communicate` = three boolean flips; one omniscient planner picks every actor);
- write scopes, event log, `causal_parent_event_ids`, refusals as history, atomic commit on `base_revision`, turn order;
- open worlds: fixed object set, closed string value domains, terminal selector grounded at translation time;
- unused fields (`information.content`, ...) carry no meaning; `owner_ref`/`action_field`/`event_id` untranslated.

## Friction

- pyperplan and Fast Downward reject numeric fluents; only ENHSP (Java 21 jar) worked.
- Untyped translation made ENHSP grind >2 min / >4 GB (killed); one subtype per component fixed it, but breaks for multi-component entities.
- String-to-string equality became a precomputed static relation (sound only while no mechanic writes either field).
- The simulator reports constant-folded conditions, so mapping back to check labels needed per-check re-evaluation.

## Verdict: **compose**

PDDL (unified-planning + ENHSP) is a sound export target for offline validation and reachability planning over
authored mechanics, but it cannot host the governed-rules runtime (no visibility, write scopes, causal event
record, or refusals as history), so the native engine stays the runtime.

Wrong-when: the translator needs hand edits for the second shipped coordination world, or the PDDL validator and
`engine.submit` disagree on any accepted/refused step of a recorded run (PDDL would then not be a faithful grounding).
