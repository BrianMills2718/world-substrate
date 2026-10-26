# Cold review, repo-wide package (round 8)

Reviewer: cold reviewer (the `company-planning:planning-compliance-reviewer` subagent), a re-review given the round-7 report.
Reviewed revision: d3050585e01102c47d0516579e6d645ac5b8eecc (subject_revision). I read it at HEAD 7afbf0a, which adds only the planning rebuild.
Verdict: pass

## Validator and reruns

- **Validator.** 8 of 8 parts ok. 42 questions (16 open, 26 resolved), 62 concepts, 91 relations, 4 diagrams. 110 file citations and 11 other sources resolve. 58 concepts are implemented and 4 dashed. 39 concepts are relied on. 29 of 29 types map onto `scientific-hypergraph@7b0638fe0aef`. Freshness is ok from d305058. The script exited 0 and printed "not compliant (1 substance check)".
- **The one failing check** is "cold review read this revision". The manifest still recorded reviewed_revision b2216ee. That is expected until this report is recorded.
- **Check reruns.**
  - `check_trace_reads.py` reported 11 runs, 0 problems, exit 0, matching the manifest.
  - `tests/test_open_attempt.py` ran 11 tests, all passed (under the project's `uv` command).
  - I did not rerun the full 727-test check, as instructed. `checks.txt` says it ran at 8e406ab, and it states that on its exit line.

## Disclosure of the later commits

`git diff 8e406ab 7afbf0a -- src scripts tests` touches only `scripts/build_metamodel.py` (13 lines, the knock-on-now type text and status). The other changes in that range are the question sources, the generated graphs and pages, and the manifests. No code under `src/` or `tests/` changed after the 727-test run, so the count stands. The `checks.txt` note is adequate; it did not name `build_metamodel.py` (note 4, since fixed).

## Open questions

- **Q28 (resolved).** Supported. `evidence/open-attempt/q28/README.md` and `probe.out` agree with the code. The structural argument carries the answer: `build_engine` never sets the built-in slots, and neither library process has `timing` or `apply_to`.
- **Q42 (resolved).** The evidence reproduces, from `~/projects/data/llm_observability.db` read-only: `world-substrate-mechanic-authoring` has 133 calls ending stop and `world-substrate-rule-writer` 153, none ending `length`; 1 and 2 further calls have no finish reason, which the evidence text already allows for. The cap is at `scripts/generate_causal_model.py:30`, from commit 8057ff4 (2026-09-08).
- **Open questions.** 16 open: Q1, Q3, Q12, Q14, Q15, Q16, Q17, Q26, Q30, Q31, Q32, Q33, Q34, Q36, Q37, Q38. Q1, Q14, Q26 and Q30 re-read; none is answered elsewhere in the repository.
- **Stale Q28 text.** None remains: Q28 is gone from the open-questions graph and `maps.js`, and `docs/plans/open_attempt.md:416` records it as resolved.
- **Missed questions.** None material. The live risk this slice adds (the rules writer misusing `immediately`) is held as the owed A5 owner run.

## Domain model and system model

- **Concept.** `knock-on-now` is now implemented at `engine.py:884` (`_settle`): waves, once per pair, `REACTION_LIMIT` 32 at `:1084`, `_refuse_round` at `:859`, `reaction_wave` set at `:940`. The relations `process` to `knock-on-now` and `knock-on-now` to `causal-parent` are kept.
- **Consistency.** The domain graph, metamodel, manifest `implemented` map, `relies_on` and both pages agree.
- **System model.** `world_substrate_model.toml` covers `reaction_wave`, the transcript `reactions[]`, the `reaction_limit` status and the `advance` command; `ODD.md` 8.20 covers the mechanism; `tests/test_system_model.py:374 test_knock_on_effects` exists.

## Diagrams, plan and page

- **Diagrams.** The four diagrams answer their stated questions; the context and domain graphs show knock-on as a substrate item, and the question graph lost its Q28 and knock-on-now nodes consistently.
- **Plan.** S2 is marked "built, not done", and the A5 run on a generated world is stated as owed in R4 (`docs/plans/open_attempt.md:215`), the S2 row (`:269`) and `:204`.
- **Page.** `proposals/planning-package/review-page/data.js` has `built_from` d305058 and `tests_run` 727; Q28 and Q42 each appear once; all eight parts are listed; the cross-link to the open-attempt page is present. The page was not rendered by the reviewer this round (the implementing agent rendered and viewed it).

## Findings (all notes)

1. The manifest carried the b2216ee review; replaced with this round's revision and verdict.
2. `evidence/open-attempt/q28/probe.out` reports "due False", which alone could mean "already handled"; the README's structural reading is the load-bearing proof.
3. Q42 keeps the cap "for now" as a hold limit while Brian said on 2026-10-26 that token limits are the wrong approach; defensible for this change, since nothing in S2 depends on it. A Brian follow-up on the key size would close it.
4. `checks.txt` should name `scripts/build_metamodel.py` in its disclosure line (fixed).
5. The pre-existing repo-format result (exit 1, compliant 0 of 1, tracked by Q15) is recorded honestly. Unchanged.

Unsure about: whether `immediately` rules written by a live model behave as the fixtures do (A5 is not yet run).

Reviewed revision: d3050585e01102c47d0516579e6d645ac5b8eecc

Verdict: pass
