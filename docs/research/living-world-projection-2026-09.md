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

The authorized standalone URL is `https://brianmills.dev/world-substrate-visualization/`. Its currently deployed surface is the earlier synthetic prototype, versioned at `prototypes/living-world-overlay-v0.html` (SHA-256 `95def20d0225a0f3df4ad25a6dd4f64853b8a7404351a871ae76f376d4443288`). The repository now also implements `world-substrate-live-projection/v0` and an integrated Waltzman client that reconstructs baseline/intervention worlds from canonical initial snapshots plus retained event deltas, with optional JSON/SSE delivery. See [live projection v0](../contracts/live-projection-v0.md) and the [Waltzman audit](../audits/waltzman-coordination-lab-v0.md).

The product decision is now made: **replace the synthetic standalone public surface with the canonical Waltzman client at the existing URL and retain the synthetic prototype as versioned design evidence.** The first public demo may use the already-generated self-contained `evidence/renders/waltzman-demo-v0.html`, which embeds the canonical projection bundles; the JSON/SSE service is useful for the live observer seam but is not a prerequisite for that first publication. Integration into World Builder is a later product choice, not a demo blocker.

## Base world and overlays

The base layer remains the spatial world: places, residents, represented objects, and visible activity. Turning overlays off must not make ordinary world events disappear. A conversation, vehicle movement, meeting, transfer, failure, or machine operation is world activity first.

Core overlays are generic simulation projections:

- **Residents** — canonical actors and their current represented locations/presentation homes.
- **Information** — represented sources, recipients, channels, deliveries, provenance, and visibility.
- **Resources** — represented stocks, capacity, reservations, transfers, shortages, and bottlenecks.
- **Processes** — scheduled/running autonomous processes and their current phase.
- **Authority** — represented permissions, jurisdictions, institutions, commitments, and decision procedures.
- **Causal focus/history** — mechanic-declared ancestry for selected consequences and recent committed transitions.

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

A later action may retain that R19 was in Ari's authorized observation/context. If an installed mechanic explicitly declares that it consumes or depends on R19, that relation can be retained as hard causal parentage inside the represented world. If a resident harness merely saw R19 before selecting an action, R19 is retained evidence/context unless the cognition system supplies a narrower attributable reason. The UI must not turn temporal precedence or prompt inclusion into stronger causal claims.

Current `causal_parent_event_ids` are mechanic-declared and validated against retained history; they are not automatically derived from instrumented reads. They explain the installed world's causal account, not scientific truth about the corresponding real-world phenomenon.

The event/evidence model therefore needs to distinguish at least:

- mechanic-declared hard causal parentage;
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

## Implemented live projection seam

The implemented projection adapter turns a real World Substrate run into:

- current world/run identity, tick, and revision;
- canonical entity/component state needed for presentation;
- scene/profile semantics and stable visual identities;
- retained events/deltas with their event IDs and statuses;
- mechanically grounded causal/evidence relations that the current contracts can actually support; and
- explicit unsupported/unknown overlay categories rather than guessed semantics.

The browser consumes an initial snapshot plus incremental event/delta data. SSE is sufficient for the first one-way live view; WebSocket remains unnecessary unless later interaction requires bidirectional low-latency transport.

No renderer callback may mutate the World. Presentation animation state, camera state, selection, and interpolation remain client-local.

## First vertical acceptance — satisfied

The early design proposed Repair Bay as the first real-run fixture. The accepted implementation has moved beyond that stepping stone: the Waltzman Coordination Lab now drives the living client from canonical World Substrate snapshot/event data and satisfies the stronger integrated gate.

Current acceptance evidence includes:

1. baseline and intervention branches reconstruct from the initial snapshot plus retained deltas;
2. canonical entity IDs, event IDs, tick/revision, and state changes come from the Engine path rather than a synthetic UI timeline;
3. the browser can play, pause, step, scrub, switch branches, and select events without changing canonical truth;
4. information context and mechanic-declared causal parentage are displayed separately;
5. constraints/institution state and detachable Waltzman analysis are visible in the same living-world surface; and
6. the same projection data is available as a self-contained static artifact and through the optional JSON/SSE service.

The immediate product move is publication of that accepted canonical client at the existing standalone visualization URL, not another projection-framework experiment.
