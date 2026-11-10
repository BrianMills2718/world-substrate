# World Substrate

Build a persistent, observable world substrate in which LLM or human policies express semantically grounded intents and installed mechanics alone determine canonical consequences.

## Start here

Read [the documentation index](docs/index.md) for the reading order, [the project wiki](docs/wiki/README.md) for orientation and [the roadmap](roadmap/README.md) for current direction. Before changing any system, read [the arc42 architecture](docs/architecture/arc42.md); required behavior is in the OpenSpec specs under `openspec/specs/` (change them through `openspec`), and human-set doctrine is in [accepted decisions](docs/decisions/); [Decision 006](docs/decisions/006-governed-rules-layer-scope.md) sets the current scope (governed-rules layer only, hosted on commodity runtimes).

Before editing a scoped subtree, read its local `AGENTS.md`:
- documentation and specs: `docs/AGENTS.md`
- planning authority: `roadmap/AGENTS.md`
- reference worlds: `reference_worlds/AGENTS.md`
- fixtures/verification: `tests/AGENTS.md`

## Invariants

- One canonical persistent world owns material truth.
- Policies and natural-language descriptions never mutate canonical state directly.
- Linguistic Core supplies senses/roles; installed mechanics supply effects.
- Mechanics propose; one enclosing transition validates and commits or refuses.
- Declared write scopes and a world's declared laws are enforced (the engine refuses a step that breaks a law and names it, `src/world_substrate/laws.py`); declared read scopes are recorded, not yet enforced.
- Composite/analytic descriptions do not duplicate primitive effects.
- Unsupported or defective behavior fails visibly without partial mutation.
- Resident cognition and post-run analysis remain separate from canonical world truth.
- Every attempted transition leaves inspectable causal evidence.
- A run reported as evidence is saved as a folder with its server run-log lines (`run-log.jsonl`) and a `TRACE_READ.md` read-through: a `## Round N` section per round naming everyone who tried a move and citing an event id, every llm_client trace id, and `## Findings`. `scripts/check_trace_reads.py` (part of `check_project.py`) enforces it; `--skeleton <folder>` prints the headings. Before any paid live run, follow the free-replay and scope rules in `tests/AGENTS.md` ([lessons](docs/wiki/lessons.md)).
- A World Substrate causal claim is about why a transition occurred **inside the represented world under its installed mechanics**; it is not by itself a claim that those mechanics are scientifically true of the real world.

## Current boundary

The World Builder at `https://brianmills.dev/world-builder/` is the live product: one box and Create simulation (pressing it is the approval, Brian 2026-10-15); the builder proposes structure, declared laws and rules, a second model reviews the rules, a free scripted test checks them, and Concordia residents play live. Its backend runs on the personal VPS (personal-vps `apps/world-builder`, image `deploy/vps/Dockerfile`, Worker `world-builder-api`); ship with `scripts/deploy_world_builder.sh`. Waltzman Coordination Lab is the showcase world; the donor-backed `/waltzman/` surface is a fallback and must not be presented as a native run.

Do not add engine, scheduler, renderer or cognition capability of World Substrate's own; host loops on Concordia or Mesa when a world needs them (replacement-first gate, [roadmap](roadmap/README.md#exact-next-action)). A bounded same-moment fixpoint of `timing: immediately` processes inside the existing commit is rule semantics, not engine capability ([Decision 009](docs/decisions/009-same-moment-knock-on-effects.md)). Pydantic AI, SimPy and Cytoscape were selected in 2026-09 but never integrated.

For every live Builder investigation, inspect the complete request/response log and retained causal trace before diagnosing from summaries or replay; summaries and replay are orientation surfaces, not the debugging source of truth.

Make reversible changes without repeated approval. Do not mutate donor repositories. New deployment or publication, provider spend outside the approved World Builder budgets, or runtime-generated-law installation outside the reviewed World Builder path requires explicit authorization; open question Q50 is settled (Brian, 2026-11-09): believability is left to the off-the-shelf people agents, with no metric, and tuned only after everything else runs well, so paid builds are no longer held for a believability judgement. Never create a special handoff document; improve the normal root -> wiki -> authority route instead.
