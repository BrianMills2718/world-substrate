## Why

The comparison with Brian's earlier Waltzman UIs (docs/research/ui-comparison-waltzman-20261117.md, feature 2) found that "What if" only puts two maps side by side, with no numbers. Brian, 2026-11-17: "on decision 2 i apprbe yourr ecommendatino" (build the outcome bar and the support-per-round chart).

## What Changes

- Under the maps, a chart of the groups supporting the decision by round: the original run (blue line, circles) and the branch (orange dashed line, squares), the number needed, and the fork round marked in words. Read from the world state's typed group_decision component.
- It appears right after What if, and when a saved branch is opened (the parent run's rounds are fetched once). It is absent for worlds with no group decision and for runs that are not branches.
