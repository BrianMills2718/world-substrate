# World workspace HTTP/browser trace read

The final walkthrough uses actual owner-auth HTTP, SQLite persistence, sealed native snapshots and the composed Living Scene. Only the policy is replaced with scripted moves at the actual base-class dispatch seam; `LLM_CLIENT_NO_SPEND=1` additionally prevents provider spend. The retained pump generation is opened read-only. The orchard is explicitly constructed from the repository orchard fixture with twelve fruit and declared actor information. It is not a new model-generated world.

## Round 1

Ava (`ava`) picks apple-1 in `r1-e00001`; its stage changes ripe→picked and ownership moves from the orchard to Ava. The native actor cognition has the original brief and one recent pick, with empty resident memory. Source: `world-builder-live/run/ed2e76fc40c548eca58678d921542480`.

## Round 2

Ava (`ava`) picks apple-10 in `r2-e00001`. Parent source: `world-builder-live/run/fc093f94b90d4f669915eee1ecd845ab`. The branch restores the exact completed round-1 snapshot and complete actor-state object, then makes the same scripted pick: `world-builder-live/run/4e8adf144bdc495ba6c58b4f769ef4bf`. The parent remains unchanged. The repeated event ID is scoped to its run; the UI shows distinct run IDs and parent/fork metadata.

## Round 3

Ava (`ava`) picks apple-11 in `r3-e00001` in the parent (`world-builder-live/run/783519f7c46a426395a65b329c055381`) and the branch (`world-builder-live/run/bde9c61cbd5f4c68a3dcb341a35ae977`). Each has its own actor-state recent history with three picks, while retaining the same brief. No invented resident memory is claimed by this scripted fixture.

## Round 4

Ava (`ava`) picks apple-12 in parent event `r4-e00001`, source `world-builder-live/run/286bf24447ae407086e72711cdd3ba0b`. Pause arrived during the previous request, so the UI reopened the completed persisted prefix rather than dropping this committed round. This is the important pause/continuation regression check.

## Findings

All 27 browser checks passed at desktop and 390px. Opening/replaying/previewing produced no POST; explicit New run/Continue/Branch used actual HTTP. The child retained ancestry, exact snapshot and actor cognition, and did not mutate its parent. Scene selection reached the parent inspector. Nine visible controls showed styled tooltips. No browser errors or failed requests occurred. Phone screenshots include actual scene objects in the first viewport. The final six native rounds recorded $0.0 and had zero llm_client calls with their six trace IDs. This verifies interface integration and persistence, not LLM believability or spatial fidelity; the world view remains explicitly schematic where geography is unauthored.

The first adapter attempt accidentally executed four resident rounds because catalog dispatch bypassed the subclass override. It was stopped and corrected. Retained synthetic-only evidence is in `unintended-run-log.jsonl` and `unintended-model-calls.json`; `harness-correction.json` records the measured $0.00136536 total (eight calls, IDs 9687843–9687850). Every call was read, including both prompts and outputs. Resident calls progressively retained prior picks; the interpreter bound the exact named apple to `pick`; all eight calls finished normally. Those four run IDs are `world-builder-live/run/cc752aac872f47fa8b484a84a29481e7`, `world-builder-live/run/3c98d5d951fe4b3988e049198ca22551`, `world-builder-live/run/7dfaadf915b144edb618671fcb308ea3`, and `world-builder-live/run/40c315fefdca4effbe5271e3621ccf53`. They are retained as a harness failure, not substituted for the final scripted evidence.

Feedback:
- obs: A subclass-only policy override was bypassed by an explicit base-class call and caused eight unintended model calls costing a measured $0.00136536; expected zero provider calls (`harness-correction.json`, `unintended-model-calls.json`).
- claim (seen, high): The harness mocked the presumed dispatch point without checking the executed call site (`scripts/world_builder_service.py`, `verify.py`).
- action (Prevent, done): Patch the exact base method and enforce `LLM_CLIENT_NO_SPEND=1`; the corrected native walkthrough has six scripted rounds and zero model calls (`verify.py`, `run-log.jsonl`, `report.json`).
