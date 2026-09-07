---
schema_version: project-wiki/v1
type: ProjectWiki
role: derived-navigation
status: active
reviewed_through: 2026-09-07
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

The intended result is a wide compositional space rather than an enumerated list of natural-language commands or one bespoke mechanic per predicate. Persistent objects participate in multiple mechanics because those mechanics act on shared typed state under declared authority.

## Start here

| Need | Read next |
| --- | --- |
| Current direction or next work | [Roadmap](../../roadmap/README.md) |
| Enduring system boundaries | [Architecture](../architecture.md) |
| Implemented M1 interface | [Core contract v0](../contracts/core-v0.md) |
| Semantic binding contract | [Semantic–mechanical binding v0](../contracts/semantic-mechanical-binding-v0.md) |
| Mechanics-agent package | [Mechanic profile v0](../contracts/mechanic-profile-v0.md) |
| Commit boundary | [Transition envelope v0](../contracts/transition-envelope-v0.md) |
| Optional read-scope verification design | [Read-scope enforcement v0](../contracts/read-scope-enforcement-v0.md) |
| Product evidence goals | [Decision 002](../decisions/002-observability-and-replay.md) |
| Semantic and causal boundary | [Decision 003](../decisions/003-semantic-mechanical-boundary.md) |
| Why neighboring projects are not the authority | [Source dispositions](../source-dispositions.md) |
| Reference-world expectations | [Reference worlds](../../reference_worlds/README.md) |
| The contested two-agent world | [Kitchen audit](../audits/kitchen-contested-world.md) |
| Rendered runs a person can read | `evidence/renders/` |

## Concepts and terminology

- **Canonical state:** the only material world truth. Prompts, narratives, UI views, resident-agent private state, and analysis are not competing authorities.
- **Semantic binding:** a Linguistic Core predicate sense, participant-role binding, causal classification, and—when causal—a binding to an installed mechanic.
- **Causal bearer:** the represented agent, process, disposition, institution, or exogenous input whose existence changes what the world can do next.
- **Mechanic:** an installed rule or process with declared applicability, local reads/writes, effects, invariants, limits, and trace behavior.
- **Mechanic profile:** the validated set of mechanics and bindings frozen for a simulation run.
- **Composite event:** a description of multiple committed events that does not reapply their effects.
- **Affordance:** one installed mechanic currently available to one actor, derived from canonical state.
- **Observation:** an actor-authorized, intentionally lossy projection of canonical state.
- **Declared enforcement coverage:** whether every consequence the mechanic author declared is bound to an enforceable interface.
- **Causal-closure assay:** fallible dependency and interaction review that searches for consequential state the author failed to declare.
- **Reference world:** a bounded end-to-end world that exercises shared substrate contracts without owning a private engine.
- **Terminal condition:** a world-specific predicate over canonical state that tells a runner represented work is complete; it should be derived when existing state already says enough.

## Four causal layers

1. Substrate physics and autonomous processes.
2. Installed institutions.
3. Resident-agent cognition.
4. Derived analytic interpretation.

Agent memory, beliefs, uncertainty, planning, and private reasoning ordinarily stay inside the resident-agent runtime. Analysis can classify exchange, trust, cooperation, or collective competence without causing those patterns again. Either layer may become mechanically explicit only when a selected world represents a causal bearer and binds it to an installed mechanic.

## Where this actually stands

The substrate prototype is complete and the flagship phase has produced its first human-facing artifact. The selected world is the kitchen: two cooks with different orders, one knife, two burners, and zero ingredient slack. Three fresh same-model/prompt services reproduced the key sequence — Bo completes at t9, releases the knife for Ama at t10, Ama takes it at t11, and both orders are filled at the t17 world terminal.

`evidence/renders/kitchen-spatial-replay-v1.html` is the primary human-facing replay. It renders one retained v3 trace as an illustrative top-down kitchen: cooks move among prep, burner and plating stations while item preparation, knife ownership, order progress and short reasoning bubbles update from the recorded service. The geometry is presentation-only and cannot mutate or replay world effects. `kitchen-flagship-v1.html` remains the denser trace-oriented timeline. The next unresolved boundary is whether/how to show or publish the graphical replay, which remains a human decision. See the [roadmap's active slice](../../roadmap/README.md#vertical-slices-and-current-work).

## What exists now?

- M1 is promoted through registered fill, heat, unheat, pour, drink, take, and give rules plus deterministic processes. Discovery, observation, causal events, atomic rejection, persistent cross-system identity, and exact pinned replay work in `core-v0`.
- Six of seven M1 action kinds have reviewed Linguistic Core bindings; `unheat` remains upstream-owned because the pinned ontology extraction contains no appropriate sense.
- `give` plus reciprocal history can be classified as derived exchange without a second transfer (M2).
- Declared **write** scopes are enforced. Rule-facing read-only hooks execute on detached state, and mechanics cannot own revision or causal history. Declared **read** scopes are recorded and remain unenforced at runtime; an optional verification design exists.
- Two adjacent mechanics were authored offline and exercised through the mechanic-profile workflow (M3, M4), and three interaction assays attack different causal-closure failure bases.
- An LLM policy has driven the ordinary affordance seam (M5).
- A materially different workshop world reuses the substrate contracts while reusing none of Castaway's mechanics (M6).
- A model authored mechanics it was not handed, including relational mechanics that affect a second entity (M7/M7b). The dominant observed failure was triviality rather than uncontrolled authority.
- Ownership references and authored field types are checked rather than left as conventions.
- The kitchen is the third world and the first one built to be watched. Its completion condition is derived from its orders, and new contested-run outputs record whether the world reached that terminal state.

## Current frontier

All six prototype success criteria are met. The immediate question is now narrow and empirical: does the kitchen's unprompted bottleneck handover recur under the same model and prompt, or was the retained service one unusually good sample?

Do not answer that by adding contracts or more substrate hardening. Repeat the service under the standing model-execution authority and compare completion, contention, displacement, and deliberate release behavior. The [roadmap](../../roadmap/README.md) owns the exact next action.

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

Retained evidence records what a particular revision/run established. In particular, `evidence/kitchen/full-service-v0.json` is intentionally historical: its trailing turns are the evidence that motivated the terminal-state fix, not the behavior of the current runner.

## Accepted authorities and decisions

- [Roadmap](../../roadmap/README.md) owns project direction and active work.
- [Architecture](../architecture.md) owns durable system boundaries.
- Accepted decisions own human-set doctrine.
- `core-v0` owns the implemented M1 seam.
- Proposed/partial contracts own only the status they explicitly claim.
- Code and tests own implemented behavior.
- Revision-bound evidence owns observed claims.
- The kitchen, rendered reasoning-vs-world view, and scarce-resource coordination are the current reversible flagship choices.

## Working context

Castaway remains the adopted M1 implementation and evidence donor. The workshop is the cross-domain reuse proof. The kitchen is the flagship experiment. Linguistic Core is the semantic interface. Cybernetic Influence, Agent Ecology, Data Contracts, and Collective Competence remain bounded design or failure-analysis donors rather than competing authorities.

## Needs resolution

- whether the kitchen's handover and turn-taking replicate under the same policy conditions;
- the upstream `unheat` semantic sense;
- progress toward leaving enforced thresholds such as cooling to a safe temperature;
- whether/when optional read-scope verification is worth its measured overhead;
- deployment/publication, which remains an explicit human authority boundary.

## Human-reviewable artifacts

- `evidence/renders/kitchen-spatial-replay-v1.html`: graphical top-down replay of a fresh terminal replication.
- `evidence/renders/kitchen-flagship-v1.html`: denser trace-oriented timeline of that retained service.
- `evidence/kitchen/full-service-replication-v1-summary.json`: hashes, method, costs and 3/3 replication result.
- `evidence/kitchen/full-service-replication-v1-run{1,2,3}.json`: raw retained v3 traces.
- `evidence/renders/kitchen-full-service.html`: intentionally historical pre-terminal run that exposed the trailing-turn defect.
- `docs/audits/kitchen-contested-world.md`: why the kitchen exists, what replicated, and the execution caveat.
- M1 freshwater traces and replay receipt: the promoted substrate baseline.
- M3–M7b audits and evidence: mechanics-authoring, interaction, policy, reuse, and authoring-rate findings.

## Roadmap

Use [the canonical roadmap](../../roadmap/README.md) for the active experiment, authority boundaries, claim limitations, and exact next action.
