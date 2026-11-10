# scene-replay Specification

## Purpose

The detachable presentation contract between a retained world trace and a graphical replay (`scene-profile/v0`).

**Scene profile v0** (folded on 2026-11-09 from `docs/contracts/scene-profile-v0.md`, status `implemented`, reviewed through 2026-09-07, last commit `b42ce05`):

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

## Requirements

### Requirement: Authority

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

Source: inferred by agent (scene profile v0)

#### Scenario: Who owns what in a replay

- **WHEN** a replay is built from a trace, a reference-world model and a scene profile
- **THEN** the retained trace owns actions, reasoning, order and progress facts, causal outcomes and terminal status, the model may supply entity identity, labels, categories, initial component values and initial ownership, and the profile owns only presentation (geometry, asset selection, action-to-motion mappings, visual state transforms and milestone labels)
- **AND** assets carry no causal meaning on their own

#### Scenario: A burner placed in the north

- **WHEN** a profile places a burner in the north of the screen while the canonical world says only `location_id: kitchen`
- **THEN** the position is illustrative, unless the world model itself represents coordinates

### Requirement: Wire shape

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

Source: inferred by agent (scene profile v0)

#### Scenario: A valid scene profile

- **WHEN** a profile has `schema_version` `world-substrate-scene-profile/v0`, a `world` naming the trace world it may render, and `assets`, `actors`, `stations`, `entities`, `action_visuals`, `state_styles`, `progress_assets` and `moment_rules` as described
- **THEN** it loads, and it may also give an optional `world_model` (resolved relative to the profile), `station_precedence_states` and scene title, theme and autoplay fields

#### Scenario: A profile for another world

- **WHEN** a profile's `world` does not match the trace's world
- **THEN** building frames fails with an error

#### Scenario: Image assets

- **WHEN** an asset is an image with a profile-relative path
- **THEN** the generated replay embeds it as a data URI, so the replay remains a single file

### Requirement: Action projection

An `action_visuals` entry may currently declare:

- `label_template`: a field-substitution label such as `cook {item} on {burner}`;
- `item_field`: which action field names the moved/changed entity;
- `actor_target.station`: move the actor toward a fixed presentation station;
- `actor_target.action_field`: use a station id named by the action itself;
- `ownership: take|release`: reconstruct presentation ownership from an
  accepted action;
- `clear_item_station`: detach a newly taken entity from a previous station;
- `set_state`: set the primary `item_field` entity's presentation state after the accepted action;
- `state_effects`: optionally update additional explicitly named visual entities, each as `{entity_field, set_state}`; this supports one causal action changing more than one represented entity without choosing a single fake visual owner;
- `item_target.station` or `.action_field`: place the entity at a station;
- `item_target.unless_state`: preserve an existing placement for selected
  states;
- `activate_station_from`: mark a workstation named by an action field active
  for that frame.

Unknown action kinds remain visible in the trace/reasoning surface but have no
spatial projection until the profile maps them.

Source: inferred by agent (scene profile v0)

#### Scenario: A mapped action moves things

- **WHEN** an accepted action's kind has an `action_visuals` entry with a `label_template`, `item_field`, an `actor_target`, `ownership` of `take` or `release`, `set_state` or `item_target`
- **THEN** the frame fills the label from the action's fields and moves the actor, the item and its presentation state as declared

#### Scenario: One action changes two entities

- **WHEN** an `action_visuals` entry lists `state_effects` of the form `{entity_field, set_state}`
- **THEN** each named visual entity takes its state after the accepted action, so one causal action can change more than one entity without a single fake visual owner
- **AND** a `state_effects` entry that names an unknown visual entity is refused with "unknown visual entity"

#### Scenario: An unmapped action kind

- **WHEN** a trace contains an action kind the profile does not map
- **THEN** it stays visible in the trace and reasoning surface and has no spatial projection

### Requirement: Station item layout

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

Source: inferred by agent (scene profile v0)

#### Scenario: Slots and overflow

- **WHEN** a station declares `item_layout` with `slots` (coordinates relative to the station rectangle, `[0, 0]` top-left and `[1, 1]` bottom-right) and an `overflow` of `grid` or `anchor`
- **THEN** placed entities take slots in stable scene-profile entity order, and the remainder is laid out on a deterministic grid (`grid`) or sent to the station's ordinary item anchor (`anchor`)
- **AND** with one slot `[0.25, 0.5]` and three placed entities, the first sits at the slot and all three get distinct positions

#### Scenario: A slot outside 0 to 1

- **WHEN** a slot coordinate is outside `0..1`
- **THEN** the profile is rejected with an error naming "relative 0..1 coordinates"

#### Scenario: Layout is presentation only

- **WHEN** a station has an `item_layout`, or has none
- **THEN** it asserts no canonical coordinates, attachment geometry or physical collision, and a profile without `item_layout` uses the earlier single-anchor path unchanged

### Requirement: Moment projection

v0 supports these trace-derived predicates:

- `retry_unavailable`: a retry followed another actor making the original plan
  unavailable;
- `filled_release`: an actor with completed progress releases a selected item;
- `take_after_release`: a different actor later takes that selected item;
- `all_progress_filled`: all represented progress records are complete.

The predicate is generic; the profile chooses the item and human-facing label.

Source: inferred by agent (scene profile v0)

#### Scenario: A trace-derived moment is labeled

- **WHEN** a trace matches one of `retry_unavailable`, `filled_release`, `take_after_release` or `all_progress_filled`
- **THEN** the replay shows the moment under the human-facing label and selected item the profile chose
- **AND** the predicates themselves are generic, such as a retry that followed another actor making the original plan unavailable, or all represented progress records being complete

### Requirement: Generation

The generic command is:

```bash
python scripts/render_scene_replay.py <trace.json> \
  --profile <scene-profile.json> \
  --output <replay.html>
```

The kitchen compatibility command remains available, but it is only a thin
wrapper selecting `reference_worlds/kitchen/scene-profile-v0.json`.

Source: inferred by agent (scene profile v0)

#### Scenario: Rendering a replay

- **WHEN** `python scripts/render_scene_replay.py <trace.json> --profile <scene-profile.json> --output <replay.html>` is run
- **THEN** it writes a read-only 2D replay HTML built from the profile and the trace
- **AND** the kitchen compatibility command is only a thin wrapper selecting `reference_worlds/kitchen/scene-profile-v0.json`

### Requirement: Profile bootstrapping

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

Source: inferred by agent (scene profile v0)

#### Scenario: A draft is bootstrapped from its inputs

- **WHEN** `scripts/bootstrap_scene_profile.py` is given a world model, a trace and the explicit asset catalog
- **THEN** it infers only facts those inputs support (trace actors, entity ids and labels, catalog asset bindings, station candidates, initial `actor:*` ownership, actor-to-goal links, and action fields whose values consistently name visual entities or stations; for Kitchen the `cook` action's item field is `item` and its station field `burner`)
- **AND** it does not invent screen coordinates or treat an action name as evidence for motion or state, and records unresolved choices under `bootstrap.todos`, so a draft may be reviewable without being renderable yet

#### Scenario: A review overlay completes the profile

- **WHEN** a presentation-only review overlay is passed with `--review` and `--require-complete`
- **THEN** unresolved geometry or unreviewed action projection is refused, and a complete result passes the generic scene profile loader and renderer
- **AND** the overlay carries no causal authority

### Requirement: Profile bootstrapping: Optional presentation auto-layout

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
visual state paths, progress assets, canonical station roles, and optional
**action-presentation bindings**. Supplying any of those declarations does not
assert or change a world fact.

Source: inferred by agent (scene profile v0)

#### Scenario: Auto-layout fills only what is missing

- **WHEN** `--auto-layout` runs after the review overlay is merged
- **THEN** it fills missing actor homes, station rectangles and anchors, and entity homes with deterministic `role-grid-v0` geometry, never overwrites reviewed coordinates, and records every generated path under `bootstrap.auto_layout.proposed_geometry` and the version under `bootstrap.auto_layout.algorithm`

#### Scenario: Auto-layout does not approve motion

- **WHEN** all geometry has been proposed by auto-layout
- **THEN** unreviewed action projection remains a bootstrap TODO, and the coordinates are illustrative and not read back into canonical world state

### Requirement: Profile bootstrapping: Explicit action-presentation bindings

`action_visual_bindings` is keyed by the exact action kind id and is never
inferred from lexical similarity. An entry has `projection` plus optional
`complete: true`. Projection values may use `$item_field` and `$station_field`;
the bootstrapper resolves those placeholders only when the retained trace shows
a unique field whose values are represented visual entities/stations. Missing
placeholders leave the action unresolved and review-required.

For example:

```json
{
  "pick_up": {
    "complete": true,
    "projection": {
      "ownership": "take",
      "clear_item_station": true,
      "actor_target": {"entity_field": "$item_field"}
    }
  },
  "attach": {
    "complete": true,
    "projection": {
      "ownership": "release",
      "set_state": "attached",
      "item_target": {"action_field": "$station_field"}
    }
  }
}
```

Applied bindings are recorded in
`bootstrap.declared_action_bindings`; placeholder failures are recorded in
`bootstrap.binding_resolution_errors`. A reviewed action projection is
authoritative over catalog defaults: it is applied to the neutral trace-inferred
field/label shape rather than deep-merged on top of catalog-only ownership,
target, or state effects.

The renderer supports `actor_target.entity_field` as a generic presentation
primitive: the actor moves toward the current visual home/station of the entity
named by that action field. This does not imply canonical coordinates or change
ownership by itself.

Auto-layout initial placement follows an entity's first relevant action only, so
a future target (for example a later `attach`) cannot leak backward into the
opening scene.

For the current acceptance fixtures, the reviewed bootstrap reproduces the
existing Kitchen and Castaway profiles exactly apart from bootstrap provenance.
The per-world review JSON is about 64% and 67% respectively of the previous
full profile payload, a 36%/33% reduction in scene-specific review content.

Source: inferred by agent (scene profile v0)

#### Scenario: A binding is keyed by the exact action kind

- **WHEN** the catalog has an `action_visual_bindings` entry for an exact action kind id, with a `projection` and optional `complete: true`
- **THEN** its `$item_field` and `$station_field` placeholders are resolved only if the retained trace shows a unique field whose values are represented visual entities or stations, and the applied binding is recorded in `bootstrap.declared_action_bindings`
- **AND** an action renamed to a lookalike (`pick_up_like`) gets no projection and stays a TODO

#### Scenario: A placeholder cannot be resolved

- **WHEN** a binding's placeholder has no matching field in the trace (a `drink` binding asking for `$station_field` on Castaway)
- **THEN** the failure is recorded in `bootstrap.binding_resolution_errors`, the action stays unresolved, and review is required

#### Scenario: A reviewed projection beats the catalog

- **WHEN** a reviewed action projection and a catalog default both exist for an action
- **THEN** the reviewed one is applied to the neutral trace-inferred shape rather than merged over the catalog's ownership, target or state effects

#### Scenario: Actor moves toward an entity

- **WHEN** a projection uses `actor_target.entity_field`
- **THEN** the renderer moves the actor toward the current visual home or station of the entity named by that action field, which implies no canonical coordinates and changes no ownership by itself
- **AND** auto-layout initial placement follows an entity's first relevant action only, so a later target cannot leak into the opening scene

#### Scenario: The acceptance fixtures reproduce

- **WHEN** the Kitchen and Castaway reviewed bootstraps run
- **THEN** they reproduce the existing profiles exactly apart from bootstrap provenance, and each review file is under 70 percent of its profile's size (the spec's measured figures are about 64 and 67 percent)

### Requirement: Implemented evidence

Workshop is the greenfield zero-review proof: bootstrap, generic item layout,
auto-layout, and explicit action bindings produce both a default replay and a
polished variant. Castaway proves materially different `fill`/`drink`, source,
vessel-state, and initial-ownership semantics with no review overlay. Kitchen
now closes the breadth gate: five explicit action bindings, two actors, two
burners, two goals, staged ingredients, shared knife ownership, and the retained
t10→t11 handoff all generate a zero-review default beside the byte-identical
polished flagship. A separate synthetic lab profile exercises a custom `scan`
action. Greenhouse, authored after the replay system was fixed, generates a
zero-review Automatic replay with no Greenhouse code: the shared `take`/`put_down`
labels use the trace-inferred field name (`item` in Kitchen, `vessel` in
Greenhouse), and the `water` binding uses `state_effects` to set the plant
`watered` and the can back to `empty` (folded from the retired
`docs/audits/greenhouse-authoring-proof.md`). Tests verify image-asset embedding and that the generic renderer contains
no Kitchen, Castaway, or Workshop entity ids.

Source: inferred by agent (scene profile v0)

#### Scenario: Worlds replay through the generic path

- **WHEN** the Workshop, Castaway, Kitchen, a synthetic lab and Greenhouse are bootstrapped and replayed
- **THEN** Workshop, Castaway, Kitchen and Greenhouse each generate a zero-review default replay through the generic renderer (Kitchen's beside its byte-identical polished flagship), and the synthetic lab exercises a custom `scan` action
- **AND** Greenhouse needs no Greenhouse code: its `water` binding uses `state_effects` to set the plant to `watered` and the can back to `empty`
- **AND** tests verify image-asset embedding and that the generic renderer contains no Kitchen, Castaway or Workshop entity ids

### Requirement: Limits

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
- zero-review explicit catalog bindings are proven across Workshop pickup/attach, Castaway fill/drink, and the five-action Kitchen flagship; new action families should remain TODOs until explicitly declared;
- the bootstrapper does not yet consume the full Linguistic Core semantic-binding graph to derive richer presentation safely.

Those limits are preferable to allowing presentation code to acquire causal
or semantic authority.

Source: inferred by agent (scene profile v0)

#### Scenario: A question beyond v0

- **WHEN** someone wants 3D, a trace that is not a `world-substrate-contested-run/v3` trace, game-engine presentation, arbitrary-code action projection, semantic assembly geometry, or richer presentation derived from the full Linguistic Core binding graph
- **THEN** v0 does not provide it
- **AND** spatial geometry stays presentation-only unless coordinates are canonical state, and new action families stay TODOs until explicitly declared, so presentation code does not acquire causal or semantic authority

### Requirement: Fresh-world presentation wins over the shared catalog (current code)

When a freshly authored world declares presentation, its declarations win over the shared asset catalog: bootstrap removes catalog bindings that collide with entities the world defines and turns an authored category asset into an exact entity binding (`scripts/run_authored_world.py:1036-1048`). This rule came out of the Repair Bay live proof.

Source: inferred by agent (Repair Bay live proof; code read on 2026-11-09)

#### Scenario: A fresh world reuses a catalog entity id

- **WHEN** a freshly authored world defines an entity whose id (such as `bo`) is also an exact binding in the shared asset catalog
- **THEN** bootstrap removes the colliding catalog binding for that entity, so the world does not inherit another world's presentation identity

#### Scenario: An authored category asset

- **WHEN** a world declares a `category_assets` entry for a category one of its entities has
- **THEN** bootstrap turns it into an exact binding for that entity, so broader shared component-value defaults cannot override it
