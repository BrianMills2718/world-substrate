---
description: Deliver Waltzman natively on the World Substrate engine and converge away from the donor.
---

# Decision 005: Native Waltzman delivery and donor convergence

Governs: RULE-APPROVAL-BEFORE-RUN, scripts/world_builder_service.py

**Status:** accepted
**Date:** 2026-09-18
**Related:** [Decision 001](001-project-scope.md), [Decision 002](002-observability-and-replay.md), [Decision 003](003-semantic-mechanical-boundary.md), [Decision 004](004-product-and-adoption-strategy.md)

## Context

The promoted Waltzman stakeholder surface proved that natural-language authoring, fresh execution, and living inspection are worth presenting as one product experience. It reached that result quickly by reusing a Cybernetic Influence V3 donor path while World Substrate continued to mature its own Builder, constrained mechanics compiler, Engine, replay, scene bootstrap, and Living Scene renderer.

That shortcut was useful for promotion, but it is not the desired permanent product architecture. World Substrate now has enough native pieces that the next product question is whether they can form one coherent end-to-end path for Waltzman-class coordination worlds without a second simulator owning consequences.

The only active product-driving user/vertical is Waltzman. That makes a Waltzman-first convergence more valuable than continuing two general simulation platforms in parallel.

## Decision

World Substrate becomes the native product substrate for the next Waltzman release.

The active product path is:

```text
one-shot text or dialogue
  -> versioned editable World Substrate draft
  -> reusable and/or bounded generated mechanics
  -> validation + human-readable review + approval
  -> World Substrate Engine commit/refusal
  -> retained canonical history
  -> automatic generic living UI
  -> Waltzman / Cybernetic-inspired inspection and analysis
```

The first release may support a bounded family of small coordination worlds rather than arbitrary simulation. It may use reusable reviewed coordination mechanics and generic/procedural presentation fallbacks. It does not need bespoke generated artwork or bespoke UI code for every world.

One-shot text authoring is sufficient for the first native release. Conversational refinement should edit the same versioned draft and may follow once the one-shot loop is dependable.

Cybernetic Influence remains a donor and temporary promoted-demo implementation lineage, not a required runtime dependency for native World Substrate. Selected Cybernetic distinctions may be promoted only where the Waltzman vertical needs them and only behind World Substrate authority boundaries. Execution-relevant distinctions such as information access, permissions, resource constraints, delays, or commitments belong in represented world state/mechanics when adopted. Post-run views such as organization groupings, information-flow summaries, intervention comparisons, or macro/micro drill-down remain read-only analysis unless a world explicitly represents them.

The existing donor-backed `/waltzman/` experience remains a regression/fallback surface while the native path is built. It must never silently substitute a retained/reference run for a failed fresh run.

## First native stopping rule

Ship the native slice when a visitor can:

1. describe a new supported coordination situation;
2. understand the system's inferred structure, assumptions, and executable rules;
3. approve and run it through the World Substrate Engine;
4. receive an automatic UI without a hand-authored scene file;
5. inspect an important result, including the actual failed/satisfied rule checks and relevant information visibility; and
6. change one supported condition and compare another run without losing the original.

Rough generic art, a bounded world vocabulary, and one-shot creation before full dialogue are acceptable. Silent missing rules, competing world authorities, uncontrolled provider spend, or reference evidence presented as a fresh run are not.

## Active uncertainties

This decision sets direction; it does not claim that the complete native path is already implemented.

- **Coordination mechanics expressiveness:** generic authoring does not yet prove it can generate Waltzman's richer information/activity/institution mechanics. The smallest acceptable fallback is a reviewed reusable coordination-mechanics package with generated parameters, not model narration of consequences.
- **Automatic-view integration:** zero-review Automatic replays exist across several worlds, while Waltzman's polished Living Scene uses a richer composed profile. The required adapter or mapping should be measured from one actual native coordination run before redesigning either renderer.
- **Intent completeness:** compiler acceptance proves structural/executable validity, not that a generated world captured every important condition from the user's description. Review must distinguish supplied requirements, inferred assumptions, implemented rules, and unsupported requests.
- **Observation authority:** actors must not receive observer-only or undelivered information. Cybernetic-style information/permission distinctions should be promoted only when they materially constrain Waltzman behavior.
- **Analysis claims:** Waltzman trust/risk/readiness or other higher-level summaries must state their definitions and evidence limits and may not rewrite canonical history.
- **Deployment:** the existing promoted donor path still has operational value. Native convergence should not create a public outage or force a hosting migration onto the critical path unless continuity requires it.

## Expected failure modes and response

- **Template masquerading as generation:** materially different prompts produce the same world with renamed actors. Response: require consequential variation in represented state, constraints, routes, goals, or mechanic parameters; state the supported family honestly.
- **Plausible but incomplete generated law:** a requested prerequisite or constraint is omitted. Response: expose requirement-to-rule coverage and refuse or visibly narrow unsupported intent rather than silently dropping it.
- **UI semantic overreach:** illustrative layout implies physical location, ownership, or causality not present in world state. Response: keep presentation downstream and label generic visualization primitives appropriately.
- **Fluent explanation outruns evidence:** a message is said to have caused a decision only because it preceded it. Response: show retained information context separately from mechanic-declared hard causal ancestry.
- **Duplicate paid work:** retries, refreshes, or double submission launch multiple provider calls/runs. Response: idempotent run creation, bounded retries, server-side quotas/budgets, and recoverable request identity.
- **Scope expansion:** work drifts into arbitrary-world support, perfect assets, a repo merger, generalized cognition, or a universal scheduler before the native Waltzman vertical works. Response: add capabilities only when an observed Waltzman failure blocks the agreed user flow.

## Consequences

- The immediate frontier moves from donor-hosting hardening to a native World Substrate Waltzman vertical while preserving the donor experience as regression/fallback.
- World Substrate remains the sole canonical consequence authority for the native path.
- Cybernetic repositories remain valuable sources of semantics, analysis, and UX patterns; their runtimes are not automatically adopted.
- Generic automatic UI is a product requirement; bespoke generated UI is not.
- Evaluation is feature acceptance around the promised flow, not a broad benchmark program.
- Jev/System-One remains available infrastructure for bounded intermediate estimates but is not on the critical path for this release.