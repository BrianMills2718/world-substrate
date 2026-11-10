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
| **World** (`world`) | The one canonical world during a run: entities with typed components, a tick and a revision. | `docs/model/ODD.md:112` | `src/world_substrate/model.py:424` |
| **Engine** (`engine`) | Applies each attempt atomically or refuses it with a recorded reason; runs due processes each tick. | `docs/model/ODD.md:229` | `src/world_substrate/engine.py:222` |
| **Event** (`event`) | The record of one attempt or process step: status, checks, changes, an id like r14-e00012. | `docs/model/ODD.md:241` | `src/world_substrate/engine.py:572` |
| **Move (action)** (`move`) | Something a person may try; its rule has checks and effects, compiled before use. | `docs/model/ODD.md:108` | `src/world_substrate/action_authoring.py:50` |
| **Process** (`process`) | A rule the world runs by itself when its checks hold: each round by default, or at once as a knock-on effect when marked immediately. | `docs/model/ODD.md:186` | `src/world_substrate/engine.py:1095` |
| **Compiler** (`compiler`) | Turns proposed rules into installed rules and derives what each may read and write. | `docs/model/ODD.md:243` | `src/world_substrate/action_authoring.py:440` |
| **Policy** (`policy`) | What chooses a person's move: scripted or an AI model picks an offered move; a resident on the live path says an attempt in its own words. Installed mechanics, not its words, decide what happens. | `README.md:43` | `src/world_substrate/policy.py:50` |
| **Linguistic Core sense and roles** (`sense`) | The meaning and participant roles of a move kind, supplied by Linguistic Core; never its effects, quantities or timing. | `AGENTS.md:19` | `src/world_substrate/semantic.py:15` |
| **Frozen mechanic profile** (`profile`) | The validated, installed rules of a world, frozen under one id before any run; changing a rule means a new profile. | `docs/model/ODD.md:245` | `src/world_substrate/profile.py:249` |
| **Declared write scope** (`write-scope`) | The fields a rule says it may change; the Engine refuses any change outside them. Read scopes are recorded, not enforced. | `AGENTS.md:21` | `src/world_substrate/engine.py:136` |
| **Causal trace** (`causal-trace`) | The retained chain of events of a run, each naming the move or process, its checks and its changes; the evidence for any claim about a run. | `AGENTS.md:25` | `src/world_substrate/engine.py:572` |
| **World kind** (`world-kind`) | Two choices a build makes first: whether the description is about people (people path) or things (causal path), and whether the world is a task, ongoing or open. | `docs/model/ODD.md:106` | `scripts/world_builder_service.py:121` |
| **World Builder and its bundle** (`builder`) | The public page and service where a person describes a world, approves its rules and watches it run; a build's output is an authoring bundle. | `docs/model/ODD.md:70` | `scripts/world_builder_service.py` |
| **Approval record** (`approval`) | A person's yes to the rules, stored with the rules' profile id and world fingerprint; every round names it. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:426` |
| **World fingerprint** (`fingerprint`) | A short hash of the bundle and rules that ties builds, rounds and shares to one world. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:389` |
| **Information item** (`information`) | A piece of information with a source and per-recipient deliveries; hidden until delivered. | `docs/model/ODD.md:265` | `src/world_substrate/information.py:57` |
| **Run loop** (`run-loop`) | Each round: everyone decides, picks are submitted in a rotating order, then processes run. | `docs/model/ODD.md (11.3)` | `scripts/run_authored_world.py:700` |
| **Lost race** (`contention`) | When an earlier move this round changed the state, an open attempt is resubmitted as is at the new revision and only its rule's checks decide it; menu paths resubmit the move if still offered, else ask once more. The refused row names the failed checks, not the event that blocked it. | `docs/model/ODD.md (11.3)` | `scripts/run_authored_world.py:850` |
| **Resident** (`resident`) | One Concordia AI agent per person: sees its brief, memory and what it can see, and answers belief, attempt (in its own words), expected effect and work; the older menu reply picks an offered move. | `docs/model/ODD.md (11.3)` | `scripts/concordia_residents.py:44` |
| **Task** (`task`) | A watched field value that takes several rounds, started by a person or the world, ended by a process: finished or failed part-way. | `docs/model/ODD.md (11.4)` | `scripts/attempts.py:17` |
| **Finished-task notice** (`notice`) | What the other people a finished task names are told, in the starter's own words about the work. | `docs/model/ODD.md (11.4)` | `scripts/attempts.py:234` |
| **Build** (`build`) | Description to spec, actions, rules, assembly, scripted test run and score. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:1635` |
| **Rules retry** (`rules-retry`) | A second rules attempt after a rejection or weak score; skipped after 80 s. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:110` |
| **Scripted test run** (`test-run`) | The build's free run with simple moves that scores the rules and lists long tasks and whether each can fail part-way. | `docs/model/ODD.md (11.2)` | `scripts/world_builder_service.py:1844` |
| **Run log** (`run-log`) | One line per request with its trace ids, cost and full artifacts; the source for shares and trace reads. | `docs/model/ODD.md:259` | `scripts/world_builder_service.py:542` |
| **Readout** (`readout`) | One AI summary of a run whose every cited event id is checked against the run. | `docs/model/ODD.md (11.5)` | `scripts/run_readout.py:113` |
| **Scene replay** (`scene-replay`) | The page's round-by-round picture of a run: who did what and said what, rebuilt from the run rows; it already quotes a retry's own words. | `docs/model/ODD.md (11.5)` | `scripts/render_scene_replay.py:449` |
| **Share link and replay** (`share`) | A saved run rebuilt from the run log that a visitor replays with no AI calls. | `docs/model/ODD.md (11.5)` | `scripts/world_builder_service.py:638` |
| **Daily allowance** (`budget`) | Visitor $3/day, owner $5/day; spend fails closed. | `docs/model/ODD.md:257` | `scripts/world_builder_service.py:57` |
| **Affordance (offered move)** (`affordance`) | A move the rules say a person can try now, with its open fields; the page a decider picks from or an attempt is read against. | `docs/plans/open_attempt.md:118` | `src/world_substrate/engine.py:395` |
| **Check** (`check`) | One condition on a move or process (actual versus required); a move commits only when every check holds, else the event records which failed. | `docs/model/ODD.md:231` | `src/world_substrate/rules.py:48` |
| **Attempt (in own words)** (`attempt`) | What a resident says it physically tries, in its own words, with no outcome field: the world, not the speaker, decides what happens. | `docs/model/ODD.md:356` | `src/world_substrate/attempt.py:221` |
| **Attempt reading** (`attempt-reading`) | The interpreter's typed reading of an attempt: one move kind and its field rows (field, value, quoted_span: the words in the attempt behind that value), or the kind 'wait'; read as unmatched if it names an unknown kind or entity, misses a field, or quotes words not said. | `docs/model/ODD.md:356` | `src/world_substrate/attempt.py:92` |
| **Unmatched attempt** (`unmatched-attempt`) | An attempt no move kind covers: it changes nothing, the person learns nothing came of it, and the run lists it for the rules writer. | `docs/model/ODD.md:359` | `src/world_substrate/attempt.py:34` |
| **Observation** (`observation`) | What one actor sees this round: the fields its senses and position allow, never the whole world. | `docs/model/ODD.md:209` | `src/world_substrate/engine.py:278` |
| **Knock-on that runs now** (`knock-on-now`) | A process marked 'immediately' runs in waves inside the same moment as the attempt or round step that set it off, until nothing more is due (a glass falls, breaks, the water spills, the neighbour hears it); each pair of process and thing fires once per moment, which is what ends every chain; new runs have no other cap (J0 of the AI judge plan), a step a failed check stops is recorded with its blocker, and a run recorded before J0 replays under its old cap of 32. | `docs/model/ODD.md (8.20)` | `src/world_substrate/engine.py:964` |
| **Living projection** (`projection`) | The read-only living client, JSON and server-sent events rebuilt from canonical snapshots and events; it never changes the world. | `openspec/specs/live-projection/spec.md:5` | `src/world_substrate/projection.py:44` |
| **Hard causal parent** (`causal-parent`) | An earlier event a rule declares as mechanically supporting this one; kept apart from the information a person merely had in mind. | `README.md:66` | `src/world_substrate/rules.py:383` |
| **Derived exchange** (`exchange`) | A composite reading (two give events make one exchange) derived from committed events, never a second effect. | `openspec/specs/transition-engine/spec.md:359` | `src/world_substrate/exchange.py:68` |
| **Installed mechanic** (`mechanic`) | One installed action rule: an action kind's selector, checks, effects and derived reads and writes, compiled and frozen in the profile; the root rule says installed mechanics alone decide what happens. | `AGENTS.md:3` | `src/world_substrate/action_authoring.py:515` |
| **Entity and component** (`entity-component`) | An entity is one thing in the world (person, wall, glass, decision) with an id, a label, categories and typed components; a component is a named record of typed fields (boundary.passable, group_decision.status) that checks read and effects write. | `docs/model/ODD.md:100` | `src/world_substrate/model.py:247` |
| **Law check** (`law-check`) | Plan declared-laws S2 (built): inside the same commit as the write-scope check, every move, round process and knock-on effect is checked against the world's declared laws; a breach refuses the whole step or moment as law_breach and names the law, and nothing changes. A test-run breach is a build finding sent to the rules writer and the world designer. | `docs/model/ODD.md (8.21)` | `src/world_substrate/laws.py:36` |
| **World design (bundle)** (`world-design`) | The build's first AI step: it reads the description and writes the world's people, places, things and starting state as an authoring bundle; plan declared-laws S1 adds the world's resources and laws to its output, and the rules writer receives them as input. | `docs/model/ODD.md:340` | `scripts/generate_world_bundle.py:53` |
| **Independent rules review** (`rules-review`) | Plan declared-laws S3 (built): a separate model call with a fresh context reads the description, the declared laws and the written rules, and lists concrete mismatches (each naming a rule and the words it contradicts) for the rules writer to fix; findings, never a pass mark. Runs on things worlds and, from 2026-10-30, on people worlds. | `docs/model/ODD.md (8.22)` | `scripts/review_rules.py:75` |
| **Run stop setting** (`run-stop`) | A per-world setting saved with the world (run_stop): stop once nothing is changing after N quiet rounds or never for being quiet, plus optional limits, a number of rounds (max_rounds) and this run's recorded AI spending (max_spend_usd); checked after each round, the run stops at whichever fires first and records why (Q12; Brian, 2026-11-10). | `openspec/specs/world-builder-page/spec.md` | `scripts/run_stop.py:65` |

## Fixed people-world part

Fixed code every people world gets from compile_spec.py; the group-decision family is added when the description has a decision.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **People world** (`people-world`) | A world built from a description about people: people, information, moments and the fixed people rules. | `docs/model/ODD.md:293` | `scripts/people_world.py:474` |
| **Communicate rule** (`communicate`) | The reviewed move that delivers an information item to its recipient. Spike code: it lives in spikes/any-scenario-2026-10/, which the live build loads through scripts/people_world.py:73. | `docs/model/ODD.md:294` | `spikes/any-scenario-2026-10/compile_spec.py:56` |
| **Scheduled moment** (`moment`) | A countdown that happens every so many rounds (a weekly meeting, a deadline). Spike code: it lives in spikes/any-scenario-2026-10/, which the live build loads through scripts/people_world.py:73. | `docs/model/ODD.md:295` | `spikes/any-scenario-2026-10/compile_spec.py:48` |
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
| **Person and brief** (`person`) | A person the spec names, with goals and beliefs, and the brief only their own resident reads. | `docs/model/ODD.md:293` | `spikes/any-scenario-2026-10/scenario_spec.py:41` |
| **Generated actions and rules** (`gen-rules`) | The moves and processes the fixed parts do not cover, written by the rules-writing AI and compiled. | `docs/model/ODD.md (11.1)` | `scripts/people_world.py:251` |
| **Place and way** (`place-way`) | Where things are, and what lies between two places (a door, a brick wall) with whether it is passable; written per world as entities from the bundle contract, and the move rule checks the way. | `docs/model/ODD.md:335` | `scripts/generate_world_bundle.py:96` |
| **Declared world law** (`world-law`) | Plan declared-laws S1 (built): a law the AI writes when it designs a world, in that world's own terms: a resource whose total only named moves may change (pencils are made only by the factory's make move), or a move meaning such as 'a purchase moves goods one way and payment the other'. Never a fixed list of move types. The bundle validator checks each law's shape; the rules writer is given the laws and told to keep them; the engine keeps them at every commit (S2, built). | `docs/plans/declared_laws.md` | `scripts/scaffold_world.py:45` |
| **Declared resource** (`resource`) | Plan declared-laws S1 (Q47, built): something the world keeps track of (cash, pencils), declared once with every field it is kept in on different entities (the customer's cash, the shop's business.cash); laws name resources, never raw fields. Each kept_in place must be a numeric field. | `docs/plans/declared_laws.md` | `scripts/scaffold_world.py:45` |

## Reference worlds code only

Hand-written code for the reference worlds (Kitchen, Waltzman and others); no generated world uses it today.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **Waltzman reference components** (`waltzman-ref`) | Trust, risk, readiness and commitment components and analyses of the hand-written Waltzman world. | `docs/wiki/README.md` | `reference_worlds/waltzman/components.py:11` |
| **Mechanisms library** (`mechanisms`) | Reusable hand-written rule families (liquid, ownership, thermal, damage, time) that reference worlds such as Castaway register (reference_worlds/castaway/overheat.py:14); generated worlds get only their compiled mechanics and processes (scripts/run_authored_world.py:71, Q28). | `src/world_substrate/mechanisms/__init__.py:1` | `src/world_substrate/mechanisms/__init__.py:3` |
| **Kitchen flagship** (`kitchen`) | The replicated scarce-knife watched world: hand-written rules of its own on the ordinary Engine. | `README.md:51` | `reference_worlds/kitchen/mechanics.py` |

## In documents only

Named in decisions or the roadmap, not on the live path.

| Concept | Definition | Defined in | Code |
| --- | --- | --- | --- |
| **Build in an agent harness** (`harness-build`) | Decision 008: worlds built by an agent that drafts, checks and edits; scripts/world_harness.py exists but the live service does not call it. | `docs/decisions/008-build-worlds-in-an-agent-harness.md:48` | `scripts/world_harness.py` |
| **Executable-law fingerprint** (`law-fingerprint`) | Roadmap hardening item: fingerprint the exact executable law and compiler version. | `roadmap/README.md:148` | `—` |
| **Skill roll** (`skill-roll`) | Plan S3: a move's outcome depends on a seeded, recorded roll against the person's skill, so someone untrained who flies a helicopter can crash it. | `docs/plans/open_attempt.md:182` | `—` |
| **Run seed** (`run-seed`) | Plan S3: one seed drawn when a run starts and recorded in the run record; each roll's dice come from hash(run seed, event id) and are recorded, so a replay reads the dice and never rolls (Q33). | `docs/plans/open_attempt.md:192` | `—` |
| **Consequence report** (`consequence-report`) | Plan ai-judge J1 (planned, not implemented): what the engine works out for an attempt no rule covers, in two passes. Pass 1, with no new rule: engine.discover for the person acting and for each person the attempt names (their moves, with which checks pass or fail), plus the current values of the entities the attempt names. Pass 2: the judge's proposed rule test-run on a copy of the world, giving its net changes, blockers, chain length and stopping point; the full chain stays in the run record. | `docs/plans/ai_judge.md:309` | `—` |
| **Judge ruling** (`judge-ruling`) | Plan ai-judge J2 (planned, not implemented): Concordia's game master (EventResolution), given the whole world and pass 1 of the consequence report, proposes a rule for the constraint an unmatched attempt raises (can coins change hands here?); after reading the pass 2 test run of that rule it confirms, revises once or withdraws. Never an outcome or another person's choice. | `docs/plans/ai_judge.md:310` | `—` |
| **Ruling-origin rule** (`ruling-rule`) | Plan ai-judge J3 (planned, not implemented): a rule in the existing declaration language made from a confirmed judge ruling after it passes the World Builder rules check and test run, recording the ruling id and round it came from; it applies to everyone in the same situation and the attempt settles through it. A ruling the language cannot express is refused and recorded as a language gap. | `docs/plans/ai_judge.md:311` | `—` |
| **Credential holder** (`credential-holder`) | Plan ai-judge J4 (planned, not implemented): who holds a credential (a password, a signed release) as a fact in the world that can change: told, overheard, copied, forged or phished. The mechanism checks the credential, not the holder. | `docs/plans/ai_judge.md:204` | `—` |
| **Norm** (`norm`) | Plan ai-judge J4 (planned, not implemented): what people expect or forbid (bribery is illegal; only Alice should log in). It can be broken; a breach is recorded and has consequences only when someone notices and acts. Never written as a declared law. | `docs/plans/ai_judge.md:188` | `—` |
| **Mid-run rulings setting** (`midrun-setting`) | Plan ai-judge Decided 5 (planned, not implemented): a per-world option, 'Judge rulings during a run': Approved by Create (default; a checked ruling is installed at once and the attempt settles through it) or Wait for my approval (the proposed rule is held, the attempt waits as pending, Approve installs the rule and settles it, Reject refuses it; nothing settles without an installed rule). | `docs/plans/ai_judge.md:155` | `—` |
| **Plain-words stopping point** (`stopping-point`) | Plan ai-judge J5 (planned, not implemented): a stopping point the person writes in plain words ('stop once the team has agreed a budget'), assessed by the judge after each round that changed something, as one more condition of the run stop setting. | `docs/plans/ai_judge.md:263` | `—` |
| **Estimate rule** (`estimate-rule`) | Plan estimate-rules E1 (planned, not implemented): a process or move whose outcome depends on a chance (later a pick or an amount) that Jev estimates from fields the rule declares; it declares a fixed question, its reads, the answer type, the model, a required fallback (refuse or a declared value) and the effects for each result. | `docs/plans/estimate_rules.md:155` | `—` |
| **Estimator** (`estimator`) | Plan estimate-rules E1 (planned, not implemented): what the engine asks for an estimate; live it is llm_client.call_decisions on Jev (one retry, then the rule's fallback), in a replay it reads the recorded estimates and stops with 'no recorded estimate' rather than call Jev; one call per distinct question and inputs per run. | `docs/plans/estimate_rules.md:181` | `—` |
| **Recorded estimate** (`recorded-estimate`) | Plan estimate-rules E1 (planned, not implemented): on the event, the question, the declared inputs and their values, Jev's answer, the model version returned, the trace id, the cost and whether it was reused from the run's cache; evidence, never world state (Q63). | `docs/plans/estimate_rules.md:123` | `—` |
| **Recorded draw** (`recorded-draw`) | Plans estimate-rules E1 and open-attempt S3 (planned, not implemented): a number drawn from hash(run seed, event id, rule id) and recorded on the event; an estimate rule's chance becomes an outcome only through it, and a replay reads it. | `docs/plans/estimate_rules.md:177` | `—` |

## Where the sources disagree

1. **Decision 008 versus the live build.** Decision 008 says worlds are built in an agent harness that drafts, checks and edits; the live service builds with fixed calls and a rules retry and does not import `scripts/world_harness.py` (open question Q14).
2. **The wiki's 'Concepts and terminology' versus this model.** The wiki (`docs/wiki/README.md`) defines engine-level terms only; people, concerns, support, tasks and residents are defined here and in ODD section 11, not there.
