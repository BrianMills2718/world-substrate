# living-scene Specification

## Purpose

Read-only logical scene frames rebuilt from retained canonical projections, and the composed renderer that draws them. Under Decision 006 (Brian, 2026-10-05: "i approve") these renderers are maintained, not extended.

**Living Scene v1** (folded on 2026-11-09 from `docs/contracts/living-scene-v1.md`, status `implemented`, reviewed through 2026-09-09, last commit `643e7d9`):

`world-substrate-living-scene/v1` is the read-only presentation contract for
turning retained canonical World Substrate projections into deterministic
logical scene frames. It is additive to `scene-profile/v0`; existing Kitchen,
Castaway, Workshop, and Greenhouse profiles remain valid on their current path.

**Composed Living Scene presentation** (folded on 2026-11-09 from `docs/contracts/composed-living-scene-v1.md`, status `implemented`, reviewed through 2026-09-10, last commit `b094e24`):

`render_composed_living_scene.py` is the product-oriented renderer for the existing
`world-substrate-living-scene/v1` logical-frame contract. It does not introduce a
second simulation contract or a second source of world truth.

The older `render_living_scene.py` remains a compatibility/debug renderer. A world
may opt into the composed renderer without changing canonical state, event history,
information delivery, causal ancestry, or simulation timing.

## Requirements

### Requirement: Living Scene: Authority

Authority is one-way:

1. the retained snapshot and event deltas own canonical world truth;
2. the retained event owns event identity, tick/revision, status, information
   context, and mechanic-declared causal ancestry;
3. a Living Scene profile may select read paths and presentation geometry;
4. browser interpolation, art, layout, and timing are presentation only.

A Living Scene profile cannot write canonical state, fabricate a delivery,
create causal parentage, edit branch history, or complete a duration-bearing
activity. Those facts must already exist in retained canonical input.

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Input seam

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

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Profile shape

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

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Exact event bindings

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

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Deterministic frame reconstruction

`build_living_scene_frames()` returns the initial frame followed by one logical
frame for every retained event boundary.

`rebuild_living_scene_frame()` reconstructs any requested boundary directly
from the initial canonical snapshot plus retained changes through that event.
Scrubbing therefore does not depend on accumulated browser state.

Logical frames include:

- exact scene/world/branch identity;
- canonical boundary index, tick, and revision;
- a presentation-safe retained event summary at that boundary;
- its exact declared or neutral event presentation record; and
- read-only projected actor/entity/activity/institution bindings.

`normalized_frame_json()` supplies stable sorted serialization for regression
and retained evidence comparisons.

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Information and outcome presentation

Living Scene frames expose a presentation-safe event summary rather than copying
the full retained event object. Actor-scoped `observation`, raw `changes`, and
`information_context` content remain evidence-layer data and are not embedded in
the generic public scene payload. Stable event/rule/tick/revision/status identity
and mechanic-declared causal parent ids may remain visible as metadata.

An exact declared `information.transmit` operation resolves canonical
`information` + `delivery` records. Source, recipient, channel, and topic may be
shown as represented transmission metadata. Message content is included only
when the information is public or the requested observer is authorized by the
canonical information-delivery visibility rules. A public scene with no observer
therefore cannot expose direct/private content merely because a delivery exists.
Message content is assigned to the DOM with `textContent`, never injected as
markup.

An exact declared `action.feedback` operation may display the retained event
status and failed check labels. It does not generate a new explanation and does
not infer causal ancestry from those labels. Rendering a transmission or cognition
context never promotes that information into `causal_parent_event_ids`.

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Time boundary

Simulation tick, event order, activity start/end ticks, and status are canonical
facts. Animation duration is presentation metadata only. Changing animation
milliseconds cannot change the logical view at a canonical event boundary.

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Time boundary: Responsive presentation overrides

Living Scene v1 may provide `mobile_home` on actors/entities, `mobile_anchor` on
activities/institutions/zones, and `mobile_rect` on zones. These are validated
with the same point/rectangle shapes as desktop presentation geometry. They are
selected only by the browser presentation layer and never change canonical
location, state, tick, event order, or branch history. `scene.mobile_min_height`
is likewise a presentation-only viewport hint.

The generic player exposes an HTML range scrubber whose values are retained
canonical frame boundaries. Selecting a value calls the same deterministic frame
render used by next/previous controls; it does not advance world time. A generic
multi-branch wrapper may swap self-contained branch documents, but it selects
retained histories rather than editing one branch into another.

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Compatibility

`load_scene_contract()` accepts both:

- `world-substrate-living-scene/v1`; and
- legacy `world-substrate-scene-profile/v0`.

Legacy profiles are returned unchanged after their minimal contract shape is
validated. The existing generic `render_scene_replay.py` path continues to own
v0 rendering semantics; Living Scene v1 does not silently reinterpret those
profiles.

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Verification fixture

`tests/fixtures/living_scene/` contains a domain-neutral retained profile,
projection bundle, and expected frame sequence. Tests also run the existing
Kitchen and Castaway profiles through their unchanged renderer path while
confirming the compatibility loader preserves them byte-for-structure.

The generic Living Scene runtime is additionally scanned for Waltzman names,
entity ids, and scenario-specific branches. Waltzman-specific composition must
live in reference-world profile/assets rather than this shared contract layer.

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Living Scene: Current implementation boundary

The deterministic read-only logical frame seam and generic 2D embodied renderer
are implemented. The renderer can place declared actors and zones, show canonical
resource/constraint values, present duration-bearing activities and institution
status, gather declared participants, visualize visibility-bounded information
transmission, show retained action feedback, apply responsive presentation
overrides, and scrub exact event boundaries. The generic multi-branch wrapper
selects among retained branch documents without rewriting history.

Actor placement is one presentation rule shared by both renderers
(`src/world_substrate/living_scene_layout.py`, settled 2026-10-06): an actor stays
where its last `actor.move_to` put it; an active activity gathers its declared
participants on a ring around its anchor; a `move_to` in the current frame wins;
and actors left on one identical point are spread on a ring around it in actor-id
order (radius `render.gather_radius`, default 11), while a single actor keeps the
exact point.

Waltzman composition is declarative reference-world data. Deeper inspection and
public funnel integration remain downstream work; the generic runtime remains
free of Waltzman entity/action branches.

Source: inferred by agent (living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Composed scene: Authority boundary

The composed renderer may choose or interpolate presentation-only properties:
illustrative background art, actor/object screen position, state styling, idle or
transition animation, event emphasis, responsive layout, labels, and inspector
layout. It may not mutate or infer canonical state.

The renderer consumes only deterministic Living Scene frames. Scrubbing still
reconstructs from the retained initial snapshot plus canonical event deltas.
Activity status and timing, institution state, resource values, commitments, and
information deliveries remain upstream facts.

Source: inferred by agent (composed living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Composed scene: Generic presentation primitives

The composed renderer supports reusable world-neutral primitives:

- image/text actor assets with persistent homes and state styling;
- image/text world objects with local status light, meter, and state effects;
- activity gathering around a declared anchor and deterministic return home;
- presentation-only state-dependent object positions;
- exact-event emphasis pulses;
- visibility-safe transient information paths and message bubbles;
- compact play/pause/step/scrub controls;
- selectable actor/entity/activity/institution anchors;
- a contextual inspector populated from already-bound canonical fields;
- desktop/mobile presentation geometry.

A `presentation.emphasize` event operation has no logical effect. It only tells the
renderer which already-declared visual object should receive a transient pulse.

Source: inferred by agent (composed living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)

### Requirement: Composed scene: Product-quality rule

The composed path exists to make the world itself the primary interface. It should
not regress into a persistent grid of cards, graph panels, or evidence tables. A
profile may retain card display as a compatibility fallback, but polished worlds
should use spatial art and local state changes wherever those are sufficient.

World-specific art, labels, positions, and exact rule bindings remain in that
reference world's profile/assets. Generic renderer source must not branch on a
world name, entity id, resident name, or scenario-specific rule id.

Source: inferred by agent (composed living scene v1; Decision 006, approved by Brian on 2026-10-05 with "i approve", keeps the renderer as maintained, not extended)
