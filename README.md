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

The project authority and design are established. The first neutral runtime slice now discovers and executes a registered liquid-fill action, advances registered clock and hydration processes, retains causal events, rejects overfill atomically, and replays exactly. Its retained evidence matches the selected fields of the pinned Castaway post-fill checkpoint. The remaining freshwater mechanisms are not yet implemented here.

Related repositories remain unchanged and are classified in [source dispositions](docs/source-dispositions.md).

## Project checks

```sh
python scripts/check_project.py
python scripts/extract_castaway_fixture.py --check
python scripts/run_first_fill_probe.py --check
```
