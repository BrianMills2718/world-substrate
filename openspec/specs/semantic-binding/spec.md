# semantic-binding Specification

## Purpose

How an action kind cites a reviewed Linguistic Core sense and roles without meaning ever implying an effect.

**Semantic–mechanical binding contract v0** (folded on 2026-11-09 from `docs/contracts/semantic-mechanical-binding-v0.md`, given in its Status line, last commit `be913a4`):

**Status:** target contract, six of seven M1 action kinds bound. `give`, `drink`, `heat`, `fill`, `take` and `pour` are bound in `src/world_substrate/semantic.py`, each citing a predicate and roles from the pinned Linguistic Core extraction. `unheat` is unbound and stays that way here: the extraction has no sense for removing a vessel from a heat source, and inventing one would break this contract's own rule that senses are cited rather than minted. The bound sense and roles **are** attached to every accepted action event as `semantic_binding`, and `null` on the unbound kind.  
**Purpose:** bind agent- or process-level meaning to an installed causal interface without allowing language to mutate the world

<!-- status-facts
semantic_bindings_bound: 6
semantic_bindings_total: 7
unbound_action_kinds: [unheat]
semantic_binding_on_events: true
-->

## Requirements

### Requirement: Boundary

A semantic binding explains what an attempt or occurrence means. A mechanic determines whether and how it changes persistent state.

A conforming binding contains:

| Field | Requirement |
| --- | --- |
| `binding_id` | Stable identity for the binding |
| `sense_id` | Pinned Linguistic Core predicate sense or an explicitly reviewed overlay |
| `roles` | Consumer participant name to reusable Linguistic Core `lc.role.*` identity |
| `role_definition_ids` | Optional profile metadata mapping participant names to predicate-local `lc.roledef.*` identities; keys must exactly match `roles`; intentionally not serialized by the v0 event binding |
| `specialization` | Optional more specific sense or world-profile specialization |
| `causal_class` | Primitive action, autonomous process, state relation, composite, analytic pattern, declaration, or installed institution |
| `causal_bearer` | Agent, process, disposition, institution, or explicit exogenous input; absent for a purely derived view |
| `mechanic_id` | Installed mechanic selected for a state-changing binding; absent for a derived-only binding |
| `interpretation_limits` | Ambiguity, unsupported senses, or abstraction limits exposed to the trace |

Free text may accompany a binding but cannot substitute for the sense, roles, bearer, and mechanic identity required by the selected profile. Predicate-local role-definition IDs are semantic compatibility metadata only: they refine which role position of a sense the consumer means, but they do not supply effects or authority. They are deliberately omitted from `SemanticBinding.as_dict()` in v0 so existing retained event/evidence identity remains stable; trace-level publication requires an explicit versioned contract/evidence change.

Source: inferred by agent (semantic-mechanical binding contract v0, applying Decision 003, accepted 2026-09-02). A human semantic review on 2026-09-12 kept the boundary while allowing richer Linguistic Core roles; its exact words were not recorded

#### Scenario: A binding describes, a mechanic acts

- **WHEN** an action kind carries a semantic binding
- **THEN** the binding explains what the attempt or occurrence means (`binding_id`, `sense_id`, `roles`, an optional `specialization`, `causal_class`, `causal_bearer`, `mechanic_id`, `interpretation_limits`), and only the mechanic decides whether and how persistent state changes
- **AND** free text may accompany a binding but cannot replace the sense, roles, bearer and mechanic identity the selected profile requires

#### Scenario: Role-definition IDs stay out of the event binding

- **WHEN** a binding carries optional `role_definition_ids`
- **THEN** their keys must exactly match `roles` and each must be an `lc.roledef.*` identity, or construction fails
- **AND** `SemanticBinding.as_dict()` leaves them out in v0, so retained event and evidence identity stays stable

### Requirement: Predicate-local role compatibility

Linguistic Core now has a candidate M4 contract that distinguishes a reusable role concept such as `lc.role.theme` from a predicate-local role definition such as `lc.roledef.give_transfer.transferred_object`. World Substrate may cite those local role-definition IDs when reviewed, while retaining the existing `lc.role.*` grounding for compatibility.

The current first proof is `binding.give.v0`: `giver`, `transferred_object`, and `recipient` cite the candidate local roles for `lc:give_transfer`. The other bound M1 actions remain valid without local role-definition metadata until corresponding LC schemas are reviewed. `unheat` remains unbound; local role metadata cannot manufacture a missing predicate sense.

This does not move the semantic/mechanical boundary. `causal_class`, `causal_bearer`, `mechanic_id`, effects, read/write authority, scheduling, invariants, and commit/refusal semantics remain World Substrate concerns.

Source: inferred by agent (semantic-mechanical binding contract v0, applying Decision 003, accepted 2026-09-02). A human semantic review on 2026-09-12 kept the boundary while allowing richer Linguistic Core roles; its exact words were not recorded

#### Scenario: The give binding cites predicate-local roles

- **WHEN** `binding.give.v0` is read
- **THEN** `giver`, `transferred_object` and `recipient` cite the local role definitions of `lc:give_transfer` (such as `lc.roledef.give_transfer.transferred_object`) alongside their `lc.role.*` roles
- **AND** the other bound actions remain valid without local role-definition metadata

#### Scenario: Local roles do not move the boundary

- **WHEN** a binding cites a predicate-local role definition
- **THEN** that is compatibility metadata only; `causal_class`, `causal_bearer`, `mechanic_id`, effects, authority, scheduling, invariants and commit and refusal semantics stay with World Substrate, and `unheat` stays unbound because local roles cannot create a missing sense

### Requirement: Binding rules

1. Resolve the predicate sense rather than matching a surface word alone.
2. Validate participant roles against the sense signature and canonical references.
3. Classify whether the binding is causally primitive, processual, relational, composite, analytic, declarative, or institutionally enforced.
4. Require a represented causal bearer for every state-changing binding.
5. Select only a mechanic installed in the active frozen profile.
6. Do not execute a composite or analytic classification after its lower-level transitions have already committed.
7. Preserve failed or ambiguous bindings as observable refusals; do not guess a state change.

Source: inferred by agent (semantic-mechanical binding contract v0, applying Decision 003, accepted 2026-09-02). A human semantic review on 2026-09-12 kept the boundary while allowing richer Linguistic Core roles; its exact words were not recorded

#### Scenario: A binding is resolved and checked

- **WHEN** an attempt is bound
- **THEN** the predicate sense is resolved rather than matched on a surface word, and the participant roles are validated against the sense signature and canonical references
- **AND** the binding is classified (primitive, processual, relational, composite, analytic, declarative or institutionally enforced), every state-changing binding has a represented causal bearer, and its mechanic is one installed in the active frozen profile

#### Scenario: A binding fails or is ambiguous

- **WHEN** a binding fails or is ambiguous
- **THEN** it is preserved as an observable refusal and no state change is guessed
- **AND** a composite or analytic classification is not executed after its lower-level transitions have already committed

### Requirement: Initial worked binding

For an ordinary transfer:

- sense: the reviewed Linguistic Core `give` sense;
- roles: giver, transferred object, recipient;
- causal class: primitive intentional action;
- bearer: the giver;
- mechanic: installed possession-transfer mechanic.

An observed reciprocal pair may later be classified as exchange. That derived classification performs no transfer. If an escrow institution couples the assets, the institution and its release transition receive their own binding and authority.

Source: inferred by agent (semantic-mechanical binding contract v0, applying Decision 003, accepted 2026-09-02). A human semantic review on 2026-09-12 kept the boundary while allowing richer Linguistic Core roles; its exact words were not recorded

#### Scenario: An ordinary transfer

- **WHEN** a giver gives an object to a recipient
- **THEN** the binding uses the reviewed `give` sense (`lc:give_transfer`) with roles giver, transferred object and recipient, causal class primitive intentional action, bearer the giver, and the installed possession-transfer mechanic (`mechanism.ownership.give`)

#### Scenario: A reciprocal pair

- **WHEN** an observed reciprocal pair of gives is later classified as exchange
- **THEN** that derived classification performs no transfer
- **AND** if an escrow institution couples the assets, the institution and its release transition get their own binding and authority

### Requirement: Vocabulary coverage audit

Before adding a new overlay term, inspect Linguistic Core and its donors for:

- persistent state relations;
- identity and lifecycle;
- location, topology, containment, and routing;
- possession, custody, access, control, title, beneficiary, and transfer authority;
- material qualities, damage, and capabilities;
- quantities, dimensions, and units;
- temporal validity and process roles; and
- institutional roles and enforceable relations.

SUMO, FrameNet, PropBank, Wikidata properties, and QUDT are candidate donors. They are not automatically runtime authorities.

Source: inferred by agent (semantic-mechanical binding contract v0, applying Decision 003, accepted 2026-09-02). A human semantic review on 2026-09-12 kept the boundary while allowing richer Linguistic Core roles; its exact words were not recorded

#### Scenario: A new overlay term is proposed

- **WHEN** someone proposes a new overlay term
- **THEN** Linguistic Core and its donors are first inspected for persistent state relations, identity and lifecycle, location and routing, possession and control, material qualities, quantities and units, temporal validity and process roles, and institutional roles
- **AND** SUMO, FrameNet, PropBank, Wikidata properties and QUDT are candidate donors only, not runtime authorities

### Requirement: Whole attempt coverage

Fresh open-attempt interpretations MUST assess whether one identified operation represents the whole utterance, before binding even a wait. The existing interpreter call MUST return coverage status (`complete`, `requires_decomposition`, `partial`, or `ambiguous`), exact nonblank action substrings, and exact nonblank unrepresented substrings. Complete requires an identified operation and no unrepresented spans; incomplete requires unrepresented spans, and only ambiguous may have no identified action span. Missing or malformed fresh assessments MUST fail closed. Exact quote checks validate evidence shape, not semantic truth.

A concrete means MUST be bound rather than substituted with the goal it serves. Expressed stance, assent and withholding or revoking assent MUST remain distinct. Quoted speech, coordinated instruments, motives and expected consequences do not themselves add independent operations. An impossible single operation remains complete and is submitted to the installed mechanics.

An incomplete interpretation MUST preserve the original utterance and available coverage, execute no part, invoke no rule judge and deliver no request. The actor MUST receive a constant clarification without privileged model reasoning; analyst evidence retains the reading. A complete operation with no installed rule remains eligible for the existing unmatched-attempt judge/request path. Historical records without coverage MUST remain readable without inventing an assessment.

Source: inferred by agent from production5 (2026-11-13), Q36 and Brian's approval “i approve proceed” after the recommended compound-attempt follow-up; technical defaults implement the approved bounded correction.

#### Scenario: A concrete recording serves a goal

- **WHEN** someone says “withhold assent by recording a concern” and an installed kind represents recording concern
- **THEN** the interpreter binds that recording rather than revoking assent; the installed rule alone decides its effects

#### Scenario: Multiple independent operations have no installed composite

- **WHEN** someone tries to repair a condition and send a separate request, and no installed composite covers both
- **THEN** coverage requires decomposition, no part is executed, no judge is called and no request reaches another actor
- **AND** the original text and coverage remain inspectable and the actor receives safe clarification

#### Scenario: An installed composite covers the request

- **WHEN** one installed composite kind and its fields represent the complete request
- **THEN** it may bind as one operation and its installed mechanics decide atomically

#### Scenario: Content and consequences are not extra operations

- **WHEN** an attempt reports quoted content with several verbs, uses coordinated instruments, or expects knock-on consequences
- **THEN** these do not alone require decomposition; an impossible identified single operation still reaches the installed rule checks

#### Scenario: Fresh missing assessments and historical unassessed readings differ

- **WHEN** a fresh model response omits or malforms coverage
- **THEN** it is retained as an interpretation rejection with no action, judge or request effect
- **AND** an older recorded reading without coverage remains readable without claiming a newly assessed interpretation
