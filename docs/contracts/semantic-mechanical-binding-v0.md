# Semantic–mechanical binding contract v0

**Status:** target contract, six of seven M1 action kinds bound. `give`, `drink`, `heat`, `fill`, `take` and `pour` are bound in `src/world_substrate/semantic.py`, each citing a predicate and roles from the pinned Linguistic Core extraction. `unheat` is unbound and stays that way here: the extraction has no sense for removing a vessel from a heat source, and inventing one would break this contract's own rule that senses are cited rather than minted. The bound sense and roles **are** attached to every accepted action event as `semantic_binding`, and `null` on the unbound kind.  
**Purpose:** bind agent- or process-level meaning to an installed causal interface without allowing language to mutate the world

<!-- status-facts
semantic_bindings_bound: 6
semantic_bindings_total: 7
unbound_action_kinds: [unheat]
semantic_binding_on_events: true
-->

## Boundary

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

## Predicate-local role compatibility

Linguistic Core now has a candidate M4 contract that distinguishes a reusable role concept such as `lc.role.theme` from a predicate-local role definition such as `lc.roledef.give_transfer.transferred_object`. World Substrate may cite those local role-definition IDs when reviewed, while retaining the existing `lc.role.*` grounding for compatibility.

The current first proof is `binding.give.v0`: `giver`, `transferred_object`, and `recipient` cite the candidate local roles for `lc:give_transfer`. The other bound M1 actions remain valid without local role-definition metadata until corresponding LC schemas are reviewed. `unheat` remains unbound; local role metadata cannot manufacture a missing predicate sense.

This does not move the semantic/mechanical boundary. `causal_class`, `causal_bearer`, `mechanic_id`, effects, read/write authority, scheduling, invariants, and commit/refusal semantics remain World Substrate concerns.

## Binding rules

1. Resolve the predicate sense rather than matching a surface word alone.
2. Validate participant roles against the sense signature and canonical references.
3. Classify whether the binding is causally primitive, processual, relational, composite, analytic, declarative, or institutionally enforced.
4. Require a represented causal bearer for every state-changing binding.
5. Select only a mechanic installed in the active frozen profile.
6. Do not execute a composite or analytic classification after its lower-level transitions have already committed.
7. Preserve failed or ambiguous bindings as observable refusals; do not guess a state change.

## Initial worked binding

For an ordinary transfer:

- sense: the reviewed Linguistic Core `give` sense;
- roles: giver, transferred object, recipient;
- causal class: primitive intentional action;
- bearer: the giver;
- mechanic: installed possession-transfer mechanic.

An observed reciprocal pair may later be classified as exchange. That derived classification performs no transfer. If an escrow institution couples the assets, the institution and its release transition receive their own binding and authority.

## Vocabulary coverage audit

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
