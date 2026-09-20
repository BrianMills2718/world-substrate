---
role: audit
status: active
reviewed_through: 2026-09-19
---

# Native Waltzman first-release static readiness review

This audit maps Decision 005's first native stopping rule to the current stacked
implementation. It is a **static/code-review result only**. It does not claim
that Linux tests, browser behavior, provider-backed one-shot generation, or the
retained diagnostic matrix have executed successfully.

The reviewed stack is:

1. PR #75 — native coordination execution / automatic Living Scene;
2. PR #79 — bounded one-shot native coordination authoring; and
3. PR #80 — retained baseline comparison and final inspection closure.

## 1. Describe a new supported coordination situation

Implemented by:

- `scripts/world_builder_app.js` — one-shot coordination description field;
- `/world-builder/api/generate-draft` in `scripts/world_builder_service.py`;
- `scripts/native_coordination_authoring.py` — bounded proposal schema,
  validation, exact source-description retention, and deterministic compilation
  to `world-substrate-authoring-bundle/v0`.

The model proposes configuration only. It cannot author executable Python,
write scopes, or causal effects in this path.

Static verdict: **implemented, execution unverified**.

## 2. Understand inferred structure, assumptions, and executable rules

The one-shot review now shows, together:

- the exact source description;
- inferred represented members/resources/gate/reports;
- extracted requirement-to-surface coverage;
- the explicit coverage limitation;
- inferred assumptions;
- explicitly unsupported requests; and
- compiler-derived review of the exact shared coordination mechanics.

Changing the description or generated bundle makes that review stale and
invalidates mechanics approval.

Static verdict: **implemented, browser behavior unverified**.

## 3. Explicitly approve and run through World Substrate Engine

The existing Builder approval boundary remains mandatory.

Native execution requires:

- a valid authoring bundle;
- a causal model that compiles against that bundle;
- exact equality with the reviewed shared coordination causal model;
- explicit `approved=true`;
- `execution_mode="native_coordination"`; and
- deterministic scripted execution.

The native run calls `run_native_coordination`, which builds and executes the
ordinary World Substrate Engine. Provider spend for execution is zero.

Static verdict: **implemented, runtime execution unverified**.

## 4. Receive automatic UI without a hand-authored scene

`scripts/run_native_coordination.py` creates the Living Scene profile from the
structured bundle and canonical live projection. The generated profile feeds the
generic composed Living Scene renderer. No per-generated-world scene file is
required.

The native acceptance matrix requires actors, resources, gate state,
canonical timeline, selection inspection, information movement, information
visibility inspection, and rule-check feedback.

Static verdict: **implemented, rendered output unverified**.

## 5. Inspect important result, rule checks, and information visibility

The Living Scene projection now exposes action feedback as:

- retained rule/check label;
- boolean satisfied/failed verdict; and
- legacy failed-reason labels.

It deliberately omits retained check `actual` and `expected` operands from
public presentation payloads.

Both generic renderers show `failed:` and `passed:` labels for the selected
canonical event boundary.

Information inspection remains actor-oriented:

- represented transmission lines show source -> recipient;
- public rendering hides direct-message content;
- actor selection exposes represented delivery count and latest represented
  source/topic while keeping private content private in the public view.

The executable native acceptance matrix now requires both
`failed_check_feedback`, `satisfied_check_feedback`, and
`information_visibility_inspection`.

Static verdict: **implemented, browser/runtime verification pending**.

## 6. Change one supported condition and compare without losing the original

The first comparison surface supports exactly one intervention:

`gate.required_approvals`.

The service:

1. validates and clones the retained baseline initial bundle;
2. validates the represented delivery/member/information family boundary;
3. refuses impossible or unchanged thresholds;
4. changes only the gate approval-threshold path;
5. recompiles the exact same shared mechanics against the comparison bundle;
6. executes a second fresh native Engine run.

The Builder retains the successful baseline bundle, approved causal model,
trace, service trace id, summary, and Living Scene. Comparison failure does not
discard it. Baseline and comparison execution are serialized to avoid retained
state races.

A provider-free integration test runs both baseline and comparison through the
real native runner and requires:

- zero provider spend in both runs;
- the same mechanic-profile id;
- terminal completion in both runs;
- unchanged baseline input; and
- materially different retained trajectories/final states.

Static verdict: **implemented, test execution pending**.

## Remaining release blockers

No further product-code gap is identified by this static review.

The release remains blocked on observed execution evidence:

- the native coordination acceptance matrix on Linux/Ubuntu;
- the focused PR #75/#79/#80 tests;
- `python scripts/check_project.py`;
- actual retained diagnostic artifacts and their hash manifest;
- classification of the previously Windows-observed Waltzman living-replay
  manifest mismatch;
- at least one provider-backed one-shot draft request through the real service;
- browser verification of the generated review/run/comparison surfaces.

Until those are observed, PRs #75, #79, and #80 should remain draft and should
not be represented as a completed native release.
