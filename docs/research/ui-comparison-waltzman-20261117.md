# World Builder vs earlier Waltzman UIs (2026-11-17)

Status: research input (observed evidence), not a plan. Source: Brian, 2026-11-17: "have you actually compared this ui to other uis? including previous versions related to my own waltzman code". Before this note, nobody had compared the current page side by side with the earlier Waltzman UIs.

Method: every reachable page was opened in Playwright (Chromium) at 1280 px and 390 px wide, and the screenshots were read. Only GET requests were allowed; every other request was blocked, apart from the read-only `POST /live-replay` map call. Blocked requests were printed only by the capture script (`evidence/ui/ui-compare-waltzman-20261117/shoot.py`, the first pass over every page plus `play/` and `build/`); there, the only requests blocked were Cloudflare `cdn-cgi/rum` beacons. The later interaction scripts blocked silently. No model call was made, nothing was spent, and nothing was clicked that runs, shares, branches or asks for a readout. Deployed pages were matched to repository files by sha256: the deployed file and the repository file were byte-identical in each case below.

Line numbers refer to commit `184f163` (the base of this branch; its `scripts/world_builder_home.html` is the deployed file, sha256 `d7a5c72e…`). Screenshots cited by name are in `evidence/ui/ui-compare-waltzman-20261117/` (viewport captures, one or more per UI).

## The Waltzman job used for the comparison

The test job has four parts:

- Ten groups (four countries, a regional health network, a partnership, and technical, legal, logistics and community groups).
- A weekly meeting.
- A decision deadline.
- Watching it run, seeing why moves were refused, and comparing runs.

For the current page I used the shared run `https://brianmills.dev/world-builder/?run=FQHXnP_TLKPi`. It was created 2026-10-23 and has 10 people, 45 rounds and a saved readout (`GET /world-builder/api/share/FQHXnP_TLKPi`). A live run and the owner-only "What if…" branch were **not viewed**: both need owner access and model spend.

## Inventory

| # | UI | Source | URL | Reachable | Viewed |
| --- | --- | --- | --- | --- | --- |
| C | Current World Builder (shared-run view) | `scripts/world_builder_home.html`, embedding the room-map viewer `viewer/smallville/` | https://brianmills.dev/world-builder/?run=FQHXnP_TLKPi | yes (deployed = local, sha256 `d7a5c72e…`) | yes, 1280 + 390 |
| D | Donor workbench "Coordination Environment Lab" (Cybernetic Influence; outcomes judged by an AI referee, not rules) | `~/code2/cybernetic_influence_v3/public/waltzman/` (local HEAD `446fd57`; the deployed step-7 title differs from local `app.js:1229`, so the deployed copy is not that HEAD) | https://brianmills.dev/waltzman/ | yes | yes: overview, case-study steps 1, 3, 4, 5 at 1280 + 390 |
| V2 | Living-world replay v2, "Coordination Hall" (hand-written six-resident world, baseline + intervention) | `evidence/renders/waltzman-living-v2.html`, built by `scripts/build_waltzman_living_replay_v2.py`; renderer `scripts/render_composed_living_scene.py`, `scripts/render_composed_living_scene_branches.py` | https://brianmills.dev/waltzman/world-substrate | yes (sha256 `c7fdfc95…` = file) | yes: both branches, last frame, gate inspector |
| V0 | Analytical demo v0 (same hand-written world) | `evidence/renders/waltzman-demo-v0.html` from `scripts/render_waltzman_demo.py` (`run_waltzman_demo.py` data) | https://brianmills.dev/world-substrate-visualization/ | yes (sha256 `295363c3…` = file) | yes: start, end of baseline |
| N | Native run 2026-10-08 (Waltzman text compiled to rules, ten groups, AI members, 12 rounds, $0.110) | `spikes/any-scenario-2026-10/evidence/waltzman-spec/run2/run/frames.html` (renderer `spikes/any-scenario-2026-10/render_run.py`) | https://brianmills.dev/world-substrate-runs/waltzman-native/ | yes (sha256 `d7edcb28…` = file) | yes |
| I | "Waltzman demo versions" index (#151, `54ca493`): an earlier side-by-side list of D, V2, N and C | `deploy/cloudflare/native-runs/index.html` | https://brianmills.dev/world-substrate-runs/ | yes | text only |
| V1 | Living-world replay v1 (precursor of V2) | `evidence/renders/waltzman-living-v1.html` (+ `-baseline-v1`, `-intervention-v1`), `scripts/build_waltzman_living_replay.py`, `scripts/render_living_scene_branches.py` | none | file only | yes, `file://`, end of baseline |
| NP | Old Network panel on the run page (added `fc73aa3` 2026-10-26, removed `843121e` 2026-11-16) | `scripts/world_builder_home.html` at `a12c2f7` (= `843121e^`), lines 359-366, plus `scripts/vendor/graph-viewer.js` at that commit | none | git history only | yes: rebuilt locally by serving the old HTML against the live read-only share API, 1280 + 390 |
| S | Read-only HTTP/SSE host for V0 | `scripts/waltzman_demo_service.py` (serves the V0 HTML plus `/api/branches`, `/api/projection`, `/api/events` SSE) | none | local only | not viewed: same HTML as V0, the SSE stream was not exercised |
| R1 | Native run 1 frames | `spikes/any-scenario-2026-10/evidence/waltzman/run/frames.html` | none | file only | not viewed: same renderer as N |
| P | Overlay prototype | `prototypes/living-world-overlay-v0.html` | none | file only | not viewed |
| — | `play/` World Replay Studio | `evidence/renders/world-replay-studio-v0.html` | https://brianmills.dev/world-builder/play/ | yes (sha256 `ce77f422…` = file) | yes, 1280 + 390 (`play-1280`): four two-person scenes (Kitchen, Castaway, Workshop, Greenhouse); the deployed page has 0 "waltzman" hits |
| — | `build/` World Authoring Studio | `evidence/renders/world-builder-v0.html` | https://brianmills.dev/world-builder/build/ | yes (sha256 `de6d7f22…` = file) | yes, 1280 + 390 (`build-1280`): a 9-step bundle editor; its description box says "Supported first-release family: 3–6 members", so it cannot hold the ten-group job; 0 "waltzman" hits |
| — | Public room-map demos | `scripts/build_public_demos.py` (pump facility, not Waltzman) feeding `viewer/smallville/` | https://brianmills.dev/world-builder/room-map/ | yes | not viewed separately: it is the same viewer C embeds |

Screenshots taken earlier are committed as `evidence/renders/waltzman-living-v1-*.png` and `waltzman-living-v2-*.png`.

## What each page shows on the Waltzman job

| UI | Ten groups, weekly meeting, deadline | Watch it run | Why moves were refused | Compare runs |
| --- | --- | --- | --- | --- |
| **C (current)** | Yes, the only UI here where a visitor makes this world from a description (N's pipeline also compiled the Waltzman text into rules, but offline, not from a page): 10 people, a "regular meeting" process and a deadline countdown (map THINGS column, screenshot `wb_run-map-end-1280`). Deadline, support and deployment values are **not on screen**: THINGS boxes show labels only, and the map shows "no move" bubbles. | Room map plus graph, Play, Previous/Next round, speed and a scrubber "Round 45 · step 202/202" (viewer controls, `viewer/smallville/index.html:42`). Default graph is "Whole network beside the map": 71 boxes and 397 links in three columns, and a third of the frame is empty black. At 390 px the map shrinks to an unreadable strip with no labels (`wb_run-map-end-390`). | Event inspector shows original words, interpretation, result, state changes, `refused_because` and Cause/Consequence buttons (`world_builder_home.html:1978-1985`). The "Why things were refused" strip and the per-round feed are moved into the collapsed "More ways to inspect this recording" for a shared run (`world_builder_home.html:2002`). | "What if…" plays a branch beside the original as two maps (`world_builder_home.html:324-329`, `1696-1716`), owner only (`:1680`); hidden on a shared run. No outcome numbers are compared. Not viewed live (spend). |
| **D (donor)** | 26 officials, four countries (a different, larger cast); the deadline is not shown as a value. | Not a player: a 7-step guided case study (`app.js:1222-1230`) with step bar, Previous/Next and `?case_step=N` links (`app.js:350`, `387`). | Step 5 pairs each official's own words "while coordination was blocked" and "after the compact", tagged CONDITIONAL / SUPPORT (`index.html:272`). Outcomes are judged by an AI referee, so "why" is reasoning, not a rule. | Step 4: three rounds as stacked bars, "26 will proceed / 6 will proceed · 20 only on conditions / 26 will proceed" (`index.html:261`, `app.js:1342`). Headline result card on the front page. |
| **V2 (Coordination Hall)** | Six hand-written residents, one meeting (ticks 4-6), no deadline. | Best stage of all: illustrated hall, each station shows its value on the map ("2 labs / need 3 labs" with a bar, gate "blocked · support 2/6 · conditional 4"), a caption "tick 6 · Coalition decision gate evaluates", one bottom transport bar (`render_composed_living_scene.py:181`). Readable on one phone screen at 390 px. | Click an object for a state inspector (`render_composed_living_scene.py:129`, `181`): state only, no causes. | "History" select switches baseline and intervention one at a time, with `?branch=…&frame=N` links (`render_composed_living_scene_branches.py:36`). No side by side. |
| **V0 (analytical)** | Same six residents; no deadline. | Always-visible "World state" tiles: Coalition, Meeting, Support 2 / 6, Branch (`render_waltzman_demo.py:30`). Clickable event list that scrubs (`:33`). Layer toggles for information, causal, constraints and analysis (`:28`). | Selected event splits "Information / cognition context" (what the person had heard) from "Mechanic-declared causal parents" with event ids (`:31`). | Branch select labelled "Baseline · blocked / Intervention · recovers" plus "fork point: e00021" (`:28`, `:62`). |
| **V1** | As V2. | Plainer version of V2: same station values and gate card; resident stance labels nearly invisible (`living_v1-baseline-end-1280`). At 390 px the resident initials, a message bubble and section titles overlap the name tags (`living_v1-390`). | No. | Branch select, as V2. |
| **N (native run)** | Yes: the same ten groups, weekly meeting and deadline, from the Waltzman text. | Scene with a reasoning card per actor in its own words, then "Engine events this round" with before → after values, and "State after this round" for every object (`frames.html:35`): `Member Support … conditional_support_count=5`, `weeks_remaining=6`, `deployment_blocked=false`. Cards overlap at 1280. At 390 the page is 405 px wide and the scene is unreadable. | Each event is marked accepted / `invalid_action` inline. | No. |
| **NP (old Network panel)** | Same share as C. | Focused graph: "Showing 5 of 71 boxes: who acted in round 1 and what that used or changed", labelled arrows (recipient, information, delivery), zoom, and "Show the whole world (71 boxes)" (`a12c2f7:scripts/world_builder_home.html:359-366`). Easier to read than C's default whole-network view. | Selecting a box shows its state. | No. |

## What each earlier UI did better and worse than C

| UI | Better than C | Worse than C |
| --- | --- | --- |
| D | Leads with the finding (headline result card). Shows the outcome measure as support/conditional bars across conditions. Pairs each person's reasoning before and after. Guided step-through with shareable step links. Usable at 390 px. | A different, hand-shaped case and not rule-enforced (index I says so). No player, no free exploration, no making a new world. Simulation generation was "temporarily unavailable" on the overview. The before/after cards overflow their columns at 1280. At 390 the sticky step bar covers the "RESULT" label. Bars use green and orange; green carries meaning for a red-green colourblind reader only with the words beside it. |
| V2 | Values drawn on the stage, decision gate central and labelled, one compact transport bar, current event as a caption, a phone layout that fits one screen. | Hand-built six-person world (not the ten-group job), no deadline, no "why", branches retained only, title overlapped by the History box at 390. |
| V0 | Persistent outcome tiles, information-vs-cause split, fork point named, clickable event list as the timeline. | Same hand-built world. The left resource card is clipped ("oss-lab validation capacity"; at 390 px the side cards are cut at both edges, `demo_v0-390`). Dense 8-9 px text. Trust/risk/readiness "proxies" are observer heuristics with no rule behind them. |
| N | Same job as C. Every object's state after each round, and before → after values per event, readable without clicking. | Overlapping cards, unusable at 390 (405 px wide), no branching, the one invalid "deployment blocked" event noted on index I. |
| NP | Focused per-round graph by default, readable. | Separate panel below the run. Replaced on purpose by the map-plus-graph stage ([unified-world-ux goal](../goals/unified-world-ux.md) step 2). |

What C does that no earlier UI does: build the ten-group world from words, enforce rules, branch from any round (owner), show a readout that names the four Waltzman mechanisms with checked event ids, and offer an actor-inputs view (`world_builder_home.html:316-321`, `373`, `2334-2357`).

## Features C lacks: verdicts

| Feature | Where it exists | C today | Verdict |
| --- | --- | --- | --- |
| 1. A persistent outcome strip for the job: members supporting / conditional / undecided, decision status, deployment status, weeks to deadline, meetings held, following the scrubber | V0 `render_waltzman_demo.py:30`; V2 gate card on stage; N "State after this round" | None. The world-state panel lists only the objects the selected event touched, plus a collapsed "All world objects (30)" (`world_builder_home.html:349`). Map THINGS boxes have no values. At round 45 nothing on screen says whether the system was deployed. | **Adopt.** Use words plus blue, orange and grey, never colour alone. |
| 2. Comparing runs as outcome numbers: per-round support/conditional bars for the original and the branch, with the fork round marked | D step 4 (`index.html:261`); V0 fork label (`:62`) | Two maps side by side, owner only, no numeric diff (`:1680`, `:1712`) | **Adapt.** One small chart under the two maps. Also show it on shared runs that carry a branch. |
| 3. Values on the stage: each thing shows its current value or status where it is drawn | V2 / V1 stations ("2 labs / need 3") | Labels only in the THINGS column; map bubbles say "no move" | **Adopt** for the few objects the outcome strip does not cover, or on selection. |
| 4. Findings first, with event ids that jump the map | D headline card and guided steps; V0 clickable event list (`:33`) | The readout is strong, but on a shared run it sits at the bottom inside "More ways to inspect", and its event ids are hover-only (`world_builder_home.html:2356`, `2002`) | **Adopt.** Show the readout summary above the map, and make each cited event select its round. A full 7-step tour: adapt later. |
| 5. Each person's own words before and after a change, side by side for the original and the branch | D step 5 (`index.html:272`); N reasoning cards | Per-event "Original words" (in this share, "Not recorded") | **Adapt** once branches carry resident words. |
| 6. Default to the focused per-round graph | NP (5 of 71 boxes); viewer's own "This round only" mode | Default "Whole network beside the map", 71 boxes / 397 links (`viewer/smallville/index.html:42`) | **Adapt.** Default to `round`, keep the whole network one click away. |
| 7. Phone layout that fits | V2 at 390 | Map unreadable at 390 | **Adapt** (already step 7 of the [goal](../goals/unified-world-ux.md)). |
| 8. "Why things were refused" strip visible on shared runs | C's own live view | Collapsed for shared runs (`:2002`) | **Adapt.** Move it next to the inspector. |
| 9. Information context vs causal parents as two labelled lanes | V0 `:31` | Cause/Consequence buttons and an actor-input section exist (`:1984-1985`) | **Ignore** as a separate feature. C covers it; only relabel if readers confuse the two. |
| 10. Trust / risk / readiness proxies, dependency-adequacy panel, layer toggles, deck.gl canvas, illustrated avatars | V0 `:28`, `:32`, `:34`; V2 art | None | **Ignore.** The proxies are heuristics with no rule behind them, and Q50 settles that there is no believability metric. The adequacy panel is tied to the hand-written world. The art direction is the Smallville-style viewer path. |

## Top five for the current page

1. An always-visible outcome strip (feature 1).
2. A run-comparison chart of support over rounds with the fork marked (feature 2).
3. Values on the stage for decision-relevant objects (feature 3).
4. Readout summary first, with clickable event ids (feature 4).
5. The focused per-round graph by default (feature 6).

## Not checked

- A live run and the What-if side-by-side view (both owner-only and paid).
- D's "Show me around" tour: it rendered greyed out and was not clicked.
- D steps 2, 6 and 7.
- S, R1 and P.
- The room-map public demos as a separate page (same viewer as C).
- D's overview and V0 were read at 390 px only at the top of the page (`donor-390`, `demo_v0-390`); their lower sections at 390 px were not checked for this note.
- Whether the shared run's map differs for runs created after 2026-11-16.

## November 27 follow-up on the unified chat

The November 17 changes already put the library in a tab, made Simple the default and retained the map, support chart and Advanced controls. The remaining gap on the landing page was that the example action filled the composer. A visitor could try wording there, but could not open the completed coordination finding. The chat now offers both actions and identifies the recording as an earlier workbench simulation.

On the saved native run, the round story already carried event IDs. The rendered sentences discarded those references. Simple now opens the cited record in place. A shared run without a written story uses its recorded events directly. At 1280 and 390 pixels, opening the final result for share FQHXnP_TLKPi showed round 14 event r14-e00012 changing the decision from authorized to deployed. Its final state at round 45 recorded five supporting, zero conditional and four required. Advanced still exposed all 45 rounds.

The earlier workbench run_5010214f2466 is a separate result. Outright support moved from 26 to six and back to 26 after a prewritten compact. At both widths one action from that finding opened the same simulated official’s statements from rounds two and three. It is the distinction between approving and still requesting safeguards that makes those statements worth showing.

The same chat built a new ten-group flood-warning world. In run 8ccb3b95b72140d79d5312884b6625a2, Country 4 and the Regional Health Network supplied the two outright votes in round one (events r1-e00005 and r1-e00008). Support held at two in round two. The model scheduled the second meeting for tick eight, although the chat draft said one meeting per round. The two-round run ended before that deadline. The Simple result now reports that the deadline was still pending and opens both contributions, including their statements.
