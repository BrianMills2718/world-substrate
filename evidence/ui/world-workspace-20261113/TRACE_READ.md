# World workspace HTTP/browser trace read

The final walkthrough uses actual owner-auth HTTP, SQLite persistence, sealed native snapshots and the composed Living Scene. Only the policy is replaced with scripted moves at the actual base-class dispatch seam; `LLM_CLIENT_NO_SPEND=1` additionally prevents provider spend. The retained pump generation is opened read-only. The orchard is explicitly constructed from the repository orchard fixture with twelve fruit and declared actor information. It is not a new model-generated world. Its stored definition deliberately omits the historical compiler display summary; the API derives that summary without changing stored rules or executing a model.

## Round 1

Ava (`ava`) picks apple-1 in `r1-e00001`; its stage changes ripe→picked and ownership moves from the orchard to Ava. The native actor cognition has the original brief and one recent pick, with empty resident memory. Source: `world-builder-live/run/defe9ee4f7834f72a8eda3a36068a819`.

## Round 2

Ava (`ava`) picks apple-10 in `r2-e00001`. Parent source: `world-builder-live/run/928b4b3ecc5847cb8cdf3e5f68c551c4`. The branch restores the exact completed round-1 snapshot and complete actor-state object, then makes the same scripted pick: `world-builder-live/run/68073b123cb24fdfaa913c6c05784ad9`. The parent remains unchanged. The repeated event ID is scoped to its run; the UI shows distinct run IDs and parent/fork metadata.

## Round 3

Ava (`ava`) picks apple-11 in `r3-e00001` in the parent (`world-builder-live/run/cf84409f6a6345d88645ed5ded8f8d6e`) and the branch (`world-builder-live/run/6c11fbf5454943f7ab8c15fad91a2c37`). Each has its own actor-state recent history with three picks, while retaining the same brief. No invented resident memory is claimed by this scripted fixture.

## Round 4

Ava (`ava`) picks apple-12 in parent event `r4-e00001`, source `world-builder-live/run/2a4ee3bd7ed14de0b0f6e7b094fde633`. Pause followed by explicit Replay retains the complete persisted prefix rather than dropping this committed round. This is the important pause/continuation regression check.

## Findings

All 27 browser checks passed at desktop and 390px. Opening/replaying/previewing produced no POST; explicit New run/Continue/Branch used actual HTTP. The child retained ancestry, exact snapshot and actor cognition, and did not mutate its parent. Scene selection reached the parent inspector. Nine visible controls showed styled tooltips. No browser errors or failed requests occurred. Phone screenshots include actual scene objects in the first viewport. The final six native rounds recorded $0.0 and had zero llm_client calls with their six trace IDs. This verifies interface integration and persistence, not LLM believability or spatial fidelity; the world view remains explicitly schematic where geography is unauthored.

The first adapter attempt accidentally executed four resident rounds because catalog dispatch bypassed the subclass override. It was stopped and corrected. Retained synthetic-only evidence is in `unintended-run-log.jsonl` and `unintended-model-calls.json`; `harness-correction.json` records the measured $0.00136536 total (eight calls, IDs 9687843–9687850). Every call was read, including both prompts and outputs. Resident calls progressively retained prior picks; the interpreter bound the exact named apple to `pick`; all eight calls finished normally. Those four run IDs are `world-builder-live/run/cc752aac872f47fa8b484a84a29481e7`, `world-builder-live/run/3c98d5d951fe4b3988e049198ca22551`, `world-builder-live/run/7dfaadf915b144edb618671fcb308ea3`, and `world-builder-live/run/40c315fefdca4effbe5271e3621ccf53`. They are retained as a harness failure, not substituted for the final scripted evidence.

Feedback:
- obs: A subclass-only policy override was bypassed by an explicit base-class call and caused eight unintended model calls costing a measured $0.00136536; expected zero provider calls (`harness-correction.json`, `unintended-model-calls.json`).
- claim (seen, high): The harness mocked the presumed dispatch point without checking the executed call site (`scripts/world_builder_service.py`, `verify.py`).
- action (Prevent, done): Patch the exact base method and enforce `LLM_CLIENT_NO_SPEND=1`; the corrected native walkthrough has six scripted rounds and zero model calls (`verify.py`, `run-log.jsonl`, `report.json`).

Historical review compatibility: the log retains bundle and rules but omits `review`; the owner API now derives the same compiler display summary used by existing shares, and leaves the stored definition unchanged. The missing-review fixture completes all 27 browser checks.

A rerun caught an overbroad stop check: `round_cap` ends one request segment, whereas `quiet_rounds`, `round_limit` and `budget` end the saved logical run. The stopped-checkpoint check now distinguishes those reasons; two native HTTP steps in every-round mode remain runnable and branchable. The failed scripted prefix and harness timing assumption are retained in `pause-harness-before.json` and `round-cap-before.txt`. The harness now requests Replay explicitly after Pause rather than assuming that Pause always changes viewing mode.

Feedback:
- obs: A truthy stopped record incorrectly treated a per-request `round_cap` as a finished logical run; the new native two-step regression preserves that distinction (`tests/test_world_catalog_service.py::CatalogServiceTests::test_request_round_cap_does_not_exhaust_logical_run`).
- action (Repair, done): Derive omitted historical display metadata on detached API reads and keep the original saved definition unchanged (`scripts/world_builder_service.py::_catalog_view`).
