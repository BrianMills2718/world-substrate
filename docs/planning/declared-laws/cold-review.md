---
description: Cold review of the declared-laws planning package, round 3 (pass).
---

# Cold review: declared-laws planning package, round 3

Reviewer: `company-planning:planning-compliance-reviewer` subagent, 2026-10-28, given the round-1 and round-2 reports.
Reviewed revision: 3e376db030b31925f7a3b9f8c6d8806e06e17b9a (HEAD of plan/declared-laws; subject_revision 9e63749, and only package files, review pages and checks.txt changed since)
Verdict: pass

Rounds 1 and 2 returned revise; their findings are all fixed (history in git for this file and `~/code/.scratch/declared-laws/NOTES.md`).

## Round-2 fixes

- **B1, refusal paths (fixed).** Piece 2, L2 and S2 (`docs/plans/declared_laws.md:157-176, 208, 256`) describe both refusal paths, and they match the code. On the move path, `Engine.apply` calls `_settle` and a refusal goes through `_reject` (`engine.py:762-781`). On the tick path, `Engine.advance` uses `_refuse_round` (`engine.py:864, 871-895`). `_settle` returns `None` today (`engine.py:896`); the plan changes that to a refusal record. A process scope breach still raises `ScopeViolation` (`engine.py:1005-1015`).
- **B2, incident attributions (fixed).** The incident table (`declared_laws.md:98-110`) agrees with the check functions in `scripts/world_builder_service.py`. Every line cite matches: `_unsourced_inputs` :840, `_conjuring_processes` :867, `_missing_components` :943, `_dead_end_stock` :960, `_starved_holders` :1023, `_vanishing_moves` :1114, `_unanswered_demand` :1130, `_second_source_processes` :1143, `_moving_processes` :1178. The saved worlds exist. Q43 and Q45 are consistent with the table. The observation checks are rightly left out.
- **B3, domain concepts (fixed).** `world-design` (implemented, `scripts/generate_world_bundle.py:53`) and `resource` (theory) are in the graph. The edges run correctly: e92 and e93 are "declares" from world-design, e96 runs world-law to gen-rules, and e103 runs rules-review to build. `relies_on` lists 18 concepts.
- **Earlier notes (fixed).** A2 demonstrates the knock-on case and names the model as the laws' author. A7 names its view, a composite-linked-view. Q48 names the decision it changes. The page links `acceptance-criteria.json`. Goal coverage counts 6 of 7 requirements covered, and the seventh is the planning-process requirement.

## Checks rerun

- Validator, `docs/planning/declared-laws/planning-package.json`: exit 1. 8 of 9 parts ok; substance 4 of 6 ok. The only failures are the cold-review verdict and `reviewed_revision`, both filled from this report.
- Validator, `docs/planning/planning-package.json` and `docs/planning/open-attempt/planning-package.json`: exit 1. The only failure in each is the old `reviewed_revision` f8dc6dad. For open-attempt, acceptance is WAIT until 2026-11-08, with 127 citations and 59 implemented concepts, all resolved.
- `md_file_cap.py --repo . --ref HEAD`: exit 0, 156 of 180 files, 0 orphans.
- `scripts/check_trace_reads.py`: exit 0, 20 runs, 0 problems.

## Findings

- **note:** set `reviewed_revision` to 3e376db0 and the verdict to pass in all three manifests (done when this report was saved).
- **note:** the domain map's `knock-on-now` cites `engine.py:884`, which now falls inside `_refuse_round`. `_settle` is at `:896`. The cite still resolves, but it should be re-pointed when S1 edits `engine.py`.
- **note:** the `_settle` refusal record and the new `_refuse_round` arguments are design, not code yet. The plan says so, and the graph marks `world-law` and `law-check` as theory.

Unsure about: the reviewer did not render the page; it read the HTML. It sampled the saved-world paths and did not open every pencil fixture.

Per package, once the fields are filled: declared-laws pass; repository pass; open-attempt pass.

Verdict: pass
