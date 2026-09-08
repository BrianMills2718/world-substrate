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

## Installed-effect preview follow-up

Warehouse Rush then drove a narrow generic policy-surface change: offered authored actions now carry a read-only preview derived from the installed mechanic's concrete effects. This does not grant policy causal authority; it exposes what the already-installed law will write.

A two-turn post-change probe costs `$0.00435080` and changes behavior materially: after the two forklift claims, both active forklift workers choose `transport-cargo`, sending west cargo to `dock-b` and east cargo to `dock-a`. A four-turn probe costs `$0.00844043` and produces two transports plus two `load-cargo` actions; the pre-change four-turn probe produced zero transports and zero loads.

The four-turn trace still contains one semantic mistake: after cargo has been loaded into a truck, the model describes an empty `drive-forklift` action as advancing the loaded cargo even though that action's installed effect preview contains only worker/forklift location writes and energy cost. The prompt currently displays `[effects: ...]` without telling the model that this is the authoritative installed-effect preview. The next cheapest experiment is therefore a prompt clarification, not persistent cognition.

## Authoritative-effect instruction and longer policy probe

The generic policy prompt was then tightened so the installed effect preview is explicitly **authoritative** and absent effects must not be inferred. Live policy structured output was also capped at 512 tokens so the provider request does not advertise an irrelevant 65k-token output ceiling.

On the same approved v0 law, a fresh four-turn probe costs `$0.00922010` and again produces two transports plus two loads. Some stale/pre-retry reasoning remains loose, but the executed retries no longer systematically treat empty forklift movement as a cargo write.

The eight-turn probe costs `$0.01500593` and makes substantially more real progress: 29 accepted actions include four transports, three loads, and one dispatch; the East Truck reaches full capacity and dispatches on turn 6. The decisive failure arrives on turn 8, when Worker A legally transports `cargo-west-1` to `dock-a`. The v0 law permits either physical dock and transport is only legal from staging, so the west cargo is then stranded at the wrong dock. This is not a hidden LLM mutation or a missing planner primitive: the installed law itself failed to represent the route-to-physical-dock constraint.

The complete responses are retained as `llm-authority-4t.json` and `llm-authority-8t.json`. Free-form policy reasoning remains analysis, not world truth; the engine still commits only the installed effects.

## Warehouse v1: represent the missing causal distinction

The smallest response is a new fixture, not a generic DSL extension. `warehouse-rush-v1.json` adds `cargo.target_dock` (`dock-a`/`dock-b`) alongside the semantic `route` (`east`/`west`). The v1 transport law requires the selected physical dock to equal that represented target.

The ordinary validator and causal compiler accept v1. After a worker claims a forklift, `cargo-west-1` exposes only `dock-b`; the `dock-a` attempt is explicitly blocked by `dock matches cargo target`. The deterministic oracle still reaches terminal in 20 accepted actions with peak actor-page size 63. v0 remains retained unchanged as the evidence that earned this representation change.

A first live v1 generation attempt reached the provider but produced no mechanics output: observability trace `world-builder-live/mechanics/787c8a58c69e4134b5f3a305ce6b36f9` records one errored call at `$0` because the pre-fix mechanics path advertised `max_tokens=65536` while the active OpenRouter key could afford 12,440. The public fail-closed ledger charged the full reservation, ending the day at `$0.49906366` committed, so no retry was made.

That operator finding drove PR #41: mechanics generation now caps output at 8192 tokens, mirroring the already-bounded live-policy path while leaving room for the ~24–28KB causal proposals observed in Warehouse Rush. The fix is merged and deployed at `c3d31de`. v1 still has no generated law to review; retest after the daily budget resets.

## Liveness/observability failure found

The first 20-turn LLM-policy request did not complete within the client observation window. Full operator logs and a live stack sample showed the request thread blocked in provider SSL read while `LLM_CLIENT_TIMEOUT_POLICY=ban` caused the intended 60-second model timeout to be ignored. The fail-closed daily ledger retained the full `$0.12` reservation.

The World Builder launch environment was changed to `LLM_CLIENT_TIMEOUT_POLICY=allow` and the service restarted. A subsequent two-turn probe completed successfully and the service log confirms `LLM_CLIENT_TIMEOUT_POLICY=allow`. The stale `$0.12` reservation from the aborted request remains committed, preserving fail-closed accounting.

## Current interpretation

Warehouse Rush now supports four conclusions:

- full request/response, causal, and operator logs are the debugging source of truth; they separated law failure, policy misunderstanding, and deployment liveness instead of collapsing them into “the run failed”;
- compiler-derived effect previews materially improve the lightweight policy, while the authority prompt reduces but does not eliminate imprecise free-form reasoning; reasoning is not canonical state and should not be treated as such;
- the eight-turn failure is primarily a **representation/law** failure: if route-to-dock identity matters causally, it must be represented or derivable in the installed mechanic rather than left for policy common sense;
- generic scalar string domains remain a real authoring weakness, but v1 should be tested before adding an enum/domain feature. Another reproduced failure or a concrete authoring-UX need should earn that generic change.

Warehouse Rush still does **not** justify persistent cognition or a heavier agent framework. The existing bounded LLM seam already dispatches one truck once the offered effects are legible; the nearer question is whether a fully specified v1 law prevents irreversible bad choices.

## Next evidence

Generate mechanics for `warehouse-rush-v1.json` through the same bounded Builder, inspect the complete proposal/compiler logs, and require the target-dock constraint before approval. If the generator still invents or confuses scalar choices despite explicit `target_dock` state, promote author-declared parameter domains/enums from “candidate” to an earned product feature.

After a coherent v1 law exists, rerun the same short and longer effect-aware policy probes. Only if a correct, recoverable law still fails should the project spend implementation effort on planning/memory/cognition infrastructure.
