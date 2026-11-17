---
description: One-page plan for the simple run view: a plain "what happened, round by round" story as the default, with the current screen kept as the advanced view.
---

# Simple run view (plan size: one page)

Goal: for a person dropped into a run who has never seen the engine, say what happened in plain words, with the current screen one click away as the advanced view. Source: Brian, 2026-11-17: "no one would be able to be dropped in here and udnerstnad htis. i feel like we need a simple and advanced interface probably", then "i approve" to option A (simple by default, current screen as Show details). Part of [unified-world-ux](../goals/unified-world-ux.md).

## Design

- **Simple (default):** the world in one sentence, the outcome bar, the support chart when the run is a branch, then "What happened, round by round": one to three plain sentences per round, naming the groups, saying what each tried and, for a refused try, why nothing happened in everyday words. Run, What if and the round slider stay.
- **Advanced ("Show details"):** the current run page, unchanged.
- **AI step:** one call per run, `POST /story`, task `world-substrate-run-story`. Plain version first: the same light model given the whole recorded event list (accepted moves, refused moves with what stopped them, unmatched attempts with the interpreter's note) and the people, and asked for the story. No extra stage. The story is cached per run and checkpoint, so reopening costs nothing.
- **Checked, not trusted:** every round named in the reply must be a round of the run; a round the model skipped gets "No recorded moves." The prose is never read back with regex.

## Cost basis (computed)

Measured on the live server (llm-cost, task world-substrate-run-readout): 86 calls, $0.1769, 1.6M tokens, about 18.6k tokens and $0.0021 per call. The story call reads the same events and writes about 1 to 4k tokens of output, so about $0.003 to $0.01 per run (calls x tokens x price, guess for the output share). Cap per call: $0.10, as for the readout. The cheapest design that does the job is this one call; no per-round calls.

## Slices

1. Service: `scripts/run_story.py` and `POST /story` with tests (prompt contains refused and unmatched attempts; validation drops unknown rounds and fills skipped ones; cache hit makes no call).
2. Page: Simple view by default, Show details switch, story rendering.
3. Live read: open the Waltzman run, read the story beside the recorded events for three rounds (trace id in the run log), record findings.

## Acceptance

A stranger can open the Waltzman run and say, from the Simple view alone, who tried what in round 2 and why it did not work. Every sentence is traceable to recorded events (slice 3 reads three rounds against the events).

## Out of scope

Simulation rules; the Advanced view's content; per-person memories.
