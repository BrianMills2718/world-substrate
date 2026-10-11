---
description: Keep semantic world description separate from the causal mechanics that decide consequences.
---

# Decision 003: Separate semantic description from causal mechanics

Governs: RULE-ATOMIC-COMMIT-OR-REFUSAL, RULE-WRITE-SCOPE, RULE-CHECKS-ARE-READ-ONLY, RULE-INFORMATION-IS-NOT-CAUSE

**Status:** accepted  
**Date:** 2026-09-02  
**Related:** [Decision 001](001-project-scope.md), [Decision 002](002-observability-and-replay.md)

## Context

World Substrate needs a vocabulary broad enough for agents to describe varied worlds without treating every linguistic predicate as an executable action. It also needs a disciplined way to extend mechanics without defining the entire universe up front or allowing prose to acquire accidental causal force.

Linguistic Core is therefore more than provenance vocabulary, but it is not a physics engine.

## Decision

World Substrate uses Linguistic Core as the semantic interface for identifying predicate senses, participant roles, and semantic relationships. Installed mechanics supply persistence, applicability, authority, quantities, effects, scheduling, invariants, and commit behavior.

A semantic binding classifies an occurrence for mechanical purposes as one of the following provisional roles:

- primitive intentional action;
- autonomous or environmental process;
- state relation;
- composite event;
- analytic or emergent pattern;
- plan, intention, or declaration; or
- institutionally enforced transition.

This is a binding classification over donor vocabulary, not a replacement upper ontology. The classification must be revised if donor analysis supplies a better existing distinction.

Only a represented bearer with independent causal force may directly produce canonical writes. Before making a named phenomenon a mechanic, apply this test:

> If lower-level events were held fixed and the named phenomenon were removed, would future state transitions or affordances change?

If not, the phenomenon is normally a derived description. It must not duplicate the effects of the events it summarizes.

Ordinary exchange is initially derived from independently attempted `give` transitions. One participant may give and the other may renege. An installed escrow or other enforcing institution can instead acquire causal force and couple transfers.

The architecture distinguishes four layers:

1. substrate physics and autonomous processes;
2. installed institutions;
3. resident-agent cognition; and
4. derived analytic interpretation.

Agent memory, beliefs, uncertainty, planning, and private reasoning remain owned by resident agents unless a selected world deliberately installs an explicit state representation that a mechanic reads. Analysis never writes canonical simulation state.

## Mechanics authoring boundary

The first extensibility experiment is pre-run and agent-assisted:

1. inspect the desired semantic world;
2. identify a missing bounded mechanic;
3. author a reviewable mechanic package;
4. validate its authority, effects, dependencies, interactions, and limitations;
5. install and freeze a mechanics profile; and
6. run the simulation under that profile.

A mechanics agent may generate declarative mechanics or executable source offline. Scenario/content authoring may only instantiate or configure installed mechanics. Runtime invention or revision of underlying world laws, including retroactive correction and branching semantics, is deferred.

## Consequences

- A Linguistic Core predicate never implies an implemented effect.
- A composite or analytic event is detachable from execution unless a causal bearer is represented.
- Mechanics and institutions propose effects; the enclosing transition owns the causally coupled commit.
- Authoring validation can prove declared enforcement coverage, not that the author remembered every consequential dependency.
- Causal closure is treated as an interaction and dependency assay with explicit residual risk.
