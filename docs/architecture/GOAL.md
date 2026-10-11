---
description: Goal, requirements, thesis and non-goals of World Substrate, the governed-rules layer for generated worlds.
---

# World Substrate goal and requirements

This is the durable statement of what World Substrate is for and how to tell whether it works. It condenses the roadmap's end goal, the operating invariants and Decisions 006 and 007; those stay the editing authorities for their own detail. The implemented system is described in [the system model](../model/ODD.md); its enforced rules and the tests that check them are in [trace.yaml](../model/trace.yaml).

## 1. Introduction and Goals

World Substrate lets a person describe a bounded world in plain language, review the rules the system compiles from that description, approve them, and then run residents (scripted, human or LLM policies) through the world. Residents only express intents. Installed, reviewed mechanics alone decide what changes in the canonical world, and every change or refusal leaves an inspectable record. Per [Decision 006](../decisions/006-governed-rules-layer-scope.md), the repository owns only the governed-rules layer; agent minds, generic schedulers and planners are hosted on off-the-shelf runtimes (Concordia, Mesa) that call into it.

### Requirements Overview

#### REQ-INTENT-NOT-CONSEQUENCE

A policy (scripted, human or LLM) can only submit an action envelope; it never writes canonical state. The Engine validates the envelope, runs the installed rule and commits all of its writes or none of them.
Success: a malformed or stale envelope, or a rule that reaches outside its declared write scope, is refused with the world's material hash unchanged and the refusal recorded (`tests/test_action_envelopes.py`, `tests/test_first_fill.py`, `tests/test_write_scope.py`).
Disproof: any test or retained run where a refused transition changed canonical state, or where model prose rather than an installed rule produced a committed change.

#### REQ-REVIEWED-AUTHORITY

The authority a rule has (what it reads, writes and when it fires) is derived by the compiler from the rule itself and shown to the reviewer; it is never taken from what the model claims.
Success: the review payload lists compiler-derived read and write paths, unknown effect paths are rejected before installation, and the compiled profile is frozen before the first run step (`tests/test_action_authoring.py`, `tests/test_run_authored_world.py`).
Disproof: a run whose installed rule wrote a path the review did not show, or a profile that changed between approval and execution.

#### REQ-APPROVAL-AND-BUDGET-BEFORE-SPEND

No mechanics run and no model call is made until the person has explicitly approved the mechanics and the request fits the daily budget.
Success: the World Builder service refuses a run without approval (HTTP 409), refuses an unapproved model before any spend, and fails closed on a corrupt budget ledger (`tests/test_world_builder_service.py`).
Disproof: a logged model call or run step that precedes approval, or a day whose recorded spend exceeds the configured cap.

#### REQ-OBSERVABLE-RUNS

Every build and run leaves a durable record from which the person can see what happened and why: events with stable ids, mechanic-declared causal parents, and a live view rebuilt only from canonical state ([Decision 002](../decisions/002-observability-and-replay.md)).
Success: snapshot plus event deltas reconstruct each canonical branch exactly, and every build and run writes its record (`tests/test_waltzman_projection.py`, `tests/test_world_builder_service.py`).
Disproof: a view showing a state the canonical event log cannot reconstruct, or a run with no durable record.

#### REQ-ANY-SCENARIO

A person can describe a scenario outside the reference worlds and get a modelled world up front, attempts over time, and rules written mid-run under the same review and approval gates ([Decision 007](../decisions/007-any-scenario-path.md)).
Success: a fresh description produces a reviewable draft, an approved run on the native Engine, and the automatic living view, with mid-run rules passing the same compiler review as up-front ones (evidence under `spikes/any-scenario-2026-10/evidence/`).
Disproof: a described scenario that can only run after hand-written Python mechanics, or a mid-run rule installed without compiler review.

### Quality Goals

1. Truthfulness of consequence: what the world records is what installed mechanics did, never what a model asserted.
2. Inspectability: a person can answer "why did this happen" from the retained record alone; observability is required, exact replay is not ([Decision 002](../decisions/002-observability-and-replay.md)).
3. Generality: the same engine and authoring path serve materially different worlds (Kitchen, Orchard, Repair Bay, Waltzman) without per-world engine code.
4. Small owned surface: anything a commodity runtime already does is adopted, not rebuilt ([Decision 004](../decisions/004-product-and-adoption-strategy.md), [Decision 006](../decisions/006-governed-rules-layer-scope.md)).

### Stakeholders

| Who | What they need from World Substrate |
| --- | --- |
| Brian (owner) | A working builder and demo that show generated worlds with executable laws, and an engine other projects can host. |
| Demo visitors and stakeholders | One click from a description to a running world they can watch and question (World Builder, Waltzman Coordination Lab). |
| Researchers using Waltzman's coordination model | A reference world whose trust, risk and coordination dynamics run under inspectable mechanics. |
| Coding agents working in the repository | Clear owners, invariants and checks for every enforced rule (this file, the system model and `trace.yaml`). |

## North star (AES extension)

Generative worlds with executable laws: a person describes any bounded world in plain words, approves the laws the system proposes, and watches residents live in it while every consequence traces back to an approved, installed rule.

## Thesis (AES extension)

A world built by LLMs stays trustworthy only if consequences come from reviewed, installed mechanics with explicit local authority, and the canonical state they write is the single place truth lives: views, cognition and analysis read it but never become alternate truth. This applies AES-CTX-004 (truth lives where it is edited) to simulation: the Engine's committed state and event log are where world truth is edited, so everything else is a projection of them.

## Thesis disproof (AES extension)

The thesis fails if a reviewed, approved world still produces consequences the person cannot trace to an installed rule, or if keeping consequences in reviewed mechanics makes describing a new scenario so slow that a direct LLM narration (for example YuLan-OneSim or Concordia's game master) gives users equally trustworthy worlds at a fraction of the effort, as measured in `spikes/any-scenario-2026-10/evidence/onesim-comparison.md`.

## Non-goals

- Recreating Dwarf Fortress, or a universal real-world ontology or physics engine.
- LLM-generated consequences, or unrestricted natural-language world mutation.
- Owning agent cognition, generic scheduling or planning that Concordia, Mesa or a PDDL planner already provides ([Decision 006](../decisions/006-governed-rules-layer-scope.md)).
- Claiming predictive or empirical validity for social or physical systems; causal claims hold inside the represented world under its installed mechanics only.
- Bulk-copying related repositories into this one ([Decision 001](../decisions/001-project-scope.md)).

## Lineage (AES extension)

None -- original repository, started 2026-08-31 under [Decision 001](../decisions/001-project-scope.md) with Castaway as the first extraction donor and Cybernetic Influence V3 as a selective capability donor. This document was condensed on 2026-10-10 from `README.md`, `AGENTS.md`, `roadmap/README.md` (End goal and Causal product contract), `docs/wiki/README.md`, and Decisions 001, 002, 004, 006 and 007.
