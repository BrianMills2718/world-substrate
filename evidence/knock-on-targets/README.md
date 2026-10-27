# Knock-on targets: give a fall something to break, and say that using it is not a guess

**Question.** After #262 the world writer offers moves that upset things, but does a live build now write a
same-moment knock-on (Decision 009)?

**Live build at b1f561f** (owner, café text `cafe.txt`, share `dI4j2qUYPBBZ`, saved as
`tests/fixtures/cafe1-live.json`): the world had tip-stack, right-stack, pick-up and put-down, and in 8 AI rounds
the customer tipped the plate stack four times and the cleaner set it upright again. No knock-on: tip-stack only set
the plates' `upright` to false, the plates had no `broken` field and rested on nothing, and the rules' only process
was new demand each round. The build's own test run said "nothing sets off a knock-on effect".

**Changes.**
1. World writer (`scripts/generate_world_bundle.py`): for each upsetting move, represent what it would set off
   (fragile things get `broken`, containers `full`/`spilled`, each loose thing's `on` names what it starts on).
2. Rules writer (`scripts/generate_causal_model.py`): fields such as upright, full, spilled, broken and wet with an
   `on` link already state the physics, so using them is not an assumption; write the ordinary consequences as
   processes with timing immediately.
3. Build (`scripts/world_builder_service.py`): a test run whose rules flip a yes/no field with nothing following
   carries that advice into the next rules attempt, and among otherwise equal attempts the one with a knock-on is
   kept. It never fails an attempt on its own (watering a plant flips a field and nothing need follow).

**Samples on the changed prompts** (café text, `run_bundle.py` / `run_rules.py`):

| Sample | World has the targets | Rules, first prompt (change 1 only) | Rules, with change 2 |
| --- | --- | --- | --- |
| 1 (`cafe-bundle-1.json`) | yes: upright, broken, full, spilled, `on` for every prop | knock-over sets upright only, "not inferred from a bump alone" (`cafe-rules-1.json`) | still none (`cafe-rules-b1.json`, trace `model-more/rules/aed5ee32681f43a49e975e9620ba2bd5`) |
| 2 (`cafe-bundle-2.json`) | yes: on, full, spilled, broken | compile error, no rules (`cafe-rules-2.log`) | `spill-wets-resting-surface`, timing immediately (`cafe-rules-b2.json`, trace `model-more/rules/86f3d17056894fc08d2a75403c8ed0ab`) |

So the prompts get about one sample in two to a knock-on; change 3 raises the chance when a build retries anyway.
A live build after deploy is the check that counts.
