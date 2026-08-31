# Research synthesis

This page compiles the findings that materially shape World Substrate. It is derived from revision-bound sources in [the manifest](../../references/sources.json).

## Dwarf Fortress lesson

Dwarf Fortress did not obtain breadth from one small universal ontology. Its effective action space comes from a large hand-built semantic substrate, parameterized content, general systems, procedural instantiation, persistence, and decades of accumulated interactions.

The reusable lesson is narrower and practical:

- rules operate over categories and properties;
- one detailed object participates in several systems;
- reactions can derive outputs from input properties;
- ongoing processes keep changing persistent state;
- content additions compose only inside implemented mechanisms; and
- simulation resolution is deliberately mixed rather than universally detailed.

World Substrate adopts this compositional pattern without claiming comparable breadth.

## Castaway findings

The Castaway `world-systems` branch is the first concrete proof that the architecture is useful.

It demonstrates:

- LLM agents selecting typed actions while engine rules own effects;
- persistent vessels shared by ownership, carrying, liquid, heat, damage, and process systems;
- conservative liquid transfer, finite sources, finite shared fire power, boiling, evaporation, cooling, spills, and hazards;
- data-only addition of a stone beaker using existing mechanics;
- actor-local observation, bounded action pages, causal events, restart, and exact replay; and
- separately labeled scripted and genuine-model evidence.

It also exposes scale limits. Sixty-nine colocated vessels produced 4,927 candidate actions and a 73.3 KB prompt in the retained measurement. Bounded presentation does not by itself bound candidate generation or visible-state context.

These findings justify Castaway as the first extraction donor. They do not prove that its engine abstractions generalize to another domain.

## Cybernetic Influence V3 findings

Cybernetic Influence V3 contains the broadest implemented neighboring machinery. Its useful distinctions include:

- existence versus agency;
- attempt versus capability, authorization, and success;
- spatial topology versus routing and permission;
- information carrier/representation/provenance versus truth or belief;
- canonical state versus analysis;
- semantic action intent versus validated patch commit; and
- exact, coarse, descriptive, and unsupported representation depth.

Its current `CanonicalWorld` provides actor-authorized context, registered transition contracts, validation, atomic commit, observations, and evidence within a Concordia-owned outer lifecycle. Its authoring/compiler work also makes a critical limitation explicit: structural validity and enforcement of declared dependencies cannot prove that an author remembered every consequential dependency.

World Substrate should reuse these distinctions and selected code patterns. It should not automatically inherit Concordia lifecycle ownership, organizational-analysis scope, or LLM/coarse consequence authority. The first neutral vertical will make that comparison concrete.

## Linguistic Core findings

The Castaway semantic review reused 18 predicates and 69 source entity types from Linguistic Core 0.3.0. It found useful vocabulary and hierarchy alongside unreliable optional roles and questionable type mappings.

The durable rule is:

> linguistic identity and category structure may help bind content to mechanics, but quantities, required arguments, validation, time, and effects remain local executable contracts.

World Substrate will depend on pinned reviewed subsets rather than treating the entire donor ontology as trusted runtime semantics.

## Dynamical Laboratory findings

The standalone Dynamical Laboratory specification provides an evaluation direction:

- treat trajectories plus metadata as reusable scientific objects;
- compare coupled and uncoupled systems;
- perturb state and rules;
- measure recurrence, recovery, alternative paths, and representation usefulness;
- avoid enumerating combinatorial trajectory spaces; and
- add complexity only after simpler experiments produce informative results.

These methods belong in later substrate evaluation. They do not justify building a second experimental framework before the first world vertical exists.

## Consolidated design consequences

1. Build the smallest neutral exact kernel that can reproduce one real composed world.
2. Separate ontology, content, rules, processes, policy, observation, and evidence.
3. Require explicit rule registration and source/sink accounting.
4. Derive affordances from current state and page presentation independently from enumeration.
5. Make unsupported mechanics visible.
6. Compile authoring data into registered contracts; never generate hidden executable code.
7. Preserve exact replay and distinguish model choice quality from world correctness.
8. Prove cross-domain generality with a second reference world before expanding the core spec.
9. Use perturbation and scaling experiments only when their result can change the architecture.

## Open research questions

- Can the first neutral component model reproduce Castaway without becoming a generic property bag?
- Which causal-closure checks are decidable from typed contracts, and which require fallible semantic review?
- Which second world adds a genuinely different mechanism family while reusing the same core?
- At what local-object count do indexing and observation selection become necessary?
- Does Concordia reduce lifecycle work without weakening deterministic consequence authority?
