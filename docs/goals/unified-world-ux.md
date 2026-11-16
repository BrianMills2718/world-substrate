# Goal: one World Builder UI, from a description to a run you can watch, replay, branch and reopen

**Execution profile:** continuous-light
Planning package: docs/planning/planning-package.json
Source: Brian, 2026-11-16: "i still have not seen a working ui. where i can give natural langague descirptions iin dialgoue with an agent to create a world. generate the world. watch the world run live or play it back or brnahc it or preivously generated worlds and which acts as a useful simulation relevant to waltzmans paper"; "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams."

## Mission

One app at brianmills.dev/world-builder where a person describes a world in a back-and-forth with an agent, sees the draft world in plain words, builds it, and then watches it on the room map with the graph beside it: live, played back from any round, or branched from any round with one thing changed. Earlier worlds and runs are in a library and reopen into the same view. Today these are separate pages (home, build, play, room-map, the old Network panel); the live run shows text rounds and the old boxes diagram, and the map exists only on a shared run (walkthrough 2026-11-16, session 94a4d2c4).

## Canonical example

Brian types, in the dialogue: "Ten groups (four countries, a regional health network, a cross-border partnership, and technical, legal, logistics and community groups) must decide by a deadline whether to activate a shared early-warning system; they meet weekly." The agent asks at most a few questions, then shows a draft in plain words that names all ten groups, the meeting and the deadline. He presses Build. The run opens on the room map with the graph beside it and plays live. He pauses at round 4, drags the round scrubber back, presses Branch, changes one thing (for example a group's concern is resolved earlier), and the branch plays beside the original so the two can be compared. He closes the tab, opens the library, and reopens the same world and both runs in the same view.

## Design method (before building)

1. Survey programs that do the same job and write what each does well and badly, from their live or documented interface (not memory): chat-to-app builders (Lovable, v0, Replit Agent), agent-town viewers (Smallville / generative agents, AI Town, Concordia), simulation tools (NetLogo, AnyLogic, Machinations), timeline and branching tools (Git graph views, video-editor timelines, Figma version history), and library sidebars (Notion, Linear). Record adopt, adapt or reject per feature with the reason.
2. Check against recognised guidance: Nielsen's usability heuristics, WCAG 2.2 AA (Brian is red-green colorblind: blue, orange and grey plus words, never colour alone), progressive disclosure, a first-visit cold read test with no jargon.
3. One app shell: library rail, stage (map + graph), round timeline with branch points, dialogue panel. Retire the old Network panel and the separate play and build pages by redirecting their links; keep old links working.

## Boundaries

In scope: the World Builder front end and the service routes it needs; the builder dialogue; plain-words draft; live, playback, branch and library views; the Waltzman scenario as the first world.
Out of scope: changing the simulation rules or the substrate; Smallville art; sending anything to anyone; changing owner-password rules (owner library stays owner-only; visitors get a clearly labelled try-it path that does not save).
Irreversible or outward actions: deploy only after the `publish-checker` subagent returns publish; no email or posts.

## Smallest vertical increments (each merges when it works)

1. Design survey and a one-page UX spec with wireframes of the shell (reviewed once).
2. Live run on the map: the live run page shows the room map and graph beside it (same view as a shared run); old Network panel removed from the live page.
3. Timeline: round scrubber and playback in the same view; the same view opens a saved run.
4. Branch: branch from any round with one change; two runs side by side.
5. Library: owner library lists worlds and runs, reopens into the view; visitor try-it path.
6. Dialogue: the describe step becomes a back-and-forth with plain-words draft and an editable "so far", keeping all named groups (the walkthrough lost 6 of 10).
7. Polish: cold-read test, phone width, accessibility, honest build-time message (the page said about a minute; it took about 3), jargon removed from build lines.

## Acceptance checks

- Each increment: tests marked with their OpenSpec scenario slug, `make check` via `batch ship`, a Playwright walk of the live page with screenshots at desktop and phone width that the agent reads.
- Full-trace visibility: every build and run trace for the walkthrough is opened and read (build trace, rule check, each resident round), a sample of ordinary rounds and every refusal, before saying it works.
- Waltzman fit: the built world is compared against the existing Waltzman world and its source documents; every named group, the weekly meeting and the deadline are present, or each omission is listed with why.
- Cost: every model-calling walkthrough records its measured cost (`llm-cost`), and the cheapest design that does the job is used first.

## Stops

- No progress: three attempts at the same failing step with no new evidence: record `blocked`, the step, the evidence and the resume event.
- Finite loop: at most 7 increments plus 2 correction rounds each.
- Strategic revalidation after three increments or about four hours: report outcome progress against enabling and process work, and retain, replace or clear the goal. Three process-only increments in a row trigger revalidation.
- A hook, permission or credential refusal is a stop: record `blocked on <person>` with the exact command; do not try other forms of it.

## Non-gating next actions

- Brian supplies Waltzman's paper if he wants the fit check made against it; without it the check uses the existing Waltzman world and its source documents.
- Brian uses the app on a real world and says what he kept; tracked on the roadmap row, does not gate this goal.
- Decisions 17 and 18 (guided page for Waltzman; the lineage finding Q60) follow this goal.
