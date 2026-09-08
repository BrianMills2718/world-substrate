---
role: contract
status: implemented
reviewed_through: 2026-09-07
---

# Action mechanic declaration v0

`world-substrate-causal-model/v0` is the reviewable causal companion to a
`world-substrate-authoring-bundle/v0`. The bundle says what is represented and
what action envelopes look like. The causal model says what those actions are
allowed to read, check, and change.

The causal model is **not source code**. A human or model may propose JSON, but
`src/world_substrate/action_authoring.py` interprets only the declaration
language below. Unknown state paths, participants, operators, or expression
forms are refused before an action rule can install.

## One declaration per action kind

Each `world-substrate-action-mechanic/v0` declaration names exactly one action
signature from the authoring bundle and declares:

- `mechanic_id`, `version`, `action_kind`, and a review rationale;
- an actor selector and one selector for every `entity_ref` action field;
- finite choices for every scalar action parameter;
- causal checks over literals, action fields, participant state, participant
  identities, and represented ownership references;
- effects that `set`, `add`, or `subtract` a supported represented state field;
- known limits, declared tests, and optional semantic bindings.

Selectors must constrain at least one category or component. A component path
may only be read or written through a participant selector that requires that
component. Scalar parameter choices are finite so discovery remains bounded.

## Authority is derived, not claimed

The proposer does **not** provide `reads` or `writes`. The compiler derives them
from selectors, checks, and effects and exposes them in the mechanics review.
Every touched entity also receives the engine's causal event id through the
compiler; an authored effect cannot write `last_cause_event_id` itself.

A compiled declaration is an ordinary action rule. Before a live run it is
installed through `MechanicProfile`, the profile is frozen, and every accepted
action still crosses `Engine.submit()` and the engine write-scope/atomic-commit
boundary. A declaration therefore does not gain more authority because an LLM
proposed it.

## Supported state surface

Action declarations may currently address:

- `location.location_id`;
- `ownership.owner_ref`;
- `portable.portable`;
- fields under `components.<declared-component>.<field>`.

`last_cause_event_id` may be inspected but is engine-owned for writes. Revision,
commands, events, registry state, arbitrary Python attributes, and undeclared
components are outside the language.

Expression forms are deliberately small: `literal`, `action_field`, participant
`path`, participant `entity_id`, participant `owner_ref`, and `event_id`. Checks
support equality/inequality, numeric ordering, and bounded `contains` semantics.
Effects support `set`, `add`, and `subtract`, with type compatibility checked at
compile time.

## Terminal condition

The causal model may declare one state-derived terminal predicate: select a
represented class of entities, apply typed checks, and require either all or any
to satisfy them. The compiler refuses empty selectors. `null` is valid when no
represented terminal can be justified; reaching a turn ceiling or exhausting
available actions is not silently converted into world completion.

## Model generation and repair

`scripts/generate_causal_model.py` gives a model the authoring bundle, the exact
allowed state paths, the response contract, and optional human guidance. The
model returns JSON text; no returned source is executed. The local compiler is
the authority gate.

One compiler-guided repair is allowed. If the first proposal uses an invalid
path or otherwise violates the language, the exact compiler error is returned
to the proposer once. Both attempts share one trace id and one hard model-budget
ceiling. If the repaired declaration still fails, generation fails and nothing
installs.

Provider-native JSON Schema is intentionally not an authority dependency. A
real Luna probe found that one OpenRouter route rejected a richer nested schema
transport even though the same proposal could be safely validated locally. The
system therefore parses JSON from ordinary bounded model output and relies on
the local compiler, not provider decoding, for causal acceptance.

## Review and execution boundary

The World Builder displays the compiled rationale, derived reads/writes, checks,
effects, limits, tests, terminal, model, and cost. A fresh run requires a
separate explicit **Approve mechanics for run** action. Editing the represented
world after generation makes the mechanics stale and revokes that approval.

Declared tests are review obligations, not evidence that arbitrary model-written
tests executed. Interaction completeness remains fallible; the existing
mechanic-profile and causal-closure doctrine still applies.
