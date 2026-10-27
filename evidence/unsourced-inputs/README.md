# Unsourced inputs and one-unit sales

**Question.** With hand-offs and cash live (#262, build b1f561f), does a pencil build now reach a sale?

**Live build** (owner, `pencil.txt`, share `NZD33sh3iX29`, saved as `tests/fixtures/pencil2-live.json`, 8 AI
rounds): goods moved for the first time (the truck carried logs, graphite and slats; the mill sawed slats), but
no pencil was made and nothing sold. Assembling a pencil needs clay, paint, erasers and ferrules; no actor or
process makes any of them and every stock starts at 0. The build's test run reported "steps that could never
happen", but its advice was generic and the redesign added no sources. Separately, `sell-pencils` charged the
price once for any quantity, because effects cannot multiply.

**Changes.**
1. Build (`scripts/world_builder_service.py`, `_unsourced_inputs`): fields a move uses up that no action makes
   (moving between holders does not count), no process renews and nobody starts with are named in the advice
   to the next rules attempt and the redesign. On the live pencil world it names clay, erasers, ferrules and
   paint; on the six other saved worlds it names nothing.
2. World writer (`scripts/generate_world_bundle.py`): every material a step uses comes from an actor who makes
   or supplies it, or a large starting stock.
3. Rules writer (`scripts/generate_causal_model.py`): a priced move hands over exactly one unit and charges the
   price once.

**Samples** (`run_bundle.py` / `run_rules.py` on `pencil.txt`):

| Sample | Rules | Unsourced inputs | Sale |
| --- | --- | --- | --- |
| 1 | the model returned no mechanics twice (`pencil-rules-1.log`); the live build retries this | - | - |
| 2 | `pencil-rules-2.json`, trace `model-more/rules/1eb6b97d4c074e6a98d57c68ea2881d2` | none | one pencil, price once |
