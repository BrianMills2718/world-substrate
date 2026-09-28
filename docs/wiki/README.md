---
schema_version: project-wiki/v1
type: ProjectWiki
role: derived-navigation
status: active
reviewed_through: 2026-09-18
authority_refs:
  - ../../README.md
  - ../../roadmap/README.md
  - ../architecture.md
  - ../decisions/001-project-scope.md
  - ../decisions/002-observability-and-replay.md
  - ../decisions/003-semantic-mechanical-boundary.md
  - ../decisions/004-product-and-adoption-strategy.md
  - ../decisions/005-native-waltzman-delivery.md
---

# World Substrate project wiki

This is the single compact orientation surface for the repository. It summarizes current truth and routes readers to native authorities; it does not replace architecture, contracts, decisions, code, evidence, or the roadmap.

## What this project is

World Substrate is a persistent, observable simulation engine and generative authoring system. Human or model policies express intents; installed mechanics with explicit local authority determine canonical consequences.

The product direction is now a **generative living-world builder over a rigorous causal engine**. The user should be able to describe a world conversationally, review represented structure and executable law, run residents/processes through it, watch it evolve spatially, and inspect why outcomes occurred without allowing presentation, cognition, or analysis to become alternate truth.

The product being demonstrated is **World Substrate**. **Waltzman Coordination Lab is its current showcase/reference world**, inspired by Cybernetic Influence v3 and Waltzman's *From Minds to Coordination*; Cybernetic Influence is research lineage, not the product or demo surface. Its first integrated local gate runs through canonical World Substrate state/events. Waltzman-specific trust structure, perceived risk, coordination readiness, detection/diagnosis/stabilization, and evasion analysis remain detachable plugins over evidence rather than universal world variables.

Public surfaces:

- World Builder: `https://brianmills.dev/world-builder/`
- Promoted Waltzman stakeholder demo: `https://brianmills.dev/waltzman/`
- Legacy standalone living-world URL: `https://brianmills.dev/world-substrate-visualization/`

The stakeholder demo is already promoted: it combines natural-language authoring, a fresh retained run, and living inspection through the bounded Cybernetic V3 donor path. That route remains useful regression/fallback evidence, but [Decision 005](../decisions/005-native-waltzman-delivery.md) makes native World Substrate convergence the active product frontier: one-shot text -> editable draft -> approved mechanics -> native Engine run -> automatic generic UI -> bounded Waltzman inspection/comparison. The old standalone URL remains legacy/design evidence.

## Start here

| Need | Read next |
| --- | --- |
| Current direction / exact next action | [Roadmap](../../roadmap/README.md) |
| Durable system boundaries | [Architecture](../architecture.md) |
| Product + procurement doctrine | [Decision 004](../decisions/004-product-and-adoption-strategy.md) |
| Native Waltzman delivery / donor boundary / stopping rule | [Decision 005](../decisions/005-native-waltzman-delivery.md) |
| Living-world overlay semantics | [Living-world projection](../research/living-world-projection-2026-09.md) |
| Implemented information/delivery seam | [Information and delivery v0](../contracts/information-delivery-v0.md) |
| Implemented canonical client seam | [Live projection v0](../contracts/live-projection-v0.md) |
| Integrated Waltzman evidence | [Waltzman Coordination Lab v0 audit](../audits/waltzman-coordination-lab-v0.md) |
| Selected commodity defaults | [Technology procurement](../research/technology-procurement-2026-09.md) |
| Multi-timescale time/process model | [Multi-timescale execution](../research/multi-timescale-execution-2026-09.md) |
| Competitive / adjacent systems | [Competitive landscape](../research/competitive-landscape-2026-09.md) |
| Off-the-shelf candidates to evaluate (not decisions) | [Off-the-shelf candidates 2026-09-25](../research/off-the-shelf-candidates-2026-09-25.md) |
| Implemented transition seam | [Core contract v0](../contracts/core-v0.md) |
| Live causal declaration language | [Action mechanic declaration v0](../contracts/action-mechanic-declaration-v0.md) |
| CVS analytical-model structural import | [CVS Situation IR structural import v0](../contracts/cvs-situation-import-v0.md) |
| Semantic/mechanical contract | [Semantic–mechanical binding v0](../contracts/semantic-mechanical-binding-v0.md) |
| Mechanic installation/profile | [Mechanic profile v0](../contracts/mechanic-profile-v0.md) |
| Replay/scene declaration | [Scene profile v0](../contracts/scene-profile-v0.md) · [Living Scene v1](../contracts/living-scene-v1.md) |
| Cross-repo donor roles | [Source dispositions](../source-dispositions.md) |
| Nontrivial live-authoring evidence | [Repair Bay live proof](../audits/repair-bay-live-preflight.md) |

## Concepts and terminology

- **Canonical state:** the only material world truth. Prompts, UI state, resident beliefs, and analyses do not compete with it.
- **Semantic binding:** a World Substrate profile over reviewed Linguistic Core meaning: pinned sense/role identities plus local specialization, causal classification, causal bearer, mechanic identity, and interpretation limits. Meaning does not imply effects.
- **Causal bearer:** represented actor, process, institution, disposition, or input whose presence changes possible transitions.
- **Mechanic:** installed rule/process with applicability, checks, declared reads/writes, effects, limits, and trace behavior.
- **Mechanic profile:** validated/frozen declaration set for a run. Future durable generated-law provenance should additionally fingerprint the exact executable law and compiler/interpreter version.
- **Affordance:** one currently available action instance derived from canonical state.
- **Observation:** actor-authorized projection of world state/information.
- **Authoring bundle:** represented entities/components/action signatures/presentation intent; not executable law by itself.
- **Causal model:** constrained reviewable declaration of executable action law; data, not model-written source code.
- **Declared enforcement coverage:** whether explicitly declared behavior is mapped to enforceable interfaces.
- **Bounded causal adequacy:** a scoped dependency inventory mapping consequential assumptions to represented state/enforcement surfaces plus residual risk. Current v0 is not counterfactual proof of necessity/sufficiency.
- **World interaction:** a represented occurrence such as moving, speaking, meeting, transferring, failing, or operating.
- **Information lineage:** representation + source + recipient + channel + delivery/observation/provenance.
- **Cognition context/evidence:** information an external resident runtime was allowed to see; this is not automatically hard causal parentage.
- **Mechanic-declared hard causal ancestry:** parent/dependency relations explicitly named by installed transitions and validated against retained history. Current runtime does not automatically derive them from instrumented reads.
- **Analytic interpretation:** detachable post-run/observer inference such as Waltzman or Levin findings.
- **Simulation time:** the canonical represented timeline for world actions/processes; it is distinct from browser/render time.
- **Process/institution cadence:** when a world mechanism becomes eligible to act on that timeline; different mechanisms need not share one rate.
- **Duration-bearing activity:** represented ongoing work such as travel, repair, testing, transport, or meetings when elapsed time/interruption matters; completion is another world transition opportunity.
- **Cognition cadence:** when a private resident runtime wakes to deliberate/replan; by default this should be driven by meaningful events rather than every low-level world step.
- **Projection state:** possible / enabled / active / realized relationship status derived for visualization from mechanics, current state, and retained history.
- **Core overlay:** generic read-only projection of residents, information, resources, processes, authority, or causal history.
- **Analytic overlay:** optional plugin annotation over evidence; never a hidden world variable merely because it is visually overlaid.

**Causal product contract:** when World Substrate says why an outcome happened, it means why the outcome followed **inside this represented world under its installed mechanics**. That is not, by itself, a scientific claim that the mechanics are true of the corresponding real-world system. Predictive validity and real-world causal identification require separate evidence.

The causal layers remain: substrate processes, installed institutions, resident cognition, and derived analysis. Resident memory/plans remain private unless a selected world explicitly represents them as mechanic-readable state.

Linguistic Core's fact-oriented design is converging on richer typed n-ary relation/role representation. World Substrate can consume that semantic precision when it becomes a stable interface, but it does not move persistence, quantities, effects, scheduling, write authority, or commit semantics into Linguistic Core.

## Sources and evidence

[Source dispositions](../source-dispositions.md) classifies donor roles and [references/sources.json](../../references/sources.json) pins reviewed revisions. Donor repositories are sources, not automatic runtime dependencies.

Important current evidence:

- M1–M7b substrate / semantic / mechanic-authoring / policy-consumer evidence;
- three replicated Kitchen full-service traces;
- Greenhouse zero-review replay as a post-renderer new-world proof;
- Orchard live causal generation + fresh-run acceptance;
- Repair Bay as the first nontrivial deployed authoring world;
- Warehouse Rush draft evidence showing a route→physical-dock omission and minimal `target_dock` repair;
- the Waltzman blocked baseline + exact-history recovery fork, canonical living projection, information/causal distinction, detachable analysis, and bounded dependency/adequacy report;
- the promoted generated-run stakeholder surface and retained promotion proof in `evidence/waltzman/public-promotion-2026-09-09.md`; and
- full World Builder request/response/operator/causal logs as the debugging source of truth.

The synthetic living-world UI source remains versioned at `prototypes/living-world-overlay-v0.html` as design evidence. The canonical Waltzman client at `evidence/renders/waltzman-demo-v0.html` remains a real-run reference/regression artifact; the promoted outreach endpoint is the generated-run `/waltzman/` surface.

## Accepted authorities and decisions

- [Roadmap](../../roadmap/README.md) owns current sequencing and exact next action.
- [Architecture](../architecture.md) owns durable boundaries.
- [Decision 001](../decisions/001-project-scope.md) owns canonical project scope.
- [Decision 002](../decisions/002-observability-and-replay.md) owns observability/replay doctrine.
- [Decision 003](../decisions/003-semantic-mechanical-boundary.md) owns the semantic/effect boundary.
- [Decision 004](../decisions/004-product-and-adoption-strategy.md) owns product direction and commodity-selection doctrine.
- [Decision 005](../decisions/005-native-waltzman-delivery.md) owns the native Waltzman delivery target, Cybernetic donor boundary, first-release stopping rule, and explicit uncertainties/failure responses.
- Implemented contracts own only their declared seam.
- Code/tests own runtime behavior.
- Revision/run-bound evidence owns observed outcome claims.
- Human product decision, 2026-09-09: the static canonical Waltzman client is retained reference/presentation evidence, not the finished outreach demo; the sendable demo requires natural-language generation + fresh execution + living inspection, and the Cybernetic donor path was authorized as the fastest promotion route.
- Human product decision, 2026-09-18: the next Waltzman release should converge that experience onto native World Substrate authoring/execution/automatic UI; Cybernetic remains donor/analysis lineage and the existing donor-backed surface remains regression/fallback during convergence.
- Human semantic review, 2026-09-12: richer Linguistic Core n-ary/role representation may refine semantic bindings, but the semantic/mechanical boundary remains unchanged; effects and consequence authority stay in World Substrate.

Decision 004 classifies uncertainty as:

- **novel** → experiment;
- **commodity** → research → reason → select; and
- **integration** → bounded conformance test.

Selected defaults are deck.gl 9.4.x, Pydantic AI 2.41.x behind `CognitionAdapter`, SimPy 4.1.2 for scheduling only, and Cytoscape.js 3.34.x for expanded graph inspection.

## Working context

| Area | Current state |
| --- | --- |
| Core transition engine | implemented; write scopes enforced; rule views detached |
| Semantic grounding | six of seven M1 kinds bound; generic live actions not yet semantically closed; `unheat` intentionally remains unbound rather than inventing an LC sense |
| Causal generation | constrained JSON proposal + local compiler + explicit approval + frozen declaration profile |
| Live policies | scripted/LLM; LLM selects only Engine-minted action IDs |
| Replay | portable read-only scene-profile renderer across multiple worlds |
| World Builder | deployed authoring + mechanics review/approval + fresh scripted/LLM runs |
| Full logs | deployed; complete request/response/compiler/operator/causal traces available |
| Living-world UI | generated-run living replay stakeholder-promoted on `65eb465a`; temporary Mac origin remains until migration to the approved shared Netcup VPS; canonical Waltzman reference client remains retained evidence |
| Live projection | implemented local first gate: exact initial-snapshot + retained-event/delta reconstruction, self-contained HTML, JSON, and one-way SSE |
| Information/conversation | implemented bounded v0: source/recipient/channel/visibility/delivery/provenance + asymmetric actor observation; not a belief model |
| Processes/institutions | Waltzman first gate has tick-specific processes, explicit commitments, a duration-bearing meeting, and an installed coalition gate; generic authoring remains narrow |
| Resident cognition | Pydantic AI selected but not integrated; current bounded policy seam remains sufficient for existing fixtures |
| Scheduling | core remains integer-tick + per-step `due()` checks; Waltzman proves scenario-specific independent trigger ticks + duration activity; SimPy future-event queue still unintegrated |
| Multi-timescale execution | first scenario gate implemented on canonical ticks with independently due processes + represented meeting duration; generic scheduler contract remains later |
| Graph inspector | Cytoscape selected; not needed for the promoted stakeholder demo |
| Persistence/auth | no saved user worlds/runs or identity-backed approvals yet |

Open work at the handoff point:

- **PR #37** — Warehouse Rush draft experiment. Useful retained evidence; provider retry remains pending and is not active roadmap priority.
- **PR #43** — CVS sustainment seam from a separate integration track. It does not set roadmap priority and should be rebased/reviewed against current main before a merge decision.

## Needs resolution

The roadmap owns ordering. Current unresolved work is split into **active hosting**, **post-demo hardening**, and **later capabilities**.

1. **Hosting migration — active:** keep the Mac as temporary/rollback origin while moving the promoted donor backend to the approved shared Netcup VPS; require health, route certification, retained-run access, browser checks, and rollback verification before cutover.
2. **First-two-minute UX — promoted regression target:** preserve the configure-first local-information-to-collective-action experience; do not reopen it as unfinished acquisition work unless evidence regresses.
3. **Executable-law provenance — post-demo hardening:** bind future approval/run identity to a fingerprint of the exact executable law plus compiler/interpreter version.
4. **Local-authority correctness — post-demo hardening:** bind write-scope placeholders to exact action roles and make authored affordance-cap overflow explicit rather than silently truncating valid actions.
5. **Repository reproducibility — post-demo hardening:** add appropriate CI/project gates and exact dependency locking when selected external dependencies enter reproducible production paths.
6. **Semantic closure — later / when blocking:** continue to cite reviewed LC senses/roles, keep unsupported bindings visible, and consume a richer LC role/relation contract only when it materially improves a real binding or authoring/review path.
7. **Generative causal closure — later research:** continue dependency inventories, gap finding, residual risk, and smallest-repair work. Automatic counterfactual/mutation verification is a deferred option, not a current requirement.
8. **Generative richer-world authoring — later:** the current Builder does not yet conversationally author Waltzman's information/activity/institution mechanics. Extend the declaration language only from another concrete world/product need.
9. **Resident cognition / generic scheduling / persistence — later:** integrate Pydantic AI, SimPy future-event scheduling, and saved user worlds only when a real scenario earns them.
10. **Mechanic failure events / read verification / scale — later:** retain as explicit boundaries and promote them only when they block a real product or evidence need.

## Architecture and workflow

```text
conversational authoring
      |
      v
represented world + dependency intent
      |
      v
semantic/action structure + generated causal declarations
      |
      v
local compiler derives authority -> human approval -> frozen declaration profile
      |
      v
resident action OR process trigger
      |
      v
Engine.submit()/process coordinator -> checks -> commit/refusal
      |
      +--> canonical state + causal/evidence history
      |
      +--> read-only live projection -> deck.gl living world
      |                             -> optional Cytoscape inspector
      |
      +--> detachable analyses -> Waltzman / Levin / future plugins
```

Pydantic AI, SimPy, deck.gl, Cytoscape, persistence, and auth are replaceable external machinery around the owned causal seam. SimPy schedules opportunities only; Pydantic AI selects attempts/utterances only; renderers and analyses are read-only. The target time model uses one canonical simulated timeline with independent process/institution/activity cadences; browser frame rate, playback speed, cognition wake cadence, and analysis sampling are not alternate world clocks.

A conversation is visible world activity even with overlays off. The information overlay adds delivery/provenance semantics. A causal overlay includes that conversation only where an installed mechanic explicitly declares the stronger parent relation. Prompt/context inclusion alone is not proof that the information caused a later decision.

## Human-reviewable artifacts

Use these first:

- `https://brianmills.dev/world-builder/` — deployed Build/Play alpha.
- `https://brianmills.dev/waltzman/` — promoted stakeholder demo: natural-language authoring, fresh retained run, and living inspection through the bounded donor path.
- `https://brianmills.dev/world-substrate-visualization/` — legacy synthetic public surface retained as design evidence.
- `evidence/renders/waltzman-demo-v0.html` — implemented self-contained canonical Waltzman reference/regression client.
- `prototypes/living-world-overlay-v0.html` — retained synthetic design prototype.
- [Waltzman Coordination Lab v0 audit](../audits/waltzman-coordination-lab-v0.md) — integrated reference-world evidence and claim boundaries.
- [Living-world projection](../research/living-world-projection-2026-09.md) — overlay semantics and accepted integration path.
- [Technology procurement](../research/technology-procurement-2026-09.md) — selected external stack and boundaries.
- [Multi-timescale execution](../research/multi-timescale-execution-2026-09.md) — canonical simulation-time / independent-cadence target and current integer-tick limitation.
- [Off-the-shelf candidates](../research/off-the-shelf-candidates-2026-09-25.md) — unevaluated standards/theory/implementation candidates from a cross-repo review.
- `evidence/renders/kitchen-spatial-replay-v1.html` — polished flagship replay.
- `evidence/renders/greenhouse-zero-review-v0.html` — new-world Automatic presentation proof.
- [Repair Bay live proof](../audits/repair-bay-live-preflight.md) — nontrivial authoring/run evidence.
- [Action mechanic declaration v0](../contracts/action-mechanic-declaration-v0.md) — current generated-law language.
- [Semantic–mechanical binding v0](../contracts/semantic-mechanical-binding-v0.md) — current downstream LC-to-mechanic profile contract.
- [Scene profile v0](../contracts/scene-profile-v0.md) — retained contested-run replay presentation contract.
- [Living Scene v1](../contracts/living-scene-v1.md) — deterministic read-only logical frames over canonical live projections.

## Roadmap

Use [the canonical roadmap](../../roadmap/README.md) for current priorities, risks, refresh triggers, and the exact next action. The wiki is navigation and current-state orientation; it must not become a second roadmap.