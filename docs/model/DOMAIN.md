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
| **World** (`world`) | The one canonical world during a run: entities with typed components, a tick and a revision. | `docs/model/ODD.md:112` | `src/world_substrate/model.py:382` |
| **Engine** (`engine`) | Applies each attempt atomically or refuses it with a recorded reason; runs due processes each tick. | `docs/model/ODD.md:227` | `src/world_substrate/engine.py:198` |
| **Event** (`event`) | The record of one attempt or process step: status, checks, changes, an id like r14-e00012. | `docs/model/ODD.md:236` | `src/world_substrate/engine.py:529` |
| **Move (action)** (`move`) | Something a person may try; its rule has checks and effects, compiled before use. | `docs/model/ODD.md:108` | `src/world_substrate/action_authoring.py:49` |
| **Process** (`process`) | A rule the world runs by itself when its checks hold: each round by default, or at once as a knock-on effect when marked immediately. | `docs/model/ODD.md:184` | `src/world_substrate/engine.py:829` |
| **Compiler** (`compiler`) | Turns proposed rules into installed rules and derives what each may read and write. | `docs/model/ODD.md:238` | `src/world_substrate/action_authoring.py:456` |
| **Policy** (`policy`) | What chooses a person's move: scripted or an AI model picks an offered move; a resident on the live path says an attempt in its own words. Installed mechanics, not its words, decide what happens. | `README.md:5` | `src/world_substrate/policy.py:50` |
| **Linguistic Core sense and roles** (`sense`) | The meaning and participant roles of a move kind, supplied by Linguistic Core; never its effects, quantities or timing. | `README.md:113` | `src/world_substrate/semantic.py:15` |
| **Frozen mechanic profile** (`profile`) | The validated, installed rules of a world, frozen under one id before any run; changing a rule means a new profile. | `docs/model/ODD.md:240` | `src/world_substrate/profile.py:266` |
| **Declared write scope** (`write-scope`) | The fields a rule says it may change; the Engine refuses any change outside them. Read scopes are recorded, not enforced. | `AGENTS.md:21` | `src/world_substrate/engine.py:88` |
| **Causal trace** (`causal-trace`) | The retained chain of events of a run, each naming the move or process, its checks and its changes; the evidence for any claim about a run. | `README.md:73` | `src/world_substrate/engine.py:529` |
| **World kind** (`world-kind`) | Two choices a build makes first: whether the description is about people (people path) or things (causal path), and whether the world is a task, ongoing or open. | `docs/model/ODD.md:106` | `scripts/world_builder_service.py:113` |
| **World Builder and its bundle** (`builder`) | The public page and service where a person describes a world, approves its rules and watches it run; a build's output is an authoring bundle. | `docs/model/ODD.md:70` | `scripts/world_builder_service.py` |
| **Approval record** (`approval`) | A person's yes to the rules, stored with the rules' profile id and world fingerprint; every round names it. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:418` |
| **World fingerprint** (`fingerprint`) | A short hash of the bundle and rules that ties builds, rounds and shares to one world. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:381` |
| **Information item** (`information`) | A piece of information with a source and per-recipient deliveries; hidden until delivered. | `docs/model/ODD.md:260` | `src/world_substrate/information.py:57` |
| **Run loop** (`run-loop`) | Each round: everyone decides, picks are submitted in a rotating order, then processes run. | `docs/model/ODD.md (11.3)` | `scripts/run_authored_world.py:347` |
| **Lost race** (`contention`) | When an earlier move this round changed the state, an open attempt is resubmitted as is at the new revision and only its rule's checks decide it; menu paths resubmit the move if still offered, else ask once more. The refused row names the failed checks, not the event that blocked it. | `docs/model/ODD.md (11.3)` | `scripts/run_authored_world.py:563` |
| **Resident** (`resident`) | One Concordia AI agent per person: sees its brief, memory and what it can see, and answers belief, attempt (in its own words), expected effect and work; the older menu reply picks an offered move. | `docs/model/ODD.md (11.3)` | `scripts/concordia_residents.py:44` |
| **Task** (`task`) | A watched field value that takes several rounds, started by a person or the world, ended by a process: finished or failed part-way. | `docs/model/ODD.md (11.4)` | `scripts/attempts.py:17` |
| **Finished-task notice** (`notice`) | What the other people a finished task names are told, in the starter's own words about the work. | `docs/model/ODD.md (11.4)` | `scripts/attempts.py:234` |
| **Build** (`build`) | Description to spec, actions, rules, assembly, scripted test run and score. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:1541` |
| **Rules retry** (`rules-retry`) | A second rules attempt after a rejection or weak score; skipped after 80 s. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:263` |
| **Scripted test run** (`test-run`) | The build's free run with simple moves that scores the rules and lists long tasks and whether each can fail part-way. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:1610` |
| **Run log** (`run-log`) | One line per request with its trace ids, cost and full artifacts; the source for shares and trace reads. | `docs/model/ODD.md:254` | `scripts/world_builder_service.py:524` |
| **Readout** (`readout`) | One AI summary of a run whose every cited event id is checked against the run. | `docs/model/ODD.md (11.5)` | `scripts/run_readout.py:125` |
| **Scene replay** (`scene-replay`) | The page's round-by-round picture of a run: who did what and said what, rebuilt from the run rows; it already quotes a retry's own words. | `docs/model/ODD.md (11.5)` | `scripts/render_scene_replay.py:398` |
| **Share link and replay** (`share`) | A saved run rebuilt from the run log that a visitor replays with no AI calls. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:598` |
| **Daily allowance** (`budget`) | Visitor $3/day, owner $5/day; spend fails closed. | `docs/model/ODD.md:252` | `scripts/world_builder_service.py:51` |
| **Affordance (offered move)** (`affordance`) | A move the rules say a person can try now, with its open fields; the page a decider picks from or an attempt is read against. | `docs/plans/open_attempt.md:118` | `src/world_substrate/engine.py:352` |
| **Check** (`check`) | One condition on a move or process (actual versus required); a move commits only when every check holds, else the event records which failed. | `docs/model/ODD.md:229` | `src/world_substrate/rules.py:48` |
| **Attempt (in own words)** (`attempt`) | What a resident says it physically tries, in its own words, with no outcome field: the world, not the speaker, decides what happens. | `docs/model/ODD.md:348` | `src/world_substrate/attempt.py:149` |
| **Attempt reading** (`attempt-reading`) | The interpreter's typed reading of an attempt: one move kind and its field rows (field, value, quoted_span: the words in the attempt behind that value), or the kind 'wait'; read as unmatched if it names an unknown kind or entity, misses a field, or quotes words not said. | `docs/model/ODD.md:348` | `src/world_substrate/attempt.py:81` |
| **Unmatched attempt** (`unmatched-attempt`) | An attempt no move kind covers: it changes nothing, the person learns nothing came of it, and the run lists it for the rules writer. | `docs/model/ODD.md:351` | `src/world_substrate/attempt.py:25` |
| **Observation** (`observation`) | What one actor sees this round: the fields its senses and position allow, never the whole world. | `docs/model/ODD.md:207` | `src/world_substrate/engine.py:235` |
| **Knock-on that runs now** (`knock-on-now`) | A process marked 'immediately' runs in waves inside the same moment as the attempt or round step that set it off, until nothing more is due (a glass falls, breaks, the water spills, the neighbour hears it); each pair of process and thing fires once per moment, and more than 32 reactions refuses the whole moment. | `docs/model/ODD.md (8.20)` | `src/world_substrate/engine.py:884` |
| **Living projection** (`projection`) | The read-only living client, JSON and server-sent events rebuilt from canonical snapshots and events; it never changes the world. | `AGENTS.md:35` | `src/world_substrate/projection.py:44` |
| **Hard causal parent** (`causal-parent`) | An earlier event a rule declares as mechanically supporting this one; kept apart from the information a person merely had in mind. | `README.md:83` | `src/world_substrate/rules.py:383` |
| **Derived exchange** (`exchange`) | A composite reading (two give events make one exchange) derived from committed events, never a second effect. | `docs/contracts/transition-envelope-v0.md:42` | `src/world_substrate/exchange.py:68` |
| **Installed mechanic** (`mechanic`) | One installed action rule: an action kind's selector, checks, effects and derived reads and writes, compiled and frozen in the profile; the root rule says installed mechanics alone decide what happens. | `AGENTS.md:3` | `src/world_substrate/action_authoring.py:456` |
| **Entity and component** (`entity-component`) | An entity is one thing in the world (person, wall, glass, decision) with an id, a label, categories and typed components; a component is a named record of typed fields (boundary.passable, group_decision.status) that checks read and effects write. | `docs/model/ODD.md:100` | `src/world_substrate/model.py:223` |

## Fixed people-world part

Fixed code every people world gets from compile_spec.py; the group-decision family is added when the description has a decision.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **People world** (`people-world`) | A world built from a description about people: people, information, moments and the fixed people rules. | `docs/model/ODD.md:285` | `scripts/people_world.py:364` |
| **Communicate rule** (`communicate`) | The reviewed move that delivers an information item to its recipient. Spike code: it lives in spikes/any-scenario-2026-10/, which the live build loads through scripts/people_world.py:73. | `docs/model/ODD.md:277` | `spikes/any-scenario-2026-10/compile_spec.py:56` |
| **Scheduled moment** (`moment`) | A countdown that happens every so many rounds (a weekly meeting, a deadline). Spike code: it lives in spikes/any-scenario-2026-10/, which the live build loads through scripts/people_world.py:73. | `docs/model/ODD.md:278` | `spikes/any-scenario-2026-10/compile_spec.py:48` |
| **Work cycle** (`work-cycle`) | Each action at most once per person per cycle of at least 3 rounds. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:517` |
| **Group decision** (`group-decision`) | A decision with support, deadline, deployment and review; changed only by fixed rules. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:86` |
| **Concern** (`concern`) | An objection a group holds on a delivered item: open, under remedy or resolved, with answered and remedy_by. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:70` |
| **Support** (`support`) | A member's stance on the decision: none, full or conditional on a concern. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:66` |
| **Remedy** (`remedy`) | A fix of a concern that takes 2 rounds; it can be stopped part-way by the concern's holder objecting. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:332` |
| **Agenda count** (`agenda`) | group_decision.agenda_items: a bare number of matters put before the decision; an item has no content. Declared in the group-decision component and changed by the compiled put-matter-on-agenda and settle-agenda-matter rules. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:101` |
| **Rollout** (`rollout`) | The deployment the world starts when the decision is authorized: 6 rounds, suspended if support falls. Its processes (authorization-withdrawn, deployment-completes, deployment-suspended, deployment-resumes, deployment-progresses) are defined in _decision_rules. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:436` |
| **Operating review** (`review`) | Every 6 rounds after deployment; may reopen each resolved concern once. | `docs/model/ODD.md (11.1)` | `spikes/any-scenario-2026-10/compile_spec.py:442` |

## Written per world by an AI

Not code: an AI writes it for each described world during the build.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **Person and brief** (`person`) | A person the spec names, with goals and beliefs, and the brief only their own resident reads. | `docs/model/ODD.md:276` | `spikes/any-scenario-2026-10/scenario_spec.py:41` |
| **Generated actions and rules** (`gen-rules`) | The moves and processes the fixed parts do not cover, written by the rules-writing AI and compiled. | `docs/model/ODD.md (11.1)` | `scripts/people_world.py:251` |
| **Place and way** (`place-way`) | Where things are, and what lies between two places (a door, a brick wall) with whether it is passable; written per world as entities from the bundle contract, and the move rule checks the way. | `docs/model/ODD.md:327` | `scripts/generate_world_bundle.py:96` |

## Reference worlds code only

Hand-written code for the reference worlds (Kitchen, Waltzman and others); no generated world uses it today.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **Waltzman reference components** (`waltzman-ref`) | Trust, risk, readiness and commitment components and analyses of the hand-written Waltzman world. | `docs/wiki/README.md` | `reference_worlds/waltzman/components.py:11` |
| **Mechanisms library** (`mechanisms`) | Reusable hand-written rule families (liquid, ownership, thermal, damage, time) that reference worlds such as Castaway register (reference_worlds/castaway/overheat.py:14); generated worlds get only their compiled mechanics and processes (scripts/run_authored_world.py:58, Q28). | `src/world_substrate/mechanisms/__init__.py:1` | `src/world_substrate/mechanisms/__init__.py:3` |
| **Kitchen flagship** (`kitchen`) | The replicated scarce-knife watched world: hand-written rules of its own on the ordinary Engine. | `README.md:152` | `reference_worlds/kitchen/mechanics.py` |

## In documents only

Named in decisions or the roadmap, not on the live path.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **Build in an agent harness** (`harness-build`) | Decision 008: worlds built by an agent that drafts, checks and edits; scripts/world_harness.py exists but the live service does not call it. | `docs/decisions/008-build-worlds-in-an-agent-harness.md:48` | `scripts/world_harness.py` |
| **Executable-law fingerprint** (`law-fingerprint`) | Roadmap hardening item: fingerprint the exact executable law and compiler version. | `roadmap/README.md:252` | `—` |
| **Skill roll** (`skill-roll`) | Plan S3: a move's outcome depends on a seeded, recorded roll against the person's skill, so someone untrained who flies a helicopter can crash it. | `docs/plans/open_attempt.md:182` | `—` |
| **Run seed** (`run-seed`) | Plan S3: one seed drawn when a run starts and recorded in the run record; each roll's dice come from hash(run seed, event id) and are recorded, so a replay reads the dice and never rolls (Q33). | `docs/plans/open_attempt.md:192` | `—` |

## Where the sources disagree

1. **Decision 008 versus the live build.** Decision 008 says worlds are built in an agent harness that drafts, checks and edits; the live service builds with fixed calls and a rules retry and does not import `scripts/world_harness.py` (open question Q14).
2. **The wiki's 'Concepts and terminology' versus this model.** The wiki (`docs/wiki/README.md`) defines engine-level terms only; people, concerns, support, tasks and residents are defined here and in ODD section 11, not there.
