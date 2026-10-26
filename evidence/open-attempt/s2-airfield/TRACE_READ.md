# Trace read: S2 live airfield run with AI residents

Run: owner allowance, deployed `623bce2` (health `build_commit` 623bce29b16c), started 2026-10-26T20:38:46Z,
share `smERAl1viGMr`, 11 server rows (`run-log.jsonl`: 1 generate, 9 run, 1 readout), $0.0372 in all. The 58
model calls are in `llm-calls.jsonl`, pulled from the VPS `llm_observability.db` by time window (ids
18450-18507: 36 Concordia resident, 12 attempt interpreter, 6 mechanic authoring, 2 world authoring, 1 world
kind, 1 readout; all `openrouter/openai/gpt-6-luna`, no errors). Description (same as S1): "A small airfield
office: a brick wall between the office and the hangar, a glass of water on the desk, a helicopter in the
hangar, and Sam, a trainee who has never flown."

This is the S2 owner run of `docs/plans/open_attempt.md` (A5 on a generated world). It was run once and is
reported as it came out; it was not rerun to get the behaviors it lacks.

## Findings

1. **A5 was not exercised: no knock-on effect happened.** No event in the run carries a reaction wave or a
   parent, and no round was refused for the reaction limit (`reaction` appears nowhere in `run-log.jsonl`).
   The cause is upstream of the engine: none of the six rules-writer answers (18452-18454, 18456-18458)
   wrote a `timing: immediately` process, though every prompt carried the instruction. Two answers used
   `each_round`; the kept rules have one process, `new-waiting-lessons`, with no timing (each round). The
   description has no push, fall or break for a chain to follow, and the glass of water got only a
   `drink-water` move. Classification: evidence absent (the world had nothing that sets off a chain). Next:
   A5 as the plan's fixture chain stays the passing proof (`tests/test_open_attempt.py::KnockOnEffectTests`);
   a generated-world A5 needs a description in which something can be knocked over.
2. **The builder kept the worst of its four test runs.** Attempt 1 (72 moves, `circling: true`,
   `never_offered: ["move"]`, `moves_at_end: ["schedule-lesson"]`) was kept over attempts 2-4, which did not
   circle and offered every move. All four scored 2 ("alive, but someone stalled") in
   `scripts/world_builder_service.py` (~line 1393), and the tie-break ranks fewer idle or stalled actors first
   (attempt 1 had one, the others two), so `circling` and `never_offered` lost to it. The served world is the
   one the builder itself said went in circles. Classification: builder selection defect, filed as #253.
3. **Three kept moves change nothing.** `teach-ground-lesson` adds 0 energy, `fly-training-lesson` adds 0
   flights (and does not check where the helicopter is), and `drink-water` sets the drinker's place to the
   place they are already in. None of these three, nor `move`, appears in any of the 36 resident prompts
   (`schedule-lesson` is in 35, `inspect-helicopter` in 32; first one is call 18459), so no resident was
   ever shown a way to fly or teach. Why the prompt leaves them out was not traced here. Classification:
   rules-writer defect (no-op effects), filed as #254.
4. **Residents adapt from what they see, again.** Sam stops scheduling at r3, the instructor at r4, the
   dispatcher at r7; each says scheduling only grows the queue and they see no way to start a flight. Nobody
   tried a free attempt outside the listed move (no fly, no wall, no glass), so A2 and A3 again were not
   exercised here. All 12 interpreter readings matched `schedule-lesson`, `inspect-helicopter` or `wait`;
   nothing was refused or unmatched.
5. **One false belief.** From r4 the mechanic says repeated inspections "have not changed the record", but
   both inspections (r1-e00003, r2-e00005) were accepted and the record shows two; the mechanic did not
   inspect again after r2. Classification: resident memory error, recorded.
6. **The progress line claims a stronger model it does not use.** "Rewriting the rules with a stronger model"
   ran on gpt-6-luna, the same model as the first try (`RULES_RETRY_MODEL` defaults to it when
   `WORLD_BUILDER_STRONG_MODEL` is unset). Classification: wording defect, filed as #255.
7. **Repeats from S1.** The readout (`world-builder-live/readout/f03a94c679cb4281a860479f94ac21db`) again
   chose the `flow` lens ("How goods moved through the chain") for a training queue, and the share page says
   8 rounds while the log holds 9 run rows and 9 rounds. Both remain open from S1 (the lens is #246).

## Round 1

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/2cd39368d906423c839ce0fd342b9b87`. The dispatcher waits (one lesson already waits).
The instructor schedules a lesson (r1-e00001), the mechanic inspects the helicopter (r1-e00003), Sam
schedules a lesson (r1-e00005). Process `new-waiting-lessons` adds one (r1-e00006, 3 to 4).

## Round 2

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/60830b96a1e94da897dd8654d879a176`. The dispatcher (r2-e00001), the instructor
(r2-e00003) and Sam (r2-e00007) schedule lessons; the mechanic inspects again (r2-e00005). Process: 7 to 8
(r2-e00008).

## Round 3

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/76b05959dce645d2af9ee649eeac0f5e`. Dispatcher (r3-e00001) and instructor (r3-e00003)
schedule. The mechanic waits (two inspections, no fault seen). Sam waits: eight lessons wait and scheduling
only grows the queue. Process: 10 to 11 (r3-e00004).

## Round 4

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/9f9c84bb4935472eb46b7737f7e802c1`. Dispatcher schedules (r4-e00001). The instructor
now waits ("no visible way to conduct a lesson"); the mechanic and Sam wait. Process: 12 to 13 (r4-e00002).

## Round 5

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/f7ca9dcd4a034ef79f773ca7616cad9e`. Dispatcher schedules (r5-e00001); the others wait.
Process: 14 to 15 (r5-e00002).

## Round 6

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/7493c38d34b1411b824033dfbfb366e8`. Dispatcher schedules (r6-e00001); the others wait.
Process: 16 to 17 (r6-e00002).

## Round 7

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/ec3b1dfc4bc3490a87e38f86b945708b`. The dispatcher now waits too: lessons pile up
faster than they are used. Everyone waits; only the process moves, 17 to 18 (r7-e00001).

## Round 8

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/6df29b82659246eebd054bdb376c3d52`. Everyone waits. Process: 18 to 19 (r8-e00001).

## Round 9

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace
`world-builder-live/run/3c50d875e9dd4159a5dc6e91fb2a4f34`. Everyone waits. Process: 19 to 20 (r9-e00001).

Build and readout traces: kind `world-builder-live/kind/6aeb3c7641c94eefa6199d0cffdca7d9`, world
`world-builder-live/world/408156f6f104447197ffbefc28f0019a`, readout
`world-builder-live/readout/f03a94c679cb4281a860479f94ac21db`.
