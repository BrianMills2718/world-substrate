---
role: research
status: active
reviewed_through: 2026-09-08
---

# Technology procurement — living worlds, cognition, scheduling, and graph inspection

## Decision frame

World Substrate should not spend experiments on technology-selection questions that mature external evidence already answers well enough. The local research program is generative causal authoring and bounded causal closure; renderer, cognition harness, scheduler, graph library, persistence, and auth are replaceable commodity layers.

Use this classification:

- **Novel uncertainty:** experiment when the answer is not mature externally and can change World Substrate architecture.
- **Commodity uncertainty:** research current benchmarks/docs/production evidence, reason from project constraints, and select.
- **Integration uncertainty:** test only that the selected dependency conforms to the World Substrate boundary.

## Selection snapshot — 2026-09-08

| Capability | Selected default | Why it fits | Boundary |
| --- | --- | --- | --- |
| Living spatial/semantic projection | deck.gl 9.4.x | GPU layer composition, picking, dynamic data updates, non-geographic `OrthographicView`, optional MapLibre integration | presentation only; no world authority |
| Resident cognition | Pydantic AI 2.41.x | typed Python agent harness, current OpenRouter support, memory/planning/tool orchestration, production-oriented v2 line | authorized observation in; selected action/utterance out; private state stays private |
| Simulated time/event queue | SimPy 4.1.2 | mature discrete-event clock, events, timeouts, process wakeups, step/run control | schedules opportunities only; World Substrate mechanics commit/refuse consequences |
| Expanded causal/institutional graph | Cytoscape.js 3.34.x | compound nodes, selectors, interaction events, mature graph layouts | read-only inspector over projection/evidence data |
| Large-graph rendering | Sigma.js, deferred | excellent WebGL large-graph path, but first need is semantic/compound inspection rather than maximum node count | revisit only if scale pressure appears |

Exact implementation versions should be pinned. The families above record the procurement evidence available on the review date and may be upgraded deliberately.

## Rendering

The default living-world UI is not a second simulation. World Substrate emits canonical identities, state deltas, world events, scene semantics, and projection metadata. deck.gl renders them as composable layers. Schematic worlds use Cartesian `OrthographicView`; real geographic worlds may add MapLibre without changing the projection contract.

The expected layer model is additive: base world, residents, information structure/activity/history, resources, processes, authority, causal focus/history, selection, and analysis-plugin annotations. Possible/enabled/active/realized are projection states derived from canonical state, installed mechanics, and retained history rather than alternate world truth.

## Resident cognition

`CognitionAdapter` is the owned seam. Pydantic AI is the default harness behind it. World Substrate supplies actor-authorized observation, engine-minted offered actions/effect semantics, budgets, and relevant private resident context; the harness returns a selected action id, optional utterance, and private-state update. Resident deliberation should usually be event-driven rather than tied to every low-level simulation step: task completion/failure, important delivered information, interaction requests, scheduled reflection, or other bounded wake conditions are the target.

Conformance tests must prove that the harness cannot mutate canonical state, cannot see observer-only evidence, cannot select actions the Engine did not offer, keeps private memory actor-private, and fails without corrupting the World. Do not run model/harness architecture tournaments unless a future question is genuinely novel and material.

## Scheduling

SimPy may own simulated clock advancement, event ordering, timeouts, and waking process coroutines. It must not become a parallel source of resource truth or consequence authority. A SimPy wakeup produces a World Substrate process attempt; the installed process mechanic still checks canonical state and the Engine still commits or refuses the transition. The target is one canonical simulation timeline supporting independently timed processes and duration-bearing activities; render time, cognition cadence, and analysis cadence remain separate. See [multi-timescale execution](multi-timescale-execution-2026-09.md).

## Graph inspection

The primary experience remains the living spatial world. Cytoscape.js is selected for an expanded non-spatial inspector when a user asks to see a complete causal, information, or institutional graph. Cross-selection should preserve canonical entity/event ids between deck.gl and Cytoscape views.

## Sources reviewed

- deck.gl 9.4.0 / `@deck.gl/core` and layer packages: <https://www.npmjs.com/package/@deck.gl/core> and <https://www.npmjs.com/package/@deck.gl/layers>
- deck.gl `OrthographicView`: <https://deck.gl/docs/api-reference/core/orthographic-view>
- Pydantic AI 2.41.0: <https://pypi.org/project/pydantic-ai/2.41.0/>
- Pydantic AI project/version policy: <https://github.com/pydantic/pydantic-ai>
- SimPy 4.1.2: <https://pypi.org/project/simpy/4.1.2/>
- Cytoscape.js releases: <https://github.com/cytoscape/cytoscape.js/releases>
- Cytoscape.js documentation: <https://js.cytoscape.org/>

## Consequence

Technology procurement is no longer a roadmap experiment. Integration work should begin only when a concrete product slice needs the selected capability, and the local proof should test the seam rather than re-answer the ecosystem-selection question.
