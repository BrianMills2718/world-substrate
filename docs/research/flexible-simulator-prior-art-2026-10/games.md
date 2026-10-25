# Games and interactive fiction survey: prior art for a flexible world simulator

Scope: Inform 7, TADS 3, The Sims, immersive-sim chemistry (Thief/Deus Ex/BotW), Dwarf Fortress, Caves of Qud, ECS (Flecs/Bevy/DOTS), tabletop adjudication (Blades in the Dark/GURPS/PbtA). Date 2026-10-24.
Verification legend: [V] fetched this session; [S] seen only in search snippet or secondary source; [U] from memory, not verified.

## 0. What we already have (read first)

- ADR-013 (`~/code2/cybernetic_influence_v3/docs/adr/013-generalized-simulator-foundation.md`): Concordia owns lifecycle. Pipeline is canonical truth -> actor-authorized observation -> open semantic intent -> declared transition authority (deterministic, stochastic, LLM, external sim, scripted, replayed) -> structured patch proposal -> generic reference/authority/topology/information/invariant checks -> atomic commit or visible rejection -> per-actor observation plus evidence. Inert things (truck, record) stay records with affordances, not fake `act` entities. Capability/permission/attempt/adjudication/outcome kept "where the question requires".
- ADR-006: organisations are derived, reversible coarse-grainings; never an executor, never in the active-system registry. ADR-013 later allows a coarse surrogate to be an active entity if it does not duplicate a simultaneously active detailed representation. This is close to example 7 but "chosen per run" is not yet a mechanism.
- `src/cybernetic_influence/active_runtime/models.py` (path in brief is stale; real path is under `src/`): `ActiveSystemSpec` has `entity_id`, `implementation_id`, `observation_port_ids`, `activation_observation_port_ids` (what wakes it), `output_port_ids`, `required_output_port_ids`, `output_port_unavailable_when` (technical availability, explicitly not permission), `initial_next_update_at` (self-scheduling). `ActiveRuntimeConfig` has per-call/run budgets. Nothing in the spec declares fidelity tier (LLM vs typed model vs code).
- world-substrate (`AGENTS.md`, research/): invariants are "mechanics propose, one transition validates and commits or refuses", declared write scopes enforced, declared reads recorded only, every attempt leaves causal evidence, Linguistic Core supplies senses/roles and installed mechanics supply effects. Decision 006 scopes the product to a governed-rules layer on commodity runtimes. Spikes show Concordia, Mesa, PDDL each compose with it and none replaces it. Prior research already cites Dwarf Fortress (rules over categories/properties, reactions derive outputs, mixed resolution) and names Inform 7 and ECS only in one sentence each in `competitive-landscape-2026-09.md` lines 202-203 ("worth citing"). `off-the-shelf-candidates-2026-09-25.md` lists PDDL, effect systems, PROV-O, Halpern-Pearl, Mesa; no ECS, no rulebook model, no TTRPG adjudication row.
- Castaway finding: 69 colocated vessels gave 4,927 candidate actions and a 73 KB prompt. Menu-style offered actions do not scale. This is the main practical argument for "attempt anything".

Net: we have the commit boundary, the evidence trail, the authority declaration, and the ports. We lack (a) a precondition/consequence rule structure that is object-local and extensible by data, (b) a reaction-propagation mechanism (observers/triggers), (c) a skill/fidelity-gated resolution procedure, (d) a way to handle "attempt with no matching mechanic".

## 1. Inform 7 (Standard Rules world model)

What: rule-based IF authoring system. Kinds (thing, container, supporter, door, person, device) with properties; every action runs through rulebooks. Docs: https://ganelson.github.io/inform-website/book/ (Writing with Inform) [V].

Action pipeline [V, WI 12.9, 7.2]: before -> instead -> check ("verifies that the action is possible"; failing check stops it) -> carry out ("makes the change... the action is committed") -> after -> report ("prints what happened"). Instead rules replace an action and count as failure. More specific rules run before general ones; stages can be reordered ("action-processing rules"). NPCs: `try` / `silently try` start an action from any rule [V, WI 12.1]. Asking an NPC to do something goes through persuasion rules (yes/no/undecided; default no); success generates the NPC's own action through the same rulebooks, and the "asking" action still counts as successful because the person did try [V, WI 12.4]. Unsuccessful-attempt rules cover NPC failure messages [V]. Capacity: containers and supporters have a carrying capacity (default 100) that refuses with "no room on" [V, WI 3.19]. Doors and locks have sections 3.12/3.13 (lockable, locked, matching key) [titles V, content not fetched].

| # | Example | Cover | Why |
|---|---|---|---|
| 1 | Door | covers | open action has check rules (not locked, not already open); locked/lockable properties; person triggers via `try`; door has no self-initiated action |
| 2 | Chair | covers | supporter kind with capacity; never acts |
| 3 | Wall | partly | going through a wall fails by check rule, but the player parser must first map words to the `going` action; an unknown verb is "I only understood you as far as..." (menu-ish grammar) |
| 4 | Voice | partly | no native sound propagation; authors hand-write "hear" via rooms; intent is never a thing |
| 5 | Helicopter | no | no skill model; authors write ad hoc |
| 6 | Clock | partly | `every turn` rules and timed events; authored per object, not a declared internal transition |
| 7 | Organisation | no | |
| 8 | AI/animal/computer | partly | persuasion + NPC rules; one fidelity (code) only |
| 9 | Thinking | no | no self-directed action kind |
| 10 | Ramifications | partly | `after` and `carry out` rules can chain by `try`; falling-and-breaking is hand-authored per case, no generic reaction layer |

ADOPT:
- The three-phase split per action kind: CHECK (pure predicate, may refuse with a reason) / CARRY OUT (state change, no output) / REPORT (observations). It matches our "propose / validate / commit / observe" but gives each mechanic author a standard shape. Also the rule-specificity ordering and the rule that refusal is a normal, reasoned outcome (supports example 3).
- Vocabulary: before / instead / after as interception rulebooks that institutions or hazards can install without editing the base action (analogue of a patch-time interceptor).
- Persuasion as a distinct attempt layer: "asked X to do Y" is itself a successful action even if X refuses (matches our attempt vs outcome split; maps to NPC autonomy).
- `try` = a rule may spawn a new attempt that re-enters the same pipeline (bounded recursion). This is the right model for automatic consequences (example 10) because the consequence goes through the same checks.
GAP: parser-bound verbs; no skills; no spatial perception model; single-threaded turn; no reaction trigger on state change (only on actions); authored by programmers in a DSL. Runtime is Inform 7 compiled to Glulx/Z-code; not embeddable for our purposes.
Maturity: Inform 7 10.x, maintained by Graham Nelson et al. (https://github.com/ganelson/inform), Artistic License 2.0 [U for version/licence].

## 2. TADS 3 / adv3 library

What: OO IF system; adv3 library implements actions as per-object, per-role methods. Docs: https://tads.org/t3doc/doc/gsg/ (check.htm, remap.htm, precond.htm, controllingtheaction.htm) [S: located by search, content summarised from snippets; docs.tads.org does not resolve].

Mechanism [S]: for each action, an object overrides stage methods via `dobjFor(Open) { preCond; remap; verify; check; action; report }`. `verify` ranks logicalness and can veto, mainly for parse disambiguation; `preCond` can change state to satisfy a condition (implicit take, implicit unlock) before check; `check` vetoes; `action` commits; `report` narrates. `remap` redirects an action to another object/action and overrides the other stages (e.g. "open the box lid" -> "open lid"). Notification hooks `beforeAction`/`afterAction` (roomBeforeAction etc.) on everything in scope broadcast to bystanders.

Coverage:
| # | Example | Cover | Why |
|---|---|---|---|
| 1 | Door | covers | per-object preCond (implicit unlock/open), check, action |
| 2 | Chair | covers | Surface/Chair classes with bulk and weight limits (class names [U]) |
| 3 | Wall | partly | same parser limitation as Inform |
| 4 | Voice | partly | senses (sight/sound/smell/touch) with "sense connectors" and sound propagation across rooms are a built-in adv3 concept [U, strong memory of `Thing.canHear`, `senseConnector`; not fetched] |
| 5 | Helicopter | no | |
| 6 | Clock | partly | `Daemon` / `Fuse` objects scheduled per turn [U] |
| 7 | Org | no | |
| 8 | Deciders | partly | NPC `ActorState` and agenda items [U] |
| 9 | Thinking | no | |
| 10 | Ramifications | partly | `beforeAction`/`afterAction` broadcast to everyone in scope is a built-in observer pattern |

ADOPT:
- `preCond` as a distinct concept from `check`: a precondition that the world may try to satisfy for the actor (take the key first, unlock first), recorded as sub-attempts. Our GM would otherwise have the LLM improvise those steps. Relevant to "door opens only when handle pushed down and pulled": the door declares an ordered precondition chain.
- Action `remap`: an object declares "attempts on me of kind A are really attempts on part B" (door handle, chair seat). A good answer to compound objects.
- Sense model with explicit connectors between locations (example 4). Verify in adv3 manual before adopting wording.
GAP: same as Inform; per-turn model; no skill or fidelity; no organisations.
Maturity: TADS 3.1.x, GPL/free licence for the system [U]; small community, low activity [U].

## 3. The Sims: smart objects and advertisements

What: autonomous Sims pick among interactions that nearby objects "advertise", scored against motives; behaviour lives in object-attached scripts (SimAntics, edited in Edith). Primary: Forbus and Wright, "Some notes on programming objects in The Sims" (2001), https://qrg.northwestern.edu/papers/Files/Programming_Objects_in_The_Sims.pdf [V: title/authors/date; I could not extract the body text, so claims below about its content are not verified against it]. Forbus's GDC course outline lists interaction types Advertised (Autonomous), Manual, Pushed (high priority), Functional, and "Invisible Objects" (phone line, visitor generator, burglar portal, sickness) https://users.cs.northwestern.edu/~forbus/c95-gd/lectures/The_Sims_Under_the_Hood_files/outline.htm [V]. Utility-over-needs framing and "information lives on the objects" are from secondary sources [S: GMTK video transcript, game-industry-library summary]. The attributed quote "the intelligence is in the objects" is unverified.

| # | Example | Cover | Why |
|---|---|---|---|
| 1 | Door | covers | object owns its interaction list and guard conditions [S] |
| 2 | Chair | covers | the canonical example: chair advertises "sit" (comfort motive); never acts [S] |
| 3 | Wall | partly | pathfinding blocks; no free-form attempt |
| 4 | Voice | no | |
| 5 | Helicopter | partly | skills gate interactions (cooking, repair) with skill levels [U] |
| 6 | Clock | covers | "invisible objects" are non-embodied world actors that run on schedule [V list] |
| 7 | Org | no | |
| 8 | Deciders | partly | one decider type (utility) |
| 9 | Thinking | partly | motives are internal state; no explicit self-action |
| 10 | Ramifications | partly | object scripts trigger other objects (fire spreads) [U] |

ADOPT:
- Affordance vocabulary: an object ADVERTISES interactions with preconditions and effects; the actor never needs to know object internals. Fixes example 2 directly and gives a way to give the LLM actor a bounded, relevance-filtered "what is possible here" list without an enumerated global menu. (Caution: this is a hint channel, not a gate; attempts outside ads must still be adjudicated.)
- Interaction classes (autonomous, manual, pushed, functional) as a tag on an attempt, useful for priority and logging.
- "Invisible object" = world-process entity (phone line, burglar portal) that is a legitimate clock-like actor. Matches ADR-013's "inert vs active" split.
GAP: closed set of authored interactions; utility scoring is a decider, not a world rule; no uncertainty/skill adjudication; proprietary Maxis code (no reusable code). Maturity: shipped game; OpenTS-style fan reimplementations exist [U]; concept only.

## 4. Immersive-sim systemic design (Thief/Deus Ex/BotW chemistry)

What: objects have properties and the engine has a small number of general interaction rules, so designers get combinations for free. BotW: GDC 2017 talks by Fujibayashi ("multiplicative gameplay") and Dohta (physics and chemistry engines); materials/elements (fire, water, electricity, wind) interacting by rule [S: press coverage; slides/video in GDC Vault not read]. Thief/System Shock 2 Dark Engine: Stimulus/Response system, where stimuli propagate through space/links and objects with matching receptors respond [U: strong memory, search failed to confirm; verify via ttlg.com or OpenDarkEngine docs before citing].

| # | Example | Cover | Why |
|---|---|---|---|
| 1 | Door | partly | locks and keys are scripted per object |
| 2 | Chair | partly | physics props only |
| 3 | Wall | covers | collision |
| 4 | Voice | covers | Thief noise propagation to AI hearing (Dark Engine sound propagation through rooms, [U]); intent not used |
| 5 | Helicopter | partly | vehicle physics; skill generally absent |
| 6 | Clock | covers | scripts/timers |
| 7 | Org | no | |
| 8 | Deciders | covers (code only) | AI state machines |
| 9 | Thinking | no | |
| 10 | Ramifications | covers | this is its point: fire ignites wood, wind moves fire, metal conducts lightning [S] |

ADOPT:
- Property-driven generic interaction rules ("flammable + heat source -> burning"), authored once over categories not objects. Already echoed in our DF lesson; BotW and S/R give the cleanest "stimulus type + intensity propagating along relations + receptor/response table" pattern for example 10 and example 4.
- Stimulus/response table as the data shape for propagation: (stimulus kind, source, intensity, medium/links) x (receptor on target) -> response proposal. Responses are proposals that go to our commit boundary.
GAP: closed physics of a few elements; no social/institutional layer; engine code is proprietary (Dark Engine source leak is not a licensable asset). Concept only.

## 5. Dwarf Fortress (material and body simulation)

What: text "raws" define creatures, materials, items, reactions, syndromes; the engine runs general systems over them. https://dwarffortresswiki.org/index.php/v0.31:Raw_file , :Reaction, :Syndrome [S via search; page fetch rate-limited]. Reaction = reagents (name, quantity, item token, material token) -> products, tied to a building [S]. Syndromes are defined inside the material or interaction they belong to and spread via contact, ingestion, inhalation, injection [S]. Our own synthesis already records the lesson (properties over categories, mixed resolution).

| # | Example | Cover | Why |
|---|---|---|---|
| 1 | Door | partly | doors are buildings with lock/forbid state; no handle mechanics |
| 2 | Chair | covers | furniture item with material weight [U] |
| 3 | Wall | covers | tile and material collision, can be mined or broken |
| 4 | Voice | partly | alerts and announcements, not sound propagation [U] |
| 5 | Helicopter | no | skills exist (dwarf skills gate job quality) but attempts are job-driven |
| 6 | Clock | covers | engine ticks: fluids, temperature, decay, syndromes |
| 7 | Org | partly | civilisations, sites and entities simulated at coarser resolution than fortress tiles (mixed resolution) [U] |
| 8 | Deciders | covers (code) | |
| 9 | Thinking | partly | thoughts and emotions logged as simulated state |
| 10 | Ramifications | covers | temperature, fluids, tissue damage cascades |

ADOPT: data-defined materials with typed property tokens; reactions as "inputs by property -> outputs" templates; syndromes as an exposure-route -> effect record attached to a substance (good template for "effect travels by contact/ingestion"); resolution tiers per system. GAP: closed, non-LLM, single-author-engine; raws are not an interchange standard; no open attempt. Maturity: Bay 12 closed source, free and paid builds; raws are moddable [U].

## 6. Caves of Qud

What: Roguelike where every object is a bag of composable "Parts" with event handlers; objects respond to fired events (spawn, move, attack, die). Bucklew describes "a set of properties composed together" rather than class hierarchy [S: Unity interview https://unity.com/resources/systems-driven-design-in-caves-of-qud]; modding docs list parts, mutations and skills all as Parts registering for events [S: https://wiki.cavesofqud.com/wiki/Modding:Events]. Talks: Bucklew "Data-Driven Engines of Qud and Sproggiwood" (IRDC 2015); GDC 2019 "End-to-End Procedural Generation in Caves of Qud" https://gdcvault.com/play/1025914; Grinblat GDC 2018 history generation [S]. Details of the event system beyond the wiki are unverified.

Coverage: Door partly (door part with open/lock events), Chair partly, Wall covers, Voice partly (noise/hearing parts [U]), Helicopter no, Clock covers (turn tick events), Org partly (factions with reputation as numeric state), Deciders code only, Thinking no, Ramifications covers (event cascades: fire, gas, liquid).

ADOPT: the part/event pattern is the most concrete model of "object owns its responses and subscribes to events": an event is fired AT an object, parts may veto or modify it (a part returning false stops the event). This is Inform's check/before/instead for arbitrary events. Factions as numeric reputation state is a cheap organisation proxy. GAP: C# in Unity, closed game, no formal separation of propose/commit. Maturity: commercial game, 1.0 released 2024 [U]; mod API only.

## 7. Entity Component System (Flecs, Bevy, Unity DOTS)

What: data = components on entities; behaviour = systems querying components. Flecs (C/C++ with bindings) adds first-class relationships (pairs) and observers: https://www.flecs.dev/flecs/Relationships.html [V], https://github.com/SanderMertens/flecs/blob/master/docs/ObserversManual.md [V headings]. Bevy: ECS Relationships (Relationship / RelationshipTarget, ChildOf) added in 0.16 https://bevy.org/news/bevy-0-16/ [V]; observers exist, with a "revamped observers API" planned as of that post [V].

Flecs details [V]: pair `(Eats, Apples)` lets an entity hold the same relationship to several targets; builtin `ChildOf` (deleting a parent deletes children) and one-way, transitive `IsA` (inheritance of components with override); relationship traits (transitive etc.) mentioned. Observers: OnAdd / OnSet / OnRemove, multi-event and multi-term observers, monitors, `yield_existing`, event propagation and forwarding along relationships, custom events, enqueue vs emit, observer ordering. Manual warns that using add/remove only to trigger observers is a bad pattern [V]. Bevy relationships are currently one-to-many only; many-to-many planned [V]. Unity DOTS (Entities package, https://docs.unity3d.com/Packages/com.unity.entities@latest) [U: not fetched; archetype ECS in C# with Burst/Jobs; no first-class relationships].

| # | Example | Cover | Why |
|---|---|---|---|
| 1 | Door | partly | components `Lockable`, `Open`; "may open" is a system/query predicate you write; ECS has no concept of attempt |
| 2 | Chair | covers | `Affords(Sit)` pair, `Capacity` component; entity never acts because it has no system |
| 3 | Wall | partly | `Solid` tag; failure semantics written by you |
| 4 | Voice | partly | custom event emitted with propagation along a relationship (Flecs event propagation/forwarding [V headings]); range rule is yours |
| 5 | Helicopter | no | |
| 6 | Clock | covers | systems/timers run on schedule |
| 7 | Org | partly | `(MemberOf, Firm)` pairs; boundary as a query over members; per-run switch = add a decider component to the Firm entity or not |
| 8 | Deciders | partly | decider component with implementation tag; fidelity is your convention |
| 9 | Thinking | partly | self-targeted `Attempt` entity |
| 10 | Ramifications | covers | observers on OnSet/OnAdd of `Position`/`Supported` etc. chain reactions; documented ordering |

ADOPT:
- Relationships as pairs (subject, relation, object) for containment, support, membership, ownership, knows, "on". Normalises our topology/permission/information edges; use the relationship vocabulary (IsA for kind inheritance, ChildOf for part-of with cascade-delete semantics, wildcard queries).
- Observers as the generic automatic-propagation mechanism: "when component X is set on any entity matching query Q, fire event E" with ordering and explicit enqueue vs immediate emit. Observers only PROPOSE patches to our commit boundary, never mutate directly. This directly implements example 10 and answers "narrator does not hold every step".
- The Attempt-as-entity pattern: an `Attempt` entity with (Actor, Target, Verb-sense) pairs is queryable, loggable, adjudicated by a system; fits the intent-recorded-never-read rule (intent is a component no system queries).
- Do not adopt the engine for the commit boundary itself: ECS gives no atomic validated patch or declared scopes, and Flecs only stores structure.
GAP: no attempt/adjudication, no information/perception model, no fidelity concept, no evidence trail. Command batching changes when events fire [V] which conflicts with our "atomic commit then observe" ordering unless wrapped.
Maturity: Flecs active (last push 2026-10-23, ~8.8k stars, MIT per LICENSE file; GitHub's SPDX field says NOASSERTION), C core with C++/C#/Rust bindings [V repo API; bindings U]. Bevy active (pushed 2026-10-24), Rust, dual MIT/Apache-2.0 (GitHub shows Apache-2.0) [V]. DOTS: Unity-proprietary, not suitable [U].

## 8. Tabletop adjudication (Blades in the Dark, GURPS, PbtA) as LLM-GM models

What: human GMs adjudicate free-form attempts with a thin procedure.

Blades in the Dark [V: https://bladesinthedark.com/action-roll]: roll only "when the PC is put to the test"; GM sets POSITION (controlled/risky/desperate, risky default) and EFFECT (limited/standard/great); dice pool = action rating dots, +1 assist (1 stress), +1 push (2 stress) or Devil's Bargain; highest die: 6 success, 4/5 success with consequence, 1-3 failure; critical = increased effect; consequences scale with position; PCs may RESIST a consequence (separate roll). The player's chosen action rating strongly shapes position and effect.
GURPS [S]: roll 3d6 under skill; untrained uses a DEFAULT derived from an attribute or related skill with a penalty that grows the less related it is; margin of success matters; defaults do not carry special benefits; example defaulting for unfamiliar vehicles -2. Exact familiarity rule not verified.
PbtA / Dungeon World [U: SRD URLs 404'd in this session]: "fiction first": a move triggers only when the fiction does the thing ("to do it, do it"); 2d6+stat, 10+ full, 7-9 with cost, 6- GM makes a move; GM principles include "ask questions" and "think offscreen".

| # | Example | Cover | Why |
|---|---|---|---|
| 1 | Door | partly | GM states preconditions informally ("it's locked") |
| 2 | Chair | partly | informal |
| 3 | Wall | covers | GM says "you can't"; no roll (roll only if uncertain with consequences) |
| 4 | Voice | partly | GM judgment |
| 5 | Helicopter | covers | untrained -> default/low pool, desperate position; outcome from recorded rating, not eloquence. Learning over rounds = progress clocks/XP [BitD clocks U] |
| 6 | Clock | covers | BitD "clocks" (segmented progress tracks) advance on schedule or on failure; also countdowns in PbtA [clocks U] |
| 7 | Org | covers | BitD crews and factions are rated entities, with faction clocks advancing "offscreen" [U] |
| 8 | Deciders | partly | GM plays NPCs; fidelity is one |
| 9 | Thinking | partly | "Study", "Attune"-style actions are targeted at self/fiction |
| 10 | Ramifications | partly | GM moves; "think offscreen" |

ADOPT (highest value for the LLM-GM seam):
- A uniform adjudication form: (1) does this attempt have uncertainty AND stakes? If neither, auto-succeed or auto-fail with reason (wall = no roll, simple door = no roll). (2) Position (risk) and Effect (magnitude) as two separate, GM-set, recorded fields. (3) Resolve from RECORDED rating + assistance + declared bargains with a published table (6 / 4-5 / 1-3). (4) Consequence selected from a typed list scaled by position. (5) Resistance as an optional reaction. This is exactly our attempt -> adjudication -> outcome split, with the LLM allowed only to choose position/effect from evidence and narrate, while the roll is code. Hard gates (phone number) belong before position as "requirements", like PbtA move triggers.
- Skill defaults (GURPS): untrained attempts are allowed with an attribute-based default minus relatedness penalty rather than refused. Handles example 5 (untrained flies and probably crashes) without a special case.
- Clocks: segmented progress trackers as the universal representation of slow learning, construction, and organisational plans (also usable for the Clock example). Learning a skill over several rounds = a clock whose completion raises a recorded rating.
- "Roll only when stakes" as a rule to avoid LLM over-adjudication cost.
GAP: depends on a human's judgment for position/effect and for what counts as a trigger; no world model. Pure procedure, license: BitD SRD is CC-BY-licensed [U]; check before copying text.

## 9. Cross-cutting findings

1. Nobody offers all ten. The closest *shape* match to our commit boundary is Inform's check/carry out/report plus Qud/ECS event propagation; the closest *procedural* match for the LLM seam is BitD's action roll; the closest *data* match is DF raws/Sims ads.
2. The common structure: object-local declarations of (preconditions, effect proposal, observation) + a global stimulus/event propagation layer + a thin adjudication procedure. We already have the middle (transition authority + commit); the missing parts are the first and third.
3. Menu vs attempt: all of these (except tabletop) bind the player to an action vocabulary. Our "attempt anything" needs a fallback path when no mechanic matches: classify as (a) auto-fail by world rule (wall), (b) unmodelled -> GM authority with declared fidelity "coarse", flagged, rate-limited. Tabletop does this by default; IF engines print "I don't understand".
4. Organisation (example 7) is only served by tabletop (BitD factions) and ECS pair-membership. ADR-006's derived-boundary approach plus an optional "surrogate decider" component is consistent with ECS membership pairs.
5. Fidelity declaration (example 8) is not found in any of these; keep our `implementation_id` and add a `fidelity` field. Gap persists.

## 10. Ranked recommendation (what to adopt)

1. Blades-in-the-Dark action-roll procedure plus GURPS defaults plus clocks, as the adjudication contract for the LLM GM (position, effect, rating, bargain, outcome table; code does the dice; hard-gate requirements before the roll). Covers examples 3, 5, 6, 7 (faction clocks), and slow learning. Source verified for BitD, GURPS defaults only partially.
2. Inform 7 check / carry out / report (plus before / instead / after interceptors and `try`) as the shape of every installed mechanic. It maps onto propose/validate/commit/observe and gives a reasoned-refusal outcome class. Examples 1, 2, 3, 10. Source verified.
3. ECS relationship pairs and observers as the propagation and structure vocabulary (Flecs manual as reference; do not embed an ECS engine). Observers propose patches; they never write. Examples 2, 4, 7, 10. Source verified.
4. TADS 3 preCond (state-satisfying preconditions) and remap (attempts on parts redirect), plus sense connectors for sound. Examples 1, 4. Partly verified; read the adv3 manual before citing.
5. Sims-style advertisements as a relevance-filtered affordance hint channel (never a gate), and "invisible object" world-process entities. Example 2, 6. Primary body text not verified.
6. Stimulus/response table shape (Dark Engine/BotW), DF reactions and syndromes, Qud event-veto parts as data patterns to borrow when writing the propagation mechanics. Unverified specifics; verify before design.

Not adopt as runtime: Inform, TADS, Qud, DF, Unity DOTS (closed, parser/turn-bound, or proprietary). Flecs/Bevy are usable as hosts but neither supplies atomic validated commit; consistent with Decision 006 ("do not add engine capability of our own; host on commodity runtimes").

Biggest unresolved gap across all eight: attempts that match no installed mechanic, and declared per-decider fidelity. Next verification targets: Dark Engine stim/response docs, adv3 manual sense chapter, Forbus/Wright paper body (PDF saved in the session scratchpad, text not extracted), Dungeon World SRD, BitD clock rules and SRD licence.
