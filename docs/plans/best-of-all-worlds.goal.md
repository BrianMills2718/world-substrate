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

## Current state (2026-10-16)

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
