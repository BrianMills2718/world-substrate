# Semantic–mechanical binding contract v0

**Status:** target contract, six of seven M1 action kinds bound. `give`, `drink`, `heat`, `fill`, `take` and `pour` are bound in `src/world_substrate/semantic.py`, each citing a predicate and roles from the pinned Linguistic Core extraction. `unheat` is unbound and stays that way here: the extraction has no sense for removing a vessel from a heat source, and inventing one would break this contract's own rule that senses are cited rather than minted. The bound sense and roles **are** attached to every accepted action event as `semantic_binding`, and `null` on the unbound kind.  
**Purpose:** bind agent- or process-level meaning to an installed causal interface without allowing language to mutate the world

## Boundary

A semantic binding explains what an attempt or occurrence means. A mechanic determines whether and how it changes persistent state.

A conforming binding contains:

| Field | Requirement |
| --- | --- |
| `binding_id` | Stable identity for the binding |
| `sense_id` | Pinned Linguistic Core predicate sense or an explicitly reviewed overlay |
| `roles` | Sense-role to canonical entity/value references |
| `specialization` | Optional more specific sense or world-profile specialization |
| `causal_class` | Primitive action, autonomous process, state relation, composite, analytic pattern, declaration, or installed institution |
| `causal_bearer` | Agent, process, disposition, institution, or explicit exogenous input; absent for a purely derived view |
| `mechanic_id` | Installed mechanic selected for a state-changing binding; absent for a derived-only binding |
| `interpretation_limits` | Ambiguity, unsupported senses, or abstraction limits exposed to the trace |

Free text may accompany a binding but cannot substitute for the sense, roles, bearer, and mechanic identity required by the selected profile.

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
