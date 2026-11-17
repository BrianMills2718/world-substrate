# Trace read: a what-if branch with one change (2026-11-17 UTC)

How it ran: the live page https://brianmills.dev/world-builder/ (live revision bd1827f), driven by a real browser as the owner, on the ten-group world `871f40df` from `../unified-world-ux-20261117-pause-at-round-4/`
(original run `28046eca`). The round slider was moved back to "Round 2 · step 4/10 · earlier round", the new control "Change one group for this branch" was set to Legal Group with the sentence
"Its data-sharing concern was settled last week, so it supports activation.", and What if was pressed. The branch is run `39d08bbb`; the page labelled it "What if from round 2: Legal Group is told “...”, playing live" beside
"Original run, kept as it was" (`desktop-branch-with-change.png`, `desktop-change-form.png`). `run-log.jsonl` is the server's own log for the five branch rounds (rounds 3 to 7). Measured cost from the rows: $0.0069 + $0.0139 + $0.0235 + $0.0127 + $0.0201 = $0.0771.
The saved actor state in every row shows the change in force for the Legal Group only: the sentence is added to that group's own brief (after the text "For this what-if branch:") and no other group's brief carries it. The raw per-call prompts in the trace store were not opened one by one;
the rows embed each round's transcript, rulings, engine events and saved state, which were read.

Traces named by the log: `world-builder-live/run/7415c8cdfc45458d9bac759647a64138`, `world-builder-live/run/0131bffa4b9f410e8d05090fb139c6a0`, `world-builder-live/run/a5696514e63b49629b5b09f387d1ace8`, `world-builder-live/run/7345f7110b1149f7b7bea6c0cb629919`, `world-builder-live/run/63fbb20a276049e687aa4c625eecea05`.

## Findings

1. **A branch with one change now works live.** Two defects in my first version were found by this live check and fixed before it passed: the first branch round was refused with "This world cannot carry on: actor context differs from the sealed state"
   (the request's briefs and the saved state's briefs differed), fixed in PR 446; then the second round was refused with the same message because later rounds took the world's original briefs, fixed in PR 447. Round 3 to 7 now all ran.
2. **The change reached the Legal Group, and only it.** The saved state of every branch round holds the added sentence in `legal-group` and in no other group.
3. **The change did not flip the Legal Group.** In rounds 3 to 7 it still wrote that it could not support activation without knowing the legal terms ("Without knowing the system's legal responsibilities or safeguards, I cannot responsibly support activating the shared system", r5-e00006; "With no legal safeguards or terms established in what I know, I should not support activation", r6-e00006),
   and its moves were refused each round (unsupported action in rounds 3 to 6, "the actor has not already recorded a stance" in round 7, r7-e00006). Its brief still says the terms are "Not specified", its memory holds its own earlier refusals, and the added line sits at the end of the brief. So the mechanism works, but one sentence did not change this group's behaviour; a stronger or earlier-placed change is untested.
4. **Not a rules change.** No rule, process or other group's brief was touched; the original run `28046eca` still reads "Run · round 5" in the library list.
5. **Leftovers from the failed attempts.** The two attempts that hit the bugs above left partial branches ("What if from round 2: Legal Group changed", rounds 2 and 3) in the library list; they are saved runs of this world and were not deleted.

## Round 3

Branch from round 2, trace `world-builder-live/run/7415c8cdfc45458d9bac759647a64138`: tried a move: community-group (unsupported action, r3-e00001); country-group-1 (precondition failed, r3-e00002); country-group-2 (precondition failed, r3-e00003); country-group-3 (accepted, r3-e00004); country-group-4 (precondition failed, r3-e00006); cross-border-partnership (precondition failed, r3-e00008); legal-group (unsupported action, r3-e00009); logistics-group (precondition failed, r3-e00011); regional-health-network (precondition failed, r3-e00013); technical-group (precondition failed, r3-e00015). Waited: none.

## Round 4

Branch from round 2, trace `world-builder-live/run/0131bffa4b9f410e8d05090fb139c6a0`: tried a move: community-group (accepted, r4-e00001); country-group-1 (accepted, r4-e00003); country-group-3 (precondition failed, r4-e00005); country-group-4 (precondition failed, r4-e00007); cross-border-partnership (precondition failed, r4-e00009); legal-group (unsupported action, r4-e00010); logistics-group (unsupported action, r4-e00011); regional-health-network (precondition failed, r4-e00013); technical-group (precondition failed, r4-e00015). Waited: country-group-2.

## Round 5

Branch from round 2, trace `world-builder-live/run/a5696514e63b49629b5b09f387d1ace8`: tried a move: community-group (unsupported action, r5-e00001); country-group-2 (precondition failed, r5-e00002); country-group-3 (precondition failed, r5-e00003); country-group-4 (precondition failed, r5-e00004); cross-border-partnership (precondition failed, r5-e00005); legal-group (unsupported action, r5-e00006); logistics-group (precondition failed, r5-e00007); regional-health-network (precondition failed, r5-e00008); technical-group (precondition failed, r5-e00009). Waited: country-group-1.

## Round 6

Branch from round 2, trace `world-builder-live/run/7345f7110b1149f7b7bea6c0cb629919`: tried a move: community-group (precondition failed, r6-e00001); country-group-2 (precondition failed, r6-e00002); country-group-3 (precondition failed, r6-e00003); country-group-4 (precondition failed, r6-e00004); cross-border-partnership (precondition failed, r6-e00005); legal-group (unsupported action, r6-e00006); logistics-group (precondition failed, r6-e00007); regional-health-network (precondition failed, r6-e00008); technical-group (precondition failed, r6-e00009). Waited: country-group-1.

## Round 7

Branch from round 2, trace `world-builder-live/run/63fbb20a276049e687aa4c625eecea05`: tried a move: country-group-1 (precondition failed, r7-e00001); country-group-2 (precondition failed, r7-e00002); country-group-3 (precondition failed, r7-e00003); country-group-4 (precondition failed, r7-e00004); cross-border-partnership (unsupported action, r7-e00005); legal-group (precondition failed, r7-e00006); regional-health-network (unsupported action, r7-e00007); technical-group (precondition failed, r7-e00008). Waited: community-group, logistics-group.

