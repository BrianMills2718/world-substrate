# Decision 004: Product direction and off-the-shelf adoption strategy

**Status:** accepted  
**Date:** 2026-09-07  
**Related:** [Decision 001](001-project-scope.md), [Decision 002](002-observability-and-replay.md), [Decision 003](003-semantic-mechanical-boundary.md)

## Context

The substrate, replay pipeline, visual authoring surface, constrained causal-mechanics compiler, and public World Builder are now implemented. The next question is not whether to keep building a bespoke framework at every layer; it is which layers are genuinely distinctive and which should use mature external systems.

The product also has two plausible faces: a rigorous world-modeling/simulation platform and a Generative-Agents-style world builder. The approved direction is to expose the latter as the product experience while preserving the former as the engine underneath.

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

Commodity capabilities should be adopted or integrated rather than reimplemented when they preserve those boundaries. Current evaluation candidates are:

- **Phaser** for browser 2D scene execution/animation (`https://phaser.io/`);
- **Concordia** and/or **LangGraph** for resident-agent cognition, memory, planning, reflection, and durable agent execution (`https://github.com/google-deepmind/concordia`, `https://docs.langchain.com/oss/python/langgraph/overview`);
- **PettingZoo** as a multi-agent interoperability/evaluation adapter, not as the world authority (`https://pettingzoo.farama.org/`);
- standard persistence/auth infrastructure for saved worlds, runs, and access control; and
- **SimPy** only if a real world demonstrates a need for richer asynchronous discrete-event scheduling (`https://simpy.readthedocs.io/`).

No candidate becomes a foundational dependency merely because this decision names it. Adoption requires a bounded consumer-path spike that demonstrates useful leverage without moving canonical consequence authority out of World Substrate.

## Delivery order

1. Stabilize current project truth, deployment records, failure observability, and CI.
2. Author one meaningfully less-trivial world through the deployed Builder and record concrete expressiveness/review failures.
3. Close the semantic loop so newly authored actions bind a reviewed Linguistic Core sense and participant roles before causal approval.
4. Compare a lightweight resident-cognition implementation with Concordia/LangGraph-backed adapters using the same World Substrate policy seam.
5. Move graphical execution toward Phaser only if it materially improves the live-world experience while retaining scene-profile semantics.
6. Add saved worlds/runs and access control after the authoring/run loop proves useful enough to persist.

## Consequences

- The project will not replace its causal kernel with a generic agent or game framework.
- LLM cognition frameworks may decide what an agent wants to do but may not determine what the world says happened.
- Renderer/game-engine code is not strategic IP; scene semantics and causal trace alignment are.
- Interoperability layers are adapters around the engine, not alternate state authorities.
- Future framework work must be justified by a real world or product failure, not by feature completeness.
