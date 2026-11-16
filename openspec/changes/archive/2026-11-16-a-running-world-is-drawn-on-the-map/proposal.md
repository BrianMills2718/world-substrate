## Why

Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams". While a world runs, the World Builder page showed text rounds, the old Network boxes and an older picture, and the room map with the graph beside it appeared only on a shared run afterwards. Increment 2 of `docs/goals/unified-world-ux.md`: the map and graph are the run's view while it plays.

## What Changes

- New service route `POST /live-replay` returns the room-map replay of the rounds finished so far, rebuilt from the server's run log (or, for the owner, a private catalog run). It saves nothing and withholds message words from visitors.
- The viewer, opened with `?embed=1`, waits for the page to post each longer replay, extends its timeline and plays on to the newest round unless the person scrubbed back.
- The run stage embeds that viewer. The old picture and the old Network panel leave the run stage.
