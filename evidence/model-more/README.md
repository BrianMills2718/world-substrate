# Model more: money, prices, distances and delivery time (2026-10-26)

Brian, 2026-10-26, on an I, Pencil world whose "Left out of the simulation" list named revenue, prices,
distances, delivery times and packaging: "why are we leaving these out", then "i dont get why there is
antyhgin we cant model?". The prompts told the AI those things could not be represented
(`scripts/world_dialogue.py` SCOPE, `scripts/generate_world_bundle.py` not_modeled). Commit 07a36a5 tells it
money, prices and feelings are number fields, places are entities, and travel or delivery time is a count of
rounds that a rule process lowers each round. Only dice-roll chance and real clock time stay out.

Same description (`description.txt`), kept-running world, owner key, one call each (no reruns):

| Run | Trace id | Cost | Left out | Money and prices | Delivery time |
| --- | --- | --- | --- | --- | --- |
| Bundle, main 623bce2 (`before.json`) | model-more/bundle/27bbdf1aed5c414f9ed3a47601a5adb1 | $0.0019 | clay; erasers, ferrules, paint; separate shops | none | none |
| Bundle, this branch (`after.json`) | model-more/bundle/afd3c9be87fa40888352fd1a13e45170 | $0.0020 | nothing | `business.cash`, `pencil_price`, `customer.cash` | `truck.rounds_left` |
| Rules for `after.json` before the countdown rule (`after-rules-1-no-countdown-rule.json`) | model-more/rules/c2464c9fae9c46c6963deb30ca15b3ee | $0.0068 | | sale charges the price | `deliver-boxes` sets `rounds_left` but hands the boxes over at once; no process counts it down |
| Rules again with the countdown rule (`after-rules-2-failed.log`) | (same script, new trace) | | | | failed compiling an unrelated check after one repair |
| Full service build, this branch (`service-build.json`) | world-builder-live/world/1859f2c9b7154d368fcc9364d2cb96cc | $0.0436 | nothing | `shop.pencil_price` only: no cash, a sale moves no money | none |

## Findings

- The "Left out" list is now empty in both builds on this branch (it had three items on main), and clay,
  erasers, ferrules and boxes are now counted stock.
- Money and delivery time are not reliably represented. One bundle had cash, prices and a delivery countdown
  field; the full service build had only a price and no countdown. An empty "Left out" list therefore does not
  yet mean everything was represented: the AI dropped cash without listing it.
- No run has shown a rule process counting a delivery down; the countdown rule in
  `scripts/generate_causal_model.py` is unverified live.
- The service build's dry run kept six of seven roles stalled (`dry_run.stalled_actors`), as on main; that is
  the existing chain-flow problem, not this change.

Reproduce: `uv run --no-project --python 3.12 --with pydantic --with-editable ~/code2/llm_client python
evidence/model-more/run_bundle.py <checkout> out.json` (and `run_rules.py <checkout> out.json rules.json`).
