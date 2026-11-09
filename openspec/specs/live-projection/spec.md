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

### Requirement: Authority

The client may play, pause, step, scrub, select, filter, change camera/layout,
or toggle overlays. None of those operations commits a World transition.

Scene coordinates and labels are presentation facts. Canonical IDs, revisions,
ticks, outcomes, state changes, observations, and causal parents come from the
retained Engine trace.

Source: inferred by agent (live projection v0, applying Decision 002, accepted 2026-09-02; the decider is not recorded)

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

### Requirement: Branching

A branch is a distinct canonical run. The Waltzman intervention branch is
constructed by exact command replay of the baseline prefix and then new
canonical attempts. The UI can compare branches, but it never rewrites the
baseline history.

Source: inferred by agent (live projection v0, applying Decision 002, accepted 2026-09-02; the decider is not recorded)
