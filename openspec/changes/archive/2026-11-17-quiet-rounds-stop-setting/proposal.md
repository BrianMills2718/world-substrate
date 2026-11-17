## Why

Brian, 2026-11-16: "i want you to build out the whole ux/ui using best practices and considering designs for simliar projgrams". The live ten-group walk of `docs/goals/unified-world-ux.md` ended at round 1 or 3 because the service refused to continue after one round in which nobody's move was accepted ("no active moves"), although the world's own stop setting says "stop once nothing is changing, after 6 quiet rounds". Language-model attempts are often not matched to a rule in a single round, so one quiet round is normal.

## What Changes

- A saved run stays continuable through quiet rounds (nothing accepted and no move open) until the world's quiet-rounds setting is reached; only then does it say there are no active moves.
