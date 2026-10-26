# Catalog

Every reader document in this repository that the [wiki index](index.md) does not already link, grouped by folder. Titles are each file's own first heading. Add a line here when you add a document a reader should find.

## docs

- [World Builder visual and usability feedback](../docs/VISUAL_FEEDBACK.md)

## docs/audits

- [Castaway zero-review scene portability](../docs/audits/castaway-zero-review.md)
- [Greenhouse fourth-world authoring proof](../docs/audits/greenhouse-authoring-proof.md)
- [Kitchen zero-review replay breadth proof](../docs/audits/kitchen-zero-review.md)
- [Living Scene embodied renderer first gate](../docs/audits/living-scene-embodied-renderer.md)
- [Living Scene information and outcome feedback gate](../docs/audits/living-scene-information-feedback.md)
- [M2 audit: the M1 `give` path against the proposed contracts](../docs/audits/m2-give-path-audit.md)
- [M3: the first offline mechanics-authoring experiment](../docs/audits/m3-overheat-authoring-experiment.md)
- [M4: an honestly-authored mechanic, and where the assays go quiet](../docs/audits/m4-spill-experiment.md)
- [M5: a policy drives the world](../docs/audits/m5-policy-consumer.md)
- [M6: a second world, and what "substrate" actually meant](../docs/audits/m6-second-world.md)
- [M7: can an agent author a mechanic it was not handed?](../docs/audits/m7-authoring-rate.md)
- [M7b: was the triviality the model's, or the language's?](../docs/audits/m7b-relational-authoring.md)
- [Native Waltzman first-release static readiness review](../docs/audits/native-waltzman-release-static-readiness-2026-09-19.md)
- [Explicit action-presentation bindings](../docs/audits/scene-action-presentation-bindings.md)
- [Scene-profile presentation auto-layout](../docs/audits/scene-profile-auto-layout.md)
- [Scene-profile bootstrap experiment](../docs/audits/scene-profile-bootstrap.md)
- [Waltzman Kitchen-quality living-world v2](../docs/audits/waltzman-kitchen-quality-v2.md)
- [Waltzman Living Replay v1 integration evidence](../docs/audits/waltzman-living-replay-v1.md)
- [Waltzman Living Scene v1 composition evidence](../docs/audits/waltzman-living-scene-profile-v1.md)
- [Waltzman M1 living-world acceptance — automated evidence](../docs/audits/waltzman-m1-acceptance-2026-09-09.md)
- [Warehouse Rush live-authoring experiment](../docs/audits/warehouse-rush-preflight.md)
- [Workshop scene-profile greenfield proof](../docs/audits/workshop-scene-greenfield.md)
- [Visual/schema world authoring builder](../docs/audits/world-authoring-builder.md)
- [Code-first world authoring starter](../docs/audits/world-authoring-starter.md)
- [World Replay Studio product surface](../docs/audits/world-replay-studio.md)

## docs/contracts

- [Composed Living Scene presentation](../docs/contracts/composed-living-scene-v1.md)
- [CVS Situation IR structural import v0](../docs/contracts/cvs-situation-import-v0.md)
- [Living Scene v1](../docs/contracts/living-scene-v1.md)
- [Mechanic profile contract v0](../docs/contracts/mechanic-profile-v0.md)
- [Native coordination one-shot authoring v0](../docs/contracts/native-coordination-authoring-v0.md)
- [Native coordination comparison v0](../docs/contracts/native-coordination-comparison-v0.md)
- [Native coordination diagnostic bundle v0](../docs/contracts/native-coordination-diagnostics-v0.md)
- [Read-scope enforcement contract v0](../docs/contracts/read-scope-enforcement-v0.md)
- [Transition envelope contract v0](../docs/contracts/transition-envelope-v0.md)

## docs/decisions

- [Decision 008: Build worlds inside an agent harness, not with bare LLM calls](../docs/decisions/008-build-worlds-in-an-agent-harness.md)
- [Decision 009: Same-moment knock-on effects are rule semantics, not new engine capability](../docs/decisions/009-same-moment-knock-on-effects.md)

## docs/experiments

- [Repair Bay mechanics review — blinded packet v0](../docs/experiments/repair-bay-review-blind-v0.md)

## docs/planning

- [Cold review of the planning package](../docs/planning/cold-review.md)
- [Cold review: open-attempt planning package](../docs/planning/open-attempt/cold-review.md)

## docs/plans

- [Goal: residents say in their own words what they physically try (open-attempt /goal launcher)](../docs/plans/open-attempt.goal.md)
- [Goal: Prove the Decision 007 describe-any-scenario path end to end in world-substrate: plain-language scenario -> checked model -> LLM residents on Concordia with the World Substrate Engine as sole consequence authority -> attempts resolved over time -> game master writes checked rules mid-run -> structured changes rendered as living-scene frames.](../docs/plans/any-scenario-poc.goal.md)
- [Plan: describe-any-scenario proof of concept (Decision 007)](../docs/plans/any_scenario_poc.md)
- [Goal: Best of all worlds — one box, rich people, exact rules, live](../docs/plans/best-of-all-worlds.goal.md)
- [Goal: World Substrate processes can change linked entities in one atomic transition: a process names participants resolved from its own entity (ownership, an entity_ref field, or shared location), so the truck's driver moves with the truck and a dying patient frees the ventilator and bed, proven on the generated truck and hospital worlds.](../docs/plans/linked-process-participants.goal.md)
- [Plan: linked participants for processes (Decision 007 follow-up)](../docs/plans/linked_process_participants.md)
- [Plan: open attempts, knock-on effects that run to the end, and skill rolls](../docs/plans/open_attempt.md)
- [Goal: no round runs or bills twice, and a run's record says why each move was refused](../docs/plans/run-loop-contention.goal.md) (superseded 2026-10-26 by open_attempt.md)
- [Goal: Every actor a scenario names reaches the generated world as an autonomous agent with a role brief taken from the scenario text, so that Rand Waltzman's scenario, rerun through the any-scenario pipeline, has the technical, legal, logistics and community groups acting in it; a fresh assessment states with event-level evidence which of the paper's four mechanisms now appear.](../docs/plans/scenario-actors-kept.goal.md)
- [Goal: The describe-any-scenario pipeline defines each world in a typed scenario spec ported from Cybernetic Influence v3's world schema (people with behavioral profiles, information items with a source, channel and recipients, scheduled moments, world records with visibility, and a coverage report), compiles it into World Substrate state using the existing information module and the reviewed communicate rule, briefs each agent with its own person profile, and reruns Rand Waltzman's scenario with a fresh assessment of the paper's four mechanisms.](../docs/plans/scenario-spec-adoption.goal.md)
- [Plan: keep every actor a scenario names, and brief each with its role](../docs/plans/scenario_actors_kept.md)
- [Plan: define generated worlds in Cybernetic Influence's scenario schema](../docs/plans/scenario_spec_adoption.md)
- [Goal: The checked system model in docs/model/ covers what it left out: the describe-any-scenario pipeline (its steps, records, views and evidence), information items (src/world_substrate/information.py) and linked process participants, with a list of the kinds of things a world can represent and which path produces each, and a comparison with Cybernetic Influence v3's world schema.](../docs/plans/system-model-pipeline.goal.md)
- [Goal: Waltzman, attempts from belief, and read traces](../docs/plans/waltzman-belief-and-traces.goal.md)
- [Goal: Rand Waltzman's bio-surveillance coordination scenario, typed as plain text, runs end to end through the any-scenario pipeline (checked model, AI members on Concordia with the World Substrate Engine as sole consequence authority, game master writing checked rules mid-run, replay frames), and a short plain-language assessment states, with event-level evidence, which of the paper's four mechanisms the generated world represents and which it misses.](../docs/plans/waltzman-scenario-run.goal.md)
- [Goal: tasks that can really fail part-way (#128, second slice)](../docs/plans/waltzman-tasks-slice2.goal.md)
- [Plan: run Waltzman's scenario through the any-scenario pipeline](../docs/plans/waltzman_scenario_run.md)

## docs/research

- [Agent Ecology 2 — Targeted Review for World Substrate](../docs/research/agent-ecology2-review.md)
- [Cybernetic Influence Lineage Review for World Substrate](../docs/research/cybernetic-influence-lineage-review.md)
- [World Substrate discussion traceability](../docs/research/discussion-traceability.md)
- [Prior art for a flexible world simulator (2026-10)](../docs/research/flexible-simulator-prior-art-2026-10.md)
- [Formal simulation and agent theory: prior art survey (scope: formal)](../docs/research/flexible-simulator-prior-art-2026-10/formal.md)
- [Games and interactive fiction survey: prior art for a flexible world simulator](../docs/research/flexible-simulator-prior-art-2026-10/games.md)
- [LLM-agent simulation platforms 2023-2026: prior-art survey (scope: llm-sims)](../docs/research/flexible-simulator-prior-art-2026-10/llm-sims.md)
- [Jev-inspired ideas for non-cognitive world modeling](../docs/research/jev-world-modeling-exploration-2026-09.md)
- [Off-the-shelf candidates to evaluate (2026-09-25)](../docs/research/off-the-shelf-candidates-2026-09-25.md)
- [Research synthesis](../docs/research/synthesis.md)
- [Living-world UI references — 2026-09-09](../docs/research/ui-references/README.md)
- [World Substrate Theory and Strategy — Working Memo](../docs/research/world-substrate-strategy-session.md)

## evidence/best-of-all-worlds

- [Every Waltzman test run, test service wb-stance-test (2026-10-16)](../evidence/best-of-all-worlds/RUNS.md)

## evidence/m1

- [M1 freshwater review](../evidence/m1/freshwater-v0.md)

## evidence/waltzman

- [Waltzman stakeholder promotion evidence — 2026-09-09](../evidence/waltzman/public-promotion-2026-09-09.md)

## evidence/waltzman-belief-and-traces

- [Trace read: c1r18](../evidence/waltzman-belief-and-traces/c1r18/TRACE_READ.md)
- [Trace read: c1r19](../evidence/waltzman-belief-and-traces/c1r19/TRACE_READ.md)
- [Trace read: c1r20](../evidence/waltzman-belief-and-traces/c1r20/TRACE_READ.md)
- [Trace read: c4-run21](../evidence/waltzman-belief-and-traces/c4-run21/TRACE_READ.md)
- [C5 at 9bfa8d3 (2026-10-23)](../evidence/waltzman-belief-and-traces/c5-9bfa8d3/README.md)

## evidence/waltzman-tasks-slice2

- [Trace read: c1r21](../evidence/waltzman-tasks-slice2/c1r21/TRACE_READ.md)
- [Trace read: c1r22](../evidence/waltzman-tasks-slice2/c1r22/TRACE_READ.md)
- [Trace read: c1r23](../evidence/waltzman-tasks-slice2/c1r23/TRACE_READ.md)
- [Trace read: c1r24](../evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md)

## reference_worlds

- [Reference worlds](../reference_worlds/README.md)

## reference_worlds/cvs_sustainment

- [CVS sustainment integration world](../reference_worlds/cvs_sustainment/README.md)

## scripts/e2e

- [World Builder checks that cost real model money](../scripts/e2e/README.md)

## spikes/replacement-2026-10

- [Replacement-first spike: Concordia (gdm-concordia 2.4.0)](../spikes/replacement-2026-10/concordia/README.md)
- [Replacement spike: Mesa (constrained-handoff)](../spikes/replacement-2026-10/mesa/README.md)
- [Replacement-first spike: PDDL toolchain (2026-10-05)](../spikes/replacement-2026-10/pddl/README.md)

## evidence/open-attempt

- [Trace read: first S1 owner run on the airfield (scripted moves, no residents)](../evidence/open-attempt/s1-airfield-scripted/TRACE_READ.md)
- [Trace read: S1 live airfield run with AI residents](../evidence/open-attempt/s1-airfield/TRACE_READ.md)
- [Q23: do generated moves check walls? (2026-10-25)](../evidence/open-attempt/q23/README.md)
- [Q28: can generated worlds reuse the library damage processes? (2026-10-26)](../evidence/open-attempt/q28/README.md)

## evidence/model-more

- [Model more: money, prices, distances and delivery time (2026-10-26)](../evidence/model-more/README.md)
