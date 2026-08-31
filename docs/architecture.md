# World Substrate architecture

## Architectural thesis

A rich deterministic world comes from shared persistent state plus reusable transition and process rules. LLM sophistication is a policy concern and must not compensate for missing world mechanics.

```text
Content definitions ─┐
Ontology bindings ───┼─> compiler/registry ─> executable rule families
Rule definitions ────┘                              |
                                                     v
Agent policy <─ observation + affordances <─ canonical world ─> events/replay
       |
       └──────────── selects typed action ──────────>|
```

## Authority boundaries

| Boundary | Owns | Must not own |
| --- | --- | --- |
| Canonical world | state, revision, authoritative time, atomic commit | policy or narrative |
| Rule registry | action schemas, guards, effects, processes, source/sink declarations | world instances |
| Content packs | objects, properties, recipes, starting state, ontology bindings | new effects without rules |
| Affordance discovery | actor-local rule instantiation, filtering, paging | consequence calculation |
| Policy adapter | LLM, human, or scripted selection and explanation | state mutation |
| Persistence | commands, events, snapshots, versions, replay inputs | alternate effects |
| Authoring/compiler | reference integrity, rule binding, declared causal closure | silently generated executable code |
| Observer surfaces | canonical and historical projections | hidden simulation state |

## Composition model

An object has stable identity and typed components or properties. Rule families declare which components they read and write.

For example, a vessel may have:

- location and owner;
- material and mass;
- capacity and condition;
- liquid contents with extensive quantities;
- temperature;
- attachment to a heat source.

Independent rules can therefore transfer the vessel, transfer its contents, heat it, cool it, damage it, or include its mass in carrying capacity. Giving away a hot vessel transfers the same object with its heat and contents intact.

Adding a stone beaker is a content extension when all required properties already exist. Adding pressure is a mechanism extension because the substrate needs pressure state, sealed-volume rules, heating interaction, failure behavior, and evidence.

## Action model

A rule schema generates finite action instances from current local state. A policy never receives an abstract promise that it can “do anything.”

`pour(source, target, amount)`, for example, requires accessible compatible vessels, positive contents, free target capacity, and an allowed integer amount. The effect moves every conserved liquid component proportionally and emits before/after evidence.

The possible action space grows through combinations of objects, relations, parameters, and rules. Presentation may be bounded even when candidate generation is large. Candidate enumeration and observation size must be measured separately.

## Process model

Processes use the same objects and advance only under canonical time. Each declares:

- activation conditions;
- state read/write surface;
- timing;
- sources and sinks;
- ordering or conflict semantics;
- termination/interruption behavior; and
- causal events.

A fire checking for fuel but never deducting it is an incomplete rule. It is not an ontology failure.

## Authoring and causal closure

Authoring produces data, not executable source code. The compiler must distinguish:

- **exact:** every declared consequence is bound to registered mechanics;
- **descriptive:** context visible to agents or observers but execution-inert;
- **unsupported:** requested behavior has no rule and blocks an exact claim.

A valid schema cannot prove that the author remembered every real-world dependency. Semantic dependency review may identify omissions, but it remains fallible. The review surface must show declared coverage and unsupported mechanisms without calling the world universally complete.

## Determinism and replay

For an exact engine/content version, initial state, seed if permitted, and recorded action sequence, the final state and causal journal must match exactly. Replaying policy decisions is unnecessary; replay consumes recorded typed actions.

Rejected, invalid, and unsupported actions never partially mutate state. Their checks and reasons remain inspectable.

## Agent and observer separation

Actors see only authorized observations, known definitions, and bounded affordances. The observer may inspect full state, histories, hidden provenance, and alternative runs. Model explanations are retained as beliefs and cannot overwrite canonical truth.

## Dependency posture

- Castaway donates the first behavior and evidence vertical.
- Cybernetic Influence V3 donates selected authoring, transition, patch-validation, and evidence patterns.
- Linguistic Core is a pinned vocabulary dependency.
- Shared `llm_client` is the only planned model-provider seam.
- Concordia remains an evaluated optional lifecycle dependency, not a foundational commitment.
