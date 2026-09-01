# Core contract v0

This contract defines the minimum neutral seam needed to reproduce the Castaway freshwater vertical without embedding Castaway-specific names in the engine.

## Records

### World

A world contains:

- `world_id`, `revision`, and integer `tick`;
- entity records indexed by stable ID;
- relation records indexed by stable ID;
- active process records;
- actor knowledge/observation records;
- accepted and rejected command records;
- causal events; and
- pinned content, rule, and engine identities.

### Entity

An entity declares:

- stable ID and category IDs;
- component records with typed values;
- location and ownership relations where applicable; and
- provenance linking content definitions to their source pack.

Components are explicit contracts, not an unconstrained prose bag. The first vertical needs identity, location, ownership, material, mass, container, liquid, temperature, condition, heat-source, and process-attachment components.

### Rule

Every action or process rule declares:

- stable rule ID and version;
- action/process kind;
- required categories/components;
- read and write paths;
- preconditions;
- effect function;
- sources, sinks, or conserved quantities;
- timing;
- emitted event schema; and
- explicit unsupported boundaries.

### Action

A typed action contains:

- actor ID;
- rule/action kind;
- object references;
- validated parameters;
- base world revision; and
- controller identity.

Natural-language text may accompany an action as explanation but is never executable input.

### Event

Each causal event records:

- event ID, tick, world revision, and rule ID/version;
- cause command/process;
- checks and their results;
- exact read/write references;
- before/after values or bounded deltas;
- source/sink/conservation ledger where relevant; and
- resulting state hash.

## Transition kernel

The records above form one canonical world `W`. The minimum state/action/
transition semantics are:

```text
observe_i(W)                    -> O_i
discover_i(W, query, cursor, limit) -> ActionPage_i
apply_r(W, action)              -> (W', events, status)
advance(W, steps)               -> (W', events)
replay(W_0, commands, pinned identities) -> (W_n, events, hashes)
```

`observe` and `discover` are actor-authorized projections of `W`; they neither
own alternate state nor calculate consequences. `O_i` is intentionally lossy:
two actors can receive different projections of the same canonical world.
A policy chooses a typed action from the discovered page. Only the registered
rule selected by that action, or a due registered process during `advance`, may
calculate a material state transition.

For an accepted action, state changes and causal events commit atomically. For a
rejected, invalid, stale, or unsupported action, the material entity, relation,
and process projection of `W'` equals that of `W`; the rejection record may
still be appended to the canonical journal. This separates evidence of an
attempt from effects on the modeled world. Replay consumes recorded commands
and pinned identities, not policy decisions, and must reproduce the same final
state, events, and hashes.

The intended interaction order is:

```text
actor observes -> engine projects authorized state
actor discovers -> registry instantiates currently available actions
policy chooses  -> typed action references the observed base revision
engine applies  -> rule validates, then atomically commits or rejects
engine advances -> due processes use the same transition authority
observer checks -> events, deltas, versions, and replay comparison
```

The positive fill-through-transfer path of this contract is implemented and evidenced
in the retained [first-fill](../../evidence/m1/first-fill-v0.json) and
[boiling](../../evidence/m1/boiling-v0.json),
[pour](../../evidence/m1/pour-v0.json),
[drink](../../evidence/m1/drink-v0.json), and
[transfer](../../evidence/m1/transfer-v0.json) receipts. Apply, discovery, minimal
observation, registered clock/hydration/thermal/cooling/fuel processes, atomic
rejection, causal events, semantic donor comparison, and replay exist for that
path. Safe and hazardous consumption effects plus capacity-checked whole-vessel
transfer are executable. Unsupported/malformed envelope counterexamples are
retained in the combined
[M1 evidence](../../evidence/m1/freshwater-v0.json). Cross-domain generality
remains an open obligation. The revision-bound
[end-to-end observation](../../evidence/m1/end-to-end-observation-v1.json)
validated the M1 maturity claim.

## Engine operations

### Discover

`discover(actor, query, cursor, limit) -> ActionPage`

The engine instantiates registered rules against actor-authorized local state. Results contain executable typed actions, blocked hints with reasons, and bounded navigation. Discovery does not advance time.

### Apply

`apply(action) -> ActionResult`

The engine checks the action kind, base revision, actor authority, references, and rule preconditions against canonical state. It commits all changes and events atomically or commits none.

Result status is one of:

- `accepted`;
- `precondition_failed`;
- `stale_revision`;
- `invalid_action`; or
- `unsupported_action`.

`invalid_action` means the command envelope or typed parameters are malformed.
`unsupported_action` means the envelope is valid but its action kind has no
registered executable rule. A registered action whose current-state guard fails
returns `precondition_failed`. None invokes an LLM consequence generator.

### Advance

`advance(steps=1) -> TickResult`

The world clock advances deterministically. Due processes execute in a documented order or through explicit conflict resolution. Every process change emits causal evidence.

### Observe

`observe(actor) -> ActorObservation`

The observation contains authorized state, received information, recent actor-visible events, relevant definitions, and an affordance-page entry point. It excludes remote or private state unless a rule delivered it.

### Snapshot and replay

`World.snapshot() -> SnapshotV1` emits a JSON-serializable object containing
`schema_version: world-substrate-snapshot/v1` and the complete canonical
material state. That state includes the engine ID, content ID, and rule-version
map; commands and events are intentionally absent. `World.from_snapshot()`
accepts only that version and reconstructs canonical state with empty history.

`Engine.replay_commands(initial_snapshot, commands, registry) -> Engine`
starts from the loaded snapshot and re-applies recorded accepted, rejected,
invalid, and advance commands without policy calls. The supplied executable
registry must match the snapshot's rule-version map. A durable replay bundle
also names the registry configuration identity because rule versions alone do
not encode constructor parameters. Evidence compares the reconstructed final
material hash and complete event sequence with the retained outputs.

## Implementation traceability obligation

Each implemented M1 rule must connect its stable rule ID and version to its
declared read/write paths, engine operation, positive and negative checks,
retained observation, and any adapted donor source. A contract entry or diagram
without that consumer path is proposed design, not an adopted capability.

## Canonical freshwater probe

Starting state:

- two actors, one clay vessel, and one separate drinking cup;
- one finite fresh-water source containing pathogens;
- one fire with finite fuel and heat power;
- rules for ownership, fill, heating attachment, heat distribution, boiling, evaporation, cooling, pouring, drinking, and giving.

Recorded choices:

1. fill the local clay vessel from the finite source;
2. attach it to the fueled fire;
3. advance canonical time until boiling rules remove pathogens;
4. detach it and advance canonical time while cooling runs automatically;
5. pour a measured amount into the separate cup;
6. advance, drink the cup's measured contents, and advance again;
7. take the same partly filled clay vessel, advance, give it to the other actor,
   and advance once more.

Required observations:

- water and fuel are actually deducted from their sources;
- salt, pathogens, heat, and volume change only through declared rules;
- the same vessel identity persists through every system;
- ongoing processes run without a new policy decision;
- rejected overfill and unsupported pressure actions are atomic;
- exact replay produces the same events and final hash.

## First-slice exclusions

The v0 contract does not require pressure, arbitrary natural-language action execution, continuous geometry, organizations, economics, seeded randomness, a browser UI, or a general authoring conversation.
