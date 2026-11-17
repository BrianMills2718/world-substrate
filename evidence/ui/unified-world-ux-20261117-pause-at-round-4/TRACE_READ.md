# Trace read: ten-group world, paused at round 4, branched from round 2 (2026-11-17 UTC)

How it ran: the live page https://brianmills.dev/world-builder/ (live revision 34d7c3b), driven by a real browser as the owner, the same dialogue as the first walk
(`../unified-world-ux-20261117/`): the ten-group text typed in, three questions answered in one typed reply (at least 6 of 10 must say yes; 8 weekly rounds; activation
means all ten share alerts and coordinate), draft read, Create pressed. Build world `871f40df`, run `28046eca`. The script watched the map's round label and pressed Pause when the
map showed "Round 4 · step 8/8 · newest round" (the round then under way finished, so the original also holds round 5). It dragged the round slider back to "Round 2 · step 4/8 · earlier round",
pressed What if (from round 2), and the branch played rounds 3 to 8 beside the original ("Original run, kept as it was" left, "What if from round 2: same start, a new draw" right). The library list shows the world
"Shared Early-Warning System Activation · 2 runs" (the title the builder gave it). `run-log.jsonl` is the server's own log for these calls (14 rows). Measured cost from the rows: dialogue 2 x $0.0003, build $0.1433, original rounds
$0.0147 + $0.0310 + $0.0085 + $0.0085 + $0.0164 (rounds 1 to 5), branch rounds $0.0085 + $0.0053 + $0.0156 + $0.0060 + $0.0173 + $0.0163 (about $0.30 in all). The raw per-call prompts in the trace store were not opened one by one;
the rows embed each call's transcript, the game master's rulings, the engine events and the final world state, which were read.

Traces named by the log: `world-builder-live/clarify/ed4911e2b0d7435590de6690c9149b3f`, `world-builder-live/clarify/1def206337d5428b9e4fd31eb73c24c4`, `world-builder-live/people/66535a7dc71f425f8a932ff59af4fc22`, `world-builder-live/kind/a9e13091a7c44e62a682f243da8fddd2`, `world-builder-live/run/7328a0690bfe4587859128e10ce13526`, `world-builder-live/run/e8285ae0fcd0420aab38f05f71b96d39`, `world-builder-live/run/fbca551ef2344835b1d6924d0bf2adc4`, `world-builder-live/run/8abc732f5257462e92c2e38c64225973`, `world-builder-live/run/abad9f59797e4bbab7c6557282333afc`, `world-builder-live/run/72e74f509ee54923924d80d96a547e2c`, `world-builder-live/run/049f91f3cf104ff6983c3e92b9bc123b`, `world-builder-live/run/cc2603e128314210b872cd02ffc91ee8`, `world-builder-live/run/5b234d2ab50f47b5a8f72326dc9154fe`, `world-builder-live/run/c0668ef359194de6919c76aef5f478e2`, `world-builder-live/run/b882dbaf2a714fd1872f5708a44771c2`.

## Findings

1. **The canonical example now plays through.** The run reached round 4 live, was paused there, scrubbed back to round 2 and branched; both runs reopen from the library list.
   This follows the service fix that lets a run continue through quiet rounds until the world's own quiet-rounds setting is reached (PR 442); before it, three earlier attempts on this step ended at round 1 or 3.
2. **The vote moved the way the description says.** The decision `Activate the shared early-warning system?` (deadline `round-8-meeting`, 6 needed) showed support 2 after round 1, 6 after round 2, 8 after round 3 and 9 after round 4 and 5, so the threshold was met in round 2.
3. **The decision is never settled.** Even with 9 supports against 6 needed the decision status stays `open` through round 5 (original) and round 8 (branch). Moves that try to settle it are refused ("a matter is still open" or "the actor does not support it yet"). So the deadline round passes without a recorded outcome.
   This is the same rule defect as in the first walk; it is in the rules the builder writes, which this goal does not change.
4. **Most refusals come from people repeating moves.** After a group has given support, its repeat give-support is refused (precondition failed) round after round, and some free-text attempts ("state my position") match no rule and are ruled out by the game master. Rounds 5 onward have 0 or 1 accepted moves.
5. **The branch differs from the original** at the same round (e.g. round 3: original accepted two moves, branch accepted two different groups), so a new draw really does diverge; it does not change any group's brief (named gap).

6. **Reopened from the library.** In a fresh browser session with no run open, the world's card was clicked in the library, then the rail item "Run · round 5" (opened run `28046eca`, map label "Round 5 · step 10/10 · newest round", `desktop-reopened-original.png`) and the item "What if from round 2 · round 8" (opened run `3a23db4f`, URL `worldRun=3a23db4f...`, map label "Round 8 · step 16/16 · newest round", `desktop-reopened-branch.png`, which also shows "parent 28046e · after round 2"). Eight other saved worlds share near-identical titles in the list, so the person has to tell worlds apart by their runs; an earlier click landed on a different world with a similar title (known polish gap, not fixed).

## Round 1

original, trace `world-builder-live/run/7328a0690bfe4587859128e10ce13526`: tried a move: community-group (unsupported action, r1-e00001); country-group-2 (accepted, r1-e00002); country-group-3 (precondition failed, r1-e00004); country-group-4 (precondition failed, r1-e00006); cross-border-partnership (unsupported action, r1-e00007); legal-group (unsupported action, r1-e00008); logistics-group (accepted, r1-e00010); regional-health-network (unsupported action, r1-e00011); technical-group (precondition failed, r1-e00013). Waited: country-group-1.

## Round 2

original, trace `world-builder-live/run/e8285ae0fcd0420aab38f05f71b96d39`: tried a move: community-group (unsupported action, r2-e00001); country-group-1 (unsupported action, r2-e00002); country-group-2 (unsupported action, r2-e00003); country-group-3 (unsupported action, r2-e00004); country-group-4 (accepted, r2-e00005); cross-border-partnership (accepted, r2-e00007); legal-group (unsupported action, r2-e00008); logistics-group (precondition failed, r2-e00010); regional-health-network (accepted, r2-e00012); technical-group (accepted, r2-e00014). Waited: none.

## Round 3

original, trace `world-builder-live/run/fbca551ef2344835b1d6924d0bf2adc4`: tried a move: community-group (unsupported action, r3-e00001); country-group-1 (accepted, r3-e00002); country-group-2 (precondition failed, r3-e00004); country-group-3 (accepted, r3-e00006); cross-border-partnership (precondition failed, r3-e00008); logistics-group (precondition failed, r3-e00010); regional-health-network (precondition failed, r3-e00012). Waited: country-group-4, legal-group, technical-group.

branch, trace `world-builder-live/run/72e74f509ee54923924d80d96a547e2c`: tried a move: community-group (accepted, r3-e00001); country-group-1 (precondition failed, r3-e00003); country-group-2 (precondition failed, r3-e00005); country-group-3 (accepted, r3-e00007); cross-border-partnership (unsupported action, r3-e00008); logistics-group (precondition failed, r3-e00010); technical-group (precondition failed, r3-e00012). Waited: country-group-4, legal-group, regional-health-network.

## Round 4

original, trace `world-builder-live/run/8abc732f5257462e92c2e38c64225973`: tried a move: community-group (accepted, r4-e00001); country-group-1 (unsupported action, r4-e00002); country-group-2 (precondition failed, r4-e00004); country-group-4 (precondition failed, r4-e00006); cross-border-partnership (precondition failed, r4-e00008); regional-health-network (precondition failed, r4-e00010); technical-group (precondition failed, r4-e00012). Waited: country-group-3, legal-group, logistics-group.

branch, trace `world-builder-live/run/049f91f3cf104ff6983c3e92b9bc123b`: tried a move: country-group-1 (precondition failed, r4-e00001); country-group-2 (precondition failed, r4-e00002); country-group-3 (precondition failed, r4-e00003); country-group-4 (precondition failed, r4-e00004); logistics-group (precondition failed, r4-e00005); regional-health-network (precondition failed, r4-e00006); technical-group (precondition failed, r4-e00007). Waited: community-group, cross-border-partnership, legal-group.

## Round 5

original, trace `world-builder-live/run/abad9f59797e4bbab7c6557282333afc`: tried a move: community-group (unsupported action, r5-e00001); country-group-2 (precondition failed, r5-e00002); country-group-3 (precondition failed, r5-e00003); country-group-4 (precondition failed, r5-e00004); cross-border-partnership (precondition failed, r5-e00005); legal-group (unsupported action, r5-e00006); regional-health-network (unsupported action, r5-e00007); technical-group (precondition failed, r5-e00008). Waited: country-group-1, logistics-group.

branch, trace `world-builder-live/run/cc2603e128314210b872cd02ffc91ee8`: tried a move: country-group-1 (accepted, r5-e00001); country-group-2 (unsupported action, r5-e00002); country-group-3 (precondition failed, r5-e00004); country-group-4 (precondition failed, r5-e00006); cross-border-partnership (unsupported action, r5-e00007); legal-group (unsupported action, r5-e00008); logistics-group (precondition failed, r5-e00010); regional-health-network (precondition failed, r5-e00012); technical-group (precondition failed, r5-e00014). Waited: community-group.

## Round 6

branch, trace `world-builder-live/run/5b234d2ab50f47b5a8f72326dc9154fe`: tried a move: country-group-1 (precondition failed, r6-e00001); country-group-2 (precondition failed, r6-e00002); country-group-3 (precondition failed, r6-e00003); country-group-4 (precondition failed, r6-e00004); cross-border-partnership (precondition failed, r6-e00005); legal-group (unsupported action, r6-e00006); logistics-group (precondition failed, r6-e00007); regional-health-network (precondition failed, r6-e00008); technical-group (precondition failed, r6-e00009). Waited: community-group.

## Round 7

branch, trace `world-builder-live/run/c0668ef359194de6919c76aef5f478e2`: tried a move: community-group (unsupported action, r7-e00001); country-group-1 (precondition failed, r7-e00002); country-group-2 (precondition failed, r7-e00003); country-group-3 (precondition failed, r7-e00004); country-group-4 (precondition failed, r7-e00005); cross-border-partnership (precondition failed, r7-e00006); legal-group (unsupported action, r7-e00007); logistics-group (precondition failed, r7-e00008); regional-health-network (precondition failed, r7-e00009); technical-group (precondition failed, r7-e00010). Waited: none.

## Round 8

branch, trace `world-builder-live/run/b882dbaf2a714fd1872f5708a44771c2`: tried a move: community-group (precondition failed, r8-e00001); country-group-1 (precondition failed, r8-e00002); country-group-2 (unsupported action, r8-e00003); country-group-3 (precondition failed, r8-e00004); country-group-4 (precondition failed, r8-e00005); cross-border-partnership (unsupported action, r8-e00006); legal-group (precondition failed, r8-e00007); logistics-group (unsupported action, r8-e00008); regional-health-network (precondition failed, r8-e00009); technical-group (precondition failed, r8-e00010). Waited: none.

