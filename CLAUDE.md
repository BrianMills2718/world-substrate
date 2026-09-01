# World Substrate

Build a general, inspectable world substrate in which LLM or human policies choose typed actions and executable rules alone determine persistent consequences. The project expands behavioral breadth through shared state, reusable rule families, ongoing processes, and content composition.

## Start here

Read [the project wiki](docs/wiki/README.md) for orientation and [the roadmap](roadmap/README.md) for current direction and the active slice. Follow the task-specific route from the wiki rather than reading every source.

Before editing a scoped subtree, read its local `CLAUDE.md`:

- documentation, research, or contracts: `docs/CLAUDE.md`
- planning authority: `roadmap/CLAUDE.md`
- reference-world material: `reference_worlds/CLAUDE.md`
- fixtures and verification: `tests/CLAUDE.md`

## Invariants

- One canonical world state owns material truth.
- Policies choose; registered rules validate and apply consequences.
- Ontology terms and content properties never imply unimplemented effects.
- Actions are generated from current state and explicit rule schemas.
- Ongoing processes use the same persistent objects and declared sources/sinks.
- Unsupported mechanisms fail visibly without state mutation.
- Actor observations remain distinct from observer truth and model explanations.
- Every mutation has causal evidence; replay uses pinned inputs without model calls.
- Seeded randomness, if later accepted, must remain rule-owned and exactly replayable.

## Current boundary

This repository is the canonical home for the initiative. M1's neutral
freshwater runtime is promoted: its registered deterministic rules and
processes reproduce the bounded Castaway vertical, retain causal evidence, and
replay from pinned inputs in a fresh process. The active roadmap frontier is
the M2 policy-consumer authorization gate; do not implement or call a model
without explicit model-execution authority and a spend cap. Castaway remains
the implementation donor beyond the adopted M1 path. Cybernetic Influence V3,
Linguistic Core, the Dynamical Laboratory specification, and shared
`llm_client` are sources or dependencies, not competing project authorities.

Make reversible local changes without repeated approval. Do not deploy, publish, spend on model calls, mutate donor repositories, or relax the deterministic-consequence boundary without explicit authorization. Never create a special handoff document; improve the normal root-to-wiki-to-authority route instead.
