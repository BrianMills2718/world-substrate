# View coverage: what each World Substrate view shows of the system model

Status: observed evidence, 2026-10-06. Probes ran at commit `2dd1503`; line numbers are updated to `d18ead6` (#117, which drops no-op moves from the offer), and G1, G2 and G7 were re-checked on `d18ead6` with the same results (the deployed pages at `https://brianmills.dev/world-builder/`, `play/` and `build/` were byte-identical to this commit's sources that day, and the API reported `build_commit 2dd1503`). The two any-scenario views and gaps G12-G16 were added 2026-10-08 at `2e409ab`, probed on the retained Waltzman run (`spikes/any-scenario-2026-10/evidence/waltzman/run/frames.html`) served locally and read in a browser (Playwright).

The model is [ODD.md](ODD.md) and [world_substrate_model.toml](world_substrate_model.toml). This page asks one question per model element: can a person looking at each view see it? Values: **shown**, **partial**, **hidden** (on purpose, with the reason), **missing**, **n/a** (that view is not about this element). The same table is in the model file's `coverage` rows; `tests/test_system_model.py` checks that every row names a declared element and gives every view.

## The views

| View | What it is | Source | Where |
| --- | --- | --- | --- |
| `home` | World Builder landing page: describe, check the rules, approve, watch it run live one round per request | `scripts/world_builder_home.html` | `https://brianmills.dev/world-builder/` |
| `build` | World Authoring Studio: edit every bundle section, generate mechanics, approve, run, native-coordination comparison, full request logs | `scripts/world_builder_app.js` via `scripts/render_world_builder.py` | `https://brianmills.dev/world-builder/build/` |
| `play` | Replay Studio: gallery of retained evidence replays | `scripts/render_replay_studio.py` | `https://brianmills.dev/world-builder/play/` |
| `round_replay` | The picture of a run inside `home` and `build` (iframe `replay_html`) | `scripts/run_authored_world.py:517` -> `scripts/render_scene_replay.py:442` | inside home/build |
| `living_scene` | Living Scene v1 renderer over a live projection | `scripts/render_living_scene.py` | offline HTML |
| `composed_living_scene` | Composed living-scene renderer with inspector; native-coordination runs and comparisons in `build`; agent_ecology3's Living view | `scripts/render_composed_living_scene.py` | inside build; offline HTML |
| `owner_run_log` | Owner-only run-log reader | `GET /runs` (`scripts/world_builder_service.py:532`), `scripts/world_builder_runs.py` | owner password |
| `scenario_replay` | Any-scenario run replay (`frames.html`): a pipeline run converted to a contested-run/v3 trace (`to_trace`) and drawn by the same renderer as `round_replay` | `spikes/any-scenario-2026-10/render_run.py:116` -> `scripts/render_scene_replay.py` | offline HTML in a run folder |
| `scenario_state_panel` | Panel under the scenario replay: per round, the non-clock Engine events (id, rule, status, state changes) and every entity's fields after the round, replayed from `events.jsonl` | `render_run.py:99` (`add_state_panel`), data from `state_rounds` (`:68`) | same page |

Deployed pages come from `deploy/cloudflare/world-builder/build.sh` (home, `play/`, `build/`); the API runs on the personal VPS from `deploy/vps/Dockerfile`. The other public URLs (`/waltzman/`, `/world-substrate-visualization/`) are not built by this repository's `deploy/` and were not checked here.

## Coverage table

| Model element | home | build | play | round_replay | living_scene | composed_living_scene | owner_run_log | scenario_replay | scenario_state_panel |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Description | shown | shown | n/a | n/a | n/a | n/a | shown | n/a | n/a |
| AuthoringBundle | partial | shown | n/a | partial | n/a | n/a | shown | partial (G12) | partial (G12) |
| CausalReview (compiler-derived authority) | partial (G5) | partial (G3) | n/a | n/a | n/a | n/a | partial (G4) | n/a | n/a |
| MechanicProfile (frozen id) | missing (G7) | missing (G7) | missing | missing | n/a | n/a | shown (G7 fixed) | missing (G7) | missing (G7) |
| Approval | partial (G6) | partial (G6) | n/a | n/a | n/a | n/a | partial (G6) | n/a (G14) | n/a (G14) |
| Run (trace) | partial (G1) | partial (G1) | partial | partial | n/a | n/a | partial (G1) | n/a | n/a |
| event `accepted` | shown | partial | shown | shown | shown | shown | partial | shown | shown |
| event `precondition_failed` | shown | partial | partial | partial | partial | partial | partial | partial (G15) | partial (G15) |
| event `stale_revision` | partial | partial | partial | partial | partial | partial | partial | n/a | n/a |
| event `scope_violation` | partial | partial | partial | partial | partial | partial | partial | partial (G15) | partial (G15) |
| event `invalid_action` | partial | partial | partial | partial | partial | partial | partial | partial (G15) | partial (G15) |
| event `unsupported_action` | partial | partial | partial | partial | partial | partial | partial | partial (G15, G16) | partial (G15, G16) |
| process-made changes (`advance`) | shown | partial | partial | missing (G8) | partial | partial | partial | missing (G8) | shown |
| run row `no_action` (waited) | shown | partial | n/a | partial | n/a | n/a | shown | partial (G16) | n/a |
| run row `nothing_left` (lost a race) | shown | partial | n/a | partial | n/a | n/a | shown | n/a | n/a |
| World (state, positions) | partial | partial | partial | partial | shown (G9, G10 fixed) | shown (G9, G10 fixed) | partial | partial (G12) | shown |
| LivingSceneFrame | n/a | partial | n/a | n/a | partial | partial | n/a | n/a | n/a |
| Comparison | n/a | shown | n/a | n/a | n/a | partial | missing (G4) | n/a | n/a |
| RunLogEntry | hidden | hidden | n/a | n/a | n/a | n/a | shown | n/a | n/a |
| BudgetLedger | partial | partial | n/a | n/a | n/a | n/a | partial | n/a | n/a |
| ScenarioModel (`model.json`) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | missing (G13) | n/a |
| CheckReport (`checks.json`) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | missing (G13) | n/a |
| Attempt (`attempts.jsonl`) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | partial (G16) | n/a |
| RuleChange (mid-run rule or ruling) | n/a | n/a | n/a | n/a | n/a | n/a | n/a | partial (G16) | partial (G16) |

Notes on the rows:

- **Refusal events, all views.** The living-scene renderers accept every engine status (`src/world_substrate/living_scene.py:38`) but show feedback only when the scene profile declares a visual for that rule (`living_scene.py:415`), and only check labels and verdicts, never operands (on purpose: operands can be actor-scoped evidence, `living_scene.py:394`). Authored-world views see refusals only through the transcript's `refused_because` check labels (`scripts/run_authored_world.py:375`), never the event itself (G1). Hence "partial".
- **RunLogEntry is hidden from visitors on purpose**: it holds other visitors' worlds and salted client fingerprints; only the owner reads it (`world_builder_service.py:499`).
- **The seven World Builder views never read pipeline output** (no file under `scripts/`, `src/`, `deploy/` names `any-scenario`), so the pipeline-only rows are `n/a` there. The pipeline's own spend cap is `spikes/any-scenario-2026-10/spend.py`, not the BudgetLedger.
- **`stale_revision` cannot occur on the pipeline path**: each resident submits the offered action right after its own `Engine.discover`, and the game master submits at `engine.world.revision` (`midrun.py:91`, `:99`).
- **InformationItem, Delivery and linked process participants** have no row: no view here was probed for them. Information items appear only in hand-authored Waltzman and native-coordination worlds; linked participants only change which entities a process event touches, and their effects reach the views as ordinary event `changes`.
- **BudgetLedger** reaches visitors only as an error message when the day's budget is used up (`world_builder_home.html:288`) and as cost receipts in `build`.

## Gaps

Each gap names what the model says, what the view does instead, the evidence, and whether it was reproduced here. Probe scripts and outputs are in `~/code/.scratch/ws-system-model/` (throwaway; not part of this change).

### G1. Authored-world runs keep no engine event records

- **Model:** every attempt writes one Engine event (`src/world_substrate/engine.py:505`): bearer, binding, observation, checks, declared read/write paths, `changes`, `hash_before`/`hash_after`. Root `AGENTS.md` tells investigators to read "the retained causal trace".
- **Code:** the authored-world run trace (`scripts/run_authored_world.py:405-446`) keeps `summary`, `transcript` and `final_snapshot`; `World.snapshot()` drops commands and events (`src/world_substrate/model.py:416`). The run log keeps the same (`scripts/world_builder_service.py:360-367`). The native-coordination path does keep them (`scripts/run_native_coordination.py:604`, `:1107`), so the two run paths differ.
- **Effect:** no view, and no retained file, can say which state paths an action changed or show the world hash chain for a Builder run; the engine's `stale_revision` event behind a `nothing_left` row is lost.
- **Reproduced: yes.** `run_authored_world.py` on `examples/world_authoring/repair-bay-v0.json` produced a trace with keys `actors, cost_usd, final_snapshot, mechanic_profile_id, model, schema_version, summary, transcript, world`, with no events. A local service run of the same world wrote run-log `/run` results with keys `final_snapshot, mover, summary, transcript`.

### G2. Home "refused" counter counts blocked offers, not refused attempts

- **Model:** a refusal is an Engine event with a non-`accepted` status for an attempt that was submitted. `blocked_by_rules` is something else: the offers `Engine.discover` withheld from an actor that round, one example per distinct (action kind, reason) (`scripts/run_authored_world.py:261-281`).
- **View:** the run headline `Round N · A allowed · R refused` adds up `blocked_by_rules` entries (`scripts/world_builder_home.html:615`, printed at `:553`), while the squares underneath ("Why things were refused") draw one refused square per actor per round (`:518`). Step 3's tooltip says "Every attempt is allowed or refused by your approved rules" (`:111`).
- **Reproduced: yes,** in a browser (Playwright) against a local API with the Repair Bay fixture world: the page said **"Round 5 · 10 allowed · 60 refused"** and drew 20 refused squares. The run log for the same run: 10 `accepted`, 9 `no_action`, 1 `nothing_left`, zero submitted attempts refused by a rule check. The number 60 measures neither attempts nor squares.

- **Fixed 2026-10-06.** The headline and the squares now count through one function (`countRound` in `world_builder_home.html`): *allowed* = moves that went through, *refused* = moves someone tried that did not go through, *held back by the rules* = people the rules kept from trying something that round (one per person per round, drawn as hatched orange squares). The same Repair Bay run in a browser now says "Round 5 · 10 allowed · 1 refused · 20 held back by the rules", matching its 10 allowed, 1 refused and 20 held-back squares. Test: `tests/test_world_builder_home.py` (`test_headline_counts_refused_attempts_not_held_back_moves`).

### G3. /build approval screen hides installed processes

- **Model:** processes are installed law: they run every round with their own checks and writes (`src/world_substrate/engine.py:762`); `CausalReview` lists them (`src/world_substrate/action_authoring.py:418`). Ongoing worlds always get 1-4 of them (`scripts/generate_causal_model.py:237`).
- **View:** the mechanics section renders `causalReview.mechanics` and the terminal only (`scripts/world_builder_app.js:270-274`); `review.processes` is never read. The Approve button sits under that list (`:275`).
- **Reproduced: yes.** Playwright on `evidence/renders/world-builder-v0.html` with a generated-mechanics response for the embedded Orchard world plus one process `regrow` ("Picked fruit grows back."): after generating, the Approve button appeared, the page text contained the mechanic but neither `regrow` nor "grows back". The home page does show processes (`world_builder_home.html:412`).

### G4. Run log keeps only key names for three logged paths

- **Model:** the run log promises that "the world and rules produced" are retained for every build (`scripts/world_builder_service.py:290-296`).
- **Code:** `_result_summary` keeps real results only for `/generate-world`, `/run`, `/clarify`, `/surprise`; `/generate-mechanics`, `/generate-draft` and `/compare-native-coordination` fall through to `{"keys": [...]}` (`world_builder_service.py:374`). So a mechanics proposal made in `build` and every comparison outcome are lost; an approved model is only recoverable if it was later sent to `/run` (whose request is logged in full when not continued, `:325-336`).
- **Reproduced: yes.** Calling `_result_summary` with each path's real response shape returned only key lists, e.g. `/generate-mechanics -> {'keys': ['causal_model', 'cost_usd', 'daily_cost_usd', 'model', 'ok', 'review', 'trace_id']}`. The model test pins the current split (`run_log.summarised_paths`), so closing the gap means updating the model.

### G5. Home approval screen shows no derived authority or limits

- **Model:** Decision 006 defines the product as rules as data -> **compiler-derived authority** -> explicit human approval. `CausalReview` carries derived `reads`, `writes` and `limits` (`action_authoring.py:402-416`).
- **View:** the home "Check the rules" step shows each rule's checks and effects in plain words (`world_builder_home.html:370-414`) but no derived read or write paths and no limits. `build` does show them (`world_builder_app.js:272`).
- **Reproduced: yes.** Playwright with the Repair Bay review (5 mechanics, 27 derived read paths, 16 derived write paths, 5 limits): 0 of 27 read paths, 0 of 16 write paths and 0 of 5 limits appeared in the page text when the Approve button became enabled. This may be a deliberate plain-language choice (effects in words imply most writes), but no doc says so, and limits are not implied by anything shown.

### G6. Approval is a request flag, not a record

- **Model:** approval is the gate between proposal and execution (Decision 006, `docs/architecture.md` "Causal authoring and installation").
- **Code:** the server refuses `/run` and `/compare-native-coordination` unless the body says `approved: true` (`world_builder_service.py:957-962`, `:998-1000`); both pages send the literal `approved:true` (`world_builder_home.html:581`, `world_builder_app.js:304`, `:319`). Nothing records who approved which causal model when; the run log has the request flag and a `world_fingerprint` of bundle + model (`:330`), which is the closest substitute.
- **Reproduced: partly.** The local run log rows from the G2 run carry `request.approved = true` and nothing else about approval. No request was sent without a UI approval (that the server accepts one follows from the code above but was not exercised).

### G7. Frozen mechanic profile id is shown nowhere and not logged

- **Model:** `MechanicProfile.freeze()` gives the installed law a stable identity before the run (`src/world_substrate/profile.py:266`); the trace carries it as `mechanic_profile_id` (`run_authored_world.py:411`).
- **Views:** no page reads `mechanic_profile_id` (`grep` over `world_builder_home.html`, `world_builder_app.js`, `render_scene_replay.py`, `render_replay_studio.py`: 0 matches), and the run log's `/run` result drops it (`world_builder_service.py:360-367`).
- **Reproduced: yes** (trace key present in the G1 run; absent from the G2 run-log result keys; grep counts above).

- **Fixed 2026-10-06 (owner run log only).** Every `/run` run-log line now keeps `result.mechanic_profile_id`, and `scripts/world_builder_runs.py` prints it once per run as `rules-id=...`. Tests: `tests/test_world_builder_service.py` (`test_every_run_logs_its_frozen_rules_identity`, `test_run_log_reader_shows_the_rules_identity_once_per_run`). The visitor pages still do not show it.

### G8. Round replay carries no trace of process-made changes

- **Model:** due processes commit `accepted` events each round via `Engine.advance` (`engine.py:762`); the transcript lists them as `world_changes`.
- **View:** the round replay builds frames from accepted actor actions (`scripts/render_scene_replay.py:237`) and never reads `world_changes` (0 matches). The home feed does print them ("By itself: ...", `world_builder_home.html:542`).
- **Reproduced: partly.** A 4-round scripted run of the Orchard world with the `regrow` process committed one process event in round 1; the rendered replay HTML contains no mention of `regrow`. Whether the picture still shows the resulting state change (for example a fruit's stage) was not checked.

### G9. Actors moved to the same place stack on one point (issue #106)

- **Model:** a frame's views are a presentation of canonical state; every actor in `views.actors` is meant to be visible.
- **View:** `actorPositions` puts every actor whose latest `actor.move_to` targets the same anchor on the identical point (`scripts/render_living_scene.py:129`, `scripts/render_composed_living_scene.py:106`).
- **Reproduced: yes.** Copy of `tests/fixtures/living_scene/neutral-render-profile-v1.json` with a second `actor.move_to` (actor-b to `resource-a`) on the same event, rendered with both renderers and read in Playwright: at frame 1 both actors sit at `(20%, 28%)` in both renderers; in the composed renderer they stay stacked at frame 2.
- **Is #106 a coverage gap?** Yes. It is the case where the element is in the frame data (`views.actors` has both) but the view makes one of them invisible: the table marks World as "shown" in the living-scene views only with this exception. It affects the `build` page's native-coordination runs (which use the composed renderer, `scripts/run_native_coordination.py:18`) and agent_ecology3's Living view. Issue #106 is open with an approved fix; this PR does not change renderer code.

- **Fixed 2026-10-06 (issue #106).** After `actor.move_to`, actors that share an identical point are spread on a ring around it (radius from the profile's `render.gather_radius`, default 11; actor-id order); a single actor keeps the exact point, and a station with an actor standing on it moves its card below the actor so its label stays readable. Test: `tests/test_living_scene_layout.py`.

### G10. The two living-scene renderers place the same actor differently

- **Observation:** on the unmodified fixture `neutral-render-projection-v0.json` + `neutral-render-profile-v1.json`, frame 2 (activity start): `render_living_scene.py` moves actor-a into the activity ring at `(50%, 32%)`; `render_composed_living_scene.py` leaves actor-a at its move-to point `(20%, 28%)`.
- **Reproduced: yes** (same Playwright probe as G9). Which placement is intended is not documented; the [Living Scene v1 contract](../contracts/living-scene-v1.md) is the place to settle it.

- **Fixed 2026-10-06.** Root cause: each renderer had its own `actorPositions`; `render_living_scene.py` applied only the current frame's `actor.move_to` (an actor jumped home on the next frame), while `render_composed_living_scene.py` replayed every earlier move and let it override an active activity's ring. Both now embed one rule (`src/world_substrate/living_scene_layout.py`): moves persist, an active activity gathers its participants, a move in the current frame wins. On the fixture both renderers now put actor-a at the move-to point in frame 1 and in the activity ring in frame 2 (Playwright). Test: `tests/test_living_scene_layout.py`.

### G11. Continued live rounds trust client-held world state

- **Model:** "one canonical persistent world owns material truth" (root `AGENTS.md`).
- **Code:** live play asks for one round at a time; between rounds the world state lives in the browser and comes back as `continue_from` (`world_builder_home.html:582`). The server checks that the snapshot's `world_id`, `content_id`, `rule_versions` and `engine_id` match the bundle (`run_authored_world.py:233-242`) but not that the entity state equals the previous round's `final_snapshot` (which the run log retains, `world_builder_service.py:366`).
- **Reproduced: no.** Read from code only; no edited snapshot was sent. This is a boundary finding, not a view gap: a visitor can only change their own world, but a logged run is not proof that round N+1 started where round N ended.

### G12. Scenario views show only what the run touched, not the world that was built

- **Model:** a pipeline run's world is the generated bundle plus causal model (`bundle.json`, `causal.json`): its name, components, every action and every process.
- **View:** the replay draws the transcript `to_trace` builds from attempts (`render_run.py:25`); the state panel lists entities by label with their field values (`render_run.py:68`). Neither names the world, its components, actions nobody attempted or processes that never fired.
- **Reproduced: yes.** Waltzman run page: actions `cast-vote`, `activate-system` (attempted) present; `submit-concern`, `hold-meeting` (never attempted) absent; component `governance_participant` absent; world label and summary absent; processes `tally-country-approval` and `apply-weekly-activated-system-wear` (fired) present, `apply-weekly-unresolved-concern-pressure` (never fired) absent. The state panel showed every entity's fields after each round.

### G13. No view shows the layer-1 scenario model or its check report

- **Model:** Decision 007 layer 1 produces a checked model (ODD, stock map, repairs, check findings; `model.json`, `checks.json`) that "the person approves ... in plain words".
- **View:** `render_run.py` reads only `summary.json`, `attempts.jsonl`, `ticks.json`, `events.jsonl` and the bundle/causal model; no page renders `model.json` or `checks.json`.
- **Reproduced: yes.** The Waltzman run page contains neither the scenario text nor any check finding (0 matches for `blocking`/`finding`).

### G14. The pipeline has no approval step before a run and no keep-or-drop step after it

- **Model:** Decision 007 item 1: "The person approves the model in plain words"; item 3: "After the run, the person keeps or drops each new rule for future runs." Decision 006's pre-run approval (P4) is amended only for rules written mid-run.
- **Code:** `run_scenario.run` builds the Engine from whatever `bundle.json`/`causal.json` are in the model folder (`run_scenario.py:148-171`); no spike file checks or records an approval, and no file implements keep-or-drop (the only mention is the docstring at `midrun.py:11`).
- **Reproduced: no.** Read from code. A boundary finding, like G11, not a view gap: it marks the Approval row `n/a (G14)` in the scenario views.

### G15. Scenario views show a refusal's status but never the check that failed

- **Model:** a refused event carries `checks` with each check's label and verdict (engine event record, ODD 8.4).
- **View:** `to_trace` sets every row's `refused_because` to `[]` (`render_run.py:50`, `:56`); `state_rounds` keeps only `event_id`, `rule_id`, `status` and `changes` (`render_run.py:93`).
- **Reproduced: partly.** The Waltzman page's embedded panel data has no `checks` key and shows the three `unsupported_action` events by status only. That run had no `precondition_failed` event, so the loss of failed-check labels was not observed on a page, only read from code.

### G16. Scenario replay drops most of each attempt and the game master's ruling; "continue" shows as `no_action`

- **Model:** an Attempt records belief, cited observations, decision, expected effect, unlisted intent, what was performed and the observed effect; a game-master ruling records the intent, the proposed rule and why it failed (`summary.json` `rules_written_mid_run`).
- **View:** `to_trace` keeps only the belief (as `said`), the performed action and its status (`render_run.py:44-52`); a `continue` decision has no `action_record`, so it becomes `no_action`, the same as a resident that was not woken (`:49`, `:55`).
- **Reproduced: yes.** Waltzman run (10 attempts: 6 offered, 3 unlisted, 1 continue): in the browser the page text contained the belief "Country A currently supports activation" but not the unlisted intent ("Propose a time-boxed ..."), not the ruling reason ("No rule could be added ..."), not any expected effect or cited observation, and not the rules id `12d71aa7843fec08` (G7); the transcript data held exactly one `no_action` row, the `continue` attempt.

## Not verified

- `/waltzman/` and `/world-substrate-visualization/` (not deployed from this repository).
- LLM-policy runs (`policy: llm`) and live LLM generation: every probe used scripted moves and canned generation responses, so no model money was spent and LLM-specific fields (`said`, `said_on_retry`) were not exercised.
- The `owner_run_log` view through the deployed service (owner password not used); its row values come from the local run log written by the same code.
- Scenario views on runs other than the Waltzman run (truck, hospital and linked runs keep no `frames.html` in evidence; their PNG frames were not re-read).
- How `play` treats non-accepted statuses in each retained replay (it embeds older renders; marked "partial" from `render_scene_replay.py:237`).
