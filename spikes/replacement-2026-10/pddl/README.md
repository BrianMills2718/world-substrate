# Replacement-first spike: PDDL toolchain (2026-10-05)

Question: can an off-the-shelf PDDL toolchain host or ground World Substrate's governed-rules
layer for the constrained-handoff world? Executed, zero LLM spend, ~40 s wall time.

## Command (from repo root)

```bash
PYTHONDONTWRITEBYTECODE=1 uv run --no-project --python 3.12 \
  --with unified-planning==1.3.0 --with up-enhsp==0.1.1 \
  --with up-pyperplan==1.1.0 --with up-fast-downward==0.5.2 \
  python spikes/replacement-2026-10/pddl/run_spike.py      # exit 0 = PASS; needs Java (ENHSP)
```

`run_spike.py` translates `constrained-handoff-v0.json` + `coordination-causal-v0.json` into a
unified-planning problem (no hand-written PDDL) and writes `domain.pddl` / `problem.pddl`.

## Observed output (2026-10-05, exit 0)

```text
== 1. translation: 4 actions, 30 fluents, 19 objects; wrote domain.pddl/problem.pddl; re-parsed OK
== 2. World Substrate reference: 6 accepted, refused attempt #3 bo:approve because ['Prerequisite A is healthy']
   validator verdict, reference plan (6 steps): VALID
   validator verdict, reference plan against re-read .pddl files: VALID
   validator verdict, refused-approval plan (3 steps): INVALID; inapplicable action: approve(bo, handoff_gate, ...)
   simulator's unsatisfied precondition(s): ['(1 <= resource_current(handoff_token))']
   failing PDDL precondition(s) mapped to WS check labels: ['Prerequisite A is healthy']
   MATCH: PDDL validator and World Substrate refuse on the same precondition
   planner pyperplan / fast-downward supports this problem kind: False   (numeric fluents)
   planner enhsp supports this problem kind: True
== 3. planner enhsp: status=SOLVED_SATISFICING plan length=6
   intervene(dev) -> communicate(dev->ana) -> approve(ana) -> communicate(dev->bo) -> approve(bo) -> finalize(bo)
   engine replay: 6/6 accepted; terminal reached=True; gate status=ready
== RESULT: PASS (0 failures)
```

The planner's plan differs from the scripted reference (intervenes first, finalize by `bo`) and
World Substrate's own `engine.discover`/`engine.submit` accepted every step.

## What PDDL tooling can replace or ground

- **Declaration language (ground, not replace):** checks/effects map mechanically onto PDDL2.1
  preconditions/effects with numeric fluents; the JSON language is a typed subset of PDDL actions.
- **Validation:** UP's `SequentialPlanValidator` reproduced World Substrate's accept/refuse verdicts
  on the reference trajectory, including the exact failing check.
- **Planning / affordance discovery:** ENHSP finds a goal-reaching plan from the authored world.
  Useful offline as an authoring check ("is the terminal reachable? which actions are dead?").

## What it could not express (printed by the script, section 4)

- information visibility / asymmetric knowledge: `communicate` is three boolean flips; one omniscient planner chooses every actor;
- write-scope enforcement, event log, `causal_parent_event_ids`, hashes, refused attempts as committed history;
- atomic commit against `base_revision`, multi-actor turn order;
- open worlds: fixed object set, closed string value domains, terminal selector grounded at translation time;
- unused fields (`information.content`, `member.role`, ...) carry no meaning in PDDL;
- `owner_ref`, `action_field`, `event_id` expressions have no translation (unused in this bundle).

## Friction

- pyperplan and Fast Downward reject numeric fluents; only ENHSP (Java 21 jar) worked.
- Untyped (single `entity` type) translation made ENHSP grind >2 min / >4 GB before being killed;
  one PDDL subtype per component fixed it, but entities with several components would break that scheme.
- String-to-string field equality was compiled to a precomputed static relation; that is only sound because
  no mechanic writes either field.
- UP's simulator reports constant-folded conditions (`1 <= resource_current(...)`), so mapping back to check
  labels needed a per-check re-evaluation.

## Verdict: **compose**

PDDL (unified-planning + ENHSP) is a sound export target for offline validation and reachability planning over
authored mechanics, but it cannot host the governed-rules runtime (no visibility, write scopes, causal event
record, or refusals as history), so the native engine stays the runtime.

Wrong-when: the translator needs hand edits for the second shipped coordination world, or the PDDL validator
and `engine.submit` disagree on any accepted/refused step of a recorded run; either would mean PDDL is not a
faithful grounding of the declaration language.
