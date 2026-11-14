# Trace read — resident run in the pump facility (2026-11-13)

Run: `policy=resident`, 6 rounds, model openrouter/openai/gpt-6-luna, world `examples/world_authoring/pump-facility-v0.json`
(three people, three rooms, four directed door halves). Budget: the World Builder default cap, $0.12 a run.
Spend measured in `~/projects/data/llm_observability.db`: 18 calls, $0.003268 for the run below (trace id
`world-builder-live-run-549b1b6d176a4566baa4d9344eeffba7`: 18 resident calls, one per person per round; I opened
`actor-inputs.json` and read the assembled prompt and output for every call of Bo, Mara and Ari, and the 22 engine events).

An earlier first run on the same world, before three fixes, is kept in `run1-before-fixes/` (trace id
`world-builder-live-run-0fb6e6f236e643078ceebc999115fd13`, $0.003375). Its trace showed the defects below; this read is of the second run.

## Findings

1. **The first run exposed three defects, all fixed, then re-run.** (a) The people were declared public without a place
   scope, so each person was told the others were "here" and believed "I am in the laboratory with Bo" while Bo was in the
   control room (run 1, Ari round 1). Fix: people are `scope: place`. (b) `open-door` was never offered to anyone
   (`never_offered: open-door`) because its form named the far side of the door (`partner`), which the actor cannot
   perceive, and the form builder drops forms naming an unperceived entity. Fix: a form may list `unobserved_refs`.
   (c) After a same-round stale revision, the retry for boundary worlds was sent without its controller and refused as
   `invalid_action: controller must be a nonempty string` (run 1: r1-e00003, r1-e00005, r6-e00013). Fix in `run_authored_world.py`.
   Run 1 also offered each person "Tell <themselves>"; fixed with `not_self`.
2. **Run 2 behaves as an inhabited place.** 14 accepted actions, no idle or stalled person, no refusal. Mara opens the
   laboratory door (r1-e00003), Bo opens his own door (r2-e00004), people walk through and return (r2-e00006, r2-e00008,
   r3-e00009 and on). Beliefs agree with the world: in round 5 Mara says "I cannot see either room's occupants from here",
   and her prompt lists only the two corridor-side door halves as in her place.
3. **Delivered messages are separate from perception.** Mara reports to Bo from the corridor (r4-e00016) while Bo is in
   the laboratory (Bo arrived r4-e00014); Bo's round 5 prompt shows the report in `report_log.entries`, and his belief says
   "Mara has also told me it is calibrated". Final state: Bo holds two reports (Mara, Ari), Ari one (Bo), Mara none.
4. **Memory and global knowledge stay available.** Bo's brief says the pump was last started two weeks ago and
   uncalibrated; he weighs that against the reports in rounds 5 and 6 ("I remember it had not been calibrated since its last start").
5. **No refusal of a closed door occurred in run 2**, because residents opened doors first. The door refusal is in run 1
   (r3-e00007 and r3-e00008, "the door must be open") and in the scripted catalog test.
6. **Rough edges, not fixed.** The recipient's raw report record (`delivery_status`, `lineage_status`, `source_revision`)
   is printed as JSON inside "Your represented state" as well as in the "Delivered to you" line, which is duplicate noise.
   Two people (Bo and Ari) repeat "The pump is calibrated." back and forth in round 5; the world has no other fixed message.
   Stale-revision retries happen after almost every same-round commit (8 of 22 events) and are resolved by the retry path.
7. **What this does not show:** one 6-round run of one model on one world; not a measure of how faithful the personalities are.

## Round 1

ari (Ari) tried calibrate-pump (r1-e00001), accepted. mara tried open-door on the laboratory door (r1-e00002 stale after Ari's
commit, then r1-e00003 accepted). bo waited: his door was closed and he had no new information.

## Round 2

bo tried open-door on the control room door (r2-e00004, accepted). mara walked into the laboratory (r2-e00005 stale,
r2-e00006 accepted). ari walked out to the corridor (r2-e00007 stale, r2-e00008 accepted).

## Round 3

mara returned to the corridor (r3-e00009). ari walked back into the laboratory (r3-e00010 stale, r3-e00011 accepted).
bo walked into the corridor (r3-e00012 stale, r3-e00013 accepted).

## Round 4

bo walked into the laboratory (r4-e00014). mara sent Bo the report from the corridor (r4-e00015 stale, r4-e00016
accepted). ari waited.

## Round 5

bo sent ari the report (r5-e00017). mara walked to the control room (r5-e00018 stale, r5-e00019 accepted). ari sent bo the report (r5-e00020 stale, r5-e00021 accepted).

## Round 6

mara walked back to the corridor (r6-e00022). Ari and bo waited, both believing the pump calibrated.
