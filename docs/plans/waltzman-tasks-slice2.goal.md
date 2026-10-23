# Goal: tasks that can really fail part-way (#128, second slice)

Follows [waltzman-belief-and-traces.goal.md](waltzman-belief-and-traces.goal.md), which is done (D1–D5; the
first #128 slice is live at 6709fa9, evidence `evidence/waltzman-belief-and-traces/c1r20/`). Brian approved
this next slice on 2026-10-23 ("yes give me the /goal text to take us through to completion").
Profile: continuous-light.

## Roadmap

| # | Goal | Depends on | Why here | Status |
| --- | --- | --- | --- | --- |
| 1 | best-of-all-worlds.goal.md | – | the live World Builder | done |
| 2 | waltzman-belief-and-traces.goal.md | 1 | enforced trace reads; #128 design and first slice | done |
| 3 | this goal | 2 | run c1r20 showed the slice cannot yet produce a part-way ending in the canonical world | done |

## What run c1r20 showed (the problems this goal fixes)

1. **No task could fail part-way.** The rules writer ignored the guidance to add a remedy stop, so
   `scripts/attempts.py` `long_tasks` reported `can_fail_part_way: false` for every task; all 21 remedies
   finished on schedule.
2. **A fix never answers the question in the concern.** A remedy only flips `concern.status`; Country Two's
   legal concern ("the local review has not yet determined whether the existing rule covers sharing this
   alert field") was resolved 14 times and reopened each time.
3. **Tasks a rule starts are not followed.** The rollout is started by the deadline rule
   (`decision-authorized-at-deadline`), not by a person's move, so the slice never shows it; it was
   authorized three times and only progressed from round 44.
4. **State contradicts itself.** The deploy move sets the system "activated" while the decision is not
   deployed, so people say "the system is already activated" for 35 rounds.

## Canonical example

Paste Rand Waltzman's scenario into https://brianmills.dev/world-builder/ as a visitor and press Create
simulation. The built world can end a task part-way (its build record says so), the page follows the
rollout as well as people's fixes, and in a live run a person starts a task believing it will work and a
later round shows it stopped or finished because of state that changed in between, which that person
notices from what they see. No concern loops through fix-and-reopen with the same unanswered question.

## Done when

- **E1. Every built world whose tasks take several rounds can end at least one of them two ways.** The build
  refuses or repairs (through the existing rules-writing retry, not hand edits) a world where `long_tasks`
  finds no task with `can_fail_part_way: true`, with a plain message if it cannot. Tests on saved worlds
  (c1r18 fixture, the c1r20 world, truck, pencil) with no AI calls.
- **E2. A fix carries its substance.** A finished remedy changes what the concern says or what its holder
  can see (the question answered either way, or the remedy recorded as not answering it), so a person
  deciding to reopen sees a reason. Measured in the live run: no concern resolved more than 4 times.
- **E3. Rule-started tasks are followed.** A task a world process starts (the rollout) appears on the page
  and in `underway` like a person's task, from start to ending, with the ending event id. Tested on a free
  replay of a saved world.
- **E4. No self-contradicting state for the rollout.** "Activated" (or the generated world's equivalent)
  cannot be true while the decision is not deployed; checked at build time and tested on saved worlds.
- **E5. One live canonical run on the owner allowance**, at the merged and deployed commit, passes C1 items
  1–7 of best-of-all-worlds.goal.md, is saved as `evidence/waltzman-tasks-slice2/<run>/` with
  `run-log.jsonl` and a `TRACE_READ.md` that `scripts/check_trace_reads.py` passes, every round read, and
  its build record shows at least one task that can fail part-way. Report every task's ending. If no task
  actually ended part-way in that run, say so: that is a correct finish once E1–E4 hold; do not rerun to
  fish for one.

Judge each criterion from the full trace of the run it names (llm_client trace ids, Engine event ids, run
log, browser log), not from a reported status.

## Order

Free replays of saved worlds first (tests/AGENTS.md, #215), then one paid build per change only where the
rules writer itself changed, then the one canonical live run (E5). Revalidate after three increments or about
four hours.

## Boundaries

- world-substrate and its own deploy only; Cybernetic Influence v3 is read-only.
- Merge after `scripts/check_project.py` exits 0 on the committed change, then deploy and confirm the live
  commit through the health endpoint. Publish-checker before anything new goes public.
- AI spend: the owner allowance only; the visitor allowance stays $3/day; no new spend route without
  Brian's yes. Report every run.
- No outreach to Waltzman. Never restart WSL. Respect the storage guard; do not route around it.
- No Waltzman-specific code paths: every fix must work for any described world.

## Forbidden substitutes

Hand-edited specs, rules or runs; scripted moves presented as AI; laptop runs presented as live; counting
summaries presented as a read-through; runs without `run-log.jsonl` and a passing `TRACE_READ.md`; rerunning
until a behaviour appears and reporting only that run; a test fixture that hard-codes a stop the rules writer
did not produce.

## Stop rules

Stop as blocked only after 3 attempts on the same reproduced blocker produce no new evidence; report the
blocker and what would unblock it. A stop at a boundary (new spend route, outreach, storage-guard block) is
a correct finish when reported with the request made.

## Do not gate on

Brian's review; Waltzman; llm_client#283; Simudyne. The retry that keeps the first `said` after changing the
move, and people misreading visible state, are recorded problems, not part of this goal.

## Progress

- 2026-10-23: goal written.
- 2026-10-23: E1-E4 built on branch `feat/tasks-slice2`, tested on free replays only. The c1r20 build's own AI answers
  (`tests/fixtures/c1r20_waltzman_build.json`, ids 15817/15819/15821 from the VPS llm_client database) are rebuilt by
  `tests/replay_build.py` with today's rules and no AI calls. Why not the rules-writing retry: in c1r20 the test run
  started at 85 s, past the 80 s rewrite cut-off, so the retry never runs for this text; and the writer spent its
  processes on clocks and deadlines the compiler already supplies. So the group-decision family itself now lets a
  remedy end two ways (the concern's holder can stop someone else's remedy part-way), and the part-way check feeds the
  retry for any other world. E2: a finished remedy records `answered` and `remedy_by`; reopening, a new concern and an
  operating review each happen at most once per concern, so a concern is answered at most four times (free replay of
  45 rounds: 3 each). E3: the rollout is followed with `world` as its starter (free replay: started r22-e00472,
  finished r30-e00600). E4: the deploy move's copy of the decision into `activation_state` is removed at build time.
- 2026-10-23: E1-E4 merged and deployed (#222, c403c79, health build_commit c403c79). E5: one live owner-allowance run
  c1r21 (share `y19zgLJkTqiw`, 46 rounds, $0.2413 run log, 519 AI calls, 0 errors), read in full:
  `evidence/waltzman-tasks-slice2/c1r21/TRACE_READ.md` (check_trace_reads passes). C1 items 1-7 pass. Build record:
  both remedy moves and the rollout `can_fail_part_way: true`. 15 tasks: 5 failed part-way (the concern's holder
  objected to someone else's remedy: r3-e00007, r3-e00013, r5-e00006, r5-e00010, r9-e00005), 10 finished, including
  the world's rollout r8-e00018 to r17-e00005. Countries Amber and Birch noticed their stopped remedies in round 4 from
  the concern's state. Most times any concern was resolved: 3. Nothing read "activated" while not deployed. Page fix
  from the read: a stop now names the person and the move instead of the rule id. Called done here, but the goal
  check rejected it (next entry). Left for the next slice: `answered` is a flag (the legal group still says the draft lacks a retention period), and readiness stays
  `not_yet_activated` after the decision is deployed.
- 2026-10-23: the goal check rejected "done": E1 had no test of the rules retry repairing a world, and E2's `answered` was
  only a flag (the legal group kept saying the draft lacked a retention period). #224 (385402a, deployed): a finished
  task tells the other people its concern names what was done, in the remover's own words; the retry-repair test runs
  the service with a stand-in rules writer and no AI calls. Live run c1r22 (share `A_tY0YwYWiyJ`, 46 rounds, $0.2055
  run log, 522 AI calls, 0 errors), read in full: `evidence/waltzman-tasks-slice2/c1r22/TRACE_READ.md`. C1 items 1-7
  pass. 11 tasks: 2 failed part-way (r3-e00013, r19-e00008, the concern's holder objecting), 9 finished, including the
  rollout r8-e00004 to r14-e00004; Countries One (r4) and Two (r20) noticed their stopped remedies and restarted them.
  Most times any concern was resolved: 2. The legal group stopped re-asking after each fix ("Without evidence that the
  current remedy fails to clarify the alert recipient, waiting is more cautious", r21). The read found an E4 break:
  the generated deploy move set readiness to "deployed" at r10 while the decision rolled out until r14, and six people
  said "already deployed". Fixed on branch `evidence/c1r22` (a decision-gated move cannot write one of the decision's
  own statuses into another record; free rebuild of this run's build answers), with the task record now naming who
  stopped a task. E5 needs one live run at that commit.
- 2026-10-23: the c1r22 fixes merged and deployed (#227, 73501bb). Live run c1r23 (share `EIm1Rml2eOIZ`, 45 rounds,
  498 AI calls, 0 errors), read in full (`evidence/waltzman-tasks-slice2/c1r23/TRACE_READ.md`), found two faults, so it
  is not the E5 run. (1) The readout read this people world as goods, because the build's fingerprint hashed `1.0`
  where the page sends `1`; fixed in #228 (89f1801). (2) Country B reopened its own concern at r14 because the words
  kept for its own fix were bookkeeping ("mark the retention concern as under remedy for two ticks"); fixed in #229
  (713a2b5, deployed): residents give a separate `work` answer saying what the work decides, and the task keeps it.
- 2026-10-23: **E5 run c1r24** at deployed 713a2b5 (share `FQHXnP_TLKPi`, 45 rounds, $0.2371, 500 AI calls, 0 errors),
  read in full: `evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md` (check_trace_reads passes). C1 items 1-7 pass
  (run stage at 121.5 s, 0 leaks, readout lens coordination with 46 of 46 change claims matching, replay with 0 AI
  calls). Build record: all four long tasks `can_fail_part_way: true`. 14 tasks: 5 failed part-way (r3-e00008,
  r3-e00010, r5-e00006, r5-e00012, r19-e00010; the concern's holder objected), 9 finished, including the world's
  rollout r8-e00013 to r14-e00012. Countries One and Two noticed their stopped fixes at r4 from the concern reading
  open and restarted; Country One at r20 named the objection. Most times any concern was resolved: 2; no person
  reopened a concern (the only reopen was the operating review, r18-e00013). Nothing read activated before deploy.
  Limit: the notice is only as specific as the person's words (Country Two's were vague, and legal said at r10 that
  "earlier remedy details are not visible"). E1-E5 are met; goal done.
