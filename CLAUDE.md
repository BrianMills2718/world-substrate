# World Substrate

Build a persistent, observable world substrate in which LLM or human policies express semantically grounded intents and installed mechanics alone determine canonical consequences.

## Start here

Read [the project wiki](docs/wiki/README.md) for orientation and [the roadmap](roadmap/README.md) for current direction. Use [architecture](docs/architecture.md) for durable boundaries and [accepted decisions](docs/decisions/) for human-set doctrine.

Before editing a scoped subtree, read its local `CLAUDE.md`:
- documentation/contracts: `docs/CLAUDE.md`
- planning authority: `roadmap/CLAUDE.md`
- reference worlds: `reference_worlds/CLAUDE.md`
- fixtures/verification: `tests/CLAUDE.md`

## Invariants

- One canonical persistent world owns material truth.
- Policies and natural-language descriptions never mutate canonical state directly.
- Linguistic Core supplies senses/roles; installed mechanics supply effects.
- Mechanics propose; one enclosing transition validates and commits or refuses.
- Declared write scopes are enforced; declared read scopes are recorded, not yet enforced.
- Composite/analytic descriptions do not duplicate primitive effects.
- Unsupported or defective behavior fails visibly without partial mutation.
- Resident cognition and post-run analysis remain separate from canonical world truth.
- Every attempted transition leaves inspectable causal evidence.
- A World Substrate causal claim is about why a transition occurred **inside the represented world under its installed mechanics**; it is not by itself a claim that those mechanics are scientifically true of the real world.

## Current boundary

The prototype phase is complete. Kitchen is the replicated flagship; Automatic replay generation works across Kitchen, Castaway, Workshop, and Greenhouse; and the deployed World Builder at `https://brianmills.dev/world-builder/` can author represented structure, request a constrained causal-mechanics proposal, review compiler-derived authority, explicitly approve it, and launch fresh scripted or LLM-selected graphical runs.

The product direction is now: **generative living worlds on top; rigorous causal engine underneath.** World Substrate is the product being demonstrated; Waltzman Coordination Lab is the current showcase/reference world, while Waltzman-specific trust/risk/readiness remain detachable analysis rather than core state. Commodity defaults are selected—deck.gl for living projection, Pydantic AI behind `CognitionAdapter`, SimPy for scheduling only, and Cytoscape.js for expanded graph inspection. See [Decision 004](docs/decisions/004-product-and-adoption-strategy.md).

The first integrated local Waltzman gate is implemented. `reference_worlds/waltzman/` runs a blocked baseline and an exact-history intervention branch through the ordinary Engine/policy seam; `world_substrate.information` provides bounded asymmetric information/delivery semantics; mechanic-declared hard-causal parents remain separate from retained information context; and `world_substrate.projection` drives a read-only living client/JSON/SSE surface from canonical snapshots and events. The generic future-event scheduler and persistent cognition adapter remain unintegrated because this accepted scenario does not require them.

The 2026-09-09 stakeholder decision supersedes the earlier static-publication target. The self-contained Waltzman client remains a reviewed reference/presentation fixture, but it is **not the finished outreach demo**. The Waltzman-facing release must let a visitor describe a situation in ordinary language, generate and review an editable simulation, run a fresh trajectory, and inspect the result through a living World-Substrate-style view. To reach that proof quickly, reuse Cybernetic Influence V3's already-implemented public V2 authoring/run/evidence pipeline behind the World Substrate demo rather than rebuilding general authoring in World Builder first. Cybernetic Influence remains implementation/research lineage, not the public product identity. The next integration boundary is a retained V3 run-projection -> living-view adapter; do not create a second simulation engine.

For every live Builder investigation, inspect the complete request/response log and retained causal trace before diagnosing from summaries or replay; summaries and replay are orientation surfaces, not the debugging source of truth.

The current bounded Waltzman adequacy report is a dependency inventory mapped to represented state and installed enforcement surfaces, with residual risk. Stronger automatic counterfactual/mutation verification is a deferred idea, not a first-demo blocker. Likewise, exact executable-law fingerprinting should strengthen future durable generated-law provenance, but it is not required to publish the hand-authored Waltzman reference demo.

Make reversible changes without repeated approval. Do not mutate donor repositories. The canonical Waltzman replacement at the existing standalone visualization URL is explicitly authorized by the 2026-09-08 product decision. Other new deployment/publication, provider spend outside an already-approved bounded service, or runtime-generated-law installation outside the reviewed World Builder path still requires explicit authorization. Never create a special handoff document; improve the normal root → wiki → authority route instead.
