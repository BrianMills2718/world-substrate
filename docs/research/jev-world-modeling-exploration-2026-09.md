---
role: research-note
status: exploratory
reviewed_through: 2026-09-17
adoption_status: not-adopted
---

# Jev-inspired ideas for non-cognitive world modeling

## Status

This note records **tentative ideas for future exploration** prompted by Jev / "System One" style typed probabilistic decision models.

Nothing here is an adopted World Substrate capability, roadmap commitment, architecture decision, dependency choice, or claim that Jev itself should be integrated. The useful object of study may be the **interface pattern** rather than the specific product:

> unstructured or high-dimensional evidence in -> bounded typed probabilistic outputs -> deterministic software remains authoritative.

The ideas below are intentionally evaluated against World Substrate's existing doctrine:

- canonical world truth remains project-owned;
- installed mechanics retain consequence authority;
- model output does not directly mutate canonical state;
- uncertainty, inference, stochasticity, and observation should be represented explicitly when they matter;
- provenance/versioning should make learned contributions inspectable; and
- derived analysis must not silently become causal world state.

## Why this may matter outside cognition

The obvious use of a fast typed model is resident action selection. That may or may not prove useful.

A potentially more interesting direction is **non-cognitive probabilistic inference inside the world-modeling stack**: perception, state estimation, stochastic kernels, latent-property estimation, or candidate-space reduction.

The central question is:

> Can learned typed probabilistic estimators expand the class of worlds World Substrate can model without surrendering explicit consequence authority?

A useful separation is:

```text
canonical represented state
        |
        +-------------------------+
        |                         |
        v                         v
explicit mechanics        learned estimators
        |                         |
        |                  typed probabilities /
        |                  bounded latent values
        |                         |
        +------------+------------+
                     |
                     v
              installed mechanic
                     |
              Engine commit/refusal
                     |
                     v
             canonical consequence
```

The learned component may inform a mechanic. It does not become the commit authority.

## Candidate exploration 1: observation and state estimation

Some useful worlds will contain facts that are only indirectly observed: noisy sensors, imperfect reports, imagery or text evidence, partial measurements, ambiguous traces, detection systems, or multi-source evidence about an underlying represented condition.

A typed probabilistic estimator could convert messy evidence into a bounded distribution:

```text
evidence:
  smoke report
  thermal reading
  sensor-health metadata

estimator output:
  fire_present:
    true: 0.81
    false: 0.19
  sensor_fault:
    true: 0.24
    false: 0.76
  severity:
    low: 0.12
    medium: 0.63
    high: 0.25
```

Important boundary: this output should not silently rewrite canonical state.

Possible representations:

1. **observation evidence only** — retained as actor-visible or observer-visible evidence;
2. **derived estimate** — a recomputable projection outside canonical material state;
3. **represented measurement artifact** — canonical because the world explicitly represents that a measurement/assessment was produced;
4. **mechanic input** — consumed by an installed mechanic only when that dependency is declared.

Research questions:

- When should an estimate be canonical evidence versus a derived projection?
- How should calibration metadata be retained?
- Can two estimators disagree without creating alternate world truth?
- How should estimator outputs participate in information lineage versus hard causal ancestry?

## Candidate exploration 2: stochastic mechanics with explicit probability kernels

Many domains legitimately require uncertainty: disease transmission, component failure, weather, ecological spread, detection, combat resolution, market response, reliability/degradation, queue/service behavior, or uncertain institutional outcomes.

A Jev-like pattern suggests separating **probability estimation** from **world transition authority**.

```text
canonical state
     |
     v
typed probabilistic kernel
     |
     +--> P(failure)      = 0.037
     +--> P(degradation)  = 0.214
     +--> P(no_change)    = 0.749
     |
     v
world-owned stochastic draw
     |
     v
installed mechanic checks outcome
     |
     v
Engine commit/refusal
```

World Substrate should own or explicitly govern the random source, seed/draw provenance where reproducibility matters, estimator/model identity, input state references, output distribution, sampled outcome, and the mechanic that turns that sampled result into a transition.

A future event could distinguish:

```text
estimated distribution
random draw
selected outcome
mechanic checks
committed effects
```

rather than collapsing uncertainty into opaque narrative.

## Candidate exploration 3: learned latent properties

Some represented properties may be difficult to specify with hand-written formulas but still useful as bounded typed estimates, for example structural instability, congestion risk, vegetation stress, terrain traversability, probability of detection, supply-chain fragility, market sentiment, fire spread potential, social tension, or equipment degradation risk.

Pattern:

```text
primitive represented state
        |
        v
versioned estimator
        |
        v
typed latent estimate
        |
        +--> analysis only
        |
        +--> represented evidence
        |
        +--> declared mechanic input
```

The architecture must make the status of the latent explicit.

A useful discipline may be:

- **analytic latent**: cannot affect transitions;
- **evidentiary latent**: represented as a measurement/assessment event;
- **causal latent**: may affect later transitions only because an installed mechanic explicitly reads it.

The existing causal-force test remains relevant: if removing the latent while holding lower-level events fixed would change later affordances or transitions, the latent has become causally operative and requires full provenance/authority treatment.

## Candidate exploration 4: affordance-space ranking and candidate reduction

Larger worlds may eventually create expensive combinatorial discovery spaces.

A learned typed scorer could help decide **where to search**, without deciding what is actually legal:

```text
10,000 candidate destinations
        |
        v
cheap learned applicability scorer
        |
        +--> A 0.002
        +--> B 0.004
        +--> C 0.910
        +--> D 0.370
        |
        v
rank / page / prioritize candidates
        |
        v
normal installed-mechanic applicability checks
```

Useful principle:

> learned ranking may reduce search cost; exact installed mechanics still determine applicability.

Research questions:

- Can ranking preserve completeness guarantees?
- How should low-scored but valid affordances remain discoverable?
- Should estimator-based pruning ever be allowed, or only ordering/paging?
- How should explicit overflow/refusal interact with approximate ranking?

## Candidate exploration 5: probabilistic interpretation of external data

When World Substrate consumes real-world or externally generated data, a typed inference layer could normalize uncertain evidence into explicit bounded claims before those claims enter a represented world.

Examples include satellite or imagery observations, qualitative reports, event extraction from text, uncertain entity resolution, sensor anomaly classification, and noisy external feeds.

This is distinct from resident cognition. The estimator is part of the **world ingestion / observation apparatus**.

Potential benefit: uncertainty becomes explicit at the boundary instead of disappearing into ETL.

Potential risk: an ingestion estimator could accidentally become a hidden semantic or causal authority. Any promoted design should make clear whether it is producing a source observation, a derived interpretation, a canonical represented fact, or evidence that an installed mechanic may later consume.

## Scaling thesis: relieve the LLM game-master bottleneck

A stronger reason to explore this pattern is **world-modeling scale**, especially where mechanisms are hard to specify explicitly.

A naive generative-world architecture often centralizes fuzzy adjudication in a general LLM:

```text
world state
   |
   v
LLM game master
   |
   +--> interpret the situation
   +--> identify relevant factors
   +--> infer a likely outcome
   +--> format the result
   +--> effectively adjudicate consequences
   |
   v
state mutation
```

That can work for prototypes, but it creates a central throughput and authority bottleneck. As worlds grow, the game master may be asked to adjudicate large numbers of semantically difficult effects involving many entities, relationships, observations, and mechanisms.

The cost is not only token spend. A universal LLM adjudicator tends to combine too many responsibilities:

- semantic interpretation;
- mechanism selection;
- latent-state inference;
- probabilistic judgment;
- consequence generation;
- formatting;
- and, in weak architectures, de facto transition authority.

A Jev-like or otherwise typed System-One layer suggests a different decomposition:

```text
world state / evidence
        |
        v
typed probabilistic estimator
        |
        v
bounded intermediate judgment
        |
        v
explicit installed mechanic
        |
        v
Engine commit/refusal
```

The estimator handles a hard-to-specify intermediate judgment. The mechanic still determines what that judgment means for the represented world.

### Where this is more useful than equations

This should not replace explicit equations or mechanistic models when those are available.

Preferred order:

```text
known quantitative relationship
    -> equation / table / explicit rule

hard quantitative relationship with trusted simulator
    -> simulator / surrogate

structured prediction with task data
    -> conventional statistical or ML model

messy semantic evidence or dynamic hypotheses
    -> typed zero-shot / System-One estimator

novel planning, explanation, invention
    -> general reasoning/generative LLM

canonical consequence
    -> installed World Substrate mechanics + Engine
```

The promising niche is therefore **hard semantic or high-dimensional mechanisms that are awkward to hand-code but do not deserve a full generative adjudication call**.

Examples might include:

- panic or unrest risk from heterogeneous observations;
- probable equipment failure mode from maintenance notes and telemetry;
- credibility or relevance classification of incoming represented reports;
- terrain or route difficulty from mixed structured and descriptive evidence;
- likelihood of detection given contextual cues;
- social or institutional pressure categories derived from many represented signals;
- external event interpretation before that evidence enters the represented world.

### Why this may matter at scale

In a persistent world, fuzzy judgments can multiply with:

- active entities;
- active relationships;
- incoming observations;
- autonomous processes;
- candidate interactions;
- and mechanism opportunities.

If each such judgment requires a general autoregressive LLM call, cognition/adjudication becomes a central simulation bottleneck even when the judgment itself is small.

A typed System-One layer could potentially move many of those judgments into cheap, bounded, parallel inference while reserving expensive LLM calls for genuinely deliberative or generative work.

Conceptually:

```text
thousands of active world situations
            |
            v
parallel bounded estimators
            |
            +--> panic risk
            +--> failure mode
            +--> detection likelihood
            +--> report relevance
            +--> route difficulty
            +--> supply disruption risk
            |
            v
explicit mechanics consume selected estimates
            |
            v
Engine remains singular consequence authority
```

The architectural payoff would be **decentralizing fuzzy adjudication without decentralizing world truth**.

### Important boundary

The target is not to replace one opaque game master with hundreds of opaque learned mechanics.

The intended sweet spot is:

> explicit mechanics for consequences; learned estimators for difficult intermediate judgments.

A model may estimate:

```text
P(panic) = 0.73
```

but it should not directly invent:

```text
therefore 40 people flee, three exits block, and food prices double
```

Those downstream consequences remain the job of installed mechanics operating over canonical state.

### Research implication

If this pattern proves useful, one important evaluation dimension is **throughput substitution**:

> How much general-LLM adjudication can be removed from a large world by replacing narrow fuzzy judgments with typed estimators, without materially weakening causal inspectability or model quality?

A future spike should therefore compare not just estimator accuracy, but:

- latency per judgment;
- cost per judgment;
- number of judgments evaluated in parallel;
- calibration quality;
- rate of LLM escalation;
- consequence-trace clarity;
- and total reduction in general game-master/model calls.

This scaling thesis is exploratory, but it may be a stronger motivation than using Jev-like models merely as another cognition adapter.

## Possible future abstraction: Estimator / Probabilistic Oracle

If repeated use cases justify it, World Substrate could eventually explore an explicit non-mutating estimator contract.

Tentative sketch:

```text
Estimator
---------
estimator_id
version
declared_read_paths
input_schema
output_schema
model/runtime identity
calibration metadata
provenance
determinism/stochasticity metadata
NO write_paths
NO direct commit authority
```

Possible call shape:

```text
estimate_e(W, input) -> TypedEstimate
```

Where `TypedEstimate` may contain a categorical distribution, bounded scalar estimate, confidence interval, calibrated probability, abstention/unsupported status, source/model/version identifiers, exact represented inputs used, and optional retained evidence references.

A mechanic that consumes an estimate would have to declare that dependency.

Example:

```text
bridge-collapse-v2 reads:
  components.bridge.load
  components.bridge.corrosion
  estimate.structural_failure_risk

check:
  structural_failure_risk > 0.75

effect:
  condition = "collapsed"
```

A corresponding trace could retain primitive inputs, estimator identity/version, probability or latent output, stochastic draw if any, mechanic threshold/check, and committed consequence.

This would be materially different from allowing a model to generate the next state directly.

## Anti-patterns

### 1. Learned next-state authority

Avoid:

```text
world state
   -> opaque learned model
   -> next canonical world state
```

unless a future research program explicitly chooses to relax the current architecture.

### 2. Probability interpreted as truth

Avoid:

```text
P(fire)=0.81
therefore canonical fire_present=true
```

without an installed representation, measurement, or transition rule explaining that conversion.

### 3. Hidden estimator dependencies

If a transition depends on a learned estimate, that dependency should not be hidden inside arbitrary rule code. It should be versioned and observable enough to distinguish primitive represented state, learned inference, stochastic selection, mechanic logic, and committed effect.

### 4. Approximate affordance pruning that silently removes valid actions

Approximate scoring should not violate the existing doctrine that bounded implementations must not silently hide valid actions when candidate limits are reached.

### 5. Vendor-specific architecture

Do not make Jev itself an authority dependency merely because it motivates this exploration. Any estimator abstraction should remain compatible with local statistical models, conventional ML, rules, simulation surrogates, or future providers.

## Evaluation criteria for a future spike

A useful experiment should demonstrate a world-modeling problem that is awkward under explicit deterministic mechanics alone.

Candidate acceptance questions:

1. Does the estimator solve a real modeling problem rather than merely replace simple code?
2. Is its output type bounded and inspectable?
3. Is uncertainty explicit rather than hidden?
4. Can model/version/input provenance be retained?
5. Does the Engine remain the only canonical commit authority?
6. Can replay or bounded reproducibility remain meaningful?
7. Can a mechanic declare exactly how the estimate affects consequences?
8. Can analysis distinguish model uncertainty from world stochasticity?
9. Can the estimator abstain or report unsupported inputs?
10. Does use of the estimator preserve the semantic/mechanical boundary?
11. Is there a deterministic or explicit baseline for comparison?
12. Does the experiment reveal a reusable abstraction rather than a one-world special case?

## Suggested first experiments

### A. Failure-risk assay

Create a tiny represented component with explicit load/corrosion state. Compare a hand-written deterministic threshold, a simple logistic/statistical estimator, and a typed learned estimator. Keep the collapse mechanic explicit and identical across estimator variants.

Measure provenance, replay behavior, calibration visibility, and whether the estimator abstraction clarifies or obscures causality.

### B. Noisy-observation assay

Create a hidden represented condition plus several noisy observation channels. Test whether a typed estimator can produce actor-specific or observer-specific probability distributions without creating alternate canonical state.

This would directly exercise the distinction between world truth, observation evidence, inferred belief/estimate, and mechanic-declared hard causal ancestry.

### C. Large-affordance ranking assay

Construct a deliberately large but deterministic affordance space. Use an approximate scorer only to rank/page candidates, then run normal exact applicability checks.

Verify that ranking improves search cost without making valid actions silently unreachable.

## Relationship to current World Substrate doctrine

The interesting synthesis is not:

> learned models decide what reality does.

It is:

> learned models may estimate uncertain or expensive-to-derive properties of a represented world; World Substrate decides how those estimates are represented, consumed, sampled, and allowed to affect canonical consequences.

A concise boundary:

```text
typed probabilistic inference
        !=
canonical consequence authority
```

Or:

> borrow estimators; own reality.

This is consistent with the existing project posture only if estimator outputs remain explicitly typed, versioned, bounded in authority, and subordinate to installed mechanics and Engine commit/refusal.

## Open questions

- Should estimates ever be stored in canonical state, or normally remain derived?
- If stored, when are they measurements versus world properties?
- How should calibration drift affect long-lived worlds?
- How should estimator upgrades interact with exact replay and historical interpretation?
- Should estimator outputs be recomputed during replay or retained as transition evidence?
- How should seeded randomness be separated from epistemic model uncertainty?
- Can a mechanic consume a full distribution rather than a sampled scalar/category?
- Can uncertain mechanics remain explainable enough for causal inspection?
- How should estimator read authority be enforced if declared read-scope enforcement is added?
- Is "Estimator" the right abstraction, or should this remain a generic external-analysis adapter until multiple worlds require it?
- Which use case actually earns this abstraction first?

## Current disposition

**Explore later; do not adopt yet.**

The most promising non-cognitive directions are:

1. probabilistic observation/state estimation;
2. stochastic mechanics with world-owned sampling;
3. versioned latent-property estimators;
4. affordance ranking without consequence authority; and
5. explicit uncertainty at external-data ingestion boundaries.

No current milestone requires any of them.
