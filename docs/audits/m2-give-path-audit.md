---
role: audit
status: active
reviewed_through: 2026-09-02
authority_refs:
  - ../decisions/002-observability-and-replay.md
  - ../decisions/003-semantic-mechanical-boundary.md
  - ../contracts/semantic-mechanical-binding-v0.md
  - ../../roadmap/README.md
---

# M2 audit: the M1 `give` path against the proposed contracts

Required by roadmap M2's "M1 audit included in the slice." Five items, each
answered from direct inspection of the running code (file:line references
below), not from the contracts' own prose. This is evidence, not a decision:
architecture, contracts, and roadmap retain their own narrower authority.

## 1. Does `owner` mean bounded possession/control, or legal title?

**Possession/control.** Every read of `OwnershipState.owner_ref` gates a
mechanical capability check, never a rights, sale, lien, or beneficiary
distinction:

- `mechanisms/ownership.py:24,73,111,236` — gates whether an actor may `take`
  or `give` a vessel (must currently hold or be the place's custodian).
- `mechanisms/liquid.py:16`, `mechanisms/thermal.py:15` — gate whether a
  vessel is in a location where pour/heat actions apply.
- `mechanisms/ownership.py:137,274`, `mechanisms/thermal.py:161` — the only
  three places `owner_ref` is *written*, each a direct consequence of a
  mechanic committing (take, give, or a fire being extinguished returning a
  vessel to its place).

There is no separate title/beneficiary field anywhere in `model.py`; `owner_ref`
*is* current custody, full stop. A world wanting legal title distinct from
possession (e.g. a loan, a lien, a trustee) would need a new component and
mechanic — `owner_ref` cannot be reused to mean that without changing its
existing semantics everywhere above.

## 2. Are any transition effects committed before the enclosing action succeeds?

**No**, structurally, for both action and process transitions:

- `engine.py:184-219` (`Engine.apply`): `rule.checks()` runs against
  `self.world` directly (read-only — verified no assignment into `world` or
  its entities in any `checks()` implementation across
  `mechanisms/{ownership,liquid,thermal}.py`). `rule.apply()` — the only
  method that mutates — runs exclusively on `candidate = self.world.clone()`,
  and `self.world` is reassigned to `candidate` only after `candidate.validate()`
  succeeds. A failing check or a failing validation never reaches the
  reassignment.
- `engine.py:275-296` (`Engine.advance`): uses a coarser save/restore
  envelope instead of the same per-action clone: `saved = self.world.clone()`
  is taken once per tick, and `self.world.commands.append(...)` writes
  directly to `self.world` *before* processes run. But this is wrapped in
  `try/except Exception: self.world = saved; raise` — any failure during
  process application restores the pre-tick state including that command
  append. No partial effect survives a failed tick.
- One local exception worth naming precisely, not a violation:
  `mechanisms/liquid.py:489` constructs a `preview = LiquidState(...)` inside
  a `checks()` method to evaluate a hypothetical resulting volume. It is a
  plain local dataclass instance never assigned to any entity or `world` —
  a read-only what-if computation, not a mutation.

## 3. Mapping current events to Decision 002's eight observability fields

| Decision 002 field | Current event field | Coverage |
| --- | --- | --- |
| what a causal bearer observed or read | *(none — `engine.observe()` output is never attached to the event)* | **gap** |
| what it attempted / what process fired | `cause` → cross-reference `world.commands[cause].action`; `rule_id`/`rule_version` | indirect, workable |
| Linguistic Core sense and roles bound to the attempt | *(none — `semantic.py`'s `SEMANTIC_BINDINGS` is a static registry, never attached to an event)* | **gap** |
| installed mechanic and authority selected | `rule_id`/`rule_version` (mechanic, yes); no field for authority/causal bearer | **partial gap** |
| applicability/authorization/resource/invariant checks | `checks` (full `Check.as_dict()` list, name + ok + actual + expected) | covered |
| proposed and committed state-path changes | `declared_write_paths` (schema) + `changes` (`differences(before, after)`) | covered |
| refusal, failure, unsupported-interaction reasons | `status` (`accepted`/`stale_revision`/`precondition_failed`/`unsupported_action`/`invalid_action`) + failing `checks` entries | covered |
| resulting persistent state identity or snapshot | `hash_after` + `world_revision` (content-addressed identity, not a full embedded snapshot — Decision 002 explicitly permits this) | covered |

**Five of eight covered, one partially covered, two are real gaps.** Both gaps
are the same shape: the binding contract (semantic-mechanical-binding-v0.md)
and the observation the actor had are both real today (`semantic.py`,
`engine.observe()`) but neither is *wired into the causal event itself* — an
inspector reading `world.events` cannot currently see what sense/roles were
bound to an accepted `give`, or what the actor observed before choosing it,
without separately consulting `semantic.py` and re-deriving the observation.
Closing this is a `core-v0` schema change (adding fields to `_event()`), not a
new mechanic — left for a future slice rather than done here, per the M2
failure boundary ("propose a versioned transition contract rather than
silently changing the implemented M1 contract").

## 4. Which current checks are goal-relative M1 invariants vs. universal substrate laws?

Classified from `mechanisms/ownership.py`'s `GiveRule`/`TakeRule` (10 named
checks total) plus the one check `Engine.apply` adds itself:

**Universal** (would apply to any world built on this substrate, regardless of content):
- "Base revision is current" (`engine.py:189` — optimistic-concurrency, enforced centrally, not per-mechanic)
- "Actor/Giver/Recipient/Vessel exists" (existence of every entity an action references)

**Goal-relative** (specific to this world's freshwater/survival content, not substrate laws):
- "Actor is alive" / "Giver is alive" (health/alive is Castaway-content, not a substrate concept)
- "Portable vessel" (this world's content decision that some containers cannot be carried)
- "Vessel is intact" (this world's condition/damage system)
- "Vessel is removed from heat" (freshwater-specific — a vessel mid-boil can't change hands)
- "Recipient capacity including vessel" (this world's weight-based carrying-capacity content)

**Mixed:** "Living distinct recipient here" and "Vessel is carried by giver" combine a
universal pattern (co-location required to interact; only the current holder
may transfer) with goal-relative specifics (alive-check; the `actor:`/`place:`
string encoding).

Concretely: 2 of 10 checks are substrate-universal; the rest are this world's
content. A second, materially different reference world (M4) should expect to
re-specify nearly all of the goal-relative checks and can rely on only the
existence and revision-currency checks coming free from the substrate.

## 5. Gap between current action IDs and Linguistic Core sense/role bindings

M1 implements seven action kinds (`rules.py`): `fill`, `heat`, `unheat`,
`pour`, `drink`, `take`, `give`. As of this audit, exactly **one** —
`give` — has a registered semantic binding (`semantic.py:SEMANTIC_BINDINGS`,
added this slice). The other six have no Linguistic Core sense/role binding
at all; they exist only as bare `kind` strings with no semantic layer above
them. This is the literal, current state of the gap the roadmap asked to be
recorded — not a judgment about which of the six should be bound next.
