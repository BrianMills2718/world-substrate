# transition-engine Specification

## Purpose

How canonical world state changes: one engine commits or refuses each transition, enforces declared write scopes, keeps rule-facing hooks read-only and records each attempt with its cause. Declared read scopes are recorded but not enforced.

**Core contract v0** (folded on 2026-11-09 from `docs/contracts/core-v0.md`, given in its Status line, last commit `2e4aa47`):

**Status:** implemented M1 contract  
<!-- status-facts
exact_replay_works: true
-->

**Scope note:** deterministic time and exact replay below describe the promoted M1 seam. Under [Decision 002](../../../docs/decisions/002-observability-and-replay.md), they are not universal requirements for later contract versions. This document is preserved rather than silently rewritten.

This contract defines the minimum neutral seam needed to reproduce the Castaway freshwater vertical without embedding Castaway-specific names in the engine.

**Transition envelope contract v0** (folded on 2026-11-09 from `docs/contracts/transition-envelope-v0.md`, given in its Status line, last commit `5606eb2`):

**Status:** partially implemented. Singular commit, atomic refusal, and causal trace are implemented in `Engine.apply`/`Engine.advance`. Independently enforced **write** scope is implemented (`scope_violation`). Rule-facing discovery, applicability, consequence, progress, and trigger hooks run against detached state and are enforced as read-only; effect application also receives detached state, while `revision`, commands, and events remain coordinator-owned. Independently enforced **read** scope is not implemented: declared reads are recorded on every event and unchecked. Institutional coupling of several bearers' effects into one transition is unimplemented and untested.  
**Purpose:** give one enclosing action or process sole authority to commit a causally coupled state transition

<!-- status-facts
write_scopes_enforced: true
read_scopes_enforced: false
-->

**Read-scope enforcement contract v0** (folded on 2026-11-09 from `docs/contracts/read-scope-enforcement-v0.md`, given in its Status line, last commit `eab5f09`):

**Status:** proposed, not implemented. Declared **read** scopes are recorded on every event and unchecked; declared **write** scopes are enforced (`scope_violation`). This document is the design the roadmap's open obligation asks for, with the mechanism named, its cost measured, and its blind spots stated. Nothing here is built.  
**Purpose:** decide whether an undeclared read can be caught at runtime, and at what price

## Requirements

### Requirement: Core: Records: World

A world contains:

- `world_id`, `revision`, and integer `tick`;
- entity records indexed by stable ID;
- relation records indexed by stable ID;
- active process records;
- actor knowledge/observation records;
- accepted and rejected command records;
- causal events; and
- pinned content, rule, and engine identities.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Records: Entity

An entity declares:

- stable ID and category IDs;
- component records with typed values;
- location and ownership relations where applicable; and
- provenance linking content definitions to their source pack.

Components are explicit contracts, not an unconstrained prose bag. The first vertical needs identity, location, ownership, material, mass, container, liquid, temperature, condition, heat-source, and process-attachment components.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Records: Rule

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

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Records: Action

A typed action contains:

- actor ID;
- rule/action kind;
- object references;
- validated parameters;
- base world revision; and
- controller identity.

Natural-language text may accompany an action as explanation but is never executable input.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Records: Event

Each causal event records:

- event ID, tick, world revision, and rule ID/version;
- cause command/process;
- checks and their results;
- exact read/write references;
- before/after values or bounded deltas;
- source/sink/conservation ledger where relevant; and
- resulting state hash.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Transition kernel

The records above form one canonical world `W`. The minimum state/action/
transition semantics are:

```text
observe_i(W)                    -> O_i
discover_i(W, query, cursor, limit) -> ActionPage_i
apply_r(W, action)              -> (W', events, status)
advance(W, steps)               -> (W', events)
replay(W_0, commands, pinned identities) -> (W_n, events, hashes)
```

The v0 `tick`/`advance` contract is the implemented M1 timing baseline. `Engine.advance()` currently checks registered processes step-by-step through their `due(world)` hooks; it does **not** claim an independently scheduled future-event queue, duration-bearing activities, or multiple canonical clocks. The richer target keeps one canonical simulated timeline while allowing mechanisms to have independent cadences. See [multi-timescale execution](../../../docs/research/multi-timescale-execution-2026-09.md).

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
in the retained [first-fill](../../../evidence/m1/first-fill-v0.json) and
[boiling](../../../evidence/m1/boiling-v0.json),
[pour](../../../evidence/m1/pour-v0.json),
[drink](../../../evidence/m1/drink-v0.json), and
[transfer](../../../evidence/m1/transfer-v0.json) receipts. Apply, discovery, minimal
observation, registered clock/hydration/thermal/cooling/fuel processes, atomic
rejection, causal events, semantic donor comparison, and replay exist for that
path. Safe and hazardous consumption effects plus capacity-checked whole-vessel
transfer are executable. Unsupported/malformed envelope counterexamples are
retained in the combined
[M1 evidence](../../../evidence/m1/freshwater-v0.json). Cross-domain generality
remains an open obligation. The revision-bound
[end-to-end observation](../../../evidence/m1/end-to-end-observation-v1.json)
validated the M1 maturity claim.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Engine operations: Discover

`discover(actor, query, cursor, limit) -> ActionPage`

The engine instantiates registered rules against actor-authorized local state. Results contain executable typed actions, blocked hints with reasons, and bounded navigation. Discovery does not advance time.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Engine operations: Apply

`apply(action) -> ActionResult`

The engine checks the action kind, base revision, actor authority, references, and rule preconditions against canonical state. It commits all changes and events atomically or commits none.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Engine operations: Causal event fields

Every event carries, in addition to the transition fields below:

- `causal_bearer` — who or what caused this. `{kind: "actor", id, controller}`
  for an attempt, `{kind: "process", id: <rule_id>, controller: null}` for a
  process.
- `semantic_binding` — the Linguistic Core sense and participant roles bound to
  the attempt, or `null` when the action kind has no binding. Six of seven M1
  action kinds are still unbound, so `null` is the common case and says so
  rather than being omitted.
- `observation` — the bounded, actor-authorised projection the bearer could see
  at the moment it chose, captured before anything mutates. `null` for a
  process, which has no observer, and for an attempt whose actor cannot
  observe.

These are the three of [Decision 002](../../../docs/decisions/002-observability-and-replay.md)'s
eight required fields that the engine computed and did not attach until this
version. `null` is emitted explicitly so "there was no observer" is
distinguishable from "not recorded".

Result status is one of:

- `accepted`;
- `precondition_failed`;
- `stale_revision`;
- `invalid_action`;
- `unsupported_action`; or
- `scope_violation`.

`invalid_action` means the command envelope or typed parameters are malformed.
`unsupported_action` means the envelope is valid but its action kind has no
registered executable rule. A registered action whose current-state guard fails
returns `precondition_failed`. None invokes an LLM consequence generator.

`scope_violation` means the attempt was applicable and the rule ran, but the
resulting changes reached state paths the rule never declared in its
`write_paths`. The candidate world is discarded, so the rule's own entitled
writes do not commit either. Its failing check names every undeclared path.
This reports a defective *rule*, not a defective attempt: it is the enforcement
of the declared read/write scope required by
[the transition envelope](spec.md), and the engine -- not the
rule -- owns it.

A declared write path is a prefix, and a `<name>` segment matches exactly one
path segment. For an action, a placeholder may bind only to an entity the
attempt itself references (`actor`, `vessel`, `source`, `target`,
`destination`, `recipient`), so a correctly shaped path cannot reach a third
party. Processes are universally quantified over the entities they apply to, so
their placeholders match any entity. `revision` is engine-owned and exempt.

A process has no attempt to refuse, so a process that writes outside its
declared scope raises `ScopeViolation` and `advance` restores the whole tick.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Engine operations: Advance

`advance(steps=1) -> TickResult`

The world clock advances deterministically. Due processes execute in a documented order or through explicit conflict resolution. Every process change emits causal evidence.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Engine operations: Observe

`observe(actor) -> ActorObservation`

The observation contains authorized state, received information, recent actor-visible events, relevant definitions, and an affordance-page entry point. It excludes remote or private state unless a rule delivered it.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Engine operations: Snapshot and replay

`World.snapshot() -> SnapshotV1` emits a JSON-serializable object containing
`schema_version: world-substrate-snapshot/v1` and the complete canonical
material state. That state includes the engine ID, content ID, and rule-version
map; commands and events are intentionally absent. `World.from_snapshot()`
accepts only that version and reconstructs canonical state with empty history.
It may also receive a world-local component-type map. Those types override same-
named process-global component registrations for that load only, so runtime-
authored worlds can replay without mutating or colliding with the global world-
pack registry.

`Engine.replay_commands(initial_snapshot, commands, registry, component_types=None) -> Engine`
starts from the loaded snapshot and re-applies recorded accepted, rejected,
invalid, and advance commands without policy calls. The supplied executable
registry must match the snapshot's rule-version map. A durable replay bundle
also names the registry configuration identity because rule versions alone do
not encode constructor parameters. Evidence compares the reconstructed final
material hash and complete event sequence with the retained outputs.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Implementation traceability obligation

Each implemented M1 rule must connect its stable rule ID and version to its
declared read/write paths, engine operation, positive and negative checks,
retained observation, and any adapted donor source. A contract entry or diagram
without that consumer path is proposed design, not an adopted capability.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: Canonical freshwater probe

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

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Core: First-slice exclusions

The v0 contract does not require pressure, arbitrary natural-language action execution, continuous geometry, organizations, economics, seeded randomness, a browser UI, or a general authoring conversation.

Source: inferred by agent (core contract v0, written for the M1 Castaway freshwater extraction under Decision 001, decided by the user on 2026-08-31; Decision 002, accepted 2026-09-02, keeps exact replay to the M1 seam; the decider of Decision 002 is not recorded)

### Requirement: Transition envelope: Pipeline

```text
actor/process observation
  -> semantic sense and role binding
  -> local mechanic selection
  -> applicability and authorization
  -> proposed effects
  -> resource and invariant validation
  -> one commit or refusal
  -> causal trace
```

Source: inferred by agent (transition envelope contract v0, applying Decision 003, accepted 2026-09-02; the decider of Decision 003 is not recorded)

### Requirement: Transition envelope: Requirements

- An attempt identifies its causal bearer and current world revision or snapshot identity.
- Semantic binding and mechanic selection occur before effect proposal.
- The selected mechanic can read and propose writes only within independently enforced state-path scope.
- Discovery, applicability checks, declared consequences, process progress, and process triggers are read-only. The coordinator invokes them against detached world state and treats a mutation as an authority violation rather than allowing it to reach canonical state.
- Effect application receives detached world state. Mechanics may propose only material changes within their declared authority; they do not own the world revision or causal history.
- `revision`, command records, and causal events are coordinator-owned. Rule code cannot advance the revision, append or rewrite history, or use a rejected candidate to modify already-committed history.
- Applicability rules, permissions, contracts, pricing rules, and institutions may inspect state and propose effects. They may not commit effects belonging to an enclosing transition that can still fail.
- The coordinator validates all causally coupled effects before committing any of them, then attaches the accepted command/event history itself.
- A refusal leaves canonical state unchanged, except for separately modeled causal events whose occurrence is independent of the refused transition.
- Successful commit records the accepted operations, relevant checks, commit order, and resulting persistent state identity.
- Derived interpretations may observe the committed history but cannot reapply its effects.

This is not a requirement for universal ACID transactions. Independent actions may commit independently. The singular boundary applies when several effects belong to one claimed causal transition.

Source: inferred by agent (transition envelope contract v0, applying Decision 003, accepted 2026-09-02; the decider of Decision 003 is not recorded)

### Requirement: Transition envelope: Examples

Two voluntary gives are independent transitions. Robin may give a spear and Friday may renege on giving coconuts. A derived `exchange` view can recognize the reciprocal history but cannot transfer either asset again.

An installed escrow release is one institutionally coupled transition. Asset release, payment, and escrow-state changes either pass validation and commit together or refuse together.

A pressure check may propose vessel damage, capability revocation, fluid release, and relation handoff as one coupled transition when the selected mechanics profile defines them as consequences of the same rupture.

Source: inferred by agent (transition envelope contract v0, applying Decision 003, accepted 2026-09-02; the decider of Decision 003 is not recorded)

### Requirement: Read scope (proposed, not built): Why writes were easy and reads are not

A write leaves a trace in state. `Engine.apply` clones the world, lets the rule
run, diffs `material_dict()` before against after, and any changed path the
rule never declared is a `scope_violation`. The evidence is the diff.

A read leaves nothing. After a rule inspects `vessel.condition.value` the world
is byte-identical, so no amount of state comparison can recover the fact. The
read has to be observed while it happens or not at all.

Source: inferred by agent (a proposed design; nobody has approved building it)

### Requirement: Read scope (proposed, not built): Mechanism: a recording proxy at the rule boundary

`Engine` passes the rule a proxy that wraps `World`, records every attribute and
key access as a dotted path, and returns a proxy for any value that could be
read further:

```text
rule.checks(RecordingWorld(world, recorder), action)
  -> recorder holds {"world.entities.clay-pot.liquid.volume_ml", ...}
  -> compare against rule.read_paths, with the same placeholder matching
     `_path_permitted` already uses for writes
  -> undeclared reads become a finding, or a refusal
```

The comparison is the part that already exists: read and write paths use one
grammar, and `_path_permitted` already resolves `<name>` placeholders against
the entities an attempt named. Only the observation is new.

This was prototyped against the freshwater world to get the numbers below. The
prototype is not in the repository; it existed to make this document's cost
claim a measurement instead of a guess.

Source: inferred by agent (a proposed design; nobody has approved building it)

### Requirement: Read scope (proposed, not built): Measured cost

Isolated `rule.checks()` on the transfer world, 2000 repetitions, best of three,
warmed:

| | per call | total |
| --- | --- | --- |
| plain | 8.5 us | 16.9 ms |
| through the recording proxy | 92.0 us | 184.1 ms |
| **overhead** | **10.9x** | |

The prototype recorded 71 distinct read paths across a 30-action trace, 64 of
them entity-level field reads.

10.9x is affordable in a verification pass and not in a run loop. `checks()` is
called for every discovered action on every `discover()`, so a page that offers
twenty affordances pays it twenty times before an actor does anything.

Source: inferred by agent (a proposed design; nobody has approved building it)

### Requirement: Read scope (proposed, not built): Recommended staging

1. **Recording, off by default.** A `--verify-reads` mode for probes, tests and
   the mechanic installer. It reports undeclared reads as findings and changes
   no behaviour. This is where the 10.9x is paid and it is the right price for
   a check that runs deliberately.
2. **Refusing, once declarations are clean.** Only after a full trace under (1)
   reports nothing, and only behind an explicit flag, because a false positive
   here refuses a legitimate action rather than emitting a warning.

Do not make it always-on. The project's own tool-loading default is that a
capability not needed in most runs should not be paid for in every run.

Source: inferred by agent (a proposed design; nobody has approved building it)

### Requirement: Read scope (proposed, not built): What it still cannot see

- **Reads through an unproxied reference.** A rule that pulls a raw object out
  once and passes it to a module-level helper reads through the raw object, and
  the proxy is not in that path. This is the same indirection blind spot
  `assay_undeclared_component_reads` has, arrived at from the other direction.
- **Per-execution, not static.** It proves that no undeclared read *occurred in
  this run*. A rule that reads a field only on a branch the run did not take is
  not covered, so this is a test-coverage-shaped guarantee, not a proof.
- **Bulk projections read everything.** `as_dict()` and `dataclasses.asdict()`
  touch every field of a component, so any rule that calls one appears to read
  the whole component. Either the projection is exempted, and reads through it
  become invisible, or it is not, and every such rule must declare a read it
  does not conceptually perform. Neither is obviously right and this is the
  design's weakest point.
- **The proxy can change behaviour if it is incomplete.** The prototype's first
  version defined `__len__` but not `__bool__`, so `if vessel:` became
  `len(Entity)` and raised `TypeError` inside a rule that was correct. A
  transparent proxy has to emulate the whole protocol surface it stands in
  front of, and getting that wrong is a defect in the enforcement mechanism
  that presents as a defect in the rule.
- **Reads by processes are universally quantified.** A process iterates all
  entities, so its recorded paths name every entity it touched while its
  declaration names `<x>`. The write-scope guard already passes `None` for
  bound refs on processes; reads need the same treatment and the same loss of
  precision.

Source: inferred by agent (a proposed design; nobody has approved building it)

### Requirement: Read scope (proposed, not built): Relationship to the existing assay

`assay.assay_undeclared_component_reads` attacks the same gap statically, by
scanning rule source for component access. It is a heuristic with a stated
blind spot, and it audits declarations rather than executions. The two are
complementary: the assay can flag a read on a branch no test exercises, and the
proxy can catch a read through indirection the assay cannot name. Neither is
sufficient, which is the same shape as the three interaction assays.

Source: inferred by agent (a proposed design; nobody has approved building it)
