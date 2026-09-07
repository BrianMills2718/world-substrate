# World Substrate

World Substrate is the canonical project for building persistent, observable worlds where agents express semantically grounded intents and installed mechanics with explicit local authority determine and commit causal consequences.

The project combines:

- typed persistent world state;
- Linguistic Core sense and role bindings without ontology-implied effects;
- reusable actions, autonomous processes, and installed institutions;
- state-derived, bounded affordances;
- singular commit boundaries and inspectable causal traces;
- pre-run, agent-assisted mechanics expansion through frozen world profiles; and
- LLM or human policies that remain outside consequence authority.

Exact replay is an implemented M1 capability, not a project-wide requirement. See [Decision 002](docs/decisions/002-observability-and-replay.md).

**Part of a wider research cluster.** This repo is the one applied consumer
in a wider cluster on canonical semantic representation and capability reuse
for AI-generated software: it consumes
[`linguistic-core`](https://github.com/BrianMills2718/linguistic-core) for
action/effect grounding, with a narrower, applied need than the cluster's
other vocabulary/compiler repos (`factgraph`, `hypergraph-schema-ir`,
`semantic-foundry`, `requirement-to-runtime-semantic-compiler`). For current
state, open cross-repo decisions, and how these repos relate, see the
baseline synthesis page in
[`BrianMills2718/vision`](https://github.com/BrianMills2718/vision):
[`wiki/synthesis/ontology-semantic-cluster-baseline-2026-09-07.md`](https://github.com/BrianMills2718/vision/blob/main/wiki/synthesis/ontology-semantic-cluster-baseline-2026-09-07.md).

Start with:

1. [Project wiki](docs/wiki/README.md) — orientation, terminology, sources, and task routes.
2. [Roadmap](roadmap/README.md) — current truth, active slice, later milestones, and decisions.
3. [Architecture](docs/architecture.md) — enduring system boundaries.
4. [Core contract v0](docs/contracts/core-v0.md) — the implemented M1 seam.
5. [Proposed semantic/mechanical contracts](docs/contracts/semantic-mechanical-binding-v0.md) — the next architecture seam.

## Where this stands

**The substrate works, the prototype phase is complete, and flagship work is underway.**

Phase one specified, built, and tested the substrate contracts. The two small reference worlds — Castaway and the workshop — exist to prove those contracts work and transfer. Phase two is about making one world worth showing rather than adding more assurance to the substrate for its own sake.

The flagship world is a kitchen where two cooks with different orders share one knife, two burners, and exactly enough ingredients that waste loses a dish. Three fresh terminal-state services reproduced the same unprompted handoff: Bo finishes at t9, releases the knife explicitly for Ama at t10, Ama takes it at t11, and both orders are complete at t17. `evidence/renders/kitchen-flagship-v1.html` turns one of those retained traces into a self-explanatory timeline showing reasoning beside order progress, holdings, knife ownership and causal actions. See [the kitchen audit](docs/audits/kitchen-contested-world.md) for the evidence and caveats, and the [roadmap](roadmap/README.md#vertical-slices-and-current-work) for the remaining human boundary.

If you are picking this up cold:

1. **Watch the flagship** — open `evidence/renders/kitchen-flagship-v1.html`. Read each cook on the outside and the shared world state in the center; t10/t11 is the knife handoff.
2. **Run one** — `python scripts/run_contested_world.py --world kitchen --turns 12` uses scripted policies and costs nothing.
3. **Read the roadmap's active slice** before changing direction. The next unresolved step is a human review/publication choice, not another substrate feature.

There is still no deployment, and no repository outside this one imports `world_substrate`.

## What phase one established

M1 is promoted. The neutral runtime reaches the pinned final freshwater checkpoint through registered fill, heat, unheat, pour, drink, take, and give actions plus deterministic processes. Retained evidence compares semantic state and conservation fields, preserves vessel identity across liquid, heat, carrying, and bounded ownership systems, and distinguishes precondition failure from unsupported and malformed actions. Its versioned initial snapshot, pinned registry/content identity, and 22 commands also reproduce the final state and events in a [fresh process](evidence/m1/transfer-replay-v1.json). The revision-bound [end-to-end observation](evidence/m1/end-to-end-observation-v1.json) passed the M1 maturity gate.

M3 is complete: one adjacent mechanic was authored offline as a reviewable package, installed with no findings, frozen into a profile, and run. It was run adversarially — the package omits a real consequential dependency — and the result is that installation alone surfaces nothing, two complementary interaction assays surface it, and one incoherence survives both. See [the M3 experiment](docs/audits/m3-overheat-authoring-experiment.md).

M7 tested the half of the central hypothesis that had never been tried: whether an agent can author a mechanic it was not handed. A model shown the workshop world — told neither which mechanic to write nor what the checks look for — produced nine installable mechanics for $0.015 with zero write-scope violations. Five added real behaviour, two were inert no-ops, and two violated an ownership convention the world never declared and therefore nothing can check. Risk did not outrun usefulness; triviality, not danger, is the bottleneck. See [the M7 audit](docs/audits/m7-authoring-rate.md).

M7b asked whether that triviality was the model's or the language's, since a language confined to one entity can only express a clamp or a decay — and, for the same reason, can barely express a scope violation. The language now expresses one relation between two entities, and the experiment was re-run unchanged otherwise. Four of eight valid declarations used the relation and two produced cross-entity behaviour nothing here could previously express, but the same two inert clamps came back: the ceiling was real and was not the main driver. Zero scope violations again, this time against machinery a relational write can genuinely load. And the empty-`owner_ref` defect recurred at the same rate from the same model — and was refused by the substrate instead of committing. See [the M7b audit](docs/audits/m7b-relational-authoring.md).

All six prototype success criteria are met as of M6. A [second reference world](docs/audits/m6-second-world.md) — a workshop of discrete parts and tools, sharing no content with Castaway — reuses the transition kernel, causal events, exact replay, the mechanic-profile installer, all three interaction assays and the policy seam with no edits, while reusing none of the Castaway mechanics. Four substrate/content couplings were found and fixed in the process.

M5 is the first time a policy other than a script drove this world: an LLM chose 16 actions through the ordinary affordance seam for $0.005, beat a no-foresight baseline on health 60 to 4, and was corrected by a mechanic when its stated belief about the world turned out to be wrong. See [the M5 audit](docs/audits/m5-policy-consumer.md).

M4 completes the pair. A second mechanic, authored without a planted omission, closes M3's uncaught incoherence and keeps volume conserved. The three assays behaved completely differently on it — the behavioural one found nothing at all, because every affordance was already refused — establishing that no single assay basis, and no pair, is sufficient. See [the M4 experiment](docs/audits/m4-spill-experiment.md).

What remains of the semantic/mechanical frontier is narrower than it was: `give` is bound and exchange derives without double application (M2), and a policy consumer has run under a granted $2 cap (M5). Still open are the upstream-owned `unheat` semantic binding, optional read-scope verification, and the other explicitly listed obligations in the roadmap.

Related repositories remain unchanged and are classified in [source dispositions](docs/source-dispositions.md).

## Project checks

```sh
python scripts/check_project.py
python scripts/run_first_fill_probe.py --check
python scripts/run_boiling_probe.py --check
python scripts/run_pour_probe.py --check
python scripts/run_drink_probe.py --check
python scripts/run_transfer_probe.py --check
python scripts/replay_transfer_evidence.py --check
python scripts/run_freshwater_probe.py --check
python scripts/run_give_exchange_probe.py --check
python scripts/run_overheat_assay_probe.py --check
python scripts/run_spill_assay_probe.py --check
python scripts/run_authoring_experiment.py --check --output evidence/m7/authoring-attempts-relational-v1.json
```

Two things here are run rather than checked, because they show behaviour rather than pin it:

```sh
# a contested run with scripted policies, no model calls
python scripts/run_contested_world.py --world kitchen --turns 12

# re-render a retained policy trace as belief beside replayed world state
python scripts/render_belief_vs_truth.py evidence/m5/llm-policy-v0.json
```

The authoring command re-grades the retained M7b declarations without calling a model. The retained M5 and M7 traces are live observation receipts rather than deterministic probes, and are deliberately not gated.

The default project check is self-contained and uses committed fixtures. When the sibling donor repositories are available, also run `python scripts/check_project.py --with-donors`; the optional donor check reads pinned revisions rather than requiring their current checkouts to remain at those commits.
