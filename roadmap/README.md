---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-11-13
---

# World Substrate living roadmap

**Authority:** [Decision 006](../docs/decisions/006-governed-rules-layer-scope.md) (current scope: the governed-rules layer on commodity runtimes), [Decision 007](../docs/decisions/007-any-scenario-path.md) (describe any scenario), [Decision 008](../docs/decisions/008-build-worlds-in-an-agent-harness.md) (build worlds in an agent harness), [Decision 009](../docs/decisions/009-same-moment-knock-on-effects.md) (same-moment effects are rule semantics), and Decisions [001](../docs/decisions/001-project-scope.md) to [005](../docs/decisions/005-native-waltzman-delivery.md). Architecture: [arc42](../docs/architecture/arc42.md). Required behavior: the [capability specs](../docs/index.md#2-what-the-code-must-do-openspec-capability-specs).
**Stage (reconciled 2026-11-13):** live World Builder alpha. The approved I0/I1 slices are delivered with retained generated/resident evidence and a deployed recording. Declared-laws S1–S3, open-attempt S1–S2 and AI-judge J0–J3 retain their separate statuses. Skill rolls, estimate rules, scientific actor adequacy and full AES runtime conformance remain outside this completed I0/I1 goal. Brian subsequently approved the bounded whole-attempt coverage correction (2026-11-13); unrelated implementation remains outside scope.
**Recent work (#323 to #345, 2026-10-31 to 2026-11-09):** requests reach the person asked (#326); a shared run shows its picture and can be watched (#328, #329, #331); refusals say what really happened (#333); the Network shows one round and uses the fast layout (#338, #344); the Waltzman rebuild was recorded (#339); the planning package caught up (#340); model routes were renamed (#341); the Waltzman lineage review was written, its recommendations not adopted (#342); Brian's scale reason for rules over an AI judge was recorded (#345).
**Deployment boundary:** the World Builder backend runs on the personal VPS and its pages on Cloudflare; shipping is `scripts/deploy_world_builder.sh`. The donor-backed `/waltzman/` demo stays a fallback and must not be presented as a native run.

## Next: inhabited spatial world — clarified direction (2026-11-13)

Brian expected a watchable, inhabited environment like [Smallville](https://reverie.herokuapp.com/arXiv_Demo/): recognizable places and objects, people moving and interacting, visible activities and conversation, with play, replay and branching. He judged the delivered schematic scene short of that experience. The deployed workspace and its technical checks remain valid for the narrower catalog/replay claims below; they did not establish that visual outcome. Do not treat the inhabited-world request as complete.

**Recommended next slice (agent recommendation, not yet implemented):** update [product context](../PRODUCT.md), [design](../DESIGN.md), and required behavior, then connect an illustrated pump facility (laboratory, corridor, control room and doors) end to end. Demonstrate a closed boundary refusing movement, an open boundary allowing it, location-sensitive observation alongside authorized remote messages and retained memories, and the same events in a watchable scene with replay and a saved-round branch. Review the rendered experience against the Smallville reference as well as testing its data; do not substitute scene visibility or passing counts for that outcome. This continues Brian's original request for a visible general-purpose world; avoid another approval checkpoint for routine implementation choices.

**Reuse and gaps:** native worlds already represent place IDs, authored boundary/passability and rule-governed movement ([location](../src/world_substrate/model.py), [airfield example](../tests/fixtures/airfield-s1-live.json)); engine observation includes colocation ([engine](../src/world_substrate/engine.py)). The newer declared actor-information projection does not automatically apply colocation ([actor information](../scripts/actor_information.py)); compose physical perception, authorization, memory and remote information delivery without erasing remembered or globally known facts. The [composed scene](../scripts/render_composed_living_scene.py) and [native Coordination Hall](https://brianmills.dev/waltzman/world-substrate) already provide illustrated backgrounds, characters, gathering and event effects. The [generic bridge](../scripts/world_scene_bridge.py) currently uses schematic slots and generic assets. Reuse these before choosing another renderer. Place topology is the practical first spatial model; general coordinates, distance, pathfinding, occlusion, travel duration and arbitrary natural-language map generation remain separate, unproven work. Do not claim a general geometric simulator exists.

Saved-round branches preserve rules and complete actor state; older incomplete recordings remain replay-only. Natural-language interventions at forks and natural-language reconfiguration of a saved world's starting conditions remain future features, distinct from creating a new world in natural language. Existing Q36 interpretation limitations remain open. Keep physical space and communication-channel reach distinct for influence operations; preserve the modeling distinctions the investigation depends on.

## Inhabited facility slice — built, reviewed against Smallville (2026-11-13)

Source: Brian's 2026-11-13 continuation request; recommendation above. [Authored facility](../examples/world_authoring/pump-facility-v0.json) (generated by [the builder script](../scripts/build_pump_facility_example.py)): laboratory, corridor and control room, two doors (each two directed boundaries; opening sets both), Ari, Mara, Bo, a pump, and delivered reports. It reuses existing mechanics: door `state` is checked by the move rule, `open-door` and `calibrate-pump` change state, `send-report` appends to the recipient's own log. New: a declared public entity may carry `scope: "place"` ([actor information](../scripts/actor_information.py), spec `information-delivery` "Place-scoped perception with distinct inputs"); an actor then perceives it only from its place, and its context separates current observation (place, who is here, reports delivered from any room), global knowledge (world summary, brief) and optional retained `memories`.

Evidence ([test](../tests/test_inhabited_facility.py), scripted choices, no model call): a closed door refuses Ari ("the door is open" check) and she stays put; after `open-door` the same move is accepted; Bo in the control room does not see the pump or laboratory door, does see the report Ari sent from the corridor, and keeps global knowledge and supplied memories as separate inputs. A real catalog run replays to the same facts (Ari's place and each door's state per frame), and a branch from the door-opened checkpoint diverges (pump calibrated, Ari still in the laboratory) while the parent keeps four rounds.

Review against the Smallville reference (rendered scene, desktop): the existing composed renderer shows three labelled rooms, portraits that move between rooms on accepted moves, door state text and pump state. It is **still short of Smallville**: flat room panels, no floor plan, doors drawn as generic shield icons, no speech or activity bubbles for reports, generic portraits. Conversation is visible only in the event record, not as a scene effect. The phone layout overlaps name tags with door icons, and the player bar is hidden in the embedded view by design. Not built: a LLM-resident run in this world (perception is verified at the context level; resident behaviour is not), free-text conversation (forms carry fixed text; open-attempt mode would allow free text), coordinates, hearing range, occlusion, travel time, pathfinding, natural-language interventions at a fork or edits to saved starting conditions. A saved round in which nobody changes anything is not branchable (existing catalog rule), so a one-round refused attempt needs another person to act in the same round. Next recommended (done below): scene effects for delivered reports and door/room art through the existing renderer's profile, then one paid resident run read in full.

**Scene effects and resident run (2026-11-13, same goal; goal profile continuous-light).** Delivered reports now draw as a message from the sender's room to the recipient's (words shown, since the studio scene is the owner's view), refused moves show a banner naming the check ("the door must be open"), and door and pump use art through the existing profile and composed renderer (no new renderer). The phone layout no longer overlaps; the tradeoff is a tall page (about 3,000 px) with gaps. A resident run ([trace read](../evidence/ui/inhabited-facility-20261113/TRACE_READ.md), six rounds, 18 model calls, measured $0.003268 under the $0.12 World Builder cap) first exposed three defects, fixed and re-run: people were seen from every room, `open-door` was never offered (its form named the unseen far half of the door; forms may now list `unobserved_refs`, and `not_self` removes "tell yourself"), and the stale-revision retry dropped its controller. In the second run all three people open doors, walk between rooms and send reports; beliefs match place (Mara: "I cannot see either room's occupants from here"); Bo weighs delivered reports against his remembered knowledge. One run of one model: not a measure of personality fidelity. Still short of Smallville: flat room panels, no floor plan, generic portraits, one door drawing for both states (state in text). Not claimed: coordinates, hearing range, free-text conversation, fork interventions.  **Second resident run, through the workspace service (same day):** the workspace always reads residents' free-text attempts, and there every "open the door" was refused because the reader's entity list lacked the far half of the door; fixed (`_read_attempt`), then six rounds ran with 15 accepted moves, $0.006423 measured. The run, its server run log, trace read, Bo's verbatim observation, branch and phone screenshots, and the three scene pages fetched from the service's scene route are in [the evidence folder](../evidence/ui/inhabited-facility-20261113/TRACE_READ.md); the earlier direct run is in `direct-harness/`. Human step: Brian views the rendered scene and judges it against Smallville (does not gate the goal).

## Viewer path: Smallville-style scene (2026-11-14)

Source: Brian, 2026-11-14: "on the smallville stuff if it is better then lets just use that. i am not going to resell or distribute anyways ... yes remove the new renderer rule." The rule against a renderer of our own is lifted for a scene viewer (engine, scheduler and cognition limits stand). Survey (researcher agent, primary sources, 2026-11-14): Smallville's front end (`joonspk-research/generative_agents`, Apache-2.0 code, Phaser 3 + Tiled map) replays from `master_movement.json` (step, then person, then `movement` [tile x,y], `pronunciatio` emoji, `description`, `chat`) but is served by Django; the art is three paid packs with no redistribution licence. AI Town needs a live Convex backend; Concordia's map viewer is geographic; Mesa is live-only. Not verified: the character sprite licence, Tiled output licence, AI Town tileset licences.

**Difficulties to settle before building (agent analysis, working default):**
1. **Space.** The substrate knows rooms, not coordinates. A map must supply anchors, door tiles and a walkable layer; paths are computed in the exporter, never in the rules.
2. **Generality.** The World Builder makes arbitrary worlds; most have no rooms (supply chains, countries). The viewer applies to spatially inhabited worlds only, so it is a second scene beside the composed one, chosen per world. A hand-drawn map fits the facility; other worlds need a layout generator from the place graph, which is separate, unproven work.
3. **Time.** A round is a set of ordered commits; Smallville steps are fixed-length with one tile per step. The exporter expands each round into walking steps and keeps a round-to-step index so checkpoints and branches select the right step.
4. **Objects and doors.** Smallville has no door or object states; entity component values (door open, pump calibrated) need a sprite or tile mapping authored in the scene profile.
5. **Activities and bubbles.** Emoji and labels come from authored per-action presentation, not inference. Smallville chat bubbles assume co-located speech; delivered reports across rooms need a new effect.
6. **Perception.** The viewer is the owner's all-seeing view; public share scenes must not show what a viewer may not see.
7. **Evidence.** The replay file must be derived from a real run's events by a tested exporter, never hand-edited.
8. **Integration.** The workspace is a static page plus API; the viewer embeds as a scene route and must work at 390px, which Smallville's desktop canvas does not.
9. **Art licence.** Smallville's art is for private use. The public World Builder and its share pages are public sites, so owner-only studio scenes may use it, public scenes need a CC0 tileset (for example Kenney) behind the same map; keep the tileset swappable.

**First slice (spike):** export the existing facility run to Smallville's replay shape on the Ville's own map (our three rooms mapped to three existing Ville areas), run its front end locally from the file, and view it at desktop and 390px. This proves the data path before any map authoring or layout generation.

**Spike result (2026-11-14):** `scripts/export_smallville_replay.py` ([spec](../openspec/specs/scene-viewer/spec.md)) exported the six-round workspace resident run as a 91-step Smallville replay on the Ville's own dorm rooms (laboratory = Maria's room, corridor = common room, control room = Klaus's room; walks 12 to 18 tiles by breadth-first search). Smallville's own front end (Django 2.2 under Python 3.9, run locally from a clone outside this repository) played it: three walking people with activity emoji (wrench, door, walking, speech) in the real tile map; viewed at 1280px. Found: no door drawing or door state (carried in text only), report text is not shown (only the speech emoji), everyone sent to the same room anchor stacks on one tile, the black patches are the Ville map's own unpainted interiors, and at 390px the fixed 1500x800 canvas shows the wrong region (no mobile layout). Smallville's art stays out of this repository (private use only).

**Static viewer (2026-11-14, Brian chose option A):** `viewer/smallville/` ([spec](../openspec/specs/scene-viewer/spec.md)) plays the export from static files (Phaser 3, no Django). Run `python3 scripts/setup_smallville_viewer.py <clone>` once (copies the map and sprites, git-ignored), export with `scripts/export_smallville_replay.py`, serve the folder, open `index.html` (`?replay=scripted` for the refusal run, `?step=N&paused=1` for a step). Fixed from the spike: doors drawn closed or open on the doorway tiles found by the exporter, the refusal reason and the report's words are readable, people sharing a room stand on different tiles, the facility fits desktop and 390px with labels enlarged when zoomed out. Viewed from the scripted refusal run (step 1: Ari refused at the closed laboratory door, Bo's question to Mara as text) and the resident run. Remaining: a report bubble clips at the phone's right edge; tile coordinates come from one hand-chosen mapping of three dorm rooms (a general layout for other worlds is unsolved); not embedded in the workspace; the owner-only studio may use Smallville's art, public scenes need a CC0 tileset.

**World layout declaration (2026-11-14, Brian: "i approve c then b then a", step B):** a bundle may now declare `layout` ([spec](../openspec/specs/scene-viewer/spec.md), `scripts/scene_layout.py`): a prepared map, a map slot per place, the two places each door joins, and each person's start and sprite. Two prepared maps exist in `viewer/maps/maps.json` (the Ville dorm, a common room with four rooms off it; Oak Hill College, a hallway with a classroom and a library). The pump facility declares its own layout and the exporter reads it; the two earlier replays reproduce byte for byte. The same run also exports on the college map (`replay-college.json`, `?replay=college`, viewed at 1280px). Still open: the World Builder's prompt does not yet offer layouts to the model (needs a deploy and a free scripted check first); worlds needing more rooms than a prepared map has fall back to the flat board; embedding in the workspace is step A.

**Owner run viewer (2026-11-14, step A; Brian viewed the page: "yes looks good"):** `scripts/open_scene_viewer.py` opens a saved run in the map viewer on the owner's machine (reads the run from the service with the owner password or from a run-log file, exports with the world's layout, serves `viewer/smallville/` on localhost). It is deliberately not part of the public workspace page: the art and map data are private-use, so nothing of them is deployed. Public scenes still need a free-to-use tileset. Checked with a run log carrying the pump facility layout, viewed at 1280px (step 40: two reports shown as text).

**Public generated map (2026-11-14, Brian: "build the public one"; slice 1 of 2):** `scripts/generated_map.py` makes the room map from code (a hub with up to four rooms off it, two-tile door gaps, furniture) and the viewer draws it with Kenney Tiny Dungeon tiles (CC0, `viewer/smallville/assets-cc0/`, licence note beside it), so nothing of Smallville's is needed. Prepared maps `public-hub-3` and `public-hub-5`; `?replay=public` shows the pump story on the first (viewed at 1280px). Slice 2 (2026-11-14): `GET /share/<id>/replay` returns the shared run on a generated map (a private map in the layout is swapped for the generated one with the same room count; no layout, no map), report words withheld from non-owners; the page `/world-builder/room-map/?share=<id>` is in the Cloudflare pages build and the shared-run view links to it. Rules overlay (Brian, 2026-11-14, "i approve"; computer only): "Show rules" tags on doors and in the margin, blue allowed / orange refused with the failed check, click for the full rule; second demo `?replay=resident` (6 rounds, words withheld), both built by `scripts/build_public_demos.py`. Layouts for new worlds (Brian, 2026-11-14, "i approve"): a small optional call after the build proposes the layout (`scripts/layout_proposal.py`; $0.0002 a call measured). Was open: the builder prompt does not yet offer layouts, so only worlds with a layout (the pump example) get a map.

## World workspace — current approved implementation (2026-11-13)

Brian requested natural-language creation as the starting page, all created worlds in a library, play/replay/branch controls and the existing spatial/visual world view. He selected completed saved-round branches first. Implementation is integrated locally: private owner SQLite catalog, exact native checkpoint hydration, independent branch lineage, creation-first library and primary composed spatial studio. The actual HTTP/SQLite/native scripted-engine browser walkthrough passes 27/27 on desktop and 390px, with exact branch cognition/snapshot and parent immutability checked; focused home/scene checks pass 41/41 and two additional actor-role browser checks pass. Independent review findings were corrected, including stopped-checkpoint eligibility and distinguishing actor selectors from literal category names. PR394–396 are merged. Frontend and backend are deployed at `aadccb5dd460618d96de702ae3c554dd5855026e`. The release gate passes 1,134 tests, 2 skipped and 229 subtests; all 14 capability specs validate. The final public player passes 41/41. Actual owner-library search/open/scene checks pass at desktop and 390px with all API responses 200, no JavaScript errors and no API mutations. Historical recovery completed additively. [Release evidence](../evidence/ui/world-workspace-20261113/delivery.json). [Evidence](../evidence/ui/world-workspace-20261113/). Existing incomplete historical recordings remain replay-only, without invented actor memories or lineage.

Natural-language interventions at a fork and natural-language configuration of a saved world’s starting conditions are explicitly future features, distinct from creating a new world from language. See [product scope](../PRODUCT.md), [design](../DESIGN.md) and the archived OpenSpec world-workspace change. No new engine, scheduler, renderer or cognition system is authorized.

## Saved-run player — approved implementation (2026-11-13)

Brian approved rebuilding the viewer after the independent usability review. The retained six-round run now has a paused player with direct round/event selection, playback through every retained event, event-specific world state and contextual actor input. Historical cause selection restores that event’s state and brings its detail into view. Phone composition uses a readable event picker; the retained round scene, full network and exact evidence remain available deeper. [Design](../DESIGN.md), [browser and review evidence](../evidence/ui/saved-player-20261113/). Local browser 38/38 and 31 home tests pass; code and task walkthrough reviews pass after diagnosed corrections. PR392 merged; frontend and backend deployed at `0496afefeecbd90e43c13e4f0be1093bbd2616b9`. The final public browser check passes 41/41 with no page errors or unexpected failed requests; all stored rounds, actor inputs and world fingerprint equal the retained recording (`evidence/ui/saved-player-20261113/live-browser/checks.json`). No new simulation or model call.

## Latest run to inspect — six rounds (2026-11-13)

[Open the fresh autonomous run](https://brianmills.dev/world-builder/?run=T-e9dYLdIi61). Start with Bo in round1, then round2: he explicitly says he is not assenting, the interpreter records assent anyway, and he notices and withdraws it. The inversion repeats in rounds3/4. This is a serious Q36 defect, preserved rather than hidden by a replacement run.

Ari repairs in round2 and revalidates in round3; public validation passes and the technical hold clears. Mara and Bo end concerned/non-assenting; Ari supports and assents but has weight0. Required assents0, pumpinactive. All actors know the initial public failed-validation hold; only Ari has private sensor details, Mara has the short report, and Bo lacks that private report. No voluntary technical evidence report was chosen; send-report is absent from resident known-action lists, limiting interpretation of that absence.

Executed current deployment b3823f6. Fresh generation plus six autonomous rounds:51nativecalls,228960tokens,measured$0.125753265,181.641821237seconds. The original authoring candidate failed review; the existing repair path produced the adopted candidate. The review's individual objections are retained as judgments, not treated as proven leaks. [Full trace and limits](../evidence/i0-i1/visible-run-20261113/TRACE_READ.md). Eighteen native actor inputs/outputs and twenty continuation comparisons match. Scientific or general semantic fidelity is not certified.

## Run inspector display correction (2026-11-13)

The existing Analyst view now shows Original words, Interpretation and Result together when an attempt square is selected under Why things were refused. Grounded fields, quoted bindings, unmatched nearest-move/reason and exact recorded changes stay distinct. Open the six-round recording above and select Bo in round1 to see the retained negation error directly, without opening JSON. Actor context hides this analyst evidence.

Q26/G17 closes on saved S1 accepted/refused/unmatched rows plus the pump recording at desktop and phone widths (`evidence/open-attempt/attempt-inspector-ui/checks.json`); no new model call or simulation. PR389 is merged and deployed at `f43846fa60cedbb50af754903d736c74d1120b2e`. Local browser78/78 and live77/77 checks pass; live rounds, actor inputs and world fingerprint equal the retained recording (`evidence/open-attempt/attempt-inspector-ui/live-checks.json`). The original recording remains unchanged. S1 still owes A2/A3 and the complete A1/A4 demonstrations retain their separate requirements.

## Delivered polarity and authority correction (2026-11-13)

Brian approved fixing the fresh run's negation/authority failures. [PR387](https://github.com/BrianMills2718/world-substrate/pull/387) merged and deployment is verified at `2ab2933e55dfe5c1c58514a3b06e052cdb30c012`, with llm_client 4ee0cf8. [Inspect Bo's unchanged non-assent](https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/polarity-bo.html) and [Ari's authority-object repair](https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/polarity-ari.html). The views display exact original words, quoted field bindings, separate consequences and nine native checks. The original autonomous recording above remains unchanged.

The existing interpreter now preserves full operation polarity/negation scope and distinguishes a person from their owned role or object. It receives visible public examples through the same actor_page projection as the actor; hidden singleton/derived fillers and unseen form descriptions stay out. No extra model stage or new engine is added. A world without a record-non-assent action keeps that attempt unmatched/no-op rather than recording positive assent.

Evidence:9recorded-policy cases,11nativecalls,measured$0.006166675,60645tokens,0tools/retries/errors. Both retained negative-assent attempts leave Bo false through the existing judge; Ari's exact repair uses technical-role-ari. Positive assent/withdrawal/concern, uncertainty, quoted negative report content and a wrong owner's authority retain their meanings and mechanical checks. Independent input/replay/raw-hash checks pass;58browser checks pass at1440/390. Normal release check1100passed,2skipped,229subtests,13 specs. [Full trace and limits](../evidence/open-attempt/preserve-operation-polarity/TRACE_READ.md). This is bounded interpretation evidence, not a new autonomous run or general semantic proof. Q36 remains open beyond these cases; existing phone scene overlap is retained.

## Delivered actor information and one concern (I0/I1)

Source: Brian's approval and activated I0/I1 goal, 2026-11-12, after documentation PR #378. The documentation-only hold was lifted for these slices only. **I0/I1 are delivered, technically verified and unjudged by Brian.** [Open the actual two-round recording](https://brianmills.dev/world-builder/?run=q88DLJnu6w-l); [read the retained trace and limitations](../evidence/i0-i1/deployed-integration-5/TRACE_READ.md). The generated/resident run used `9a8cf47`; the final state-display correction is deployed at `a17406390325f0b485b62f5fc0d564c73de70706`. Prior failed attempts and before-fix screenshots remain preserved.

Ari alone receives C/8/V17; Mara receives the short report with an explicitly unspecified source; Bo sees the authorized public hold without that report. Both policy paths use declared inputs, and continuation seals bind actor-owned history. Actual condition, historical report, expressed stance, recorded assent and hold remain separate. All actors can record a position; only the required actors count toward activation. Ari's repair and revalidation clear the technical hold without supplying consent. The recording ends with zero assents and no activation. Recorded immediate reactions now appear in both state displays.

Evidence: 18 fully read native calls, six exact input/output matches and four exact continuation checks; measured run cost $0.05697485. The release gate passed 1,066 tests, 2 skipped and 229 subtests. Saved-world/build replay retained 28 worlds with no errors or lost working worlds. Independent focused reviews and publication scans passed. [Acceptance entries](../docs/planning/open-attempt/acceptance-criteria.json) are built, with no invented human verdict. This does not validate real-world persuasion or every natural-language reading: Mara's compound dissent did not commit a stance, and Q36 retains that counterexample. New reports, positive assent, stance commits and activation were unchosen here, with their rule checks recorded separately. No Jev, solver/cognition framework or unrelated judge work was added.

## Delivered whole-attempt correction (Q36)

Source: Brian,2026-11-13,“i approve proceed”. [PR384](https://github.com/BrianMills2718/world-substrate/pull/384) merged at `b3823f60b378450279ac3d096db5ee27117fa873`, now deployed on the backend and page with llm_client `4ee0cf800587598672dfacfed99ea2954c2e01e6`. [Read the retained evidence](../evidence/open-attempt/whole-attempt-coverage/TRACE_READ.md); [inspect safe compound rejection](https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/coverage-compound.html) and [Mara's separate concern recording](https://hive.brianmills.dev/plans/world-substrate/main/proposals/open-attempt/review-page/coverage-mara.html).

Fresh interpretations assess whole-attempt coverage in the existing call. Concrete means differ from goals; stance differs from assent. Incomplete, invalid or unread assessments execute no part, invoke no judge and deliver no request. Both actor information modes receive constant safe clarification; complete missing-rule requests retain their route. Historical readings remain unassessed. No sequencer or model stage was added.

Evidence:1097tests passed,2skipped,229subtests;13 specs. Saved worlds28,0errors,0lost;12browser scenarios/40assertions with console/network/page errors0. Independent code and bounded contract reviews pass; both packages validate, with the existing conditional comparison, future system map and nightly coverage pending. Three native interpreter calls cost measured$0.00097666: Mara's exact words bind state-concerned, repair stays repair, and true compound wording detects two acts but omits required quote evidence and safely rejects. Model-free restored-world replay commits only Mara's stance; it is not a fresh resident-policy run. Q36 stays open for general semantic accuracy. Existing phone scene clipping remains; essential clarification and state changes below the stage are readable.

## Pre-implementation review and AES adoption (2026-11-12)

**Follow-up design disposition:** Brian approved resolving the remaining contracts and challenging the architecture across influence, program and physical processes. Q76/Q83/Q84 now have selected conceptual contracts in the AI-judge and estimate plans; their J4/E1/E5 implementations and adequacy evidence remain unbuilt. Six conceptual closures across the two reviews leave 43 open questions and 53 resolved. No simulator implementation is authorized by this documentation change.

**Recommendation and order:** first design the complete actor-input boundary (including summaries, briefs, memory and recent events), then carry one concern through distinct condition, claim, stance and institutional hold. This prevents information leakage and forced persuasion before expanding scenario breadth. Keep explicit scenario assumptions rather than promising general scientific fidelity. Program and physical adapters remain conditional on a concrete investigation: use existing hosts under the shared process contract, not a new native engine. The [three-process examination](../docs/model/modeling-choices.md#architecture-challenge-across-three-kinds-of-process) explains the alternatives, limitations and tradeoffs.

**AES interpretation:** the earlier 344 findings comprised 137 missing requirement annotations and 207 missing scenario markers, not 344 demonstrated behavior defects. Scan roots now include the actual script, spike and reference-world owners. Only directly checked existing tests gain links; incomplete consent, read authority, uncertainty, aggregate spending and storage durability remain explicit gaps. Current receipts supersede old counts. The eight arc42 format findings are resolved with truthful headings, lineage and a distinct documentation-locality citation; no runtime guarantee is inferred from their closure.


The first reconciliation covered current architecture, accepted decisions, four active plans, their packages and all 49
previously open questions. At that checkpoint three conceptual questions were resolved (Q63, Q73, Q75); 46 remained because the
ledger also tracks known defects, unbuilt contracts and empirical evidence. An open implementation item is
not an undecided design principle. The follow-up above resolves credential representation
(Q76, J4), estimator dependency selection (Q83, E1), and observation-estimate placement (Q84, E5). Their
implementation/evidence gates remain; conceptual resolution is not a claim of delivered behavior. Do not require fabricated closure before building the evidence it needs.

AES currently means Lockstep plus the feedback and policy layers. The approved one-tool design keeps
OpenSpec, installs Lockstep from AES canonical, and retains Company Planning's substantive review workflow.
The legacy `aes` CLI and `.aes/target.yaml` are not the adoption target. [Lockstep configuration](../lockstep.yaml)
declares the normative-document/specification scope; Claude/Codex hook entries and a lefthook command are
configured. Runtime files are not yet covered by that layout, and this review does not claim installed git-hook
execution merely from a configuration file. The existing global hook chain remains unchanged.

`make planning-check` checks source attribution, the four plan acceptance files, and
OpenSpec; it is now part of `make check`. `make lockstep` additionally exposes the whole-tree/trace checks.
The reviewed trace check at PR #377 reports 329 missing requirement-to-code/test links (128 requirement annotations and 201 scenario markers). Its blocking configuration is
preserved; full trace conformance is not claimed. Q77 owns the remaining compliance gap. Plan-format checks,
substantive review and complete runtime traceability are separate claims.

The documented design defaults preserve actor-owned choices, norms distinct from constraints, explicit
estimate semantics, scenario-specific skill/price assumptions and first-principles adequacy before empirical
comparison. Remaining behavioral, performance and implementation questions retain their closure evidence in
the [ledger](../docs/planning/open-questions.json). Checks and cold-review reports bind their own revisions;
this paragraph does not declare universal optimality or predictive validity.

The rule-source review exposed two remaining evidence risks under Q77. Budget admission reserves the remaining allowance and rejects an unreadable ledger, but this does not establish a hard aggregate cap across all downstream model calls, concurrency and late hedges ([service budget boundaries](../scripts/world_builder_service.py), [reviewed trace contract](../docs/model/trace.yaml)). Separately, `_record_response` catches log-write failures and continues the request; a successful response therefore does not guarantee a retained run record. Storage-failure durability remains unmet, and stronger spending guarantees remain unverified. Neither is closed by updating the source-review date; implementation or focused evidence must resolve them before those stronger claims are made.

## Active documentation completion checklist

Source: Brian's November 12 documentation-only goal, following PR #377. This section owns progress for that goal; implementation remains on hold. The completion criterion is coherent, reviewable contracts and explicit residual uncertainty, not closing implementation defects on paper.

| Authority / source class | Disposition and remaining work | Completion evidence |
| --- | --- | --- |
| Accepted decisions, arc42, ODD, DOMAIN and METAMODEL | Keep their scoped authority; reconcile promises against the selected heterogeneous-model and information boundaries | No contradictory current promise; expressibility, integration and adequacy distinguished |
| Modeling choices and conceptual glossary | Update the complete actor-input contract and concrete single-concern scenario; verify JEV/System 1 and conceptual source qualifications | End-to-end asymmetric-evidence example, cross-checked against credentials and physical sensing |
| Active AI-judge, estimate, declared-laws and open-attempt plans and OpenSpec specs | Update only affected requirements, dependencies and acceptance examples; preserve built/unbuilt distinctions | Each proposed change has an owning slice and reviewable outcome; no implementation claimed |
| Question source and generated ledger | Review every open item; retain known defects and evidence needs with classification, owner, dependency, closure evidence and revisit trigger | No agent-resolvable conceptual blocker left undispositioned; no fabricated empirical closure |
| Source manifests, lineage reviews and retained run records | Keep as source/historical evidence; current recommendations cite successor decisions where they differ | Claims trace to sources; historical evidence is not rewritten into a new result |
| Planning packages and generated review pages | Regenerate from owning sources after contract changes; preserve historical evidence and pending judgments | Focused validators, substantive independent review and live final-candidate page verification |
| Current AES documentation requirements | Reconcile current sources and justified links; retain runtime conformance gaps | Report documentation findings separately from missing traceability and behavioral defects |

Design and question-disposition increments complete at fdca8f4; independent second review passed with no remaining substantive blocker. Current increment: final evidence metadata, focused checks, merge and hosted-page verification. Implementation remains on hold. No paid runs or feature work belong to this goal. After three substantive increments, compare progress with this outcome; broad review is bounded to two rounds, with later repair tied to concrete findings.

## Outcome and success criteria

### End goal

Build a **generatively authored, reviewable, persistent simulation platform for plausible worlds**. A person describes a bounded world in plain words; the system compiles its structure and executable law; the person can review the important assumptions; residents and processes inhabit the world under the installed rules; and the person watches and questions the result through a live view.

> **Generative worlds with executable laws.**
> Generative-World Builder on top; rigorous causal world engine underneath.

Why rules rather than an AI judge: scale. Brian, 2026-11-09, quoted in full in [arc42 section 1](../docs/architecture/arc42.md#architectural-thesis): facts must carry their implications and blockers down causal chains far longer than a model can follow.

### Actor, recurring job and investment boundary

- **Actor:** a World Builder visitor (or Brian as owner) at <https://brianmills.dev/world-builder/>.
- **Recurring job and baseline:** the visitor describes a situation in plain words, presses Create simulation (which is the approval), and watches the generated people act under the installed rules. Today each person picks a move the rules offer or writes an open attempt in their own words (S1); same-moment knock-on chains run inside one commit (S2); skill-shaped failures never appear because skill rolls are not built (S3).
- **Inspectable result:** the run page and its build record: what each person tried, what the rules did and why, every event with its cause; a share link replays the run for free.
- **Stage and investment boundary:** prototype stage; this repository and its own deploy only; visitors share $3.00 a day and the owner has $5.00 a day (`scripts/world_builder_service.py`); new paid builds under the declared-laws plan follow the plain-version comparison (Q60); no new service, engine or repository without Brian's yes.

### Causal product contract

A World Substrate causal claim explains why a transition occurred **inside the represented world under the installed mechanics that governed that run**. It is not, by itself, a claim that those mechanics are true of the real world; predictive validity and real-world causal identification need separate evidence. `causal_parent_event_ids` are mechanic-declared and validated against retained history, never inferred from temporal order or from what a resident was shown. The Waltzman adequacy report is a bounded dependency inventory with residual risk, not counterfactual proof.

### Current showcase world — Waltzman Coordination Lab

Rand Waltzman's bio-surveillance coordination scenario (*From Minds to Coordination*) is the showcase. It builds through the people-world path (`scripts/people_world.py` and the scenario-spec pipeline in `spikes/any-scenario-2026-10/`), declares laws over the counts it keeps and gets the same rules review as a world of things (#314). The hand-authored Waltzman reference world (`reference_worlds/waltzman/`) remains the regression fixture for the living-view and causal semantics. The [lineage review of 2026-11-07](../docs/audits/waltzman-lineage-review-2026-11-07.md) found the generated Waltzman world stipulates some of what the paper's mechanisms should produce; its recommendations are not adopted (Q60).

### Prototype phase — complete

Persistent typed canonical state; bounded observations and state-derived affordances; scripted, human and LLM selection outside consequence authority; semantic/mechanical separation; reviewed frozen profiles; atomic commit or refusal with write-scope enforcement; retained causal evidence; transfer to materially different worlds (Castaway, Kitchen, Workshop, Greenhouse, Orchard, Repair Bay, Waltzman).

### Waltzman demo acceptance criteria

The 2026-09-09 stakeholder promotion met ten criteria through the reference world plus the donor authoring path: a living view driven by canonical snapshots and events; represented information with source, recipient, channel and visibility; residents acting through the policy seam; outcomes depending on represented resources and institutions; one simulated timeline; inspectable causality with information kept apart from causal parents; detachable Waltzman analysis; an exact-history intervention fork; a bounded dependency report; and one continuous public experience. Evidence: [promotion record](../evidence/waltzman/public-promotion-2026-09-09.md). Saved user worlds, persistent cognition, generic scheduling and predictive validity were outside that gate. The separate human world-only review of `evidence/renders/waltzman-living-v1.html` (Company Planning #222) has no recorded answer; `evidence/waltzman/m1-acceptance-candidate-v1.json` still reads `pending_human_world_only_review` at tested revision 27164359.

## Canonical outcome probe

The steps a visitor takes end to end, which every plan's outcome step names one of:

1. Describe a situation in plain words on <https://brianmills.dev/world-builder/> and press Create simulation.
2. The builder generates the world (places, things, people, the moves they may attempt), its declared laws and its rules; a second model reviews the rules; a free scripted test checks that something can happen.
3. The residents act each round, and the installed rules decide each effect: accepted, refused with the failing check, or changed state that later rules react to.
4. The page shows the run round by round, with each event's cause and the build record.
5. The visitor reads why things happened, follows a cause back, and can replay the saved run for free.

Fixtures with narrower roles: M1 Castaway freshwater (the neutral substrate baseline with exact replay), Kitchen (replicated watched-world behavior), Greenhouse (new-world presentation), Orchard (live authoring acceptance), Repair Bay (first nontrivial deployed authoring world), Warehouse Rush (a law/representation omission and its repair), and the Waltzman reference world.

## Current truth

State, not narrative. Code paths are the evidence; the [arc42 building blocks](../docs/architecture/arc42.md#5-building-block-view) map each one.

- One `World` owns canonical truth. Prompts, page state, residents' memories and analyses are not alternate authorities.
- Write scopes are enforced. Declared read scopes are recorded, not enforced; the project check reports `read_scopes_enforced` as a constant (Q34, Q66).
- Write-scope placeholders are bound to participants, not to one specific action role (Q67).
- A world's declared laws are checked at every commit; a step that breaks one is refused and names the law (`src/world_substrate/laws.py`). People worlds declare laws too (#314).
- An independent rules review by a model of another family (chosen as gemini-3.1-pro-preview in `evidence/declared-laws/s3-review-choice/`; the route is `openrouter/google/gemini-4-argon` since #341, `scripts/review_rules.py:18`) runs on every kept try; an unreviewed try ranks below every reviewed one.
- Open attempts (S1): an interpreter reads a resident's words into one typed move or leaves it unmatched; an unmatched attempt changes nothing except a request to another person, which is delivered to that person (#326).
- Same-moment knock-on effects (S2): `timing: immediately` processes settle in waves inside the one commit. Since the AI judge plan's J0 (2026-11-10) there is no cap: each (process, entity) pair fires once per moment, so 50 chains of 100 links finish in one moment; every step names its cause, a step a failed check stops is shown with its blocker, and runs recorded before J0 replay under their old cap of 32.
- Residents run on Concordia since 2026-10-16 (`scripts/concordia_residents.py`). Since the AI judge plan's J2 (2026-11-10) the Concordia game master (`EventResolution`, `scripts/judge.py`) is on only for attempts no rule covers; since J3 (2026-11-10) a confirmed ruling becomes a rule: installed at once, or held until the owner approves it, per the world's setting `Judge rulings during a run` (`scripts/rulings.py`).
- The Decision 008 agent harness (`scripts/world_harness.py`) exists but the live service does not call it (Q14).
- The people-world path imports code from `spikes/any-scenario-2026-10/` at run time (`scripts/people_world.py:26,76-77`).
- The mechanic profile id does not include a compiler or interpreter version (Q69); the 256-move discovery cap truncates silently (Q69); a mechanic that raises mid-rule is rolled back and re-raised, not recorded as a refusal (Q69).
- About fourteen hand-written build checks still run, each added after one bad world; none has been retired by declared laws yet (Q45).
- Rules default to `openrouter/openai/gpt-6-luna`: re-measured on 2026-10-23, 23 of 24 builds reached their finish line and 19 of 24 were also faithful, at $0.0032 per build ([trace read](../evidence/luna-rules-2026-10-23/TRACE_READ.md)).
- The World Builder page is one box and Create simulation (Brian, 2026-10-15); live play goes one round per request and pauses at a finish line, after 4 quiet rounds, on an error and every 100 rounds; builds and runs are background jobs because Cloudflare cuts requests at 100 seconds; share links store and replay runs.
- Deployment: pages on Cloudflare Worker `world-builder-pages`, API edge `world-builder-api`, service container on the personal VPS since 2026-10-05 (binding `0.0.0.0:8813` inside the container, `LLM_CLIENT_TIMEOUT_POLICY=ban`); up to four AI jobs at once. All public pages answered HTTP 200 on 2026-11-09.
- Scheduling is integer ticks; `Engine.advance()` checks each process with `due(world)`; World Builder processes run `each_round` or `immediately`. No future-event queue exists.
- deck.gl is loaded only by the Waltzman reference client (`scripts/render_waltzman_demo.py`); the World Builder draws its network with the vendored graph viewer. Pydantic AI, SimPy, Cytoscape.js, PettingZoo and Mesa are not used in `src/` or `scripts/`.
- The native coordination vertical, one-shot authoring and run comparison are on main since 2026-10-05 (#75, #79, #80); `scripts/check_native_coordination.py` passes for two worlds on one shared profile with no provider spend.
- Semantic binding: six of seven M1 action kinds cite a reviewed Linguistic Core sense; `unheat` is deliberately unbound. Kitchen and Greenhouse events can carry Castaway mechanic ids because binding is by bare action kind (Q64).
- No hosted CI: `.github/workflows/native-coordination-linux.yml` was removed on 2026-11-10 (Q70, Brian approved); `scripts/check_project.py` already ran every command it ran and gates each merge through `ship`.

## Applicable context

- [arc42](../docs/architecture/arc42.md): goal, requirements, constraints, source dispositions, building blocks, deployment and risks.
- [Capability specs](../docs/index.md#2-what-the-code-must-do-openspec-capability-specs): transition engine, rule authoring, mechanic installation, authoring bundle, semantic binding, information delivery, live projection, scenes, native coordination and the World Builder page.
- [System model](../docs/model/ODD.md) with [trace.yaml](../docs/model/trace.yaml): each enforced rule, its owner and its test.
- [Open questions](../docs/planning/open-questions.json) and the [planning package](../docs/planning/planning-package.json).
- [Lessons](../docs/wiki/lessons.md): read before planning a goal.
- [Flexible simulator prior art](../docs/research/flexible-simulator-prior-art-2026-10.md), [competitive landscape](../docs/research/competitive-landscape-2026-09.md), [technology procurement](../docs/research/technology-procurement-2026-09.md).

## Constraints and authorities

```text
plain-language description  (Create simulation = approval)
  -> authoring bundle (structure, declared resources and laws) + causal model (rules as data)
  -> local compiler derives authority; independent rules review; free scripted test
  -> frozen mechanic profile
  -> resident move or open attempt (Concordia) OR process trigger
  -> Engine checks + one commit/refusal + same-moment knock-on waves + declared-law check
  -> canonical state + causal events + run log
  -> read-only views (round feed, Network, build record, share-link replay)
```

Hard constraints:

- policy or model prose cannot mutate canonical state;
- a mechanic cannot enlarge its own write authority;
- generated source code is never a causal-law fallback;
- analysis cannot rewrite history or duplicate primitive effects;
- presentation is downstream and read-only;
- resident harnesses choose attempts and utterances but never adjudicate consequences;
- information delivery and context never become hard causal parentage automatically;
- causal claims about the represented world are not marketed as real-world causal truth;
- the adequacy inventory is not marketed as counterfactual proof;
- no engine, scheduler, renderer or cognition capability of World Substrate's own (Decision 006); a bounded same-moment fixpoint inside the existing commit does not count (Decision 009).

## Vertical slices and current work

### Milestone horizon

| Milestone | State | What it establishes |
| --- | --- | --- |
| M0 to M7b substrate and generative mechanics | complete | persistent governed world; authoring, compiler and policy seams |
| Kitchen, Greenhouse, Orchard, Repair Bay | complete first gates | watched-world behavior, portable replay, live generated-law authoring |
| Waltzman reference world and stakeholder demo | promoted 2026-09-09 | living projection, information, intervention fork, bounded adequacy; donor-backed public demo |
| Native coordination vertical | landed 2026-10-05 | #75, #79, #80 |
| Replacement-first gate | recorded 2026-10-05 | Concordia, Mesa, PDDL compose; none replaces the governed-rules layer |
| Natural-language World Builder | live since 2026-10-05 | one box, Create simulation, live play, share links |
| Concordia residents | live since 2026-10-16 | AI residents through an established framework |
| Open attempts | S1 and S2 built; S3 not built | own-words attempts; same-moment knock-on effects; skill rolls next |
| AI judge ([plan](../docs/plans/ai_judge.md)) | J0, J1, J2 and J3 built 2026-11-10; Q96 exchange consent before J5; J4 exploration only | knock-on chains of any length; an AI judge (Concordia's game master) rules only on what no rule covers, from the engine's consequence report |
| Declared laws | S1 to S3 built; S4 under way; S5 follows the plain-version comparison (Q60) | worlds declare laws, the engine keeps them, a second model reviews the rules |
| Estimate rules | plan 2026-11-10, package compliant (#366); nothing built | a rule's outcome can depend on a chance Jev estimates from named facts, rolled, recorded and replayed without Jev; only slice E4 (judge-proposed estimate rules) waits for the judge's J3 ([plan](../docs/plans/estimate_rules.md)) |
| Hardening | queued | law fingerprint with compiler version, role-bound scopes, visible discovery overflow, recorded mechanic exceptions, locking |
| Persistence and second-domain proof | split | private owner world/run catalog and spatial workspace deployed; exact branch state and replay verified; scientific proof beyond Waltzman remains later |

### Active slice

Current task: preimplementation readiness review.

Source: Brian, 2026-11-12: "before we move to implementaiotn ... make sure all our normative docuemtnationa nd plans are optimal and that all open questions have been resolved ... maybe get complaint with the new aes canonical system". Reconcile the actual current standard, authoritative documents and every question before resuming implementation. A resolved design decision is not evidence that its code works. Questions requiring implementation, calibration or scale evidence stay explicit with closure conditions; do not close them to produce a zero count.

The modeling guide’s [biosurveillance application](../docs/model/modeling-choices.md#worked-application-the-biosurveillance-partnership) recommends causal separation for the next social-model slice; it is not an independent implementation authorization or replacement roadmap.

### Previously planned implementation sequence (conditional on this review)

1. **Declared laws S4** ([plan](../docs/plans/declared_laws.md)): let declared laws and the rules review retire the hand-written build checks. Done so far: free replay of every saved world (`scripts/check_saved_worlds.py`), fixes from the S4 live builds (one-way moves kept #309, places and owners shown to the reviewer #310, fields only one thing can fill #312, people worlds get laws and review #314, every kept people try reviewed #317, trades named from one side #319, the round told to each person #320 and #323). Not yet done: retiring any hand-written check (Q45).
2. **Declared laws S5**: live builds of four varied descriptions in parallel. Follows the plain-version comparison (Q60, settled 2026-11-09 by Brian's plain-version rule); one Waltzman rebuild ran on 2026-11-04 on his yes for that build (`evidence/declared-laws/s4-waltzman-3/`).
3. **Open attempts S3** ([plan](../docs/plans/open_attempt.md)): seeded, recorded skill rolls on action mechanics, with the roll's skill path in derived reads (Q33, Q40).
4. **Estimate rules E1** ([plan](../docs/plans/estimate_rules.md)): chance rolls on Jev's estimate, sharing the skill roll's run seed (Q33); whichever of S3 and E1 lands first builds the seed. Brian approved planning it on 2026-11-10.

### Hardening queue

Small reversible changes, none reopening the architecture: fingerprint the exact executable law plus compiler version; bind write-scope placeholders to one action role; make discovery-cap overflow visible; record mechanic exceptions as refusals; enforce or honestly report read scopes; add a lockfile when a dependency enters a reproducible production path. Details and sources: Q34, Q66, Q67, Q68, Q69.

### Deliberately deferred

Automatic counterfactual adequacy verification; always-on read-scope enforcement; persistent resident cognition; a future-event scheduler; saved user worlds and identity; massive or distributed scale. Promote one only when a concrete product or evidence need earns it.

## Decisions and assumptions

### Replacement-first gate disposition (recorded 2026-10-05)

Three executed spikes hosted the governed-rules layer on the constrained-handoff world (`spikes/replacement-2026-10/`; each `run_spike.py` exits nonzero on failure, zero provider spend). Re-run independently before recording: all three exit 0.

| Candidate | What it was asked to replace | Evidence | Disposition |
| --- | --- | --- | --- |
| Concordia (`gdm-concordia` 2.4.0) | agent/game-master loop | its game master drives the run while resolution calls only `Engine.discover`/`submit`: 7 events, world-state sha256 identical to the native run, 11/11 checks. A native Concordia rewrite of the rules is 51 lines of our own code (Concordia ships no rule, check, authority or atomic-commit primitive) and lacks staleness checks, write scopes and compiler validation. | **compose**: use as the resident loop when LLM residents are needed; keep the Engine as sole authority |
| Mesa 3.5.1 | model/agent loop, scheduling, data collection | Mesa loop over the Engine gives the same hash, same events and `Engine.replay()` ok (70 glue lines). A rules-in-Mesa rewrite loses, demonstrated by code: atomic commit (partial write persisted), write-scope enforcement (out-of-scope write went through), recorded cause, rules-as-checkable-data, replay from a recorded log. | **compose** when a world needs grids/networks, stochastic activation or parameter sweeps; not adopt |
| PDDL (unified-planning 1.3.0 + ENHSP) | declaration language / validation / planning | rules translated programmatically to PDDL (4 actions, 30 fluents). The validator accepts the reference plan and rejects the refused approval on the same precondition the Engine refused ("Prerequisite A is healthy"). ENHSP found a different 6-step plan, and the Engine accepted all 6 steps and reached `ready`. Cannot express information visibility, write scopes, causal records, refused-attempt history, open worlds. | **compose**: an export for offline validation and "is the goal reachable" checks; not the runtime or declaration language |

**Result:** no candidate replaces the governed-rules layer, and each can host or check it. World Substrate therefore keeps exactly that layer (rules as data -> compiler-derived authority -> explicit approval -> atomic commit/refusal with recorded cause) and **stops growing its own runtime extras**. Outer loops, resident cognition, scheduling, spatial structure and sweeps come from Concordia or Mesa when a world first needs them; formal validation and planning come from a PDDL export.

**Wrong when:** the first LLM-resident run through Concordia needs a game-master component that writes state outside `Engine.submit`, or more glue than the `CognitionAdapter` path; a Mesa (or other) release ships transactional state with write scopes and per-change history; the PDDL translator needs hand edits for distributed-approval, or the validator and `engine.submit` disagree on any step of a recorded run. Any one of these means re-running the gate for that candidate.

Spike-noted defects to fix in World Substrate itself: a mechanic that raises mid-rule surfaces as an exception rather than a recorded refusal event (listed under Q69 below); the PDDL export's constant order varies with the hash seed (cosmetic, from the library's writer).

### Product and adoption posture

| Layer | Posture on 2026-11-09 |
| --- | --- |
| Canonical state, transition kernel, authority, trace semantics | project-owned |
| Rule language, compiler, declared laws, rules review | project-owned |
| Semantic binding | project-owned profile over pinned Linguistic Core meaning |
| Resident loop | Concordia (integrated) |
| Spatial structure, sweeps, stochastic activation | Mesa when a world needs it (not integrated) |
| Formal validation and reachability | PDDL export (spike only) |
| Live view | vendored shared graph viewer in the World Builder; deck.gl only in the Waltzman reference client |
| Scheduling | integer ticks today; SimPy was selected in 2026-09 but never integrated, and Decision 006 now routes scheduling to Concordia or Mesa |
| Persistence and identity | share links only; commodity infrastructure later |

### Information and causality rule

Keep apart: world interaction (Mara speaks to Ari); information lineage (representation, source, recipient, channel, delivery); cognition context (what a resident was shown); mechanic-declared causal ancestry; and analytic interpretation. Temporal order or prompt inclusion never makes information a hard cause of a decision.

### Adequacy rule

The bounded adequacy report answers which consequential assumptions were inventoried, where they are represented, which rules enforce them and what residual risk remains. It does not prove each dependency necessary and sufficient; that is a deferred research option.

### Semantic-profile rule

Linguistic Core contributes meanings and roles. World Substrate's profile owns only the bridge (specialization, causal classification, bearer, mechanic, limits) and never moves persistence, effects, scheduling, write authority or commit semantics into Linguistic Core.

### Approval and law provenance rule

An approval should point to one exact executable law identity for the run. Freezing the profile is a partial implementation; add the compiler version before user-generated laws become long-lived (Q69).

### Experiment-selection rule

Novel uncertainty: experiment. Commodity uncertainty: research, reason, select. Integration uncertainty: prove the selected adapter conforms. A test runs only when a named decision cannot be settled by argument or prior art.

## Evidence and review artifacts

- <https://brianmills.dev/world-builder/> (live alpha), <https://brianmills.dev/world-builder/play/> (Replay Studio), <https://brianmills.dev/waltzman/> (donor fallback).
- Declared-laws and open-attempt run evidence: every trace read is listed in the [documentation index](../docs/index.md#8-run-evidence); the latest Waltzman build is [s4-waltzman-3](../evidence/declared-laws/s4-waltzman-3/TRACE_READ.md).
- [gpt-6-luna rules measurement](../evidence/luna-rules-2026-10-23/TRACE_READ.md).
- Replacement-first spikes: `spikes/replacement-2026-10/` ([Concordia](../spikes/replacement-2026-10/concordia/README.md), [Mesa](../spikes/replacement-2026-10/mesa/README.md), [PDDL](../spikes/replacement-2026-10/pddl/README.md)).
- Waltzman reference world: `evidence/waltzman/`, `evidence/renders/waltzman-demo-v0.html`, [promotion record](../evidence/waltzman/public-promotion-2026-09-09.md).
- Planning review pages: `hive.brianmills.dev/plans/world-substrate/main/proposals/{planning-package,open-attempt,declared-laws}/review-page/`.

Open pull requests: none on 2026-11-09 (`gh pr list --state open`).

## Risks and needs resolution

| Priority | Risk or open need | Current stance |
| --- | --- | --- |
| P0 | the generated Waltzman world stipulates outcomes its mechanisms should produce (Q60) | settled 2026-11-09 by Brian's plain-version rule: compare against one model given the whole scenario before more repair or S5 |
| P1 | hand-written build checks keep growing (Q45) | retire them only when declared laws and the review demonstrably cover the incident |
| P1 | declared laws can be wrong for the world, or missing (Q48, Q49) | read S4 and S5 builds for counterexamples |
| P1 | the agent harness is not on the live path (Q14) | measure a harness build against the 150 s first-round target (a people build must play its first round within 150 s of Create simulation) |
| P1 | law fingerprint lacks compiler version; silent discovery truncation; unrecorded mechanic exceptions (Q69) | hardening queue |
| P1 | write-scope placeholders are not role-bound (Q67) | hardening queue |
| P2 | read scopes are recorded, not enforced, and the check reports a constant (Q34, Q66) | report honestly first; enforce when a run needs it |
| P2 | live path imports spike code (`spikes/any-scenario-2026-10/`, Q71) | move what the live path needs into `scripts/` or `src/` when next changed |
| P2 | hosted CI conflicts with the no-hosted-CI rule (Q70) | done 2026-11-10 (Brian approved): the project check already ran every test it ran; workflow removed |
| P2 | `schemas/world-authoring-bundle-v0.schema.json` rejects law-bearing bundles (Q65) | fix the schema to match the validator |
| P3 | `unheat` lacks a pinned Linguistic Core sense | upstream semantic gap |
| P3 | no counterfactual adequacy proof; no scale demonstration | deferred |

## Human decisions

Answered (kept as the record): World Substrate is the one canonical project (001); observability required, exact replay not (002); meaning does not imply effects, and richer Linguistic Core roles do not move mechanics upstream (003, 2026-09-12 review); own causal reality and borrow commodity machinery (004); converge the next Waltzman release on native World Substrate (005, 2026-09-18); hold at the governed-rules layer (006, 2026-10-05); describe any scenario (007); build worlds in an agent harness (008); same-moment effects are rule semantics (009, 2026-10-26); Create simulation is the approval (2026-10-15); Concordia hosts residents; gpt-6-luna is the default model, sol only when sharing with Waltzman (2026-10-16); adopt the open-attempt plan (2026-10-25) and the declared-laws plan (2026-10-28); believability is the off-the-shelf people agents' job, no metric, tuned once everything else runs well (Q50, 2026-11-09); when a run stops is a per-world setting, "stop condition should be configurable" (Q12, 2026-11-10; built in PR #356: stop once nothing is changing after 6 quiet rounds by default, or always run every round); a world can also stop after a number of rounds or once a run has spent a dollar limit, "i should be able to stop a world based on budget or number of rounds or a natural langue stopping potin that the judge assesses once we build him" (2026-11-10; round and spending limits built, the plain-words stopping point is R11/A8 of the AI judge plan).

Open: none awaiting Brian. Each question, open or answered, is in the [open questions ledger](../docs/planning/open-questions.json) with what it blocks.

Q16, Q17, Q60 and Q70 were settled by the agent on 2026-11-09 (technical calls, or settled by Brian's plain-version rule); the ledger records each.

## Refresh and reset triggers

Refresh this roadmap when:

- Brian answers a new question in the ledger;
- a declared-laws or open-attempt slice lands, or a hand-written build check is retired;
- the agent harness reaches the live path;
- a hardening item lands;
- any Decision 006 wrong-when condition fires;
- evidence contradicts a current-truth statement.

Replan rather than extend blindly if:

- a view needs to invent canonical facts;
- generated rules routinely need model-written code;
- information and cognition cannot be kept apart without leaking observer truth;
- adequacy work grows faster than useful world complexity;
- an external dependency requires surrendering Engine consequence authority; or
- a feature is proposed for completeness rather than a concrete product or evidence need.

## Exact next action

The approved fresh run and its bounded polarity/reference correction are delivered. Inspect the original autonomous run separately from the labeled corrected-input checks above; do not regenerate a world to hide the original failures or reimplement the same guard. Q36 remains open for further observed meaning errors and unsupported operations. If an investigation needs explicit refusal distinguished from absence of assent, design that represented operation and its exposure rather than inventing it in the interpreter. No new implementation or paid run is authorized by this progress entry. Broader scientific adequacy and the older queue remain open; Q96 precedes J5.

1. **Declared laws S4:** retire the first hand-written build check whose incident a declared law or the rules review now covers, proven on the saved worlds with `scripts/check_saved_worlds.py` and `scripts/replay_build.py` before any paid run (Q45).
2. Before S5's paid builds or more people-world repair, run the plain-version comparison (Q60), with its cost worked out first.
3. In parallel, the hardening queue items that need no paid run (Q66, Q67, Q69).

Do not add engine, scheduler, renderer or cognition capability of World Substrate's own ([Decision 006](../docs/decisions/006-governed-rules-layer-scope.md); [Decision 009](../docs/decisions/009-same-moment-knock-on-effects.md) sets out what does not count).
