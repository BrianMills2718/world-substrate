# World Substrate

> **Global navigation:** the [Vision knowledge index](https://github.com/BrianMills2718/vision/blob/main/wiki/index.md) is the cross-repository entry point. This README is the local entry point.

World Substrate is a persistent, observable world engine in which people (AI, scripted or human) express intents and **installed mechanics, not model prose, decide canonical consequences**. A generative builder sits on top: describe a world in plain words, and it proposes the world's structure, its laws and its rules as data that a local compiler checks before anything runs.

- **World Builder:** <https://brianmills.dev/world-builder/>: one box and one Create simulation button. Pressing it is the approval; the world is built, its rules reviewed by a second model and tested for free, and then played live one round at a time.
- **Waltzman donor demo (fallback):** <https://brianmills.dev/waltzman/>
- **2026-09 synthetic prototype (design evidence only):** <https://brianmills.dev/world-substrate-visualization/>

## Start here

1. [Documentation index](docs/index.md): the reading order and every document.
2. [Architecture (arc42)](docs/architecture/arc42.md): goal, requirements, building blocks, deployment, risks.
3. [Project wiki](docs/wiki/README.md): current state, terminology, what needs resolution.
4. [Roadmap](roadmap/README.md): stage, active slice, risks and the exact next action.
5. [Capability specs](docs/index.md#2-what-the-code-must-do-openspec-capability-specs) under `openspec/specs/`: what the code must do.
6. [Decisions](docs/index.md#4-decisions-madr-records): 001 to 009; [Decision 006](docs/decisions/006-governed-rules-layer-scope.md) sets the current scope.

## Where this stands

State on 2026-11-09 (`main` at `0e66a98`). The prototype substrate phase is complete; the World Builder is the live product surface; Waltzman Coordination Lab is the showcase world.

| Capability | Current state |
| --- | --- |
| Canonical typed world state, atomic commit or refusal, causal events | built |
| Declared write scopes | enforced; declared read scopes are recorded, not enforced |
| Rule language and compiler | built: rules as data with compiler-derived authority; processes run each round or immediately; linked participants |
| Declared world laws | built and deployed: each world declares its resources and laws (people worlds too since #314); the engine refuses a step that breaks one and names the law |
| Independent rules review | built and deployed: a model of another family reads the rules against the description and laws |
| Open attempts | built: residents say what they try in their own words; requests reach the person asked (#326); skill rolls not built |
| Same-moment knock-on effects | built: waves inside one commit, no cap since 2026-11-10 (each rule fires once per thing per moment), every step names its cause, blocked steps shown ([Decision 009](docs/decisions/009-same-moment-knock-on-effects.md)) |
| Residents | Concordia since 2026-10-16; since 2026-11-10 (AI judge J2) Concordia's game master (`EventResolution`) is on only as the judge for attempts no rule covers: it proposes a rule, test-runs it on a copy, then confirms, revises once or withdraws; a confirmed ruling becomes a rule since J3 (2026-11-10): installed at once ("Approved by Create", the default) or held until the owner presses Approve ("Wait for my approval"), with a ruling the rules language cannot express listed as a language gap |
| Live play, share links, run page | deployed on the personal VPS since 2026-10-05; a share link stores and replays a run |
| Linguistic Core binding | six of seven M1 action kinds; generated action kinds are not semantically bound |
| Waltzman reference world | blocked baseline, exact-history intervention, living projection, information kept apart from causal parents, detachable analysis |
| Saved user worlds and identity | share links only; the owner is identified by password |

## Architectural thesis

A rich world should come from **shared persistent state, semantic grounding and installed causal mechanics**, not from asking a model to narrate plausible consequences. Brian's reason is scale (2026-11-09): facts must carry their implications and blockers down causal chains far longer than a model can follow; his words are quoted in [arc42 section 1](docs/architecture/arc42.md#architectural-thesis).

Policies receive bounded observations and offered moves, or write an open attempt that an interpreter reads into one typed move; they never mutate world truth. Linguistic Core supplies meanings and roles, never effects ([Decision 003](docs/decisions/003-semantic-mechanical-boundary.md)). World Substrate is the governed-rules layer only; resident loops, scheduling and planning come from Concordia, Mesa or a PDDL export when a world needs them ([Decision 006](docs/decisions/006-governed-rules-layer-scope.md)).

## Reference worlds

| World | Purpose |
| --- | --- |
| Castaway | M1 reference world: persistent state, processes, semantic bindings, exact pinned replay |
| Workshop | second world: showed which "general" code was really freshwater content |
| Kitchen | replicated watched world: three runs reproduced Bo filling at t9, releasing the shared knife at t10, Ama taking it at t11, terminal at t17 |
| Greenhouse | new world with zero-review automatic replay |
| Orchard, Repair Bay | live authoring acceptance; first nontrivial deployed authoring world |
| Waltzman Coordination Lab | showcase: the hand-authored reference world, and the scenario built live through the people-world path |
| CVS sustainment | import of a Compositional Viable Systems situation |

See [reference_worlds/README.md](reference_worlds/README.md).

## Important current limitations

Tracked with sources in the [open questions ledger](docs/planning/open-questions.json) and [arc42 section 11](docs/architecture/arc42.md#11-risks-and-technical-debt):

- Declared read scopes are recorded, not enforced, and write-scope placeholders are bound to participants rather than one action role.
- The mechanic profile id does not include a compiler version; the 256-move discovery cap truncates silently; a mechanic that raises is rolled back and re-raised rather than recorded as a refusal.
- Compiler acceptance establishes declared authority and type consistency, not causal completeness; the Waltzman adequacy report is a dependency inventory, not counterfactual proof.
- Causal parents are mechanic-declared and history-validated, not inferred from reads, and not proof of real-world causality.
- The Decision 008 agent harness exists but the live service does not call it; the people-world path imports code from `spikes/any-scenario-2026-10/`.
- Information delivery is bounded: no generic latency, corruption, audience groups or deception.
- Scheduling is integer ticks with per-step `due()` checks; there is no future-event queue.
- `unheat` stays unbound because Linguistic Core has no reviewed sense for it.

## Cross-repo role

World Substrate is the applied persistent-world engine and a demanding consumer of semantic grounding. Ontology terms do **not** imply causal effects here. Donor repositories are sources, not automatic adoption instructions; their roles are in [arc42 section 3](docs/architecture/arc42.md#source-dispositions) and the [ontology/semantic cluster architecture](https://github.com/BrianMills2718/vision/blob/main/wiki/synthesis/ontology-semantic-cluster-current-architecture-2026-09-07.md).

## Verification

`make check` runs the project check: navigation, authority surfaces, links, spec status facts, retained evidence and the test suite. The tests need `pydantic`, Concordia, `pytest` and `pytest-xdist`, which the plain system Python lacks; the Makefile supplies them through `uv`:

```sh
make check
# the same as:
PYTHONDONTWRITEBYTECODE=1 uv run -q --no-project --python 3.12 --with pydantic --with pyyaml --with gdm-concordia==2.4.0 \
  --with pytest --with pytest-xdist python scripts/check_project.py
```

A pass on a clean checkout stamps its tree in `~/.cache/world-substrate/passed-trees/`; `scripts/deploy_world_builder.sh` skips the gate for a tree that already passed (a squash merge keeps the pull request's tree), and otherwise runs it before deploying. Before merge, run only the test files a change touches (`python -m pytest tests/test_x.py -n 8`) and look at any page it changes; the full check runs nightly on main through `gates-nightly`, and a nightly failure goes to an agent to fix.

Useful deterministic probes:

```sh
python scripts/run_waltzman_demo.py --check
python scripts/run_first_fill_probe.py --check
python scripts/run_transfer_probe.py --check
python scripts/replay_transfer_evidence.py --check
python scripts/run_freshwater_probe.py --check
python scripts/run_give_exchange_probe.py --check
python scripts/run_overheat_assay_probe.py --check
python scripts/run_spill_assay_probe.py --check
```

Use `python scripts/check_project.py --with-donors` when the locally pinned donor revisions are available. Every run reported as evidence needs `run-log.jsonl` and a `TRACE_READ.md` (`scripts/check_trace_reads.py`); before any paid live run, follow the free-replay rules in [tests/AGENTS.md](tests/AGENTS.md).
