# Requests reach the person asked: the 27 unread attempts replayed again (2026-10-31)

Question: in the eleven declared-laws live runs, 12 of the 17 attempts the reader still could not match were a person
asking someone else to act, and those words reached no one (`../unmatched-replay/README.md`, finding 2). Does the
reader now name who is asked, without taking a move away from an attempt that has one?

Change under test: `prompts/attempt_interpreter.yaml` 1.2 and the `asks` field of `src/world_substrate/attempt.py`.
An unmatched attempt that names another person in the run is still recorded as changing nothing; the runner tells the
asker their words reach that person and gives the person asked the words, quoted, as their next round's note
(`scripts/run_authored_world.py`, test `tests/test_open_attempt.py::RequestTests`).

Inputs: the same 27 recorded calls as `../unmatched-replay/`, sent with `scripts/replay_interpreter.py` through
today's prompt with the same model, kinds and entities. Paid on the owner allowance: $0.0070 (first draft) and
$0.0084 (final), traces `world-substrate-interpreter-replay-8ed5c884` and `world-substrate-interpreter-replay-a25d3fa1`.
Every call is in `llm-calls-prompt-1.2a.jsonl` and `llm-calls.jsonl`; the readings are in `replay-prompt-1.2a.txt`
and `replay.jsonl` (the last five rows repeat 22290 three times and 22229 twice).

| Attempts | Prompt 1.1 (`../unmatched-replay`) | First draft of 1.2 | Final 1.2 |
| --- | --- | --- | --- |
| match a move | 10 | 9 | 16 |
| unmatched, the one asked named | 0 | 14 | 7 |
| unmatched, no one asked | 17 | 4 | 4 |

## Findings

1. The first draft named the one asked for all 12 requests and for 21928 (a purchase in a world with no buying move), but it also turned 22290 ("I try to order boxed pencils
   from the pencil factory"), which 1.1 read as `buy-boxes`, into a request. A request field invites the reader to
   treat any order as asking. The final prompt says a kind always comes first: ordering goods a kind exchanges is that
   kind, and `asks` is filled only when the kind is `none`.
2. With that rule the s3-pencil shop's five orders (22229, 22258, 22268, 22279, 22290) all read as `buy-boxes` with the
   shop as buyer, 22290 in 3 of 3 tries and 22229 in 2 of 2. So did the s3-pencil-2 shops' order (22346, as
   `deliver-boxed-pencils` from the factory) and the s3-pencil sawmill's question to the logger (22218, as `buy-logs`).
   These were never requests the world lacked a rule for; the reader missed the move.
3. The seven that stay requests are in s2-pencil-2, a world with no buying moves (its kinds are cut, saw, mine, make,
   assemble, pack, book, deliver and buy-pencil): the sawmill asking the logger for logs five times, and the factory
   asking the trucking company and the graphite mine to move goods. Each names the right person, so each would now
   reach them.
4. The four with no one asked are not requests: the lead works buying graphite and the sawmill carrying logs itself
   (s2-pencil-2, moves that world does not have) and the s4-cafe waiter's two tray moves (no tray kind). None names
   anyone.
5. Not shown here: what the person asked does with a request. That needs a live run (paid, needs Brian's yes).
