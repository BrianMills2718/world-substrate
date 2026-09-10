---
role: contract
status: implemented
reviewed_through: 2026-09-09
---

# Living Scene v1

`world-substrate-living-scene/v1` is the read-only presentation contract for
turning retained canonical World Substrate projections into deterministic
logical scene frames. It is additive to `scene-profile/v0`; existing Kitchen,
Castaway, Workshop, and Greenhouse profiles remain valid on their current path.

## Authority

Authority is one-way:

1. the retained snapshot and event deltas own canonical world truth;
2. the retained event owns event identity, tick/revision, status, information
   context, and mechanic-declared causal ancestry;
3. a Living Scene profile may select read paths and presentation geometry;
4. browser interpolation, art, layout, and timing are presentation only.

A Living Scene profile cannot write canonical state, fabricate a delivery,
create causal parentage, edit branch history, or complete a duration-bearing
activity. Those facts must already exist in retained canonical input.

## Input seam

The logical frame builder consumes:

```text
world-substrate-live-projection/v0
  initial_snapshot: world-substrate-snapshot/v1
  events: ordered canonical events with deterministic leaf changes
+
world-substrate-living-scene/v1
  read-only presentation declarations
        |
        v
deterministic logical scene frames
```

The implementation is in `world_substrate.living_scene` and deliberately has
no DOM or browser dependency.

## Profile shape

Required top-level objects are:

- `assets` — explicit presentation assets;
- `zones` — illustrative rectangles and optional anchors;
- `actors` — canonical entity bindings plus optional presentation homes;
- `entities` — canonical entity bindings plus optional presentation homes;
- `activities` — canonical activity entity bindings and anchors;
- `institutions` — canonical institution entity bindings and anchors;
- `event_visuals` — exact rule-id keyed presentation declarations;
- `state_styles` — downstream appearance metadata.

`scene` and `presentation` are optional downstream metadata objects. Unknown
top-level fields fail loud so a typo cannot silently become an assumed contract.

Each actor/entity/activity/institution declaration may name an explicit
canonical `entity`; otherwise the visual id is used as the canonical entity id.
Its `bindings` map presentation field names to dotted read paths relative to
that canonical entity.

Example:

```json
{
  "schema_version": "world-substrate-living-scene/v1",
  "scene_id": "neutral-lab-v1",
  "world": "neutral-lab",
  "assets": {},
  "zones": {
    "room": {"rect": [0, 0, 100, 100], "anchor": [50, 50]}
  },
  "actors": {
    "actor-a": {
      "home": [20, 50],
      "bindings": {"stance": "components.commitment.stance"}
    }
  },
  "entities": {},
  "activities": {},
  "institutions": {},
  "event_visuals": {},
  "state_styles": {}
}
```

## Exact event bindings

`event_visuals` is keyed by exact canonical `rule_id`. The logical projector
does not infer semantics from action or rule names. If a retained event has no
matching declaration, the frame exposes a neutral `generic_event` with no
presentation operations.

Declared operations are presentation records. They may name an `op`, optional
presentation metadata, and dotted `read_paths`. Authority-bearing mutation
fields such as `changes`, `after`, `before`, `causal_parent_event_ids`,
`information_context`, or canonical/world state payloads are rejected in a
profile operation.

Later renderer work may add reusable operation semantics, but those operations
remain downstream of the retained event and cannot become mechanics.

## Deterministic frame reconstruction

`build_living_scene_frames()` returns the initial frame followed by one logical
frame for every retained event boundary.

`rebuild_living_scene_frame()` reconstructs any requested boundary directly
from the initial canonical snapshot plus retained changes through that event.
Scrubbing therefore does not depend on accumulated browser state.

Logical frames include:

- exact scene/world/branch identity;
- canonical boundary index, tick, and revision;
- the retained event at that boundary;
- its exact declared or neutral event presentation record; and
- read-only projected actor/entity/activity/institution bindings.

`normalized_frame_json()` supplies stable sorted serialization for regression
and retained evidence comparisons.

## Time boundary

Simulation tick, event order, activity start/end ticks, and status are canonical
facts. Animation duration is presentation metadata only. Changing animation
milliseconds cannot change the logical view at a canonical event boundary.

## Compatibility

`load_scene_contract()` accepts both:

- `world-substrate-living-scene/v1`; and
- legacy `world-substrate-scene-profile/v0`.

Legacy profiles are returned unchanged after their minimal contract shape is
validated. The existing generic `render_scene_replay.py` path continues to own
v0 rendering semantics; Living Scene v1 does not silently reinterpret those
profiles.

## Verification fixture

`tests/fixtures/living_scene/` contains a domain-neutral retained profile,
projection bundle, and expected frame sequence. Tests also run the existing
Kitchen and Castaway profiles through their unchanged renderer path while
confirming the compatibility loader preserves them byte-for-structure.

The generic Living Scene runtime is additionally scanned for Waltzman names,
entity ids, and scenario-specific branches. Waltzman-specific composition must
live in reference-world profile/assets rather than this shared contract layer.

## Current implementation boundary

The deterministic read-only logical frame seam and a generic 2D embodied renderer
are implemented. The renderer can place declared actors and zones, show canonical
resource/constraint values, present duration-bearing activities and institution
status, gather declared participants around an active activity, and apply exact
`actor.move_to` presentation operations. These behaviors remain downstream of
canonical frame state.

Information transmission, action-result feedback, Waltzman composition, deeper
inspection, and public product integration remain separate downstream work units.
The generic renderer must remain free of Waltzman entity/action branches.
