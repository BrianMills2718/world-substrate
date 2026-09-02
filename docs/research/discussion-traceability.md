---
role: research-traceability
status: active
reviewed_through: 2026-09-02
authority_refs:
  - ../../roadmap/README.md
  - ../architecture.md
  - ../decisions/001-project-scope.md
  - ../decisions/002-observability-and-replay.md
  - ../decisions/003-semantic-mechanical-boundary.md
---

# World Substrate discussion traceability

This index maps the 2026-09-02 strategy discussion and donor reviews to their current repository disposition. It preserves institutional memory without making a research ledger into a competing roadmap.

## Status vocabulary

| Status | Meaning |
| --- | --- |
| **accepted** | Project doctrine recorded in an accepted decision or authoritative architecture |
| **active** | Selected by the canonical roadmap as current work |
| **proposed** | A target contract or design that has not been implemented |
| **provisional** | Useful working classification subject to donor or implementation evidence |
| **open** | Requires research, evidence, or a human choice |
| **deferred** | Intentionally outside the current version |
| **rejected** | Explicitly excluded as a project requirement or architecture direction |
| **implemented** | Exists in code/tests; the associated claim remains bounded to that implementation |

## Core strategy

| Discussion proposition | Status | Authoritative destination | Notes |
| --- | --- | --- | --- |
| Persistent canonical world state is fundamental | **accepted** | [Architecture](../architecture.md), [Decision 001](../decisions/001-project-scope.md) | Resident cognition and analysis do not become competing world truth |
| Observability is a core product requirement | **accepted** | [Decision 002](../decisions/002-observability-and-replay.md) | Traces expose observation/read, attempt, binding, authority, checks, effects, refusal, and result |
| Determinism and exact reproducibility are not product goals | **accepted** | [Decision 002](../decisions/002-observability-and-replay.md) | M1 replay remains an implemented fact and optional diagnostic |
| Policies and natural-language prose do not directly mutate canonical state | **accepted** | [Decision 001](../decisions/001-project-scope.md), [Architecture](../architecture.md) | Installed mechanics determine consequences |
| Linguistic Core is the semantic sense-and-role interface | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) | It does not supply persistence, effects, scheduling, or invariants |
| Existing ontologies should be inspected before inventing classifications | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md), [semantic binding proposal](../contracts/semantic-mechanical-binding-v0.md) | SUMO, FrameNet, PropBank, Wikidata properties, and QUDT are candidate donors |
| A linguistic predicate is not automatically an executable primitive | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) | Binding classification remains provisional |
| Only represented bearers with independent causal force write canonical state | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) | Bearers include agents, processes, dispositions, institutions, and explicit exogenous inputs |
| Composite and emergent descriptions must not double-apply primitive effects | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) | Collective Competence is the main theory donor |
| One enclosing transition owns each causally coupled commit | **accepted** | [Architecture](../architecture.md), [transition envelope proposal](../contracts/transition-envelope-v0.md) | This is narrower than universal ACID |
| Accounting and conservation are goal-relative | **accepted** | [Decision 002](../decisions/002-observability-and-replay.md), [mechanic profile proposal](../contracts/mechanic-profile-v0.md) | No universal mass/energy requirement |
| Pre-run mechanics-agent authoring is the initial extensibility hypothesis | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md), [Roadmap](../../roadmap/README.md) | Installer review and a frozen profile precede a run |
| Runtime installation or revision of world laws | **deferred** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) | Prospective installation, retroactive correction, branching, and technology-local invention remain future research |

## Semantic and causal model

| Discussion proposition | Status | Repository destination | Remaining question |
| --- | --- | --- | --- |
| Primitive action, autonomous process, state relation, composite, analytic pattern, declaration, and installed institution form a useful binding classification | **provisional** | [Semantic binding proposal](../contracts/semantic-mechanical-binding-v0.md) | Does an existing donor ontology provide a better classification? |
| Causal-force counterfactual test | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) | Application to particular social and institutional terms remains case-specific |
| Ordinary exchange consists of independently initiated gives | **accepted direction** | [Roadmap M2](../../roadmap/README.md) | Must be established by implementation evidence |
| One participant may give while the other reneges | **active** | [Roadmap M2](../../roadmap/README.md) | Required negative scenario |
| A derived exchange classification performs no additional transfers | **active** | [Roadmap M2](../../roadmap/README.md) | Required anti-double-application test |
| Escrow may acquire causal force and couple transfers | **proposed later slice** | [Transition envelope proposal](../contracts/transition-envelope-v0.md), [Roadmap M5](../../roadmap/README.md) | Exact institution and rights model remain open |
| Substrate physics, installed institutions, resident cognition, and analytic interpretation are distinct layers | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md), [Architecture](../architecture.md) | Selected worlds may explicitly represent only the cognition needed by a mechanic |
| Agent beliefs, uncertainty, memory, and plans ordinarily remain in the resident runtime | **accepted** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) | No required canonical `believes(...)` relation |
| Provenance, possession, custody, access, control, title, beneficiary, and transfer authority should remain distinct when material | **provisional** | [Semantic binding proposal](../contracts/semantic-mechanical-binding-v0.md), [Roadmap M2 audit](../../roadmap/README.md) | Which distinctions are required by the selected scenario? |
| M1 `owner` is bounded operational possession/control, not universal legal ownership | **accepted claim boundary** | [Reference worlds](../../reference_worlds/README.md), [Roadmap M2 audit](../../roadmap/README.md) | Later rights decomposition must not silently reinterpret old evidence |
| Attributes need not be a new top-level ontology category | **open** | [Research synthesis](synthesis.md) | Donors may represent them as relations, qualities, functions, quantities, or components |
| Birthplace, parenthood, citizenship, headquarters, and similar state relations require a coverage audit before adding an overlay | **open** | [Semantic binding proposal](../contracts/semantic-mechanical-binding-v0.md) | Determine whether Linguistic Core or a donor already supplies each sense/relation |

## Mechanics and composition

| Discussion proposition | Status | Repository destination | Notes |
| --- | --- | --- | --- |
| Entities remain open to unrelated components while each mechanic has closed local authority | **proposed** | [Mechanic profile v0](../contracts/mechanic-profile-v0.md) | `requires`, `optional_modifiers`, and `forbids` do not define a closed global schema |
| Mechanics declare and enforce state-path reads and writes | **proposed** | [Mechanic profile v0](../contracts/mechanic-profile-v0.md), [Transition envelope v0](../contracts/transition-envelope-v0.md) | Broad valid JSON is not an authority boundary |
| Mechanics propose effects rather than mutate during validation | **proposed** | [Transition envelope v0](../contracts/transition-envelope-v0.md) | Inspired by AE2 failure and Cybernetic Influence V3 boundary |
| Offline mechanics agents may produce declarative packages or executable source | **accepted direction** | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) | Installation requires scope, interaction evidence, limitations, and profile freezing |
| Every mechanic package states representation depth and invalid questions | **proposed** | [Mechanic profile v0](../contracts/mechanic-profile-v0.md) | Exact, stochastic, empirical, scripted, external, and bounded model-mediated forms may share an interface |
| Declared enforcement coverage is compiler-checkable | **proposed** | [Architecture](../architecture.md), [Mechanic profile v0](../contracts/mechanic-profile-v0.md) | It covers only what the author declared |
| Global causal closure cannot generally be proven from declarations | **accepted risk** | [Architecture](../architecture.md), [Research synthesis](synthesis.md) | Missing truck, fuel, berth, customs, or labor dependencies are the canonical donor example |
| Causal closure should be an assay with residual-risk reporting | **proposed** | [Roadmap M4](../../roadmap/README.md) | Combine semantic inspection, dependency comparison, write-overlap analysis, and adversarial interactions |
| Interaction complexity is potentially combinatorial rather than one mechanic per predicate | **accepted motivation** | [Strategy ledger](world-substrate-strategy-session.md), [Research synthesis](synthesis.md) | The empirical question is whether agent teams can grow coherent coverage faster than integration risk grows |
| The sealed-pot interaction is the reference physical coherence example | **research example** | [Architecture](../architecture.md), [Strategy ledger](world-substrate-strategy-session.md) | Heat, pressure, strength, damage, containment, and flow can be locally valid yet globally inconsistent |

## Roadmap traceability

| Candidate work | Current disposition | Reason |
| --- | --- | --- |
| Audit M1 against semantic and causal boundaries | **active within M2** | Reuse existing evidence before broadening |
| Hand-bind `give`; derive exchange; demonstrate reneging | **active M2** | Establish one trusted semantic/transition reference |
| Genuine LLM policy consumer | **conditional enabling experiment** | Does not test the principal mechanics-authoring uncertainty; still requires model-call authority and spend cap |
| First offline agent-authored adjacent mechanic | **conditional M3** | Begins only after binding, authority, commit, and observability work together |
| Causal-coherence assay | **conditional M4** | Immediately stress the hand-built and agent-authored mechanics |
| Rights decomposition and installed escrow institution | **conditional M5 area** | Ordering may change after M2/M3 evidence |
| Non-agent autonomous process | **conditional M6 area** | Required to avoid an agent-only causal model |
| Second materially different world | **human decision later** | Must test actual reuse rather than cosmetic content variation |
| Runtime law changes | **deferred** | Not required to test the central pre-run authoring hypothesis |
| Scale and dynamical evaluation | **deferred** | Activate only when measurements can change an architecture decision |

The roadmap remains authoritative for ordering. Earlier slice sequences in the strategy ledger are alternatives considered during discussion, not accepted plans.

## Donor traceability

| Donor | Preserved research record | Principal retained lesson | Code adopted? |
| --- | --- | --- | --- |
| Castaway | [Research synthesis](synthesis.md) and M1 evidence | Persistent shared objects and composed physical mechanics | Bounded M1 path only |
| Linguistic Core | [Strategy ledger](world-substrate-strategy-session.md), [Research synthesis](synthesis.md) | Semantic senses and roles need explicit mechanical binding | Pinned semantic subset, not inferred mechanics |
| Agent Ecology 2 | [Targeted review](agent-ecology2-review.md) | Rights distinctions, installed institutions, premature-effect failure, singular commit | No |
| Agent Ecology and Agent Ecology 3 | [Strategy ledger](world-substrate-strategy-session.md) | Hardcoded social policy is not emergence; broad architectures can conceal conflicting authority | No |
| Cybernetic Influence V3/V2/original | [Lineage review](cybernetic-influence-lineage-review.md) | Canonical intent/patch/commit, local bounded authority, derived macro-levels, explicit closure gap | No |
| Data Contracts | [Strategy ledger](world-substrate-strategy-session.md), [Research synthesis](synthesis.md) | Explicit compositional boundaries and compact observability | No |
| Collective Competence | [Strategy ledger](world-substrate-strategy-session.md), [Research synthesis](synthesis.md) | Do not double-count mechanism, capability, dynamics, and outcome | No |
| Dynamical Laboratory | [Research synthesis](synthesis.md) | Perturbation and representation comparisons belong after executable worlds | No |

## Rejected directions

| Direction | Status | Reason |
| --- | --- | --- |
| Implement one independent mechanic for every Linguistic Core predicate | **rejected** | Predicates include states, composites, declarations, and analytic descriptions; interactions dominate raw predicate count |
| Let ontology type labels branch directly into effects | **rejected** | Semantic vocabulary does not confer causal authority |
| Let a joint LLM adjudicator edit the full canonical world | **rejected as default architecture** | Broad scope defeats local authority and makes omissions difficult to detect |
| Treat exchange, trust, cooperation, organizations, or collective competence as automatic additional causes | **rejected** | Derived descriptions would double-apply lower-level behavior |
| Require universal conservation of mass and energy | **rejected** | Invariants are selected relative to the simulation goal and representation |
| Require determinism, exact replay, or event-sourced reconstruction | **rejected** | Observability is the actual product requirement |
| Require a universal canonical belief schema | **rejected** | Cognition belongs to resident agents unless explicitly mechanized |
| Treat agent-generated simulation results as real-world prediction | **rejected product claim** | Predictive validity is not the project goal |
| Adopt donor code merely because its ideas are useful | **rejected** | Donors remain read-only unless a later consumer path justifies narrow adoption |

## Unresolved provenance and coverage

- “Company planning” was mentioned as an idea donor during discussion, but the exact GitHub repository was not conclusively identified. No revision-bound claim is attributed to it yet.
- The session ledgers preserve the substantial written analysis created during the discussion. They are not a verbatim export of every chat message.
- If a ledger conflicts with an accepted decision, the decision wins. If it conflicts with the roadmap on ordering, the roadmap wins. If it claims implemented behavior that code/tests do not support, code and evidence win.

## Research records

- [World Substrate theory and strategy session](world-substrate-strategy-session.md)
- [Agent Ecology 2 targeted review](agent-ecology2-review.md)
- [Cybernetic Influence lineage review](cybernetic-influence-lineage-review.md)
- [Current research synthesis](synthesis.md)
