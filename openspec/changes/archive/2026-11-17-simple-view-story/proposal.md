## Why

Brian, 2026-11-17: "no one would be able to be dropped in here and udnerstnad htis. i feel like we need a simple and advanced interface probably", then "i approve" to a simple view by default with the current screen as the advanced view. A stranger opening the Waltzman run saw refusal labels and event ids and could not say who tried what.

## What Changes

- The run page opens in a Simple view: what the world is, the outcome bar and support chart, and one to three plain sentences per round. The current screen is the Advanced view behind a switch.
- A new `/story` service call writes the account with one light AI call (a few for a long run), checks that each sentence cites events of that round, and keeps it per checkpoint in its own table so reopening is free.

Plan: docs/plans/simple-run-story.md. Source: Brian, 2026-11-17.
