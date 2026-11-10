# causal-model-authoring Specification

## Purpose

The reviewable rule language (`world-substrate-causal-model/v0`): a model proposes rules as data, a local compiler derives what each rule reads and writes, and the rules run only after approval. Since 2026-10-15 pressing Create simulation is the approval.

**Action mechanic declaration v0** (folded on 2026-11-09 from `docs/contracts/action-mechanic-declaration-v0.md`, status `implemented`, reviewed through 2026-09-07, last commit `807053e`):

`world-substrate-causal-model/v0` is the reviewable causal companion to a
`world-substrate-authoring-bundle/v0`. The bundle says what is represented and
what action envelopes look like. The causal model says what those actions are
allowed to read, check, and change.

The causal model is **not source code**. A human or model may propose JSON, but
`src/world_substrate/action_authoring.py` interprets only the declaration
language below. Unknown state paths, participants, operators, or expression
forms are refused before an action rule can install.

## Requirements

### Requirement: One declaration per action kind

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

Source: inferred by agent (action mechanic declaration v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded). Create simulation as the approval: Brian, 2026-10-15: "it should just basically be a screen to type in what you want and then i button to create simulation", then "i approve" (Decision 005)

### Requirement: Authority is derived, not claimed

The proposer does **not** provide `reads` or `writes`. The compiler derives them
from selectors, checks, and effects and exposes them in the mechanics review.
Every touched entity also receives the engine's causal event id through the
compiler; an authored effect cannot write `last_cause_event_id` itself.

A compiled declaration is an ordinary action rule. Before a live run it is
installed through `MechanicProfile`, the profile is frozen, and every accepted
action still crosses `Engine.submit()` and the engine write-scope/atomic-commit
boundary. A declaration therefore does not gain more authority because an LLM
proposed it.

Source: inferred by agent (action mechanic declaration v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded). Create simulation as the approval: Brian, 2026-10-15: "it should just basically be a screen to type in what you want and then i button to create simulation", then "i approve" (Decision 005)

### Requirement: Supported state surface

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

Source: inferred by agent (action mechanic declaration v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded). Create simulation as the approval: Brian, 2026-10-15: "it should just basically be a screen to type in what you want and then i button to create simulation", then "i approve" (Decision 005)

### Requirement: Terminal condition

The causal model may declare one state-derived terminal predicate: select a
represented class of entities, apply typed checks, and require either all or any
to satisfy them. The compiler refuses empty selectors. `null` is valid when no
represented terminal can be justified; reaching a turn ceiling or exhausting
available actions is not silently converted into world completion.

Source: inferred by agent (action mechanic declaration v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded). Create simulation as the approval: Brian, 2026-10-15: "it should just basically be a screen to type in what you want and then i button to create simulation", then "i approve" (Decision 005)

### Requirement: Model generation and repair

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

Source: inferred by agent (action mechanic declaration v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded). Create simulation as the approval: Brian, 2026-10-15: "it should just basically be a screen to type in what you want and then i button to create simulation", then "i approve" (Decision 005)

### Requirement: Review and execution boundary

The World Builder displays the compiled rationale, derived reads/writes, checks,
effects, limits, tests, terminal, model, and cost. A fresh run requires a
separate explicit **Approve mechanics for run** action. Editing the represented
world after generation makes the mechanics stale and revokes that approval.

Declared tests are review obligations, not evidence that arbitrary model-written
tests executed. Interaction completeness remains fallible; the existing
mechanic-profile and causal-closure doctrine still applies.

Source: inferred by agent (action mechanic declaration v0, applying Decision 004, accepted 2026-09-07; the decider is not recorded). Create simulation as the approval: Brian, 2026-10-15: "it should just basically be a screen to type in what you want and then i button to create simulation", then "i approve" (Decision 005)

### Requirement: Processes, timing and linked participants (current code)

Since the contract was written the rule language gained optional `processes`: things the world does by itself with no actor, in the same selector, check and effect language, compiled to ordinary process rules with installer-checked scopes. A causal model may declare up to 28 processes (`MAX_PROCESSES`, `src/world_substrate/action_authoring.py:29`). Each process has a `timing` of `each_round` (the default, once per round) or `immediately` (a same-moment knock-on reaction under Decision 009) (`PROCESS_TIMINGS`, `action_authoring.py:30`), and may name linked participants resolved from the matching entity so one process event can change linked entities (`action_authoring.py:265-330`). Rule generation asks the model for a JSON object (`response_format={"type": "json_object"}`, `scripts/generate_causal_model.py:733`).

Source: inferred by agent (read from the code on 2026-11-09; the processes extension follows Brian, 2026-10-05: "my conception is that this is like continuous worlds we should be building"; immediate timing follows Decision 009, Brian, 2026-10-26: "i approve")

### Requirement: Create simulation is the approval (current code)

On the public landing page, pressing Create simulation is the explicit approval of the generated rules: the run starts at once and the rules open afterwards from "See how it works". The service still refuses a run that was not approved (HTTP 409).

Source: Brian, 2026-10-15: "it should just basically be a screen to type in what you want and then i button to create simulation", then "i approve" to running without a review stop (Decision 005)

### Requirement: Discovery cap (current code)

Action discovery offers at most 256 action instances per actor (`MAX_DISCOVERED_ACTIONS`, `src/world_substrate/action_authoring.py:31`). Instances past the cap are dropped without a visible refusal; making overflow visible is an open hardening item (open questions ledger).

Source: inferred by agent (read from the code on 2026-11-09)
