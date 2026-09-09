# World Substrate

> **Global navigation:** use the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md) as the canonical cross-repo entry point. This README remains the local entry point for this repository’s implementation, design, and evidence.

World Substrate is a persistent, observable world engine in which agents express semantically grounded intents and **installed mechanics—not model prose—determine canonical consequences**.

The project now includes both the causal engine and a deployed authoring product:

**World Builder:** https://brianmills.dev/world-builder/

**Living-world visualization prototype:** https://brianmills.dev/world-substrate-visualization/

The live Builder can define represented world structure, request a constrained LLM mechanics proposal, show compiler-derived authority for review, require explicit approval, and launch a fresh scripted or LLM-selected graphical run in the browser.

## Start here

1. [Project wiki](docs/wiki/README.md) — compact orientation, terminology, current state, and task routes.
2. [Roadmap](roadmap/README.md) — canonical planning authority, current frontier, risks, and exact next action.
3. [Architecture](docs/architecture.md) — durable system boundaries and composition model.
4. [Decision 004](docs/decisions/004-product-and-adoption-strategy.md) — approved Generative-World Builder / off-the-shelf adoption strategy.
5. [Living-world projection](docs/research/living-world-projection-2026-09.md) — one-world overlay model, information/causality distinction, and first live-integration acceptance.
6. [Technology procurement](docs/research/technology-procurement-2026-09.md) — selected deck.gl / Pydantic AI / SimPy / Cytoscape defaults.
7. [Multi-timescale execution](docs/research/multi-timescale-execution-2026-09.md) — one canonical world timeline, independent mechanism cadences, duration-bearing activities, event-driven cognition.
8. [Competitive landscape](docs/research/competitive-landscape-2026-09.md) — adjacent systems and the "own reality; borrow minds" strategy.
9. [Core contract v0](docs/contracts/core-v0.md) — implemented transition substrate.
10. [Action mechanic declaration v0](docs/contracts/action-mechanic-declaration-v0.md) — constrained live causal-authoring language.

## Where this stands

The **prototype substrate phase is complete**. The system has progressed from a neutral transition kernel to a deployed authoring/run loop and a deployed synthetic living-world visualization prototype.

The **current prototype/deliverable is the Waltzman Coordination Lab demo**. The roadmap is organized around making that demo real through World Substrate rather than treating Waltzman as a later optional vertical. Live projection, information/conversation semantics, multi-timescale processes and activities, institutions, resident cognition, bounded causal-adequacy reporting, and intervention/fork behavior are enabling slices to add only as the Waltzman scenario requires them.

| Capability | Current state |
| --- | --- |
| Canonical typed world state | implemented |
| Atomic commit/refusal + causal events | implemented |
| Declared write-scope enforcement | implemented |
| Rule-facing authority isolation | implemented |
| Linguistic Core binding | implemented for six of seven M1 action kinds; live generic action authoring is not yet semantically closed |
| Scripted / human / LLM policy seam | implemented |
| Offline model-assisted mechanic authoring | implemented and assayed |
| Constrained live causal-mechanic generation | implemented and deployed |
| Generic graphical replay | implemented |
| Zero-review replay bootstrap/auto-layout | demonstrated across multiple real worlds |
| Visual world authoring | implemented and deployed |
| Fresh scripted/LLM graphical run | implemented and deployed |
| Standalone living-world visualization | deployed prototype; synthetic timeline; not yet fed by World Substrate |
| Waltzman slice 1: live read-only projection seam | next implementation slice |
| Waltzman slice 2: first-class information/conversation semantics | not yet implemented |
| Waltzman multi-timescale scheduling / duration activities | not yet implemented; current runtime is integer tick + per-step process `due()` checks; SimPy selected as future scheduler only |
| Waltzman resident cognition | not yet integrated; Pydantic AI selected behind adapter; target cognition wakeups are event/meaning-driven rather than every microstep |
| Waltzman institutions / intervention / causal-adequacy workflow | not yet implemented; add from scenario pressure |
| Saved user worlds/runs | not yet implemented; not required for first Waltzman demo unless the scenario proves otherwise |

The current live path is:

```text
authoring bundle
  -> bounded mechanics proposal
  -> local causal compiler
  -> compiler-derived authority review
  -> explicit approval
  -> frozen mechanic profile
  -> scripted or LLM policy chooses an offered action
  -> Engine commit/refusal
  -> retained causal trace
  -> graphical replay
```

See [the live authoring audit](docs/audits/live-world-authoring.md).

## Current deliverable

The target experience is one coherent **Waltzman Coordination Lab** run in which residents inhabit a bounded coordination world, receive asymmetric represented information, communicate through represented channels, act under resource/process/institution constraints, and evolve on one canonical simulated timeline. The user watches and interrogates the world through the living client, while Waltzman trust/risk/readiness analysis remains detachable from canonical world truth.

The first integrated demo must make it possible to distinguish world interaction, information lineage, cognition context/evidence, hard mechanical causal ancestry, and analytic interpretation rather than collapsing them into a single narrative explanation. It should also support at least one represented intervention/fork and expose consequential dependency assumptions plus residual causal-adequacy risk rather than claiming completeness.

See the [roadmap acceptance criteria](roadmap/README.md) for the authoritative demo definition.

## Current next move

The exact next action is **Waltzman demo slice 1**, not another framework bake-off, generic breadth exercise, or toy world. Feed a real retained World Substrate run (prefer Repair Bay) into the versioned living-world prototype through the smallest read-only projection seam, preserving canonical entity/event IDs and existing scene semantics. Repair Bay is the technical stepping stone, not the deliverable.

After that works, move directly to **Waltzman slice 2**: first-class information/conversation representation sufficient to model asymmetric information in the target scenario so visible agent interaction and provenance overlays are grounded in world truth. Subsequent process, institution, cognition, intervention, and causal-adequacy work should be justified against the Waltzman demo acceptance criteria. The [roadmap](roadmap/README.md) owns the full sequence.

## Architectural thesis

A rich world should come from **shared persistent state + semantic grounding + installed causal mechanics**, not from asking an LLM to narrate plausible consequences.

Policies may be scripted, human, or model-driven. They receive bounded observations and state-derived affordances and may select only actions the world offers. They do not directly mutate world truth.

Linguistic Core supplies meanings and participant roles. It does not supply persistence, quantities, effects, scheduling, authority, or commit semantics. Those belong to installed mechanics. See [Decision 003](docs/decisions/003-semantic-mechanical-boundary.md).

## Product direction

The approved product posture is:

> **Generative worlds with executable laws.**
> The product experience is a Generative-World Builder / living-world interface over a rigorous causal engine.

The current product proof for that posture is the **Waltzman Coordination Lab demo**. Generality remains an architectural constraint and later validation target; it should not displace delivery of the current vertical.

Keep project-owned:

- canonical state and identity;
- transition authority and refusal semantics;
- semantic/mechanical binding;
- causal mechanic declarations/compiler;
- local write authority;
- causal trace semantics; and
- the declarative mapping from world truth to presentation.

Use mature commodity systems around that kernel rather than rebuilding them. The selected defaults are **deck.gl 9.4.x** for the living projection client, **Pydantic AI 2.41.x** behind `CognitionAdapter`, **SimPy 4.1.2** for simulated-time/event scheduling only, and **Cytoscape.js 3.34.x** for expanded causal/institutional graph inspection. PettingZoo remains a future interoperability option; persistence/auth should use standard infrastructure. Commodity choices follow research → reason → select, while local tests prove only boundary conformance. See [Decision 004](docs/decisions/004-product-and-adoption-strategy.md), [technology procurement](docs/research/technology-procurement-2026-09.md), and [living-world projection](docs/research/living-world-projection-2026-09.md).

## Reference worlds and product evidence

| World | Purpose | Current evidence |
| --- | --- | --- |
| Castaway | M1 implementation/reference world | persistent state, processes, semantic bindings, exact pinned replay |
| Workshop | cross-domain substrate reuse | materially different mechanics and components |
| Kitchen | flagship watched world | replicated scarce-knife coordination; polished + Automatic graphical replay |
| Greenhouse | post-renderer authoring proof | new world, shared tool handoff, zero-review Automatic replay |
| Orchard | live-authoring acceptance fixture | generated causal law, compiler review, explicit approval, fresh scripted/LLM run |
| Repair Bay | Waltzman slice-1 technical fixture | generated five-action law, deterministic solvability, bounded LLM terminal run, full-log evidence; suitable retained run for live projection |
| Waltzman Coordination Lab | current integrated deliverable | target living coordination scenario; enabling slices in progress |

The Kitchen remains the flagship completed watched-world demonstration: three same-model/prompt replications reproduced Bo completing at t9, deliberately releasing the shared knife at t10, Ama taking it at t11, and both orders reaching the t17 terminal. See [the Kitchen audit](docs/audits/kitchen-contested-world.md).

## Important current limitations

These are active boundaries, not hidden TODOs:

- Newly authored generic actions can have valid causal mechanics without yet binding a reviewed Linguistic Core sense/role mapping.
- The live causal declaration language intentionally does not express arbitrary Python, continuous physics, unrestricted collection mutation, or every institution/process form.
- Compiler acceptance establishes declared authority/type consistency, not global causal completeness.
- Declared read scopes are recorded but not enforced at runtime; an optional verification design exists.
- First-class generic information/conversation semantics required by the Waltzman demo are not yet implemented.
- Resident-agent memory, reflection, long-range planning, and social cognition are not yet part of the runtime.
- Multi-timescale scheduling, duration-bearing activities, and generalized institutions are not yet implemented; add the minimum needed from Waltzman scenario pressure.
- The deployed Builder creates fresh runs but does not yet provide durable user-owned world/run persistence.
- Runtime mechanic/process implementation exceptions should become explicit causal failure events rather than only process-boundary errors.

The roadmap owns prioritization of these boundaries.

## Cross-repo role

World Substrate is the applied persistent-world engine and a demanding consumer/testbed for semantic grounding. Linguistic Core can ground action/relation identity and roles, but ontology terms do **not** imply causal effects here. World Substrate is not the ordinary application SystemSpec or a global semantic authority.

For the current authority matrix, lineage dispositions, empirical gates, and cleanup policy, see the [current ontology/semantic cluster architecture](https://github.com/BrianMills2718/vision/blob/main/wiki/synthesis/ontology-semantic-cluster-current-architecture-2026-09-07.md). Donor repositories are sources, not automatic adoption instructions. See [source dispositions](docs/source-dispositions.md).

## Verification

The default project check validates navigation, authority surfaces, links, contract status facts, retained evidence, and the neutral test suite:

```sh
python scripts/check_project.py
```

Useful deterministic probes include:

```sh
python scripts/run_first_fill_probe.py --check
python scripts/run_transfer_probe.py --check
python scripts/replay_transfer_evidence.py --check
python scripts/run_freshwater_probe.py --check
python scripts/run_give_exchange_probe.py --check
python scripts/run_overheat_assay_probe.py --check
python scripts/run_spill_assay_probe.py --check
```

Use `python scripts/check_project.py --with-donors` when the locally pinned donor revisions are available.

For current work, do not infer direction from old milestone narratives: read the [roadmap](roadmap/README.md).
