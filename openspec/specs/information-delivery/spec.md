# information-delivery Specification

## Purpose

Represented information and its delivery to observers, kept separate from private cognition and from causal parentage.

**Information and delivery v0** (folded on 2026-11-09 from `docs/contracts/information-delivery-v0.md`, status `implemented`, reviewed through 2026-09-08, last commit `72fb4d8`):

World Substrate can represent information as canonical world state without
turning information, private cognition, or later analysis into the same causal
thing.

The implemented v0 types are `InformationState` and `DeliveryState` in
`world_substrate.information`.

## Requirements

### Requirement: Representation

An information item records:

- represented content;
- `source_id`;
- `channel_id`;
- `visibility` (`direct` or `public` in v0);
- an optional topic;
- an optional `derived_from_info_id` lineage edge; and
- whether the item is active in the represented world.

A delivery records:

- the information item;
- recipient;
- channel;
- status (`pending`, `delivered`, or `observed` are the v0 states consumed by
  the visibility seam); and
- the canonical tick at delivery when available.

These records are world facts only because a selected world chooses to
represent them. They do not imply a resident belief state.

Source: inferred by agent (information and delivery v0, applying Decision 003, accepted 2026-09-02). Same-moment reactions get a causal parent under Decision 009: Brian, 2026-10-26: "i approve"

### Requirement: Observation rule

For actor-local observation:

1. a represented source can inspect its own information item;
2. a direct recipient does not receive the item or its delivery record until
   the delivery is `delivered` or `observed`;
3. a public active item is visible to local actors; and
4. unrelated actors do not gain a direct item merely because it exists in
   canonical state.

The Waltzman acceptance fixture proves asymmetric delivery: a system briefing
can be delivered to Mara without Ari seeing it, and a later represented Mara →
Ari message becomes visible to Ari only after the communication mechanic
commits.

Source: inferred by agent (information and delivery v0, applying Decision 003, accepted 2026-09-02). Same-moment reactions get a causal parent under Decision 009: Brian, 2026-10-26: "i approve"

### Requirement: Causality rule

Information lineage and hard causal ancestry are distinct.

Engine events may retain `information_context` derived from the actor's bounded
observation. That means the information was represented in the actor's context;
it does **not** claim the information mechanically caused the action.

A rule may opt into `DeclaresCausalParents` or
`DeclaresProcessCausalParents` and name retained event IDs only when that rule
mechanically consumes or otherwise explicitly justifies those parents. The
Engine stores those IDs as `causal_parent_event_ids` separately from
`information_context`.

Temporal precedence and prompt inclusion are insufficient to promote a message
to hard ancestry.

Source: inferred by agent (information and delivery v0, applying Decision 003, accepted 2026-09-02). Same-moment reactions get a causal parent under Decision 009: Brian, 2026-10-26: "i approve"

### Requirement: Current limits

v0 does not generically model channel latency, probabilistic delivery,
corruption, belief revision, deception detection, audience groups, information
expiration, or arbitrary provenance graphs. Extend the contract only when a
real world needs those distinctions.

Source: inferred by agent (information and delivery v0, applying Decision 003, accepted 2026-09-02). Same-moment reactions get a causal parent under Decision 009: Brian, 2026-10-26: "i approve"

### Requirement: Same-moment reactions cite their cause (current code)

A same-moment knock-on reaction cites as its hard causal parent the latest event of the same moment it reacts to (`Engine._settle`, `src/world_substrate/engine.py:938-972`). A moment that would need more than 32 reactions (`REACTION_LIMIT`, `engine.py:1153`) or a reaction that would break a declared law is refused whole.

Source: Decision 009, Brian, 2026-10-26: "i approve"
