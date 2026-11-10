# Trace read: fifty chains of a hundred links (J0, acceptance A1)

Run: World Builder `/run`, scripted policy, 1 round, built from `tests/knock_on_worlds.py` `fifty_chains(50, 100)`
on the J0 branch (local service, port 8891). Saved by `agent:j0-evidence`. Run log line read whole with a script
and by eye where it matters (first, middle and last waves; every `reaction_steps` cause checked by program).

Trace id: `world-builder-live/run/1625a3332ece40a8bf9d8cb602e96a4d`. The scripted policy makes no model call, so
this id names the run's own record only: it holds no llm_client call, and the run cost is 0.0 (measured,
`cost_usd` in the run log line).

## Findings

- The whole knock-on finished in the moment Sam pulled the lever: 5,000 link falls in 100 reaction events
  (waves 1 to 100), each event with 50 steps, no refusal. Engine events: 101 (the pull plus 100 reactions).
- Every step has a cause: the program check found 0 of 5,000 steps whose `caused_by` is not the step before it in
  its own chain (`c7-42` is caused by `c7-41`'s step in the event before). The round's `knock_on` summary reads
  `{trigger: r1-e00001, trigger_rule: pull-lever, steps: 5000, with_cause: 5000, blocked: 0}`.
- `reaction_limit` in the run record is `null`: this run ran with no cap, and replay will use none.
- In the final snapshot all 5,000 links have `fallen: true`.
- The run page (run-page.png) shows "Knock-on effects of r1-e00001 (pull lever): 5000 steps run, 5000 with a cause,
  no refusal"; each step's "Caused by" link moves to the step it names.

## Round 1

Sam (`sam`) pulled the lever (`r1-e00001`, rule `pull-lever`, accepted; the scripted policy "chose the allowed move it had
done least recently"). In the same moment the first link of every chain fell (`r1-e00002`, wave 1, 50 steps
`c1-1` … `c50-1`, each caused by `e00001`), then each wave knocked the next link of all fifty chains: `r1-e00003`
(wave 2) … `r1-e00100` (wave 99) and `r1-e00101` (wave 100, links `c1-100` … `c50-100`, caused by `e00100`).
Nothing was blocked and nothing was refused. No one else acted; no world event outside the knock-on.
