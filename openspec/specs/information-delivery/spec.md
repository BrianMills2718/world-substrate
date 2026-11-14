# information-delivery Specification

## Purpose

Represented information and its delivery to observers, kept separate from private cognition and from causal parentage.

**Information and delivery v0** (folded on 2026-11-09 from `docs/contracts/information-delivery-v0.md`, status `implemented`, reviewed through 2026-09-08, last commit `72fb4d8`):

World Substrate can represent information as canonical world state without
turning information, private cognition, or later analysis into the same causal
thing.

The implemented v0 types are `InformationState` and `DeliveryState` in
`world_substrate.information`.

## Requirements

### Requirement: Representation

An information item records:

- represented content;
- `source_id`;
- `channel_id`;
- `visibility` (`direct` or `public` in v0);
- an optional topic;
- an optional `derived_from_info_id` lineage edge; and
- whether the item is active in the represented world.

A delivery records:

- the information item;
- recipient;
- channel;
- status (`pending`, `delivered`, or `observed` are the v0 states consumed by
  the visibility seam); and
- the canonical tick at delivery when available.

These records are world facts only because a selected world chooses to
represent them. They do not imply a resident belief state.

Source: inferred by agent (information and delivery v0, applying Decision 003, accepted 2026-09-02). Same-moment reactions get a causal parent under Decision 009: Brian, 2026-10-26: "i approve"

#### Scenario: An item and its delivery are recorded as world facts

- **WHEN** a selected world represents a message and its delivery
- **THEN** the information item records its content, `source_id`, `channel_id`, `visibility` (`direct` or `public`), an optional topic, an optional `derived_from_info_id`, and whether it is active
- **AND** the delivery records the item, recipient, channel, status (`pending`, `delivered` or `observed`) and, when available, the canonical tick at delivery

#### Scenario: A record is not a belief

- **WHEN** an information item or delivery exists in canonical state
- **THEN** it is a world fact only because the world chose to represent it, and it implies no belief state in any resident

### Requirement: Observation rule

For actor-local observation:

1. a represented source can inspect its own information item;
2. a direct recipient does not receive the item or its delivery record until
   the delivery is `delivered` or `observed`;
3. a public active item is visible to local actors; and
4. unrelated actors do not gain a direct item merely because it exists in
   canonical state.

The Waltzman acceptance fixture proves asymmetric delivery: a system briefing
can be delivered to Mara without Ari seeing it, and a later represented Mara →
Ari message becomes visible to Ari only after the communication mechanic
commits.

Source: inferred by agent (information and delivery v0, applying Decision 003, accepted 2026-09-02). Same-moment reactions get a causal parent under Decision 009: Brian, 2026-10-26: "i approve"

#### Scenario: A direct recipient waits for delivery

- **WHEN** a direct item has a delivery to Mara with status `pending`
- **THEN** Mara's observation contains neither the item nor its delivery record
- **AND** once the delivery is `delivered` or `observed`, both appear in her observation

#### Scenario: A source and a public item

- **WHEN** an actor is the represented source of an item, or the item is public and active
- **THEN** the source can inspect its own item even before delivery, and every local actor can see the public active item

#### Scenario: Unrelated actors see nothing

- **WHEN** a direct item exists in canonical state and an actor is neither its source nor a recipient whose delivery is `delivered` or `observed`
- **THEN** that actor's observation does not contain the item or the delivery

#### Scenario: The Waltzman fixture delivers asymmetrically

- **WHEN** a system briefing is delivered to Mara and, later, Mara sends a represented message to Ari
- **THEN** Mara sees the briefing and its delivery record while Ari does not
- **AND** Ari sees Mara's message and its delivery only after the communication mechanic commits,, and Selene does not see them

### Requirement: Causality rule

Information lineage and hard causal ancestry are distinct.

Engine events may retain `information_context` derived from the actor's bounded
observation. That means the information was represented in the actor's context;
it does **not** claim the information mechanically caused the action.

A rule may opt into `DeclaresCausalParents` or
`DeclaresProcessCausalParents` and name retained event IDs only when that rule
mechanically consumes or otherwise explicitly justifies those parents. The
Engine stores those IDs as `causal_parent_event_ids` separately from
`information_context`.

Temporal precedence and prompt inclusion are insufficient to promote a message
to hard ancestry.

Source: inferred by agent (information and delivery v0, applying Decision 003, accepted 2026-09-02). Same-moment reactions get a causal parent under Decision 009: Brian, 2026-10-26: "i approve"

#### Scenario: Information context is not causal parentage

- **WHEN** an engine event retains `information_context` from the actor's bounded observation
- **THEN** the context means only that the information was represented in the actor's context
- **AND** the event carries no `causal_parent_event_ids` unless its rule declared them (the Waltzman start-meeting event lists three messages in `information_context` and has no `causal_parent_event_ids`)

#### Scenario: A rule declares its causal parents

- **WHEN** a rule opts into `DeclaresCausalParents` or `DeclaresProcessCausalParents` and names retained event IDs because it mechanically consumes them
- **THEN** the Engine stores those IDs as `causal_parent_event_ids`, separately from `information_context`

#### Scenario: Timing and prompt inclusion are not enough

- **WHEN** a message came before an action in time or was included in the actor's prompt
- **THEN** that alone does not make the message a hard causal ancestor of the action

### Requirement: Current limits

v0 does not generically model channel latency, probabilistic delivery,
corruption, belief revision, deception detection, audience groups, information
expiration, or arbitrary provenance graphs. Extend the contract only when a
real world needs those distinctions.

Source: inferred by agent (information and delivery v0, applying Decision 003, accepted 2026-09-02). Same-moment reactions get a causal parent under Decision 009: Brian, 2026-10-26: "i approve"

#### Scenario: A world needs more than v0 models

- **WHEN** a world needs channel latency, probabilistic delivery, corruption, belief revision, deception detection, audience groups, information expiration or arbitrary provenance graphs
- **THEN** v0 does not model them generically
- **AND** the contract is extended only when a real world needs those distinctions

### Requirement: Same-moment reactions cite their cause (current code)

A same-moment knock-on reaction SHALL cite as its hard causal parent the latest event of the same moment it reacts to (`Engine._settle`, `src/world_substrate/engine.py:964`), and each of its steps SHALL name the step that caused it (`reaction_steps`: `it`, `caused_by`, `via`). New runs have no cap on a moment's reactions: each (process, entity) pair fires at most once per moment, so every chain ends. A knock-on step that a failed check stopped SHALL be recorded with its blocker (`blocked_reactions`: the rule, the thing, the step it came after, the failed check and its value), and nothing follows from it. A run recorded with a limit (records made before the AI judge plan's J0 ran under 32, `LEGACY_REACTION_LIMIT`, `engine.py:155`) replays under it, and a moment over that limit, or a reaction that would break a declared law, is refused whole.

Source: Decision 009, Brian, 2026-10-26: "i approve"; the cap removed by the AI judge plan's J0 (Brian, 2026-11-09: "50 things could propagate down a causal chain 100 links deep"; build approved 2026-11-10)

#### Scenario: A reaction names the event it reacts to

- **WHEN** a same-moment knock-on reaction fires
- **THEN** `Engine._settle` records as its hard causal parent the latest event of that moment that changed its entity, else the triggering event (in the glass-chain test, the fall cites the push, the break cites the fall, and the spill and crash-sound each cite the break)

#### Scenario: A knock-on step names the step that caused it

- **WHEN** one move sets off chains of knock-on effects in one moment
- **THEN** each step's record names the step that caused it (`caused_by`) and the linked things it came through (`via`), with no cap on how many steps the moment has

#### Scenario: A stopped step is recorded with its blocker

- **WHEN** a knock-on step's rule has a check that reads the changed thing and holds, and another check fails (a loaded truck with fuel 0)
- **THEN** the step does not happen, and the round's `blocked_reactions` names the rule, the thing, the step it came after, and the failed check with its value

#### Scenario: A moment needs too many reactions

- **WHEN** a run recorded under a limit (32 for runs recorded before J0) has a moment that would need more reactions than that
- **THEN** the whole moment is refused with status `reaction_limit` and the failed check "Knock-on effects settle within 32 reactions"
- **AND** the world is left as it was, with the refusal as the only event added

#### Scenario: A reaction would break a declared law

- **WHEN** a reaction would break a declared law
- **THEN** the whole moment is refused with status `law_breach`

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

### Requirement: Initial exposure and source-grounded actor inputs

Source: Brian's approved I0/I1 goal, 2026-11-12; integration-2 findings 3, 5 and 6.

An explicitly already received report SHALL compile as delivered exposure, with actual transmitter distinct from current holder and apparent source. An unspecified actual source SHALL remain unspecified. The existing build review SHALL inspect the actual assembled initial actor inputs against the original source, including private existence or values disclosed through narrator-only negative knowledge. A declared actor-information world SHALL NOT be delivered when that review is missing, unavailable, incomplete or rejects any actor or public-summary authorization. Historical pending defaults SHALL remain compatible.

#### Scenario: Received information is not awaiting a second delivery

- **WHEN** a source explicitly says one person already received a report
- **THEN** that recipient observes its delivered record at initialization without a new send action
- **AND** no belief, stance or assent follows automatically

#### Scenario: Withheld facts leak through a profile

- **WHEN** a draft tells Mara she has not seen a privately named batch that only Ari knows
- **THEN** the actual draft context is included in the source-grounded review
- **AND** a rejection, missing verdict or unavailable review prevents delivery of that candidate

### Requirement: Place-scoped perception with distinct inputs

Source: Brian's 2026-11-13 inhabited-facility request; inferred by agent for the mechanism.

A declared public entity MAY be scoped to a place. An actor SHALL perceive a place-scoped entity's declared fields only while the entity stands in, or is, the actor's current place. Unscoped declared entities remain known everywhere. When a declaration uses a place scope, the actor's observation SHALL also name the actor's place, list the declared entities physically present with it, and list reports delivered to the actor from its own declared report log regardless of place. The actor's prompt context SHALL present that observation, global knowledge (world summary and the actor's declared brief and knowledge) and any supplied retained memories as separate inputs; delivered reports and memories SHALL NOT be treated as physical perception, and place scope SHALL NOT be treated as a distance, hearing or occlusion model.

#### Scenario: A closed door blocks movement and opening it permits movement

- **GIVEN** a world with a closed directed door between two rooms
- **WHEN** an actor attempts to walk through it
- **THEN** the door's own rule refuses the attempt and the actor stays in the room
- **AND** after the actor opens the door the same attempt is accepted and changes the actor's place

#### Scenario: Observation follows place while reports and knowledge do not

- **GIVEN** an actor in another room from a place-scoped object and a report delivered to that actor
- **WHEN** the actor's context is built
- **THEN** the object's fields are absent and the delivered report is present
- **AND** global knowledge remains present and supplied memories appear only as memories

#### Scenario: Replay and a branch show the same facts

- **WHEN** a run is replayed and a saved round is branched with a different later choice
- **THEN** the replayed scene shows each person's place and each door's state as the rounds recorded them
- **AND** the branch begins from the checkpoint's facts and diverges without changing its parent
