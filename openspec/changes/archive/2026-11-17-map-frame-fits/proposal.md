## Why

Brian, 2026-11-17: "the display isnt working did you even tes thits?" The embedded map on the run page showed only the top third of the viewer: the viewer was 1,939 px tall inside a 617 px frame, so the round slider and most of the graph were hidden behind a scroll inside the frame.

## What Changes

- The embedded viewer tells the page its height; the page sizes the map frame to it (up to 3,200 px), so the round slider and the whole graph are on the page with no inner scroll.
