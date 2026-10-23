# Trace read: c1r21

Live owner-allowance run of the canonical Waltzman example at live build_commit c403c79 (#128 slice 2, PR #222),
2026-10-23, browser start 20:05:44Z. Driven through the real page by Playwright (c1rlive.mjs), so the page carried
each round's open tasks (`underway`) back to the server. Share link `y19zgLJkTqiw` (45 rounds; the page sent a 46th
/run after the share was made, as in runs 19 and 20). 48 server rows (1 /generate-world, 46 /run, 1 /readout), all
who=owner, $0.2413 on the run log; 519 AI calls under the 49 trace ids, 0 errors, $0.2661 in llm_client (510
resident, 3 mechanic-authoring, 2 scenario-spec, 2 action-signatures, 1 world-kind, 1 readout).
How it was read: every round's ten people (belief, expects, said, move wanted, move done, result, event id) and every
world event, dumped round by round (c1r18read/dump.py, 2151 lines), all 46 rounds read in full; every task's start
and ending taken from the rows' `underway` lists. The ten round-1 AI calls (llm_client ids 16328-16337, pulled
read-only from the VPS database) were opened for the private-information check.

## Findings

**Verdict: PASS on C1 items 1-7 at c403c79, and E1-E4 hold in the live run.** Five tasks failed part-way and the
people whose tasks failed noticed it from what they saw.

1. Build streams and round 1 plays within 150 s: press 2.4 s after start (20:05:46.4Z), last round-1 AI call
   20:07:44.6Z, round-1 row 20:07:45Z: about 118 s. Build steps shown as they finished: 5.7, 32.5, 46.7, 85 s. Pass.
2. Ten people, each a Concordia AI member reading only its own brief: round 1 has ten
   `world-builder-concordia-resident` calls, one per person. Each group's private text appears only in its own call:
   16328 community, 16330 legal, 16332 technical, 16334 logistics; Countries Cedar 16329, Dune 16331, Birch 16333,
   the network 16335, the partnership 16336 and Country Amber 16337 see none (leakcheck.txt). Pass.
3. Each group's concern delivered to its named member through its own channel, all in round 1: r1-e00001 community
   to Country Cedar, r1-e00011 legal to Country Birch, r1-e00013 logistics to the regional health network, r1-e00017
   technical to Country Amber. Pass.
4. No narrowing over 40+ rounds: all ten acted in the first 20 rounds (all ten in round 1). Distinct move kinds per
   10 rounds: 17 / 7 / 14 / 5 / 6 of 20 kinds. The quiet later rounds are people choosing to wait ("no new
   evidence"), not a shrinking offer. Pass.
5. Concern resolved, support both ways, decision only by rule events: first resolution r3-e00017. Support down:
   r1-e00022, r8-e00017, r22-e00005 (Birch's own move), r22-e00018. Up: r4-e00005, r4-e00009, r8-e00003, r8-e00005,
   r8-e00007 (Dune gives), r12-e00001, r24-e00003, r25-e00001. Decision status changed only by rules: authorized
   r8-e00018, deployment progresses r12-e00007 to r16-e00004, deployed r17-e00005, suspended r22-e00019, resumes
   r25-e00007. Pass.
6. Readout names event ids for each mechanism: 40 of 40 readout change claims match this trace (c1r/c2check.py on
   the share record, exit 0). Pass.
7. Share link replays with no AI spend: `y19zgLJkTqiw` opened as a fresh visitor replayed 45 rounds; the page made 2
   API calls (share, health) and 0 AI calls (c1r21-replay.json, replaycheck exit 0). Pass.

C4 and C5 are not properties of a Waltzman run and were not rerun (standing rule #215). C6: every row of this run is
in run-log.jsonl with its trace id.

### Build record (E1)

The /generate-world row's `dry_run.long_tasks`: resolve-concern and resolve-own-concern (started by a person) and
decision-authorized-at-deadline / at-last-deadline (started by the world) all `can_fail_part_way: true`. The rules
writer wrote no generated processes; the remedy stop is the compiled group-decision family's object-to-remedy.

### Every task's ending (E3, D5)

14 tasks started by people, 1 started by the world. 5 failed part-way, 10 finished.

| Started | Who | Ended |
| --- | --- | --- |
| r2-e00001 | community group (remedy on Cedar's concern) | finished r3-e00017 |
| r2-e00003 | Country Amber (own concern) | **failed** r3-e00013 (technical group objects) |
| r2-e00005 | Country Birch (own concern) | **failed** r3-e00007 (legal group objects) |
| r2-e00015 | regional health network (own concern) | finished r3-e00017 |
| r4-e00001 | Country Amber | **failed** r5-e00010 (technical objects) |
| r4-e00003 | Country Birch | **failed** r5-e00006 (legal objects) |
| r6-e00001, r6-e00003 | Countries Amber, Birch | finished r7-e00011 |
| r8-e00018 | the world (rollout, decision-authorized-at-deadline) | finished r17-e00005 (deployment-completes) |
| r9-e00001 | Country Birch | **failed** r9-e00005 (legal objects, same round) |
| r10-e00003 | Country Birch | finished r11-e00009 |
| r22-e00003, r22-e00007, r22-e00009 | Country Amber, legal group, logistics group | finished r23-e00015 |
| r23-e00001 | community group | finished r24-e00011 |

**Noticed from what they see.** Round 4, Country Amber: its concern "has reopened and is now open again; the
technical and legal groups have objected to remedies". Round 4, Country Birch: "my previous remedy attempt did not
persist, and the legal group has objected to the remedy". Round 6, Birch: "Previous attempts ... did not persist".
Round 7, Birch waits: "already tried starting the remedy, so I should give it time", and that remedy finishes
r7-e00011 because the legal group settled its own issue r7-e00003 instead of objecting. That is the canonical
example: a person starts a task expecting it to work, a later round shows it stopped by state that changed in
between (the holder's objection), and the person reads that from the concern's state.

The rollout was followed on the page and in `underway` from r8-e00018 to r17-e00005; the live page at round 10 shows
"Under way since round 8: Started by the world's own rule — decision authorized at deadline (r8-e00018)"
(c1r21-round10.png).

### E2 and E4 in the live run

- E2: final times_resolved community 2, legal 3, logistics 2, technical 2 (most 3, limit 4). Every finished remedy
  recorded `answered: true` and `remedy_by`. The operating review reopened every concern once (r21-e00006); later
  reviews were held without reopening (r30-e00016, r35-e00010, r40-e00013, r45-e00008). No fix-and-reopen loop.
- E4: no change set anything "activated" while the decision was not deployed (the copy was dropped at build time).

### Open problems (not fixed in this run)

- `answered` is a flag, not substance: the legal group keeps saying "the draft still lacks a retention period"
  after its concern is answered (r13 on), and at r31 names "the absence of a concrete way to correct the draft": no
  move changes the draft text.
- The opposite of the E4 problem: the system's readiness record stays `not_yet_activated` after the decision is
  deployed (r25 to the end), because nothing sets it once the copy is removed; people say "deployed but not
  activated", and the partnership says approval is "still false" (r21 on).
- The page named a stop by its rule id ("Ended by decision.action.object to remedy"); fixed after this run in the
  same PR as this evidence (it now names the person and the move).
- Misreads of visible state: Amber r3 believed its concern "now settled" right after it was stopped; legal r18 says
  the decision "has not been authorized" while it was deployed.
- When the first choice is refused, the retry keeps the first `said` (many "(retried)" rows), and several people
  wanting the single settle move in one round get `nothing_left` (r13, r35, r38).
- The rules-writing retry cannot run for this text (test run starts past the 80 s rewrite cut-off), so E1 is met by
  the compiled family, not by the writer.

## Build and readout traces

- `/generate-world` 2026-10-23T20:07:35Z $0.0622: `world-builder-live/kind/b970d62fc3ff4330b7ddf0c450665ca2`, `world-builder-live/people/3fcc046d453442af9cc28c5397e5fb81`
- `/readout` 2026-10-23T20:15:49Z $0.0032: `world-builder-live/readout/fc94056761324c6390e3237668ae6dcb`

## Round 1

Trace `world-builder-live/run/e1c758de85e04b269bd4959ed7bde683`, $0.0025.

Read: All ten act. Each group delivers its own concern to its named member through its own channel: community->Country Cedar r1-e00001, legal->Country Birch r1-e00011, logistics->regional health network r1-e00013, technical->Country Amber r1-e00017. The four countries, network and partnership put the decision on the agenda. Rule r1-e00022 makes the four holders' support conditional. No task starts.

- community-group: accepted r1-e00001 did=communicate
- country-amber: accepted r1-e00003 did=put-matter-on-agenda
- country-birch: accepted r1-e00005 did=put-matter-on-agenda
- country-cedar: accepted r1-e00007 did=put-matter-on-agenda
- country-dune: accepted r1-e00009 did=put-matter-on-agenda
- legal-group: accepted r1-e00011 did=communicate
- logistics-group: accepted r1-e00013 did=communicate
- regional-health-network: accepted r1-e00015 did=put-matter-on-agenda
- technical-group: accepted r1-e00017 did=communicate
- the-partnership: accepted r1-e00019 did=put-matter-on-agenda

World events: r1-e00001, r1-e00002, r1-e00003, r1-e00004, r1-e00005, r1-e00006, r1-e00007, r1-e00008, r1-e00009, r1-e00010, r1-e00011, r1-e00012, r1-e00013, r1-e00014, r1-e00015, r1-e00016, r1-e00017, r1-e00018, r1-e00019, r1-e00020, r1-e00021, r1-e00022

## Round 2

Trace `world-builder-live/run/de3c0484c70c4adf95621d46a0ea38d6`, $0.0038.

Read: Tasks start: community starts the remedy on Cedar's concern r2-e00001; Amber r2-e00003, Birch r2-e00005 and the network r2-e00015 start remedies for their own concerns (Birch expects 'remedy under way, two ticks'). Others review, plan and settle agenda items. Remedy countdown r2-e00023.

- community-group: accepted r2-e00001 did=resolve-concern
- country-amber: accepted r2-e00003 did=resolve-own-concern
- country-birch: accepted r2-e00005 did=resolve-own-concern
- country-cedar: accepted r2-e00007 did=consider-local-concern wanted=resolve-own-concern
- country-dune: accepted r2-e00009 did=settle-agenda-matter wanted=consider-local-concern
- legal-group: accepted r2-e00011 did=review-information-sharing-requirements
- logistics-group: accepted r2-e00013 did=plan-implementation-logistics
- regional-health-network: accepted r2-e00015 did=resolve-own-concern
- technical-group: accepted r2-e00017 did=complete-system-readiness-work
- the-partnership: accepted r2-e00019 did=settle-agenda-matter

World events: r2-e00001, r2-e00002, r2-e00003, r2-e00004, r2-e00005, r2-e00006, r2-e00007, r2-e00008, r2-e00009, r2-e00010, r2-e00011, r2-e00012, r2-e00013, r2-e00014, r2-e00015, r2-e00016, r2-e00017, r2-e00018, r2-e00019, r2-e00020, r2-e00021, r2-e00022, r2-e00023

## Round 3

Trace `world-builder-live/run/2bf273a0385f4b19a9d9395e839e365a`, $0.0027.

Read: First part-way endings: the legal group objects to Birch's remedy r3-e00007 and the technical group to Amber's r3-e00013, both stopped with the concern open again. The community and network remedies finish r3-e00017 (remedy-completes): first resolution. Amber believes its concern 'now settled' (a misread: it was just stopped).

- country-amber: accepted r3-e00001 did=settle-agenda-matter
- country-birch: accepted r3-e00003 did=settle-agenda-matter
- country-cedar: accepted r3-e00005 did=settle-agenda-matter
- legal-group: accepted r3-e00007 did=object-to-remedy
- logistics-group: accepted r3-e00009 did=settle-logistics-issue-through-planning
- regional-health-network: accepted r3-e00011 did=settle-agenda-matter
- technical-group: accepted r3-e00013 did=object-to-remedy

World events: r3-e00001, r3-e00002, r3-e00003, r3-e00004, r3-e00005, r3-e00006, r3-e00007, r3-e00008, r3-e00009, r3-e00010, r3-e00011, r3-e00012, r3-e00013, r3-e00014, r3-e00015, r3-e00016, r3-e00017

## Round 4

Trace `world-builder-live/run/054ee2fdfcea456599c51b8449c37bc9`, $0.0036.

Read: Noticed from what they see: Amber says its concern 'has reopened and is now open again; the technical and legal groups have objected to remedies'; Birch says 'my previous remedy attempt did not persist, and the legal group has objected to the remedy'. Both restart (r4-e00001, r4-e00003). Cedar r4-e00005 and the network r4-e00009 restore full support after their remedies finished.

- country-amber: accepted r4-e00001 did=resolve-own-concern
- country-birch: accepted r4-e00003 did=resolve-own-concern
- country-cedar: accepted r4-e00005 did=restore-full-support
- legal-group: accepted r4-e00007 did=put-matter-on-agenda wanted=resolve-concern
- regional-health-network: accepted r4-e00009 did=restore-full-support
- technical-group: accepted r4-e00011 did=review-technical-operation wanted=resolve-concern

World events: r4-e00001, r4-e00002, r4-e00003, r4-e00004, r4-e00005, r4-e00006, r4-e00007, r4-e00008, r4-e00009, r4-e00010, r4-e00011, r4-e00012, r4-e00013, r4-e00014, r4-e00015, r4-e00016

## Round 5

Trace `world-builder-live/run/ec2d383b6c754f85833d859cfa3beea6`, $0.0045.

Read: Second stops: legal objects again r5-e00006 (Birch's), technical r5-e00010 (Amber's); both tasks end failed. Others settle and put agenda items.

- country-amber: accepted r5-e00001 did=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-cedar: accepted r5-e00004 did=put-matter-on-agenda wanted=settle-agenda-matter
- legal-group: accepted r5-e00006 did=object-to-remedy
- regional-health-network: accepted r5-e00008 did=settle-agenda-matter
- technical-group: accepted r5-e00010 did=object-to-remedy
- the-partnership: accepted r5-e00012 did=put-matter-on-agenda wanted=settle-agenda-matter

World events: r5-e00001, r5-e00002, r5-e00003, r5-e00004, r5-e00005, r5-e00006, r5-e00007, r5-e00008, r5-e00009, r5-e00010, r5-e00011, r5-e00012, r5-e00013, r5-e00014, r5-e00015

## Round 6

Trace `world-builder-live/run/d38eb565d00d4669904cfa7195828db7`, $0.0042.

Read: Amber r6-e00001 and Birch r6-e00003 restart; Birch: 'Previous attempts ... did not persist, and the legal group has objected'. Technical settles its own issue r6-e00009 instead of objecting. Remedy countdown r6-e00015.

- country-amber: accepted r6-e00001 did=resolve-own-concern
- country-birch: accepted r6-e00003 did=resolve-own-concern
- country-cedar: accepted r6-e00005 did=settle-agenda-matter
- legal-group: accepted r6-e00007 did=put-matter-on-agenda wanted=resolve-concern
- technical-group: accepted r6-e00009 did=settle-technical-issue-through-review wanted=resolve-concern
- the-partnership: accepted r6-e00011 did=settle-agenda-matter

World events: r6-e00001, r6-e00002, r6-e00003, r6-e00004, r6-e00005, r6-e00006, r6-e00007, r6-e00008, r6-e00009, r6-e00010, r6-e00011, r6-e00012, r6-e00013, r6-e00014, r6-e00015

## Round 7

Trace `world-builder-live/run/345d8865758b4c64958d5db46f17a2b1`, $0.0032.

Read: Legal settles its own issue through review r7-e00003 instead of objecting; Birch waits ('already tried starting the remedy, so I should give it time'). Both remedies finish r7-e00011.

- country-dune: accepted r7-e00001 did=put-matter-on-agenda
- legal-group: accepted r7-e00003 did=settle-legal-issue-through-review
- logistics-group: accepted r7-e00005 did=put-matter-on-agenda
- technical-group: accepted r7-e00007 did=put-matter-on-agenda

World events: r7-e00001, r7-e00002, r7-e00003, r7-e00004, r7-e00005, r7-e00006, r7-e00007, r7-e00008, r7-e00009, r7-e00010, r7-e00011

## Round 8

Trace `world-builder-live/run/70ecca0c4de948b2b81abdaead1c6dbb`, $0.0033.

Read: Amber r8-e00003 and Birch r8-e00005 restore full support; Dune gives support r8-e00007. Legal raises a new concern r8-e00009 ('the draft still lacks a retention period'), which makes Birch conditional again r8-e00017. The deadline rule authorizes the decision r8-e00018: the rollout starts as a task the world started.

- community-group: accepted r8-e00001 did=settle-agenda-matter
- country-amber: accepted r8-e00003 did=restore-full-support
- country-birch: accepted r8-e00005 did=restore-full-support
- country-dune: accepted r8-e00007 did=give-support
- legal-group: accepted r8-e00009 did=raise-new-concern
- logistics-group: accepted r8-e00011 did=settle-agenda-matter
- technical-group: accepted r8-e00013 did=settle-agenda-matter

World events: r8-e00001, r8-e00002, r8-e00003, r8-e00004, r8-e00005, r8-e00006, r8-e00007, r8-e00008, r8-e00009, r8-e00010, r8-e00011, r8-e00012, r8-e00013, r8-e00014, r8-e00015, r8-e00016, r8-e00017, r8-e00018, r8-e00019

## Round 9

Trace `world-builder-live/run/17129613d14946fd8f1cba6c186bdab5`, $0.0039.

Read: Birch restarts its remedy r9-e00001; legal objects in the same round r9-e00005, so the task ends failed. Rollout under way.

- country-birch: accepted r9-e00001 did=resolve-own-concern
- country-dune: accepted r9-e00003 did=put-matter-on-agenda
- legal-group: accepted r9-e00005 did=object-to-remedy wanted=resolve-concern
- technical-group: accepted r9-e00007 did=put-matter-on-agenda

World events: r9-e00001, r9-e00002, r9-e00003, r9-e00004, r9-e00005, r9-e00006, r9-e00007, r9-e00008, r9-e00009, r9-e00010

## Round 10

Trace `world-builder-live/run/6b5e5f2d67e34181b2b31f2d6dfe3868`, $0.0046.

Read: Birch restarts r10-e00003 (finishes next round). Legal reviews requirements r10-e00008, logistics plans r10-e00010, technical reviews r10-e00013. Remedy countdown r10-e00018.

- country-amber: accepted r10-e00001 did=settle-agenda-matter
- country-birch: accepted r10-e00003 did=resolve-own-concern
- country-cedar: accepted r10-e00005 did=settle-agenda-matter
- country-dune: nothing_left  did=- wanted=settle-agenda-matter
- legal-group: accepted r10-e00008 did=review-information-sharing-requirements
- logistics-group: accepted r10-e00010 did=plan-implementation-logistics
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter
- technical-group: accepted r10-e00013 did=review-technical-operation wanted=settle-agenda-matter
- the-partnership: nothing_left  did=- wanted=settle-agenda-matter

World events: r10-e00001, r10-e00002, r10-e00003, r10-e00004, r10-e00005, r10-e00006, r10-e00007, r10-e00008, r10-e00009, r10-e00010, r10-e00011, r10-e00012, r10-e00013, r10-e00014, r10-e00015, r10-e00016, r10-e00017, r10-e00018

## Round 11

Trace `world-builder-live/run/f97937600e0a4ed290afe94bab158cf6`, $0.0032.

Read: Birch's remedy finishes r11-e00009. Legal, logistics and technical settle their own issues (r11-e00001/03/05).

- legal-group: accepted r11-e00001 did=settle-legal-issue-through-review
- logistics-group: accepted r11-e00003 did=settle-logistics-issue-through-planning
- technical-group: accepted r11-e00005 did=settle-technical-issue-through-review

World events: r11-e00001, r11-e00002, r11-e00003, r11-e00004, r11-e00005, r11-e00006, r11-e00007, r11-e00008, r11-e00009

## Round 12

Trace `world-builder-live/run/424dd48da90648b2ad0d21fe1e6e1b22`, $0.0032.

Read: Birch restores full support r12-e00001; legal puts a matter on the agenda r12-e00003. Deployment progresses r12-e00007 (rollout counting down).

- country-birch: accepted r12-e00001 did=restore-full-support
- legal-group: accepted r12-e00003 did=put-matter-on-agenda

World events: r12-e00001, r12-e00002, r12-e00003, r12-e00004, r12-e00005, r12-e00006, r12-e00007, r12-e00008

## Round 13

Trace `world-builder-live/run/94eea4ca9aae46809a5960bc3a9c3097`, $0.0060.

Read: Community settles the agenda item r13-e00001; legal reviews again r13-e00006, saying the draft still lacks a retention period although its concern is marked answered. Eight others wanted the one settle move or waited (nothing_left). Deployment progresses r13-e00014.

- community-group: accepted r13-e00001 did=settle-agenda-matter
- country-amber: nothing_left  did=- wanted=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-cedar: nothing_left  did=- wanted=settle-agenda-matter
- legal-group: accepted r13-e00006 did=review-information-sharing-requirements
- logistics-group: nothing_left  did=- wanted=settle-agenda-matter
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter
- technical-group: nothing_left  did=- wanted=settle-agenda-matter
- the-partnership: nothing_left  did=- wanted=settle-agenda-matter

World events: r13-e00001, r13-e00002, r13-e00003, r13-e00004, r13-e00005, r13-e00006, r13-e00007, r13-e00008, r13-e00009, r13-e00010, r13-e00011, r13-e00012, r13-e00013, r13-e00014

## Round 14

Trace `world-builder-live/run/aa6a6ef5b05b4f5a8176beea647bd301`, $0.0035.

Read: Legal puts a matter on the agenda r14-e00001; everyone else waits, saying their concerns are resolved and nothing new is visible. Deployment progresses r14-e00005.

- legal-group: accepted r14-e00001 did=put-matter-on-agenda

World events: r14-e00001, r14-e00002, r14-e00003, r14-e00004, r14-e00005

## Round 15

Trace `world-builder-live/run/885d4240d856405494971302d5ff6d64`, $0.0045.

Read: Amber settles the agenda item r15-e00001; legal settles its issue through review r15-e00004. Deployment progresses r15-e00010.

- country-amber: accepted r15-e00001 did=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- legal-group: accepted r15-e00004 did=settle-legal-issue-through-review
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter
- the-partnership: nothing_left  did=- wanted=settle-agenda-matter

World events: r15-e00001, r15-e00002, r15-e00003, r15-e00004, r15-e00005, r15-e00006, r15-e00007, r15-e00008, r15-e00009, r15-e00010

## Round 16

Trace `world-builder-live/run/7b6f74d68f144247a86f1e78800a5c00`, $0.0031.

Read: No accepted person move; everyone waits citing no new evidence. Deployment progresses r16-e00004 (last tick).


World events: r16-e00001, r16-e00002, r16-e00003, r16-e00004, r16-e00005

## Round 17

Trace `world-builder-live/run/9da606b65df946da9559eda4db9673e2`, $0.0034.

Read: Legal puts a matter on the agenda r17-e00001. Deployment completes r17-e00005: the world's rollout task ends (finished) and the decision reads deployed. Operating review nears r17-e00006.

- legal-group: accepted r17-e00001 did=put-matter-on-agenda

World events: r17-e00001, r17-e00002, r17-e00003, r17-e00004, r17-e00005, r17-e00006

## Round 18

Trace `world-builder-live/run/74fe960980d74ed88b8a4b04361c5d12`, $0.0055.

Read: Community settles the agenda r18-e00001; legal reviews r18-e00006 and believes the decision 'has not been authorized' (a misread: it is deployed). Review nears r18-e00012.

- community-group: accepted r18-e00001 did=settle-agenda-matter
- country-amber: nothing_left  did=- wanted=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-cedar: nothing_left  did=- wanted=settle-agenda-matter
- legal-group: accepted r18-e00006 did=review-information-sharing-requirements wanted=settle-agenda-matter
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter
- the-partnership: nothing_left  did=- wanted=settle-agenda-matter

World events: r18-e00001, r18-e00002, r18-e00003, r18-e00004, r18-e00005, r18-e00006, r18-e00007, r18-e00008, r18-e00009, r18-e00010, r18-e00011, r18-e00012

## Round 19

Trace `world-builder-live/run/f798f72732cd4e32b151b34fc1141742`, $0.0034.

Read: Legal settles through review r19-e00001; others wait. Review nears r19-e00005.

- legal-group: accepted r19-e00001 did=settle-legal-issue-through-review

World events: r19-e00001, r19-e00002, r19-e00003, r19-e00004, r19-e00005

## Round 20

Trace `world-builder-live/run/f03b39ffb927410599c73dab0ce7c3a7`, $0.0030.

Read: No accepted person move; all wait. Review nears r20-e00004.


World events: r20-e00001, r20-e00002, r20-e00003, r20-e00004, r20-e00005

## Round 21

Trace `world-builder-live/run/b85c52c419d1424b9c74803c62adc2cb`, $0.0033.

Read: Legal reviews r21-e00001. The operating review reopens every concern for reexamination r21-e00006 and is held r21-e00007 (each concern's one review). The partnership says approval is 'still false' while the decision is deployed.

- legal-group: accepted r21-e00001 did=review-information-sharing-requirements

World events: r21-e00001, r21-e00002, r21-e00003, r21-e00004, r21-e00005, r21-e00006, r21-e00007

## Round 22

Trace `world-builder-live/run/b5c0cef11e694f368b1cfc90fd362a7b`, $0.0038.

Read: People act on the reopened concerns: Amber restarts its remedy r22-e00003, legal r22-e00007 and logistics r22-e00009 start remedies on the legal and logistics concerns; community holds local engagement r22-e00001; Birch makes support conditional r22-e00005; Cedar becomes conditional by rule r22-e00018 and deployment is suspended r22-e00019.

- community-group: accepted r22-e00001 did=conduct-local-engagement
- country-amber: accepted r22-e00003 did=resolve-own-concern
- country-birch: accepted r22-e00005 did=make-support-conditional
- legal-group: accepted r22-e00007 did=resolve-concern
- logistics-group: accepted r22-e00009 did=resolve-concern
- regional-health-network: nothing_left  did=- wanted=resolve-own-concern
- technical-group: accepted r22-e00012 did=review-technical-operation
- the-partnership: accepted r22-e00014 did=put-matter-on-agenda

World events: r22-e00001, r22-e00002, r22-e00003, r22-e00004, r22-e00005, r22-e00006, r22-e00007, r22-e00008, r22-e00009, r22-e00010, r22-e00011, r22-e00012, r22-e00013, r22-e00014, r22-e00015, r22-e00016, r22-e00017, r22-e00018, r22-e00019, r22-e00020

## Round 23

Trace `world-builder-live/run/2f21d76882c94544ba0f81d771bf6347`, $0.0045.

Read: Community starts a remedy on its concern r23-e00001. The three remedies from round 22 finish r23-e00015 (Amber's, legal's, logistics').

- community-group: accepted r23-e00001 did=resolve-concern
- country-amber: accepted r23-e00003 did=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-cedar: nothing_left  did=- wanted=resolve-own-concern
- logistics-group: accepted r23-e00007 did=plan-implementation-logistics
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter
- technical-group: accepted r23-e00010 did=settle-technical-issue-through-review
- the-partnership: nothing_left  did=- wanted=settle-agenda-matter

World events: r23-e00001, r23-e00002, r23-e00003, r23-e00004, r23-e00005, r23-e00006, r23-e00007, r23-e00008, r23-e00009, r23-e00010, r23-e00011, r23-e00012, r23-e00013, r23-e00014, r23-e00015, r23-e00016

## Round 24

Trace `world-builder-live/run/077316963a82480a988ac6a2180c1081`, $0.0031.

Read: Birch restores full support r24-e00003; community, legal and logistics settle their own issues; the community remedy finishes r24-e00011.

- community-group: accepted r24-e00001 did=settle-community-issue-through-engagement
- country-birch: accepted r24-e00003 did=restore-full-support
- legal-group: accepted r24-e00005 did=settle-legal-issue-through-review
- logistics-group: accepted r24-e00007 did=settle-logistics-issue-through-planning

World events: r24-e00001, r24-e00002, r24-e00003, r24-e00004, r24-e00005, r24-e00006, r24-e00007, r24-e00008, r24-e00009, r24-e00010, r24-e00011, r24-e00012

## Round 25

Trace `world-builder-live/run/8e4a62321d8249ffa1f25b272438cc8d`, $0.0035.

Read: Cedar restores full support r25-e00001; legal puts a matter on the agenda r25-e00003; deployment resumes r25-e00007 and the decision is deployed again, to the end of the run.

- country-cedar: accepted r25-e00001 did=restore-full-support
- legal-group: accepted r25-e00003 did=put-matter-on-agenda

World events: r25-e00001, r25-e00002, r25-e00003, r25-e00004, r25-e00005, r25-e00006, r25-e00007, r25-e00008

## Round 26

Trace `world-builder-live/run/0e99d8cc115b487eadf893848b0b9f1f`, $0.0050.

Read: Birch r26-e00001 and the partnership r26-e00009 settle agenda items; legal reviews r26-e00004; the network adds an item r26-e00007.

- country-birch: accepted r26-e00001 did=settle-agenda-matter
- country-cedar: nothing_left  did=- wanted=settle-agenda-matter
- legal-group: accepted r26-e00004 did=review-information-sharing-requirements wanted=settle-agenda-matter
- logistics-group: nothing_left  did=- wanted=settle-agenda-matter
- regional-health-network: accepted r26-e00007 did=put-matter-on-agenda wanted=settle-agenda-matter
- the-partnership: accepted r26-e00009 did=settle-agenda-matter

World events: r26-e00001, r26-e00002, r26-e00003, r26-e00004, r26-e00005, r26-e00006, r26-e00007, r26-e00008, r26-e00009, r26-e00010, r26-e00011, r26-e00012, r26-e00013

## Round 27

Trace `world-builder-live/run/8be5f0241be947f0b2056ac440727568`, $0.0035.

Read: Legal settles through review r27-e00001; others wait citing resolved concerns.

- legal-group: accepted r27-e00001 did=settle-legal-issue-through-review

World events: r27-e00001, r27-e00002, r27-e00003, r27-e00004, r27-e00005

## Round 28

Trace `world-builder-live/run/36440e4186014ee0b02cd276269b55ad`, $0.0031.

Read: No accepted person move; all wait. People say the system is deployed but not activated (readiness never moves after the copy was removed).


World events: r28-e00001, r28-e00002, r28-e00003, r28-e00004, r28-e00005

## Round 29

Trace `world-builder-live/run/4946c8147c8d4f1da854804a0049285d`, $0.0035.

Read: Legal r29-e00001 and the network r29-e00003 put matters on the agenda.

- legal-group: accepted r29-e00001 did=put-matter-on-agenda
- regional-health-network: accepted r29-e00003 did=put-matter-on-agenda

World events: r29-e00001, r29-e00002, r29-e00003, r29-e00004, r29-e00005, r29-e00006, r29-e00007

## Round 30

Trace `world-builder-live/run/ea91a4169d07424687d50f5ec5e0d3db`, $0.0052.

Read: Community, Amber and the network settle agenda items (r30-e00001/03/11); logistics adds one r30-e00009. Review held r30-e00016 with no reexamination (each concern already reviewed once).

- community-group: accepted r30-e00001 did=settle-agenda-matter
- country-amber: accepted r30-e00003 did=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-cedar: nothing_left  did=- wanted=settle-agenda-matter
- country-dune: nothing_left  did=- wanted=settle-agenda-matter
- legal-group: nothing_left  did=- wanted=settle-agenda-matter
- logistics-group: accepted r30-e00009 did=put-matter-on-agenda
- regional-health-network: accepted r30-e00011 did=settle-agenda-matter
- the-partnership: nothing_left  did=- wanted=settle-agenda-matter

World events: r30-e00001, r30-e00002, r30-e00003, r30-e00004, r30-e00005, r30-e00006, r30-e00007, r30-e00008, r30-e00009, r30-e00010, r30-e00011, r30-e00012, r30-e00013, r30-e00014, r30-e00015, r30-e00016

## Round 31

Trace `world-builder-live/run/f9b5569314734484b06d5730c2495008`, $0.0034.

Read: No accepted person move. Legal speaks of 'the absence of a concrete way to correct the draft': no move changes the draft text.


World events: r31-e00001, r31-e00002, r31-e00003, r31-e00004

## Round 32

Trace `world-builder-live/run/c8e4e1545da44b928324ab8dd6561124`, $0.0035.

Read: Logistics plans implementation r32-e00001. The partnership: putting the decision on the agenda 'adds work without approving activation'.

- logistics-group: accepted r32-e00001 did=plan-implementation-logistics

World events: r32-e00001, r32-e00002, r32-e00003, r32-e00004, r32-e00005, r32-e00006

## Round 33

Trace `world-builder-live/run/b63b9b3550fe4548b8d059bfa84d840e`, $0.0035.

Read: Legal adds an item r33-e00001; logistics settles its issue r33-e00003.

- legal-group: accepted r33-e00001 did=put-matter-on-agenda
- logistics-group: accepted r33-e00003 did=settle-logistics-issue-through-planning

World events: r33-e00001, r33-e00002, r33-e00003, r33-e00004, r33-e00005, r33-e00006, r33-e00007

## Round 34

Trace `world-builder-live/run/8dc40f85520f4302995f7fa0e2a23f56`, $0.0052.

Read: Community r34-e00001 and legal r34-e00007 settle agenda items; Dune r34-e00005 and the partnership r34-e00010 add items.

- community-group: accepted r34-e00001 did=settle-agenda-matter
- country-amber: nothing_left  did=- wanted=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-dune: accepted r34-e00005 did=put-matter-on-agenda wanted=settle-agenda-matter
- legal-group: accepted r34-e00007 did=settle-agenda-matter
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter
- the-partnership: accepted r34-e00010 did=put-matter-on-agenda wanted=settle-agenda-matter

World events: r34-e00001, r34-e00002, r34-e00003, r34-e00004, r34-e00005, r34-e00006, r34-e00007, r34-e00008, r34-e00009, r34-e00010, r34-e00011, r34-e00012, r34-e00013, r34-e00014

## Round 35

Trace `world-builder-live/run/498cd4dd0f5b40ed916d2c13296208e3`, $0.0042.

Read: Amber settles the agenda r35-e00001; several others wanted the same one move (nothing_left). Review held r35-e00010.

- country-amber: accepted r35-e00001 did=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-dune: nothing_left  did=- wanted=settle-agenda-matter
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter
- the-partnership: nothing_left  did=- wanted=settle-agenda-matter

World events: r35-e00001, r35-e00002, r35-e00003, r35-e00004, r35-e00005, r35-e00006, r35-e00007, r35-e00008, r35-e00009, r35-e00010

## Round 36

Trace `world-builder-live/run/19a59b8658514cfeb357447e8ba3fc57`, $0.0028.

Read: The network adds an agenda item r36-e00001; others wait.

- regional-health-network: accepted r36-e00001 did=put-matter-on-agenda

World events: r36-e00001, r36-e00002, r36-e00003, r36-e00004, r36-e00005, r36-e00006

## Round 37

Trace `world-builder-live/run/c4e6def07df14800bd9100ea01ceafe2`, $0.0052.

Read: Community r37-e00001 and logistics r37-e00008 settle; Dune r37-e00006 and the network r37-e00010 add items.

- community-group: accepted r37-e00001 did=settle-agenda-matter
- country-amber: nothing_left  did=- wanted=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-cedar: nothing_left  did=- wanted=settle-agenda-matter
- country-dune: accepted r37-e00006 did=put-matter-on-agenda wanted=settle-agenda-matter
- logistics-group: accepted r37-e00008 did=settle-agenda-matter
- regional-health-network: accepted r37-e00010 did=put-matter-on-agenda wanted=settle-agenda-matter

World events: r37-e00001, r37-e00002, r37-e00003, r37-e00004, r37-e00005, r37-e00006, r37-e00007, r37-e00008, r37-e00009, r37-e00010, r37-e00011, r37-e00012, r37-e00013, r37-e00014

## Round 38

Trace `world-builder-live/run/5b9169d913374add9bf0978a6061d279`, $0.0045.

Read: Amber settles r38-e00001; others wanted the same settle (nothing_left).

- country-amber: accepted r38-e00001 did=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-cedar: nothing_left  did=- wanted=settle-agenda-matter
- country-dune: nothing_left  did=- wanted=settle-agenda-matter
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter

World events: r38-e00001, r38-e00002, r38-e00003, r38-e00004, r38-e00005, r38-e00006, r38-e00007, r38-e00008, r38-e00009

## Round 39

Trace `world-builder-live/run/677645d6e3f84a28bc5ee0fbe89153f9`, $0.0032.

Read: Legal r39-e00001 and technical r39-e00003 add agenda items.

- legal-group: accepted r39-e00001 did=put-matter-on-agenda
- technical-group: accepted r39-e00003 did=put-matter-on-agenda

World events: r39-e00001, r39-e00002, r39-e00003, r39-e00004, r39-e00005, r39-e00006, r39-e00007

## Round 40

Trace `world-builder-live/run/90440daa98294c80b10cb1cf2ac3b494`, $0.0042.

Read: Birch r40-e00001 and Cedar r40-e00003 settle; legal reviews r40-e00006. Review held r40-e00013.

- country-birch: accepted r40-e00001 did=settle-agenda-matter
- country-cedar: accepted r40-e00003 did=settle-agenda-matter
- country-dune: nothing_left  did=- wanted=settle-agenda-matter
- legal-group: accepted r40-e00006 did=review-information-sharing-requirements
- regional-health-network: nothing_left  did=- wanted=settle-agenda-matter
- technical-group: nothing_left  did=- wanted=settle-agenda-matter

World events: r40-e00001, r40-e00002, r40-e00003, r40-e00004, r40-e00005, r40-e00006, r40-e00007, r40-e00008, r40-e00009, r40-e00010, r40-e00011, r40-e00012, r40-e00013, r40-e00014

## Round 41

Trace `world-builder-live/run/9591503795d947bab88706d425e73b86`, $0.0035.

Read: Legal settles through review r41-e00001; the partnership adds an item r41-e00003.

- legal-group: accepted r41-e00001 did=settle-legal-issue-through-review
- the-partnership: accepted r41-e00003 did=put-matter-on-agenda

World events: r41-e00001, r41-e00002, r41-e00003, r41-e00004, r41-e00005, r41-e00006, r41-e00007

## Round 42

Trace `world-builder-live/run/7c81ab74db024f92a7323f42b6ed9ec8`, $0.0056.

Read: Community, logistics and the partnership settle (r42-e00001/09/13); legal r42-e00007 and the network r42-e00011 add items.

- community-group: accepted r42-e00001 did=settle-agenda-matter
- country-amber: nothing_left  did=- wanted=settle-agenda-matter
- country-birch: nothing_left  did=- wanted=settle-agenda-matter
- country-cedar: nothing_left  did=- wanted=settle-agenda-matter
- country-dune: nothing_left  did=- wanted=settle-agenda-matter
- legal-group: accepted r42-e00007 did=put-matter-on-agenda wanted=settle-agenda-matter
- logistics-group: accepted r42-e00009 did=settle-agenda-matter
- regional-health-network: accepted r42-e00011 did=put-matter-on-agenda wanted=settle-agenda-matter
- the-partnership: accepted r42-e00013 did=settle-agenda-matter

World events: r42-e00001, r42-e00002, r42-e00003, r42-e00004, r42-e00005, r42-e00006, r42-e00007, r42-e00008, r42-e00009, r42-e00010, r42-e00011, r42-e00012, r42-e00013, r42-e00014, r42-e00015, r42-e00016, r42-e00017

## Round 43

Trace `world-builder-live/run/ce55936fea8d45e8937cd3c855bd3a7a`, $0.0032.

Read: No accepted person move; all wait, citing no new evidence.


World events: r43-e00001, r43-e00002, r43-e00003, r43-e00004

## Round 44

Trace `world-builder-live/run/ca5b8f78365c446daf23e521ef8b9259`, $0.0032.

Read: Legal reviews r44-e00001; others wait.

- legal-group: accepted r44-e00001 did=review-information-sharing-requirements

World events: r44-e00001, r44-e00002, r44-e00003, r44-e00004, r44-e00005, r44-e00006

## Round 45

Trace `world-builder-live/run/5488f51378294276be2ba90d974ba9ec`, $0.0035.

Read: Community holds local engagement r45-e00001; legal settles through review r45-e00003. Review held r45-e00008.

- community-group: accepted r45-e00001 did=conduct-local-engagement
- legal-group: accepted r45-e00003 did=settle-legal-issue-through-review

World events: r45-e00001, r45-e00002, r45-e00003, r45-e00004, r45-e00005, r45-e00006, r45-e00007, r45-e00008

## Round 46

Trace `world-builder-live/run/bff6905d112d439a829d942010c82e16`, $0.0035.

Read: Community settles its issue through engagement r46-e00001; legal r46-e00003, the network r46-e00005 and the partnership r46-e00007 add agenda items. Decision still deployed; nobody resolves a concern a fifth time.

- community-group: accepted r46-e00001 did=settle-community-issue-through-engagement
- legal-group: accepted r46-e00003 did=put-matter-on-agenda
- regional-health-network: accepted r46-e00005 did=put-matter-on-agenda
- the-partnership: accepted r46-e00007 did=put-matter-on-agenda

World events: r46-e00001, r46-e00002, r46-e00003, r46-e00004, r46-e00005, r46-e00006, r46-e00007, r46-e00008, r46-e00009, r46-e00010, r46-e00011

