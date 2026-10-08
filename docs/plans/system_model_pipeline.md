---
plan_id: "system-model-pipeline"
dependencies: []
dependencies_reviewed: "2026-10-08"
planning_path: prototype
planning_path_ref: docs/plans/system_model_pipeline/path-decision.json
method_conformance_receipt: docs/plans/system_model_pipeline/conformance-receipt.json
goal:
  outcome: "The checked system model in docs/model/ covers what it left out: the describe-any-scenario pipeline (its steps, records, views and evidence), information items (src/world_substrate/information.py) and linked process participants, with a list of the kinds of things a world can represent and which path produces each, and a comparison with Cybernetic Influence v3's world schema."
  canonical_example: "tests/test_system_model.py fails naming attempt_log.jsonl when run_scenario.py's attempts.jsonl writer is renamed, and passes on the real code; ODD.md section 4.1 says a pipeline-generated world has entities with components plus actions and processes, and no person-with-profile or information-item kind."
  forbidden_substitutes: "claims in the model not established by reading the code or probing retained evidence; text search where the Python parser can do the check; changing spikes/any-scenario-2026-10/ code."
  boundaries: "world-substrate only; docs/model/, tests/test_system_model.py and this plan; no model spend by the work itself; merge through a pull request after scripts/check_project.py passes."
  done_when: "The drift test checks the pipeline records and writers, the Attempt fields, the evidence folders, the substrate component kinds and the process link kinds in both directions; it was shown to fail once on a renamed writer; VIEW_COVERAGE.md has the scenario replay and its state panel with numbered gaps; the project gate exits 0 with no skipped tests on the merge commit."
  do_not_gate_on: "fixing the gaps the model finds (G12-G16); Brian's review."
  stop_after: 3
---
# Plan: extend the system model to the any-scenario pipeline

## Goal

The system model ([ODD.md](../model/ODD.md), [world_substrate_model.toml](../model/world_substrate_model.toml), [VIEW_COVERAGE.md](../model/VIEW_COVERAGE.md), drift test `tests/test_system_model.py`, PR #118) describes only the public World Builder path. This plan extends it to the any-scenario pipeline (`spikes/any-scenario-2026-10/`, Decision 007), information items and linked process participants (PR #136).

**Execution profile:** `continuous-light`. One writer, reversible, documentation and one test file.

## Actor, result and example

- **Actor:** an agent or person investigating World Substrate who needs to know what the pipeline stores, which process writes each file, and what a generated world can and cannot represent (the comparison point with Cybernetic Influence v3's world schema).
- **Result:** the three model files and the drift test cover the pipeline, information items and linked participants.
- **Example:** ODD.md section 4.1 says a pipeline-generated world contains only entities with components plus actions and processes, with no person-with-profile and no information-item kind; renaming `attempts.jsonl` in `run_scenario.py` makes the drift test fail naming the new file.

## Authority and non-goals

- **Authority:** Brian approved the extension on 2026-10-08 (world-substrate is his repository). One agent writes, in its own worktree.
- **Non-goals:** changing pipeline code under `spikes/any-scenario-2026-10/`; fixing the gaps the model finds (G12-G16); changing other repositories; any model spend or deploy.

## Design (minimal vertical and reset boundary)

1. Model the pipeline's entities, processes and file records with writer file and function; add information items, deliveries and linked participants.
2. Add a kinds-by-path table and a donor-schema comparison, each cell established from code.
3. Extend the drift test with the Python parser: pipeline records both ways, Attempt fields, evidence folders, `register_component` kinds in `src/world_substrate/`, `PROCESS_LINKS`.
4. Add the scenario replay and its state panel to VIEW_COVERAGE.md, probed on the retained Waltzman run in a browser.

Minimal vertical: one pipeline record (`attempts.jsonl`) checked both ways by the drift test. Reset boundary: everything is in `docs/model/`, `tests/test_system_model.py` and this plan; reverting the pull request restores the PR #118 model. Non-goals for this vertical are those listed under Authority and non-goals: no pipeline code change, no gap fixes, no other repository, no spend or deploy. No coordinated-work ceremony is added: no work-unit graph, no claims beyond the worktree, no handoff document; one agent does it in one session.

## Success and disproof

Success is the acceptance checks below. The approach is disproved if the parser cannot resolve a pipeline write site (the extractor raises instead of guessing), or if a claim in the model is contradicted by the code or the retained evidence.

## Acceptance checks

Each is judged from the full output of the named run, not a status line.

| ID | Criterion | Run and what must be seen in its trace |
| --- | --- | --- |
| M1 | Drift test passes on the code and fails once on a renamed record writer | `python3 -m pytest tests/test_system_model.py` run twice in the implementing session; both runs' output is quoted in the pull request description, where the failing run's assertion must name `attempt_log.jsonl` and the passing run must show every test passing after the file is restored |
| M2 | Every new coverage cell that is `partial` or `missing` names a numbered gap with evidence | the browser probe of `spikes/any-scenario-2026-10/evidence/waltzman/run/frames.html`; its results (page-text matches and state panel contents) are written into each gap's Reproduced line in VIEW_COVERAGE.md, which must show the evidence behind G12-G16 |
| M3 | `scripts/check_project.py` exits 0 with no skipped tests on the merge commit | the gate run on a clean checkout of the merge commit; its full output is posted as a comment on the merged pull request, where it must show the test count, `OK` with no `skipped=`, and exit code 0 |

## Activation facts

All four declared false (`system_model_pipeline/activation-facts.json`): no shared mechanism is changed (documentation and one test file in this repository); no empirical comparison is proposed (the drift test and browser probe verify the built result); no LLM is central (the work reads code and retained evidence; no model call); no irreversible action or spend (reverts with git, no deploy).

## Uncertainties

- Whether the pipeline's records change under the adopted plan `scenario_actors_kept` while this lands. Resolved by the drift test: it fails on any changed record until the model is updated.
- Views not probed for information items and linked participants. Owner: the next change that adds a view of them; until then they have no coverage row (VIEW_COVERAGE.md says so).
