## Why

The comparison with Brian's earlier Waltzman UIs (docs/research/ui-comparison-waltzman-20261117.md, feature 1) found that nothing on the run page says where the group decision stands: at round 45 it could not be seen whether the system was deployed. Brian, 2026-11-17: "on decision 2 i apprbe yourr ecommendatino" (build the outcome bar and the support-per-round chart).

## What Changes

- Above the map, a bar shows the group decision, its status, support and conditional counts against the number needed, each group's position counted by value, meetings held, and the deadline meeting, all as they stand after the round the map shows; it follows the round slider. Words carry the meaning; the status tag is blue for open and orange for settled, with grey for waiting.
- It is read from the world state's typed components (group_decision, support, moment), never from prose, and is absent for worlds with no group decision.
