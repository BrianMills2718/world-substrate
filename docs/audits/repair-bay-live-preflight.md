---
role: audit
status: active
reviewed_through: 2026-09-07
---

# Repair Bay: nontrivial live-authoring preflight

## Question

Can the current authored-world contract and constrained action-mechanic language carry a materially harder world through the ordinary fresh-run path without adding substrate features first?

This is a **zero-spend local preflight**, not yet the deployed Builder/model-generation/human-approval result. Its job is to prove the target world is solvable with today's language and to expose product/runtime failures before spending model calls.

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

None of those prevented or corrupted this preflight, so they remain outside this slice.

## Next experiment

Use this same Repair Bay bundle in the deployed World Builder. Generate the mechanics rather than supplying the baseline causal file, inspect the compiler-derived review, approve only matching law, run Scripted first, then use the already-approved bounded LLM policy path if useful.

The next implementation change should come from the first discrepancy between the generated/reviewed world and this known-solvable baseline, not from another preliminary hardening pass.
