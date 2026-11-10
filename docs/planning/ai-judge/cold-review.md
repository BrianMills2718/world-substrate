# Cold review: AI judge planning package (`docs/planning/ai-judge/planning-package.json`)

This is a re-review. The previous review read `fcdd8a2`. Since then the plan content has changed: J0 was built, A1 and A7 were marked built, citations moved, and 11 OpenSpec specs gained scenarios.

- **What I read:** the checkout `/home/brian/code2/worktrees/ws-judge-j0b`, branch `feat/judge-j0-live`. I modified nothing (`git status --short` is empty).
- **Live records I checked:** the five share records named in A1 and A7, fetched from `https://brianmills.dev/world-builder/api/share/<id>`. I also rendered all five run pages and the review page with headless Chromium.

## Validator

`validate_planning_package.py --repo . docs/planning/ai-judge/planning-package.json` exits **1**.

| Group | Result |
|---|---|
| Parts | 9 of 10 ok, 0 failing, 1 pending (investigation: not due for this repository) |
| Substance checks | 9 of 13 ok, 0 failing, 4 pending (route, project-layer spectrum, 3 stages untested, the previous report's verdict line) |
| Initiative and spectrum tiers | 0 of 4 ok, 4 pending (due 2026-11-12) |
| Coverage | pending: 13 requirements, 12 covered, 1 about the planning process; A1, A7 and A8 were edited, so they are re-judged tonight |
| Goal provenance | ok |
| Freshness | **fails**: 18 plan files changed since `fcdd8a2`. This is expected; this review is what clears it. |

## Checks rerun (all reproduce the manifest and `docs/planning/ai-judge/checks.txt`)

| Check | Result |
|---|---|
| Durable documents (arc42) | exit 1, 12 findings (tracked by Q77) |
| Project navigation | exit 0, 0 findings |
| Repository format | exit 0, compliant 1 of 1 |
| Trace reads | exit 0, 38 runs, 0 problems |
| Wiki and Markdown cap | exit 1: 160 Markdown files, 13 more than two links deep, 10 not linked, 12 durable findings (tracked by Q77) |
| Doc reachability | exit 0, 127 reachable, 0 unreachable |
| Project check | exit 0: 891 passed, 2 skipped, 222 subtests passed |

I reran the project check at HEAD. Between `6dc7d37` and HEAD only the two package files changed.

## Previous findings (review of fcdd8a2)

- **A. `run-stop` had no `implemented` entry: fixed.** The manifest now has `"run-stop": "scripts/run_stop.py:65"`, which is `parse_run_stop`, and the validator's concept check passes.
- **Note, J5 backstop: fixed.** The plan asks once every 6 quiet rounds (`docs/plans/ai_judge.md:283`).

## Blocking findings

**B1. Acceptance A7 (`docs/planning/ai-judge/acceptance-criteria.json`, A7): "built" will stop being true within days.**
- The page shows the old run's refusal only because the server adds it when the share is opened. It reads the refusal from its run log, and only from the newest 3 daily log files (`scripts/world_builder_service.py:579` `SHARE_LOOKBACK_DAYS = 3`, `:627-635`, `:1443`).
- I confirmed the stored record for `OWjUKGkZzOtr` lacks `refusals_marked`, so the refusal is not saved in it.
- After three more days of runs, the 2026-11-10 log drops out of that window. The link will then read "By itself: wind topples the first" with no refusal, which is exactly A7's failure example.
- **Fix:** write the refusal into the stored share once, at read time or by a backfill, or re-save this share as a new one. Then re-read the live page after the 3-day window has passed.

**B2. Review page (`proposals/ai-judge/review-page/body.html:3`, and the generated package section of `index.html`) does not match the manifest.**
- The status line says "Status (2026-11-09): complete draft... Nothing is built yet", but A1 and A7 are marked built.
- The checks table is from the 2026-11-09 run on `0dcbcd6`: 144 Markdown files, 0 not linked, 121 reachable, 862 tests. The manifest has 160, 10, 127 and 891.
- Only 2 of the 4 diagrams are drawn: the domain map and the question map. The context view (`docs/model/ODD.md` section 3) and the metamodel are neither drawn nor shown; the page only links to the repository-wide page.
- **Fix:** update the status line, rerun `tools/planning/build_ai_judge_page.py` against the current manifest, draw the context view and the metamodel on the page, then render it and look.

**B3. Acceptance A2 and the plan (`acceptance-criteria.json` A2 criterion; `docs/plans/ai_judge.md:104-106` against `:435-440`): the criterion promises what the design does not deliver.**
- A2 says the judge is handed "every knock-on effect and every blocker" of its proposed rule. Canonical example step 4 says "the copy's full knock-on chain".
- The design, and Q74 (resolved), give the judge only the net changes, the blockers, the chain length and where it stopped. A 5,000-step chain is about 500,000 tokens.
- No criterion shows the judge receiving the result of a long chain, which is Brian's "50 things ... 100 links deep" delivered "to the ai judge". A2's only chain case reaches step 40.
- **Fix:** reword A2 and step 4 to the net-change report. Add a saved case where the proposed rule sets off a long chain (for example the 50 × 100 world). Expected result: the judge read the net changes and every blocker, while the run page holds all the steps.

**B4. Acceptance A2, A4, A5 and A6 (`docs/plans/ai_judge.md:88-90`; the first step of each entry): Brian cannot follow the demonstration.**
- Each starts with "build the port world from its description (the plan's canonical example)".
- That description exists only in the plan, and it is cut off: "the dispatcher sends a truck...". A search of the repository found no full text.
- Each build writes the rules afresh, so a fresh AI build will not reliably produce the exact strings the expected results quote, such as "sign release: blocked, inspected is false" or a second trader's offer.
- **Fix:** write out the full port description in the demonstration, or make the port a saved run as A3 and A1 already are. Also name the world description for A8's "team world".

**B5. Plan and ledger are missing the repository's own earlier version of this feature (`docs/plans/ai_judge.md:238`, `:245`, `:402-417`).**
- The plan says "There is no AI judge" and "no rule is installed mid-run today", and its prior-art and reuse sections were searched only in the catalogues.
- But this repository already has a game master that writes general rules mid-run for attempts no rule covers. It checks them and installs them into the running engine, or records a one-off ruling. Sources: `spikes/any-scenario-2026-10/midrun.py`, Decision 007 (Brian, 2026-10-07: "The game master should be able to write new rules mid-run, not just make one-off rulings"), and ODD 8.19.
- Its runs recorded 27 such rules (`spikes/any-scenario-2026-10/evidence/waltzman/run/summary.json` has 3; `.../waltzman-spec/run2/run/summary.json` has 24), plus a measured cost of about $0.10 per attempt.
- The D2 question's own recommendation (`docs/planning/open-questions.json:405`) said: "reuse the spike's mid-run path ... rather than a new one".
- This bears on J2 and J3 (reuse or build new), on the cost basis, and on the plain baseline: 27 existing rulings could be read before any new calls.
- **Fix:** add a ledger question (reuse or replace the spike's mid-run path, and what its 27 rules show), cite Decision 007 as a source, and correct the "Current truth" lines.

**B6. Open questions: a material question is missing (`docs/plans/ai_judge.md:257` R7, `:358-362`, `:276-278`).**
- R7 makes the judge Concordia's `EventResolution` with "no judge prompt of our own". Its output must be a rule in the declaration language, followed by a confirm-or-revise pass. J5 also hands it the stopping-point question.
- In Concordia 2.4.0, `EventResolution` turns a suggested action into a free-text event statement through a chain of thinking steps (`event_resolution.py:45-75`, `:132-222`).
- Getting a typed rule, a second pass over a test-run report, or a reached/not-reached answer out of it needs thinking steps we write ourselves. That is arguably exactly the "judge prompt of our own" R7 forbids.
- No ledger question asks whether this works or what counts as conditioning rather than our own prompt.
- **Fix:** add the question, settled by reading Concordia's code: what `event_resolution_steps` and components may supply, and whether that meets R7. Record the answer before J2.

## Notes (not blocking)

- **N1. Plan citations have drifted since J0 moved code:**
  - `engine.py:380-440` (`ai_judge.md:94`, `:124`, and A2's evidence): `discover` is now at `:395`.
  - `run_authored_world.py:601-634` (`:126`) is now about `:709-742`.
  - `:576-580` (`:240`) is now about `:656`.
  - `action_authoring.py:893-927` (`:151`) is now about `:925-960`. Q79's source `action_authoring.py:893` is a blank line.
  - `world_builder_service.py:1603` for "Simulate as" (`:174`) is now a `raise`.
  - `:1797` (`:496`) is now `:1844`.
  - `run_authored_world.py:38` (`:424`) is now `:39`.
- **N2. Ledger sources point at the wrong plan lines:**
  - Q74 cites `ai_judge.md:490, 309, 406`; the content is at `:430-442` and `:519`.
  - Q76 cites `:497`; should be `:526`.
  - Q81 cites `:323`; should be `:352-357`.
- **N3. Q75 and Q76 status disagrees across files.** The ledger has both open, but the plan's U2 (`ai_judge.md:523-525`) and the page's "Your decisions" call them settled. Q75 is rightly open. Its sources should cite the sawmill case, where the model named the logger's choice yet its rule moved the logs anyway. One option to weigh: a free routing test from what the proposed rule writes to (does it change another person's holdings?).
- **N4. `relies_on` is incomplete.** It lacks `affordance` (`engine.discover`, which pass 1 reads) and `share` (J0 changed how shares replay, and A1 and A7 are judged on share links).
- **N5. The cost basis assumes no revision.** It counts 2 judge calls and 1 rules review per unmatched attempt. In the plain baseline all 3 first rules were flawed, so the revision path is the likely case. Worked out: 30 judge calls × $0.00215 = $0.065, plus 20 reviews × $0.049 = $0.98. The total is then about $1.13 per run with the J5 check, above the plan's $1.00 per owner run (`ai_judge.md:514`). J2's test of whether the review flags the sawmill price is the right gate. The figure and the cap should be restated with the revision path counted.
- **N6. Stage evidence (`stage_effects`):**
  - The declaration check is marked `shown` on `rules-check.json`, which is a schema validation. The contract never counts that as an effect. It is needed by construction anyway, because a rule that does not compile cannot be installed; say that instead.
  - The side-by-side compares the plain version with today's no-judge path, not with a built judge.
  - Only the rules review has a stated drop condition. Pass 2's test run, the one revision and pass 1 have none.
- **N7. Pass 1 rests on a requirement, not a shown gap.** It is kept without a gap the plain version showed (`ai_judge.md:505-508`). Its real basis is Brian's "along with blockers"; say so.
- **N8. A7 shows a rendering, not a replay (uncertain).** The demonstration renders a stored share. `Engine.replay_commands` under the recorded limit is exercised only by tests, so the failure example "the refused moment now goes through" cannot appear on the page.
- **N9. A1 wording.** A1's expected result for "loop" is abstract ("each rule fires once for each thing"). Plainer: "40 steps, d1 last, nothing after it". Separately, the plan's own A1 text (`ai_judge.md:293-294`) quotes "step 40 shows 'blocked: the truck has no fuel'". The acceptance file has the live wording (item 41) right.
- **N10. Unreproducible helper.** The A1 and A7 live runs were posted by an uncommitted scratch helper, `post_live.py` (`evidence/ai-judge/j0/live-shares.json:2`). The live server did run them: shares are assembled from its own run log. Commit the helper or describe how to reproduce.
- **N11. Stale baseline lines.** `ai_judge.md:81-82` and `:232-235` still describe the 32-step cap as current. They are dated to `0dcbcd6`; mark them "removed in J0".
- **N12. Page build and layout:**
  - The page is built by the per-plan `tools/planning/build_ai_judge_page.py` with a hand-written `body.html`, not by the shared builder's five-part template. There is no open-questions page and no page per diagram.
  - At 390px phone width it scrolls 7px sideways.
  - The served URL shows `main` at `d89a446` until this branch merges. The repository is public and owned by `BrianMills2718`, so the personal site is the right place to serve it.
- **N13. Parts not due yet.** The investigation part, the project-layer spectrum file, `initiative` and `spectrum_rungs` are absent (pending, not yet due for this repository). Without a spectrum file I could not test the project terms against the planning layer.
- **N14. Stops search.** `stops.searched` did not include `brian-positions`; the tool is not installed. My own `git log --all --grep` for overbuilt, start over, archive and "a patch" found no stop beyond D2. The D2 stop is correctly recorded as lifted by Brian's 2026-11-09 words, and no step resumes a stop that holds.
- **N15. Previous verdict line format.** The previous report wrote its verdict as bold text, not as the final line, so the validator shows it as pending. This report replaces it.

## What I confirmed holds

- **A1 works live.**
  - The "fifty chains" page reads "5,000 steps run, 5,000 with a cause, no refusal", and its list opens to 5,000 steps, each linked to its cause.
  - In "loop", d1 is knocked once at wave 40 and the moment ends.
  - In "truck without fuel", item 41 is orange: "blocked: truck leaves (truck) did not happen: 'the truck has fuel' was not true (it was 0)."
- **A7's two links show what the entry quotes today**, subject to B1.
- **Plain baseline.** I read both files of the sawmill and cafe cases (and the shop's rules-check result). The findings hold. The sawmill test run's one law breach was on `saw-slats`, not the new rule (`flags_buy_cedar_logs: false`), and the 3-log attempt moved 3 logs for 10 coins. `llm-cost` confirms the 3 calls cost $0.0061 and the rules-review token medians (9,407 in, 2,856 out, $0.699 over 24 calls). All computed figures recompute within rounding.
- **Domain model.** The 7 planned concepts are rightly dashed: no code matches them in `src/` or `scripts/`. I spot-checked 20 `implemented` citations; all land on the named code. `knock-on-now`, ODD 8.20 and the metamodel node match the J0 code (no cap, once per pair, blocked steps recorded, `recorded_reaction_limit`).
- **Metamodel mapping.** `sci:RelationType`, `sci:RelationInstance`/`RoleBinding` and `sci:RoleType`/`declaresRole` all exist in `scientific-hypergraph` at the pinned commit `7b0638f`.
- **Router record.** It chose `composite-linked-view`, which every entry names.

## Judgments I am unsure about

- **B6:** whether configured `EventResolution` thinking steps count as "a judge prompt of our own" is a reading of Decision 006 that Brian may see differently. The gap itself (no ledger question) is clear.
- **B5:** whether it is blocking or a note. I made it blocking because the ledger itself recommended reusing that path, and the plan says nothing like it exists.
- **N8:** whether "replay" in the goal boundary means opening a saved run (which the page does) or re-executing it with the engine (which only the tests do).

Reviewed revision: a863097f680904b03383a268041469d377086031

Blocking findings to fix first: B1 (A7 refusal expires), B2 (page stale and missing two diagrams), B3 (A2 promises the full chain; no long-chain case), B4 (port description cut off), B5 (repository's own mid-run rule writing omitted), B6 (no question on getting a typed rule out of Concordia's game master under R7).

Verdict: revise
