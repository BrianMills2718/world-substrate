---
schema_version: project-wiki/v1
type: ProjectWiki
role: derived-navigation
status: active
reviewed_through: 2026-11-09
authority_refs:
  - ../../README.md
  - ../../roadmap/README.md
  - ../architecture/arc42.md
  - ../../openspec/specs/
  - ../decisions/001-project-scope.md
  - ../decisions/002-observability-and-replay.md
  - ../decisions/003-semantic-mechanical-boundary.md
  - ../decisions/004-product-and-adoption-strategy.md
  - ../decisions/005-native-waltzman-delivery.md
  - ../decisions/006-governed-rules-layer-scope.md
  - ../decisions/007-any-scenario-path.md
  - ../decisions/008-build-worlds-in-an-agent-harness.md
  - ../decisions/009-same-moment-knock-on-effects.md
---

# World Substrate project wiki

One page of current state. It summarizes and routes; it does not replace the
[architecture](../architecture/arc42.md), the [capability specs](../index.md#2-what-the-code-must-do-openspec-capability-specs),
the decisions, the code, the evidence or the [roadmap](../../roadmap/README.md). Every document is
listed in the [documentation index](../index.md). Checked against `main` at `0e66a98` on 2026-11-09.

## What this project is

World Substrate is a persistent, observable world engine with a generative builder on top. A person
describes a world in plain words; a model proposes its structure and rules as data; a local compiler
derives what each rule may read and write; and once the rules are approved, residents (scripted, human
or AI) say what they try while installed rules alone decide what changes. Every change or refusal is
recorded with its cause.

Brian's reason for keeping consequences in rules rather than an AI judge is scale (2026-11-09, quoted in
full in [arc42 section 1](../architecture/arc42.md#architectural-thesis)): facts must carry their
implications and blockers down long causal chains automatically.

The public surface is the **World Builder** at <https://brianmills.dev/world-builder/>: one box and one
Create simulation button. Pressing it is the approval (Brian, 2026-10-15). The builder makes the world,
its declared laws and its rules, has another model review the rules, runs a free scripted test, then
plays the world live one round at a time with Concordia residents. **Waltzman Coordination Lab**
(Rand Waltzman's bio-surveillance coordination scenario) is the showcase world; the older donor-backed
demo at <https://brianmills.dev/waltzman/> is kept as a fallback. Both answered HTTP 200 on 2026-11-09.

Scope is set by [Decision 006](../decisions/006-governed-rules-layer-scope.md): World Substrate is the
governed-rules layer (rules as data, compiler-derived authority, approval, atomic commit or refusal with a
recorded cause). Resident loops, scheduling and planning come from Concordia, Mesa or a PDDL export when a
world needs them.

## Start here

| Need | Read |
| --- | --- |
| Every document, in reading order | [Documentation index](../index.md) |
| Architecture: goal, requirements, building blocks, deployment, risks | [arc42](../architecture/arc42.md) |
| What the code must do | [OpenSpec capability specs](../index.md#2-what-the-code-must-do-openspec-capability-specs) |
| Stage, active slice and exact next action | [Roadmap](../../roadmap/README.md) |
| What would have made earlier work faster (read before planning) | [Lessons](lessons.md) |
| The system as a checked model | [ODD](../model/ODD.md), [trace.yaml](../model/trace.yaml), [view coverage](../model/VIEW_COVERAGE.md) |
| What a world is made of, built versus theory | [Domain model](../model/DOMAIN.md), [metamodel](../model/METAMODEL.md) |
| What the project does not yet know | [Open questions](../planning/open-questions.json), [planning package](../planning/planning-package.json) |
| Open attempts, knock-on effects, skill rolls | [Open-attempt plan](../plans/open_attempt.md): S1 and S2 built, S3 not built |
| Worlds declare their own laws | [Declared-laws plan](../plans/declared_laws.md): S1 to S3 built, S4 under way, S5 follows the plain-version comparison (Q60) |
| Waltzman lineage against the general simulator vision | [Lineage review, 2026-11-07](../audits/waltzman-lineage-review-2026-11-07.md) (recommendations not adopted) |
| Prior art for attempts, affordances, knock-on effects | [Flexible simulator prior art](../research/flexible-simulator-prior-art-2026-10.md) |

## Concepts and terminology

The full glossary is [arc42 section 12](../architecture/arc42.md#12-glossary). The terms used most:

- **Canonical state:** the one material world truth. Prompts, page state, residents' beliefs and analyses
  read it and never compete with it.
- **Authoring bundle:** what exists in a world (entities, typed properties, relations, action signatures,
  presentation intent, declared resources and laws). Not executable law by itself.
- **Causal model:** the reviewable rule language (`world-substrate-causal-model/v0`): actions and
  processes with selectors, checks and effects, as data, never model-written source.
- **Derived authority:** the read and write paths the compiler finds in a rule. A rule cannot write
  outside them; read scopes are recorded but not enforced.
- **Mechanic profile:** the frozen set of installed rules for one run. Its id does not yet include a
  compiler version (open question).
- **Declared law:** a world's own conservation or payment law, checked at every commit; a step that
  breaks one is refused and names it (`src/world_substrate/laws.py`).
- **Open attempt:** a resident's move in their own words, read by an interpreter into one typed move or
  left unmatched; an unmatched attempt changes nothing except a request to another person, which is
  passed on to that person (#326).
- **Same-moment knock-on effect:** a `timing: immediately` process that reacts inside the same commit, in
  waves of at most 32 reactions ([Decision 009](../decisions/009-same-moment-knock-on-effects.md)).
- **Task under way:** a move that only starts a duration-bearing activity; later rounds' processes finish
  it or stop it part-way, from what is true then (`scripts/attempts.py`; read in
  [c1r24](../../evidence/waltzman-tasks-slice2/c1r24/TRACE_READ.md)).
- **Semantic binding:** an action kind's citation of a reviewed Linguistic Core sense and roles. Meaning
  never implies an effect; six of seven M1 kinds are bound and `unheat` is deliberately unbound.
- **Information lineage versus causal parent:** who was told what, by which channel, is recorded
  separately from the causal parents a rule declares. Being shown a message is not proof it caused a
  decision.
- **Causal claim boundary:** "why this happened" means why inside the represented world under its
  installed rules, not a claim about the real world.

## Sources and evidence

Donor repositories and their roles are in [arc42 section 3](../architecture/arc42.md#source-dispositions);
[references/sources.json](../../references/sources.json) pins reviewed revisions. Donors are sources, not
runtime dependencies.

Every run reported as evidence is a folder with `run-log.jsonl` and a `TRACE_READ.md`, enforced by
`scripts/check_trace_reads.py`; the [documentation index](../index.md#8-run-evidence) lists all of them.
The evidence most often needed:

- the declared-laws builds, S1 to S4, including the Waltzman rebuild of 2026-11-04
  ([s4-waltzman-3](../../evidence/declared-laws/s4-waltzman-3/TRACE_READ.md));
- the open-attempt airfield runs ([S2](../../evidence/open-attempt/s2-airfield/TRACE_READ.md));
- the gpt-6-luna rules measurement: 23 of 24 builds reached their finish line, 19 of 24 also faithful, at
  $0.0032 per build ([trace read](../../evidence/luna-rules-2026-10-23/TRACE_READ.md));
- three replicated Kitchen full-service traces (`evidence/kitchen/full-service-replication-v1-summary.json`);
- the Waltzman reference world's blocked baseline and intervention fork (`evidence/waltzman/`).

Full World Builder request, response, compiler, operator and causal logs are the debugging source of
truth; summaries and replays are orientation only.

## Accepted authorities and decisions

- [Roadmap](../../roadmap/README.md) owns sequencing and the exact next action.
- [arc42](../architecture/arc42.md) owns durable boundaries; the [capability specs](../../openspec/specs/)
  own required behavior, each for its own seam.
- Decisions [001](../decisions/001-project-scope.md) (one canonical project),
  [002](../decisions/002-observability-and-replay.md) (observability required, exact replay not),
  [003](../decisions/003-semantic-mechanical-boundary.md) (meaning does not imply effects),
  [004](../decisions/004-product-and-adoption-strategy.md) (own causal reality, borrow the rest),
  [005](../decisions/005-native-waltzman-delivery.md) (native Waltzman delivery),
  [006](../decisions/006-governed-rules-layer-scope.md) (governed-rules layer only),
  [007](../decisions/007-any-scenario-path.md) (describe any scenario),
  [008](../decisions/008-build-worlds-in-an-agent-harness.md) (build worlds in an agent harness) and
  [009](../decisions/009-same-moment-knock-on-effects.md) (same-moment effects are rule semantics).
- Code and tests own runtime behavior; run-bound evidence owns observed outcomes.
- Human product decisions recorded without exact words: 2026-09-09 (a sendable demo needs
  natural-language generation, a fresh run and living inspection), 2026-09-18 (converge on native World
  Substrate), 2026-09-12 (richer Linguistic Core roles allowed; the semantic/effect boundary unchanged).

## Working context

| Area | State on 2026-11-09 |
| --- | --- |
| Transition engine | built; write scopes enforced; read scopes recorded only (the check reports a constant, Q34) |
| Rule authoring | built: rules as data, compiler-derived authority, processes `each_round` or `immediately`, linked participants |
| Declared laws and rules review | built (S1 to S3); people worlds such as Waltzman declare laws and get the review (#314) |
| Open attempts | built (S1); requests reach the person asked (#326); skill rolls not built (S3) |
| Residents | Concordia residents since 2026-10-16 (`scripts/concordia_residents.py`); the Concordia game master is off |
| World Builder | live on the VPS since 2026-10-05; share links store and replay runs; the Network shows one round at a time (#338, #344) |
| Budget | visitors share $3.00 a day, the owner $5.00; up to four AI jobs at once (`scripts/world_builder_service.py`) |
| Agent harness (Decision 008) | `scripts/world_harness.py` exists but the live service does not call it (Q14) |
| People-world path | imports code from `spikes/any-scenario-2026-10/` at run time (`scripts/people_world.py:26,76-77`) |
| Scheduling | integer ticks; `Engine.advance()` checks each process with `due(world)`; no future-event queue |
| Living scene renderers | maintained, not extended (Decision 006) |
| Persistence and identity | no saved user worlds beyond share links; owner identified by password only |

## Needs resolution

The [open questions ledger](../planning/open-questions.json) holds each item with what it blocks, what
would settle it, its owner and sources. The ones that shape the next work:

1. **Q60 (agent, settled 2026-11-09 by Brian's plain-version rule):** compare today's generated people-world
   rules with one model given the whole scenario, before S5's paid builds or more people-world repair.
2. **Q12 (Brian, answered 2026-11-10):** "stop condition should be configurable". Each world now has a
   "When to stop a run" setting (stop once nothing is changing after 6 quiet rounds by default, or always run
   every round), built in PR #356 (`scripts/run_stop.py`). Brian, 2026-11-10: "i should be able to stop a world
   based on budget or number of rounds or a natural langue stopping potin that the judge assesses once we build him".
   The same setting now also takes "Stop after N rounds" and "Stop when this run has spent $X" (the cost llm_client
   recorded for the run's calls, checked before each round), each optional; the run stops at whichever fires first.
   The plain-words stopping point waits for the judge ([AI judge plan](../plans/ai_judge.md), R11, A8).
3. **Q14:** the Decision 008 harness exists but the live service does not use it.
4. **Q34:** declared read scopes are not enforced.
5. **Q45, Q48, Q49:** retiring hand-written build checks once declared laws cover them; laws that are
   wrong for their world; builds that declare no payment law.
6. Hardening carried from the architecture review: law fingerprints without a compiler version,
   write-scope placeholders not bound to one action role, the 256-move discovery cap truncating silently,
   and mechanic exceptions not recorded as refusals ([arc42 section 11](../architecture/arc42.md#11-risks-and-technical-debt)).

## Architecture and workflow

```text
plain-language description  --(Create simulation = approval)-->
  structure + declared laws (authoring bundle)      rules (causal model)
                 \                                   /
                  compiler derives authority; laws checked; rules reviewed by a second model
                                    |
                     free scripted test run; frozen mechanic profile
                                    |
        Concordia resident picks an offered move or writes an open attempt
                                    |
     Engine: checks -> one commit or refusal -> same-moment knock-on waves -> declared-law check
                                    |
            canonical state + causal events + run log (run-log.jsonl, trace ids)
                                    |
          read-only views: round feed, Network, build record, share-link replay
```

The building blocks and their code are in [arc42 section 5](../architecture/arc42.md#5-building-block-view)
and [model.c4](../architecture/model.c4). Views, residents' memories and analyses never write canonical
state.

## Human-reviewable artifacts

- <https://brianmills.dev/world-builder/>: the World Builder (one box, Create simulation, live play).
- <https://brianmills.dev/world-builder/play/>: Replay Studio over retained traces.
- <https://brianmills.dev/world-builder/build/>: the advanced form editor.
- <https://brianmills.dev/waltzman/>: the donor-backed Waltzman demo, kept as fallback.
- <https://brianmills.dev/world-substrate-visualization/>: the 2026-09 synthetic prototype, design evidence only.
- Review pages for the planning packages: `hive.brianmills.dev/plans/world-substrate/main/proposals/{planning-package,open-attempt,declared-laws}/review-page/`.
- `evidence/renders/waltzman-demo-v0.html`, `evidence/renders/kitchen-spatial-replay-v1.html` and
  `evidence/renders/greenhouse-zero-review-v0.html`: retained reference replays.

## Roadmap

Use [the roadmap](../../roadmap/README.md) for priorities, risks, refresh triggers and the exact next
action. This wiki is orientation only and must not become a second roadmap.
