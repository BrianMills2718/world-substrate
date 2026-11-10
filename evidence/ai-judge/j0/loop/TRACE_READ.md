# Trace read: a loop of 40 (J0, acceptance A1 "a loop still ends")

Run: World Builder `/run`, scripted policy, 1 round, `tests/knock_on_worlds.py` `loop(40)` on the J0 branch: forty
dominoes in a ring, each knocked by the one before, `d1` knocked by `d40`. Saved by `agent:j0-evidence`. Run log
line read whole.

Trace id: `world-builder-live/run/92449584a9604b04b06cd2904e92cb2c`. Scripted, no model call: no llm_client
call under this id; cost 0.0 (measured, run log `cost_usd`).

## Findings

- The loop ended without any cap: 40 steps in 40 waves, each (process, domino) pair fired once. `d1`, pulled by
  Sam, was knocked once more by `d40` at the end (`r1-e00041`, wave 40) and nothing followed, because the
  pair (knocked-by-the-one-before, d2) had already fired this moment.
- `knock_on`: `{trigger: r1-e00001, trigger_rule: pull-lever, steps: 40, with_cause: 40, blocked: 0}`;
  `reaction_limit: null`.
- The once-per-pair rule is what ends loops now, as Decision 009 (amended in this PR) says.

## Round 1

Sam (`sam`) pulled `d1` (`r1-e00001`, `pull-lever`, accepted). Knock-on in the same moment: `d2` fell (`r1-e00002`, wave 1,
caused by `e00001`), `d3` (`r1-e00003`, wave 2) … `d40` (`r1-e00040`, wave 39), then `d1` again (`r1-e00041`,
wave 40, caused by `e00040`; its knocks count went from 0 to 1). The round ended with 41 engine events, no refusal,
nothing blocked.
