---
schema_version: project-roadmap-front-door/v1
role: canonical-planning
status: active
context_ref: ../docs/wiki/README.md
reviewed_through: 2026-11-10
---

# World Substrate living roadmap

**Authority:** [Decision 006](../docs/decisions/006-governed-rules-layer-scope.md) (current scope: the governed-rules layer on commodity runtimes), [Decision 007](../docs/decisions/007-any-scenario-path.md) (describe any scenario), [Decision 008](../docs/decisions/008-build-worlds-in-an-agent-harness.md) (build worlds in an agent harness), [Decision 009](../docs/decisions/009-same-moment-knock-on-effects.md) (same-moment effects are rule semantics), and Decisions [001](../docs/decisions/001-project-scope.md) to [005](../docs/decisions/005-native-waltzman-delivery.md). Architecture: [arc42](../docs/architecture/arc42.md). Required behavior: the [capability specs](../docs/index.md#2-what-the-code-must-do-openspec-capability-specs).
**Stage (2026-11-09, `main` at `0e66a98`, #345):** live World Builder alpha. A plain description becomes a world with declared laws and rules, a second model reviews the rules, a free scripted test checks them, and Concordia residents play it live; residents can write open attempts and requests reach the person asked. Two adopted plans are under way: [declared laws](../docs/plans/declared_laws.md) (S1 to S3 built, S4 under way, S5's paid builds wait on Q50) and [open attempts](../docs/plans/open_attempt.md) (S1 and S2 built, S3 skill rolls not built).
**Recent work (#323 to #345, 2026-10-31 to 2026-11-09):** requests reach the person asked (#326); a shared run shows its picture and can be watched (#328, #329, #331); refusals say what really happened (#333); the Network shows one round and uses the fast layout (#338, #344); the Waltzman rebuild was recorded (#339); the planning package caught up (#340); model routes were renamed (#341); the Waltzman lineage review was written, its recommendations not adopted (#342); Brian's scale reason for rules over an AI judge was recorded (#345).
**Deployment boundary:** the World Builder backend runs on the personal VPS and its pages on Cloudflare; shipping is `scripts/deploy_world_builder.sh`. The donor-backed `/waltzman/` demo stays a fallback and must not be presented as a native run.

## Outcome and success criteria

### End goal

Build a **generatively authored, reviewable, persistent simulation platform for plausible worlds**. A person describes a bounded world in plain words; the system compiles its structure and executable law; the person can review the important assumptions; residents and processes inhabit the world under the installed rules; and the person watches and questions the result through a live view.

> **Generative worlds with executable laws.**
> Generative-World Builder on top; rigorous causal world engine underneath.

Why rules rather than an AI judge: scale. Brian, 2026-11-09, quoted in full in [arc42 section 1](../docs/architecture/arc42.md#architectural-thesis): facts must carry their implications and blockers down causal chains far longer than a model can follow.

### Actor, recurring job and investment boundary

- **Actor:** a World Builder visitor (or Brian as owner) at <https://brianmills.dev/world-builder/>.
- **Recurring job and baseline:** the visitor describes a situation in plain words, presses Create simulation (which is the approval), and watches the generated people act under the installed rules. Today each person picks a move the rules offer or writes an open attempt in their own words (S1); same-moment knock-on chains run inside one commit (S2); skill-shaped failures never appear because skill rolls are not built (S3).
- **Inspectable result:** the run page and its build record: what each person tried, what the rules did and why, every event with its cause; a share link replays the run for free.
- **Stage and investment boundary:** prototype stage; this repository and its own deploy only; visitors share $3.00 a day and the owner has $5.00 a day (`scripts/world_builder_service.py`); new paid builds under the declared-laws plan follow the plain-version comparison (Q60); no new service, engine or repository without Brian's yes.

### Causal product contract

A World Substrate causal claim explains why a transition occurred **inside the represented world under the installed mechanics that governed that run**. It is not, by itself, a claim that those mechanics are true of the real world; predictive validity and real-world causal identification need separate evidence. `causal_parent_event_ids` are mechanic-declared and validated against retained history, never inferred from temporal order or from what a resident was shown. The Waltzman adequacy report is a bounded dependency inventory with residual risk, not counterfactual proof.

### Current showcase world — Waltzman Coordination Lab

Rand Waltzman's bio-surveillance coordination scenario (*From Minds to Coordination*) is the showcase. It builds through the people-world path (`scripts/people_world.py` and the scenario-spec pipeline in `spikes/any-scenario-2026-10/`), declares laws over the counts it keeps and gets the same rules review as a world of things (#314). The hand-authored Waltzman reference world (`reference_worlds/waltzman/`) remains the regression fixture for the living-view and causal semantics. The [lineage review of 2026-11-07](../docs/audits/waltzman-lineage-review-2026-11-07.md) found the generated Waltzman world stipulates some of what the paper's mechanisms should produce; its recommendations are not adopted (Q60).

### Prototype phase — complete

Persistent typed canonical state; bounded observations and state-derived affordances; scripted, human and LLM selection outside consequence authority; semantic/mechanical separation; reviewed frozen profiles; atomic commit or refusal with write-scope enforcement; retained causal evidence; transfer to materially different worlds (Castaway, Kitchen, Workshop, Greenhouse, Orchard, Repair Bay, Waltzman).

### Waltzman demo acceptance criteria

The 2026-09-09 stakeholder promotion met ten criteria through the reference world plus the donor authoring path: a living view driven by canonical snapshots and events; represented information with source, recipient, channel and visibility; residents acting through the policy seam; outcomes depending on represented resources and institutions; one simulated timeline; inspectable causality with information kept apart from causal parents; detachable Waltzman analysis; an exact-history intervention fork; a bounded dependency report; and one continuous public experience. Evidence: [promotion record](../evidence/waltzman/public-promotion-2026-09-09.md). Saved user worlds, persistent cognition, generic scheduling and predictive validity were outside that gate. The separate human world-only review of `evidence/renders/waltzman-living-v1.html` (Company Planning #222) has no recorded answer; `evidence/waltzman/m1-acceptance-candidate-v1.json` still reads `pending_human_world_only_review` at tested revision 27164359.

## Canonical outcome probe

The steps a visitor takes end to end, which every plan's outcome step names one of:

1. Describe a situation in plain words on <https://brianmills.dev/world-builder/> and press Create simulation.
2. The builder generates the world (places, things, people, the moves they may attempt), its declared laws and its rules; a second model reviews the rules; a free scripted test checks that something can happen.
3. The residents act each round, and the installed rules decide each effect: accepted, refused with the failing check, or changed state that later rules react to.
4. The page shows the run round by round, with each event's cause and the build record.
5. The visitor reads why things happened, follows a cause back, and can replay the saved run for free.

Fixtures with narrower roles: M1 Castaway freshwater (the neutral substrate baseline with exact replay), Kitchen (replicated watched-world behavior), Greenhouse (new-world presentation), Orchard (live authoring acceptance), Repair Bay (first nontrivial deployed authoring world), Warehouse Rush (a law/representation omission and its repair), and the Waltzman reference world.

## Current truth

State, not narrative. Code paths are the evidence; the [arc42 building blocks](../docs/architecture/arc42.md#5-building-block-view) map each one.

- One `World` owns canonical truth. Prompts, page state, residents' memories and analyses are not alternate authorities.
- Write scopes are enforced. Declared read scopes are recorded, not enforced; the project check reports `read_scopes_enforced` as a constant (Q34, Q66).
- Write-scope placeholders are bound to participants, not to one specific action role (Q67).
- A world's declared laws are checked at every commit; a step that breaks one is refused and names the law (`src/world_substrate/laws.py`). People worlds declare laws too (#314).
- An independent rules review by a model of another family (chosen as gemini-3.1-pro-preview in `evidence/declared-laws/s3-review-choice/`; the route is `openrouter/google/gemini-4-argon` since #341, `scripts/review_rules.py:18`) runs on every kept try; an unreviewed try ranks below every reviewed one.
- Open attempts (S1): an interpreter reads a resident's words into one typed move or leaves it unmatched; an unmatched attempt changes nothing except a request to another person, which is delivered to that person (#326).
- Same-moment knock-on effects (S2): `timing: immediately` processes settle in waves inside the one commit. Since the AI judge plan's J0 (2026-11-10) there is no cap: each (process, entity) pair fires once per moment, so 50 chains of 100 links finish in one moment; every step names its cause, a step a failed check stops is shown with its blocker, and runs recorded before J0 replay under their old cap of 32.
- Residents run on Concordia since 2026-10-16 (`scripts/concordia_residents.py`); the Concordia game master is off, so there is no AI judge.
- The Decision 008 agent harness (`scripts/world_harness.py`) exists but the live service does not call it (Q14).
- The people-world path imports code from `spikes/any-scenario-2026-10/` at run time (`scripts/people_world.py:26,76-77`).
- The mechanic profile id does not include a compiler or interpreter version (Q69); the 256-move discovery cap truncates silently (Q69); a mechanic that raises mid-rule is rolled back and re-raised, not recorded as a refusal (Q69).
- About fourteen hand-written build checks still run, each added after one bad world; none has been retired by declared laws yet (Q45).
- Rules default to `openrouter/openai/gpt-6-luna`: re-measured on 2026-10-23, 23 of 24 builds reached their finish line and 19 of 24 were also faithful, at $0.0032 per build ([trace read](../evidence/luna-rules-2026-10-23/TRACE_READ.md)).
- The World Builder page is one box and Create simulation (Brian, 2026-10-15); live play goes one round per request and pauses at a finish line, after 4 quiet rounds, on an error and every 100 rounds; builds and runs are background jobs because Cloudflare cuts requests at 100 seconds; share links store and replay runs.
- Deployment: pages on Cloudflare Worker `world-builder-pages`, API edge `world-builder-api`, service container on the personal VPS since 2026-10-05 (binding `0.0.0.0:8813` inside the container, `LLM_CLIENT_TIMEOUT_POLICY=ban`); up to four AI jobs at once. All public pages answered HTTP 200 on 2026-11-09.
- Scheduling is integer ticks; `Engine.advance()` checks each process with `due(world)`; World Builder processes run `each_round` or `immediately`. No future-event queue exists.
- deck.gl is loaded only by the Waltzman reference client (`scripts/render_waltzman_demo.py`); the World Builder draws its network with the vendored graph viewer. Pydantic AI, SimPy, Cytoscape.js, PettingZoo and Mesa are not used in `src/` or `scripts/`.
- The native coordination vertical, one-shot authoring and run comparison are on main since 2026-10-05 (#75, #79, #80); `scripts/check_native_coordination.py` passes for two worlds on one shared profile with no provider spend.
- Semantic binding: six of seven M1 action kinds cite a reviewed Linguistic Core sense; `unheat` is deliberately unbound. Kitchen and Greenhouse events can carry Castaway mechanic ids because binding is by bare action kind (Q64).
- No hosted CI: `.github/workflows/native-coordination-linux.yml` was removed on 2026-11-10 (Q70, Brian approved); `scripts/check_project.py` already ran every command it ran and gates each merge through `ship`.

## Applicable context

- [arc42](../docs/architecture/arc42.md): goal, requirements, constraints, source dispositions, building blocks, deployment and risks.
- [Capability specs](../docs/index.md#2-what-the-code-must-do-openspec-capability-specs): transition engine, rule authoring, mechanic installation, authoring bundle, semantic binding, information delivery, live projection, scenes, native coordination and the World Builder page.
- [System model](../docs/model/ODD.md) with [trace.yaml](../docs/model/trace.yaml): each enforced rule, its owner and its test.
- [Open questions](../docs/planning/open-questions.json) and the [planning package](../docs/planning/planning-package.json).
- [Lessons](../docs/wiki/lessons.md): read before planning a goal.
- [Flexible simulator prior art](../docs/research/flexible-simulator-prior-art-2026-10.md), [competitive landscape](../docs/research/competitive-landscape-2026-09.md), [technology procurement](../docs/research/technology-procurement-2026-09.md).

## Constraints and authorities

```text
plain-language description  (Create simulation = approval)
  -> authoring bundle (structure, declared resources and laws) + causal model (rules as data)
  -> local compiler derives authority; independent rules review; free scripted test
  -> frozen mechanic profile
  -> resident move or open attempt (Concordia) OR process trigger
  -> Engine checks + one commit/refusal + same-moment knock-on waves + declared-law check
  -> canonical state + causal events + run log
  -> read-only views (round feed, Network, build record, share-link replay)
```

Hard constraints:

- policy or model prose cannot mutate canonical state;
- a mechanic cannot enlarge its own write authority;
- generated source code is never a causal-law fallback;
- analysis cannot rewrite history or duplicate primitive effects;
- presentation is downstream and read-only;
- resident harnesses choose attempts and utterances but never adjudicate consequences;
- information delivery and context never become hard causal parentage automatically;
- causal claims about the represented world are not marketed as real-world causal truth;
- the adequacy inventory is not marketed as counterfactual proof;
- no engine, scheduler, renderer or cognition capability of World Substrate's own (Decision 006); a bounded same-moment fixpoint inside the existing commit does not count (Decision 009).

## Vertical slices and current work

### Milestone horizon

| Milestone | State | What it establishes |
| --- | --- | --- |
| M0 to M7b substrate and generative mechanics | complete | persistent governed world; authoring, compiler and policy seams |
| Kitchen, Greenhouse, Orchard, Repair Bay | complete first gates | watched-world behavior, portable replay, live generated-law authoring |
| Waltzman reference world and stakeholder demo | promoted 2026-09-09 | living projection, information, intervention fork, bounded adequacy; donor-backed public demo |
| Native coordination vertical | landed 2026-10-05 | #75, #79, #80 |
| Replacement-first gate | recorded 2026-10-05 | Concordia, Mesa, PDDL compose; none replaces the governed-rules layer |
| Natural-language World Builder | live since 2026-10-05 | one box, Create simulation, live play, share links |
| Concordia residents | live since 2026-10-16 | AI residents through an established framework |
| Open attempts | S1 and S2 built; S3 not built | own-words attempts; same-moment knock-on effects; skill rolls next |
| AI judge ([plan](../docs/plans/ai_judge.md)) | J0 built 2026-11-10; J1 to J3 and J5 next; J4 exploration only | knock-on chains of any length; an AI judge (Concordia's game master) rules only on what no rule covers, from the engine's consequence report |
| Declared laws | S1 to S3 built; S4 under way; S5 follows the plain-version comparison (Q60) | worlds declare laws, the engine keeps them, a second model reviews the rules |
| AI judge | draft plan, direction approved 2026-11-09; build started 2026-11-10 (J0) | the engine works out every knock-on effect and blocker; a judge rules only on gaps, its rulings become checked rules ([plan](../docs/plans/ai_judge.md)) |
| Estimate rules | draft plan 2026-11-10; nothing built | a rule's outcome can depend on a chance Jev estimates from named facts, rolled, recorded and replayed without Jev; only slice E4 (judge-proposed estimate rules) waits for the judge's J3 ([plan](../docs/plans/estimate_rules.md)) |
| Hardening | queued | law fingerprint with compiler version, role-bound scopes, visible discovery overflow, recorded mechanic exceptions, locking |
| Persistence and second-domain proof | later | saved user worlds beyond share links; proof beyond Waltzman |

### Active slice — declared laws S4, then skill rolls

1. **Declared laws S4** ([plan](../docs/plans/declared_laws.md)): let declared laws and the rules review retire the hand-written build checks. Done so far: free replay of every saved world (`scripts/check_saved_worlds.py`), fixes from the S4 live builds (one-way moves kept #309, places and owners shown to the reviewer #310, fields only one thing can fill #312, people worlds get laws and review #314, every kept people try reviewed #317, trades named from one side #319, the round told to each person #320 and #323). Not yet done: retiring any hand-written check (Q45).
2. **Declared laws S5**: live builds of four varied descriptions in parallel. Follows the plain-version comparison (Q60, settled 2026-11-09 by Brian's plain-version rule); one Waltzman rebuild ran on 2026-11-04 on his yes for that build (`evidence/declared-laws/s4-waltzman-3/`).
3. **Open attempts S3** ([plan](../docs/plans/open_attempt.md)): seeded, recorded skill rolls on action mechanics, with the roll's skill path in derived reads (Q33, Q40).
4. **Estimate rules E1** ([plan](../docs/plans/estimate_rules.md)): chance rolls on Jev's estimate, sharing the skill roll's run seed (Q33); whichever of S3 and E1 lands first builds the seed. Brian approved planning it on 2026-11-10.

### Hardening queue

Small reversible changes, none reopening the architecture: fingerprint the exact executable law plus compiler version; bind write-scope placeholders to one action role; make discovery-cap overflow visible; record mechanic exceptions as refusals; enforce or honestly report read scopes; add a lockfile when a dependency enters a reproducible production path. Details and sources: Q34, Q66, Q67, Q68, Q69.

### Deliberately deferred

Automatic counterfactual adequacy verification; always-on read-scope enforcement; persistent resident cognition; a future-event scheduler; saved user worlds and identity; massive or distributed scale. Promote one only when a concrete product or evidence need earns it.

## Decisions and assumptions

### Replacement-first gate disposition (recorded 2026-10-05)

Three executed spikes hosted the governed-rules layer on the constrained-handoff world (`spikes/replacement-2026-10/`; each `run_spike.py` exits nonzero on failure, zero provider spend). Re-run independently before recording: all three exit 0.

| Candidate | What it was asked to replace | Evidence | Disposition |
| --- | --- | --- | --- |
| Concordia (`gdm-concordia` 2.4.0) | agent/game-master loop | its game master drives the run while resolution calls only `Engine.discover`/`submit`: 7 events, world-state sha256 identical to the native run, 11/11 checks. A native Concordia rewrite of the rules is 51 lines of our own code (Concordia ships no rule, check, authority or atomic-commit primitive) and lacks staleness checks, write scopes and compiler validation. | **compose**: use as the resident loop when LLM residents are needed; keep the Engine as sole authority |
| Mesa 3.5.1 | model/agent loop, scheduling, data collection | Mesa loop over the Engine gives the same hash, same events and `Engine.replay()` ok (70 glue lines). A rules-in-Mesa rewrite loses, demonstrated by code: atomic commit (partial write persisted), write-scope enforcement (out-of-scope write went through), recorded cause, rules-as-checkable-data, replay from a recorded log. | **compose** when a world needs grids/networks, stochastic activation or parameter sweeps; not adopt |
| PDDL (unified-planning 1.3.0 + ENHSP) | declaration language / validation / planning | rules translated programmatically to PDDL (4 actions, 30 fluents). The validator accepts the reference plan and rejects the refused approval on the same precondition the Engine refused ("Prerequisite A is healthy"). ENHSP found a different 6-step plan, and the Engine accepted all 6 steps and reached `ready`. Cannot express information visibility, write scopes, causal records, refused-attempt history, open worlds. | **compose**: an export for offline validation and "is the goal reachable" checks; not the runtime or declaration language |

**Result:** no candidate replaces the governed-rules layer, and each can host or check it. World Substrate therefore keeps exactly that layer (rules as data -> compiler-derived authority -> explicit approval -> atomic commit/refusal with recorded cause) and **stops growing its own runtime extras**. Outer loops, resident cognition, scheduling, spatial structure and sweeps come from Concordia or Mesa when a world first needs them; formal validation and planning come from a PDDL export.

**Wrong when:** the first LLM-resident run through Concordia needs a game-master component that writes state outside `Engine.submit`, or more glue than the `CognitionAdapter` path; a Mesa (or other) release ships transactional state with write scopes and per-change history; the PDDL translator needs hand edits for distributed-approval, or the validator and `engine.submit` disagree on any step of a recorded run. Any one of these means re-running the gate for that candidate.

Spike-noted defects to fix in World Substrate itself: a mechanic that raises mid-rule surfaces as an exception rather than a recorded refusal event (listed under Q69 below); the PDDL export's constant order varies with the hash seed (cosmetic, from the library's writer).

### Product and adoption posture

| Layer | Posture on 2026-11-09 |
| --- | --- |
| Canonical state, transition kernel, authority, trace semantics | project-owned |
| Rule language, compiler, declared laws, rules review | project-owned |
| Semantic binding | project-owned profile over pinned Linguistic Core meaning |
| Resident loop | Concordia (integrated) |
| Spatial structure, sweeps, stochastic activation | Mesa when a world needs it (not integrated) |
| Formal validation and reachability | PDDL export (spike only) |
| Live view | vendored shared graph viewer in the World Builder; deck.gl only in the Waltzman reference client |
| Scheduling | integer ticks today; SimPy was selected in 2026-09 but never integrated, and Decision 006 now routes scheduling to Concordia or Mesa |
| Persistence and identity | share links only; commodity infrastructure later |

### Information and causality rule

Keep apart: world interaction (Mara speaks to Ari); information lineage (representation, source, recipient, channel, delivery); cognition context (what a resident was shown); mechanic-declared causal ancestry; and analytic interpretation. Temporal order or prompt inclusion never makes information a hard cause of a decision.

### Adequacy rule

The bounded adequacy report answers which consequential assumptions were inventoried, where they are represented, which rules enforce them and what residual risk remains. It does not prove each dependency necessary and sufficient; that is a deferred research option.

### Semantic-profile rule

Linguistic Core contributes meanings and roles. World Substrate's profile owns only the bridge (specialization, causal classification, bearer, mechanic, limits) and never moves persistence, effects, scheduling, write authority or commit semantics into Linguistic Core.

### Approval and law provenance rule

An approval should point to one exact executable law identity for the run. Freezing the profile is a partial implementation; add the compiler version before user-generated laws become long-lived (Q69).

### Experiment-selection rule

Novel uncertainty: experiment. Commodity uncertainty: research, reason, select. Integration uncertainty: prove the selected adapter conforms. A test runs only when a named decision cannot be settled by argument or prior art.

## Evidence and review artifacts

- <https://brianmills.dev/world-builder/> (live alpha), <https://brianmills.dev/world-builder/play/> (Replay Studio), <https://brianmills.dev/waltzman/> (donor fallback).
- Declared-laws and open-attempt run evidence: every trace read is listed in the [documentation index](../docs/index.md#8-run-evidence); the latest Waltzman build is [s4-waltzman-3](../evidence/declared-laws/s4-waltzman-3/TRACE_READ.md).
- [gpt-6-luna rules measurement](../evidence/luna-rules-2026-10-23/TRACE_READ.md).
- Replacement-first spikes: `spikes/replacement-2026-10/` ([Concordia](../spikes/replacement-2026-10/concordia/README.md), [Mesa](../spikes/replacement-2026-10/mesa/README.md), [PDDL](../spikes/replacement-2026-10/pddl/README.md)).
- Waltzman reference world: `evidence/waltzman/`, `evidence/renders/waltzman-demo-v0.html`, [promotion record](../evidence/waltzman/public-promotion-2026-09-09.md).
- Planning review pages: `hive.brianmills.dev/plans/world-substrate/main/proposals/{planning-package,open-attempt,declared-laws}/review-page/`.

Open pull requests: none on 2026-11-09 (`gh pr list --state open`).

## Risks and needs resolution

| Priority | Risk or open need | Current stance |
| --- | --- | --- |
| P0 | the generated Waltzman world stipulates outcomes its mechanisms should produce (Q60) | settled 2026-11-09 by Brian's plain-version rule: compare against one model given the whole scenario before more repair or S5 |
| P1 | hand-written build checks keep growing (Q45) | retire them only when declared laws and the review demonstrably cover the incident |
| P1 | declared laws can be wrong for the world, or missing (Q48, Q49) | read S4 and S5 builds for counterexamples |
| P1 | the agent harness is not on the live path (Q14) | measure a harness build against the 150 s first-round target (a people build must play its first round within 150 s of Create simulation) |
| P1 | law fingerprint lacks compiler version; silent discovery truncation; unrecorded mechanic exceptions (Q69) | hardening queue |
| P1 | write-scope placeholders are not role-bound (Q67) | hardening queue |
| P2 | read scopes are recorded, not enforced, and the check reports a constant (Q34, Q66) | report honestly first; enforce when a run needs it |
| P2 | live path imports spike code (`spikes/any-scenario-2026-10/`, Q71) | move what the live path needs into `scripts/` or `src/` when next changed |
| P2 | hosted CI conflicts with the no-hosted-CI rule (Q70) | done 2026-11-10 (Brian approved): the project check already ran every test it ran; workflow removed |
| P2 | `schemas/world-authoring-bundle-v0.schema.json` rejects law-bearing bundles (Q65) | fix the schema to match the validator |
| P3 | `unheat` lacks a pinned Linguistic Core sense | upstream semantic gap |
| P3 | no counterfactual adequacy proof; no scale demonstration | deferred |

## Human decisions

Answered (kept as the record): World Substrate is the one canonical project (001); observability required, exact replay not (002); meaning does not imply effects, and richer Linguistic Core roles do not move mechanics upstream (003, 2026-09-12 review); own causal reality and borrow commodity machinery (004); converge the next Waltzman release on native World Substrate (005, 2026-09-18); hold at the governed-rules layer (006, 2026-10-05); describe any scenario (007); build worlds in an agent harness (008); same-moment effects are rule semantics (009, 2026-10-26); Create simulation is the approval (2026-10-15); Concordia hosts residents; gpt-6-luna is the default model, sol only when sharing with Waltzman (2026-10-16); adopt the open-attempt plan (2026-10-25) and the declared-laws plan (2026-10-28); believability is the off-the-shelf people agents' job, no metric, tuned once everything else runs well (Q50, 2026-11-09); when a run stops is a per-world setting, "stop condition should be configurable" (Q12, 2026-11-10; built in PR #356: stop once nothing is changing after 6 quiet rounds by default, or always run every round); a world can also stop after a number of rounds or once a run has spent a dollar limit, "i should be able to stop a world based on budget or number of rounds or a natural langue stopping potin that the judge assesses once we build him" (2026-11-10; round and spending limits built, the plain-words stopping point is R11/A8 of the AI judge plan).

Open: none awaiting Brian. Each question, open or answered, is in the [open questions ledger](../docs/planning/open-questions.json) with what it blocks.

Q16, Q17, Q60 and Q70 were settled by the agent on 2026-11-09 (technical calls, or settled by Brian's plain-version rule); the ledger records each.

## Refresh and reset triggers

Refresh this roadmap when:

- Brian answers a new question in the ledger;
- a declared-laws or open-attempt slice lands, or a hand-written build check is retired;
- the agent harness reaches the live path;
- a hardening item lands;
- any Decision 006 wrong-when condition fires;
- evidence contradicts a current-truth statement.

Replan rather than extend blindly if:

- a view needs to invent canonical facts;
- generated rules routinely need model-written code;
- information and cognition cannot be kept apart without leaking observer truth;
- adequacy work grows faster than useful world complexity;
- an external dependency requires surrendering Engine consequence authority; or
- a feature is proposed for completeness rather than a concrete product or evidence need.

## Exact next action

1. **Declared laws S4:** retire the first hand-written build check whose incident a declared law or the rules review now covers, proven on the saved worlds with `scripts/check_saved_worlds.py` and `scripts/replay_build.py` before any paid run (Q45).
2. Before S5's paid builds or more people-world repair, run the plain-version comparison (Q60), with its cost worked out first.
3. In parallel, the hardening queue items that need no paid run (Q66, Q67, Q69).

Do not add engine, scheduler, renderer or cognition capability of World Substrate's own ([Decision 006](../docs/decisions/006-governed-rules-layer-scope.md); [Decision 009](../docs/decisions/009-same-moment-knock-on-effects.md) sets out what does not count).
