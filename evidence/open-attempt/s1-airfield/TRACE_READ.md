# Trace read: S1 live airfield run with AI residents

Run: owner allowance, deployed `87b4aa2`, started 2026-10-26T03:47:54Z, share `PKVERt8chzt7`, 11 server rows
(`run-log.jsonl`: 1 generate, 9 run, 1 readout), $0.0319 in all. The 65 model calls are in `llm-calls.jsonl`
(ids 18374-18438: 36 Concordia resident, 20 attempt interpreter, 5 mechanic authoring, 2 world authoring,
1 world kind, 1 readout). Description: "A small airfield office: a brick wall between the office and the
hangar, a glass of water on the desk, a helicopter in the hangar, and Sam, a trainee who has never flown."

This is the S1 live run of `docs/plans/open_attempt.md` (A2-A4, A9) after `../s1-airfield-scripted/` showed
that no resident moved there. It was run once and is reported as it came out; it was not rerun to get the
behaviors it lacks.

## Findings

1. **Residents moved, every round.** Each round's mover is `llm-resident (Concordia)` on
   `openrouter/openai/gpt-6-luna`, four resident calls per round. The repair from `#242` (AI moves are always
   residents) works live. Classification: pass.
2. **A4 passes live: a refused or unmatched attempt changes nothing.** 15 attempts were refused by a check or
   matched no move (r1-e00002, r1-e00004, r2-e00003, r2-e00005, r3-e00002, r3-e00006, r4-e00002, r4-e00003,
   r6-e00001, r6-e00002, r7-e00001, r8-e00001, r8-e00002, r9-e00001, r9-e00002). Each records the same world
   hash before and after, empty changes and `changed: false`, and every unmatched one is listed in the
   round's `unmatched_attempts` with the interpreter's nearest move and reason. Classification: pass.
3. **A2 and A3 were not exercised.** Nobody tried to fly the helicopter or go through the wall, so the run
   says nothing about a free attempt with a fallback (A2) or an attempt stopped by the world (A3). The cause is
   in the build, not the run:
   - The kind call `world-builder-live/kind/6b84ab150e3e4ec19a9e30bef271ed72` (18374) answered
     `about_people: false`, yet the world build `world-builder-live/world/3fb55edadef84f4d9516b25d7cde231e`
     added an instructor, a mechanic, a dispatcher and a recurring training-request process that the
     description does not have. The queue grows from 1 to 14 waiting sessions.
   - Sam, the instructor and the dispatcher start in the office, the mechanic and helicopter in the hangar, and
     the brick wall (`passable: false`) is the only way between them. The builder's own test runs said
     "never possible: practice flight" on all three attempts, and the third was accepted anyway.
   - The redesign calls (18379-18381) proposed an `open-boundary` move (opening the brick wall); it is absent
     from the final moves (move, request-training, prepare-helicopter, practice-flight, drink-water).
   Classification: evidence absent (the attempts the claim needs never happened). Next: A2 as the plan's
   fixture run on this saved world ("fly the helicopter to the coast"), A3 as an interpreted attempt at the
   wall on the same world.
4. **The refusal reason reads as a fact, not a requirement.** Sam's refused `request-training` shows
   `you are the dispatcher`, which is the check's label. "Only the dispatcher can request training" is what
   it means. The residents read it correctly anyway: Sam's r2 belief says the dispatcher, not Sam, must
   request training. Classification: wording defect, filed.
5. **Residents adapt from what they see.** The dispatcher stops requesting at nine waiting sessions (r5) and
   says a longer queue would not help; Sam stops repeating a role-refused attempt (r4) and asks instead
   (r6, r9); the mechanic waits once the helicopter is ready. Their `belief` and `expects` fields name the
   earlier failures they noticed.
6. **The interpreter keeps "ask" apart from "do".** "Ask to be assigned a waiting session" maps to
   `request-training` (then refused by role); "ask what I should do" is unmatched. That is the Q22 default
   (an unmatched attempt changes nothing), applied consistently.
7. **The readout used the wrong lens.** `world-builder-live/readout/d8ec00271e774939aa848c8818ae6c2c` chose
   the `flow` lens ("How goods moved through the chain") for a training-queue world, so all four of its
   mechanisms are "missing". Its summary sentence is accurate. Classification: readout lens choice defect,
   filed.
8. **Round count.** The share page says 8 rounds; the log holds 9 run rows and 9 transcript rounds. Not yet
   explained; recorded as an open item rather than guessed at.

## Round 1

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/c1fe6bbb43834088a046829a5ee12266`. The dispatcher's "request one training
session" is accepted (r1-e00001). The instructor's invitation to Sam is unmatched (r1-e00002, nearest
request-training: a conversation, not a request). Sam asks the dispatcher to be assigned the waiting session;
it is read as request-training and refused, `you are the dispatcher` (r1-e00004). The mechanic waits. The
recurring process adds a session (r1-e00005, 2 to 3).

## Round 2

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/c2b737f1b4214f3d8db1f4ff1f4e18b0`. Dispatcher requests again (r2-e00001). The
instructor, noting the invitation changed nothing, tells the dispatcher they are ready; read as
request-training and refused by role (r2-e00003). Sam asks again and is refused by role (r2-e00005); Sam's
belief now says the dispatcher must request training. The mechanic waits. Process: 4 to 5 (r2-e00006).

## Round 3

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/83e911794f1d48c591758222ad240495`. Dispatcher requests (r3-e00001). The
instructor repeats the readiness line; this time it is unmatched (r3-e00002, nearest practice-flight). The
mechanic inspects the helicopter, accepted as prepare-helicopter (r3-e00004). Sam asks the instructor to
begin a session; read as request-training and refused by role (r3-e00006). Process: 6 to 7 (r3-e00007).

## Round 4

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/64bce53865be41e89919c050e390925e`. Dispatcher requests, saying the queue is
already large (r4-e00001). The instructor asks Sam whether he is ready, unmatched (r4-e00002). The mechanic
tells the dispatcher the helicopter is ready, unmatched (r4-e00003). Sam waits, saying a role-refused attempt
is not worth repeating. Process: 8 to 9 (r4-e00004).

## Round 5

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/737fd2fcf4164e1190102383ec5f90a8`. All four wait: the dispatcher because more
requests only lengthen the queue, the instructor because the wall blocks the hangar and only the dispatcher
can request, the mechanic and Sam because nothing they tried changed anything. Only the process acts
(r5-e00001, 9 to 10).

## Round 6

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/ad3904744086488f934e204a2ed75324`. The instructor asks the dispatcher what is
needed to arrange a session, unmatched (r6-e00001). Sam asks what to do to be assigned, unmatched
(r6-e00002). The dispatcher and mechanic wait. Process: 10 to 11 (r6-e00003).

## Round 7

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/3d35c888205d476f948f8a6025932273`. The instructor asks the dispatcher to assign
a waiting session, unmatched (r7-e00001: assigning an existing session is not adding one). The dispatcher,
mechanic and Sam wait. Process: 11 to 12 (r7-e00002).

## Round 8

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/65a848688c944dfda168a38308ff7c1b`. The instructor asks what step is needed
before an assignment, unmatched (r8-e00001). Sam asks to be assigned one of the twelve sessions; read as
request-training and refused by role (r8-e00002). The dispatcher and mechanic wait. Process: 12 to 13
(r8-e00003).

## Round 9

Actor ids: `dispatcher`, `instructor`, `mechanic`, `sam`. Trace `world-builder-live/run/ee0990e41abc49088de5be32f5485c56`. The instructor says they are available
whenever a session is assigned, unmatched (r9-e00001). Sam asks what he can do to be assigned, unmatched
(r9-e00002). The dispatcher and mechanic wait. Process: 13 to 14 (r9-e00003).
