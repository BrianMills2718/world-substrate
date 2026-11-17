# Trace read: ten-group early-warning world, built and run through the World Builder page (2026-11-17 UTC)

How it ran: the live page https://brianmills.dev/world-builder/ (live revision 6908732), driven by a real browser as the owner. The ten-group text from the goal
was typed in the describe box, "Let the AI ask you a few questions" was pressed, the three questions were answered in one typed reply (at least 6 of 10 must say yes;
8 weekly rounds to the deadline; activation means all ten groups share alerts and coordinate), the draft was read, and "Use this description and create" was pressed.
The build is world `6c347f95` and the run is `efd18749`; the round-3 What if branch is run `3cbde19f`. `run-log.jsonl` is the server's own log for those calls (11 rows,
from `/data/home/.local/state/world-builder/runs/runs_2026-11-17.jsonl` on the VPS). Measured cost from the rows: clarify 2 x $0.0002, build $0.1326, run rounds
$0.0053 + $0.0067 + $0.0056, branch rounds $0.0039 + $0.0030. Everything below was read from those rows (the actors' attempts, readings, refusals,
engine events and final world state), not from the page's summary line. The raw per-call prompts held in the trace store were not opened one by one; the rows
embed each call's transcript, the game master's rulings and the trace ids.

Traces named by the log: `world-builder-live/clarify/5c3a2f4e3c3c49738da27555ff0c3590` and `world-builder-live/clarify/71bcac786a8c4a1a803f4cb39d424e79` (the dialogue turns),
`world-builder-live/kind/d7fd50b127d742de987351ca92bc874e` and `world-builder-live/people/cdd3b130856c44368a74b1c2b4764172` (build),
`world-builder-live/run/677430468a0e4406b7ac9530d632ae3b` (round 1), `world-builder-live/run/167f23502c774fd4aca9a28f5700509d` (round 2),
`world-builder-live/run/1d31b14af5cb4c5a8a6aeae99f359e00` (round 3), `world-builder-live/run/50b40b99f81a4beb80e817ff1832d589` (branch round 3),
`world-builder-live/run/ed00d3ff38e24047ba7b8511cecddccc` (branch round 4).

## Findings

1. **The dialogue and the draft worked.** First turn asked three questions (what the groups are called, what counts as approval, how many rounds); the typed answer produced a draft
   naming Country A to D, the Regional Health Network, the Cross-Border Partnership and the Technical, Legal, Logistics and Community Groups (10), the weekly meeting, eight rounds
   to the deadline and the at-least-6-of-10 rule. Build `people/cdd3b130...` kept all 10 groups.
2. **Round 1 is a real vote.** Seven of ten groups had a give-support move accepted (r1-e00001 community, r1-e00003 country-a, r1-e00007 country-c, r1-e00009 country-d,
   r1-e00011 partnership, r1-e00013 legal, r1-e00019 technical). Country B, Logistics and the Regional Health Network tried to settle the decision directly and were refused
   "a matter is still open on the agenda" (r1-e00005, r1-e00015, r1-e00017). In round 2 country-b (r2-e00001) and regional-health-network (r2-e00008) were accepted; the final world
   state has full support recorded for 8 of the 10 groups and the decision still says `status: open`.
3. **The vote never closes, so the run dies by round 3.** No move in this world settles the decision once enough support exists; the settle move is refused while the matter is open.
   From round 3 every group either waits or re-tries a move that is refused ("the actor does not support it yet", although their support is recorded), and the run ends with
   `active_at_end: false`. So the run cannot reach round 4 and the page says "no active moves at this saved round". This is a defect in the rules the builder wrote for a group decision, not in the page.
4. **People cannot see the tally.** Their own beliefs read "I cannot see the other groups' votes or the tally" (r2-e00003 country-c, r3-e00002 country-b). The world shows each person only their own support.
5. **The builder's own dry run had already said so.** Its check for the first ten-group build recorded `active_at_end: false`, `circling: true` and all ten groups stalled, and the build was
   still offered as ready. The page does not tell the person that the world will stall.
6. **What if worked.** From round 2 of the original (paused, slider moved back, button read "What if... (from round 2)") a branch was created and played rounds 3 and 4 beside the original
   (the page showed "Original run, kept as it was" left and "What if from round 2: same start, a new draw" right). The branch round 3 accepted logistics-group (r3-e00004) where the original refused it,
   then stalled the same way at round 4. The lever is a new draw only; changing one group's brief is not built.
7. **Not reached:** pausing at round 4 of the original (the run ended at round 3).

## Round 1

Trace `world-builder-live/run/677430468a0e4406b7ac9530d632ae3b`. Tried: community-group (r1-e00001 accepted), country-a (r1-e00003 accepted), country-b (r1-e00005 refused, matter still open),
country-c (r1-e00007 accepted), country-d (r1-e00009 accepted), cross-border-partnership (r1-e00011 accepted), legal-group (r1-e00013 accepted), logistics-group (r1-e00015 refused, matter still open),
regional-health-network (r1-e00017 refused, matter still open), technical-group (r1-e00019 accepted). Process r1-e00020 moment-countdown ran. 7 accepted of 10; all ten spoke in their own words.

## Round 2

Trace `world-builder-live/run/167f23502c774fd4aca9a28f5700509d`. Tried a move: country-b (r2-e00001 accepted), country-c (r2-e00003 refused, "the actor does not support it yet"), legal-group (r2-e00005 refused, same reason),
logistics-group (r2-e00006 unsupported: "state aloud that Logistics Group supports", ruled by the game master as no installed rule), regional-health-network (r2-e00008 accepted). Waited: community-group, country-a, country-d,
cross-border-partnership, technical-group. Process r2-e00009 moment-countdown ran.

## Round 3

Original, trace `world-builder-live/run/1d31b14af5cb4c5a8a6aeae99f359e00`: country-a (r3-e00001 refused), country-b (r3-e00002 refused), logistics-group (r3-e00003 unsupported: "record Logistics Group's support"); the other seven waited
(community-group, country-c, country-d, cross-border-partnership, legal-group, regional-health-network, technical-group); r3-e00004 moment-countdown. Accepted 0, so the run ended with no active moves.
Branch from round 2, trace `world-builder-live/run/50b40b99f81a4beb80e817ff1832d589`: country-a (r3-e00001 refused), country-b (r3-e00002 refused), legal-group (r3-e00003 refused), logistics-group (r3-e00004 accepted),
technical-group (r3-e00006 refused); community-group, country-c, country-d, cross-border-partnership, regional-health-network waited; process r3-e00007.

## Round 4

Branch only, trace `world-builder-live/run/ed00d3ff38e24047ba7b8511cecddccc`: country-b (r4-e00001 refused, "the actor does not support it yet") and regional-health-network (r4-e00002 refused, same); the other eight waited
(community-group, country-a, country-c, country-d, cross-border-partnership, legal-group, logistics-group, technical-group). Accepted 0; the branch ended with no active moves, as the original did.
