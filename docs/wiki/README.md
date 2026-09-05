---
schema_version: project-wiki/v1
type: ProjectWiki
role: derived-navigation
status: active
reviewed_through: 2026-09-02
authority_refs:
  - ../../README.md
  - ../../roadmap/README.md
  - ../architecture.md
  - ../decisions/001-project-scope.md
  - ../decisions/002-observability-and-replay.md
  - ../decisions/003-semantic-mechanical-boundary.md
---

# World Substrate project wiki

This is the single orientation surface for the project. It explains the current synthesis and routes readers to native authorities; it does not replace them.

## What this project is

World Substrate is a persistent, observable simulation substrate. LLM or human policies express semantically grounded intents. Linguistic Core identifies senses and participant roles. Installed mechanics with explicit local authority determine and commit canonical consequences.

The intended result is a wide compositional space rather than an enumerated list of natural-language commands or one bespoke mechanic per predicate. A persistent vessel can participate in liquid, heat, containment, material, carrying, and rights mechanics because those mechanics act on the same object under declared scopes.

## Start here

| Need | Read next |
| --- | --- |
| Current direction or next work | [Roadmap](../../roadmap/README.md) |
| Enduring system boundaries | [Architecture](../architecture.md) |
| Implemented M1 interface | [Core contract v0](../contracts/core-v0.md) |
| Proposed semantic binding | [Semantic–mechanical binding v0](../contracts/semantic-mechanical-binding-v0.md) |
| Proposed mechanics-agent package | [Mechanic profile v0](../contracts/mechanic-profile-v0.md) |
| Proposed commit boundary | [Transition envelope v0](../contracts/transition-envelope-v0.md) |
| Proposed read-scope enforcement | [Read-scope enforcement v0](../contracts/read-scope-enforcement-v0.md) |
| Product evidence goals | [Decision 002](../decisions/002-observability-and-replay.md) |
| Semantic and causal boundary | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) |
| Why neighboring projects are not the authority | [Source dispositions](../source-dispositions.md) |
| Consolidated research findings | [Research synthesis](../research/synthesis.md) |
| Full discussion lineage and disposition | [Discussion traceability](../research/discussion-traceability.md) |
| Reference-world expectations | [Reference worlds](../../reference_worlds/README.md) |
| The contested two-agent world | [Kitchen audit](../audits/kitchen-contested-world.md) |
| Rendered runs a person can read | `evidence/renders/` |

## Concepts and terminology

- **Canonical state:** the only material world truth. Prompts, narratives, UI views, resident-agent private state, and analysis are not competing authorities.
- **Semantic binding:** a Linguistic Core predicate sense, participant-role binding, causal classification, and—when causal—a binding to an installed mechanic.
- **Causal bearer:** the represented agent, process, disposition, institution, or exogenous input whose existence changes what the world can do next.
- **Mechanic:** an installed rule or process with declared applicability, local reads/writes, proposed effects, invariants, limits, and trace behavior.
- **Mechanic profile:** the validated set of mechanics and bindings frozen for a simulation run.
- **Primitive action:** an independently attempted action, such as one agent giving an object.
- **Composite event:** a description of multiple events, such as two reciprocal gives classified as exchange. It normally performs no additional state change.
- **Installed institution:** a represented causal bearer, such as escrow, whose enforced rules alter affordances or transitions.
- **Affordance:** one installed mechanic currently available to one actor, derived from canonical state. It establishes neither broad reachability nor reliable competency.
- **Observation:** an actor-authorized, intentionally lossy projection of canonical state.
- **Declared enforcement coverage:** whether every consequence the mechanic author declared is bound to an enforceable guard, transition, or process.
- **Causal-closure assay:** fallible dependency and interaction review that searches for consequential state the author failed to declare.
- **Reference world:** a bounded end-to-end world that exercises shared substrate contracts without owning a private engine.

## Four causal layers

1. Substrate physics and autonomous processes.
2. Installed institutions.
3. Resident-agent cognition.
4. Derived analytic interpretation.

Agent memory, beliefs, uncertainty, planning, and private reasoning ordinarily stay inside the resident-agent runtime. Analysis can classify exchange, trust, cooperation, or collective competence without causing those patterns again. Either layer may become mechanically explicit only when a selected world represents a causal bearer and binds it to an installed mechanic.

## Where this actually stands

The substrate works, and the part that matters has started.
Every contract the prototype set out to test holds. A third world — the kitchen
— now runs a complete two-agent service, which is the first thing here a person
could be shown, though not yet without narration. See
[the roadmap's active slice](../../roadmap/README.md#vertical-slices-and-current-work)
for where it stands and the next two increments, and
[the kitchen audit](../audits/kitchen-contested-world.md) for what the run does.
The inventory below is what exists, not what is left.

## What exists now?

- M1 is promoted through registered fill, heat, unheat, pour, drink, take, and give rules plus deterministic processes. Discovery, observation, causal events, atomic rejection, semantic donor comparison, persistent cross-system vessel identity, and exact 22-command replay all work in the implemented `core-v0` path.
- `give` is bound to a pinned Linguistic Core sense, and exchange is a derived read-only classification that performs no second transfer (M2).
- Declared **write** scopes are enforced by the engine. Declared **read** scopes are recorded on every event and are not enforced at runtime.
- Two adjacent mechanics have been authored offline, installed through the mechanic-profile contract, frozen into a profile, and exercised (M3, M4): overheat damage and vessel-failure spill.
- Three interaction assays exist on three different bases — declarations, differential behaviour, and conserved-quantity accounting. Each has a stated blind spot; no single basis and no pair is sufficient.
- Contract status is mixed rather than binary: `core-v0` is implemented; mechanic-profile and transition-envelope are **partially** implemented; semantic-mechanical-binding remains a target. Each contract states its own current status.
- Exact replay remains valid M1 evidence but is not a future product requirement.
- Linguistic Core is the selected semantic interface. Its coverage of persistent state, qualities, quantities, rights, and institutional relations still requires a donor audit, and 6 of 7 M1 action kinds still have no binding.
- An LLM policy has driven the world through the ordinary affordance seam (M5), and a second reference world — a workshop of discrete parts and tools sharing no content with Castaway — reuses the transition kernel, events, replay, installer, assays and policy seam (M6).
- A model has authored mechanics it was not handed, with the checks withheld from it (M7): 9 of 10 installed, 0 write-scope violations, and the dominant failure mode was triviality rather than danger.
- Ownership references are checked rather than conventional, closing the one defect class M7 found that nothing could catch.

## Current frontier

All six prototype success criteria are met, and both halves of the central
hypothesis have been probed: whether bad mechanics get caught (M3, M4) and
whether an agent can author useful ones unaided (M7).

What remains is incremental hardening rather than an open question. The
roadmap's Open obligations table is the live list; the largest single item is
the three uncovered Decision 002 observability fields, which are one `core-v0`
schema change rather than six separate ones.

[The roadmap](../../roadmap/README.md) holds the exact next action. Continuing
is a scope choice, not an obligation.

## Architecture and workflow

```text
semantic intent or autonomous trigger
        |
        v
Linguistic Core sense + role binding
        |
        v
installed local mechanic -> proposed effects -> validation -> one commit/refusal
        |                                              |
        v                                              v
bounded observation                         persistent state + causal trace
                                                       |
                                                       v
                                            detachable analytic views
```

## Sources and evidence

[Source dispositions](../source-dispositions.md) classifies material donors and [references/sources.json](../../references/sources.json) pins reviewed revisions. Donors are design, implementation, or failure-analysis inputs; they are not code-adoption instructions.

## Accepted authorities and decisions

- [Roadmap](../../roadmap/README.md) owns project direction and active work.
- [Architecture](../architecture.md) owns durable system boundaries.
- Accepted decisions own human-set doctrine.
- `core-v0` owns the implemented M1 seam.
- Proposed contracts own target interfaces only.
- Code and tests own implemented behavior.
- Revision-bound evidence owns observed claims.

## Working context

Castaway remains the adopted M1 implementation and evidence donor. Linguistic Core is now the semantic interface. Cybernetic Influence, Agent Ecology, Data Contracts, and Collective Competence contribute bounded design or failure findings without becoming competing project authorities.

The immediate work reuses the existing M1 `give` path to test semantic binding, primitive versus derived causation, local authority, and observability before open-ended mechanics authoring.

## Needs resolution

- the donor coverage of state relations, qualities, quantities/units, rights, and institutions;
- the smallest mechanics representation that avoids family-specific compiler branches;
- the first bounded adjacent mechanic for an offline authoring experiment;
- conflict, precedence, revocation, and entity-replacement semantics; and
- the second reference world.

## Human-reviewable artifacts

The current outcome-bearing artifacts remain the M1 traces, replay receipt, combined [machine](../../evidence/m1/freshwater-v0.json) and [human](../../evidence/m1/freshwater-v0.md) receipts, and validated [end-to-end observation](../../evidence/m1/end-to-end-observation-v1.json).

The new decisions and proposed contracts are reviewable design artifacts, not runtime evidence.

## Roadmap

Use [the canonical roadmap](../../roadmap/README.md) for the active vertical, claim boundaries, conditional milestones, and exact next action.
