---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Repair Bay: nontrivial live-authoring proof

## Question

Can the current authored-world contract and constrained action-mechanic language carry a materially harder world through the ordinary fresh-run path without adding substrate features first?

This began as a **zero-spend local preflight** to prove the target world was solvable with today's language. The deployed Builder follow-through is now retained below: live mechanics generation, compiler review, scripted and LLM-selected runs, and the first product failure it exposed.

## Fixture

`examples/world_authoring/repair-bay-v0.json` represents:

- four technicians;
- three broken machines with different required tools/parts;
- one shared diagnostic scanner, one wrench, and one insulated driver;
- three matching repair parts; and
- five action kinds: `claim-tool`, `diagnose`, `repair`, `handoff-tool`, and `release-tool`.

`examples/world_authoring/repair-bay-causal-v0.json` is a hand-reviewed deterministic baseline using only `world-substrate-causal-model/v0`. `repair` atomically changes four represented entities: machine, part, held tool, and technician.

## Scripted baseline

Command:

```sh
python scripts/run_authored_world.py \
  examples/world_authoring/repair-bay-v0.json \
  examples/world_authoring/repair-bay-causal-v0.json \
  --policy scripted --turns 12
```

Retained evidence:

- `evidence/repair-bay/scripted-baseline-v0.json`
- `evidence/renders/repair-bay-scripted-v0.html`

Result: **5 turns, 10 accepted actions, terminal reached**.

The run includes three contested initial tool claims, six stale-revision retries, one technician losing the initial race after retry, three diagnoses, three repairs, and a scanner handoff. The final repair itself is selected again after a stale revision caused by the handoff and still reaches terminal.

## What this established

1. **No causal-language extension was required.** Existing selectors, comparisons, ownership expressions, scalar updates, and multi-entity effects express the baseline world.
2. **The initial action space is nontrivial but below the current cap.** Each actor sees 48 candidates: 3 claims, 3 diagnoses, 27 repair combinations, 12 handoffs, and 3 releases. The 256-per-mechanic discovery cap cannot silently shape this experiment.
3. **Contention is real rather than narrated.** Actors decide against one revision; accepted claims invalidate peers, which retry against new affordances. One actor finds nothing left after retry.
4. **Multi-entity causal writes stay under the ordinary engine boundary.** A repair updates machine status, part installation/provenance, tool wear, and technician energy as one transition.
5. **The naive zero-spend policy can still finish.** Resident cognition is not required merely to make this particular target world solvable.

## Concrete failures found

### Fresh-world entity ids leaked reference-world presentation identity

The authored technician id `bo` collided with an exact entity binding in the shared retained-world scene catalog. A fresh world could therefore inherit another world's presentation identity solely by reusing a bare entity id.

The smallest generic fix spans the fresh-run presentation seam: `scripts/run_authored_world.py` discards colliding exact reference-world bindings for authored entities and materializes explicit world-local category assets as exact bindings; `scripts/bootstrap_scene_profile.py` gives exact bindings precedence over broader category/component defaults. A focused regression uses a fresh Orchard actor named `bo`.

### Specific tool categories need authored assets

The Repair Bay initially declared only a generic `tool` asset. Shared presentation inference resolved the `wrench` category more specifically and the replay then lacked that asset in the fresh world's allowed asset set. This was fixed **in the world declaration**, by explicitly providing `scanner`, `wrench`, and `driver` assets/category bindings. No renderer or scene-profile feature was added.

## Deliberately not fixed here

- generic semantic bindings remain empty;
- resident memory/planning is absent;
- saved worlds/runs are absent;
- the causal DSL remains narrow; and
- no general affordance/discovery redesign was added.

None of those prevented or corrupted this proof, so they remain outside this slice.

## Deployed Builder follow-through

### Generated mechanics

The deployed Builder generated all five Repair Bay action mechanics with `openrouter/openai/gpt-5.6-luna` for **$0.00631945** (`world-builder-live/mechanics/98622cb483da4264ab75aa8b6da5f039`). The returned declaration compiled under the ordinary local authority review with no DSL extension.

The generated law was not byte-for-byte the hand baseline, which is useful rather than a defect. In particular, generated `diagnose` only marks a machine diagnosed; the hand baseline also spends technician energy and scanner wear. Generated handoff/release has no wear gate; the hand baseline deliberately used one to keep the deterministic first-available baseline from gratuitous shuffling. Generated `repair` still couples machine, part, technician, and tool state and preserves the intended matching checks.

These differences were visible in compiler review before approval; none required inventing state or arbitrary code.

### First live product failure: presentation namespace leakage

The exact authored bundle then returned HTTP 500 during fresh replay rendering. Local reproduction identified two presentations of the same defect class: authored technician id `bo` inherited Kitchen's exact `bo` asset, and `tool_kind=wrench` inherited a shared Workshop component-value asset even though the authored world declared its own tool presentation.

The branch fix makes fresh-world presentation declarations outrank retained reference-world catalog defaults. No causal code or renderer feature was added.

### Generated-law scripted behavior

With that presentation failure removed locally, the ordinary `scripted-first-available` policy ran the exact generated law for 30 turns: **90 accepted actions, terminal not reached**. It diagnosed all three machines, then cycled legal `handoff-tool` actions instead of choosing repair.

A deterministic oracle using the **same generated mechanics** reaches terminal in 11 accepted actions. Therefore this failure is not causal-language expressiveness or an invalid generated mechanic; it is policy/affordance selection under a world with several simultaneously legal but strategically poor actions.

### Bounded LLM policy

The deployed service still ran the pre-fix presentation code, so a naming-only temporary bundle variant avoided the two known catalog collisions while preserving the same generated causal declaration. Under the existing bounded service, Luna reached terminal in **5 turns with 15 accepted actions** for **$0.0072462** (`world-builder-live/run/ad1f335a490f432f8429a2f1917aea4d`). It adapted after stale-revision races and completed all three repairs.

This is evidence **against** jumping immediately to a resident-cognition framework: the existing lightweight LLM policy seam is already sufficient for this world, while the deterministic first-available baseline is intentionally not a planner.

## Retained live evidence

- `evidence/repair-bay/live-generated-mechanics-v0.json` — exact deployed generation response and compiler review;
- `evidence/repair-bay/live-generated-scripted-v0.json` — exact-bundle generated-law scripted trace after the local presentation fix;
- `evidence/repair-bay/live-llm-v0.json` — bounded successful live LLM trace with the temporary naming-only deployment workaround; and
- `evidence/repair-bay/live-experiment-v0-summary.json` — concise disposition of the full experiment.

## Next experiment

Do **not** add cognition infrastructure or widen the DSL from this result. The next unresolved product question is review comprehensibility: can a human distinguish the generated law from the hand baseline, understand the consequences of differences such as the handoff/release gate, and approve/refuse with confidence?

Use Repair Bay's generated proposal as the first review fixture, including plausible-but-material alternatives. Let an observed review failure—not preliminary hardening—choose the next implementation slice.
