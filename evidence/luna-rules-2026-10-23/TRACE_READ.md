# Trace read: gpt-6-luna for World Builder rules, 2026-10-23

Question: is `openrouter/openai/gpt-6-luna` good enough to write World Builder rules, or is
`openrouter/openai/gpt-5.6-sol` still needed for the rules retry? Brian approved the test and the default
switch on 2026-10-23 ("yes").

Setup: a local World Builder service (`scripts/world_builder_service.py` at b7aeb7c; the build path is
unchanged at b1d326c) with `WORLD_BUILDER_STRONG_MODEL=openrouter/openai/gpt-6-luna`, so the first rules
attempt, every rules rewrite and the people-world calls all used gpt-6-luna. Things worlds were driven by
`scripts/measure_world_builder.py --kinds task` four times over its six built-in descriptions. These are the
2026-10-05 measurement's "same six descriptions": the four landing-page examples plus the two from the cold
first-visit review (the garden's "before noon" is the review's dropped deadline). The script was committed
as "the measurement tools" the same evening (#102, 65e503e). Criterion as on 2026-10-05: the
scripted dry run reaches the world's finish line (`dry_run.terminal_reached`). People worlds were built
twice from the Waltzman description through `world_def: people`. Costs come from the llm_client call log
(`~/projects/data/llm_observability.db`, `llm_calls`, these trace ids). Stdout: `round1.txt` to `round4.txt`.
Server lines: `run-log.jsonl`. Rules and moves were read from the run log. Scripted dry runs were replayed
locally (no model calls) where the summary did not explain the result.

## Findings

- **Things worlds: 23 of 24 builds reached their finish line** (rounds: 6, 6, 5, 6). On the same six
  descriptions, 2026-10-05 measured gpt-5.6-luna at 11/24 and gpt-5.6-sol at 6/6. Cost: 61 calls, $0.0768,
  or $0.0032 per build. 18 builds needed one rules call. 6 used an inner compiler-guided repair or a rewrite.
  None errored.
- **The one miss (R3.1, garden) is a test-harness limit, not the model.** All four rule sets were correct
  (take can, water plant, set can down). The scripted policy takes the least recently done move, so it picks
  the can up and puts it straight back down. Watering four plants then takes 15 rounds, and the task test
  stops at 12 (`DRY_RUN_TURNS`). Replayed for 24 rounds, the same rules finish in round 15. Three rewrites
  ($0.009) were spent on rules that were already right. Saved as `tests/fixtures/garden-luna-r3.json`.
- **The finish line is a weaker check than "the rules say what the description says".** Four of the 23
  finished builds drop a stated constraint without listing it in `not_modeled`. In three of the four salad
  builds (R1.2, R2.2, R4.2), the rules check that the knife is free but no rule ever takes it, so both cooks
  work in the same round and the one shared knife constrains nothing. Only R3.2 has take and put-down rules.
  The library build R1.3 finishes as soon as *any* book is lent, although three are to be lent. Under this
  stricter reading, 19 of 24 builds are faithful and finished. The rules retry runs only when the finish
  line is missed, so a stronger retry model would not have fixed any of these four. 2026-10-05 did not check
  faithfulness, so sol has no number to compare.
- **Constraints left out are mostly declared.** All four delivery builds list fuel use in `not_modeled`.
  Every firefighting build makes putting out a fire require a connected hose. One (R2.5) still lists that
  requirement as not modeled, a wrong note on correct rules.
- **Harness bug found and fixed:** the summary's `never_offered` counted only the moves offered when each
  person first chose, so a move made on a same-round retry was reported as never possible. R1.5 said
  `extinguish-fire` was never possible although it ran twice. For ongoing worlds this feeds false "never
  possible" guidance into rule rewrites. Fixed in `scripts/run_authored_world.py`, with the test
  `test_a_move_made_on_a_same_round_retry_is_not_reported_never_offered` on the saved fixture
  `tests/fixtures/firefighting-luna-r1.json`.
- **People worlds (Waltzman): both builds ran, at $0.0522 and $0.0563**, against $0.49–0.67 per sol rules call
  on 2026-10-16 (`world-builder-live/people/*` in the call log). Build 1 kept everyone active for 24 rounds
  (score 4 of 4). Build 2 left the partnership and the regional health network stalled. Its one rewrite was
  skipped because the build was already past `PEOPLE_REWRITE_BY_S` (80 s), a time limit rather than the model.
  In both builds the compiler guard dropped the model's meeting rules for writing state the compiled meeting
  moments own, so "members meet regularly" is classed unsupported. That is a boundary between the rules
  prompt and the compiler. The stronger evidence for this path is the live Waltzman gate C1–C6, which passed
  on 2026-10-21 with gpt-6-luna for every call (`evidence/best-of-all-worlds/final-b7d1dc5`, #198).
- **Why the local call log showed no gpt-6-luna rule writing:** the live service on the VPS logs to its own
  database (`LLM_CLIENT_DB_PATH=/data/llm_client/llm_observability.db`, `deploy/vps/Dockerfile`), so live
  luna builds since 2026-10-16 never reach `~/projects/data/llm_observability.db`.
- **Decision:** gpt-6-luna stays the default for the rules retry and the people world. Total measured spend
  was $0.1853 (73 calls).

## Builds

Things worlds, in run order (R = round, then description index 0–5: delivery, garden, salad, library,
bakery, firefighting).

| Build | Trace id | What the trace showed |
| --- | --- | --- |
| R1.0 | `world-builder-live/world/666b24f47e1c4a1aadfc0a0a6ae2d868` | First rules: `deliver` never possible (owner `entity:van` vs `actor:van`); rewrite finished in 6 rounds. Fuel in `not_modeled`. 4 calls, $0.0054. |
| R1.1 | `world-builder-live/world/1a44b24594a94c5c8093c762dae16fd0` | Water plant / hand over can; all four plants watered in 9 rounds. |
| R1.2 | `world-builder-live/world/47d775134b7b443eafadfe4cba8ab2d7` | One rule `finish-salad-order` checks the knife is free but never takes it; three orders in 2 rounds. Finished, not faithful. |
| R1.3 | `world-builder-live/world/e02e9c5f237b47ef8b87761fe5a6c765` | Finish line `any` book off the shelf; done after one loan in round 1. Finished, not faithful. |
| R1.4 | `world-builder-live/world/0558b94623bd44a5aa8db966f6d9bef0` | Flour to dough to bread to sale; finish at 4 sold in 11 rounds. |
| R1.5 | `world-builder-live/world/185fa5e9bd1f46018c28ae2250c10e15` | Inner compiler repair, then connect hose and two extinguishes, all in round 1 via retries. `never_offered` falsely listed extinguish-fire (bug fixed). |
| R2.0 | `world-builder-live/world/b838f9f1bd9141a198d70481b9363333` | Drive needs fuel; three packages delivered by round 3. |
| R2.1 | `world-builder-live/world/3a0fcdb9d0a94be48cadf57935dac482` | Take, water, share can; finished in 10 rounds. |
| R2.2 | `world-builder-live/world/0ab2edb5a69d47ad8b6d74d7f5167bfb` | `prepare-salad-order` checks the knife is free; nothing takes it. Finished, not faithful. |
| R2.3 | `world-builder-live/world/38815aabadcb40298c5db1403b11da86` | All three books need a borrower; finished in 3 rounds. |
| R2.4 | `world-builder-live/world/152c9cde052a4ef38ecdb67323248091` | Bakery chain; replayed: make dough, bake, buy alternate until 4 sold in round 9. |
| R2.5 | `world-builder-live/world/b47b516620fc4f53a4fb5fee5b656e36` | Put-out-fire requires a connected hose; `not_modeled` wrongly says that requirement is left out. |
| R3.0 | `world-builder-live/world/ca276f59940f44fa9888781203364123` | Drive needs fuel; delivered in 6 rounds. |
| R3.1 | `world-builder-live/world/55ed34c1b051487799ab23f9286305fc` | The miss. Four correct rule sets; the scripted test needs 15 rounds and stops at 12. 6 calls, $0.0118. |
| R3.2 | `world-builder-live/world/3d3fcc5298f54af9aaa1611182a094f8` | Take knife, finish order holding it, put knife down; 8 rounds. The faithful salad build. |
| R3.3 | `world-builder-live/world/3ea10e8806c24b3cacb6bbac7baee200` | First rules let nobody act ("run produced no actions"); rewrite lent all three books. |
| R3.4 | `world-builder-live/world/c1a2556deb9d4330aa9dc43edbdce98d` | Bakery chain; 4 sold in round 12, the last test round. |
| R3.5 | `world-builder-live/world/ca4659d3603447edb6d7877b30c9c311` | Inner compiler repair; hose connected before either fire. |
| R4.0 | `world-builder-live/world/443281372da64b6e88b9e8db1b97fa15` | Drive needs fuel; delivered by round 3. |
| R4.1 | `world-builder-live/world/04e988417ef94569b52935fb90c19be5` | Take can, water; finished in 5 rounds with one gardener doing all of it (`idle_actors`: gardener-ben). |
| R4.2 | `world-builder-live/world/e607a1c8f37548d5a450a90bcab5fcfe` | Knife only checked as present and portable. Finished, not faithful. |
| R4.3 | `world-builder-live/world/f41e5c2aec5a4434a286ac7a3b2b8f79` | Inner compiler repair; all three books off the shelf. |
| R4.4 | `world-builder-live/world/60b5ff8601044577b14929348666d04f` | Bakery chain; 4 sold in round 12. |
| R4.5 | `world-builder-live/world/a479ea0c3b1b44009f869fc02ed56f9b` | Put-out-fire requires the connected hose; round 1. |

People worlds (Waltzman description):

| Build | Trace id | What the trace showed |
| --- | --- | --- |
| P1 | `world-builder-live/people/84ad17adf0d14d1c9928f5e9854829ed` | 10 people, 19 rules. 24-round test: 190 accepted moves, nobody idle or stalled, active at the end. `deploy-system` never possible (the decision was never authorized). Meeting rule effects were dropped as compiler-owned. $0.0522. |
| P2 | `world-builder-live/people/0775bdbdeee54549b4ce6df639ee9b1b` | 10 people, 20 rules. 8-round test (past the 80 s rewrite cut-off): 68 accepted moves; partnership and regional health network stalled; three generated moment processes were dropped as compiler-owned. $0.0563. |
