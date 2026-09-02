# Decision 002: Observability is required; exact replay is not

**Status:** accepted  
**Date:** 2026-09-02  
**Supersedes:** project-wide interpretations of replay in planning and architecture; does not supersede M1 evidence or `core-v0`

## Context

M1 deliberately used deterministic rules, pinned inputs, state hashes, and fresh-process replay to establish a narrow freshwater vertical. That evidence is valid. The project has since clarified that exact reproducibility is not the product goal and must not constrain every later representation.

A persistent world must remain inspectable even when resident-agent decisions, stochastic mechanics, external inputs, or selected subsystem implementations are not exactly reproducible.

## Decision

Observability is a core requirement. A transition trace must make it possible to inspect, as applicable:

- what a causal bearer observed or read;
- what it attempted or what process fired;
- the Linguistic Core sense and roles bound to the attempt;
- the installed mechanic and authority selected;
- applicability, authorization, resource, and invariant checks;
- proposed and committed state-path changes;
- refusal, failure, and unsupported-interaction reasons; and
- the resulting persistent state identity or snapshot.

Exact replay, deterministic execution, bit-for-bit reproduction, and reconstruction of the whole world from an event log are not project requirements or universal promotion gates.

Mechanics may be deterministic, stochastic, empirical, scripted, externally supplied, or bounded model-mediated when their representation, authority, omissions, and observability are explicit. Policies and unbounded prose still may not mutate canonical state directly.

M1 replay remains:

- an implemented property of `core-v0`;
- evidence supporting the M1 promotion claim; and
- an optional debugging technique where economical.

It is not an architectural mandate for future contracts.

## Consequences

- Future milestones are promoted by inspectable causal behavior and goal-relative evidence, not exact replay.
- Snapshots and stable identifiers may be retained without adopting event sourcing.
- Randomness need not be replayable, though its use and effects must be observable at the fidelity required by the world.
- Existing M1 replay code, tests, receipts, and historical wording remain evidence of what M1 implemented.
