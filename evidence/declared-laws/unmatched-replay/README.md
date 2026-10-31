# Every attempt the current design's live runs could not read, replayed (2026-10-31)

Question: the build's test run picks typed moves directly, so it never uses people's own words or the reader that
turns words into a move (problem 5). Does that reader still lose turns live, now that #317 and #319 are in?

Inputs: every recorded interpreter call that matched no move in the eleven declared-laws live runs
(`../s1-pencil` to `../s4-waltzman-2`): 27 calls in 7 runs (`s2-pencil-3`, `s3-pencil-3`, `s4-waltzman` and
`s4-waltzman-2` had none). Each was sent again through today's prompt (`prompts/attempt_interpreter.yaml` 1.1)
with the same inputs, once, by `scripts/replay_interpreter.py`. Cost $0.0064 on the owner allowance; the 27
calls are in `llm-calls.jsonl` (traces `world-substrate-seller-wording-*`, the script's name for them at the time)
and the readings in `replay.jsonl`.

| What the person tried | Calls | Now |
| --- | --- | --- |
| a trade worded from the seller's side ("I sell one slat to the factory") | 9 | all 9 match the trade, right roles (#319) |
| "order boxed pencils from the pencil factory" | 1 (22290) | matches `buy-boxes`; four near-identical "place an order" calls (22229-22279) still do not |
| asking someone else to act: "I call the logger and ask them to send logs", "place an order with the factory" | 12 | none; no move does it, and nothing tells the person asked |
| a middle step the world folds into another move (buy or carry the logs, where `saw-slats` takes them from the logger) | 3 (21860, 21905, 21928) | none |
| something the world really has no move for (turn or pick up a tray) | 2 (22783, 22793) | none, correctly |

Findings:

1. **#319 settled every seller-side miss.** 10 of 27 now match, with the right buyer and seller.
2. **The remaining gap is requests, not reading.** 12 of the 17 still unmatched are a person asking another person to
   do something. The reader is right that no move does it. But the asked person never learns of it, so in `s2-pencil-2`
   the sawmill asked the logger for logs four times and the factory asked its suppliers twice, and in `s3-pencil` a
   shop placed the same order five times, each turn lost. The actor prompt invites this ("anything a person in your place could try with their body,
   voice or hands"), and the world already has a represented way to carry words to someone
   (`src/world_substrate/information.py`, source, recipient, channel and delivery). Recommended next slice: an attempt
   that asks a named person to act is delivered to that person as something they see next round, and changes nothing
   else. The asked person still decides, and the rules still decide what happens.
3. **One inconsistency.** "place an order for boxed pencils with the pencil factory" (4 calls) reads as none, while
   "order boxed pencils from the pencil factory" (22290) reads as `buy-boxes`. In that world a shop buys boxes from the
   carrier, so the factory as seller would be refused by the rules either way. Left as is.
4. **What the test run cannot show.** These are words only live AI people produce, so a typed test run never meets
   them. A regression replay like this one costs cents and catches reader changes; it cannot vouch for a new world
   before anyone has spoken in it.
