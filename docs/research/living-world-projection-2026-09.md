---
role: research-design
status: active
reviewed_through: 2026-09-08
authority_refs:
  - ../../roadmap/README.md
  - ../architecture.md
  - ../decisions/004-product-and-adoption-strategy.md
  - technology-procurement-2026-09.md
---

# Living-world projection — one world, dynamic semantic overlays

## Purpose

World Substrate should feel like a living world rather than a trace viewer while preserving the rule that presentation never becomes a second source of truth. The primary experience is one persistent spatial scene. Core semantic overlays are drawn on that same scene and update as canonical state and retained events change.

The authorized standalone prototype is deployed at `https://brianmills.dev/world-substrate-visualization/` and versioned at `prototypes/living-world-overlay-v0.html` (SHA-256 `95def20d0225a0f3df4ad25a6dd4f64853b8a7404351a871ae76f376d4443288`). That public surface still uses its original synthetic timeline. The repository now also implements `world-substrate-live-projection/v0` and an integrated local Waltzman client that reconstructs baseline/intervention worlds from canonical initial snapshots plus retained event deltas, with JSON/SSE delivery. See [live projection v0](../contracts/live-projection-v0.md) and the [Waltzman audit](../audits/waltzman-coordination-lab-v0.md). Public replacement remains a separate deployment authority decision.

## Base world and overlays

The base layer remains the spatial world: places, residents, represented objects, and visible activity. Turning overlays off must not make ordinary world events disappear. A conversation, vehicle movement, meeting, transfer, failure, or machine operation is world activity first.

Core overlays are generic simulation projections:

- **Residents** — canonical actors and their current represented locations/presentation homes.
- **Information** — represented sources, recipients, channels, deliveries, provenance, and visibility.
- **Resources** — represented stocks, capacity, reservations, transfers, shortages, and bottlenecks.
- **Processes** — scheduled/running autonomous processes and their current phase.
- **Authority** — represented permissions, jurisdictions, institutions, commitments, and decision procedures.
- **Causal focus/history** — mechanically supported ancestry for selected consequences and recent committed transitions.

Analytic overlays are plugins, not universal world state. Waltzman trust structure, perceived risk, and coordination readiness belong here, as do future Levin, logistics, epidemiology, market, command-and-control, or other lenses.

## Time in the projection

The client may animate at arbitrary frame rates and expose playback speeds such as 1x/10x/100x, but those controls are presentation only. It follows canonical simulation timestamps/ticks/events and may interpolate between them; it cannot manufacture elapsed world time. As the runtime grows beyond the current integer-tick baseline, the same projection should support independently timed activities/processes without changing this authority rule. See [multi-timescale execution](multi-timescale-execution-2026-09.md).

## Information is not the same thing as causal ancestry

If Mara speaks to Ari, the simulation may retain several distinct facts:

```text
world interaction: Mara speaks to Ari
information representation: utterance R19
source: Mara
recipient: Ari
channel: conversation
observation/delivery: Ari receives R19
```

Those are canonical world/information events when the selected world represents them. They do **not** automatically prove that R19 caused Ari's later choice.

A later action may retain that R19 was in Ari's authorized observation/context. If an exact mechanic mechanically reads or depends on R19, that dependency can be a hard causal parent. If a resident harness merely saw R19 before selecting an action, R19 is retained evidence/context unless the cognition system supplies a narrower attributable reason. The UI must not turn temporal precedence or prompt inclusion into stronger causal claims.

The event/evidence model therefore needs to distinguish at least:

- hard mechanical causal parentage;
- information delivery / observation lineage;
- evidence/context available to cognition; and
- derived analytic interpretation.

## Relationship lifecycle for projection

For many overlay kinds the UI should distinguish four projection states:

| Projection state | Meaning |
| --- | --- |
| **possible** | installed structure permits the relationship/process |
| **enabled** | current state makes it available/applicable now |
| **active** | it is currently operating, binding, in transit, or underway |
| **realized** | a retained event says it actually happened in the selected history window |

Examples:

- information: channel exists → recipient reachable → message in transit/conversation underway → delivery retained;
- causality: mechanic dependency exists → mechanic applicable → prerequisite currently binding → committed event retained;
- resources: route/capacity relationship exists → currently usable → transfer underway → delivery/consumption retained;
- authority: rule/jurisdiction exists → currently applicable → decision/authorization in progress → authorization/refusal retained.

These are projection states derived from canonical state, installed mechanics, and history. They are not new world truth.

## Selected rendering stack

Decision 004 and the technology-procurement note select deck.gl 9.4.x as the default living-world projector. Schematic worlds use `OrthographicView`; real geography may add MapLibre. Cytoscape.js is reserved for a deliberately expanded non-spatial graph inspector rather than replacing the living spatial world.

The intended client shape is additive:

```text
base world
residents
information structure / activity / history
resources
processes
authority
causal focus / history
selection + explanation
analysis-plugin annotations
```

Cross-selection must preserve canonical entity/event IDs. Selecting an actor or event should filter/highlight relevant overlay data without inventing new relationships.

## Proposed live projection seam

The first implementation should be deliberately small. A projection adapter should turn a real World Substrate run into:

- current world/run identity, tick, and revision;
- canonical entity/component state needed for presentation;
- scene/profile semantics and stable visual identities;
- retained events/deltas with their event IDs and statuses;
- mechanically grounded causal/evidence relations that the current contracts can actually support; and
- explicit unsupported/unknown overlay categories rather than guessed semantics.

The browser needs an initial snapshot plus an incremental event/delta stream. SSE is sufficient for the first one-way live view; WebSocket is unnecessary unless later interaction requires bidirectional low-latency transport.

No renderer callback may mutate the World. Presentation animation state, camera state, selection, and interpolation remain client-local.

## First vertical acceptance

The first integration should use an existing real World Substrate run rather than adding another world mechanic. Repair Bay is a suitable fixture because it has multiple actors, contested tools, accepted/refused/retried actions, and retained full logs.

Acceptance for the first slice:

1. the versioned prototype consumes a real World Substrate snapshot/run instead of its synthetic state table;
2. canonical entity IDs, event IDs, tick/revision, and accepted/refused results match the retained trace exactly;
3. the browser can play, pause, step, scrub, and select residents/events without changing canonical truth;
4. movement/state visuals are derived through scene semantics rather than hard-coded Repair Bay entity logic;
5. causal highlighting never treats ordinary observation/context as hard mechanical causation;
6. information/conversation overlays remain absent or explicitly unsupported until first-class information semantics exist;
7. complete request/response logs and retained traces remain the debugging source of truth.

Once that is green, the next generic capability is first-class information/conversation representation and delivery. That unlocks genuinely visible agent interaction, provenance-aware information overlays, and the Waltzman Coordination Lab without making Waltzman constructs part of the core world.
