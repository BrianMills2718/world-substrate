---
schema_version: project-wiki/v1
type: ProjectWiki
role: derived-navigation
status: active
reviewed_through: 2026-08-31
authority_refs:
  - ../../README.md
  - ../../roadmap/README.md
  - ../architecture.md
  - ../decisions/001-project-scope.md
---

# World Substrate project wiki

This is the single orientation surface for the project. It explains the current synthesis and routes readers to native authorities; it does not replace them.

## What this project is

World Substrate is a general executable environment for persistent worlds. LLM or human policies choose among state-derived actions. Registered rules and ongoing processes alone validate and change canonical state.

The intended result is a wide **compositional** action space rather than an enumerated list of natural-language commands. A vessel with capacity, material, contents, temperature, ownership, and location can participate in many independent rule families because those systems read the same persistent object.

## Start here

| Need | Read next |
| --- | --- |
| Current direction or next work | [Roadmap](../../roadmap/README.md) |
| Enduring system boundaries | [Architecture](../architecture.md) |
| First implementation interface | [Core contract](../contracts/core-v0.md) |
| Why neighboring projects are not the authority | [Source dispositions](../source-dispositions.md) |
| Consolidated research findings | [Research synthesis](../research/synthesis.md) |
| Human-set and reversible decisions | [Project-scope decision](../decisions/001-project-scope.md) |
| Reference-world expectations | [Reference worlds](../../reference_worlds/README.md) |

Read one route, then the relevant code or evidence. Do not load every donor repository.

## Concepts and terminology

- **Ontology:** identifiers, categories, properties, and relations used to describe what exists. It does not execute behavior.
- **Content:** particular materials, objects, recipes, locations, actors, and initial states.
- **Rule family:** an executable action or process over categories/properties, such as transfer between compatible containers.
- **Affordance:** one rule instance currently available to one actor, derived from canonical state. It establishes neither general reachability beyond that state nor reliable competency across variation.
- **Process:** a rule that continues when authoritative time advances, such as burning, cooling, growth, or debt accrual.
- **Canonical state:** the only material world truth. Prompts, narratives, UI views, and analysis are projections.
- **Observation:** an actor-authorized, intentionally lossy projection of canonical state; it is not a second state authority.
- **Causal closure:** every consequence claimed as mechanically enforced has a registered guard, transition, process, or declared source/sink.
- **Reference world:** a bounded end-to-end world that exercises shared substrate contracts without owning a private engine.

## What exists now?

- The project goal, architecture, core contract, source dispositions, implementation roadmap, and pinned freshwater expected-behavior fixture are established here.
- The neutral consumer path now reaches the pinned post-drink checkpoint through registered fill, heat, unheat, pour, and drink rules plus deterministic clock, hydration, thermal, evaporation, pathogen-removal, cooling, fuel, consumption, and hazard processes. Discovery, minimal observation, causal events, atomic rejection, semantic donor comparison, and exact replay run here; see the [first-fill](../../evidence/m1/first-fill-v0.json), [boiling](../../evidence/m1/boiling-v0.json), [pour](../../evidence/m1/pour-v0.json), and [drink](../../evidence/m1/drink-v0.json) evidence.
- Castaway has a working deterministic survival/physical prototype and retained evidence in its donor repository.
- Cybernetic Influence V3 has implemented authoring, canonical-world, typed transition, Concordia lifecycle, evidence, and analysis capabilities for socio-technical worlds.
- Linguistic Core has a large reviewed vocabulary source, but not executable mechanics.
- The rest of the neutral freshwater runtime—whole-vessel ownership transfer and the complete scenario receipt—has **not** yet been extracted into this repository.

The last point is the first implementation frontier. Documentation presence is not implementation.

## Sources and evidence

[Source dispositions](../source-dispositions.md) maps every material donor to an exact revision or file hash and states whether this project will reuse, adapt, depend on, or merely learn from it. The machine-readable record is [references/sources.json](../../references/sources.json).

Donor repositories remain read-only during consolidation. A capability becomes part of World Substrate only after its consumer path runs here and its evidence is retained here.

## Accepted authorities and decisions

- [Roadmap](../../roadmap/README.md) owns project direction and active work.
- [Architecture](../architecture.md) owns durable system boundaries.
- [Core contract](../contracts/core-v0.md) owns the first runtime seam.
- [Project-scope decision](../decisions/001-project-scope.md) records the user-approved goal and exclusions.
- Code and tests, once present, own implemented behavior.
- Revision-bound evidence owns observed claims.

## Working context

Castaway is the first reference world because it supplies a concrete composition test: the same vessel participates in ownership, carrying, liquid transfer, heating, damage, and ongoing processes. Cybernetic Influence V3 is the strongest source for authoring and causal-closure ideas, but its Concordia-first socio-technical product and permissive coarse/LLM transition authorities are not automatically inherited.

## Needs resolution

These choices are intentionally deferred until evidence makes them relevant:

- whether seeded stochastic transition rules belong in the core;
- which second reference world best proves cross-domain reuse;
- what local-object, actor-count, prompt-size, or throughput target defines the first scale milestone;
- whether Concordia adds value after the neutral deterministic vertical exists.

None blocks the first extraction slice.

## Architecture and workflow

```text
ontology + content
       |
       v
registered action/process rules <--- authoring + causal-closure validation
       |
       v
canonical persistent world -----> causal events + snapshots + replay
       ^
       |
bounded actor observation + generated affordances
       ^
       |
LLM, human, or scripted policy chooses only
```

See [Architecture](../architecture.md) for boundaries and the [core contract](../contracts/core-v0.md) for the first executable path.

## Human-reviewable artifacts

The current outcome-bearing artifacts are the locally runnable
[first-fill](../../evidence/m1/first-fill-v0.json) and
[boiling](../../evidence/m1/boiling-v0.json),
[pour](../../evidence/m1/pour-v0.json), and
[drink](../../evidence/m1/drink-v0.json) traces and replays. They adopt only
those consumer paths; the Castaway donor remains implementation authority for
the rest of the freshwater vertical.

## Roadmap

Use [the canonical roadmap](../../roadmap/README.md) for current work, evidence, decisions, and promotion triggers.
