# Cold review, round 4: estimate-rules planning package

Reviewer: the `company-planning:planning-compliance-reviewer` subagent, run once on 2026-11-10 at commit 8fff8596d96fecabecfe86c69ff1e057966054eb (branch plan/estimate-rules-fix). Its report follows word for word; the reviewer wrote the full sha from the task's 8fff859 prefix and said so, and the real full sha is the one above.

The N1–N8 fixes hold up against the files, and nothing blocking remains. A few notes stay, mainly in the new cost basis and in Q89.

Reviewed revision: 8fff859e8cf9fe64ae2ba6cbd2a5a0a0a2e2c0d1 (the HEAD named in the task; I did not re-run `git rev-parse`, so the full sha is unconfirmed beyond the 8fff859 prefix)

I read the repository and the package at that revision and edited nothing.

## Validator

- I ran the validator from the repository root. It reported 7 of 12 substance checks ok, 0 failing and 5 pending.
- The pending substance items are the guess-basis Jev variants, the planned plain-version comparison and the 3 untested stages.
- Another 5 checks are pending only because they are required from 2026-11-12 or later (initiative, spectrum rungs, production rungs, thesaurus and system map).
- Cost basis: 8 AI steps (3 measured, 4 computed, 1 guess).
- Metamodel: 29 types, all mapped onto scientific-hypergraph@7b0638fe0aef.
- Stops: searched 4 ways, 0 found.
- Coverage: 2 requirements, both covered; A1, A2, A3, A4, A5 and A7 were edited after the stored judgment, so the nightly run judges them again.
- The only FAIL is freshness. It names docs/model/DOMAIN.md, docs/model/ODD.md, docs/model/domain.graph.json, `acceptance-criteria.json`, `estimate_rules.md` and the ai-judge spec. A new review record clears it.
- My shell wrapper (`| tail`) swallowed the validator's own exit status, so I did not capture it. The "Verdict: not compliant" line is consistent with exit 1.
- The cold_review part now reports ok because the manifest names the 3286054 report. It will show a stale `revise` verdict until this review is recorded.

## Previous findings

- **B1 (wrong domain anchors): fixed in substance.**
  - The five anchors were corrected in the domain model and `implemented` map (`build` → 1635, `test-run` → 1844).
  - At this HEAD those two lines are now an `attempts.append` call and a blank line, because the file shifted. That is line drift, which you excluded, so I do not count it.
- **N1 (resident, interpreter and readout cost): fixed, with caveats under N-new1.**
  - Four computed steps now cover residents, interpreter and readout.
  - From the airfield `llm-calls.jsonl`, the resident mean is 1,256 input and 124 output tokens (36 calls). The interpreter mean is 993 and 68 (12 calls). The readout is 1,523 and 309.
  - Waltzman: residents 2,761 and 223, interpreter 3,231 and 242. All have zero cached tokens.
  - The arithmetic reproduces: $0.045, $0.0107, $0.0003, about $0.057 with Jev, and about $0.13 for Waltzman-sized prompts.
  - The per-call costs recorded in the evidence ($0.000188, $0.000133, $0.000307; Waltzman $0.000388 and $0.000444) match.
  - The cap is $0.13 in the plan (`estimate_rules.md:~78-80, ~500`), the cost basis and the page.
- **N2 (`relies_on`): fixed.**
  - `test-run`, `run-loop`, `budget` and `scene-replay` are added (planning-package.json:227-230).
  - All four are in the domain graph as implemented Substrate nodes.
  - I found no further domain concept the plan changes or reads that is missing.
- **N3 (variant count): fixed.** The plan now says "10 cases x 4 variants". No "3 variants" remains in the plan, the page or the manifest.
- **N4 (Q88 wording): fixed.** The plan and Q88's ledger text (the Uncertainties section) say agreement shows only that the two are interchangeable, and E2 prefers bands where Q82 finds Jev flat. The wording is in the plan (about line 461 onward); the ledger text itself I did not re-open.
- **N5 (Decision 006 question): fixed as a record, argument partly weak.**
  - Q89 exists, is resolved, is marked inferred by agent, and cites Q27.
  - Its sources check out: Decision 006:25, Decision 009:26, `open_attempt.md:192`, and `estimate_rules.md:315` and `:530`.
  - The plan's "Needs Brian" paragraph now says he can reopen it.
  - See N-new2 for the weak point.
- **N6 (ford refusal wording): fixed.**
  - The refusal now reads "the cart could not get across the ford", and the plan states that each attempt draws its own number.
  - The same wording appears in A7, `body.html` and the page's walk-through.
  - No "too deep today" text remains outside the old review and the stored coverage trace.
- **N7 (A4 saved draft): fixed.**
  - The demonstration uses a saved draft "bakery oven, fallback removed".
  - The failure example says the fallback-removed draft passing the check is the broken case.
  - A reader could see that fail.
  - The entry is still `not built` with entrypoint `planned`, so there was nothing to open.
- **N8 (decisions list): fixed.** The page's "Your decisions" paragraph lists Q82–Q86, Q88, Q87 (settled) and Q89 (settled, can be reopened), and `index.html` matches `body.html`.
- **N9 (system model, spectrum, goal fields): unchanged.** The WAIT items stay until 2026-11-12.
- **N10 and N11 (acceptance, open questions): unchanged and still hold.**
- **Citations added this round: correct.** The new `consequence-report` anchor `scripts/consequence_report.py:67` is `pass_one`, the concept's entry point.

## Checks

- I reran the `llm_calls` aggregation and the saved `llm-calls.jsonl` files read-only. They match the manifest's token counts and per-call costs.
- The checks block was re-recorded at 590530c with 902 tests passed (902 passed, 2 skipped, 222 subtests passed).
- I did not rerun `check_project.py`, so I did not confirm the 902 figure or the doc reachability, trace-read or wiki-cap counts myself.

## Blocking findings

None.

## Notes

- **N-new1: cost basis for the E1 live run (planning-package.json cost steps, `estimate_rules.md` around lines 427-445).**
  - The Waltzman-sized variant mixes the Waltzman token sizes with the airfield call counts.
  - The Waltzman evidence has 110 resident and 97 interpreter calls, about 0.88 interpreter calls per resident call. The airfield ratio is 0.33, which gives the 80 interpreter calls assumed.
  - Applying the Waltzman ratio would put the interpreter near $0.09 and the whole run near $0.19, above the $0.13 cap.
  - The mixed worst case already totals about $0.1298, within 0.2% of the cap, so "reaches day 30 either way" is asserted rather than shown. The claim stands only because the cap was set to the same number.
  - The sawmill is closer to the airfield world, so $0.06 is plausible.
  - The plan also assumes one round equals one day and four resident calls per person per round.
  - I would label the $0.13 figure as an upper estimate and keep the cap with real headroom (for example $0.20).
- **N-new2: Q89 argument (3) rests on an unbuilt, unratified design.** The skill roll is "designed but not built" and Q33 is open. Decision 009 (the fixpoint) is the real precedent, and arguments (1), (2) and (4) carry the case. Q27's own wording said such calls are Brian's, so the "inferred by agent, can reopen" labelling matters. It is already there, so this is a note.
- **N-new3: the plain-version comparison is still `planned` and all 3 stages are `untested`.** This is unchanged and shows WAIT. The design does not depend on either. The cheapest-design paragraph argues declared bands against Jev. Q88 names the decision it would change, which is the case for running it rather than arguing it.
- **Open-questions map.** It excludes resolved Q87 and Q89, and its stated question now says so (planning-package.json diagram entry).
- **Line drift in existing citations.** At this HEAD, `build` at `world_builder_service.py:1635` and `test-run` at `:1844` have drifted. Excluded as agreed.
- **Page and render.**
  - I confirmed from the HTML source that the page draws every part inline. I did not render it in a browser.
  - Links are `blob/main` on the `BrianMills2718` repository, which is correct for a personal-account repository. They resolve after merge.
  - Re-running the page builder left the tree clean, so `index.html` is up to date.

Judgments I am unsure about: whether N-new1 should be blocking. I kept it a note because the sawmill run is small, the airfield figures are the closer match, and the page and plan label the $0.13 figure as a cap with its computation shown. N-new2 is also a judgment call.

Verdict: pass

## Earlier reviews of this package

## Earlier review: round 3, at 3286054 (verdict revise)

Reviewed revision: 32860542557cf2698a05669b4b29b5041a7e1818

Branch `plan/estimate-rules`, confirmed with `git rev-parse HEAD`; the base is origin/main d89a446. The previous round read 0c09c1d. I edited no file.

### Validator

I ran `validate_planning_package.py --repo . docs/planning/estimate-rules/planning-package.json` from the repository root and captured its own exit status: **1**.

- **Parts:** 8 of 10 ok, 1 failing, 1 pending. The failing part is cold_review, marked missing, which saving this report resolves. The pending part is investigation, required only of a new or full_method repository.
- **Substance:** 6 of 11 ok, 0 failing, 5 pending:
  - route: absent;
  - spectrum: absent;
  - cost basis: 5 AI steps, of which 3 measured, 1 computed and 1 guess (the Jev variants of the comparison);
  - plain baseline: planned, 10 cases;
  - stage effects: 3 stages, all untested.
- **Citations:** 245 file citations and 23 other sources resolve.
- **Domain model:** 64 concepts implemented, 15 dashed; the plan names 27 concepts it relies on.
- **Metamodel:** 29 types, all mapped onto scientific-hypergraph@7b0638fe0aef.
- **Stops:** searched 4 ways, 0 found.
- **Initiative and spectrum tiers:** 0 of 4 ok, 4 pending; these are required from 2026-11-12.
- **Coverage:** pending. Two requirements, both covered. Criteria A1, A2, A3 and A5 were edited after the stored judgment, so the nightly run judges them again.
- **Goal provenance:** ok.
- **Freshness:** ok. Reviewed at 4b5bda9, and no plan file has changed since.
- **Verdict line:** "not compliant (1 parts)".

Nothing fails apart from cold_review.

### Checks I reran (read-only, at HEAD)

| Check | Manifest | My run |
| --- | --- | --- |
| doc reachability | exit 0; 129 reachable, 0 unreachable | exit 0; 129 reachable, 0 unreachable |
| trace reads | exit 0; 38 runs, 0 problems | exit 0; `runs=38 problems=0` |
| wiki and Markdown cap | exit 1; 162 files, 28 unreachable (10 not linked, 18 deep), 16 durable findings | exit 1; same counts |
| durable documents | exit 1; 16 findings | exit 1; 16 findings (8 stale, 3 heading, 2 goal-field, 1 each of the other three kinds) |
| Jev cost | 14,222 calls, $0.3963, median 656 input and 78 output tokens | the same |
| rules-writer cost | 68 calls, median $0.0021, median 11,551 input and 1,574 output tokens, 0% cached | the same |
| Jev latency (`llm_calls`, split on `error_type`) | 18,671 ok at 0.43 s; 745 provider errors at 0.89 s; 585 network errors at 20.2 s | 18,671 at 0.432 s; 745 at 0.895 s; 585 at 20.236 s |

The expected-time arithmetic gives 0.607 s, which matches the stated 0.61 s.

All the checks reproduce.

### Previous round's findings

1. **Checks did not reproduce (blocking): fixed.** All checks were rerun at 4b5bda9, and they reproduce at HEAD (table above). Each inherited failure names Q77. Doc reachability is now 0 unreachable, because docs/catalog.md links the J0 trace reads.
2. **Wrong code locations in `implemented` (blocking): partly fixed. It stays blocking (new finding B1).** Engine, event, process, causal-trace, knock-on-now, write-scope, affordance, observation, fingerprint and run-loop now point at the right code. Five entries still point at the wrong code, two of them concepts the plan depends on. The claimed fix, "copied from the repository package, whose implemented map is the current one", carries the same wrong anchors from `tools/planning/domain_src.py`.
3. **Missing question about the free test run and Jev spend (blocking): fixed.** Q87 is resolved by argument. The code it cites holds:
   - the scripted test runs at `scripts/world_builder_service.py:1845` and `:2215`;
   - `_trace_cost` at `:297`, which calls `get_cost(trace_id=…)`;
   - `_reserve_daily_budget` and `_settle_daily_budget` at `:225` and `:238`;
   - the live run settles from its trace cost at `:2635-2637`.

   The plan text is at `docs/plans/estimate_rules.md:334-346` and `:354-356`.
4. **Declared bands not argued away (blocking): fixed.** The plan now argues them (`estimate_rules.md:430-446`), adds them as variant (d) of the comparison, and records Q88 with a named decision: whether E2's rules writer prefers bands. A weakness in Q88's test remains; see N4.
5. **Plain baseline only planned, 3 stages untested (note): unchanged.** It stays a note, for the reasons given last round.
6. **No domain node for replay (note): not fixed, with a reason.** The manifest note explains it as bookkeeping. The `share` node partly covers it ("replays with no AI calls"). Still a note.
7. **subject_revision and checks header stale (note): fixed.** Both now say 4b5bda9.
8. **Page shows cold review as missing (note): unchanged, as expected.** `proposals/estimate-rules/review-page/index.html:304`. Rebuild the page after saving this report.
9. **Jargon in acceptance entries (note): fixed.** A1 explains "model version" and "trace id". A2 explains replay and the damaged copy. A3 explains the fallback and "Jev unreachable". A5 explains the attempt's wording and a resident's reasoning.
10. **Reading of "propagate" (note): fixed.** `estimate_rules.md:507-510` now states the reading the plan takes and rules out the probabilistic-logic alternative.
11. **Stops (note): unchanged, holds.** I reran `git log -i --grep=jev` and `brian_positions.py "jev estimate probability rule stop"` (keyword-only in that environment). They return the same Jev records the manifest lists, and none is a stop.
12. **System model, spectrum and initiative (pending).** See N9.

### Findings

#### Blocking

**B1. domain_model, `docs/planning/estimate-rules/planning-package.json:111, :132, :133, :134, :167` (source: `tools/planning/domain_src.py:12, :33-35, :72`): five concepts still cite the wrong code. Carried over from finding 2.**

| Concept | Cited | What is there | Where the concept is |
| --- | --- | --- | --- |
| `build` (the plan relies on it) | `world_builder_service.py:1591` | the docstring of `_dialogue_call`, a generic budgeted model call | `_generate_world`, `:1635` |
| `test-run` (Q87's subject; E2 changes it) | `:1797` | budget-exception handling inside the rules-retry loop | the scripted run, `:1842-1846` (and `:2215` on the people path) |
| `world` | `model.py:382` | a line inside `Entity.from_dict` | `class World`, `:424` |
| `rules-retry` | `world_builder_service.py:266` | the `LATE_HEDGE_RESERVE` comment | `RULES_RETRY_MODEL`, `:110`, or `_retry_label`, `:1029` |
| `entity-component` | `model.py:223` | a blank line | `register_component`, `:188`, or `class Entity`, `:247` |

- **Why it matters:** a reader who follows "build" or "scripted test run" to check what the plan changes lands on unrelated code.
- **Fix:** correct the five tuples in `domain_src.py` and regenerate. That also fixes the domain graph's explain text and the repository package.

#### Notes

**N1. plan, `docs/plans/estimate_rules.md:78` and `:479`: the live E1 run's resident calls are missing from `cost_basis`.**

- The plan says the E1 live run costs "under $0.05 of owner allowance (computed below)". But the costing below covers only Jev, $0.00084 per run.
- The run also calls the Concordia residents, because A1 needs Mara's own move and reason. It also calls the attempt interpreter, and possibly the readout.
- These calls are an AI step the plan runs, and `parts.plan.cost_basis.steps` does not list them.
- From the repository's own saved runs, per person and per round: airfield s2 cost about $0.00019 per resident call and $0.00013 per interpreter call; Waltzman s4-3 cost about $0.00039 and $0.00044.
- With two people over 30 days that is about $0.02 to $0.05, which is at or near the $0.05 cap. If the cap is reached, the run stops before day 30 and A1 cannot be shown.
- Fix: add a computed step for the residents and the interpreter, and set the E1 cap from it.

**N2. plan, `planning-package.json:197` (`relies_on`): incomplete.** The plan changes or reasons with four concepts the list leaves out. All four are in the graph with the correct status.

- `test-run`: E2 adds a stand-in estimator to it (Q87).
- `run-loop`: E1 writes `scripts/run_authored_world.py` and the run seed; Q85 touches it.
- `budget`: Q87 concludes the daily ledger now includes Jev calls.
- The run page, either `scene-replay` or `readout`: A1 to A7 all add rows to it.

Add them.

**N3. plan, `docs/plans/estimate_rules.md:421`: stale count.** It says "10 cases x 3 variants (below)", but the comparison now has four variants, (a) to (d). The total in the same bullet, $0.0065, already counts all four.

**N4. open_questions, Q88 (`tools/planning/questions_src.py`; plan `:442-444`): agreement with Jev stands in for correctness.**

- Q88's test, bands within 0.1 of Jev on 8 of 10 cases, treats Jev as the reference. Nothing in the plan says Jev's chances are right: Q82 asks whether they even rise with the facts, and `do_not_gate_on` excludes calibration.
- If the bands disagree, the plan keeps Jev without knowing which answer is better.
- The test still names a decision and costs $0.0021, so it is not wasted. But Q88 should say that agreement shows the two are interchangeable, not that Jev is better, and what E2 does when Q82 finds Jev flat.

**N5. open_questions: a missing question about Decision 006, settled by agent argument where Q27 set the precedent that Brian decides.**

- Q27 held that whether new control flow in `engine.py` is the engine capability Decision 006 forbids "is not settled by agent argument". Brian's yes became Decision 009.
- This plan puts a seeded draw and an injected model call inside `Engine.apply`'s commit. It argues the draw is rule semantics, not "stochastic activation" (`estimate_rules.md:303-306`), and says "Needs Brian: none open" (`:498-501`).
- The argument is reasonable, and Brian asked for exactly this feature, so the outcome probably would not change. That is why this is a note.
- Fix: record a resolved question citing Q27 and why this case differs, or offer a one-line Decision 010 for his yes.

**N6. plan, Decided 4 and A7 (`estimate_rules.md:147-150`, `:193`): the draw key on a move.**

- The draw is keyed by event, so two attempts to cross the ford on the same day get separate draws. One cart can be refused with "the ford is too deep today" while another crosses.
- That is a valid per-attempt reading, but the refusal text describes the state of the day.
- Either key a constraint's draw by tick and the values it reads, or reword the refusal ("the cart could not get across").

**N7. acceptance, A4 `expected` (`acceptance-criteria.json`): part of it cannot fail visibly.**

- "the build record shows any draft without a fallback rejected" shows nothing when the rules writer happens to include a fallback. A build whose check is broken would look the same.
- Use a saved draft with the fallback removed, as A2 does with its damaged copy.

**N8. review_page, `proposals/estimate-rules/review-page/index.html:316` (from `body.html:175`): "Your decisions" is out of date.**

- It lists Q82 to Q86 but not Q87 or Q88. The manifest and the questions table on the same page include both.
- The page is also built by a per-plan builder (`tools/planning/build_estimate_rules_page.py`), not the shared `scripts/build_review_page.py` that the contract names. The repository's other plan pages are built the same way.
- I could not render the page because Playwright's browser is not installed. From the HTML source:
  - The container view is drawn inline as SVG, with the planned estimator in orange and dashed. It answers its stated question.
  - The domain and question maps are drawn by `maps.js`.
  - Every part has a section.
  - The `blob/main` links resolve only after merge. The page says so, and the repository is under `BrianMills2718`, so the personal plan site is the right home.

**N9. system_model, spectrum and goal fields: partly checked.**

- `executes_typed_rules` is true, with basis `engine.py:597`.
- I checked three mappings against the kernel at 7b0638f: `role` same as `sci:RoleType`, `action-kind` specializes `sci:RelationType`, `sense` composes `sci:declaresRole`. All three terms exist at that revision and are used in the kernel's schema in those senses.
- The estimate block, recorded estimate and recorded draw are planned types, deferred to E1 with a stated reason.
- The `spectrum`, `spectrum_rungs` and `initiative` fields are absent, and the validator shows them as WAIT until 2026-11-12. The arc42 goal-field gaps are inherited and tracked by Q77.

**N10. acceptance and coverage: holds.** I split Brian's words myself, in his nouns:

| His requirement | Covered by |
| --- | --- |
| not just the judge uses Jev | A1, A4, A7 |
| certain types of rules | A1, A6 |
| constraints | A7 |
| that propagate | A1 (knock-on steps citing the failure); A7 (no logs on a blocked day) |
| based on Jev | A1, A7 |

- The `outcome` line keeps every one of them, and the stored coverage record agrees.
- Every view is a table or prose in a composite view, not a graph. The router record `docs/planning/estimate-rules/router/run-page.recommendation.json` names `composite-linked-view`.
- All entries are `not built` with entrypoint `planned`, so there was no entrypoint to open.

**N11. open_questions, other.**

- Q63 is still open even though the plan answers it. That is acceptable because it closes when E1 lands.
- Q82, Q83 and Q85 each propose a measurement that names the decision its result changes. Nothing already in the repository settles any of them: the old probe's coarse answers do not show whether the chance is flat.
- The sources I opened say what the questions claim: `estimate_rules.md:123, :158, :312, :334, :343, :430, :465, :483, :495`; `ai_judge.md:264`; `005-native-waltzman-delivery.md:86`; `006-governed-rules-layer-scope.md:25`; `arc42.md:292`; `profile.py:22`; `maintenance-estimator-probe-v0.json:299`; `world_builder_service.py:225, :297, :1845, :2215`.

### Judgments I am unsure about

- **B1.** I kept it blocking because the re-review rule keeps a partly fixed blocking finding blocking, and the fix the author described carries the same errors. Taken on its own, a wrong anchor on a concept whose implemented status is correct is close to the line.
- **N1.** It could be blocking if the sawmill has three or more people, or Waltzman-sized prompts: the resident and interpreter cost would then exceed the $0.05 cap and A1's 30 days would not be reached. With a small world and two people it most likely fits.
- **N5.** Whether Brian would want to rule on the Decision 006 boundary again for an estimate inside the commit, given he asked for the feature.

Verdict: revise

Fix first: B1. Correct the five anchors in `tools/planning/domain_src.py`: `build` → `world_builder_service.py:1635`, `test-run` → `:1842`, `world` → `model.py:424`, `rules-retry` → `world_builder_service.py:110`, `entity-component` → `model.py:188` or `:247`. Then regenerate and re-run the validator. I recommend fixing N1 in the same pass. Everything else is a note.

### After this review (added by the plan's author, not the reviewer)

This report is the reviewer's own, saved as it came. Its verdict stands: **revise**. No fourth round was run:
on 2026-11-10 the coordinator asked for this round to be finished, only its blocking finding fixed, and the
plan shipped (Brian: an hour of review rounds is too long).

- **B1 (blocking): fixed after this review, not re-reviewed.** The five anchors in `tools/planning/domain_src.py`
  now point at the code the reviewer named (`build` -> `scripts/world_builder_service.py:1635`, `test-run` ->
  `:1844`, `world` -> `src/world_substrate/model.py:424`, `rules-retry` -> `scripts/world_builder_service.py:110`,
  `entity-component` -> `src/world_substrate/model.py:247`). The values are the same as the judge lane's pull
  request #363, so the two merge cleanly. The domain model and both packages were regenerated.
- **Still open (notes, not fixed):** N1 (the E1 live run's resident and interpreter calls are not in the cost
  basis; computed from the saved airfield run, they are about $0.00093 per person per day, so two people over 30
  days is about $0.056, above the plan's $0.05 cap), N2 (`relies_on` misses test-run, run-loop, budget and the
  run page), N3 ("3 variants" should read 4), N4 (Q88 treats agreement with Jev as correctness), N5 (no
  question records why an estimate inside the commit is within Decision 006, as Q27 did), N6 (a refusal on a
  move describes the day but the draw is per attempt), N7 (A4 cannot fail visibly without a saved draft that
  lacks a fallback), N8 (the page's "Your decisions" list omits Q87 and Q88).

---

### Normative reconciliation re-review — 2026-11-12

Scope: repository package and open-attempt, declared-laws, AI-judge and estimate-rules packages, reviewed together against their shared model and question ledger. This verdict concerns documentation reconciliation. It does **not** certify all implementation slices, predictive validity, complete runtime traceability or full AES conformance.

Previous findings:

- **Fixed — shared checks:** trace-read records now reproduce: `python3 scripts/check_trace_reads.py --root evidence` returned **47 runs, 0 problems, exit 0**.
- **Fixed — method scope:** all five manifests declare `full_method`; investigation, route and semantic-spectrum records distinguish current capabilities from planned contracts.
- **Fixed — open-attempt ownership:** its plan correctly identifies declared-laws as the repository package’s current plan.
- **Fixed — open-attempt acceptance:** A1–A9 now have explicit demonstrations, expected results and failure examples. The novice crash probability follows from the declared dice distribution: **75% versus 12.5%**, not a guaranteed outcome or an empirical aviation claim.
- **Fixed — AI-judge evidence:** historical baseline results and J2/J3 evidence are distinguished. The additional model reviewer is deferred from the minimum required design; existing advisory behavior is not presented as demonstrated semantic protection.
- **Fixed — Q96 design:** the offer contract specifies immutable terms, parties, acceptance, expiry, withdrawal, approval binding and atomic settlement/consumption. The domain model marks the offer as planned; A5 covers the associated failures. The implementation defect correctly remains open.
- **Fixed — stopping:** J5 requires assessment after every completed round; unchanged material fields do not establish that a natural-language condition remains false.
- **Fixed — review pages:** the rebuilt pages remove the identified obsolete reaction-cap, signature/consent, universal-sampling, Q63-status and whole-run-cost claims.

The conceptual guide is coherent with Brian’s direction: heterogeneous models selected by process; actor-owned interpretation and choice; constraints distinguished from norms; explicit uncertainty lifetimes; and resource tradeoffs subordinate to preserving the investigation’s required distinctions. The three conceptual closures, Q63/Q73/Q75, are justified. The **46 remaining open questions** include implementation defects, evidence obligations and explicitly deferred later-slice design work; they must not be reported as universally resolved.

Validator reruns used installed Company Planning `0.2.0+codex.20261112213000` with `--offline-coverage`:

| Package | Parts | Substance | Exit before recording this review |
|---|---|---|---|
| Repository | 10 OK | 10 OK, 2 pending | 1: stale review |
| Open-attempt | 10 OK | 10 OK, 2 pending | 1: stale review |
| Declared-laws | 10 OK | 10 OK, 2 pending | 1: stale review |
| AI-judge | 9 OK, 1 failure | 11 OK, 1 pending | 1: old `revise` and stale review |
| Estimate-rules | 10 OK | 9 OK, 1 failure, 3 pending | 1: old report verdict format and stale review |

All five have four passing initiative/tier checks and a pending system-map requirement dated November 17. Review metadata and the final validator receipts must be updated after recording this review; these pre-update results are not passing compliance receipts.

Remaining limits: baseline/stage-effect evidence and estimate workload guesses remain explicitly pending. Q96 implementation, later-slice design gates, storage failure behavior, aggregate budget verification, legacy documentation findings and broader AES trace coverage remain open. I inspected source files and rebuilt page content, but did not independently repeat the parent’s browser verification or exhaustively reverify every historical quotation and live acceptance demonstration. No additional blocking finding remains **within this documentation-reconciliation scope**.

Scoped dispositions: repository **pass**; open-attempt **pass**; declared-laws **pass**; AI-judge **pass**; estimate-rules **pass**.

Reviewed revision: 0d2a8752ee5625c7e55dd1e1bedb87ab77c7ef73

Verdict: pass

---

### Modeling-contract re-review — 2026-11-12

Scope: changes since `65ffed8` to the shared modeling contracts, question dispositions, acceptance criteria, review pages and AES mappings used by all five planning packages. This is a substantive review of those changes, not a fresh certification of every historical claim or runtime capability.

- **Q76 — resolved appropriately:** the selected contract separates credential knowledge, physical custody, current verifier validity and institutional permission. Disclosure belongs to the actor; verification belongs to the mechanism. Revocation does not erase memory, and detecting a norm violation does not supply an observer with knowledge or compel a human response. Symbolic credentials are explicitly an approximation.
- **Q83 — resolved appropriately:** dependency selection follows the modeled mechanism and interventions. The blade’s two varying inputs are justified only within explicit fixed assumptions and exclusions. Missing inputs, versioned context, cache identity and persistent/shared uncertainty have defined treatment. Model agreement is not presented as proof of sufficiency.
- **Q84 — finding fixed:** the original draft left exposure-time context ambiguous. The revised contract captures the projected content, geometry, light, observer position, source revision/time and model identity when the opportunity occurs. Retries preserve that snapshot; changed conditions require a separately authored opportunity; late results cannot overwrite a terminal disposition. Exposure-specific draw identity avoids accidentally sharing one draw across recipients. A5 and the review page reflect this correction.
- **Architecture challenge — coherent:** the influence, program and physical examples expose different representational requirements without proposing a speculative universal engine. Native expressibility, generated-language support, live integration and scientific adequacy remain distinct. Once-per-pair termination is correctly distinguished from numerical convergence.
- **AES mappings — appropriately bounded:** the inspected existing tests directly support their named information-delivery, write-scope and hook-authority scenarios. Scan roots include the actual owners. Annotation coverage is not presented as behavioral validation, and existing consent, visibility, durability and spending gaps remain explicit.

Verification: committed revision confirmed; working tree clean at inspection; `git diff --check` returned exit 0 before commit; ledger independently counted **96 questions: 43 open, 53 resolved**. Generated estimate and judge pages contain the revised contract dispositions and exposure-time qualification. No simulation or backend evaluation was performed for this review. The parent’s running full check and final package-validation receipts are separate verification obligations.

No remaining substantive finding or human scope decision was identified for these documentation contracts. J4, E1 and E5 remain unbuilt; the complete actor-input boundary still needs its owning design and implementation. These conceptual closures do not establish credential secrecy, perception accuracy, estimator calibration, scientific fidelity or complete AES conformance.

Scoped dispositions for the shared changes: repository **pass**; open-attempt **pass**; declared-laws **pass**; AI-judge **pass**; estimate-rules **pass**.

Reviewed revision: 05356af5ded4f719d5b4c3878bb7fc91ab6c5008

Verdict: pass
