---
description: One-page plan for the simple run view: a plain "what happened, round by round" story as the default, with the current screen kept as the advanced view.
---

# Simple run view (plan size: one page)

Goal: for a person dropped into a run who has never seen the engine, say what happened in plain words, with the current screen one click away as the advanced view. Source: Brian, 2026-11-17: "no one would be able to be dropped in here and udnerstnad htis. i feel like we need a simple and advanced interface probably", then "i approve" to option A (simple by default, current screen as Show details). Part of [unified-world-ux](../goals/unified-world-ux.md).

## Design

- **Simple (default):** one sentence on what the world is (taken from the world's own saved description, no extra call), the outcome bar, the support chart on a branch, then "What happened, round by round": one to three plain sentences per round naming the groups, what each tried and, for a refused or unmatched try, why nothing happened in everyday words. Run, What if and the round slider stay; moving the slider scrolls the story to that round.
- **Advanced:** the current run page, unchanged, behind a switch labelled "Advanced view" (not "Show details": that label already folds one rule's details). A plain link from Simple view reaches it, and Advanced view links back.
- **Event list (new `story_events`, not `evidence_events`):** one row per actor per round for every status except `no_action`: `status`, `did.kind`, `did.attempt`, `did.why`, `did.nearest_kind`, `refused_because` (empty for unmatched attempts, whose reason is `did.why`), `ruling.state`, `said`, accepted change text, and the row's `event_id`. `evidence_events` stays as it is (the readout depends on it).
- **AI step:** `POST /story`, task `world-substrate-run-story`, bound to the server's own record of the catalog run (never rounds sent by the client). Plain version first: one call given the whole event list and the people. The prompt tells the model to translate engine check labels into everyday words. Reply: a list of `{round (integer), sentences[], event_ids[]}`.
- **Length rule (proof, not a test):** estimate characters before the call. Under the budget: one call. Over it (the readout notes about 40k tokens for 40 rounds): split into slices of about 15 rounds, one call each, with the people list repeated. A slice that fails shows "rounds N to M were not summarised"; nothing is cut silently and "No recorded moves." is only written for a round that has no non-`no_action` row.
- **Checked, not trusted:** the round is a JSON integer matched against real rounds; each `event_ids` entry must exist in the recording and a sentence with none is dropped (same pattern as `validate_readout`); dropped ones are counted on the page. Prose is never read back with regex.
- **Where it is kept:** a new table `catalog_stories(checkpoint_id primary key, story, trace_id, created)` in `world_catalog.py`, separate from the immutable checkpoint body (analysis never mixes with canonical state). It is written once, when a saved run is first opened in Simple view or finishes, never per round of a live run. A live run shows "The story is written when the run finishes." Shared links read the story from the run log only while it is retained (3 days); otherwise they show the plain states below.
- **Plain states on the page:** loading, failed (one retry button), old run with no events, things worlds with no people (the story names things instead of groups), no story yet.
- **Registration:** `/story` is added to the service's path list, request summary and result summary so each call leaves a readable trace.
- **Spec:** an OpenSpec change `world-builder-page` for the Simple view and a new requirement for the story service.

## Cost basis (computed)

Measured on the live server (llm-cost, task world-substrate-run-readout): 86 calls, $0.1769, 1.6M tokens, about 18.6k tokens and $0.0021 per call. A long run is about 40k input tokens (the readout's own comment, not measured here); a story reads more per row, so a 45-round run is a few slices. Worked out: 3 slices x about 40k tokens at the readout's measured $0.0021 per 18.6k tokens is about $0.014, plus output (guess). Short runs: about $0.003. Run once per saved run because of the cache. Cap per call: $0.10, as for the readout. The cheapest design that does the job is this one call; no per-round calls.

## Slices

0. Count first: number of events and characters `story_events` gives for the real Waltzman run (settles the slice rule).
1. Service: `scripts/run_story.py`, the table and `POST /story` with tests (prompt contains the `did.why` and `did.attempt` strings; validation drops unknown rounds and unsupported sentences; cache hit makes no call; long list splits).
2. Page: Simple view by default, Show details switch, story rendering.
3. Live read: open the Waltzman run, read the story beside the recorded events for three rounds (trace id in the run log), record findings.

## Acceptance

A stranger can open the Waltzman run and say, from the Simple view alone, who tried what in round 2 and why it did not work. Every sentence is traceable to recorded events (slice 3 reads three rounds against the events).

## Out of scope

Simulation rules; the Advanced view's content; per-person memories.
