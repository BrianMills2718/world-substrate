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
