---
schema_version: project-wiki/v1
type: ProjectWiki
role: derived-navigation
status: active
reviewed_through: 2026-09-08
authority_refs:
  - ../../README.md
  - ../../roadmap/README.md
  - ../architecture.md
  - ../decisions/001-project-scope.md
  - ../decisions/002-observability-and-replay.md
  - ../decisions/003-semantic-mechanical-boundary.md
  - ../decisions/004-product-and-adoption-strategy.md
---

# World Substrate project wiki

This is the single compact orientation surface for the repository. It summarizes current truth and routes readers to native authorities; it does not replace architecture, contracts, decisions, code, evidence, or the roadmap.

## What this project is

World Substrate is a persistent, observable simulation engine and generative authoring system. Human or model policies express intents; installed mechanics with explicit local authority determine canonical consequences.

The product direction is now a **generative living-world builder over a rigorous causal engine**. The user should be able to describe a world conversationally, review represented structure and executable law, run residents/processes through it, watch it evolve spatially, and inspect why outcomes occurred without allowing presentation, cognition, or analysis to become alternate truth.

The first serious application vertical is a **Coordination Environment Lab** inspired by Cybernetic Influence v3 and Waltzman's *From Minds to Coordination*. Waltzman-specific trust structure, perceived risk, coordination readiness, detection/diagnosis/stabilization, and evasion analysis remain detachable plugins over evidence rather than universal world variables.

Public surfaces:

- World Builder: `https://brianmills.dev/world-builder/`
- Living-world visualization prototype: `https://brianmills.dev/world-substrate-visualization/`

The living-world prototype is currently a UI prototype with synthetic timeline data. The active implementation goal is to feed it a real World Substrate run.

## Start here

| Need | Read next |
| --- | --- |
| Current direction / exact next action | [Roadmap](../../roadmap/README.md) |
| Durable system boundaries | [Architecture](../architecture.md) |
| Product + procurement doctrine | [Decision 004](../decisions/004-product-and-adoption-strategy.md) |
| Living-world overlay semantics | [Living-world projection](../research/living-world-projection-2026-09.md) |
| Selected commodity defaults | [Technology procurement](../research/technology-procurement-2026-09.md) |
| Competitive / adjacent systems | [Competitive landscape](../research/competitive-landscape-2026-09.md) |
| Implemented transition seam | [Core contract v0](../contracts/core-v0.md) |
| Live causal declaration language | [Action mechanic declaration v0](../contracts/action-mechanic-declaration-v0.md) |
| Semantic/mechanical contract | [Semantic–mechanical binding v0](../contracts/semantic-mechanical-binding-v0.md) |
| Mechanic installation/profile | [Mechanic profile v0](../contracts/mechanic-profile-v0.md) |
| Replay/scene declaration | [Scene profile v0](../contracts/scene-profile-v0.md) |
| Cross-repo donor roles | [Source dispositions](../source-dispositions.md) |
| Nontrivial live-authoring evidence | [Repair Bay live proof](../audits/repair-bay-live-preflight.md) |

## Concepts and terminology

- **Canonical state:** the only material world truth. Prompts, UI state, resident beliefs, and analyses do not compete with it.
- **Semantic binding:** reviewed Linguistic Core sense/roles plus causal classification; meaning does not imply effects.
- **Causal bearer:** represented actor, process, institution, disposition, or input whose presence changes possible transitions.
- **Mechanic:** installed rule/process with applicability, checks, declared reads/writes, effects, limits, and trace behavior.
- **Mechanic profile:** validated/frozen mechanic set for a run.
- **Affordance:** one currently available action instance derived from canonical state.
- **Observation:** actor-authorized projection of world state/information.
- **Authoring bundle:** represented entities/components/action signatures/presentation intent; not executable law by itself.
- **Causal model:** constrained reviewable declaration of executable action law; data, not model-written source code.
- **Declared enforcement coverage:** whether explicitly declared behavior is bound to enforceable interfaces.
- **Bounded causal closure:** evidence that material dependencies are represented/enforced/coarse/external/unsupported/unknown, with residual risk rather than a universal completeness proof.
- **World interaction:** a represented occurrence such as moving, speaking, meeting, transferring, failing, or operating.
- **Information lineage:** representation + source + recipient + channel + delivery/observation/provenance.
- **Cognition context/evidence:** information an external resident runtime was allowed to see; this is not automatically hard causal parentage.
- **Hard causal ancestry:** mechanically supported parent/dependency relations for committed transitions.
- **Analytic interpretation:** detachable post-run/observer inference such as Waltzman or Levin findings.
- **Projection state:** possible / enabled / active / realized relationship status derived for visualization from mechanics, current state, and retained history.
- **Core overlay:** generic read-only projection of residents, information, resources, processes, authority, or causal history.
- **Analytic overlay:** optional plugin annotation over evidence; never a hidden world variable merely because it is visually overlaid.

The causal layers remain: substrate processes, installed institutions, resident cognition, and derived analysis. Resident memory/plans remain private unless a selected world explicitly represents them as mechanic-readable state.

## Sources and evidence

[Source dispositions](../source-dispositions.md) classifies donor roles and [references/sources.json](../../references/sources.json) pins reviewed revisions. Donor repositories are sources, not automatic runtime dependencies.

Important current evidence:

- M1–M7b substrate / semantic / mechanic-authoring / policy-consumer evidence;
- three replicated Kitchen full-service traces;
- Greenhouse zero-review replay as a post-renderer new-world proof;
- Orchard live causal generation + fresh-run acceptance;
- Repair Bay as the first nontrivial deployed authoring world;
- Warehouse Rush draft evidence showing a route→physical-dock omission and minimal `target_dock` repair; and
- full World Builder request/response/operator/causal logs as the debugging source of truth.

The living-world UI source is versioned at `prototypes/living-world-overlay-v0.html`; it is design evidence, not evidence of a real simulation run until the live projection slice replaces its synthetic data.

## Accepted authorities and decisions

- [Roadmap](../../roadmap/README.md) owns current sequencing and exact next action.
- [Architecture](../architecture.md) owns durable boundaries.
- [Decision 001](../decisions/001-project-scope.md) owns canonical project scope.
- [Decision 002](../decisions/002-observability-and-replay.md) owns observability/replay doctrine.
- [Decision 003](../decisions/003-semantic-mechanical-boundary.md) owns the semantic/effect boundary.
- [Decision 004](../decisions/004-product-and-adoption-strategy.md) owns product direction and commodity-selection doctrine.
- Implemented contracts own only their declared seam.
- Code/tests own runtime behavior.
- Revision/run-bound evidence owns observed outcome claims.

Decision 004 now classifies uncertainty as:

- **novel** → experiment;
- **commodity** → research → reason → select; and
- **integration** → bounded conformance test.

Selected defaults are deck.gl 9.4.x, Pydantic AI 2.41.x behind `CognitionAdapter`, SimPy 4.1.2 for scheduling only, and Cytoscape.js 3.34.x for expanded graph inspection.

## Working context

| Area | Current state |
| --- | --- |
| Core transition engine | implemented; write scopes enforced; rule views detached |
| Semantic grounding | six of seven M1 kinds bound; generic live actions not yet semantically closed |
| Causal generation | constrained JSON proposal + local compiler + explicit approval + frozen profile |
| Live policies | scripted/LLM; LLM selects only Engine-minted action IDs |
| Replay | portable read-only scene-profile renderer across multiple worlds |
| World Builder | deployed authoring + mechanics review/approval + fresh scripted/LLM runs |
| Full logs | deployed; complete request/response/compiler/operator/causal traces available |
| Living-world UI | deployed standalone prototype; synthetic data; source now versioned |
| Live projection | **active next slice**; no canonical feed yet |
| Information/conversation | no first-class generic representation/delivery contract yet |
| Processes/institutions | core engine concept exists; generic authoring surface is not rich enough for Coordination Lab yet |
| Resident cognition | Pydantic AI selected but not integrated; current bounded LLM seam remains sufficient for existing fixtures |
| Scheduling | SimPy selected for future timing/event queue only; not yet integrated |
| Graph inspector | Cytoscape selected; not yet needed in active slice |
| Persistence/auth | no saved user worlds/runs or identity-backed approvals yet |

Open work at the handoff point:

- **PR #37** — Warehouse Rush draft experiment. Useful retained evidence; v1 provider retry remains pending but is deliberately deferred behind live projection.
- **PR #43** — CVS sustainment seam from a separate integration track. It does not set roadmap priority and should be rebased/reviewed against current main before a merge decision.

## Needs resolution

The roadmap owns ordering; the important unresolved capabilities are:

1. **Live projection seam:** real canonical snapshot/events must drive the living client without renderer-owned truth.
2. **Information/conversation semantics:** represent utterances/messages, source/recipient/channel/provenance/visibility, and delivery distinctly from private cognition.
3. **Causal/evidence lineage:** distinguish hard mechanical ancestry from observation/context and analytic inference.
4. **Generative causal closure:** dependency inventory → enforcement mapping → counterexamples/probes → residual-risk report → smallest repair.
5. **Processes/institutions:** generic authoring for meetings, schedules, external events, permissions, commitments, and decision procedures when the Coordination Lab demands them.
6. **Resident cognition:** integrate Pydantic AI behind a narrow adapter only when richer worlds need persistent memory/planning/social behavior.
7. **Semantic closure/review:** generic new action kinds should eventually bind reviewed Linguistic Core senses/roles; improve review representation when real users cannot distinguish material law differences.
8. **Persistence/auth:** saved worlds/runs and identity-backed approvals after the authoring/run workflow earns durable state.
9. **Mechanic/process error events:** promote implementation failures into explicit causal failure evidence when needed for trust/debugging.
10. **Scale/read enforcement:** defer until measured pressure appears.

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
local compiler derives authority -> human approval -> frozen profile
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

Pydantic AI, SimPy, deck.gl, Cytoscape, persistence, and auth are replaceable external machinery around the owned causal seam. SimPy schedules opportunities only; Pydantic AI selects attempts/utterances only; renderers and analyses are read-only.

A conversation is visible world activity even with overlays off. The information overlay adds delivery/provenance semantics. A causal overlay includes that conversation only where the retained causal/evidence model supports the stronger relation. Prompt/context inclusion alone is not proof that the information caused a later decision.

## Human-reviewable artifacts

Use these first:

- `https://brianmills.dev/world-builder/` — deployed Build/Play alpha.
- `https://brianmills.dev/world-substrate-visualization/` — living-world visual interaction prototype.
- `prototypes/living-world-overlay-v0.html` — versioned prototype source.
- [Living-world projection](../research/living-world-projection-2026-09.md) — overlay semantics and first integration acceptance.
- [Technology procurement](../research/technology-procurement-2026-09.md) — selected external stack and boundaries.
- `evidence/renders/kitchen-spatial-replay-v1.html` — polished flagship replay.
- `evidence/renders/greenhouse-zero-review-v0.html` — new-world Automatic presentation proof.
- [Repair Bay live proof](../audits/repair-bay-live-preflight.md) — nontrivial authoring/run evidence.
- [Action mechanic declaration v0](../contracts/action-mechanic-declaration-v0.md) — current generated-law language.
- [Scene profile v0](../contracts/scene-profile-v0.md) — current read-only presentation contract.

## Roadmap

Use [the canonical roadmap](../../roadmap/README.md) for current priorities, risks, refresh triggers, and the exact next action. The wiki is navigation and current-state orientation; it must not become a second roadmap.
