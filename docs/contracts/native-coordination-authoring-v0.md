---
role: contract
status: proposed
reviewed_through: 2026-09-19
---

# Native coordination one-shot authoring v0

This contract defines the bounded natural-language front door for the first
native Waltzman release. It does not define arbitrary-world generation or
conversational refinement.

## Product path

The v0 path is:

```text
one description
  -> versioned native-coordination draft
  -> deterministic World Substrate authoring bundle
  -> requirement / assumption / unsupported-intent review
  -> shared reviewed coordination mechanics
  -> explicit mechanics approval
  -> native World Substrate Engine execution
  -> automatic Living Scene
```

The original description is retained exactly in the draft artifact.

## Model authority

The model proposes configuration only:

- world label, summary, and location;
- 3-6 represented members and roles;
- one uniquely authorized member;
- exactly four represented prerequisites/resources;
- exactly one restorable prerequisite that begins below its requirement;
- direct represented reports with distinct recipients;
- an approval threshold;
- extracted requirement coverage;
- explicit assumptions; and
- explicit unsupported requests.

The model does **not** author executable law, Python, write scopes, or causal
effects in this path.

The executable family remains the reviewed shared native coordination model:

- `coordination.action.communicate`;
- `coordination.action.approve`;
- `coordination.action.intervene`; and
- `coordination.action.finalize`.

The deterministic draft compiler produces the ordinary
`world-substrate-authoring-bundle/v0` consumed by the existing compiler and
Engine.

## Intent completeness boundary

The review distinguishes:

- extracted requirements and the represented surface assigned to each;
- inferred assumptions;
- explicitly unsupported requests; and
- compiler-derived executable mechanics.

Requirement coverage is review evidence, not proof that every material clause
in the description was extracted correctly. The UI must preserve the original
description so a user can compare it with the inferred structure.

Unsupported requests must remain visible. The v0 path may visibly narrow them;
it must not silently convert them into narration or pretend they execute.

## Supported family

The first release intentionally supports one bounded coordination family:

- 3-6 members in one shared coordination space;
- exactly four prerequisites/resources;
- one unique intervention authority;
- one restorable prerequisite initially below requirement;
- direct source-to-recipient represented information delivery;
- unique report recipients sufficient to cover the approval threshold;
- member approval;
- represented prerequisite restoration; and
- gate finalization.

Arbitrary scheduling, probabilistic behavior, deception, hidden cognition,
custom institution semantics, generalized activities, and arbitrary generated
mechanics are outside this one-shot path unless separately represented and
reviewed by a later contract.

## Approval and staleness

Generating a draft does not approve mechanics.

The Builder receives the exact shared causal model and compiler-derived review,
sets `mechanicsApproved=false`, and requires the ordinary explicit approval
before a run.

The generated bundle is editable. If it changes after draft/mechanics review,
the review is marked stale and mechanics approval is invalidated. The original
description, requirement review, and assumptions remain provenance for the
generated version rather than silently changing to describe later edits.

If a user replaces the shared mechanics through the generic mechanics
generator, execution returns to the generic authored-world path. It may not
continue to claim native-coordination execution.

## Execution authority

A one-shot native draft uses explicit
`execution_mode="native_coordination"`.

The service accepts that mode only when:

1. the authoring bundle validates;
2. the causal model compiles against the bundle;
3. the supplied causal model exactly equals the reviewed shared coordination
   causal model;
4. mechanics approval is explicit; and
5. policy is the deterministic scripted native path.

The native runner remains the same Engine/Living Scene path proven by the
native coordination vertical. Provider spend for execution is zero.

Generic authored worlds keep `execution_mode="authored_world"` and the
existing scripted/LLM policy seam.

## Provider spend

One-shot extraction shares the World Builder's existing server-side rate limit
and daily spend ledger. Draft generation has its own bounded per-request cap.

A provider failure after reservation fails closed and charges the reserved
amount under the existing budget-ledger semantics.

## Debugging evidence

The Builder log records the complete `/generate-draft` request and response,
including:

- retained draft;
- compiled authoring bundle;
- shared causal model;
- requirement/assumption review;
- model and cost;
- daily committed cost; and
- trace id.

The subsequent `/run` response retains the Engine trace and Living Scene HTML
through the existing log surface.

## First verification

The focused static/runtime suite for this contract is:

```bash
python -m pytest \
  tests/test_native_coordination_authoring.py \
  tests/test_world_builder_service.py \
  tests/test_world_authoring_builder.py
```

This does not replace the native coordination Linux gate from
`native-coordination-diagnostics-v0.md`. Until that underlying gate is
executed, this stacked slice remains unverified end to end.
