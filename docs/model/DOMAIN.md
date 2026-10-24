---
description: Domain model of World Substrate: the ideas it is about, which are fixed code and which an AI writes per world.
---

# World Substrate domain model

The graph is [domain.graph.json](domain.graph.json) (Representation Router `typed-graph/v1`). This page is its glossary.
The model's main job is to keep two levels apart: **the substrate** (code every world runs through) and **one world** (what an AI writes for a described world, or the hand-written Waltzman reference). A problem is a substrate problem when the concept it lives in is one of the first two kinds below.

## Substrate code (every world)

Fixed code every world runs through: the Engine, compiler, run loop, service, records.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **World** (`world`) | The one canonical world during a run: entities with typed components, a tick and a revision. | `docs/model/ODD.md:112` | `src/world_substrate/engine.py` |
| **Engine** (`engine`) | Applies each attempt atomically or refuses it with a recorded reason; runs due processes each tick. | `docs/model/ODD.md:227` | `src/world_substrate/engine.py:558` |
| **Event** (`event`) | The record of one attempt or process step: status, checks, changes, an id like r14-e00012. | `docs/model/ODD.md:236` | `src/world_substrate/engine.py:505` |
| **Move (action)** (`move`) | Something a person may try; its rule has checks and effects, compiled before use. | `docs/model/ODD.md:108` | `src/world_substrate/action_authoring.py:367` |
| **Process** (`process`) | A rule the world runs by itself each tick when its checks hold. | `docs/model/ODD.md:184` | `src/world_substrate/engine.py:762` |
| **Compiler** (`compiler`) | Turns proposed rules into installed rules and derives what each may read and write. | `docs/model/ODD.md:238` | `src/world_substrate/action_authoring.py:367` |
| **Approval record** (`approval`) | A person's yes to the rules, stored with the rules' profile id and world fingerprint; every round names it. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:418` |
| **World fingerprint** (`fingerprint`) | A short hash of the bundle and rules that ties builds, rounds and shares to one world. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:381` |
| **Information item** (`information`) | A piece of information with a source and per-recipient deliveries; hidden until delivered. | `docs/model/ODD.md:260` | `src/world_substrate/information.py:57` |
| **Run loop** (`run-loop`) | Each round: everyone decides, picks are submitted in a rotating order, then processes run. | `docs/model/ODD.md (11.3)` | `scripts/run_authored_world.py:460` |
| **Lost race** (`contention`) | When an earlier pick changed the state, a later pick is resubmitted or re-chosen once; if nothing is left the person gets nothing_left and is not told why. | `docs/model/ODD.md (11.3)` | `scripts/run_authored_world.py:536` |
| **Resident** (`resident`) | One Concordia AI agent per person: sees its brief, memory and what it can see, answers belief, move, expected effect and work. | `docs/model/ODD.md (11.3)` | `scripts/concordia_residents.py:29` |
| **Task** (`task`) | A watched field value that takes several rounds, started by a person or the world, ended by a process: finished or failed part-way. | `docs/model/ODD.md (11.4)` | `scripts/attempts.py:17` |
| **Finished-task notice** (`notice`) | What the other people a finished task names are told, in the starter's own words about the work. | `docs/model/ODD.md (11.4)` | `scripts/attempts.py:234` |
| **Build** (`build`) | Description to spec, actions, rules, assembly, scripted test run and score. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:1538` |
| **Rules retry** (`rules-retry`) | A second rules attempt after a rejection or weak score; skipped after 80 s. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:263` |
| **Scripted test run** (`test-run`) | The build's free run with simple moves that scores the rules and lists long tasks and whether each can fail part-way. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:1607` |
| **Run log** (`run-log`) | One line per request with its trace ids, cost and full artifacts; the source for shares and trace reads. | `docs/model/ODD.md:254` | `scripts/world_builder_service.py:478` |
| **Readout** (`readout`) | One AI summary of a run whose every cited event id is checked against the run. | `docs/model/ODD.md (11.5)` | `scripts/run_readout.py:125` |
| **Share link and replay** (`share`) | A saved run rebuilt from the run log that a visitor replays with no AI calls. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:598` |
| **Daily allowance** (`budget`) | Visitor $3/day, owner $5/day; spend fails closed. | `docs/model/ODD.md:252` | `scripts/world_builder_service.py:51` |

## Fixed people-world part

Fixed code every people world gets from compile_spec.py; the group-decision family is added when the description has a decision.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **People world** (`people-world`) | A world built from a description about people: people, information, moments and the fixed people rules. | `docs/decisions/008-build-worlds-in-an-agent-harness.md` | `scripts/people_world.py:225` |
| **Communicate rule** (`communicate`) | The reviewed move that delivers an information item to its recipient. | `docs/model/ODD.md:277` | `spikes/any-scenario-2026-10/compile_spec.py` |
| **Scheduled moment** (`moment`) | A countdown that happens every so many rounds (a weekly meeting, a deadline). | `docs/model/ODD.md:278` | `spikes/any-scenario-2026-10/compile_spec.py:48` |
| **Work cycle** (`work-cycle`) | Each action at most once per person per cycle of at least 3 rounds. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:517` |
| **Group decision** (`group-decision`) | A decision with support, deadline, deployment and review; changed only by fixed rules. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:86` |
| **Concern** (`concern`) | An objection a group holds on a delivered item: open, under remedy or resolved, with answered and remedy_by. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:70` |
| **Support** (`support`) | A member's stance on the decision: none, full or conditional on a concern. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:66` |
| **Remedy** (`remedy`) | A fix of a concern that takes 2 rounds; it can be stopped part-way by the concern's holder objecting. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:332` |
| **Agenda count** (`agenda`) | group_decision.agenda_items: a bare number of matters put before the decision; an item has no content. | `docs/model/ODD.md (11.1)` | `scripts/people_world.py:279` |
| **Rollout** (`rollout`) | The deployment the world starts when the decision is authorized: 6 rounds, suspended if support falls. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:399` |
| **Operating review** (`review`) | Every 6 rounds after deployment; may reopen each resolved concern once. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:442` |

## Written per world by an AI

Not code: an AI writes it for each described world during the build.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **Person and brief** (`person`) | A person the spec names, with goals and beliefs, and the brief only their own resident reads. | `docs/model/ODD.md:276` | `scripts/people_world.py:355` |
| **Generated actions and rules** (`gen-rules`) | The moves and processes the fixed parts do not cover, written by the rules-writing AI and compiled. | `docs/model/ODD.md (11.1)` | `scripts/people_world.py:260` |

## Waltzman reference code only

Hand-written code for the Waltzman reference world; no generated world uses it.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **Waltzman reference components** (`waltzman-ref`) | Trust, risk, readiness and commitment components and analyses of the hand-written Waltzman world. | `docs/wiki/README.md` | `reference_worlds/waltzman/components.py:11` |

## In documents only

Named in decisions or the roadmap, not on the live path.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **Build in an agent harness** (`harness-build`) | Decision 008: worlds built by an agent that drafts, checks and edits; scripts/world_harness.py exists but the live service does not call it. | `docs/decisions/008-build-worlds-in-an-agent-harness.md:48` | `scripts/world_harness.py` |
| **Executable-law fingerprint** (`law-fingerprint`) | Roadmap hardening item: fingerprint the exact executable law and compiler version. | `roadmap/README.md:359` | `—` |

## Where the sources disagree

1. **Decision 008 versus the live build.** Decision 008 says worlds are built in an agent harness that drafts, checks and edits; the live service builds with fixed calls and a rules retry and does not import `scripts/world_harness.py` (open question Q14).
2. **The wiki's 'Concepts and terminology' versus this model.** The wiki (`docs/wiki/README.md`) defines engine-level terms only; people, concerns, support, tasks and residents are defined here and in ODD section 11, not there.
