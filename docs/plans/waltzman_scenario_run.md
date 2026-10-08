---
plan_id: "waltzman-scenario-run"
dependencies: []
dependencies_reviewed: "2026-10-08"
planning_path: durable_solo
planning_path_ref: docs/plans/waltzman_scenario_run/path-decision.json
method_conformance_receipt: docs/plans/waltzman_scenario_run/conformance-receipt.json
goal:
  outcome: "Rand Waltzman's bio-surveillance coordination scenario, typed as plain text, runs end to end through the any-scenario pipeline (checked model, AI members on Concordia with the World Substrate Engine as sole consequence authority, game master writing checked rules mid-run, replay frames), and a short plain-language assessment states, with event-level evidence, which of the paper's four mechanisms the generated world represents and which it misses."
  canonical_example: "Running spikes/any-scenario-2026-10/model_scenario.py on the scenario text in docs/plans/waltzman_scenario_run.md produces a model with recorded trace ids; run_scenario.py runs AI members on it to a recorded end (terminal, quiescent or max ticks); and docs/plans/waltzman_scenario_run.md (Assessment) gives, for each mechanism (concerns delivered to different members through separate channels; meetings that slow; settled issues that reopen; support that becomes conditional), either the Engine event ids and rules that show it or the plain statement that the world does not represent it and why."
  forbidden_substitutes: "hand-edited generated models presented as generated; scripted members presented as AI choices; a mechanism marked represented without an event id from the recorded run; an assessment written from the scenario text or the model file without the run; rerunning until a mechanism appears and reporting only that run (every run made is reported)."
  boundaries: "world-substrate only; work merges through pull requests after scripts/check_project.py passes; cybernetic_influence_v3 and other repositories read-only; no deploy, no outreach to Waltzman, no change to the live World Builder or /waltzman/; model spend capped at $2 for this plan, measured by spikes/any-scenario-2026-10/spend.py from its value at the plan's start; raising it needs Brian's yes."
  done_when: "Acceptance checks W1-W5 in docs/plans/waltzman_scenario_run.md pass, each judged from the full trace of its named run (llm_client trace ids, Engine event lists with event ids, check logs, frames with screenshots, project gate output); report the trace ids and evidence for each, and report every pipeline and member run made, not only the best."
  do_not_gate_on: "whether any particular mechanism appears (the assessment reports what happened); Brian's review; Waltzman's reaction or any outreach; the linked-participants hospital pipeline-only result; distance-limited sensing; Simudyne's reply."
  stop_after: 3
---
# Plan: run Waltzman's scenario through the any-scenario pipeline

## Goal

**Mission:** The point of the any-scenario work is a demo in which Rand Waltzman describes a situation and watches it play out. This plan runs his own scenario, the opening of *From Minds to Coordination*, through the pipeline as it stands. It reports honestly what the generated world captures and what it misses, so the next step is chosen from evidence rather than hope.

**Execution profile:** `continuous-light`

One writer, reversible, one repository.

**Stage and investment boundary:** an evaluation run. About 2–4 hours of agent work and at most $2 of model spend.

**Scenario text** (from the paper's opening, as summarized in `cybernetic_influence_v3/docs/WALTZMAN_OUTREACH_DRAFT.md` and `docs/research/001-from-minds-to-coordination.md`):

> A partnership of four countries and a regional health network must decide by a deadline whether to activate a cross-border bio-surveillance early-warning system. Technical, legal, logistics and community groups each raise small, true but local concerns through their own channels to different members. Members meet regularly; the concerns slow meetings, reopen settled issues and make support conditional, which can delay or block deployment.

**Canonical example:** see the goal block. The pass condition is a complete run plus an honest assessment. It is not the appearance of any particular behavior.

**Forbidden substitutes:** see the goal block.

**Repository / working scope:** `world-substrate`, using `spikes/any-scenario-2026-10/`.

## Actor, result and authority

- **Actor:** Brian, deciding whether the "describe any scenario" path is close enough to show Waltzman, and what to fix first.
- **Result:** a recorded run of his scenario, with frames, and a one-page assessment.
- **Concrete example of the result:** the plan's Assessment section is a four-row table, one row per mechanism, with columns for the verdict, the evidence, and what is missing. One row reads, for example: "Concerns delivered to different members | represented | event `e00012` (rule `deliver-legal-concern`) changes only the Country B member's known concerns, and that member's next decision cites it | — ". The screenshot of the matching replay round sits next to it. The actual verdicts and ids come from the recorded run.
- **Authority:** Brian asked for this goal on 2026-10-08 ("give me the new /goal text"), after the recommendation to run Waltzman's scenario. The implementing agent is the sole writer. Other repositories are read-only.
- **Non-goals:**
  - contacting Waltzman;
  - deploying anything;
  - changing the live World Builder;
  - tuning the pipeline until the mechanisms appear;
  - a comparison between pipeline variants or models.

## Acceptance Checks

| ID | Criterion | Evidence to report |
| --- | --- | --- |
| W1 | The scenario text becomes a checked model through the pipeline (model step plus at most 3 automatic repair rounds) | the trace ids in `model.json`, the final check counts, and a list of every pipeline run made |
| W2 | AI members run on that model on Concordia, with the Engine as the only state authority and the game master on | the run summary (how it ended, attempts, cost), the event count, and the trace id |
| W3 | Frames are rendered from the run, with a screenshot of one round that shows member decisions and Engine events | screenshot path, plus the round's event ids |
| W4 | The assessment gives, for each of the four mechanisms, "represented", with event ids and rule ids from the recorded run, or "missing", with the reason | `docs/plans/waltzman_scenario_run.md`, section "Assessment" |
| W5 | Evidence is committed and the project gate passes | the evidence folder path, plus the `scripts/check_project.py` output and exit code |

## Trace review per criterion

| ID | Run whose full trace is examined | Where it lives | What must be seen beyond the outcome |
| --- | --- | --- | --- |
| W1 | Every pipeline run of the scenario text | `llm_client` traces by id, and the run folder's `model.json`, `checks.json` and repair records | The model was built from the text without hand edits. Repairs came from the automatic loop. Every run made is listed. |
| W2 | Every AI-member run | The run folder (`events.jsonl`, `attempts.jsonl`, `summary.json`), packed with `run-artifacts` | Each state change has an Engine event id. Member decisions cite only their own observations. Rules written mid-run carry checks verdicts. |
| W3 | The render of the W2 run | Rendered HTML and screenshot | The screenshot round's panel lists Engine event ids that exist in `events.jsonl`. |
| W4 | The full trace of the W2 member run: every Engine event, every member attempt record (belief, cited observations, decision), every game-master rule record with its checks verdict, and the model's rules | The W2 run folder (`events.jsonl`, `attempts.jsonl`, `summary.json` with `rules_written_mid_run`), the model folder (`causal.json`), and the `llm_client` traces by id, packed with `run-artifacts` | Each "represented" cell cites an event id and rule id that exist in those files, and the member records that show the effect (for example, a decision citing a concern only that member received). Each "missing" cell names what the model lacks, checked against `causal.json`. |
| W5 | The project gate (`scripts/check_project.py`) on the exact merge commit, run in a git checkout | Full terminal output, saved beside the evidence | Each named check passes (navigation, authority, links, pinned sources). The runtime test count includes the existing tests and no test was skipped. `git diff --stat` shows only the spike, evidence and plan paths. Exit 0. |

## Success and disproof

- **Success:** W1–W5 pass. The assessment is accurate against the recorded files.
- **Disproof** (of the claim that the pipeline is close to a demo of this scenario): the assessment finds three or more of the four mechanisms missing, or the pipeline cannot produce a runnable model in 3 repair rounds. That outcome is a valid result of this plan, not a failure to hide.

## Model calls

- **Call graph and result boundaries,** in pipeline order. Each call returns:
  - **ODD:** a JSON object.
  - **Bundle:** a JSON world bundle validated by `validate_bundle`.
  - **Mechanics:** a JSON causal model compiled by `CausalModel.from_dict`.
  - **Stock map, sensing map, outflow coverage:** Pydantic records validated against the world's own fields and rule ids.
  - **Extreme-conditions and anomaly reviews:** Pydantic verdicts with verbatim log quotes.
  - **Rule writer:** a JSON change list, compiled locally.
  - **Members:** the Pydantic `Attempt`.
  - **Game-master rules:** compiled and checked before installation.
- **Prose never mutates state.**
- **Tracing:** every call goes through `llm_client` with its own `any-scenario-` trace id. Calls are logged to `calls_<date>.jsonl` and summed by `spend.py`.

## Spend and irreversible actions

- **Spend:** OpenRouter model calls under Brian's key.
  - **Authorizer:** Brian. He requested this goal on 2026-10-08, and adopting it sets a $2 cap measured from `spend.py`'s value at the plan's start.
  - **Raising the cap:** needs his explicit yes.
  - **Expected cost:** about $0.50–$1.00 (the model step with sol-tier rules, up to 3 repairs, and one member run).
- **Irreversible actions:** none. There is no deploy and no outreach.
- **Promotion condition:** nothing is shown to Waltzman or deployed from this plan. Before any promotion, one authentic run must hold: a fresh pipeline run of this scenario text on a real model, with its trace ids reported, whose member run shows at least three of the four mechanisms with Engine event ids. A demo is a later, separately approved plan, after an assessment with at most one missing mechanism and a working UI slice Brian has clicked through.

## Uncertainties

Each of these is material: if it resolves badly, the conclusion about how close the demo is changes.

| Uncertainty | Owner | Evidence that resolves it |
| --- | --- | --- |
| Whether the generator represents information that reaches different members | Implementing agent | W4 row 1: delivery events with recipient-specific changes, or their absence in the model |
| Whether a "task" world's size limit (about 10 entities) is enough for this scenario | Implementing agent | W1 model entity count, and the ODD's `not_modeled` list |
| Whether rule writing mid-run invents the coordination rules the paper describes | Implementing agent | W2 game-master records: rules written, checks verdicts, events |

## Prior art and parallel-implementation check

Existing ownership was searched in world-substrate's Decisions 004–007 and in the any-scenario and linked-participants plans. Internal lineage was searched in `cybernetic_influence_v3`, whose live `/waltzman/` demo runs a hand-built 26-role version of this scenario through fixed scenario types, and in World Substrate's native coordination vertical, `reference_worlds/waltzman`, which is hand-authored. Each candidate gets exactly one disposition: reuse, extend, compose, supersede, or bounded exception.

| Candidate | Disposition |
| --- | --- |
| Any-scenario pipeline (`spikes/any-scenario-2026-10/`) | **reuse**, unchanged except fixes the run shows are needed |
| Cybernetic Influence v3 Waltzman scenario and outreach summary | **reuse** as the source of the scenario text and of the four mechanisms (read-only) |
| `reference_worlds/waltzman` (hand-authored native coordination world) | **bounded exception**: not used as input, because the point is generation from text. It is a reference for what a complete model contains. |

**Check for a silent parallel implementation:** no new runner, checker or renderer is added. `git diff --stat origin/main` at the end touches only `spikes/any-scenario-2026-10/` fixes, the evidence folder, and this plan.

## Activation facts

The machine record is `waltzman_scenario_run/activation-facts.json`.

- **`llm_central`: true.** Generation and members are model calls.
- **`irreversible_or_spend_action`: true.** OpenRouter spend, capped at $2. Nothing is irreversible.
- **`shared_mechanism`: false.** No new or changed shared mechanism or contract. A run, an assessment and evidence only.
- **`empirical_comparison_proposed`: false.** One scenario is run and assessed, not a comparison between alternatives.

## Increments

1. Pipeline run (W1).
2. Member run and frames (W2, W3).
3. Assessment, evidence and gate (W4, W5).

## Loop Bounds

- **No-progress stop:** three attempts on the same reproduced blocker without new evidence.
- **Finite bound:** at most 2 pipeline runs and 3 member runs, all reported.
- **Revalidation:** after three increments or about four hours.

## Non-Gating Next Actions

- A larger "ongoing" world size for the full 26 roles.
- Distance-limited sensing.
- A demo UI slice for Brian to click through.

## Assessment

From pipeline run `waltzman-20261008T123134` and member run `run-20261008T125239`. Evidence is in `spikes/any-scenario-2026-10/evidence/waltzman/`.

**Bottom line:** none of the four mechanisms appears in the run. The generated model has the parts for two of them: a concern can be sent to one member, and a meeting resolves a concern. But it has no source of concerns. The four groups that raise them are listed as not modeled. So every member approved in the first round, and the system was switched on in the second (`e00011`). By the plan's own disproof condition (three or more missing), the pipeline is not close to a demo of this scenario.

| Mechanism | Verdict | Evidence | What is missing |
| --- | --- | --- | --- |
| Concerns delivered to different members through separate channels | missing | Rule `submit-concern` adds to one recipient's `concerns_received` and `unresolved_concerns` (`causal.json`). It was offered to every member in round 1 (`run/attempts.jsonl`, tick 0), and none chose it. Country A's belief: "no observed concerns or conditional-support requirement". No `submit-concern` event exists in `run/events.jsonl.gz`. | The groups that raise concerns (technical, legal, logistics, community) and their channels are in the model's `not_modeled` list (`model.json`). Members have no concern of their own to send. |
| Meetings that slow | missing | Rule `hold-meeting` uses meeting time and resolves one concern, but it is offered only when a member holds a concern. It never fired. | There is no meeting schedule, and no rule makes a meeting longer as concerns pile up. Both are in `not_modeled`. |
| Settled issues that reopen | missing | Votes go from `approve` to `counted_approve` (`e00001`–`e00005`, `e00007`). No rule sets a vote back. `apply-weekly-unresolved-concern-pressure` needs more than eight unresolved concerns, and it never fired. | No rule reopens a decision. |
| Support that becomes conditional | missing | Every member has a field `conditional_support`, false at the start. No rule in `causal.json` writes it. | No rule makes support depend on a concern being resolved. |

Members did try to coordinate on concerns. In round 2, Countries B, C and D each proposed a shared register of concerns or a time-boxed review, an action the model did not offer. The game master's proposed rules made the checks worse, so each attempt was recorded as a ruling with no effect (`e00008`–`e00010`, traces `any-scenario-gm-waltzman-20261008T123134-gm1` to `-gm3`). That is where rule-writing mid-run could have added a concern mechanism, and it did not.

**What to fix first** (from this run, not tuned to it): make the concern sources part of the world. The four groups need to be actors, or a process needs to deliver true local concerns to specific members on a schedule. Without them the members have nothing to coordinate about. The model step dropped them, even though the scenario text names them. A size limit of about 10 entities for a "task" world may be the cause. The plan listed that as an uncertainty, and this run is consistent with it but does not prove it.

## Current State

| Check | Status | Evidence |
| --- | --- | --- |
| W1 | met | Pipeline run `waltzman-20261008T123134`: traces `any-scenario-waltzman-{odd,bundle,mechanics,stocks,sensing}-20261008T123134`, plus repairs `-repair1/2/3-20261008T123134`. Repair 1 was kept; repairs 2 and 3 were reverted. The final checks are 14 blocking and 15 advisory, with 5 of the 7 rules fired (`spikes/any-scenario-2026-10/evidence/waltzman/model.json`, `spikes/any-scenario-2026-10/evidence/waltzman/pipeline.log`). This was the only pipeline run that made model calls. The first launch failed before any call, because its environment lacked `llm_client`. |
| W2 | met | Member run `run-20261008T125239` (trace `any-scenario-run-waltzman-20261008T123134-20261008T125239`): AI members on Concordia (`openrouter/openai/gpt-5.6-luna`), game master on. It ended `terminal` at tick 2 with 13 Engine events, 10 attempts and 3 game-master rulings, costing $0.004 (`spikes/any-scenario-2026-10/evidence/waltzman/run/summary.json`). This was the only member run. The first launch was refused by the scratch storage guard and made no calls. |
| W3 | met | `spikes/any-scenario-2026-10/evidence/waltzman/run/frame-round1-votes.png` shows round 1: each member's decision and its Engine events `e00001`–`e00005` and `e00007`. `spikes/any-scenario-2026-10/evidence/waltzman/run/frame-round2-gm.png` shows round 2: the game-master rulings and the activation. |
| W4 | met | The Assessment above: all four mechanisms are missing, each with its reason. |
| W5 | met | `scripts/check_project.py` was run on merge commit `29998ec` in the main world-substrate checkout, with `node` and `llm_client` available. It exited 0 with 554 tests OK and none skipped (`spikes/any-scenario-2026-10/evidence/waltzman/gate-merge-29998ec.log`). Without `node` and `llm_client`, two older tests skip (`test_world_builder_home`, `test_jev_estimator_probe`). The earlier `gate.log` (551 OK, 1 skipped) comes from that environment. Deviation: besides the plan, `spend.py` and the evidence, the merge added `tests/test_waltzman_scenario_run.py`, which pins the assessment's claims to the recorded files. |

Spend: $7.07 at the plan's start, $7.59 after both runs ($0.52 of the $2 cap; `spend.py`).
