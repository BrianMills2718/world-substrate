---
role: contract
status: implemented
reviewed_through: 2026-09-07
---

# Scene profile v0

A scene profile is the detachable presentation contract between a retained
world trace and a graphical replay. It does **not** add facts to the world,
change mechanics, or become a second canonical state.

The v0 pipeline is:

```text
reference-world model
        +
retained contested-run/v3 trace
        +
scene-profile/v0
        +
asset bindings
        |
        v
read-only 2D replay HTML
```

## Authority

Authority is deliberately one-way:

1. The retained trace owns actions, reasoning, order/progress facts, causal
   outcomes, and terminal status.
2. The reference-world model may supply entity identity, labels, categories,
   initial component values, and initial ownership.
3. The scene profile owns only presentation: geometry, asset selection,
   action-to-motion mappings, visual state transforms, and milestone labels.
4. Assets carry no causal meaning on their own.

A scene profile may place a burner in the north of the screen even when the
canonical world says only `location_id: kitchen`. That position is illustrative
unless the world model itself represents coordinates.

## Wire shape

`schema_version` is `world-substrate-scene-profile/v0`.

A profile contains:

- `world`: the trace world it may render;
- optional `world_model`: a reference-world JSON file, resolved relative to the
  profile;
- `assets`: named emoji/text/image assets;
- `actors`: actor asset, accent, home position, and carrying offsets;
- `stations`: 2D rectangles and anchors for surfaces, workstations, sources,
  and goal/progress panels, with optional presentation-only multi-item layout;
- `entities`: visualized world entities, asset bindings, home positions, and
  optional initial-state paths into the world model;
- `action_visuals`: declarative mappings from action kind to label template, actor target,
  ownership change, item state, target station, and active workstation;
- `state_styles`: appearance transforms for represented item states;
- optional `station_precedence_states`: states whose explicit station placement
  should be drawn ahead of a still-recorded ownership attachment;
- `progress_assets`: semantic progress labels to assets;
- `moment_rules`: labels for trace-derived moments such as contention,
  handoff, takeover, or terminal completion;
- scene title/theme/autoplay presentation fields.

Image assets use a profile-relative path and are embedded as data URIs in the
output so the generated replay remains a single file.

## Action projection

An `action_visuals` entry may currently declare:

- `label_template`: a field-substitution label such as `cook {item} on {burner}`;
- `item_field`: which action field names the moved/changed entity;
- `actor_target.station`: move the actor toward a fixed presentation station;
- `actor_target.action_field`: use a station id named by the action itself;
- `ownership: take|release`: reconstruct presentation ownership from an
  accepted action;
- `clear_item_station`: detach a newly taken entity from a previous station;
- `set_state`: set the entity's presentation state after the accepted action;
- `item_target.station` or `.action_field`: place the entity at a station;
- `item_target.unless_state`: preserve an existing placement for selected
  states;
- `activate_station_from`: mark a workstation named by an action field active
  for that frame.

Unknown action kinds remain visible in the trace/reasoning surface but have no
spatial projection until the profile maps them.

## Station item layout

A station may optionally declare `item_layout` to arrange more than one entity
placed at that station without changing any world relationship:

```json
{
  "item_layout": {
    "slots": [[0.28, 0.64], [0.72, 0.64], [0.50, 0.38]],
    "overflow": "grid"
  }
}
```

Slot coordinates are relative to the station rectangle: `[0, 0]` is its
top-left and `[1, 1]` its bottom-right. Placed entities consume slots in stable
scene-profile entity order. If there are more placed entities than explicit
slots, `overflow: "grid"` lays out the remainder deterministically;
`overflow: "anchor"` sends the remainder to the station's ordinary item anchor.
Values outside `0..1` are rejected.

This is presentation state only. It does not assert canonical coordinates,
attachment geometry, or physical collision. Profiles without `item_layout` use
the previous single-anchor path unchanged.

## Moment projection

v0 supports these trace-derived predicates:

- `retry_unavailable`: a retry followed another actor making the original plan
  unavailable;
- `filled_release`: an actor with completed progress releases a selected item;
- `take_after_release`: a different actor later takes that selected item;
- `all_progress_filled`: all represented progress records are complete.

The predicate is generic; the profile chooses the item and human-facing label.

## Generation

The generic command is:

```bash
python scripts/render_scene_replay.py <trace.json> \
  --profile <scene-profile.json> \
  --output <replay.html>
```

The kitchen compatibility command remains available, but it is only a thin
wrapper selecting `reference_worlds/kitchen/scene-profile-v0.json`.

## Profile bootstrapping

`scene-profile/v0` now has a reviewable bootstrap path:

```bash
python scripts/bootstrap_scene_profile.py <world-model.json> <trace.json> \
  --catalog reference_worlds/scene-asset-catalog-v0.json \
  --output <draft-profile.json>
```

The bootstrapper may infer only facts supported by its inputs: trace actors,
entity ids and labels, asset bindings from the explicit catalog, portable or
referenced visual entities, category-backed canonical station candidates,
initial `actor:*` ownership, actor-to-goal links represented in the world model,
and candidate action fields whose values consistently name visual entities or
stations.

It deliberately does **not** invent screen coordinates or treat an action name
as sufficient evidence for motion/state semantics. Unresolved choices are
recorded under `bootstrap.todos`. A draft may therefore be reviewable without
being renderable yet.

A presentation-only review overlay can fill those TODOs:

```bash
python scripts/bootstrap_scene_profile.py <world-model.json> <trace.json> \
  --catalog reference_worlds/scene-asset-catalog-v0.json \
  --review <scene-review-v0.json> --require-complete \
  --output <scene-profile-v0.json>
```

`--require-complete` refuses unresolved geometry or unreviewed action
projection. The assembled result then passes the generic scene profile loader
and renderer. The review overlay carries no causal authority; it only resolves
illustrative presentation choices.

### Optional presentation auto-layout

`--auto-layout` fills missing actor homes, station rectangles/anchors, and
entity homes with deterministic `role-grid-v0` presentation geometry. It runs
after the review overlay is merged and never overwrites reviewed coordinates.
Every generated path is recorded under
`bootstrap.auto_layout.proposed_geometry`; `bootstrap.auto_layout.algorithm`
records the layout version. These coordinates are illustrative and must not be
read back into canonical world state.

Auto-layout uses already inferred/reviewed scene roles and action targets. It
does **not** approve action motion/state semantics, so unreviewed action
projection remains a bootstrap TODO even when all geometry is proposed.

The CLI form is:

```bash
python scripts/bootstrap_scene_profile.py <world-model.json> <trace.json> \
  --catalog reference_worlds/scene-asset-catalog-v0.json \
  --review <scene-review-v0.json> --auto-layout --require-complete \
  --output <scene-profile-v0.json>
```

The asset catalog uses
`world-substrate-scene-asset-catalog/v0`. It is an explicit input that maps
known entity/component/category patterns to assets, portable-state hints,
visual state paths, progress assets, and canonical station roles. Supplying an
asset in that catalog does not assert a world fact.

For the current acceptance fixtures, the reviewed bootstrap reproduces the
existing Kitchen and Castaway profiles exactly apart from bootstrap provenance.
The per-world review JSON is about 64% and 67% respectively of the previous
full profile payload, a 36%/33% reduction in scene-specific review content.

## Implemented evidence

The kitchen spatial replay is generated by the generic renderer plus its scene
profile. Castaway is the second real-world proof. Workshop is the greenfield
proof: no Workshop scene profile existed before the test; bootstrap + a 62.6%
presentation review overlay produced a working replay from a seven-turn real
engine trace without a Workshop branch in the renderer. The greenfield
single-anchor finding is now closed generically: `frame-a` declares relative
item slots, and its two legs plus seat render at distinct positions. A separate synthetic
lab profile also exercises a custom `scan` action. Tests verify image-asset
embedding and that the generic renderer contains no Kitchen, Castaway, or
Workshop entity ids.

## Limits

v0 is intentionally small:

- 2D only;
- designed around `world-substrate-contested-run/v3` traces;
- spatial geometry is presentation-only unless coordinates are canonical state;
- action projection is declarative but uses a finite set of projection
  operations rather than arbitrary code;
- progress panels assume the trace exposes actor-keyed progress records;
- the generic renderer has a simple browser presentation, not a game engine;
- cross-world reuse is proven on Kitchen, Castaway, greenfield Workshop, plus a synthetic lab;
- station item layout supports explicit relative slots plus deterministic grid/anchor overflow, but does not infer semantic assembly geometry;
- profile bootstrapping infers identity/asset/station/action-field structure; optional auto-layout can propose missing illustrative geometry, while ambiguous action motion/state still requires review;
- the bootstrapper does not yet consume the full semantic-binding graph to infer
  richer action animation safely.

Those limits are preferable to allowing presentation code to acquire causal
or semantic authority.
