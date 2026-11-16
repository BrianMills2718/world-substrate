# One World Builder UI: spec

Goal: [unified-world-ux](../goals/unified-world-ux.md). Source: Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams." Layout and choices below are inferred by agent from the survey; Brian approves by using it.

## What exists today (walked live 2026-11-16)

`scripts/world_builder_home.html` (one page, four stages: describe, working, review, run) plus `world_builder_app.js`. The run stage shows text rounds, the old Network boxes, a recorded-picture iframe and a saved-run player. The room map and graph (`viewer/smallville/`, `room-map/`) open only from a shared run. A build took about 3 minutes while the page said "about a minute". The agent kept 4 of 10 groups described.

## The shell

```
+--------------------------------------------------------------------------------+
| World Builder   Waltzman scenario  >  Run 2  >  Original        [Share]        |
| Status: Running, round 6 of ?   [Pause]  Speed [1 2 3 4 5]                     |
+----------+---------------------------------------------+-----------------------+
| WORLDS   |                                             | TALK                  |
| + New    |   STAGE: room map, graph beside it          | Agent: Which groups   |
| search   |   (people in offices, meeting room,         | decide? ...           |
| * Waltz. |    messages as chat lines)                  | You: ten groups ...   |
|   Run 1  |                                             | DRAFT (editable)      |
|   Run 2  |                                             |  10 groups, weekly    |
|    what  |                                             |  meeting, deadline    |
|    if... |                                             | [Build] / [Ask what-if]|
+----------+---------------------------------------------+-----------------------+
| TIMELINE  |--1--2--3--[4]--5--6-->   o branch "concern fixed early" from round 4  |
| [Step back] [Play] [Step]   Round 4 of 11    [What if... (branch from here)]       |
| LOG tabs: Story | Turns | Details   (keys S, T, D)    search the log            |
+--------------------------------------------------------------------------------+
```

Phone width: the library and talk panels become two drawers; the stage is first, then the timeline, then the log.

## States

1. **Describe** (dialogue): the agent asks at most three questions, one at a time, each with suggested answers. The draft sits beside the chat as plain words, editable. A "make it more precise" button rewrites the draft.
2. **Draft**: plain-words summary names every group, the meeting and the deadline, and lists what was left out. Build is the approval. An old draft version is read-only with "Back to latest".
3. **Building**: steps appear as they finish; the time shown is the measured one (about 3 minutes), not "a minute"; no internal terms.
4. **Run**: live on the stage. Pause, speed 1 to 5, step. Pauses itself when the tab is inactive and says so.
5. **Playback**: the same stage and timeline; scrubbing never runs the AI. Any round can be named ("moment") and restored without losing the current state.
6. **Branch**: "What if..." at a round opens an isolated copy with one change typed in words; it plays beside the original on the same timeline. Keep or discard. Nothing edits a run in place.
7. **Library**: World, then Runs, then Branches. Gallery and list, star to pin, search, last opened first. Owner library stays owner-only; visitors get a try-it path that is not saved and says so.

## Rules for every screen

- Status always visible: Draft, Building, Running, Paused, or Replay at round N of M, plus the branch name (Nielsen 1).
- Plain words only: "What if", never "branch" or "checkpoint" in the interface (Nielsen 2).
- Blue, orange and grey, each with a word and a shape; never red against green (WCAG 1.4.1; Brian is red-green colorblind).
- Every drag has a button or key alternative; targets at least 24 by 24 px (WCAG 2.5.7, 2.5.8); focus never hidden by sticky bars (2.4.11).
- Space pauses, left and right arrows step; the live log is a polite status region.
- The layout is illustrative where the world has no places (note under the title; spec `scene-viewer`).

## From the survey (adopt list; sources in the survey notes)

Editable approve-gated draft (Lovable); read-only old versions; branch as isolated copy then keep or discard (Replit); always-on snapshots (Simulink, Smallville forking); one screen for live, replay and speed (NetLogo, Smallville); auto-pause on inactivity (AI Town); name a moment and restore without losing state, duplicate from here (Figma); click to inspect, change creates a branch (AnyLogic); searchable log with jump-to-turn (Langfuse), rulings in plain words (Concordia); keyboard view switching (LangSmith); World, Runs, Branches library with star and saved filter (Notion, Linear, Claude Projects). Rejected: git as the version model, hash labels, CLI or URL control, a fixed branch cap. Optional later: "run it N times" for chance-driven worlds.

## Build order and how each reuses the code

2. **Live run on the map.** New route `POST /live-replay` takes the same body as `/share` and returns `_public_replay(_assemble_share(...))` without saving. The run stage embeds `room-map/` in an iframe with `?embed=1`; after each round the page posts the new replay to it (`ws-replay`), the same way it already posts `ws-round` to the old picture. The old picture iframe and the Network panel leave the run stage.
3. **Timeline.** The viewer's round slider and the saved player's round list merge into one timeline bar under the stage.
4. **Branch.** Reuses catalog branching (`catalog_run_id` plus checkpoint) behind the "What if" button; two runs drawn beside each other.
5. **Library.** The existing library (`drawLibrary`, `openCatalogWorld`) becomes the left rail.
6. **Dialogue.** The existing `/clarify` dialogue moves to the right panel and keeps every named group in the draft (a test counts named groups in the description against the draft).
7. **Polish.** Cold-read with a person who has not seen it, phone width, accessibility, jargon, honest times.

Each step: OpenSpec change, tests marked with the scenario slug, `batch ship`, publish-checker, deploy, live walk with traces read.
