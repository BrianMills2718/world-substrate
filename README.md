# World Substrate

World Substrate is the canonical project for building persistent, observable worlds where agents express semantically grounded intents and installed mechanics with explicit local authority determine and commit causal consequences.

The project combines:

- typed persistent world state;
- Linguistic Core sense and role bindings without ontology-implied effects;
- reusable actions, autonomous processes, and installed institutions;
- state-derived, bounded affordances;
- singular commit boundaries and inspectable causal traces;
- pre-run, agent-assisted mechanics expansion through frozen world profiles; and
- LLM or human policies that remain outside consequence authority.

Exact replay is an implemented M1 capability, not a project-wide requirement. See [Decision 002](docs/decisions/002-observability-and-replay.md).

Start with:

1. [Project wiki](docs/wiki/README.md) — orientation, terminology, sources, and task routes.
2. [Roadmap](roadmap/README.md) — current truth, active slice, later milestones, and decisions.
3. [Architecture](docs/architecture.md) — enduring system boundaries.
4. [Core contract v0](docs/contracts/core-v0.md) — the implemented M1 seam.
5. [Proposed semantic/mechanical contracts](docs/contracts/semantic-mechanical-binding-v0.md) — the next architecture seam.

## Current status

M1 is promoted. The neutral runtime reaches the pinned final freshwater checkpoint through registered fill, heat, unheat, pour, drink, take, and give actions plus deterministic processes. Retained evidence compares semantic state and conservation fields, preserves vessel identity across liquid, heat, carrying, and bounded ownership systems, and distinguishes precondition failure from unsupported and malformed actions. Its versioned initial snapshot, pinned registry/content identity, and 22 commands also reproduce the final state and events in a [fresh process](evidence/m1/transfer-replay-v1.json). The revision-bound [end-to-end observation](evidence/m1/end-to-end-observation-v1.json) passed the M1 maturity gate.

The strategy frontier is now semantic/mechanical integration: audit the promoted vertical against Linguistic Core and the causal-force boundary, bind the existing primitive `give` mechanic, derive ordinary exchange without double application, and establish the transition envelope needed before agent-authored mechanics. A genuine policy consumer remains an enabling experiment and still requires explicit model-call authority and a spend cap.

Related repositories remain unchanged and are classified in [source dispositions](docs/source-dispositions.md).

## Project checks

```sh
python scripts/check_project.py
python scripts/run_first_fill_probe.py --check
python scripts/run_boiling_probe.py --check
python scripts/run_pour_probe.py --check
python scripts/run_drink_probe.py --check
python scripts/run_transfer_probe.py --check
python scripts/replay_transfer_evidence.py --check
python scripts/run_freshwater_probe.py --check
```

The default project check is self-contained and uses committed fixtures. When the sibling donor repositories are available, also run `python scripts/check_project.py --with-donors`; the optional donor check reads pinned revisions rather than requiring their current checkouts to remain at those commits.
