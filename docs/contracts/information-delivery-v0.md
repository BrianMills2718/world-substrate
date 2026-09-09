---
role: contract
status: implemented
reviewed_through: 2026-09-08
---

# Information and delivery v0

World Substrate can represent information as canonical world state without
turning information, private cognition, or later analysis into the same causal
thing.

The implemented v0 types are `InformationState` and `DeliveryState` in
`world_substrate.information`.

## Representation

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

## Observation rule

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

## Causality rule

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

## Current limits

v0 does not generically model channel latency, probabilistic delivery,
corruption, belief revision, deception detection, audience groups, information
expiration, or arbitrary provenance graphs. Extend the contract only when a
real world needs those distinctions.
