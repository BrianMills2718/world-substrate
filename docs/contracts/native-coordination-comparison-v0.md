---
role: contract
status: proposed
reviewed_through: 2026-09-19
---

# Native coordination comparison v0

This contract defines the first bounded "change one condition and compare"
interaction for native Waltzman delivery.

## Purpose

After a user has explicitly approved the shared native coordination mechanics
and completed one native run, the Builder may create one comparison run without
discarding or rewriting the original.

The v0 comparison changes exactly one supported initial condition:

```text
gate.required_approvals
```

No executable rule, information record, actor authorization, resource state,
event, command, or prior trace is edited in place.

## Baseline retention

When a fresh run succeeds, the Builder retains:

- the exact initial authoring bundle used for that run;
- the exact approved causal model;
- the execution mode;
- the returned trace;
- the returned Living Scene HTML; and
- the service trace id.

Starting a comparison does not clear those objects.

A comparison failure also leaves the baseline visible.

## Supported intervention

The comparison request sends the retained baseline bundle and requested threshold to the service. The service clones and validates the baseline, applies the one supported mutation, recompiles the shared causal model against the resulting comparison bundle, and only then executes it.

It may replace only:

```text
entities.<gate>.components.gate.required_approvals
```

The new threshold must:

- be an integer;
- be at least 1;
- be no greater than the number of represented informed report recipients; and
- differ from the retained baseline threshold.

The service counts an informed recipient only through a represented delivery whose `recipient_id` names a represented member and whose `info_id` names represented information. The retained baseline threshold must itself be within that supported informed-recipient count; malformed or impossible baselines are refused before the comparison run.

The one-shot authoring family requires at least two distinct report recipients
so every generated first-release world has at least one alternate valid
threshold.

## Mechanics authority

The comparison reuses the exact causal model retained with the approved
baseline.

It does not call mechanics generation and does not create new executable law.

The service still applies the ordinary native-coordination run boundary:

- the modified authoring bundle must validate;
- the causal model must compile against it;
- the causal model must exactly equal the reviewed shared coordination model;
- execution mode is `native_coordination`; and
- policy is deterministic scripted execution.

## Fresh execution

A comparison is a second fresh Engine run. It is not:

- an edit of baseline commands or events;
- a fork that rewrites retained history;
- a post-hoc change to a Living Scene frame; or
- an analytic prediction of what would have happened.

The request log contains the complete comparison bundle, making the changed
initial condition inspectable.

## Presentation

The Builder keeps the baseline Living Scene visible and adds:

- baseline threshold and result summary;
- comparison threshold and result summary; and
- the comparison Living Scene.

The two traces remain separately inspectable in Full logs.

The UI may state the represented difference in outcomes. It may not claim that
the threshold is a real-world cause beyond the installed mechanics governing
these two represented runs.

## Limits

The v0 comparison surface does not yet support arbitrary state editing,
multi-variable experiments, probabilistic sweeps, sensitivity analysis,
automatic causal identification, or provider-generated intervention advice.

Those additions require separate contracts rather than extending this control
implicitly.

## Verification

Focused verification:

```bash
python -m pytest \\
  tests/test_native_coordination_comparison.py \\
  tests/test_world_builder_service.py \\
  tests/test_world_authoring_builder.py
```

The comparison also depends on the native coordination runner and therefore
inherits the Linux verification gate from
`native-coordination-diagnostics-v0.md`.
