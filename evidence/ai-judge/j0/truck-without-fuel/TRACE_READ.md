# Trace read: truck without fuel (J0, acceptance A1 blocked step)

Run: World Builder `/run`, scripted policy, 1 round, `tests/knock_on_worlds.py` `truck_without_fuel(40)` on the J0
branch: a 40-step loading line, then "a loaded truck leaves if it has fuel"; the truck has fuel 0. Saved by
`agent:j0-evidence`. Run log line read whole.

Trace id: `world-builder-live/run/87174bcf171d418db528453aadfd0eae`. Scripted, no model call: no llm_client
call under this id; cost 0.0 (measured, run log `cost_usd`).

## Findings

- All 40 loading steps ran in the moment of Sam's pull (`r1-e00002` … `r1-e00041`, waves 1 to 40, each caused by
  the step before).
- The blocked step is recorded with its blocker: `blocked_reactions` =
  `[{rule_id: truck-leaves, it: truck, after: r1-e00041, after_rule: loading-step-done, failed: [{check: "the truck
  has fuel", actual: 0}]}]`. The truck stayed in the yard; nothing followed from it.
- `knock_on`: `{steps: 40, with_cause: 40, blocked: 1}`; `reaction_limit: null`.
- Page wording (run-page.png): "blocked: truck leaves (truck) did not happen: “the truck has fuel” was not true
  (it was 0). Nothing followed from it. After r1-e00041", item 41, in orange with a dashed border after step 40.
  Acceptance A1 words it "blocked: the truck has no fuel"; the page states the failed check and its value instead,
  which is the same fact read straight from the rule.
- Side observation, not J0: the several-round task tracker (#128) opened a task for Sam's pull at `r1-e00001`
  (lever, `components.link.fallen`) and shows it "Under way since round 1" though the pull finished at once. The
  tracker treats `link.fallen = true` as a task because one rule ends it (loading-step-done) and another acts while
  it holds (truck-leaves reads the last step). Pre-existing heuristic; it only shows on this synthetic world.

## Round 1

Sam (`sam`) pulled the lever (`r1-e00001`, `pull-lever`, accepted); the task tracker opened a task at `r1-e00001` that was
still under way when the one-round run ended (no ending event). The loading line ran in the same moment:
`step-1` (`r1-e00002`, wave 1) … `step-40` (`r1-e00041`, wave 40). After `r1-e00041` the rule `truck-leaves`
had its first check true (the last loading step is done) but "the truck has fuel" false (fuel 0), so it was
recorded as blocked and did not fire. 41 engine events, no refusal.
