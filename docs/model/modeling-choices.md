# Choosing models for an investigation

Reviewed 2026-11-12. This conceptual glossary complements the [engine glossary](../architecture/arc42.md#12-glossary). It describes modeling choices, not delivered capabilities or a second roadmap.

**Preserve the distinctions the investigation depends on.** Brian explicitly endorsed this principle in the November 12 discussion, including speed, money and computational scale as tradeoffs. His direction establishes heterogeneous modeling: people normally have cognition, personality and characteristics; programs can use executable code; physical processes can use dynamics. Simplifying people to prescribed behavior is a deliberate approximation. Jev can represent many kinds of behavior, not just people.

The heuristics below are recommendations inferred from that direction. They do not establish that every representation is implemented or that a learned model is faithful.

## What already exists

- [Architecture](../architecture/arc42.md), [ODD](ODD.md), [domain](DOMAIN.md) and [metamodel](METAMODEL.md) document execution and representation. A discrete substrate inventory does not establish that continuous dynamics are outside the vision.
- [AI judge decisions](../plans/ai_judge.md#decided), approved November 9, distinguish constraints, decisions and norms. Another person's choice belongs to that person.
- [Estimate rules](../plans/estimate_rules.md) is a draft, planning approved November 10. Its design defaults are agent inferences, not individually approved requirements or built capabilities.
- Cybernetic Influence V3's [ontology and machinery note](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/446fd57191614be1284655fa8970cf547783df6b/docs/research/general-purpose-simulator-ontology-and-machinery.md) separates existence from agency and describes people through goals, memories and beliefs rather than action scripts. Its [external review packet](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/446fd57191614be1284655fa8970cf547783df6b/docs/research/028-general-simulator-external-review-packet.md) discusses deterministic, stochastic, learned and external authorities. These are research inputs pinned to donor revision `446fd57191614be1284655fa8970cf547783df6b`.
- The [Waltzman lineage review](../audits/waltzman-lineage-review-2026-11-07.md) supplies historical critique. Later approved decisions govern where they differ. This guide supplies the missing connection between investigation requirements, modeling vocabulary and resource choices.

## A concrete example

A locked door involves a credential-checking program, a person who knows a password, a material barrier and an institutional policy about entry. Code checks the password. A person's policy decides whether to disclose it, using their observations, beliefs, memory and motivations. Physical mechanics determine whether damage defeats the barrier. A norm prohibits unauthorized entry; detection and enforcement can fail or involve further choices.

Replacing all four with “only Alice can enter” removes credential theft, persuasion, disobedience and forced entry by construction. No comparative run is needed to establish that loss. A study only of queue length may deliberately abstract those mechanisms away. The question determines which distinctions must survive.

## Worked application: the biosurveillance partnership

**Status:** first-principles application and implementation recommendation, November 12. Brian approved applying this guide to a concrete influence-operations scenario after PR #374. This section does not report a new run or amend the active implementation sequence.

Use the existing partnership deciding whether to activate a cross-border early-warning system by a deadline ([scenario source in ODD](ODD.md#10-the-any-scenario-pipeline-and-this-model)). That repository formulation already says concerns slow meetings and make support conditional. Those are candidate effects to investigate; putting them in the scenario as required outcomes would prejudge the result. The paper's conceptual influence hypothesis motivates this question; the choices below are our modeling recommendations, not equations supplied by the paper.

**Investigation:** under what circumstances do locally plausible communications change collective coordination, and when is delay instead a reasonable response to a genuine problem? A useful run can end in informed approval, informed refusal, unnecessary delay or pressure having no effect. Activation alone is not success, and delay alone is not evidence of manipulation.

An outcome-neutral starting description would establish the partnership, deadline, decision procedure, participants' differing responsibilities and relationships, system readiness, communication channels and available evidence. It would let groups communicate concerns without instructing recipients how to react. The analyst's hypothesis and desired comparison stay outside actor context; each actor receives only its own goals, memories and accessible observations.

### Distinctions the investigation needs

| Distinction | Concrete instance | Consequence of collapsing it |
| --- | --- | --- |
| Actual condition versus reported claim | A validation test failed; someone says it failed; someone falsely reports a failure | Cannot distinguish warranted caution from misleading communication |
| Delivery versus interpretation | Mara receives a report but doubts its source or judges it irrelevant | Receipt becomes persuasion by definition |
| Interpretation versus personal commitment | Mara accepts a narrow flaw but still supports a limited launch | Concern automatically becomes opposition |
| Personal stance versus institutional hold | Mara remains supportive while a mandatory verification hold remains active | A procedural blocker is mistaken for changed belief |
| Task completion versus problem resolution | A review finishes but identifies a remaining flaw | Waiting becomes a cure regardless of what was done |
| Individual decision versus collective result | Ari disagrees; the decision procedure may or may not require Ari's assent | A vote, veto, consensus and informal agreement become interchangeable |
| Shared source versus independent evidence | Several reports repeat one originating claim | Repetition is mistaken for corroboration |
| Legitimate disagreement versus coordinated pressure | Similar concerns arise independently or from shared direction | The model labels disagreement as manipulation before examining it |

These distinctions are necessary by construction: a model with no independent underlying condition cannot answer whether caution tracks real defects. No sample of successful runs repairs that representational omission.

### Process-level model choices

| Process | Recommended starting representation | Required boundary / approximation |
| --- | --- | --- |
| People reading, discussing and committing | Off-the-shelf cognition, normally LLM policies with distinct profiles and persistent memory | Recipient owns interpretation and choice; no omniscient briefing or rule-forced stance change |
| Routing messages and recording evidence provenance | Code for recipients, channels, timing, access and source identity | Delivery does not update support; information becomes available through represented communication, observation or inference |
| Technical readiness and validation | Explicit state and task-specific mechanics; use established dynamics only if their detail matters | A compact readiness condition may suffice if it preserves distinct defects, remedies and decision-relevant evidence; engineering-performance questions need appropriate technical detail |
| Formal decision procedure and deadline | Executable institution-specific rules | Represent actual voting/hold rules, not a universal consensus procedure; distinguish mandatory rules from breakable norms |
| Resource use and remediation | Code for allocations and elapsed work, with scenario-specific completion effects | Spending or completing a task does not by itself establish that the defect is gone |
| Bounded observation or equipment judgment | Jev or another estimator when the contextual task and alternatives are specified | Its estimate is not ground truth; persistent uncertainty and per-event variation have different lifetimes |
| Bounded choices inside an actor policy | A typed model is an optional implementation choice | Preserve that actor's information, goals and state; do not move the choice into world mechanics |
| Post-run interpretation | Analysis over the retained event and observation record | A model's explanation is not proof of a mental cause; distinguish exposure, stated reasons and committed actions |

Do not aggregate the decision makers or communicating groups in this initial question: their different information, relationships and institutional roles are the mechanism of interest. Background services and quiet intervals may be coarsened if doing so preserves delivery, deadlines and task dependencies.

### First-principles checks before choosing a run

Read the authored rules and actor-context construction against these counterexamples:

1. A recipient can receive a concern and retain support; a mandatory hold can still prevent activation.
2. A false report can influence a person without changing the actual equipment condition.
3. A repair can change equipment state without instantly changing everyone's beliefs; the result must reach them.
4. A completed review can conclude that activation should remain blocked.
5. A repeated report retains common provenance; it need not be interpreted as fresh independent evidence.

These are representational possibilities, not prescribed human responses or a new believability score. Source inspection can reject a design that forbids them. A focused execution test is justified later where it is uncertain whether the implemented boundary actually works. Existing approved comparison work retains its own scope.

### Resource choices for this scenario

Use actor activations and relevant message deliveries as the workload units, rather than polling every person on every tick. Deliberation may also be triggered by a remembered obligation, meeting or deadline; silence is not proof that cognition has no work to do. Batch only decisions that are independent at the same simulated moment, and preserve causal ordering when one person's message changes another's information.

A worked-out accounting form is **calls = authoring calls + sum of cognition calls over actor activations + interpretation calls + uncached estimate calls + adjudication calls + retries**. Do not count a call twice when a backend combines roles. Compute token or request charges using the selected backend's actual billing units; no price or latency measurement is asserted here. Trace storage includes model inputs/outputs and observations, not just committed world events. Longer memories, shared evidence and large meetings affect workload even with a fixed population.

Reduce unnecessary activations, repeated prompt material and irrelevant context before replacing consequential human choices with scripted rules. Cache technical estimates only while all their relevant dependencies are unchanged. Consider a surrogate when the same bounded process is reused enough to repay construction and validation costs; preserve the causal distinctions above and document its domain. Actual throughput and the point at which aggregation becomes necessary remain Q85/workload-specific questions.

### Recommended next implementation work

Source inspection at revision `019287b` finds two distinct starting points. The [native reference mechanics](../../reference_worlds/waltzman/mechanics.py) derive stance from objective resource/constraint state (`_expected_stance`, `reassess_commitment`); the [reference probe](../../reference_worlds/waltzman/probe.py) scripts briefing, relay and intervention sequences and asserts blocked/ready outcomes. Preserve this as a declared fixture. Separately, the [generated-world compiler](../../spikes/any-scenario-2026-10/compile_spec.py) installs `concern-makes-support-conditional` and timed `remedy-completes` processes. This is source evidence about those paths, not a claim that every authored world uses them.

The first useful slice is one concern traveling from source to recipient, with four independently represented things: **the underlying condition, the delivered claim, the recipient's stance, and any institutional hold**. Use the existing authoring and actor-policy seams. A communication should alter delivery and available evidence; the recipient chooses its response; a real task changes only its declared condition; institutional rules determine the procedural consequence. Keep each step inspectable, including the actual context shown to the recipient.

Review the entire resident input boundary: observation, recent events, summary, brief and memory. [Information filtering](../../src/world_substrate/information.py) filters message entities by delivery but passes non-information entities through; [resident context construction](../../scripts/run_authored_world.py) also adds recent actor/rule labels. Message filtering alone therefore does not establish asymmetric knowledge across the complete input. Trace each included field to information the actor can legitimately access before claiming that boundary works.

This is a recommendation for the owning people-world plan, not authorization to build a new cognition framework or change the roadmap here. It can be assessed against the counterexamples above before adding more actors, richer numeric trust variables or a Jev approximation. Existing Q60 and Q75/Q76 own the social-model and decision/norm questions; existing estimate questions own backend adequacy and performance. Where the separation already exists, reuse it; where a compiler or generated rule forces the response, repair that owner rather than add an overlay.

The remaining substantive uncertainties are the adequacy of the chosen actor policies, which scenario-specific conditions determine readiness, and which institution's decision procedure is intended. Those need explicit scenario assumptions and, where behavior remains unknown, targeted evidence. They do not prevent identifying the required causal separation now.

## Complete actor-information contract

**Proposed contract, inferred by agent from Brian's November 12 direction; implementation is unbuilt.** This section specifies the boundary required by the single-concern investigation, not a new cognition framework. It refines the [Q84 exposure contract](../plans/estimate_rules.md#q84-design-contract-deliver-evidence-without-deciding-belief). The engine may use hidden state to compute a consequence; that does not authorize sending that state to an actor.

For every input delivered to a policy, retain its actor, simulated time, source event or initial-knowledge declaration, authorized projection, and transformation that produced it. Initial knowledge is a scenario assumption with an owner and scope; it is not automatically all canonical state. Later observations add available evidence. Interpretation, inference, uncertainty and choice belong to that actor's policy. An actor can infer a hidden fact from accessible evidence, correctly or incorrectly; the platform must not supply the answer as an observation because the analyst knows it.

| Input or surface | Required contract | Forbidden shortcut |
| --- | --- | --- |
| Perception and message delivery | Deliver only authorized fields through a represented channel, including source/provenance the actor can access; retain opportunity-time conditions and recipient-specific disposition | Passing all colocated component fields, or telling a recipient a hidden exposure was suppressed |
| World summary and initial brief | Separate shared public setup from actor-specific role, prior knowledge, personality and goals; derive each factual statement from declared initial knowledge or authorized evidence | Copying the analyst hypothesis, undisclosed defect, another actor's private intention or target outcome into a global summary |
| Recent events | Include only events the actor performed, witnessed through its channel, or learned through a delivered report; render labels with the same field policy | Globally listing accepted rule ids, actor names or hidden task completion |
| Persistent memory, recall and summaries | Store the actor's own received evidence, actions and policy-produced interpretations with their distinction intact; any compression or retrieval consumes only that actor's authorized history | Rebuilding memory from omniscient canonical history or turning a remembered claim into an objective fact |
| Offered actions and labels | Offer actor-known action forms and targets; keep an open attempt path for uncertain possibilities. Validate actual executability at submission | Revealing a hidden defect, password, private actor or secret state because its value changes which action appears |
| Refusals and confirmations | Return the observable result and any explanation authorized by the represented interface; keep the full internal blocker in the restricted execution trace | Explaining that a guessed credential equals an expired secret, or revealing a concealed person's refusal |
| UI, replay, tools and exported context | Declare actor-view versus analyst-view mode; actor-controlled tools and human policies see the same authorized projection as model policies | Feeding omniscient hover text, event panels, tool responses or analyst replay back into actor decisions |
| Model calls and diagnostics | Separate actor-policy input from privileged mechanics/estimator input. Retain exact assembled context, model/configuration identity and result for authorized inspection | Assuming a filtered observation proves the prompt, retrieval result and tool loop are filtered |

Visibility includes existence, identifiers, counts, ordering, labels and error text where these convey a hidden distinction. Two worlds that differ only in actor-inaccessible facts must produce the same actor-input material and offered descriptions until a declared observation, action result or actor-owned inference makes a difference. This is a contract for modeled information flows, not a claim to cryptographic protection against timing or infrastructure side channels. A recipient may legitimately learn a gate is closed by trying it; it need not learn the internal reason. Whether an institution publicly announces a hold is an explicit channel rule.

**Temporal and failure behavior.** Capture an exposure's content, observer/channel conditions and source revision at its authored opportunity time. Delivery retries resume that identity and captured context; they do not redraw detection or read today's geometry for yesterday's event. A committed source event survives a delivery failure. An unavailable perception backend has the declared exposure disposition; it must not silently deliver privileged truth or erase the event. A late result cannot replace a terminal disposition. Missing context or uncertain provenance is surfaced to the run controller and recorded; it must not be repaired by inserting an omniscient summary. Actor-facing failure text is itself filtered. Continuation restores each actor's authorized memory and unresolved exposure identities without importing another actor's history.

**Evidence and review.** The retained restricted record must let an authorized reviewer reconstruct every actor call, including prompts, tool inputs/results and memory transformations, from the inputs actually used. Record the link from each factual input to its initial-knowledge or exposure source, and distinguish actor inference from supplied evidence. A full analyst trace is privileged material; access to it is not permission for simulated actors to read it. Ordinary runs as well as failures need that evidence. Context pruning may remove information, but cannot add hidden facts. No new runtime schema or trace-storage implementation is claimed here.

**Observed gaps at baseline `6b3959c`.** In [the resident caller](../../scripts/run_authored_world.py), `_view` removes named private holder components, while `_recent_for` renders accepted event bearer/rule labels across the event stream without an actor-visibility check. `_llm_choice` adds `world_summary`, `brief` and `recent` after presentation; the Concordia call sites likewise add those fields, and continuation can supply `prior_recent`. [Resident memory](../../scripts/concordia_residents.py) persists observed strings across requests, so an early leak can survive later filtering. [Information visibility](../../src/world_substrate/information.py) explicitly passes non-information/non-delivery entities through. These source findings identify work to perform; they do not establish that every possible field leaks in every world. The complete boundary needs one field-by-field audit through both policy paths and their tools, not another filter applied only to messages.

### End-to-end single-concern scenario contract

**Selected design assumptions, inferred by agent; no run or predictive claim.** Use the partnership above with engineer Ari, coordinator Mara and committee member Bo. A technical validation condition is either failed or passed; a signed report records a specific test and revision. Ari initially knows the test result through the test interface. Mara and Bo initially know only the public project purpose, decision procedure, deadline and their individual role/profile. No participant is instructed to be persuaded, obstructive or supportive. Personality and goals inform their LLM policies rather than prescribing an outcome.

The institution in this example requires a recorded passing validation result and assent from Mara and Bo before activation. A reported concern may request an investigation, but cannot by itself create a mandatory hold. An actual failed validation creates the formal hold; only an authorized passing revalidation clears it. The public dashboard publishes the hold status and the existence of a review, but not private reports or test details. Because the hold rule is public and failure is its sole cause here, a published hold legitimately reveals that validation failed. The asymmetric evidence concerns test details, severity, provenance and remedy claims, not secrecy of that inferable binary result. Initial knowledge above is before the first dashboard delivery; subsequent dashboard observations are shared evidence. This is one explicit procedural assumption, not a universal institutional model. Assent is an actor-owned action; a public supportive statement need not count as recorded assent. Withholding assent can block activation even after a hold clears.

| Stage | Canonical consequence | What actors receive and may decide |
| --- | --- | --- |
| Initial condition | Record the actual test result, report identity/revision, hold state and channel rules separately | Ari gets the result; everyone gets the public dashboard projection. Nobody gets another person's private beliefs. The dashboard can reveal that a hold exists without revealing its cause. |
| Originating claim | Ari or another actor authors a claim with source, content and intended recipients; false content does not change the test result | Sender knows its own message; recipients learn nothing until delivery. A knowingly false claim is a scenario possibility, not the default intention. |
| Asymmetric delivery | Deliver a report to Mara, and a different report or no report to Bo, recording recipient, source lineage and simulated time | Each policy receives only its own evidence. Repeated copies keep common source identity where visible; neither receipt nor repetition changes stance automatically. |
| Interpretation and response | Record any explicit speech, request, assent or withdrawal through that actor's chosen attempt and installed mechanics | Mara may consider the claim credible and Bo may disagree; either can retain support, ask questions or withhold assent. Private interpretation stays in policy state unless expressed. No rule forces these responses. |
| Investigation or remediation | A declared task changes only its specified condition or produces a new test result; work completion alone does not clear the hold | Task performers get their authorized observations. Other actors learn its outcome through the dashboard or a report, not through global memory refresh. A completed review may confirm failure. |
| Revalidation and collective action | An authorized passing test clears the technical hold. Activation still checks current recorded assents and the stated procedure | People may remain doubtful, reverse themselves or refuse despite a passing test. Conversely both may favor activation while the technical hold still prevents it. |
| Analysis | Analyst compares actual conditions, delivery history, expressed reasons, actions and institutional result | Analysis may identify patterns, but a persuasive causal explanation requires evidence beyond temporal ordering or fluent post-run narration. |

The same contract admits a false warning when validation passed, a true warning when validation failed, a delayed genuine report, an unrepaired defect after review, and continued disagreement after repair. These are alternatives to represent, not required experimental runs. If hidden conditions change while the authorized evidence remains the same, immediate actor context remains unchanged; downstream consequences may differ when the represented mechanism acts or evidence arrives. If only a claim changes, the physical condition remains unchanged. This prevents the comparison from presupposing either irrational delay or successful persuasion.

**Cross-checks.** For credentials, knowing/copying a password is actor-specific information; the program verifies a submitted value using privileged verifier state. A valid password need not imply permission, and revocation need not erase memory. Refusal text exposes only the verifier interface's declared response. For a physical sensor, the solver may read actual pressure while a resident receives a noisy, delayed instrument reading with units, measurement time and accessible calibration information. A later solver update cannot rewrite an earlier reading or the actor's memory. Both cases use the same information/consequence distinction without treating humans as credential programs or replacing physical dynamics with social choice.

**Implementation-ready order and limits.** First inventory and constrain every context ingress named above, including restored history; then use the existing authoring, delivery and policy seams to implement the single-concern path; finally inspect retained contexts and transitions against the counterexamples before claiming asymmetric knowledge. The [open-attempt follow-up I0/I1](../plans/open_attempt.md#information-boundary-and-concern-follow-up-selected-design-unbuilt) owns this sequence; the information-delivery OpenSpec targets adopt the required behavior while implementation remains unbuilt. Existing estimate Q84/E5 owns uncertain exposure, Q76/J4 owns credentials, and the social correction remains under Q60; this section does not close those implementation/evidence items. No further product choice is needed for this example: the institution and initial knowledge are declared assumptions. A different investigation must state its own procedure, information channels and adequacy limits.

## Architecture challenge across three kinds of process

**Design examination, 2026-11-12:** Brian approved this first-principles review before implementation. The examples below are counterexamples and contracts, not simulation results or claims of predictive accuracy. The recommendation is **one authority for committed consequences, with different models for different processes**. Decision 006 still rules out building our own cognition framework, scheduler, VM or physics engine. Existing hosts may supply those behaviors through a declared boundary; such adapters are not delivered merely because the boundary can be described.

| Investigation | Distinctions that must survive | Starting method and boundary | Current limitation / decisive counterexample |
| --- | --- | --- | --- |
| Influence operation in the partnership | Actual defect, originating claim, exposure, interpretation, personal stance, formal hold, remediation result | LLM actors with individual profiles, memory and authorized context; code for channels, resources and the actual decision procedure | A received concern can leave support unchanged. The generated family currently forces conditional support and resolves concerns on a timer; that stipulates a social result rather than examining it. |
| Program controlling a door | Program state and version, submitted input, credential validity, possession/knowledge, institutional permission, human disclosure | Execute the relevant program or a faithful finite abstraction; keep disclosure in the actor policy and gate operation in the verifier | Mallory can present a copied valid password despite lacking institutional permission; a revoked password can fail despite Alice remembering it. Native Python rules can express such mechanics, but no general program-execution adapter is established by the generated DSL. |
| Heating a sealed vessel | Quantities and units, elapsed simulated time, pressure/temperature/material state, rupture, conservation boundary, sensor readings | An appropriate existing solver or a justified simpler model supplies a candidate state change over a declared interval; the governing transition validates and commits it | A reaction needing the same process/entity twice in one instant is not a general fixpoint under the current once-per-pair rule. Ending a reaction sweep proves termination, not numerical convergence or physical adequacy. |

### Shared process boundary, not a universal transition language

For each composed process, record these items in the owning world or plan. This is a documentation contract; it introduces no new runtime schema or infrastructure.

- **Purpose and domain:** investigation, interventions, valid operating range and deliberate omissions. State separately whether a model is expressible in native code, expressible in the generated rule language, integrated in the live path, and adequate for this investigation.
- **State and reads:** typed values, units where applicable, causal owner, dependencies and persistent hidden state. Model state may be hidden from actors without being absent from the simulation. Do not encode the same causal effect in both a host and an engine rule.
- **Information access:** the complete projection an actor or estimator may receive, including summaries, recent events, briefs and memory. Location alone is not permission to read internal fields. An estimator of world mechanics and an actor's own inference can have different information boundaries.
- **Output authority:** a typed attempt, observation, estimate or proposed material delta, with its distinct authorized destination. External model output cannot silently become canonical fact. Check declared writes, preconditions and relevant invariants before committing a delta.
- **Time and coupling:** simulated start/end time, cadence, ordering and which earlier outputs each input depends on. A solver owns its internal integration and convergence; dependent models exchange results at declared boundaries. If a solver needs callbacks within an interval, specify that coupling before claiming a one-step adapter suffices. A stale input revision causes explicit recomputation or refusal, never an unnoticed overwrite.
- **Uncertainty and identity:** event versus persistent-condition uncertainty, shared causes, random realization identity, model/configuration/version identity and the retained evidence needed to understand the result. Repeatability is optional where not required; provenance is not.
- **Failure and resources:** incomplete/invalid/unsupported output, non-convergence, unavailable backend and exhausted budget have explicit dispositions. A failed atomic proposal commits no partial material delta. Retain inputs, outputs and failure evidence; account for model calls, solver work, context, memory and trace storage. Do not replace a failed model with a different causal story silently.

### Source findings and their consequences

At the reviewed baseline `65ffed8`, these are observed implementation boundaries:

1. [The generated decision-family compiler](../../spikes/any-scenario-2026-10/compile_spec.py) installs `concern-makes-support-conditional` because residents did not reliably reduce support, and `remedy-completes` resolves a concern at timer completion. Those rules may model a deliberately stipulated institution or fixture. They cannot be presented as general persuasion or successful repair. The condition/claim/stance/hold separation above remains the first substantive people-world correction.
2. [Engine observation](../../src/world_substrate/engine.py) projects colocated entities and requires a location; [information filtering](../../src/world_substrate/information.py) restricts message/delivery components while other fields remain available. [The resident caller](../../scripts/run_authored_world.py) also supplies events, summary and brief. Thus hiding a message does not prove that passwords, private beliefs or latent defects are hidden throughout the context. Audit the complete projection before asserting asymmetric information.
3. [Reaction settling](../../src/world_substrate/engine.py) fires each process/entity pair once per moment. Keep that bounded semantics; do not call it a general fixpoint solver. [Generated action authoring](../../src/world_substrate/action_authoring.py) supports only its declared effect operations and timing modes. Numeric components alone do not establish arbitrary physical or program expressibility.
4. [The Builder's things/people selector](../../scripts/world_builder_service.py) is an authoring convenience. It must not force every process in a mixed world to use the same implementation method or determine whether an entity can act.

These findings do not justify a new universal engine. First specify and enforce the complete observation boundary; separate scenario stipulations from shared mechanics; define a concrete host adapter only when a chosen investigation needs behavior the existing method cannot express. Mapping a requirement to code establishes its owner and evidence path, not scientific validity.

### Recommended sequence and tradeoffs

1. **Settle the small conceptual contracts now:** credentials and norms (Q76), estimator dependencies (Q83), and uncertain observation (Q84). Their owning plans define the selected contracts; backend adequacy and implementation evidence remain separately open where needed.
2. **Design the complete actor-input boundary, then the single-concern path.** This addresses the influence investigation and credential secrecy together. It costs broader inspection than message filtering alone, but avoids validating runs whose actors are omniscient. Preserve forced support/remedy rules as labeled fixture behavior until their owner is repaired.
3. **Link stable promises into AES, using direct evidence.** Correct scan roots and existing test links first. A requirement with only part of its behavior implemented remains incomplete; a missing annotation is not automatically a missing capability. Universal read enforcement, durable consent and storage-failure guarantees must not acquire false implementation labels.
4. **Select a program or physical adapter only for a concrete investigation.** The benefit is broader applicability with commodity tools; the cost is a real coupling, validation and resource obligation. Do not build speculative adapters merely to make a generality claim.

No human scope decision is needed for these documentation contracts. A proposal to abandon governed consequence authority, build a new engine, or promise a specified scientific accuracy would require a separate product decision. No such proposal is adopted here.

## Glossary

### What is represented

| Term | Meaning here |
| --- | --- |
| Entity | A represented thing: person, organization, vehicle, program or message. Existence does not imply agency. |
| Component / process | A part or evolving behavior of an entity or environment. Choose methods at this level; one entity can need several. |
| Actor / policy | A decision maker and the procedure selecting its attempts from its information and internal state. Policies can be learned, scripted or human-controlled. |
| Mechanism | An account of how conditions and actions cause consequences. An executable engine rule can still encode the wrong account. |
| Constraint | What is possible within the modeled world. Distinguish physical, technical and deliberately stipulated constraints. |
| Decision | A choice attributable to an actor. One actor's attempt does not supply another actor's consent. |
| Norm | What ought to happen or is institutionally permitted. A breakable norm allows violation; detection and sanction are separate processes. |
| Consent / permission / executability | An actor's agreement; institutional authorization; whether a mechanism accepts an action. None implies the other two. |
| World fact / observation / belief | What is true in the simulated world; information available to an actor; what that actor takes to be true. They can differ. |
| Analyst interpretation | An explanation of the trace, which does not create facts or establish what an actor believed. |
| Causal ownership | Which actor or process supplies a change or choice. Composition must not duplicate that authority or silently transfer it. |

### How it is represented

| Term | Meaning here |
| --- | --- |
| Modeling role | The job: policy, physical transition, perception, estimate, adjudication or presentation. Distinct from implementation technology. |
| Implementation method | Code, mathematical dynamics, stochastic process, generative language model, typed decision model, learned surrogate or composition. |
| Typed decision model | Produces an answer within a bounded schema. Jev is a candidate; output shape does not establish causal validity. |
| Jev / System 1 | Jev is the named TypeSafe AI System One model exposed through DigitalOcean's typed state/question API (`/v1/systemone`), not an acronym or a general synonym for learned simulators. “System 1” is a cognitive analogy/product description, not evidence of its internal mechanism, calibration, fidelity or end-to-end cost/latency. See the [official interface documentation](https://docs.digitalocean.com/products/inference/how-to/use-system-one-api/). |
| Learned surrogate | An approximation replacing another model or process within a stated domain. It can represent human, mechanical, biological or other behavior. |
| Resolution / aggregation | Which individual distinctions and time/space scales survive; aggregation combines individuals or events. |
| Fidelity | Adequacy for the stated question and interventions. Detail, fluent explanations and replayability are insufficient evidence. |
| Approximation | A deliberate simplification with an applicability boundary and an account of conclusions it no longer supports. |
| Intervention | A change the investigator reasons about, such as altered access, incentives or message content. Its causal pathway must survive modeling. |
| Calibration | Agreement between stated probabilities and observed frequencies over an appropriate reference class. It does not transfer automatically between tasks. |

### Uncertainty, time and resources

| Term | Meaning here |
| --- | --- |
| Epistemic uncertainty | Lack of knowledge about a condition or mechanism. A fixed but unknown fact need not vary on repeated attempts. |
| Stochastic variability | Variation the world model generates between events, conditional on state. Its dependence structure must be specified. |
| Subjective confidence | An actor's confidence in a belief; may differ from truth and estimator confidence. |
| Answer confidence | A model's confidence in an answer, not automatically event frequency or actor belief. |
| Latent state | A persistent modeled condition hidden from some observers. Establish it at its causal lifetime, then preserve it until changed. |
| Simulated time / cadence | Time inside the world, and when a process updates. Neither is API response time. |
| Wall time / latency / throughput | Elapsed execution time; delay for a request or step; completed work per unit time. Improving one need not improve the others. |
| Resource budget / scalability | Limits on money, CPU/GPU work, memory, storage, bandwidth and quotas; how demands grow with population, interactions, events, context and duration. |

## Selection heuristics

State the investigation, interventions and required distinctions. Choose the simplest adequate method for each process, with explicit information and authority boundaries.

| Need | Starting choice | What would make it inadequate |
| --- | --- | --- |
| Known program behavior, accounting, software permissions | Code or faithful abstraction | Replacing exploitable behavior with intended policy |
| Known physical relationships | Appropriate dynamics or established solver | Omitting relevant scale, thresholds or feedback |
| Justified event variation | Stochastic process with conditional dependencies | Invented probabilities or independent draws for shared causes |
| Human interpretation, planning and communication | Cognition with personality, memory and partial observations; normally an LLM policy | Omniscience, generic agreeableness, prescribed conclusions or missing actions |
| Bounded contextual judgment or selection | Typed decision model such as Jev | Missing options, context, persistent state or expressive freedom |
| Repeated costly process within a known domain | Surrogate, cached computation or aggregation | Losing relevant identities, network position, rare thresholds or intervention responses |

Jev might estimate equipment failure, classify a sensor observation, select a controller action or participate in a person's policy. These are different roles with different authority. The estimate plan's restriction on choosing for people applies to **mechanics estimates**, not to Jev inside a person's policy.

Hybrid models are an option: an LLM maintains interpretation, a typed model makes bounded selections using that state, and code executes consequences. This is not a measured improvement. Every boundary needs inputs, memory, timing, outputs, permitted writes and failure behavior. A cheap fallback must not overwrite beliefs or bypass consent.

Dennett's stances offer explanatory perspectives: physical processes, designed function, or beliefs and desires. They do not prescribe implementation technology; his discussion emphasizes intentional explanation's usefulness and limits ([Dennett](https://edge.org/3rd_culture/dennett2/dennett2_p4.html)). Levin's axis of persuadability motivates asking which interventions a system responds to, from physical modification through feedback/training to communication. It is a research lens, not a proven routing algorithm ([Levin, TAME, Figure 2](https://doi.org/10.3389/fnsys.2022.768201)). Our heuristic is to preserve the relevant response repertoire regardless of implementation method.

## Probability is a modeling decision

Jev's hosted interface accepts context and typed questions and returns bounded answers ([API documentation](https://docs.digitalocean.com/products/inference/how-to/use-system-one-api/)). That alone does not justify interpreting its probabilities as world-event frequencies.

Specify what an estimate estimates, whose information it uses, its reference class and when the underlying condition can change:

- **Unknown condition:** whether a ford is already passable. Repeated attempts do not justify independently resampling its condition. Establish a latent condition per world, or retain uncertainty explicitly until evidence resolves it.
- **Variable event:** a passable ford may still involve slipping on a crossing. Represent shared weather, load and event dependence before choosing independent draws.
- **Classification:** whether a stopping condition is already satisfied. Sampling answer confidence randomly terminates runs; use the declared assessment/uncertainty policy instead.
- **Actor choice:** an individual's response. A mechanics estimate cannot replace their decision. A probabilistic actor policy may make it if that policy owns the relevant state.

Sampling depends on the estimate's meaning; it is not compulsory for every typed answer. This resolves a conceptual ambiguity in the draft estimate plan, without establishing calibration, choosing numeric probabilities or implementing a replacement.

## Speed, money and computational scale

**Optimize among adequate alternatives.** If the budget cannot preserve an essential distinction, narrow the supported question, declare an approximation or stop. Do not silently present the cheaper model as answering the original question.

These are analytical accounting relationships, not measured performance or prices:

- Requests = sum over process activations of calls per activation, including interpretation, retries, authoring and adjudication where applicable. Distinguish cache hits from actual calls.
- Monetary cost = inference billing + compute hosting + storage/network + other billed services. Token-priced inference sums uncached input tokens × input price, cached input tokens × cache price, and output tokens × output price, plus any request fee. Use actual billing units for other APIs; do not count hosted inference resources twice.
- Wall time is bounded below by the longest dependent chain and by total work divided by sustainable capacity. Parallelism helps independent work, not necessary causal sequencing.
- All-to-all directed candidate pairs number N(N−1), counting each actor's possible partners; sparse interaction work instead follows represented edges. Neither count automatically equals model calls.

For each design record activation frequency, context growth, dependency depth, peak concurrency, quotas, CPU/GPU work, memory and trace storage. Label measured values, worked-out estimates and guesses. Long runs can be dominated by retrieval, context growth and trace retention. Price and latency rankings need current evidence; “System 1” does not prove end-to-end speed or cost.

Separate upfront construction, training, validation and precomputation from recurring execution and maintenance. For a fixed workload, total cost over R runs is setup cost + R × per-run cost + maintenance. This is a worked-out accounting form, not a price estimate; use a sum when runs differ. A surrogate with higher setup cost becomes worthwhile only over a sufficient reuse horizon, while still preserving the required distinctions. Include human authoring/review effort separately with an explicit valuation if converting it to money.

Prefer event-driven activation when quiet intervals have no relevant effect. Batch independent questions when information boundaries permit. Cache all relevant dependencies, including model and prompt versions; estimates and random draws have different lifetimes. Aggregate only when identity, network structure and heterogeneity are dispensable for the question. Escalation to a richer model needs a declared trigger and consistent state; confidence alone is not a proven detector of missing mechanisms.

## Recording and resolving choices

A short decision in the owning scenario or plan records:

1. Investigation, interventions and distinctions that must survive.
2. Process, causal owner, accessible information and state lifetime.
3. Method, resolution and omissions; why simpler choices are insufficient.
4. Uncertainty semantics, dependence, evidence and applicability limits.
5. Resource calculation and its basis; failure and fallback behavior.
6. What finding would require revisiting the choice.

This is a documentation pattern, not a new runtime schema or acceptance gate. Resolve questions through definitions, construction, counterexamples and prior art first. Run an evaluation only for named uncertainty those cannot settle. Model agreement and attractive stories do not establish real-world validity. Q60's separately approved social comparison remains its existing task; Q50 already rejects a custom believability metric as a finish gate.

### Remaining questions

These routes into the [existing ledger](../planning/open-questions.json) are not a duplicate status tracker. Definitions and evidence remain in [questions_src.py](../../tools/planning/questions_src.py).

| Existing questions | Settled principle; remaining evidence |
| --- | --- |
| Q59: generality | Inspect required mechanisms and interventions, not just vocabulary. New worlds address remaining behavioral uncertainties. |
| Q63, Q75, Q76, Q96: estimates, choices, norms, exchanges | Estimates are non-authoritative; consent is separate. Q96 records unoffered coins being taken through an installed rule: compiler checks do not prove fidelity. Repair/evidence remain with existing owners. |
| Q82, Q83: relevant facts and read coverage | Declare dependencies before interpreting model agreement. Backend sensitivity and adequacy remain uncertain; monotonicity is not calibration. |
| Q84: noticing | Separate delivery, detection, interpretation and response. Probabilities and contextual adequacy remain scenario-specific. |
| Q85: scale | Workload/dependency accounting precedes benchmarking. Throughput, tail latency and saturation need measurement for the chosen workload. |
| Q86: stopping | Assessing an existing fact differs from generating an event. The stopping policy and implementation still need explicit treatment. |
| Q88: replacement by bands | Small-case agreement does not establish preserved interventions or boundaries. Define applicability before replacement. |

Review notes, November 12: source inventory found strong execution vocabulary but no unified modeling guide. Newer approved constraint/decision/norm distinctions and the existing consent counterexample are incorporated here. Remaining risks concern whether composed models preserve relevant causal and informational distinctions within their resource envelope.
