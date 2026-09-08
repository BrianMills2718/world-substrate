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

This is the single orientation surface for the project. It summarizes current truth and routes readers to native authorities; it does not replace architecture, contracts, decisions, code, or evidence.

## What this project is

World Substrate is a persistent, observable simulation engine and authoring system. LLM or human policies express intents. Linguistic Core supplies semantic senses and participant roles. Installed mechanics with explicit local authority determine canonical consequences.

The product direction is a **Generative-World Builder on top of a rigorous causal world engine**. The distinctive claim is not that an LLM can narrate a plausible world; it is that the world has represented state, installed law, and inspectable evidence for what actually happened.

The deployed product is available at `https://brianmills.dev/world-builder/`.

## Start here

| Need | Read next |
| --- | --- |
| Current direction / exact next action | [Roadmap](../../roadmap/README.md) |
| Durable system boundaries | [Architecture](../architecture.md) |
| Product + off-the-shelf strategy | [Decision 004](../decisions/004-product-and-adoption-strategy.md) |
| Competitive / adjacent-system research | [Competitive landscape](../research/competitive-landscape-2026-09.md) |
| Implemented transition seam | [Core contract v0](../contracts/core-v0.md) |
| Live causal declaration language | [Action mechanic declaration v0](../contracts/action-mechanic-declaration-v0.md) |
| CVS analytical-model structural import | [CVS Situation IR structural import v0](../contracts/cvs-situation-import-v0.md) |
| Semantic/mechanical contract | [Semantic–mechanical binding v0](../contracts/semantic-mechanical-binding-v0.md) |
| Mechanic installation/profile | [Mechanic profile v0](../contracts/mechanic-profile-v0.md) |
| Commit boundary | [Transition envelope v0](../contracts/transition-envelope-v0.md) |
| Optional read-scope verification | [Read-scope enforcement v0](../contracts/read-scope-enforcement-v0.md) |
| Replay/scene declaration | [Scene profile v0](../contracts/scene-profile-v0.md) |
| Why neighboring repos are not authority | [Source dispositions](../source-dispositions.md) |
| Reference worlds | [Reference-world guide](../../reference_worlds/README.md) |
| Live authoring evidence | [Live authoring audit](../audits/live-world-authoring.md) |
| Flagship behavior | [Kitchen audit](../audits/kitchen-contested-world.md) |

## Concepts and terminology

- **Canonical state:** the only material world truth. Prompts, UI, model beliefs, and analysis are not competing authorities.
- **Semantic binding:** a Linguistic Core sense plus participant-role mapping and causal classification.
- **Causal bearer:** the represented actor, process, institution, disposition, or input whose presence changes possible transitions.
- **Mechanic:** an installed rule/process with applicability, declared state authority, checks, effects, limits, and trace behavior.
- **Mechanic profile:** the validated/frozen set of mechanics used for one run.
- **Affordance:** one currently available action instance derived from canonical state.
- **Observation:** an actor-authorized projection of canonical state.
- **Composite event:** a description of committed lower-level events that does not apply their effects again.
- **Declared enforcement coverage:** whether everything the author explicitly declared is bound to an enforceable interface.
- **Causal-closure assay:** fallible review/testing that searches for consequential dependencies the author did not declare.
- **Authoring bundle:** non-causal represented structure, action signatures, and presentation declarations.
- **Causal model:** constrained, reviewable law for action signatures; it is data, not model-written executable source.
- **Terminal condition:** a state-derived predicate saying represented work is complete.
- **Automatic replay:** graphical presentation generated from world/trace/shared presentation semantics without world-specific renderer code.
- **Polished replay:** optional art-direction overlay on top of the same world truth.

The four causal layers remain: substrate processes, installed institutions, resident-agent cognition, and derived analytic interpretation. Agent memory/plans remain private cognition unless a selected world explicitly represents them as mechanic-readable state.

## Sources and evidence

[Source dispositions](../source-dispositions.md) classifies donor roles and [references/sources.json](../../references/sources.json) pins reviewed revisions. Donor repositories may contribute ideas, evidence, or adopted code only through an explicit consumer path.

Retained evidence is revision/run scoped. Important current evidence includes:

- M1 freshwater traces and fresh-process replay for the implemented substrate baseline;
- M3/M4 mechanic-authoring and causal-coherence assays;
- M5 LLM policy use through the ordinary affordance seam;
- M6 Workshop cross-domain reuse;
- M7/M7b model-authored mechanic experiments;
- three replicated Kitchen full-service traces;
- Greenhouse zero-review replay as the post-renderer new-world proof; and
- Orchard live causal-generation + fresh-run acceptance evidence.

Historical evidence is not rewritten to resemble current behavior. For example, the old Kitchen full-service trace keeps its trailing turns because those turns motivated the terminal-state fix.

## Accepted authorities and decisions

- [Roadmap](../../roadmap/README.md) owns current planning and prioritization.
- [Architecture](../architecture.md) owns durable system boundaries.
- [Decision 001](../decisions/001-project-scope.md) owns canonical project scope.
- [Decision 002](../decisions/002-observability-and-replay.md) owns observability/replay doctrine.
- [Decision 003](../decisions/003-semantic-mechanical-boundary.md) owns the semantic/effect boundary.
- [Decision 004](../decisions/004-product-and-adoption-strategy.md) owns the Generative-World Builder and off-the-shelf adoption posture.
- Implemented contracts own only their declared seam; proposed/partial contracts must say so.
- Code/tests own current runtime behavior.
- Revision-bound evidence owns observed outcome claims.

## Working context

The substrate phase is complete. Current product/engineering truth:

| Area | Current state |
| --- | --- |
| Core transition engine | implemented; write scopes enforced; rule views detached |
| Semantic grounding | six of seven M1 kinds bound; generic live actions not yet semantically closed |
| Kitchen flagship | 3/3 replicated handoff/completion; polished and Automatic replay |
| Replay system | one generic renderer + scene semantics + auto-layout across real worlds |
| Builder | deployed; structural authoring + causal proposal/review/approval + fresh runs |
| Causal generation | Luna proposes constrained JSON; local compiler is authority; one repair attempt allowed |
| Live policies | scripted or LLM; LLM selects only engine-minted action IDs |
| Deployment | public static Builder/Play shell + loopback API behind Cloudflare |
| Spend control | per-call caps + rate limits + persistent $0.50/day reservation ledger |
| Resident cognition | intentionally separate; durable memory/reflection/planning not yet implemented |
| User persistence | no saved-user-world/run product yet |

Reference-world roles:

- **Castaway:** M1 implementation/evidence donor.
- **Workshop:** materially different reuse proof.
- **Kitchen:** flagship watched world.
- **Greenhouse:** new-world/Automatic-replay portability proof.
- **Orchard:** live-authoring acceptance fixture.

The approved implementation strategy is to keep the causal kernel custom and evaluate mature systems around it. Phaser is the leading browser-rendering candidate; Concordia/LangGraph are cognition candidates; PettingZoo is an interoperability candidate; persistence/auth should use standard infrastructure; SimPy is conditional on demonstrated scheduling pressure. None is adopted as causal authority merely by being named. The [competitive landscape](../research/competitive-landscape-2026-09.md) explains why the project should own causal-world authoring/authority while borrowing cognition, scale, evaluation, and commodity infrastructure from adjacent systems.

## Needs resolution

These are the important open boundaries now:

1. **Semantic closure for live authoring:** generated action mechanics can currently compile while `semantic_bindings` is empty; new authored action kinds should eventually bind a reviewed Linguistic Core sense/role mapping.
2. **Less-trivial authoring proof:** Orchard is intentionally tiny. The next real product test must exercise multiple actors/resources/actions and reveal the first genuine causal-language/review failure.
3. **Mechanic failure evidence:** implementation exceptions are safely isolated/rolled back but should become explicit `mechanic_error` / `process_error` causal events.
4. **Approval/auth semantics:** public same-origin/rate-limit controls bound abuse economically, but identity and durable server-issued approval receipts remain product/security decisions.
5. **Resident cognition:** memory, reflection, planning, schedules, and social models should be added behind the policy seam, preferably via a bounded off-the-shelf comparison rather than a framework rewrite.
6. **Saved worlds/runs:** the live Builder currently creates ephemeral fresh runs; durable user-owned worlds/run history are not yet a product surface.
7. **Read-scope verification:** declared reads remain recorded but not enforced; activate only if measured value justifies overhead.
8. **Upstream semantic gap:** `unheat` still lacks an appropriate pinned Linguistic Core sense.
9. **Deployment reproducibility/CI:** source is pinned, but the live Python dependency environment is not fully hermetic and permanent required CI is still desirable.

## Architecture and workflow

```text
represented structure
      |
      v
semantic intent / action signature
      |
      v
reviewed semantic binding (partial for generic live authoring today)
      |
      v
constrained causal-mechanic declaration
      |
      v
local compiler derives authority + validates paths/types
      |
      v
explicit approval -> frozen mechanic profile
      |
      v
scripted / human / LLM policy selects offered action_id
      |
      v
Engine.submit() -> checks -> one commit or refusal
      |
      +--> canonical persistent state + causal event
      |
      +--> retained trace -> scene semantics -> graphical replay
```

Off-the-shelf cognition, renderer, interoperability, persistence, and auth may surround this path. They must not replace the Engine as consequence authority.

## Human-reviewable artifacts

Use these instead of reading every milestone audit:

- `https://brianmills.dev/world-builder/` — deployed Build/Play product surface.
- `evidence/renders/kitchen-spatial-replay-v1.html` — polished graphical flagship.
- `evidence/renders/kitchen-zero-review-v0.html` — Automatic Kitchen breadth proof.
- `evidence/renders/greenhouse-zero-review-v0.html` — new-world Automatic proof.
- `evidence/renders/world-replay-studio-v0.html` — retained-world Studio.
- [Live authoring audit](../audits/live-world-authoring.md) — real mechanics-generation/policy calls and service guards.
- [Action mechanic declaration contract](../contracts/action-mechanic-declaration-v0.md) — live causal language/authority boundary.
- [Scene profile contract](../contracts/scene-profile-v0.md) — trace/world/presentation-to-replay boundary.
- [Greenhouse proof](../audits/greenhouse-authoring-proof.md) — end-to-end fourth-world portability evidence.
- [Kitchen audit](../audits/kitchen-contested-world.md) — replicated flagship behavior.
- [Decision 004](../decisions/004-product-and-adoption-strategy.md) — current product/adoption strategy.

## Roadmap

Use [the canonical roadmap](../../roadmap/README.md) for current priorities, risks, refresh triggers, and the exact next action. The wiki is navigation; it must not become a second roadmap.
