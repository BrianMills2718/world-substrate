# live-projection Specification

## Purpose

The one-way observer seam from canonical history to a living client: a snapshot plus incremental canonical events and deltas.

**Live projection v0** (folded on 2026-11-09 from `docs/contracts/live-projection-v0.md`, status `implemented`, reviewed through 2026-09-08, last commit `72fb4d8`):

The live projection is a one-way observer seam from canonical World Substrate
history to a living client. It never becomes a second world authority.

`world_substrate.projection` implements the v0 seam.

## Requirements

### Requirement: Wire shape

`schema_version` is `world-substrate-live-projection/v0`.

A projection bundle contains:

- one `world-substrate-snapshot/v1` initial snapshot;
- the ordered retained Engine events with stable event IDs and leaf deltas;
- a branch ID;
- downstream scene/presentation metadata;
- optional event annotations;
- optional detachable analysis; and
- optional bounded causal-adequacy reporting.

The material world at any event can be reconstructed by applying each retained
`changes` row to the initial material state in order. The Waltzman acceptance
fixture verifies that this reconstruction equals the final canonical material
world and hash for both baseline and intervention branches.

Source: inferred by agent (live projection v0, applying Decision 002, accepted 2026-09-02; the decider is not recorded)

#### Scenario: A projection bundle carries its parts

- **WHEN** a live projection bundle is built
- **THEN** its `schema_version` is `world-substrate-live-projection/v0`
- **AND** it contains one `world-substrate-snapshot/v1` initial snapshot, the ordered retained Engine events with stable event IDs and leaf deltas, a branch ID and downstream scene and presentation metadata, plus optional annotations, detachable analysis and bounded causal-adequacy reporting

#### Scenario: The world can be rebuilt from the bundle

- **WHEN** each retained `changes` row is applied in order to the initial material state
- **THEN** the material world at any event is reconstructed
- **AND** for the Waltzman acceptance fixture, the reconstruction equals the final canonical material world and hash on both the baseline and the intervention branch

### Requirement: Authority

The client may play, pause, step, scrub, select, filter, change camera/layout,
or toggle overlays. None of those operations commits a World transition.

Scene coordinates and labels are presentation facts. Canonical IDs, revisions,
ticks, outcomes, state changes, observations, and causal parents come from the
retained Engine trace.

Source: inferred by agent (live projection v0, applying Decision 002, accepted 2026-09-02; the decider is not recorded)

#### Scenario: A client operation does not change the world

- **WHEN** a client plays, pauses, steps, scrubs, selects, filters, changes camera or layout, or toggles an overlay
- **THEN** no World transition is committed

#### Scenario: Scene facts versus canonical facts

- **WHEN** a client shows a scene
- **THEN** its coordinates and labels are presentation facts, while canonical IDs, revisions, ticks, outcomes, state changes, observations and causal parents come from the retained Engine trace

### Requirement: Incremental delivery

`projection_sse_messages()` encodes the one-way stream as:

```text
snapshot
world-event
world-event
...
complete
```

`scripts/waltzman_demo_service.py` exposes that stream as `text/event-stream`.
SSE is sufficient for the current read-only requirement; WebSocket or
bidirectional control is not part of v0.

Source: inferred by agent (live projection v0, applying Decision 002, accepted 2026-09-02; the decider is not recorded)

#### Scenario: The stream order

- **WHEN** `projection_sse_messages()` encodes a bundle
- **THEN** the stream is one `snapshot` message, then one `world-event` message per retained event in order, then a `complete` message
- **AND** `scripts/waltzman_demo_service.py` serves that stream as `text/event-stream`

#### Scenario: A client asks to send commands

- **WHEN** a client needs WebSocket or other bidirectional control
- **THEN** v0 does not provide it, because one-way SSE is sufficient for the current read-only requirement

### Requirement: Branching

A branch is a distinct canonical run. The Waltzman intervention branch is
constructed by exact command replay of the baseline prefix and then new
canonical attempts. The UI can compare branches, but it never rewrites the
baseline history.

Source: inferred by agent (live projection v0, applying Decision 002, accepted 2026-09-02; the decider is not recorded)

#### Scenario: An intervention branch is a distinct run

- **WHEN** the Waltzman intervention branch is built
- **THEN** it is constructed by exact command replay of the baseline prefix followed by new canonical attempts, so its first events carry the same IDs as the baseline's events
- **AND** the UI can compare the branches, but it never rewrites the baseline history
