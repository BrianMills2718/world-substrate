# Research synthesis

This page compiles revision-bound findings that materially shape World Substrate. It is research input, not a second roadmap or a statement that donor code has been adopted. Exact revisions are recorded in [the manifest](../../references/sources.json).

The fuller reasoning is preserved in the [strategy-session ledger](world-substrate-strategy-session.md), [Agent Ecology 2 review](agent-ecology2-review.md), and [Cybernetic Influence lineage review](cybernetic-influence-lineage-review.md). [Discussion traceability](discussion-traceability.md) marks each material proposition as accepted, active, proposed, provisional, open, deferred, rejected, or implemented and points to its current authority.

## Dwarf Fortress lesson

Dwarf Fortress did not obtain breadth from one small universal ontology. Its action space comes from a large semantic substrate, parameterized content, general systems, procedural instantiation, persistence, and accumulated interactions.

The reusable lesson is narrower:

- rules operate over categories and properties;
- one persistent object participates in several systems;
- reactions can derive outputs from input properties;
- ongoing processes keep changing persistent state;
- content composes only inside implemented mechanisms; and
- simulation resolution can be deliberately mixed.

The mixed-resolution lesson is architectural, not cosmetic: persistent systems do not need one shared cadence. Cheap world processes can continue at their natural rates while slower institutions and expensive resident cognition wake only when relevant. World Substrate should therefore target one canonical simulated timeline with independently scheduled mechanisms, while keeping render time, cognition cadence, and analysis cadence separate. See [multi-timescale execution](multi-timescale-execution-2026-09.md).

World Substrate adopts this compositional pattern without claiming comparable breadth.

## Castaway findings

The Castaway `world-systems` branch is the first concrete implementation donor.

It demonstrates:

- policies selecting typed actions while engine rules own effects;
- persistent vessels shared by bounded ownership, carrying, liquid, heat, material, and process systems;
- finite sources, liquid transfer, boiling, evaporation, cooling, spills, and hazards;
- data-only addition of an object when all required mechanics already exist;
- actor-local observation, bounded action pages, causal events, restart, and exact M1 replay; and
- separately labeled scripted and genuine-model evidence.

It also exposes scale limits. Sixty-nine colocated vessels produced 4,927 candidate actions and a 73.3 KB prompt in the retained measurement. Bounded presentation does not by itself bound candidate generation or visible-state context.

Castaway establishes the promoted M1 vertical. It does not prove cross-domain generality, global causal closure, or that exact replay should constrain future worlds.

## Linguistic Core findings

The Castaway review reused 18 predicates and 69 source entity types from Linguistic Core 0.3.0. The current subset is evidence that Linguistic Core can ground meaning, not evidence that the subset covers persistent world modeling.

The durable boundary is:

> Linguistic Core supplies predicate senses, participant roles, hierarchy, and semantic relationships. Installed mechanics supply persistence, quantities, required state, validation, authority, time, effects, and invariants.

The next audit must check state relations, qualities, identity/lifecycle, topology, containment, quantities/units, rights, and institutional relations across Linguistic Core and its donors before adding a new taxonomy. SUMO, FrameNet, PropBank, Wikidata properties, and QUDT are candidates, not automatic runtime authorities.

A semantic predicate is not automatically an engine action. The same vocabulary can describe primitives, autonomous processes, states, composites, declarations, institutions, or analytic patterns.

## Cybernetic Influence lineage findings

### V3

Cybernetic Influence V3 is the closest donor to the desired transition discipline. It contributes:

- one canonical persistent world separated from agent cognition;
- semantic intent separated from validated effect;
- transition authorities that propose patches;
- one validation-and-commit boundary;
- topology separated from routing, permission, perception, and success;
- derived macro-levels and analysis isolated from simulation authority;
- declared representation depth; and
- detailed causal traces.

Its negative result is equally important. The current general path uses open action prose without Linguistic Core sense/role binding, has only three exact general contract families, gives one joint LLM authority broad world access, and does not enforce declared read/write paths at commit. A cargo-transfer mechanic may ignore modeled truck, fuel, berth, customs, or labor state while remaining locally valid.

V3 therefore supplies a transition-envelope and observability donor, not a complete semantic or extensible-mechanics solution. Concordia is a lineage-specific lifecycle choice, not an architectural conclusion for World Substrate.

### V2 and the original repository

V2 supplies the stronger bounded-authority pattern: one local resolver for an attempted interface with an output envelope unable to express unrelated effects. World Substrate should generalize this as independently enforced state-path scope.

The original repository supplies a useful semantic complexity gate: promote a donor term into runtime structure only when it changes what exists, what can be perceived, what can be attempted, or what the world does next. Otherwise it belongs in language, scenario metadata, or analysis.

The lineage also warns against representing both a detailed organization and a coarse organizational surrogate as simultaneous causes of the same outcome.

## Agent Ecology lineage findings

Agent Ecology 2 is valuable primarily as a design and failure corpus.

Its strongest positive lessons are:

- an installed contract or institution can acquire genuine causal force;
- permission, access, control, beneficiary status, provenance, and physical possession are different relations;
- agents need discovery of mechanics, scope, requirements, and cost before attempting them; and
- a small kernel must expose real enabling primitives before agents can construct institutions.

Its strongest negative case is premature effect application. Contract state updates can be applied during permission checking before the enclosing action completes. Locally reasonable permission, pricing, invocation, and contract mechanisms therefore compose into an incoherent transition.

The corrective rule is:

> Applicability, authorization, payment, and institutional rules may propose effects, but only the enclosing causally coupled transition commits them after all checks succeed.

The broader Agent Ecology lineage warns that hardcoded cooperation, reciprocity, grudge, market, or organization rules demonstrate the consequences of installed policy. They do not establish that those patterns emerged from more primitive mechanics.

No Agent Ecology code is adopted by default.

## Data Contracts and Collective Competence findings

Data Contracts reinforces explicit boundaries, composition rules, validation surfaces, and compact observability at interfaces. Its value is in contract design rather than domain ontology or code extraction.

Collective Competence supplies the anti-double-counting distinction among:

- mechanism;
- capability;
- observed dynamics; and
- achieved outcome.

A measurable macro-pattern does not gain independent causal force merely because it can be named. A coarse surrogate may replace or summarize lower-level mechanisms, but it must declare the resolution it replaces and must not execute alongside them for the same causal responsibility.

## Global coherence

Global coherence is not mainly the problem of obtaining plausible equations. It is the problem of making independently authored mechanics share meanings, units, identity, update order, capability revocation, and authority.

A sealed clay pot can individually support heat, pressure, material strength, container damage, and fluid flow while the composition remains incoherent:

- pressure continues to rise after rupture;
- the broken pot remains sealed and retains container capability;
- water is simultaneously retained and leaked;
- quantity is duplicated or lost;
- mechanics use incompatible units or timing;
- heat and contents remain attached to an object that damage replaced with fragments; or
- two mechanics apply the same consequence.

A compiler can verify only dependencies and consequences the author declared. Call that **declared enforcement coverage**. A **causal-closure assay** must additionally inspect neighboring semantic state, compare mechanic graphs, search for overlapping authority, and generate interaction counterexamples. Its result is evidence with residual risk, not a proof of universal completeness.

## Mechanics-agent hypothesis

The central research hypothesis is that LLM-agent teams can expand a bounded world before a run by finding missing mechanics and producing reviewable packages faster than interaction complexity becomes unmanageable.

A useful package includes:

- Linguistic Core senses, roles, and causal classification;
- causal bearer;
- required state, optional modifiers, and incompatibilities;
- enforced reads, writes, effects, and scheduling;
- goal-relative invariants;
- dependencies and unsupported interactions;
- positive, refusal, boundary, interference, and double-application tests;
- representation limits and invalid questions; and
- a trace contract.

The installer validates the package and freezes a mechanics profile before simulation. Runtime invention or revision of world laws remains a later research problem.

## Observability and agent cognition

Observability is a product requirement. A builder should be able to inspect what a bearer observed or read, what it attempted, how it was semantically bound, which local mechanic applied, which checks ran, what committed, and why an attempt refused or failed.

Resident-agent memory, beliefs, uncertainty, plans, and private reasoning ordinarily remain in the agent runtime. The world contains the agent, delivered observations, externalized actions, and their consequences. Canonical `believes(...)` state is optional and should exist only when a selected mechanic needs an explicit belief representation.

Exact replay is an M1 capability and optional diagnostic, not a universal evidence requirement.

## Consolidated design consequences

1. Build the smallest persistent, observable vertical that tests one important uncertainty.
2. Separate semantic vocabulary, content, mechanics, policy, resident cognition, canonical state, and analysis.
3. Bind Linguistic Core senses and roles to a smaller set of causal primitives and processes.
4. Require a represented causal bearer and one locally scoped transition authority for every canonical write.
5. Let mechanics and institutions propose effects; let one enclosing transition commit causally coupled changes.
6. Keep entities open to unrelated components while keeping each mechanic's reads and writes closed.
7. Apply only goal-relative accounting and conservation invariants.
8. Permit offline agent-authored mechanics after review, installation, interaction assays, and profile freezing.
9. Make unsupported mechanics and residual closure risk visible.
10. Treat exact replay as an optional technique and M1 implementation fact.
11. Prove reuse with a materially different second world before making broad generality claims.
12. Add perturbation and scaling work only when its result can change the architecture.

## Open research questions

- What does Linguistic Core already provide for state relations, attributes/qualities, quantities, rights, and institutions?
- What is the smallest executable primitive set for the first target world?
- What is the smallest mechanics language that avoids a new compiler branch per family?
- How should simultaneous writes, precedence, capability revocation, and entity replacement compose?
- Which closure risks can typed contracts expose, and which require fallible semantic and adversarial review?
- What evidence is sufficient to freeze one agent-authored mechanic for an exploratory run?
- Which second world adds a genuinely different mechanism family?
- What concurrency semantics are required when resident agents deliberate concurrently but canonical writes contend?
- At what scale do indexing and observation selection become necessary?
