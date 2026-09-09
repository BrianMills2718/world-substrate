# World Substrate

> **Global navigation:** use the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md) as the canonical cross-repo entry point. This README remains the local entry point for this repository’s implementation, design, and evidence.

World Substrate is a persistent, observable world engine in which agents express semantically grounded intents and **installed mechanics—not model prose—determine canonical consequences**.

The project now includes both the causal engine and a deployed authoring product:

**World Builder:** https://brianmills.dev/world-builder/

**Standalone living-world URL:** https://brianmills.dev/world-substrate-visualization/

The live Builder can define represented world structure, request a constrained LLM mechanics proposal, show compiler-derived authority for review, require explicit approval, and launch a fresh scripted or LLM-selected graphical run in the browser.

The standalone living-world URL currently serves the earlier synthetic visualization prototype. The approved next product move is to replace that surface with the already-implemented canonical Waltzman Coordination Lab client while retaining the synthetic prototype as versioned design evidence.

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

The **current prototype/deliverable is the Waltzman Coordination Lab demo**. Its first integrated local gate is now implemented through the real World Substrate path: canonical projection, asymmetric represented information, explicit mechanic-declared causal parents, a duration-bearing meeting, a represented coalition institution, exact-history intervention/fork behavior, detachable Waltzman analysis, and bounded dependency/adequacy reporting. Persistent cognition and a generic future-event scheduler were not required for this first gate.

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
| Public standalone visualization | synthetic prototype currently deployed; canonical Waltzman replacement now authorized as the next product step |
| Waltzman live read-only projection | implemented local first gate; exact snapshot/event reconstruction plus JSON/SSE observer seam |
| First-class information/delivery v0 | implemented; asymmetric source/recipient/channel/visibility/delivery/provenance plus retained context evidence |
| Waltzman cadence / duration activity | implemented scenario first gate on canonical integer ticks; generic SimPy/future-event scheduler remains later |
| Waltzman resident cognition | persistent cognition not integrated; existing bounded policy seam is sufficient for the accepted first gate |
| Waltzman institution / intervention / adequacy | implemented first bounded gate; coalition decision, exact-history fork, intervention, eight declared dependency mappings + residual risk |
| Saved user worlds/runs | not yet implemented; not required for first Waltzman demo unless the scenario proves otherwise |

The current live authoring path is:

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

The first integrated demo distinguishes world interaction, information lineage, cognition context/evidence, mechanic-declared hard causal ancestry, and analytic interpretation rather than collapsing them into a single narrative explanation. It also supports a represented intervention/fork and exposes consequential dependency assumptions plus explicit residual risk.

**Causal claim boundary:** World Substrate explains why an outcome occurred **inside the represented world under the installed mechanics that governed the run**. That does not by itself claim that those mechanics are scientifically true of the corresponding real-world system. Predictive validity, calibration, and real-world causal identification require separate evidence.

The current Waltzman adequacy report should be read as a bounded dependency inventory: eight declared consequential assumptions are mapped to represented state and installed enforcement surfaces, with known residual risks. It is not a counterfactual proof of necessity/sufficiency. Stronger automatic counterfactual/mutation verification is a deferred research idea, not a first-demo requirement.

See the [roadmap acceptance criteria](roadmap/README.md) and [Waltzman audit](docs/audits/waltzman-coordination-lab-v0.md) for the authoritative demo definition and evidence.

## Current next move

The integrated Waltzman first gate is implemented, reviewed, and landed on `main` through PR #47. The product decision is now made: **replace the existing standalone synthetic visualization with the canonical Waltzman client at the existing public visualization URL.**

The first public demo does **not** require World Builder integration. Present Waltzman as a reviewed reference world running through the real substrate; do not imply that the current Builder generatively authored its richer hand-written information/activity/institution mechanics.

The generated `evidence/renders/waltzman-demo-v0.html` is already self-contained and embeds the canonical baseline/intervention projection bundles, so the first public demo can remain a static read-only surface. The JSON/SSE service remains available as an optional observer/live seam rather than a publication prerequisite.

Before publication, make only the small truth-label cleanup needed to avoid overclaiming—especially describing the current adequacy surface as mapped dependencies rather than counterfactual proof and describing causal parentage as mechanic-declared. Then publish the canonical artifact, smoke-test the public URL, and stop. The [roadmap](roadmap/README.md) owns the post-demo hardening sequence.

## Architectural thesis

A rich world should come from **shared persistent state + semantic grounding + installed causal mechanics**, not from asking an LLM to narrate plausible consequences.

Policies may be scripted, human, or model-driven. They receive bounded observations and state-derived affordances and may select only actions the world offers. They do not directly mutate world truth.

Linguistic Core supplies meanings and participant roles. It does not supply persistence, quantities, effects, scheduling, authority, or commit semantics. Those belong to installed mechanics. See [Decision 003](docs/decisions/003-semantic-mechanical-boundary.md).

## Product direction

The approved product posture is:

> **Generative worlds with executable laws.**
> The product experience is a Generative-World Builder / living-world interface over a rigorous causal engine.

The current product proof for that posture is the **Waltzman Coordination Lab demo**. Generality remains an architectural constraint and later validation target; it should not displace delivery of the current vertical.

Waltzman is currently a **reviewed reference world**, not proof that the live Builder can conversationally generate its complete richer law. Generic authoring of information/activity/institution mechanics remains a later capability to earn from another concrete world rather than a prerequisite for publishing this demo.

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
| Waltzman Coordination Lab | current integrated deliverable | reviewed reference world: blocked baseline, exact-history intervention recovery, canonical living projection, information/causal overlays, detachable analysis |

The Kitchen remains the flagship completed watched-world demonstration: three same-model/prompt replications reproduced Bo completing at t9, deliberately releasing the shared knife at t10, Ama taking it at t11, and both orders reaching the t17 terminal. See [the Kitchen audit](docs/audits/kitchen-contested-world.md).

## Important current limitations

These are active boundaries, not hidden TODOs:

- Newly authored generic actions can have valid causal mechanics without yet binding a reviewed Linguistic Core sense/role mapping.
- The live causal declaration language intentionally does not express arbitrary Python, continuous physics, unrestricted collection mutation, or every institution/process form.
- Compiler acceptance establishes declared authority/type consistency, not global causal completeness.
- Declared read scopes are recorded but not enforced at runtime; an optional verification design exists.
- Current action write-scope placeholder binding is participant-bounded but not yet role-specific; strengthening `<target>`/`<source>`/etc. to bind exactly to their named action roles is planned post-demo hardening.
- Current authored-action discovery has a finite candidate cap; silent overflow should become explicit refusal or paging before large generated worlds depend on it.
- Current `MechanicProfile.freeze()` gives a reviewed package set a stable declaration identity, but future durable generated-law provenance should also fingerprint the exact executable law and compiler/interpreter version.
- `causal_parent_event_ids` are mechanic-declared and history-validated; they are not currently inferred from instrumented reads or proof of real-world causality.
- The bounded Waltzman adequacy report maps declared dependencies to installed enforcement surfaces; automated counterfactual/mutation verification is deferred.
- Information/delivery v0 is intentionally bounded: generic latency, corruption, audience groups, belief revision, and deception semantics are not yet modeled.
- Resident-agent memory, reflection, long-range planning, and social cognition are not yet part of the runtime; the first Waltzman gate uses the existing policy seam.
- The Waltzman fixture has tick-specific processes, one duration-bearing activity, and one represented institution, but the generic future-event/SimPy scheduler and generalized process/institution authoring surface are not yet implemented.
- The deployed Builder creates fresh runs but does not yet provide durable user-owned world/run persistence.
- Runtime mechanic/process implementation exceptions should become explicit causal failure events rather than only process-boundary errors.

None of the post-demo hardening items above requires reopening the core product architecture. The roadmap owns prioritization.

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
python scripts/run_waltzman_demo.py --check
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