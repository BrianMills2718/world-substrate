# Waltzman simulator lineage and recommendations

Review, 2026-11-07. **Revise the product approach while retaining the useful implementation.** The lineage supports a general exploratory simulator as the intended product. The current work has built useful enforcement and inspection machinery, but its Waltzman showcase increasingly substitutes a compiled concern-and-decision procedure for the social mechanism it is meant to explore. More successful runs of that procedure will not, by themselves, close the gap.

The recommended next step is a bounded comparison on the same situations: retain today's implementation as a baseline, compare a simpler hybrid simulation, and judge whether consequential behavior comes from the represented people, information and material constraints. Do not start another replacement repository or expand the existing repair loop before that comparison.

Review boundary: product concept and current prototype; decide what direction merits further work. Compare original requirements, paper, code and retained runs. Historical narrative necessarily reads prior decisions; independently check current technical findings against code and artifacts. No predictive-validity or deployment-readiness claim.

## Concise investigation notes

- Baseline: World Substrate `5719983` (2026-11-06), clean primary checkout. Review uses a separate worktree. Relevant predecessor: Cybernetic Influence v3; related branch: Wargame. Historical repositories and original statements are being investigated separately.
- The stated outcome remains a generatively authored persistent simulation platform; Waltzman is a showcase. Yet the roadmap explicitly defers generality and predictive behavioral validity from promotion. See [roadmap](../../roadmap/README.md), outcome and demo acceptance criteria.
- The narrow governed-rules scope was approved by Brian on October 5; it is not sufficient evidence of accidental drift. October 7 explicitly restores an any-scenario path, attempted actions, and rules written during a run. See [Decision 006](../decisions/006-governed-rules-layer-scope.md) and [Decision 007](../decisions/007-any-scenario-path.md).
- Preliminary distinction: enforcement correctness, adequacy of a generated model, and validity of inferences from its output are separate claims. The [architecture](../architecture.md) correctly limits its causal claims to installed mechanics. The review will check whether product acceptance preserves that distinction.
- The [system model](../model/ODD.md), sections 4.1–4.2, records authoring-path gaps relative to the donor, including person profiles and information representations. These are leads to verify in current source, not assumed current defects.
- No implementation changed; no paid simulation run requested. Next evidence: current resident inputs, generated rules, and complete retained run records.
- Correction after source inspection: the old any-scenario comparison in ODD 4.1–4.2 does not describe the newer people-world route. `scripts/people_world.py` and `scenario_spec.py` restore behavioral profiles, information items and scheduled moments; `assemble_people_world` returns individual briefs. Do not diagnose their universal absence.
- Current source establishes a stronger concern: `compile_spec.py:312–338` automatically makes support conditional when an open concern is delivered and resolves a remedy on its countdown. Neither process evaluates the substance of the concern or remedy. The comments tie the former to a run where agents did not choose the desired support decrease.
- Current live open attempts remain interpretations into installed action kinds; unmatched attempts do not install new mechanics (`run_authored_world.py:576`, `attempt.py:109–124`). Distinguish this from the October 7 offline game-master experiment.
- Paper read in full by the research lane: 19 pages, supplied PDF hash matches repository provenance. It presents a conceptual micro-to-macro influence mechanism, not calibrated equations. A procedural blockage alone does not establish that mechanism.

## Findings and recommendations

### What the original vision requires

The strongest repository statement is **flexible exploratory simulation with selective, question-relative exactness**. Wargaming, economics and organizational analysis are examples. People, material constraints, information and evolving relationships should coexist; exact bookkeeping serves the question rather than defining the product. This is explicit in V3's [foundation decision](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/446fd57191614be1284655fa8970cf547783df6b/docs/adr/013-generalized-simulator-foundation.md#context) and [external review packet](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/446fd57191614be1284655fa8970cf547783df6b/docs/research/028-general-simulator-external-review-packet.md) (transition authorities and structural endogeneity).

A practical interpretation is: a person can describe a bounded new situation, inspect its assumptions, run it, intervene, and understand what happened without commissioning a new scenario engine. It need not simulate everything, predict real-world probabilities, or reproduce identical prose. It does need an honest way to handle an important interaction that its initial model omitted.

There is a real unresolved design tension. V3 accepted coarse LLM adjudication where exactness was unnecessary; World Substrate's [founding decision](../decisions/001-project-scope.md) made LLM-generated consequences a non-goal. Both directions were recorded as accepted. This review cannot dismiss the latter as an agent mistake. It can identify its consequence: broad usefulness now depends on generating sufficiently complete executable mechanics, a harder task than generating a plausible next event. The later [any-scenario decision](../decisions/007-any-scenario-path.md) partly reopened that boundary.

### How the work changed

Dates below identify decisions or repository history, not dates when every capability worked.

| Period | Direction and result | Significance |
| --- | --- | --- |
| March 2026 | Wargame's separate line combines natural-language action, mechanical tendencies and LLM adjudication; root commit `2a5d9c5`. | Relevant prior art in the workspace; shared ideas do not prove direct code ancestry. |
| July 23 | V3 begins with a clean vertical extracted from V2, deferring broader authoring; root `1363f03`. | A legitimate small start that does not itself prove generality. |
| July 31–August 11 | The foundation comparison initially preserves existing CI invariants; the owner clarifies the general simulator goal and selects Concordia. | The problem of treating existing machinery as the objective was already explicitly recognized. See V3 ADR-013 and research 026. |
| August 14 | V3 separates scenario execution from analysis after the research question had entered actor/adjudicator context. | A substantive correction: a simulation should not be steered toward the analyst's desired finding. See [ADR-014](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/446fd57191614be1284655fa8970cf547783df6b/docs/adr/014-separate-simulation-and-analysis-authority.md). |
| August 31–September 2 | World Substrate becomes a separate project, with Castaway mechanics and CI ideas as donors; executable rules own consequences. | Stronger internal consistency, with a much larger burden on model authoring and causal coverage. |
| September 7–18 | Generative living worlds become the product framing; Waltzman becomes the showcase; delivery concentrates on a native coordination vertical. | Reasonable staging, provided success of that vertical is not read as success of the broader product. See Decisions [004](../decisions/004-product-and-adoption-strategy.md) and [005](../decisions/005-native-waltzman-delivery.md). |
| September 30–October 5 | V3 adopts a replacement-first gate; World Substrate retains a narrow governed-rules layer around external runtimes. | Approved restraint on what to build internally, not abandonment of the general simulator. See [V3 ADR-017](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/446fd57191614be1284655fa8970cf547783df6b/docs/adr/017-replacement-first-simulation-platform.md) and Decision 006. |
| October 7–8 | Decision 007 restores describe-any-scenario, attempts that can fail over time, and rules written during a run. The donor scenario schema is adopted. | The generality gap is recognized again. The decision explicitly notes that five weeks of native work produced one situation shape. |
| October 15–23 | The build path gains profiles, communication and compiled group decisions. Harness-based authoring is directed; recurring remedies, reviews and support transitions accumulate. | Some real capabilities return, but more of the example's expected behavior is encoded in the compiler. `b7d1dc5` makes concern-driven loss of support automatic; `c403c79` adds interruptible remedies. |
| October 26–November 6 | Open attempts, same-moment consequences and declared laws strengthen execution. A retained November 4 Waltzman run still exhibits procedural concern resolution. | These improvements matter, but do not establish that the influence mechanism or cross-domain authoring problem is solved. |

The history is therefore more complicated than a pristine vision being forgotten. The broader goal was repeatedly restated, legitimate narrower slices were approved, and the same product gap resurfaced. My inference is that **local acceptance tests became substitutes for the containing objective**.

### Three problems that change the next decision

**1. Important social outcomes are stipulated where the simulator should let them be contested.**

Observed in current source: [compile_spec.py](../../spikes/any-scenario-2026-10/compile_spec.py), lines 312–338, automatically turns a full supporter's stance conditional when an open concern arrives. The comment records the motivation: an earlier run's agents never chose to make support conditional. The same code resolves a remedy by elapsed rounds. Lines 120–142 hard-code remedy, deployment and review timing; lines 450–464 reopen resolved concerns on a review schedule.

For example, a legal concern can be marked resolved after its timer expires without a changed agreement, named authority or safeguard being represented. An actor may object and stop the remedy; that is useful agency, but completion still does not require substantive legal work. A rule that automatically withdraws support can be a valid representation of an explicit institutional policy. It cannot simultaneously demonstrate that a recipient was influenced into withdrawing support.

The retained [November 4 run](../../evidence/declared-laws/s4-waltzman-3/run-log.jsonl) makes this concrete. In row 2, `r1-e00022` changes support from 5 to 1 after delivery, through `concern-makes-support-conditional`. In row 9, a reopened technical concern causes `r8-e00021` to reduce support from 4 to 3, followed by rejection at `r8-e00023`. Row 10 reopens the decision, so rejection is an intermediate event, not the final result.

Its [model calls](../../evidence/declared-laws/s4-waltzman-3/llm-calls.jsonl), rows 88 and 107, show a member first accepting a resolved legal status and later asking again for the actual legal safeguards. The prompt explicitly instructs residents to treat resolved status as substantive resolution. This is an intentionally coarse abstraction plus resident nonadherence, not simply an unnoticed stale-text bug. The model cannot answer the substantive question those residents are asking.

**Consequence:** plausible-looking coordination failure can arise from the stipulated procedure and mismatched abstractions. It does not yet isolate the paper's social mechanism. **Cheapest resolution:** make the automatic transition an explicit scenario assumption; test a version where recipients can dismiss, investigate, accept or act on the concern, and where a remedy changes the relevant represented condition.

**2. Open-ended authoring and action remain bounded by what the implementation already knows how to express.**

Counterevidence matters: the newer [people-world path](../../scripts/people_world.py) does have individual profiles and briefs, information items and scheduled moments. It would be wrong to repeat the older ODD table as proof that these are universally absent. The current source also permits natural-language attempts and visible refusals.

However, [run_authored_world.py](../../scripts/run_authored_world.py), lines 574–580, maps those attempts into installed action kinds; [attempt.py](../../src/world_substrate/attempt.py), lines 109–124, marks an absent kind unmatched. This live route does not implement the offline experiment's general mid-run law invention. Moreover, `assemble_people_world` preserves the compiler's ownership of concern/decision state and removes generated actions whose effects were entirely discarded (lines 424–460). The generator cannot freely replace that procedural model merely by describing a different social situation.

This is not a demand for infinite actions or universal physics. The problem is the missing product-level answer to an ordinary novel interaction that matters to the user's question. A refusal is honest; repeatedly authoring a bespoke extension afterward is not yet a general simulator.

**Consequence:** new labels and generated peripheral actions can conceal reuse of the same central situation shape. **Cheapest resolution:** expose the modeling boundary and use a deliberately different scenario, including a mixed social/material dependency, to test transfer without edits to scenario-specific compiler code. Test one meaningful new relationship or capability arising during execution; either support it or clearly narrow the claim.

**3. The checks increasingly establish activity and lawful execution rather than explanatory adequacy.**

The [roadmap](../../roadmap/README.md) explicitly defers generality and predictive behavioral validity from the promoted slice. Deferring prediction is appropriate. Deferring proof of generality is also legitimate for a first demo, but then that demo cannot settle the main product question.

The more revealing mismatch is [people_world.py](../../scripts/people_world.py), lines 114–157: guidance requires people to keep acting, reversals to remain possible, and post-deployment activity to continue. Compiler comments record reviews and agenda mechanics added when residents reasonably waited after completion. Activity can be an intentional world requirement, but a high count of moves does not distinguish meaningful adaptation from repetitive administrative work. Conversely, justified waiting can be correct behavior.

The existing tests accurately verify the stipulated procedure. They are useful engineering evidence; their passing cannot establish the realism or relevance of the assumptions they encode. The [earlier lineage review](cybernetic-influence-lineage-review.md#causal-closure-the-central-shared-research-problem) already identified the same problem through cargo transport that ignored fuel, trucks or customs despite locally valid effects.

**Consequence:** fixing each disappointing trajectory by adding a rule or guidance sentence can improve the next demonstration while reducing its ability to surprise or challenge the theory. **Cheapest resolution:** state the analyst's question and discriminating outcomes before authoring; keep that desired finding out of resident/adjudicator prompts; treat missing consequential dependencies as modeling failures rather than merely adding more activity.

### What Waltzman's paper should contribute

*From Minds to Coordination* describes plausible local interactions accumulating into collective coordination effects, including heterogeneous adaptive pressure and defenses that detect, diagnose and stabilize decision conditions. It also considers intermittent pressure and apparently legitimate contextual events. It supplies a conceptual hypothesis, not fitted behavioral equations or validated detectors. See the repository's [paper source note](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/446fd57191614be1284655fa8970cf547783df6b/docs/research/001-from-minds-to-coordination.md) and [paper-fidelity analysis](https://github.com/BrianMills2718/cybernetic_influence_v3/blob/446fd57191614be1284655fa8970cf547783df6b/docs/research/paper-fidelity-gap-analysis-2026-09-14.md); supplied PDF pages 2–3, 5–7, 10–17.

Use the paper to choose questions and stress situations. Do not turn its analytic vocabulary into universal world variables, or make delay automatically mean manipulation and approval automatically mean success. Genuine adverse evidence can justify delay. Effective stabilization can result in informed refusal.

There is promising prior work to preserve: the September fidelity analysis describes a larger resource-intervention fork where resources did not restore coordination and the concerns changed. Those complete traces were not re-read here, so this is a candidate for comparison, not independently confirmed evidence. Do not conclude that all prior work is empty or that the newest implementation is necessarily the strongest demonstration.

### Recommendations

1. **Restore the product's acceptance criterion.** A bounded situation should be instantiated through the ordinary authoring path, with inspectable assumptions and consequential interactions, without a new bespoke compiler family. Keep the governed-rules repository narrow; judge the assembled product separately.
2. **Keep selective exactness.** Use exact mechanics for inventories, identity, permissions, commitments and explicit procedures when they matter. Use bounded, recorded judgment for uncertain social interpretation where a trustworthy mechanistic model is unavailable. Any adjudicated effects must still be typed, scoped, validated and attributable. This is a proposed amendment to the rules-only boundary, not an instruction already authorized by this review.
3. **Separate what actors believe from what exists and what institutions require.** A communicated concern is evidence to a recipient; an institutional hold is a procedural rule; a modeled repair changes the relevant world condition. Do not make one status field silently stand for all three. Keep trust/risk/readiness as optional interpretations unless a scenario explicitly installs a justified causal model of them.
4. **Compare on the same cases before replacing anything.** Start with the existing coordination situation and one materially different situation, such as a transport operation where a damaged bridge, permissions, communication and actor commitments interact. Within the coordination case distinguish ordinary disagreement, genuine adverse evidence and adaptive pressure. Outcomes must remain open, including pressure failing and caution being justified. This is a proposed coverage set, not a claim about statistically sufficient sample sizes.
5. **Use the simplest adequate baseline.** Give a plain model the complete bounded scenario, actor-local context for each decision, and an explicit event/state ledger; validate its proposed changes. Compare with today's generated-rule path. The decision is whether extra authoring and enforcement stages improve consequential consistency enough to justify their constraints. Do not infer superiority from a framework name or a passing schema check.
6. **Allow model evolution deliberately.** Exploratory play may admit a recorded ruling or a versioned new rule when an important interaction is missing. Comparative experiments should freeze the model or restart compared branches under the same revision. Otherwise the model changes in response to the outcome it is supposed to explain.

Before a comparison is run, specify the question, the expected causal dependencies, what result would count against each approach, and read the complete traces of every decisive case. No provider budget or runtime estimate is asserted here; measure a single complete case before approving a batch.

**Keep:** canonical identity/state, scoped effects, atomic refusal, evidence retention, actor-local observations, scenario review, analysis separation, and existing worlds as regression examples. **Reconsider:** universal rules-only consequence authority, fixed social workflow families presented as general social mechanics, and motion/activity as a fidelity criterion. **Do not build yet:** another engine, a larger ontology, more overlays, or another sequence of scenario-specific repairs.

### Questions to resolve through the comparison

The first is substantive: what should be possible to learn from a run that the author did not already write into it? The second is architectural: which consequences need exact mechanics for that learning to be credible, and which need inspectable judgment? The third is practical: can the same path instantiate a different situation without code changes?

My recommendation is to answer those through the bounded comparison above. Do not make broad prediction or empirical calibration the next gate; that would demand a different product from the one originally sought. Do require enough representational fidelity that an apparent finding cannot be explained merely by a hard-coded outcome or a missing interaction.

### Evidence boundary and verification

- Current code: World Substrate `57199831e4f258adcb9048cbb5d07f39136e6924`; donor documents: V3 `446fd57191614be1284655fa8970cf547783df6b`.
- History: relevant commits and accepted decisions inspected; original CI/V2 contents were not independently reconstructed. Wargame is adjacent prior art, not proven ancestry. This is a selected lineage, not an exhaustive archive history.
- Primary intent: original statements were checked separately against the committed decision records. Private transcript text is not reproduced here.
- Paper: all 19 pages of the supplied PDF read; its SHA-256 matches repository provenance. No claim of calibrated predictive validity follows from it.
- Retained run: November 4, deployed revision `096c129`, distinct from current HEAD. All 12 server rows and 216 model-call records were parsed; the consequential engine changes, resident responses and decisive legal-reopening prompt were inspected. This is bounded causal-path evidence, not a full semantic certification of every duplicated prompt/schema in the bundle and not a success-rate audit.
- Current automatic support withdrawal and timed remedy behavior reproduced without model calls using the existing `GroupDecisionTests` in `tests/test_scenario_spec.py`: `python -m pytest tests/test_scenario_spec.py -k 'an_open_concern_makes_a_full_supporters_support_conditional_by_rule or the_person_a_concern_reached_can_resolve_it_on_their_own_side or support_waits_on_a_received_concern_and_returns_once_it_is_resolved' -q -p no:cacheprovider` returned **3 passed, 47 deselected, exit 0**. This establishes implementation behavior, not behavioral validity.
- No implementation, active product decision, deployment or model behavior is changed by this review. Recommendations remain proposals.
