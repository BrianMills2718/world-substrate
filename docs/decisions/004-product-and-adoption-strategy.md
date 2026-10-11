---
description: Generative-World Builder product direction and the off-the-shelf adoption strategy.
---

# Decision 004: Product direction and off-the-shelf adoption strategy

Governs: RULE-BUDGET-FAILS-CLOSED, scripts/world_builder_service.py

**Status:** accepted  
**Date:** 2026-09-07  
**Updated:** 2026-09-08
**Related:** [Decision 001](001-project-scope.md), [Decision 002](002-observability-and-replay.md), [Decision 003](003-semantic-mechanical-boundary.md)

## Context

The substrate, replay pipeline, visual authoring surface, constrained causal-mechanics compiler, and public World Builder are now implemented. The next question is not whether to keep building a bespoke framework at every layer; it is which layers are genuinely distinctive and which should use mature external systems.

The product also has two plausible faces: a rigorous world-modeling/simulation platform and a Generative-Agents-style world builder. The approved direction is to expose the latter as the product experience while preserving the former as the engine underneath.

Follow-on [competitive-landscape research](../research/competitive-landscape-2026-09.md) supports this layer split: Concordia/AgentSociety/OASIS/SOTOPIA are stronger neighbors for cognition, social simulation, scale, or evaluation, while PettingZoo/Melting Pot demonstrate the value of environment-governed transitions. World Substrate should differentiate on generative causal authoring, bounded authority, and provenance rather than rebuilding those neighboring stacks.

## Decision

World Substrate will pursue a **Generative-World Builder front end over a rigorous causal world engine**.

The following remain project-owned because they define the product's causal trust boundary:

- canonical persistent world state and identity;
- transition/commit/refusal semantics;
- constrained causal-mechanic declaration and compiler;
- semantic-to-mechanical binding and represented causal bearers;
- local mechanic authority and write-scope enforcement;
- causal event/trace semantics; and
- declarative scene semantics that map world truth to presentation.

Commodity capabilities should be selected from current external evidence and integrated behind replaceable boundaries rather than reimplemented. The 2026-09-08 procurement review in [technology procurement](../research/technology-procurement-2026-09.md) selects these defaults:

- **deck.gl 9.4.x** as the default living-world projector, using `OrthographicView` for schematic/non-geographic worlds and MapLibre integration when real geography is required;
- **Pydantic AI 2.41.x** as the default resident-cognition harness behind a thin `CognitionAdapter`; LangGraph and Concordia remain alternatives, not required comparison arms;
- **SimPy 4.1.2** only for simulated-time/event scheduling. Its clock, event queue, timeouts, and process wakeups may schedule opportunities, but SimPy resources or processes do not become canonical world authority;
- **Cytoscape.js 3.34.x** for an expanded causal/institutional graph inspector when a non-spatial graph surface is needed; Sigma.js is deferred until graph-scale pressure makes its large-graph rendering advantage material;
- **PettingZoo** as a future interoperability/evaluation adapter, never as alternate world authority; and
- standard persistence/auth infrastructure for saved worlds, runs, and access control.

Version families above record the procurement snapshot, not a floating-dependency policy. Implementation lockfiles should pin exact versions and upgrade deliberately.

### Decision rule for uncertainty

Use three categories so experiments are reserved for questions that are actually ours:

- **Novel uncertainty** — the field has no mature external answer and the result can materially change World Substrate architecture. **Experiment.** Generative causal closure is the primary example.
- **Commodity uncertainty** — benchmarks, research, production experience, and mature libraries already answer the question well enough. **Research → reason → select.** Model, renderer, agent harness, graph library, persistence, and auth selection normally belong here.
- **Integration uncertainty** — the architectural principle is already known, but a chosen dependency must prove it respects the World Substrate boundary. **Run a bounded conformance test**, not a comparative bake-off.

A commodity dependency is accepted when external evidence supports the choice and its adapter preserves the causal authority boundary. Local testing should prove conformance: authorized observations only, engine-minted actions only, no canonical mutation, private cognition isolation, bounded failure behavior, stable identity/provenance, and read-only presentation/analysis.

## Delivery order

The living roadmap remains authoritative for which product experiment runs next. This decision changes how commodity technology is chosen and how selected dependencies enter the system:

1. Preserve current project truth and full-log observability while running the roadmap-selected world/product experiment.
2. Extend owned world semantics only from concrete expressiveness, closure, or observability failures.
3. When live graphical execution is the selected slice, integrate deck.gl behind the existing scene/projection boundary and test read-only conformance rather than renderer alternatives.
4. When durable resident cognition is needed, integrate Pydantic AI behind `CognitionAdapter` and test observation/action/privacy/failure boundaries rather than agent-harness alternatives.
5. When richer simulated scheduling is needed, use SimPy for clock/event scheduling only; when a full non-spatial graph inspector is needed, use Cytoscape.js.
6. Keep generative causal closure—dependency inventory, enforcement mapping, counterexamples, residual risk—as owned experimental work.
7. Add saved worlds/runs and access control once the authoring/run loop proves persistence value.

## Consequences

- The project will not replace its causal kernel with a generic agent or game framework.
- LLM cognition frameworks may decide what an agent wants to do but may not determine what the world says happened.
- Renderer/game-engine code is not strategic IP; scene semantics and causal trace alignment are.
- Interoperability layers are adapters around the engine, not alternate state authorities.
- Future framework integration must be justified by a real world or product need, not by feature completeness.
- Do not spend local experiments rediscovering mature model/harness/renderer/library selection results; reserve experiments for World Substrate-specific uncertainty.
- Selected commodity dependencies remain replaceable adapters; selection does not move canonical consequence authority out of World Substrate.
