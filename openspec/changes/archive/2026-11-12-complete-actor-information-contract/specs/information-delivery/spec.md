## ADDED Requirements

### Requirement: Complete actor-input boundary (target, unbuilt)

Every actor-policy input SHALL be derived from that actor's declared initial knowledge, authorized observations or actor-owned inferences. The boundary SHALL cover perception, briefs, world summaries, recent events, memory/recall and their compression, restored history, offered actions and labels, confirmations/refusals, tools and actor-facing UI. Privileged world facts, another actor's private state and analyst hypotheses SHALL NOT enter through any of those surfaces merely because they exist in canonical state. Hidden-state differences SHALL NOT change actor-visible input, identifiers, counts, ordering or action descriptions until a declared observation, action result or actor-owned inference makes a difference. This is a modeled information-flow target, not a claim of infrastructure side-channel protection or delivered universal read enforcement.

Source: Brian's explicit documentation goal, 2026-11-12; inferred by agent from the complete actor-information contract and single-concern scenario in docs/model/modeling-choices.md. Documentation adopted only; runtime behavior remains unbuilt.

#### Scenario: Hidden state cannot leak through another ingress

- **WHEN** two worlds differ only in facts inaccessible to Mara and neither emits a new authorized observation or action result
- **THEN** Mara receives the same authorized input material and offered descriptions across perception, brief, summary, recent events, restored memory, action labels, tools and actor-facing UI
- **AND** hidden facts are not revealed through identifiers, counts, ordering or error text

#### Scenario: An actor infers without receiving hidden truth

- **WHEN** Mara reasons from an authorized report and her own profile and memory
- **THEN** her policy may form a belief or inference that differs from canonical truth or another actor's interpretation
- **AND** memory and later summaries distinguish supplied evidence from actor-owned inference rather than upgrading a claim to an objective fact

#### Scenario: Consequence validation does not reveal every blocker

- **WHEN** an actor attempts an action whose internal precondition depends on hidden state
- **THEN** installed mechanics may read that state and validate the attempt
- **AND** the actor receives only the result and explanation authorized by the represented interface while the restricted trace retains the internal blocker
- **AND** candidate-action descriptions do not reveal hidden values before the attempt

#### Scenario: Analyst access does not become actor access

- **WHEN** an analyst inspects canonical history, a full replay, model diagnostics or another actor's memory
- **THEN** those privileged surfaces remain separate from actor-controlled UI, tools, retrieval and policy input
- **AND** a human-controlled policy receives the same authorized projection as a model-controlled policy for the same actor role

#### Scenario: A reviewer reconstructs the actual policy input

- **WHEN** an authorized reviewer inspects an ordinary or failed actor call
- **THEN** the retained record includes the assembled prompt/context, tool inputs and results, model/configuration identity and memory transformations actually used
- **AND** supplied facts link to declared initial knowledge or an authorized exposure while actor-owned inferences remain identified as such
- **AND** this privileged record is not automatically available to simulated actors

### Requirement: Exposure-time context and idempotent delivery (target, unbuilt)

An uncertain exposure SHALL have a durable recipient-specific identity and captured opportunity-time content, observer/channel inputs, source revision/time and model context. Delivery retries or continuation SHALL use that captured context and existing disposition rather than redraw or substitute later conditions. Interpretation and choice SHALL remain actor-owned. This target does not change the v0 Current limits requirement or claim probabilistic delivery is implemented.

Source: Brian's explicit documentation goal, 2026-11-12; inferred by agent from Q84 in docs/plans/estimate_rules.md and docs/model/modeling-choices.md. Documentation adopted only; runtime behavior remains unbuilt.

#### Scenario: Retry preserves the earlier opportunity

- **WHEN** a delivery attempt is retried after the observer moves or conditions change
- **THEN** it resumes the same exposure identity and captured opportunity-time conditions without a new detection draw
- **AND** a new opportunity exists only if the authored channel rule emits one
- **AND** a late backend result cannot overwrite a terminal exposure disposition

#### Scenario: Delivery failure preserves the source and secrecy

- **WHEN** an exposure backend is unavailable after its source event committed
- **THEN** the source event remains committed and the declared delivery failure/fallback disposition is retained
- **AND** the actor receives neither privileged truth nor a notice exposing a hidden suppressed opportunity
- **AND** continuation restores that actor's authorized memory and unresolved exposure identities without importing another actor's history
