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

## Current boundary

The prototype phase is complete. Kitchen is the replicated flagship; Automatic replay generation works across Kitchen, Castaway, Workshop, and Greenhouse; and the deployed World Builder at `https://brianmills.dev/world-builder/` can author represented structure, request a constrained causal-mechanics proposal, review compiler-derived authority, explicitly approve it, and launch fresh scripted or LLM-selected graphical runs.

The product direction is now: **generative living worlds on top; rigorous causal engine underneath.** The current deliverable is the Coordination Environment Lab/Waltzman demo, while Waltzman-specific trust/risk/readiness remain detachable analysis rather than core state. Commodity defaults are selected—deck.gl for living projection, Pydantic AI behind `CognitionAdapter`, SimPy for scheduling only, and Cytoscape.js for expanded graph inspection. See [Decision 004](docs/decisions/004-product-and-adoption-strategy.md).

The first integrated local Waltzman gate is implemented. `reference_worlds/waltzman/` runs a blocked baseline and an exact-history intervention branch through the ordinary Engine/policy seam; `world_substrate.information` provides bounded asymmetric information/delivery semantics; explicit hard-causal parents remain separate from retained information context; and `world_substrate.projection` drives a read-only living client/JSON/SSE surface from canonical snapshots and events. The generic future-event scheduler and persistent cognition adapter remain unintegrated because this accepted scenario does not require them. The authorized public visualization is still the earlier synthetic prototype; publication/replacement remains a separate authority decision. For every live Builder investigation, inspect the complete request/response log and retained causal trace before diagnosing from summaries or replay; summaries and replay are orientation surfaces, not the debugging source of truth.

Make reversible changes without repeated approval. Do not mutate donor repositories. New deployment/publication, provider spend outside an already-approved bounded service, or runtime-generated-law installation outside the reviewed World Builder path still requires explicit authorization. Never create a special handoff document; improve the normal root → wiki → authority route instead.
