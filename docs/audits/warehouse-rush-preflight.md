---
role: audit
status: planned-preflight
reviewed_through: 2026-09-07
---

# Warehouse Rush live-authoring experiment

## Why this world

Repair Bay proved that the current causal declaration can express contested tools, relational effects, multi-entity repair, and a useful bounded LLM policy without a heavier cognition framework. The next experiment should change the failure surface rather than make Repair Bay larger.

Warehouse Rush adds three represented locations, scalar destination parameters, local observation boundaries, two scarce forklifts, six cargo-to-truck destination relations, truck capacities, and a terminal that requires both trucks to dispatch. It stays inside the existing action DSL so any failure can be attributed to authoring/review, observation/affordances, policy planning, or presentation rather than a predeclared need for new language.

## Fixture

- 4 workers at `staging`, each with finite energy;
- 2 shared portable forklifts at `staging`;
- 3 east-bound and 3 west-bound cargo units at `staging`;
- east truck at `dock-a`, west truck at `dock-b`, capacity 3 each;
- actions: `move`, `claim-forklift`, `release-forklift`, `transport-cargo`, `load-cargo`, `dispatch-truck`;
- terminal: all selected trucks have status `dispatched`.

The retained hand causal baseline is an oracle/solvability reference, not the law the Builder is expected to copy verbatim.

## Evidence order

1. Compile and execute the hand baseline locally; prove the intended world is solvable without changing the DSL.
2. Measure initial and peak discovered-action counts so the 256-action ceiling cannot silently contaminate interpretation.
3. Generate a fresh law through the already-authorized bounded World Builder service.
4. Inspect the **complete** generation request/response and compiler review before approving anything.
5. Run zero-spend Scripted first and inspect the full causal trace, not only summary/replay.
6. If the law is sound but Scripted fails, run the existing bounded LLM policy and inspect its full trace.
7. Let the first material discrepancy choose the next implementation slice.

## What to look for in full logs

- destination parameter choices that omit or invent locations;
- ownership/location guards around forklift claim/release;
- cargo being transportable from the wrong location or repeatedly transportable after loading;
- cargo destination matched against the wrong truck field;
- truck capacity overrun or dispatch before full load;
- actions hidden by local observation even though mechanics are correct;
- repeated legal-but-useless action churn;
- stale-revision retries masking a coordination failure;
- replay/presentation disagreement with canonical state.

## Stop conditions

Do not widen the DSL, add a cognition framework, or generalize the renderer before this experiment produces a concrete failure that requires it. If the existing law and lightweight policy solve Warehouse Rush, move to a qualitatively harder world/process boundary rather than hardening preliminaries.
