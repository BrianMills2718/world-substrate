# Goal: Best of all worlds — one box, rich people, exact rules, live

Brian, 2026-10-16: "give me the /goal for the best of all worlds final version". This file is the goal loop's single
authority: mission, boundaries, checks, increments, current state. Designs and evidence stay at their native locations.

**Execution profile:** continuous-light

One writer; every change is reversible; deploys go to Brian's own site, which needs no yes when nothing private becomes
public.

## Mission

The public World Builder (https://brianmills.dev/world-builder/) turns any typed description into a living simulation
that combines what each earlier version did best:

| From | Kept |
| --- | --- |
| World Builder (one-box, #152-#158) | one box and one button; build steps stream as they happen; worlds keep running; rules are exact, compiled and readable from "See how it works"; descriptions about things still work |
| Cybernetic Influence v3 (`/waltzman/`) | people with goals, beliefs, channels and private information; AI members who reason every turn; a coordination readout of what happened and why |
| October 8 pipeline (`spikes/any-scenario-2026-10/`) | ScenarioSpecV1 people, compiled communicate and meeting rules, Concordia residents with memory (Decision 006: host resident loops on Concordia, add no cognition of our own) |

and fixes what each lacked: rules that can move both ways (concerns can be resolved, support restored, a decision
reconsidered), nobody stuck with nothing to do, a short wait before anything plays, and a link that shows a finished
run instantly.

**Stage:** product V1 of the public demo. No estimate beyond the loop bounds below.

**Canonical example:** paste Rand Waltzman's scenario (`docs/plans/waltzman_scenario_run.md`, the quoted text) into the
live page as a visitor and press Create simulation →
1. the build steps stream, and the first round plays within 150 seconds of the press;
2. the people are the partnership, four countries, the regional health network and the technical, legal, logistics and
   community groups, each played by an AI member reading only its own goals, beliefs and information;
3. each group's concern is delivered to its named country through its own channel (communicate events);
4. over at least 40 rounds the world does not narrow to one or two repeated moves, and every person takes at least one
   allowed action in the first 20 rounds;
5. at least one concern is resolved and at least one member's support changes in each direction, and the activation
   decision ends authorized, deployed, postponed or blocked only by a rule's event, never by the referee's say-so;
6. a "What happened" readout names, for each of the paper's four mechanisms (local concerns through separate channels,
   slowed meetings, reopened settled issues, conditional support delaying deployment), the event ids that show it or
   the plain reason it is missing;
7. a share link opens that same finished run instantly, with no AI spend, for someone who never pressed anything.

**Forbidden substitutes:** the hand-authored `reference_worlds/waltzman` world or the fixed native-coordination template
presented as generated; a scenario spec, rule set or run edited by hand; scripted or "first available" moves presented as
AI choices; a local or laptop run presented as the live site; a mechanism marked present without an event id from the
recorded run; rerunning until a behavior appears and reporting only that run (report every run); a screenshot or replay
of an older version presented as current; Waltzman-specific code paths (the example must come out of the general
pipeline).

## Boundaries

- In scope: `world-substrate` (service, page, people pipeline, Concordia hosting, readout, share links) and its deploy
  through `scripts/deploy_world_builder.sh` (personal-vps `apps/world-builder`, brianmills.dev Worker).
- Out of scope: Cybernetic Influence v3 (read-only, donor only, Decision 005); Simudyne; outreach to Waltzman (the draft
  `cybernetic_influence_v3/docs/WALTZMAN_OUTREACH_DRAFT.md` needs Brian's exact-text approval and is not part of done).
- Merge: pull requests after `scripts/check_project.py` exits 0 on the committed change; then deploy and confirm the live
  page and backend report the merged commit.
- Public data: run the `publish-checker` subagent before the first deploy of share links (they publish generated runs);
  descriptions typed by visitors are stored only when they press Share.
- Spend: the visitor allowance stays $3/day; test runs use the owner allowance; builds stay within PEOPLE_WORLD_BUDGET or
  a new per-build cap stated in the PR. No new spend route without Brian's yes.
- Never restart WSL; no destructive server operations beyond the deploy script's own image pruning.

## Acceptance checks

| ID | Criterion | Evidence to report |
| --- | --- | --- |
| C1 | Canonical example items 1-5 on the live site | browser run log with timings and per-round moves; build job progress; llm_client trace ids; Engine event ids for the communicate, resolve and support-change events; the live commit |
| C2 | Item 6, the readout | the readout text from the live page beside the event ids it cites, each checked against the run's trace |
| C3 | Item 7, the share link | the link opened in a fresh browser with no owner password, matching the run's rounds; the server log showing no AI call for it |
| C4 | A things description still works | "a pencil logistics and supply network" on the live site: builds as things, runs at least 20 rounds without narrowing to one move |
| C5 | Failures say so plainly | a forced budget stop and a forced rules rejection each show a plain message on the page, never "internal world-builder error" |
| C6 | Every run is accounted for | a list of every live and local run made under this goal with its trace id and outcome |

Every LLM behavior claim is judged from the full trace of the run it names (each tool and model call, its arguments and
result, the Engine events), not from counts or the final screen. For each failure, say whether the needed evidence never
came back, came back unused, or the expectation was wrong.

## Increments

1. **Rules that move both ways, nobody idle.** The rule writer gets resolve/restore/reconsider and idle-actor guidance;
   the test run's idle and circling checks trigger the one rules rewrite. Proven on Waltzman live (C1 items 4-5).
2. **Concordia residents play the people.** Host the October 8 resident loop (`run_scenario.py`) behind `/run` for people
   worlds, with per-person memory and the brief; the game master stays off unless bounded. Proven by trace: each move
   names the resident's belief and expected effect.
3. **Shorter wait.** Start playing as soon as the compiled communicate and meeting rules exist, or lower thinking effort,
   chosen by one side-by-side run of the same text recorded in this file (time and quality). Proven by C1 item 1.
4. **"What happened" readout.** The four mechanisms as detachable analysis over recorded events (Cybernetic v3's lens,
   ported, not imported). Proven by C2.
5. **Share link and a featured example.** A finished run saved and replayed without AI calls; the Waltzman run linked
   from "or try an example". Proven by C3.
6. **Regression and failure messages.** C4 and C5.

## Loop bounds

- Stop as blocked only after 3 attempts on the same reproduced blocker produce no new evidence or safe next action;
  report the blocker, its owner and the resume event.
- Revalidate after three increments or about four hours: report outcome, enabling and process progress, and whether to
  retain, replace or clear this goal. Three process-only increments in a row trigger revalidation, not a fourth.

## Non-gating next actions

- Brian's own look at the live page; Waltzman's reaction; any outreach.
- llm_client#283 (default 60 s cutoff on long calls) is the shared library's to fix; the VPS image already sets
  `LLM_CLIENT_TIMEOUT_POLICY=ban` (#158).
- The shared AI lock: a build blocks other visitors' AI rounds while it runs; fix only if it blocks C1.

## Current state (2026-10-20)

- Live: world-substrate `1a5498f`, llm_client `2d30c34`. Final set run on the owner allowance; every run, with trace ids,
  is in [evidence/best-of-all-worlds/RUNS.md](../../evidence/best-of-all-worlds/RUNS.md) ("Final set at f365d6b and
  1a5498f"), files in [evidence/best-of-all-worlds/final-1a5498f/](../../evidence/best-of-all-worlds/final-1a5498f/).
- C1, C2, C3, C6 pass: Waltzman run c1r15, share `_-7-ZRvA84QU`: round 1 at 139 s, all ten people act in round 1,
  7-9 distinct moves in every 10-round window over 45 rounds, four concerns on four group channels, concerns resolved,
  support conditional and restored, decision authorized by rule event r8-e00010, readout 4/4 mechanisms with event ids
  (78/78 claimed changes match the trace), share replays 45 rounds with no AI call, no private concern leaks into
  another person's prompt.
- C5 passes: forced rules rejection (c4-run13) and forced visitor and owner budget stops each show a plain message.
- **C4 is not met.** Of the two pencil runs at 1a5498f, c4-run13 narrowed to two moves with five idle workers, and
  c4-run14 looked busy only because a process created every good from nothing each round. The earlier 20122ef pass
  (c4-run10) met C4 only by its letter: delivering and selling were never possible. Root causes and proposed fixes:
  [#187](https://github.com/BrianMills2718/world-substrate/issues/187). Brian approved stopping runs here and reporting
  every result (2026-10-20); the next step is fixing #187, then one new pencil set.
- Pencil set at `b582c79` (Brian's yes, 2026-10-20): c4-run15 (share `4p5LQlDRNbdf`) is a real supply chain and passes
  C4; c4-run16 (share `M6CqmOQP-qt5`) fails in substance because processes do the carrier's transport (#190). So C4 now
  passes on one of two builds. `b582c79` also changed the rules text the Waltzman build uses (`world_kind="ongoing"`), so
  C1-C3 and C6 evidence at `1a5498f` does not cover `b582c79`; one Waltzman run there awaits Brian's yes.
- #187 fix (#189, live at `b582c79`): an ongoing world whose best rules still leave a
  step impossible or a worker idle gets its structure redesigned once from the test run; a process that adds a good
  some action makes from other goods blocks the top score and is named in the rewrite guidance; the structure contract
  asks for one carry action per kind of goods. Replayed on the saved pencil runs, the new check flags exactly the runs
  whose goods were conjured (c4-run10, c4-run14 and three earlier) and none of the Waltzman worlds or c4-run11.
- Fixes since 2026-10-19: #185 and #186 (hand-off actions name both ends, field examples are valid names), llm_client
  #291 (an empty OpenRouter account is reported as out of credit, not "busy").

## Previous state (2026-10-19)

- C1-C6 were reported as passing on the live site at `20122ef`; C4 was later judged a pass by the letter only (see
  current state) (live page and backend confirmed by the deploy script). Every run
  of the final increment, with trace ids, is in
  [evidence/best-of-all-worlds/RUNS.md](../../evidence/best-of-all-worlds/RUNS.md) ("Final increment live runs"); logs and
  analyses in [evidence/best-of-all-worlds/final-20122ef/](../../evidence/best-of-all-worlds/final-20122ef/).
- C1-C3: Waltzman run c1r13, share `iHoA-8UItGra`: round 1 at 112 s, all ten people act in round 1, 11-14 distinct moves
  in every 10-round window over 45 rounds, four concerns delivered on four separate channels, concerns resolved, support
  made conditional and restored, decision status changed 9 times by rule events only, readout 4/4 mechanisms with event
  ids (53/53 claimed changes match the trace), share replays 45/45 rounds with no AI call.
- C4: pencil run c4-run10, share `xNX6oCJNzwxK`: things world, 26 rounds, 5 distinct moves every window. Open gap (#179):
  delivering and selling pencils never become possible, so 3 of 8 actors stay idle.
- C5: forced rules rejection (c4-run10) and forced visitor and owner budget stops (test container on the live image) each
  show a plain message.
- Fixes this increment: #177 agenda meets while the decision is in effect, #178 readout shows whole values, #180 AI jobs
  run at once with one locked budget ledger (round 1 went from ~220 s to 112 s), #181 owner budget message, #182 up to
  four guided rules attempts for things worlds, #183 a dry run that selects no actor guides the next rewrite.

## Previous state (2026-10-17)

- C1-C6 checked on the live site, every run listed with trace ids in
  [evidence/best-of-all-worlds/RUNS.md](../../evidence/best-of-all-worlds/RUNS.md) (raw browser logs and share records
  in `~/code/.scratch/waltzman-demo/` c1-c5). C1 and C2 at `784e66d`, C3-C5 at `79f46fd`; live now `87d3986` (#164 plain
  rules-rejection message, #165 failed runs log their trace id; neither touches building or rounds).
- C1: build streamed, round 1 by ~122 s, 10/10 act in round 1, authorized only by the deadline rule (r8-e00024), all
  four mechanisms with event ids; share `OzydbZ8mNbdZ`. C2: 28/28 cited events match the trace. C3: share replays
  259/259 rounds with no password and no AI call. C4: pencil builds as things, 26 rounds, 7 distinct moves every
  round, but one move is never possible (#166). C5: plain messages for a rules rejection and two budget stops.
- Increment 2 done (2026-10-17, live at `abf9b05`): people in people worlds are Concordia residents
  (`scripts/concordia_residents.py`, ported from the October 8 loop; #168, #169 gate, #170). Each is a Concordia
  `EntityAgentWithLogging` with its own memory carried between one-round requests and an acting step that names its
  belief, an offered action and the expected effect; the game master stays off. Live Waltzman visitor runs
  `bhE4uvdDzg78` (32b2d34) and `umwwKYrbOVGR` (abf9b05): every run's mover is `llm-resident (Concordia)`; at abf9b05
  98/98 attempted moves name belief and expected effect; C2 49/49 and 46/46; C3 replays with no AI call.
- Judged: in `umwwKYrbOVGR` activity falls after deployment completes in round 29 (2-3 real moves per 10 rounds);
  the residents' beliefs say why (deployed, concerns resolved). That is the world reaching its end, not repetition
  of one move; `bhE4uvdDzg78` kept 6-8 distinct moves per 10 rounds through round 45.
- Open: #166 (moves that never become possible).

## Previous state (2026-10-16)

- Route change (Brian, 2026-10-16): the build moves into an agent harness (Codex on OpenRouter gpt-6-luna) that
  drafts, runs the compiler and dry run, and makes small edits until they pass; see
  [Decision 008](../decisions/008-build-worlds-in-an-agent-harness.md). Bare one-shot calls plus hand-written retries
  were the source of the repeated build failures (inc15f–inc15l).
- Laptop llm_client monthly cap for world-substrate raised to $40 (Brian approved 2026-10-16); local real runs are
  available again.
- Live at `031dce5`: people descriptions build people worlds (#157), no 60 s cutoff and empty memories allowed (#158).
- Waltzman on the live site: build 331 s; 30 AI rounds with no single-move loop; late rounds narrow to "hold meeting" and
  "request decision delay"; in the quick test 5 of 10 members stopped being able to act
  (`~/code/.scratch/waltzman-demo/` `one-box/wzlive2.log`). Increment 1 is next.

## /goal launcher

```text
Goal: The live World Builder turns any typed description into a living simulation that has the best of every version: one box and one button, streamed build steps, exact readable rules, people with goals, beliefs and private information played by Concordia AI members, rules that move both ways, a short wait, a "What happened" readout and an instant share link. Read and follow docs/plans/best-of-all-worlds.goal.md.
Profile: continuous-light.
Canonical example: pasting Rand Waltzman's scenario into https://brianmills.dev/world-builder/ as a visitor and pressing Create simulation streams the build and plays the first round within 150 s; the ten people (partnership, four countries, health network, technical, legal, logistics and community groups) each act from their own brief; each group's concern reaches its named country through its own channel; over 40+ rounds the world never narrows to one or two repeated moves and everyone acts in the first 20; a concern is resolved and support changes both ways; the decision ends only by a rule's event; a readout names event ids for each of the paper's four mechanisms or the reason one is missing; a share link replays that run instantly with no AI spend.
Forbidden substitutes: the hand-authored Waltzman world or native-coordination template presented as generated; hand-edited specs, rules or runs; scripted moves presented as AI; laptop runs presented as live; mechanisms marked present without event ids; rerunning until a behavior appears and reporting only that run; older screenshots; Waltzman-specific code paths.
Boundaries: world-substrate and its own deploy only; Cybernetic Influence v3 read-only; merge after scripts/check_project.py exits 0 on the committed change, then deploy and confirm the live commit; publish-checker before share links first go live; visitor allowance stays $3/day, tests use the owner allowance, no new spend route without Brian's yes; no outreach to Waltzman; never restart WSL.
Done when: checks C1-C6 in docs/plans/best-of-all-worlds.goal.md pass on the live site at a named commit, each reported with its browser run log, llm_client trace ids, Engine event ids and the list of every run made. Judge each criterion from the full trace of the run it names (session, tool and LLM calls, commits, check output, messages), not from a reported status or final output alone.
Stop as blocked only after 3 attempts on the same reproduced blocker produce no new evidence or safe next action; report the blocker, owner, and resume event; a stop at a boundary above (new spend, outreach, a destructive server change) is a correct terminal when reported with the request made. Do not gate on: Brian's review of the page; Waltzman's reaction or any outreach; llm_client#283; Simudyne.
Revalidate after three increments or about four hours; report outcome/enabling/process progress and whether to retain, replace, or clear this goal. If it is misaligned, stop substantive execution and return control; do not label strategic misalignment a technical blocker.
```
