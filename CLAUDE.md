# World Substrate

Build a persistent, observable world substrate in which LLM or human policies express semantically grounded intents and installed mechanics alone determine canonical consequences. Expand behavioral breadth through shared state, Linguistic Core bindings, reusable mechanics, autonomous processes, installed institutions, and frozen world profiles.

## Start here

Read [the project wiki](docs/wiki/README.md) for orientation and [the roadmap](roadmap/README.md) for current direction and the active slice. Follow the task-specific route from the wiki rather than reading every source.

Before editing a scoped subtree, read its local `CLAUDE.md`:

- documentation, research, or contracts: `docs/CLAUDE.md`
- planning authority: `roadmap/CLAUDE.md`
- reference-world material: `reference_worlds/CLAUDE.md`
- fixtures and verification: `tests/CLAUDE.md`

## Invariants

- One canonical persistent world owns material truth.
- Policies and natural-language descriptions do not directly mutate that truth.
- Linguistic Core identifies senses and participant roles; installed mechanics supply effects.
- Every state-changing transition identifies a causal bearer and one local authority.
- Mechanics, permissions, and institutions propose effects; one enclosing transition commits causally coupled writes.
- Declared write scopes are enforced at state paths; declared read scopes are recorded, not enforced.
- Composite and analytic descriptions do not duplicate their underlying effects.
- Unsupported mechanics and interactions fail visibly without partial mutation.
- Resident-agent cognition remains distinct from canonical world state and post-run analysis.
- Every attempted transition produces sufficient causal trace for inspection.
- Exact replay is an optional M1/debugging capability, not a universal requirement.
- Accounting and conservation invariants are goal-relative to the selected world and mechanic.

## Current boundary

This repository is the canonical home for the initiative. M1's neutral freshwater runtime remains promoted: its registered deterministic rules and processes reproduce the bounded Castaway vertical, retain causal evidence, and replay from pinned inputs in a fresh process. Those are M1 implementation facts, not universal architecture requirements.

M2 through M7 are complete and all six prototype success criteria are met: `give` is semantically bound, exchange is derived, write scopes are enforced, ownership references are checked, two mechanics were authored offline and assayed, an LLM policy has driven the world, and a second reference world reuses the contracts. What remains is incremental hardening, listed as Open obligations in the roadmap — read it for the frontier rather than inferring direction here. Runtime law revision is deferred; do not call a model without explicit model-execution authority and a spend cap.

Castaway remains the implementation donor beyond the adopted M1 path. Linguistic Core and the classified research repositories are sources or dependencies, not competing authorities or code-adoption instructions.

Make reversible changes without repeated approval. Do not deploy, publish, spend on model calls, mutate donor repositories, or install runtime-generated mechanics without explicit authorization. Never create a special handoff document; improve the normal root-to-wiki-to-authority route instead.
