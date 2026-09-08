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

The product direction is now: **Generative-World Builder on top; rigorous world-modeling/causal engine underneath.** Keep the canonical state, transition kernel, semantic/mechanical binding, causal compiler, and trace model project-owned. Prefer off-the-shelf infrastructure for cognition, rendering, interoperability, persistence, and auth when it does not acquire causal authority. See [Decision 004](docs/decisions/004-product-and-adoption-strategy.md).

The immediate functional gate is human review comprehensibility on the retained Repair Bay law. Extend the constrained causal language only from concrete failures; do not fall back to arbitrary model-written code. For every live Builder investigation, inspect the complete request/response log and retained causal trace before diagnosing from summaries or replay; summaries and replay are orientation surfaces, not the debugging source of truth.

Make reversible changes without repeated approval. Do not mutate donor repositories. New deployment/publication, provider spend outside an already-approved bounded service, or runtime-generated-law installation outside the reviewed World Builder path still requires explicit authorization. Never create a special handoff document; improve the normal root → wiki → authority route instead.
