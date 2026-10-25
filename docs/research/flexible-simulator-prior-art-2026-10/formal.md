# Formal simulation and agent theory: prior art survey (scope: formal)

Date: 2026-10-24. Verified = fetched/seen this session. "Unverified" = from background knowledge only.
Tests: 1 Door, 2 Chair, 3 Wall, 4 Voice, 5 Helicopter, 6 Clock, 7 Org granularity, 8 Decider fidelity, 9 Thinking-as-action, 10 Ramification.

## 0. What we already have (read first)

- ADR-013 (cybernetic_influence_v3/docs/adr/013-generalized-simulator-foundation.md, accepted): Concordia owns the lifecycle. Standard path is world truth -> authorized observation -> open semantic intent -> declared *transition authority* (deterministic / stochastic / LLM / external / scripted / replayed; declares read/write, fidelity, invalid questions) -> structured patch -> generic validation -> atomic commit or visible rejection -> per-actor observation + evidence. Capability / permission / attempt / adjudication / outcome are distinguished "where the question requires".
- ActiveSystemSpec (active_runtime/models.py ~l.61): per-entity observation ports, output ports, required outputs, `activation_observation_port_ids` (what wakes it), `initial_next_update_at` (self-schedule), `output_port_unavailable_when` (state conjunction that withdraws an output; commented as "technical availability, not permission"). This is already DEVS-shaped (ports + external wake + scheduled internal wake) but not named as such.
- ADR-006: organisations are reversible derived coarse-grainings over members, never executors; boundary input/output = routed effect crossing the membership boundary; collapse must report what it hides.
- world-substrate: Engine proposes/validates/commits with declared write scopes (reads recorded, not enforced); refusals are history; PDDL spike 2026-10-05 verdict "compose" (unified-planning 1.3.0 + ENHSP validate/plan authored mechanics offline; cannot host runtime: no visibility, write scopes, refusals-as-history, open worlds). SimPy selected for scheduling only. off-the-shelf-candidates (09-25) lists PDDL, effect systems, PROV-O, Halpern-Pearl, Mesa as "not yet evaluated"; none of DEVS, event calculus, C+/BC, BFO, ODD, Levin appear as candidates (grep found only Levin as a detachable analysis plugin).
- Net: the *shape* (attempt, authority, patch, commit) exists. What is missing is (a) a formal vocabulary to name it, (b) an automatic-ramification mechanism (test 10), (c) a skill/knowledge gate model (test 5), (d) a decider-fidelity declaration standard (test 8).

---

## 1. DEVS / Parallel DEVS (Zeigler)

What: Formalism where an atomic model has state, time-advance `ta`, internal transition `delta_int`, external transition `delta_ext`, confluent `delta_con` (Parallel DEVS), output `lambda` (emitted only before an internal transition), and input/output ports; coupled models wire ports and are closed under coupling (a coupled model is itself an atomic-equivalent). Primary: Zeigler, Praehofer, Kim, *Theory of Modeling and Simulation* (Academic Press, 2000; book, not fetched, unverified details). Implementation doc verified: https://github.com/iscar-ucm/xdevs.py

| # | Verdict | Why |
|---|---|---|
| 1 Door | covers | Pure external-transition model: state changes only on input port events, never self-triggers. Preconditions (unlocked, handle down) are guards in `delta_ext`; failure is a no-op (or a "refused" output). |
| 2 Chair | partly | Passive model with no `ta`=infinity and no internal transitions fits "never acts"; "affords sitting" and weight limit are state/guard conventions, not DEVS concepts. |
| 3 Wall | partly | A wall model can absorb "move" inputs and emit a refusal. DEVS has no notion of who may send what; world-decides-effect is a modelling choice, not enforced. |
| 4 Voice | partly | Port coupling with a propagation model (sound medium as a coupled model with range-limited routing) works; intent stays in the message payload. DEVS neither forbids nor records the intent/effect split. |
| 5 Helicopter | no | Skill/held-fact gates are just state; nothing in DEVS helps. |
| 6 Clock | covers | This is exactly the internal transition: `ta` = period, `lambda` emits tick, `delta_int` advances. Door vs clock = external-only vs internal. Best fit of any framework. |
| 7 Org granularity | covers | Closure under coupling: a firm is either an atomic model or a coupled model of members, and a coupled model is behaviourally substitutable. Consistent with ADR-006 (boundary = coarse-graining), but DEVS "morphisms/ homomorphism" for checking that the coarse model agrees with the fine one is the real prize (unverified in detail). Dynamic-structure DEVS (DSDEVS) allows swapping per run. |
| 8 Deciders | partly | A decider is just an atomic model whose `delta_ext` calls an LLM or code; fidelity labelling is not in the formalism. Real-time xDEVS can couple wall-clock I/O (verified). |
| 9 Thinking | partly | Self-loop: model sends to its own input port, or does it in `delta_int`. Nothing special. |
| 10 Ramification | partly | Chained coupling gives cascades (glass pushed -> position model -> falls -> breaks) but you must author every coupling; no automatic derivation from state constraints. Simultaneous events handled by `delta_con` + the Select function (tie-breaking), which is genuinely useful for determinism. |

ADOPT
- Vocabulary: external transition / internal transition / confluent transition / time advance / output-before-internal / ports / closed under coupling. Use it to name what ActiveSystemSpec already does and to document door-vs-clock in one sentence.
- Rule: output happens only at internal transitions (Classic) / produced by lambda; inputs only via ports; this matches "world decides, agent only emits".
- Deterministic tie-break for simultaneous events (confluent function or Select) - cheap, solves ordering disputes in the commit loop.
- Optionally use xDEVS or PythonPDEVS as the *event executive* instead of SimPy for scheduling-only (they already model ports/coupling), but SimPy decision is already made; evaluate only if port wiring becomes hand-rolled.

GAP: no affordance/capability concept, no permission vs attempt, no knowledge/skill gating, no automatic consequence closure, no provenance or refusal history; models are authored code, not data.

Maturity: xdevs.py: Python, GPL-3.0, PyPI 3.0.0, last push 2026-09-30 (GitHub API, verified). GPL is a licensing constraint for adoption as a dependency. PythonPDEVS: Python, Apache-2.0 docs (verified from MSDL docs search result) at https://msdl.uantwerpen.be/documentation/PythonPDEVS ; defaults to Parallel DEVS, Classic optional; not on PyPI (pip found no pypdevs); GitHub mirror capocchi/PythonPDEVS last push 2018 (Apache-2.0) - effectively unmaintained mirror, maintenance of the MSDL git unverified. DEVSimPy (capocchi, GPL-3.0, pushed 2026-10-07) is a GUI around DEVS. Conclusion: adopt the formalism, not necessarily a library.

---

## 2. Event Calculus (Kowalski-Sergot; Shanahan; Mueller)

What: Logic formalism with `Initiates(e,f,t)`, `Terminates`, `HoldsAt(f,t)`, `Happens(e,t)`, `Releases` (non-inertial fluents), and state constraints for indirect effects (ramifications). Frame problem solved by circumscription/inertia (default persistence). Primary: Mueller, *Commonsense Reasoning* (Elsevier); DEC Reasoner https://decreasoner.sourceforge.net/ (verified exists; CPL 1.0, C and Python, SAT-based; supports deduction, abduction/planning, postdiction, model finding; ASP port via clingo exists as a prototype "no longer updated" - verified from search result). Shanahan 1999 "The Event Calculus Explained" - unverified.

| # | Verdict | Why |
|---|---|---|
| 1 Door | covers | `Initiates(Open(d), Opened(d), t)` with a precondition axiom `Happens(Open) -> HoldsAt(Unlocked) & HoldsAt(HandleDown)`. Event calculus also distinguishes "attempt happened" from "effect initiated" if you model only Initiates conditions. |
| 2 Chair | partly | Static `Affords(sit)` fluent plus a weight constraint; fine, but no built-in affordance semantics. |
| 3 Wall | covers | No `Initiates(Walk, Position)` axiom fires when `HoldsAt(Solid(w))`; inertia keeps the person in place. Attempt-with-no-effect is the default in EC. |
| 4 Voice | partly | `Happens(Shout)` with a trigger axiom that creates `Heard(x)` only for x within range; intent as a ground term never referenced by axioms. Works, but you author the range rule. |
| 5 Helicopter | partly | Probabilistic outcomes are not in classical EC (probabilistic extensions exist; unverified). Skill as fluent plus a threshold rule is expressible; stochastic crash needs an external die. |
| 6 Clock | covers | `Happens` can be generated by periodic trigger axioms or narrative; DEC has `Happens` with time axis and trajectory/continuous change (Trajectory axioms). |
| 7 Org | no | Not addressed. |
| 8 Deciders | no | Not addressed. |
| 9 Thinking | partly | Mental events/fluents (Mueller models beliefs and sensing in chapter on mental states, unverified) - possible. |
| 10 Ramification | covers | State constraints + `Releases` + causal trigger axioms ("when X holds, event Y happens") give automatic indirect effects; EC literature handles the ramification problem directly (Shanahan; Mueller ch. on state constraints; unverified chapters). |

ADOPT
- The *Initiates / Terminates / Releases / HoldsAt* vocabulary for effects as "changes to inertial fluents", with default persistence (frame solution) - this is precisely the discipline "only the declared write scope changes".
- Trigger axioms ("event-generating rules": when a fluent configuration holds, an event Happens at t+delta) as the mechanism for automatic propagation (test 10). Keep it as a world-rule layer that fires after each commit until quiescence.
- Distinction of inertial fluents vs. "released" (free) fluents vs. derived/state-constraint fluents (computed, not stored). Cleanly tells the engine what must be recomputed.

GAP: Reasoners are batch/SAT (query a whole timeline), not an incremental runtime; DEC Reasoner is SourceForge, CPL, little maintenance (last release date not verified). No agent/authority/visibility model. Treat as a specification language, not a runtime.

Maturity: DEC reasoner Python/C, Common Public License 1.0, SourceForge, activity unverified. Dormant.

---

## 3. Situation Calculus / Golog (Reiter)

What: Second-order logic of actions: situations are action histories `do(a,s)`; fluents are situation-dependent; precondition axioms `Poss(a,s)`; *successor state axioms* give frame-problem solution by collecting all effect axioms per fluent (Reiter's solution); Golog/IndiGolog are agent programming languages on top. Primary: Reiter, *Knowledge in Action* (MIT Press, 2001) - unverified directly; successor state axiom form confirmed from AAAI/Toronto papers in search results (e.g. https://www.cs.toronto.edu/~sheila/publications/fri-bai-mci-kr08.pdf).

| # | Verdict | Why |
|---|---|---|
| 1 Door | covers | `Poss(open(d),s) <=> unlocked(d,s) & handleDown(d,s)`. A clean precondition-vs-attempt split: attempt is outside Poss. |
| 2 Chair | partly | Affordance as fluent. |
| 3 Wall | covers | Successor state axiom for position has no effect clause when blocked. |
| 4 Voice | partly | As EC. |
| 5 Helicopter | partly | Stochastic Situation Calculus (Bacchus/Halpern/Levesque; Reiter ch. on stochastic actions, unverified) is the formal way to add probabilistic outcomes keyed on state; knowledge via epistemic situation calculus (Scherl-Levesque) is the formal "held facts gate". |
| 6 Clock | partly | Natural actions / time exist (Reiter ch. 7 "Time, Concurrency, and Processes", unverified) but clumsy. |
| 7 Org | no | |
| 8 Deciders | partly | Golog/IndiGolog = agent programs interleaving sensing and acting; deciders as programs. |
| 9 Thinking | partly | Epistemic extension: knowing/sensing actions change `K` fluent; "think" = action that updates K. |
| 10 Ramification | partly | Needs explicit indirect-effects extension (state constraints compiled into successor state axioms; Lin, McIlraith; unverified). |

ADOPT
- Successor state axiom pattern: *one rule per state variable collecting every action that can change it* - gives a precise checkable meaning to "effects confined to declared writes" and lets a validator find all mechanics that may touch a field (answers the "reads recorded not enforced" gap indirectly).
- `Poss` (possible) separate from "attempt" - vocabulary already in ADR-013.
- Epistemic variant (knowledge fluent K, sensing actions) as the theory for held-fact gates and "thinking" as a self-directed epistemic action.

GAP: Logic-only; practical implementations are Prolog (ECLiPSe/SWI) academic code, mostly dormant (unverified per project). Centralised omniscient theory, same as the PDDL spike's limitation.

Maturity: theory mature; implementations (IndiGolog, ReadyLog) academic, status unverified.

---

## 4. Action languages C+ and BC / BC+ (causal laws, ASP)

What: Declarative languages for transition systems with *causal laws* (`caused F if G after H`, `inertial F`, `nonexecutable A if G`); static laws derive indirect effects (ramifications) from definite causal explanation; compile to ASP or SAT. CCalc (C+), CPLUS2ASP (C+ and BC+). Primary: Lee, Lifschitz, Yang, "Action Language BC: Preliminary Report", IJCAI 2013 (verified bibliographic record https://mlanthology.org/ijcai/2013/lee2013ijcai-action); Babb & Lee, "Action Language BC+", AAAI 2015 / TPLP (https://ojs.aaai.org/index.php/AAAI/article/view/9405); Giunchiglia et al., "Nonmonotonic causal theories", AIJ 2004 (unverified fetch).

| # | Verdict | Why |
|---|---|---|
| 1 Door | covers | `nonexecutable open(D) if locked(D)`; `open(D) causes opened(D)`. |
| 2 Chair | partly | Static fluent. |
| 3 Wall | covers | `nonexecutable` or silent absence of effect; inertia default. |
| 4 Voice | partly | Concurrent actions allowed (C+ supports concurrency); range via static laws. |
| 5 Helicopter | partly | Probabilistic extension exists (pBC+, LPMLN-based; appeared in TPLP search result, only titles seen) but is research. |
| 6 Clock | partly | Exogenous / "caused by default" actions can model clock ticks; no native time-advance semantics. |
| 7 Org | no | |
| 8 Deciders | no | |
| 9 Thinking | partly | Ordinary action. |
| 10 Ramification | covers | Strongest: static causal laws `caused broken(G) if falling(G) & onFloor(G)`; closure under causal laws is the definition of the transition, so indirect effects are *part of the semantics*, not an add-on. Also gives principled treatment of "cause" (no spontaneous truth: everything true must be caused or inertial). |

ADOPT
- Principle of *causal explanation*: a fact changes only if some rule causes it or inertia keeps it; reject patches with unexplained changes. Maps to "commit validates declared invariants" and to the existing causal-parent evidence.
- Three law types as the minimum mechanism taxonomy: dynamic laws (action causes effect), static laws (fluent derived from fluents = ramification), executability constraints. Use as the schema for a ramification layer: static laws re-evaluated to fixpoint after each commit.
- Concurrency (several agents' attempts in one step) with explicit conflict handling.
- Clingo as an optional offline checker (like the existing PDDL validator spike); clingo 5.8.2, MIT, last push 2026-10-24 (verified, maintained). Telingo (temporal ASP) unverified.

GAP: Closed, grounded finite domains (same open-world objection as the PDDL spike); no visibility; no stochasticity in mainstream versions; grounding blow-up. CPLUS2ASP repos: babb517/cplus2asp (pushed 2015, NOASSERTION), azreasoners/Cplus2ASP (pushed 2024-12-31) - low maintenance; a 2026 arXiv paper (2605.09528, title seen in search result, not read) suggests it is still referenced.

---

## 5. PDDL / STRIPS and PDDL+ (processes and events)

What: STRIPS/PDDL actions = parameters, preconditions, add/delete (or assign) effects; PDDL2.1 adds numeric fluents and durative actions; **PDDL+** (Fox & Long, JAIR 27, 2006, https://arxiv.org/abs/1110.2200, verified via search) adds **autonomous processes** (continuous change whenever preconditions hold) and **exogenous events** (instantaneous, fire when preconditions become true; not chosen by the agent) with hybrid-automaton semantics. The environment, not the planner, triggers them - exactly the "world decides" part.

| # | Verdict | Why |
|---|---|---|
| 1 Door | covers | Action `open` with preconditions. |
| 2 Chair | partly | Predicate; weight is numeric fluent. |
| 3 Wall | covers | Precondition unmet -> action inapplicable, i.e. simply not executable (note: PDDL treats it as not-in-the-menu, which is the thing Brian does NOT want; the attempt must still be *recorded and fail*. Spike confirmed refusal-as-history absent). |
| 4 Voice | no | No knowledge/visibility. |
| 5 Helicopter | no | Deterministic; PPDDL/RDDL exist for probabilistic (unverified). |
| 6 Clock | covers | PDDL+ process (e.g., `increase time (* #t 1)`) and events (`when time=T`): the formal "internal transition". |
| 7 Org | no | |
| 8 Deciders | no | |
| 9 Thinking | no | |
| 10 Ramification | covers (PDDL+ events) / partly | PDDL+ *events* fire automatically on state (glass falls once unsupported) and processes continue; also PDDL axioms (derived predicates, PDDL2.2) give derived-fact ramification. |

ADOPT
- PDDL+ taxonomy of change sources: **actions** (agent-chosen) vs **events** (instant, state-triggered, exogenous) vs **processes** (continuous while true). This is the cleanest published split for "who may trigger what" and for automatic propagation; make it the vocabulary for mechanic kinds.
- Keep the 2026-10-05 spike verdict: export authored mechanics to PDDL via unified-planning (1.3.0, Apache-2.0, pushed 2026-10-22, verified) for offline validation/reachability. Add events/processes to the translator when ramification layer exists; ENHSP supports PDDL+ (unverified for current version; UPMurphi / DiNo are PDDL+ planners, mention only from search result).
- Derived predicates (axioms) for computed state.

GAP: Already listed in the spike: no visibility, scopes, history, open world. Planner-oriented (find a plan), not simulator-oriented; PDDL+ solvers are slow (hybrid reachability). VAL validator: BSD-3, last push 2021-10-18 (verified; stale).

Maturity: unified-planning Python Apache-2.0 active; ENHSP Java; PDDL+ planners academic.

---

## 6. Russell & Norvig agent model (PEAS, environment properties)

What: Agent = architecture + program mapping percept sequence to action; sensors/actuators; PEAS (Performance, Environment, Actuators, Sensors); environment properties: fully/partially observable, single/multi-agent, deterministic/stochastic, episodic/sequential, static/dynamic, discrete/continuous, known/unknown; agent types (simple reflex, model-based, goal-based, utility-based, learning). Primary: *Artificial Intelligence: A Modern Approach*, 4th ed. (Pearson, 2020), ch. 2 (book; unverified fetch, standard content). Site: https://aima.cs.berkeley.edu/ (not fetched).

| # | Verdict | Why |
|---|---|---|
| 1-3 | no | Objects are environment, not modelled beyond "environment state". |
| 4 Voice | partly | Sensor/actuator split: speaking is actuator, hearing is sensor mediated by environment. Good framing for intent-vs-effect. |
| 5 Helicopter | partly | "Environment decides outcome; agent only selects act" is the interface; skill is inside agent/environment state. |
| 6 Clock | partly | Clock = agent with trivial program (simple reflex on time percept), or a dynamic-environment process. |
| 7 Org | partly | Multi-agent environment discussion (cooperative/competitive); no boundary notion. |
| 8 Deciders | covers | Agent function independent of implementation; "agent program" may be table, rules, LLM, learner. The agent-types ladder is a fidelity vocabulary (reflex -> model-based -> goal -> utility -> learning). |
| 9 Thinking | partly | Internal state update in model-based agents; "action" restricted to actuators. |
| 10 | no | |

ADOPT
- Percept / action interface contract (agent never touches world; world returns percepts) - already in ADR-013.
- Environment-property checklist as a per-world declaration (observable? deterministic? static vs dynamic? multi-agent?) in the ODD-like world description; "dynamic" = the world advances while the agent deliberates, directly relevant to LLM latency (needs clocks tied to simulated, not wall time).
- Agent-type ladder as the labelled fidelity levels for test 8 (reflex code / model-based typed model / goal-based LLM).

GAP: Textbook; no executable artifact, no object model.

---

## 7. BFO (Basic Formal Ontology; dispositions, functions, capabilities, realization)

What: ISO/IEC 21838-2 top-level ontology: continuants (independent, specifically dependent: qualities and *realizable entities* = dispositions, roles, functions) vs occurrents (processes). A disposition is borne by a bearer, exists even when not manifest, and is *realized* in a process of a matching type. Primary: BFO-2020 repo https://github.com/BFO-ontology/BFO-2020 (verified, pushed 2026-10-06; license field not reported by API, commonly CC BY 4.0, unverified); ISO/IEC 21838-2 (unfetched; the search did not return the text). Directly relevant: Beverley, Limbaugh, Merrell, Koch, Smith, "Capabilities: An Ontology" https://arxiv.org/abs/2405.00183 (verified abstract: dispositions are tendencies/powers; capabilities are the subset whose realizations we care about).

| # | Verdict | Why |
|---|---|---|
| 1 Door | covers (conceptually) | Door bears a disposition (to open) whose realization requires a trigger process and conditions; present even while locked. Distinguishes *having* the disposition from *its realization happening*. Cannot trigger itself: dispositions are realized only in triggering processes. |
| 2 Chair | covers | Chair bears a disposition/"affordance to support sitting"; weight limit = disposition threshold; chair never acts. Roles/functions (designed for sitting) separate from dispositions. |
| 3 Wall | covers | Solidity = disposition to resist penetration; an attempted walk = process in which that disposition is realized (as resisting). Attempt is an event that happens regardless. |
| 4 Voice | partly | Speech process, sound process; ontology gives vocabulary, not propagation. Intent is a mental quality/disposition of the speaker, orthogonal to causal process. |
| 5 Helicopter | covers (concept) | Pilot bears a capability (skill) = disposition realized in flying; recorded skill is a quality/disposition of the person; acquiring skill = process changing the disposition. Capabilities paper formalises exactly this. Probabilities are out of scope. |
| 6 Clock | partly | Clock bears a disposition realized by self-sustaining process (periodic process); BFO has no scheduler. |
| 7 Org | covers (vocabulary) | Organisation as object aggregate vs independent continuant with members; BFO extension (Common Core Ontologies, unverified) models organisations; supports both views. |
| 8 Deciders | no | |
| 9 Thinking | partly | Mental processes are occurrents with the agent as participant and themselves as bearer (via IAO/mental-process extension, unverified). |
| 10 Ramification | partly | Dispositions realized by processes that in turn trigger other dispositions give the chain structure (glass has fragility disposition, realized when impact process occurs), but no execution. |

ADOPT
- **Disposition (latent, exists while not manifest) vs. its realization (a process that occurs when triggered under conditions)** as the canonical model for door/chair/wall/helicopter/skill. Add "trigger", "realization conditions", and "bearer". This gives ADR-013's capability vs attempt vs outcome a standard grounding: capability = disposition; attempt = trigger event; outcome = realization (or non-realization).
- Use the **Capabilities: An Ontology** (Beverley et al. 2024) definitions for skill/capability vocabulary, citing them rather than inventing.
- Separate *function* (designed-for, a social/teleological fact) from *disposition* (physical) and *role* (contextual, externally conferred): chair function = sitting-support; role = "seat of the chairman". Prevents conflating "affordance" with "authorisation" (ADR-013 permission).
- Keep BFO as a **vocabulary / sanity check for the type system**, not a runtime. Use OWL file from BFO-2020 repo if an ontology export is wanted.

GAP: Descriptive ontology, no dynamics, no probabilities, no triggers semantics beyond "realization conditions". Debate on whether function is a kind of disposition (FOUST, from search snippet). BFO 2020 limitations on dependent-continuant realizables noted in arXiv 2506.17085 (snippet only).

Maturity: standard; OWL artefacts maintained (BFO-2020 repo active 2026-10); no simulation code.

---

## 8. ODD protocol (Overview, Design concepts, Details)

What: Standard documentation protocol for agent-based and other simulation models; 2020 second update (Grimm et al., JASSS 23(2):7, https://www.jasss.org/23/2/7.html, verified via search) adds guidance for complex models, rationale and evaluation sections, links to code. Element list (purpose and patterns; entities, state variables, scales; process overview and scheduling; design concepts; initialization; input data; submodels) is from background knowledge, unverified in this session. Design concepts (basic principles, emergence, adaptation, objectives, learning, prediction, sensing, interaction, stochasticity, collectives, observation) likewise unverified.

| # | Verdict | Why |
|---|---|---|
| 1-3 | no | Documentation, not a mechanism. |
| 4 Voice | partly | "Sensing" and "interaction" design concepts force you to state what agents can perceive/who they interact with. |
| 5 Helicopter | partly | "Adaptation/learning" concepts demand declaration of skill change rules. |
| 6 Clock | partly | "Process overview and scheduling" declares which processes run when and in what order. |
| 7 Org | covers (documentation) | "Collectives" design concept names exactly the question of aggregate vs individual entities. |
| 8 Deciders | covers (documentation) | "Objectives", "prediction", "adaptation" force declaring decision model and its fidelity. |
| 9 | no | |
| 10 | no | Scheduling order is declared, propagation not. |

ADOPT
- Use ODD headings as the **required metadata card of every world/run** (purpose, entities & state & scales, scheduling, design concepts incl. sensing/collectives/stochasticity/observation, initialization, input data, submodels); this is a field-standard way to satisfy "declare fidelity and assumptions" (ADR-013) and automatic replay catalogue. The 2020 version's "rationale" and "evaluation" additions fit the non-prediction caveat in ADR-013.
- ODD+D (decision-making extension, Müller et al. 2013, unverified) specifically for human-decision documentation.

GAP: Documentation only, no machine-readable schema (as far as verified); no code.

Maturity: community standard, widely used; Mesa/NetLogo ecosystems reference it.

---

## 9. Levin: TAME and the "spectrum of agency"

What: Levin, "Technological Approach to Mind Everywhere" (Front. Syst. Neurosci. 16:768201, 2022; https://arxiv.org/abs/2201.10346, https://www.frontiersin.org/articles/10.3389/fnsys.2022.768201/full). Verified from the text: agency is graded not binary; the paper's term is "axis of persuadability" (Figure 2), not "spectrum of persuadability"; rungs: A physical rewiring only (e.g. mechanical clock), B setpoint-based control (homeostatic circuit; goal encoded in setpoint), C training/reinforcement (animals), D rational persuasion (humans). "Cognitive light cone" = boundary of an agent's area of concern (Figure 4). The empirical stance: the right level of agency is decided by which interventions work, so the classification is by what the observer must do to change behaviour.

| # | Verdict | Why |
|---|---|---|
| 1-3 | partly | Door/chair/wall are rung A (change only by rewiring); the framework explains why they need no decider. |
| 4 Voice | partly | Cognitive light cone = scope of concern of an agent; sound/intent range separate. |
| 5 Helicopter | partly | Skill learning corresponds to training rung C. |
| 6 Clock | covers (labelled) | Levin explicitly uses mechanical clocks as lowest rung. Clock acts on schedule without any persuadability. |
| 7 Org | covers (labelled) | Multiscale competency: collective as agent depends on scale of observation; matches "boundary over members" and Levin-informed analysis already in ADR-013/006. |
| 8 Deciders | covers (labelled) | The rung gives a declared *kind* of decider: rewire-only / setpoint (typed controller) / learner / LLM (persuadable by argument). Directly supplies the "fidelity declaration" taxonomy by control interface. |
| 9 Thinking | partly | Cognitive light cone expansion; no mechanism. |
| 10 | no | |

ADOPT
- Per-entity "how may it be influenced" tag (rewire-only, setpoint, trainable, persuadable) as a decider-fidelity/ agency-level field, with the clock at rung A and LLM person at D. Cite TAME, mark as taxonomy (not mechanism).
- "Cognitive light cone" as the declared horizon of what an agent models/concerns itself with; compatible with observation ports.
- Treat agency level as chosen per run by the observer (matches org granularity per run).

GAP: Conceptual, empirical-biology framework; no formal semantics or code; evidence in-repo already treats Levin as detachable analysis overlay (living-world-projection note), so adoption stays at vocabulary/analysis layer.

Maturity: published paper; no software.

---

## 10. Cross-cutting matrix (best single source per test)

| # | Best framework | Residual gap (needs our own glue) |
|---|---|---|
| 1 Door | BFO (concept) + Situation Calculus Poss / C+ `nonexecutable` (rule); DEVS for ext-only | Attempt-that-fails must be recorded (none of the planners do this; ADR-013 does). |
| 2 Chair | BFO disposition/function | No runtime. |
| 3 Wall | C+/EC default-inertia | Same as 1. |
| 4 Voice | R&N sensor/actuator + DEVS port coupling | Propagation model authored; "intent logged, never read" is our policy (unprecedented in the survey). |
| 5 Helicopter | BFO capability + stochastic/epistemic Sit. Calc. | Skill-gated probability tables; learning over rounds; nothing off-the-shelf. |
| 6 Clock | DEVS internal transition; PDDL+ process | Already in SimPy/ActiveSystemSpec. |
| 7 Org | DEVS closure under coupling; Levin; ADR-006 | Equivalence check coarse vs fine (DEVS morphism, unverified depth). |
| 8 Deciders | R&N agent types; Levin rungs | Declaration schema is ours. |
| 9 Thinking | Epistemic Sit. Calc.; R&N model-based agent | Self-directed action convention. |
| 10 Ramification | C+/BC+ static laws; EC trigger axioms; PDDL+ events | An incremental fixpoint engine over our typed patch; none of the logic tools are incremental runtimes. |

## 11. Ranked recommendation

1. **C+/BC+ causal-law taxonomy + Event Calculus trigger axioms for the ramification layer (test 10).** Biggest hole in our stack. Implement natively as post-commit static/trigger rules iterated to fixpoint, inside the same atomic commit (so scopes/evidence still apply). Use clingo (MIT, maintained) only as an offline cross-check, as the PDDL spike did. Do not adopt CCalc/DEC runtime.
2. **DEVS vocabulary** (external/internal/confluent transition, ports, closure under coupling, tie-break). Zero-code, names what ActiveSystemSpec already does and settles door-vs-clock and organisation-as-coupled-model. Only consider xdevs.py (GPL-3.0) or PythonPDEVS as an executive if SimPy proves insufficient.
3. **BFO disposition/realization/function/role vocabulary with the Beverley et al. capabilities paper** to ground ADR-013's capability/permission/attempt/outcome and the chair/door/helicopter tests; use as naming standard and sanity check, not runtime.
4. **PDDL+ action/event/process classification** for mechanic kinds; extend the existing unified-planning export to events/processes for offline validation.
5. **Situation Calculus successor-state-axiom discipline and its epistemic extension** as theory for write-scope enforcement and for held-fact/skill gates and thinking-as-action. Theory only.
6. **ODD (2020 update) as the mandatory world/run description card**, and **R&N environment properties + Levin persuadability rungs** as the fidelity/agency declaration fields.

Honest conclusion: no surveyed framework gives the whole bundle. None record failed attempts as first-class history, enforce visibility, gate on recorded skill stochastically, or run incrementally with LLM deciders. The appropriate move is to adopt names and laws (items 1-6) and keep the existing engine. Sources I could not open: Zeigler book, Reiter book, Mueller book, ISO 21838-2, AIMA, Shanahan, ODD element list (all unverified, content from background knowledge).
