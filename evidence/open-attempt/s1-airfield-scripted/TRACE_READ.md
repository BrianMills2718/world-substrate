# Trace read: first S1 owner run on the airfield (scripted moves, no residents)

Run: owner allowance, deployed `fe8c492`, started 2026-10-26T01:11:18Z, share `bdS0KIsTlmsB`, 12 server rows
(`run-log.jsonl`: 1 generate, 10 run, 1 readout), $0.0139 in all. The model calls are in `llm-calls.jsonl`
(ids 18366-18373). Description: "A small airfield office: a brick wall between the office and the hangar,
a glass of water on the desk, a helicopter in the hangar, and Sam, a trainee who has never flown."

This run was meant to be the S1 live run (`docs/plans/open_attempt.md`, A2-A4 and A9). It is kept as
evidence of why it could not be. The repair is verified by `../s1-airfield/`.

## Findings

1. **No resident ever moved, so open attempts were never exercised.** Every round's mover is
   `scripted-least-recent`, at $0. The build trace `world-builder-live/kind/90041716bf8c4eb7a7f8ac3bbf364038`
   (call 18366) answered `about_people: false`: "mainly a place and its objects, with Sam mentioned only as a
   trainee and no interactions, differing goals or decisions". A world of things gets no briefs. The page
   ticks "AI chooses each person's moves" only for people worlds, and with the box ticked in a things world
   it would have sent `policy: "llm"` (a menu chooser), never `resident`, so S1 could not run in this world
   at all. Classification: evidence absent (the mover the claim needs never ran). Repair: commit `16d5b18`,
   where the page sends `resident` whenever AI chooses the moves.
2. **The builder added doorways the description does not have.** The world trace
   `world-builder-live/world/c7672e9ad57a4615832ace86d5af9860`, redesign call 18370, got the guidance "every
   actor role must be able to act regularly" after its test run found the instructor stuck. It answered with
   `office-doorway` and `hangar-doorway` (`passable: true`), and every round's move goes through them. The
   brick wall's own passage is kept with `passable: false`, so a wall attempt can still be refused (A3 stays
   testable). The description does not say there is no door, so this is a filled-in assumption, not a broken
   rule.
3. **The page calls the added doorway "left out"** (BrianMills2718/world-substrate#241). `not_modeled` holds "A doorway between the office and
   hangar, added to give the actors a passable route around the brick wall", and the page shows it under
   "Left out of the simulation". The doorway is in the bundle, so the label tells a visitor the opposite of
   what happened.
4. **The builder invented an instructor.** The description names only Sam; the generated bundle has
   `instructor` as a second actor. With no world-kind lens for this, the readout
   (`world-builder-live/readout/bd80ea3667b0486e8de0cfb8a0130f04`, call 18373) read it with the goods-flow
   lens and found every mechanism missing. That is accurate for this run, and the wrong lens for the world.
5. **Sam never used the helicopter or the lessons.** The scripted mover only moved Sam and the instructor
   back and forth. The run summary's `never_offered` says `practice-flight` and `study-lesson` need
   `person.role` to be `trainee` and that nothing ever changes the instructor's role. Meanwhile
   `new-training-lessons-arrive` raised `waiting_lessons` from 3 to 13 over ten rounds with no one studying.

## Round 1

Trace `world-builder-live/run/94b65300c64d4970a9e9996713e74015`. instructor: move to airfield-office by
hangar-doorway, accepted (r1-e00001). sam: move to hangar by office-doorway, accepted (r1-e00003). World:
new-training-lessons-arrive r1-e00004 (waiting_lessons 3 to 4).

## Round 2

Trace `world-builder-live/run/7bec742d215b4207adc4ac957abfc63b`. instructor: move to hangar by office-doorway,
accepted (r2-e00001). sam: move to airfield-office by hangar-doorway, accepted (r2-e00003). World: r2-e00004
(4 to 5).

## Round 3

Trace `world-builder-live/run/95b0390e5e184b27bd139a51d5fd1150`. instructor: move back to airfield-office
(r3-e00001). sam: move to hangar (r3-e00003). World: r3-e00004 (5 to 6).

## Round 4

Trace `world-builder-live/run/64530e66f222467c983d16315e06c21c`. instructor: move to hangar (r4-e00001).
sam: move to airfield-office (r4-e00003). World: r4-e00004 (6 to 7).

## Round 5

Trace `world-builder-live/run/d411c4f8707e4284b553f29616ce7bcd`. instructor: move to airfield-office
(r5-e00001). sam: move to hangar (r5-e00003). World: r5-e00004 (7 to 8).

## Round 6

Trace `world-builder-live/run/b74fc47d95514e1f8a2391b8de37b4a2`. instructor: move to hangar (r6-e00001).
sam: move to airfield-office (r6-e00003). World: r6-e00004 (8 to 9).

## Round 7

Trace `world-builder-live/run/16c5c277623c4ec0bf2a9a4baf741db7`. instructor: move to airfield-office
(r7-e00001). sam: move to hangar (r7-e00003). World: r7-e00004 (9 to 10).

## Round 8

Trace `world-builder-live/run/91b47a7908df45e4bd2b55a0a944e3cd`. instructor: move to hangar (r8-e00001).
sam: move to airfield-office (r8-e00003). World: r8-e00004 (10 to 11).

## Round 9

Trace `world-builder-live/run/98049618d99e4731821794daffb2f72e`. instructor: move to airfield-office
(r9-e00001). sam: move to hangar (r9-e00003). World: r9-e00004 (11 to 12).

## Round 10

Trace `world-builder-live/run/1a211488805f48978110932ba6682ac0`. instructor: move to hangar (r10-e00001).
sam: move to airfield-office (r10-e00003). World: r10-e00004 (12 to 13).
