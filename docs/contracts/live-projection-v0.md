---
role: contract
status: implemented
reviewed_through: 2026-09-08
---

# Live projection v0

The live projection is a one-way observer seam from canonical World Substrate
history to a living client. It never becomes a second world authority.

`world_substrate.projection` implements the v0 seam.

## Wire shape

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

## Authority

The client may play, pause, step, scrub, select, filter, change camera/layout,
or toggle overlays. None of those operations commits a World transition.

Scene coordinates and labels are presentation facts. Canonical IDs, revisions,
ticks, outcomes, state changes, observations, and causal parents come from the
retained Engine trace.

## Incremental delivery

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

## Branching

A branch is a distinct canonical run. The Waltzman intervention branch is
constructed by exact command replay of the baseline prefix and then new
canonical attempts. The UI can compare branches, but it never rewrites the
baseline history.
