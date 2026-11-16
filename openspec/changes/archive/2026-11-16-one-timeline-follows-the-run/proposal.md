## Why

Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams". Increment 3 of `docs/goals/unified-world-ux.md`: one timeline. A saved run had two round controls (the map's scrubber and the page's round list) that did not agree.

## What Changes

- The embedded map viewer tells the page which round it shows and whether that is the newest, and offers "Back to the newest round" after the person scrubs back.
- For a saved run, the page's own Prev, Round and slider controls are hidden; the map's timeline chooses the round and the saved-run panels below follow it.
