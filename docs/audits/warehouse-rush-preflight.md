---
role: audit
status: active-experiment
reviewed_through: 2026-09-08
---

# Warehouse Rush live-authoring experiment

## Question

Can the existing Builder author and run a world with three locations, scalar action parameters, local observation, scarce mobile equipment, destination-matched cargo, capacity-limited trucks, and multi-step coordination without a new causal DSL or cognition framework?

## Fixture

The current fixture has four workers, two shared forklifts, six cargo units, two trucks at separate docks, and seven action kinds: `move`, `claim-forklift`, `release-forklift`, `drive-forklift`, `transport-cargo`, `load-cargo`, and `dispatch-truck`. Cargo/truck `route` values are `east`/`west`; physical action `dock` values are `dock-a`/`dock-b`; generic movement uses `location`. The terminal requires all trucks to be `dispatched`.

The hand causal model is only a solvability oracle. It reaches terminal in 20 accepted actions. Peak discovery during that oracle is 63 total candidates on one actor page, safely below the 256 cap.

## Fixture failure found before live approval

The first hand baseline was itself wrong: transport moved the worker/cargo without moving the owned forklift, and the action set had no honest way to return an empty forklift from a dock. Full state review caught the ownership/location split before it was promoted as evidence. The fixture was repaired by adding `drive-forklift`, making walking empty-handed, moving the forklift during cargo transport, and requiring forklift colocation for load/use. No DSL extension was required.

## Generated-law review

Five bounded generation attempts were retained under `evidence/warehouse-rush/` for a total mechanics-generation cost of `$0.04016310`.

1. Attempt 1: rejected. It compared cargo route labels `east`/`west` directly to physical dock ids and made ordinary dock movement illegal with a bad `contains` check.
2. Attempt 2: rejected after broader review. Guidance fixed the scalar-domain bug, but exposed the fixture-level missing empty-forklift movement described above.
3. Attempt 3: rejected after the fixture repair. It mixed route labels into movement parameter choices, emitted contradictory `contains` validation, repeated the route/dock mismatch, and omitted the terminal.
4. Attempt 4: rejected after renaming route/dock/location domains. Parameter choices improved, but contradictory `contains` checks and post-transport load prerequisites remained.
5. Attempt 5: approved after explicit review guidance. Its scalar domains, ownership/location checks, route matching, capacity checks, energy writes, and terminal are coherent. The exact generated law reaches terminal under the deterministic oracle in 20 accepted actions with peak page size 63.

The repeated failures are evidence that generic string fields/parameters lack an explicit semantic/domain contract. Do not implement a new enum/domain feature solely from this note, but treat it as the leading authoring-language candidate if another distinct world reproduces the same failure.

## Policy evidence

`scripted-first-available` on the approved generated law fails decisively: 30 turns, 72 accepted actions, terminal false, zero cargo loaded, and all four workers at zero energy. Accepted actions are 24 claims, 24 releases, 12 walks, and 12 empty forklift drives, with 64 stale-revision retries. This is policy selection failure, not causal expressiveness.

A bounded two-turn Luna probe on the same law succeeds at the first meaningful planning test for `$0.00373640`: both forklifts are claimed, then Worker B transports East Cargo 1 to `dock-a`. Other workers reposition in response to stale races. A separate four-turn probe costs `$0.00817640` and exposes a sharper policy-surface failure: it accepts 16 actions but moves no cargo, choosing six `drive-forklift` actions while its reasoning repeatedly claims those empty drives are carrying or advancing cargo. The trace shows the model is not merely planning poorly; it is misunderstanding what an offered action does.

## Liveness/observability failure found

The first 20-turn LLM-policy request did not complete within the client observation window. Full operator logs and a live stack sample showed the request thread blocked in provider SSL read while `LLM_CLIENT_TIMEOUT_POLICY=ban` caused the intended 60-second model timeout to be ignored. The fail-closed daily ledger retained the full `$0.12` reservation.

The World Builder launch environment was changed to `LLM_CLIENT_TIMEOUT_POLICY=allow` and the service restarted. A subsequent two-turn probe completed successfully and the service log confirms `LLM_CLIENT_TIMEOUT_POLICY=allow`. The stale `$0.12` reservation from the aborted request remains committed, preserving fail-closed accounting.

## Current interpretation

Warehouse Rush does not justify DSL breadth or a cognition framework yet. It does justify three narrower conclusions:

- full request/response and operator logs are essential; summary/replay alone would have hidden both the generated-law contradictions and the service timeout policy;
- generated scalar string domains remain a real review weakness, because multiple superficially compiler-valid proposals were behaviorally impossible;
- the existing lightweight LLM policy already shows qualitatively better action selection than first-available on the harder world.

## Next evidence

Improve the generic policy presentation so an offered authored action includes a concise compiler-derived preview of its installed effects. The current presentation shows only action kind and arguments, which makes `drive-forklift` indistinguishable from cargo movement at the consequence level. Re-run the same bounded probe after that narrow change. Do not add persistent cognition unless the model still fails while seeing the actual installed effects. Keep schema-domain work conditional on another reproduced scalar-domain failure or on a concrete authoring UX requirement.
