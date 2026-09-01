# World Substrate

World Substrate is the canonical project for building rich, inspectable worlds where agents choose actions and executable rules determine consequences.

The project combines:

- typed persistent world state;
- ontology-informed content without ontology-implied effects;
- reusable actions and ongoing process rules;
- state-derived, bounded affordances;
- causal events, persistence, and exact replay; and
- LLM or human policies that remain outside consequence authority.

Start with:

1. [Project wiki](docs/wiki/README.md) — what the project is, terminology, sources, and task routes.
2. [Roadmap](roadmap/README.md) — current truth, active slice, later milestones, and decisions.
3. [Architecture](docs/architecture.md) — enduring system boundaries.
4. [Core contract](docs/contracts/core-v0.md) — the first implementation seam.

## Current status

The project authority and design are established. The neutral runtime now reaches the pinned post-drink checkpoint through registered fill, heat, unheat, pour, and drink actions plus deterministic clock, hydration, thermal, evaporation, pathogen-removal, cooling, fuel, consumption, and harm rules. Its retained evidence compares semantic state and conservation fields rather than donor-specific hashes, and exact local replay passes. Whole-vessel ownership transfer remains to complete M1.

Related repositories remain unchanged and are classified in [source dispositions](docs/source-dispositions.md).

## Project checks

```sh
python scripts/check_project.py
python scripts/extract_castaway_fixture.py --check
python scripts/run_first_fill_probe.py --check
python scripts/run_boiling_probe.py --check
python scripts/run_pour_probe.py --check
python scripts/run_drink_probe.py --check
```
