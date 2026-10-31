# Seller wording: interpreter prompt 1.1 replayed on recorded attempts (2026-10-31)

Pencil build 4 (`../s3-pencil-4/TRACE_READ.md` finding 5) lost five turns. The miner and the mill said "I sell one
... to ...", and the customers said "I try to buy pencils", but the trades are named from one side (`buy-graphite`,
`buy-slats`, `sell-pencils`). The interpreter answered `none` ("there is no sell-graphite action kind"), although
the same rules let either side start the trade. In the same build, it matched two other seller attempts (calls
22560 and 22601), so the reading changed from call to call.

The fix is one added rule in `prompts/attempt_interpreter.yaml` (version 1.1): a kind named from one side of an
exchange is also the move of the person on the other side, and its fields are filled by who plays each part.

`scripts/replay_interpreter.py` sent the exact recorded inputs (person, attempt, kinds, entities, model) through the
new prompt:

| Set | Calls | Before | After |
| --- | --- | --- | --- |
| Failed exchange attempts from pencil build 4 (22533, 22541, 22586, 22644, 22575), 3 tries each | 15 | 0 of 15 matched | 15 of 15 matched the trade, with the person as seller (or as customer) and the right partner |
| Controls from pencil build 4 that already matched (22560, 22601, 22546, 22520, 22515, 22611) | 6 | 6 matched | 6 matched, same kind and fields |
| Negative controls that rightly matched nothing (airfield 18388, 18424, 18436, 18410; café 22783, 22793) | 6 | 6 none | 6 none, with the same reasons |

These are 27 calls costing $0.006, under trace ids `world-substrate-seller-wording-63778d19`, `-831f4a02` and
`-010ea12f`. The full calls (messages and responses) are in `llm-calls.jsonl`, and the readings are in
`pencil4-failures-and-controls.jsonl` and `negative-controls.jsonl`. The prompt's effect on a live build has not yet
been seen in one.
