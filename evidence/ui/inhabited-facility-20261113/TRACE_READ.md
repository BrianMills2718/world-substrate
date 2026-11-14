# Trace read — resident run through the world workspace service (2026-11-13)

How it ran: the real `WorldBuilderHandler` HTTP service (the workspace's own `/run` and `/worlds/<id>/runs/<id>/scene` routes) on a temporary
catalog, `policy=resident` (Concordia residents with free-text attempts read by the interpreter, the path the workspace always uses),
one saved round per request because catalog runs advance one round at a time, model openrouter/openai/gpt-6-luna. `run-log.jsonl` is that service's
own `GET /runs?full=1` output (six rows, one per round), not assembled by hand. Measured cost from the six rows: $0.006423 against the $0.12
World Builder cap per run. Scene HTML was fetched from the service's scene route and screenshotted (`workspace-*.png`, desktop 1280px and phone 390px, all viewed).
Earlier direct-harness run and its trace read: `direct-harness/` (it first exposed the three defects, fixed in PR #400).

Two earlier service attempts on this world ended after round 1 or 2 with every open-door attempt "unmatched" (trace ids
`world-builder-live/run/8392666156d343ceaf1eed915baef6de`, `d533a47dd4084234af8030fcc49634a4`, `e49604ad1b244c06985a07df6f8ad8a5`, `c9450554dd174da89c9f2deb0e91eec2`);
that is finding 1 below.

## Findings

1. **Root cause found only through the workspace path.** The typed path (direct harness) offered `open-door`, but the free-text reader refused
   every "open the door" with `partner='lab-door-in' names no entity in this world`: the reader's entity list was the actor's perceived
   entities, and the far half of the door is not perceived. Each such round ended with nothing accepted and the catalog marked the run
   non-continuable ("no active moves"). Fix (`_read_attempt`): entities named by the actor's own known forms are known to it. After the fix the same
   world ran six rounds.
2. **The run is an inhabited place.** 15 accepted moves in six rounds across three people: opening doors (r1-e00003 Bo, r1-e00005 Mara), calibrating (r1-e00001), walking between rooms, and reports (r3-e00001 Ari to Bo, r4-e00001 Ari to Mara,
   r4-e00005 Mara to Ari, r5-e00003 Mara to Bo). Beliefs match place: Mara in the lab (r3): "I cannot see either of them here"; Bo in the corridor (round 5) sees "Ari, Control room door (corridor side), Laboratory door (corridor side), Mara".
3. **Bo's own observation, separated inputs** (`bo-observation-round5.txt`, verbatim model input): memory block (rounds 1 to 4 in his own words), represented state "You are in the Corridor" with his own report log, "In this place with you: Ari, ... Mara", "Delivered to you from ari: The pump is calibrated.", and brief/global knowledge ("last started two weeks ago ...") in a separate block. His round 4 belief ("Ari has told me the pump is calibrated, and I can see its status is calibrated") shows the delivered report and the perceived pump together.
4. **The branch** (`workspace-branch-diverged.png`, scripted catalog run through the same service, a different test on the same world, not LLM evidence): forked from the door-opened checkpoint, Ari stays in the laboratory with the door open and the pump calibrated, while the parent run has Ari walking out; the parent keeps its rounds.
5. **Rough edges, not fixed.** Report records print as raw JSON in "Your represented state" as well as in the "Delivered to you" line; Ari, Bo and Mara repeat the one fixed message to each other; in round 5 Bo walks back to the control room instead of staying near the news. One run of one model; no claim about personality fidelity.

## Round 1

Per-round trace id `world-builder-live/run/12211af49fd3431b9aaeea5c620dd4ee`: ari tried to calibrate the pump (r1-e00001), bo opened the control room door (r1-e00003) and mara opened the laboratory door (r1-e00005), all accepted. Beliefs match the closed doors.

## Round 2

Trace `world-builder-live/run/a1e3fbb5e8104ed5ad828c5cf33f5dcf`: ari walked to the corridor (r2-e00001), bo walked to the corridor (r2-e00003), mara walked into the laboratory (r2-e00005); all accepted.

## Round 3

Trace `world-builder-live/run/c63e2c75910942d6bdc5a12dc10b051e`: ari told bo "The pump is calibrated." (r3-e00001), bo walked into the laboratory (r3-e00003), mara walked back to the corridor (r3-e00005).

## Round 4

Trace `world-builder-live/run/3ca8aafe759a450ea72c4bd6ea1c714c`: ari told mara (r4-e00001), bo walked to the corridor (r4-e00003), mara told ari (r4-e00005). Bo's belief cites Ari's delivered report.

## Round 5

Trace `world-builder-live/run/26f400721a7043cb81d30d783c6fe1a0`: ari waited; bo walked into the control room (r5-e00001); mara told bo (r5-e00003).

## Round 6

Trace `world-builder-live/run/db77f00fc8ec4d7fb6ab72437386d3f5`: ari walked to the control room (r6-e00001); bo and mara waited, Bo believing the pump calibrated from two delivered reports.
