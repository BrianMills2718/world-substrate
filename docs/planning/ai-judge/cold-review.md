# Cold review: AI judge planning package

Third independent review by the `planning-compliance-reviewer` subagent, 2026-11-09. Earlier rounds:
review 1 on `05cdde8` (revise, 6 blocking findings) and review 2 on `40748fc` (revise, 3 blocking
findings), each fixed in the following commits. The two items this review left unchecked (the reason the
rules check rejected the waiter rule, and steps 4-6 of the canonical example) were checked by the
coordinating agent: `evidence/ai-judge/plain-baseline/rules-check.json:4` gives the `'from'` field-name
rejection, and `docs/plans/ai_judge.md` steps 4-6 move the coins only when Rosa signs.

Reviewed revision: f9cd08252d0b404b11d517ac687252b8ca63fcbf (content revision bcebb76eb981)

**Verdict: pass.** All 3 blocking findings and all 4 notes from review 2 are fixed in the sources. I found no new blocking issue.

**Review 2 findings**
1. **Waiter case: fixed.** The plan (`docs/plans/ai_judge.md:451,459`), `body.html:140` and the manifest verdict now say the ruling allowed the pickup, named the engine's own blocker, and was rejected only for the field name "from". That matches `evidence/ai-judge/plain-baseline/cafe-waiter-picks-up-tray.json`: the tray is on the counter, and the engine-blocked rows give "held by the waiter, actual counter". I did not re-check the "from" rejection against `rules-check.json`.
2. **Pass 2 stage effects: fixed.** The declaration check is "shown" for malformed rules only. The test-run stage, the revision and pass 1 are all "untested". The new script `evidence/ai-judge/plain-baseline/sawmill_test_run.py` is deterministic and makes no model call. Its output `sawmill-test-run.json` supports the claim:
   - The scripted run tried only quantity 1 across 11 buy moves and `flags_buy_cedar_logs` is false.
   - A 3-log attempt was accepted: 3 logs moved, 10 coins paid, and no failed checks.
   - The `saw-slats` law breach in the same file belongs to a different rule. It is not a flag on the sawmill rule.
3. **Pass 1: fixed.** The plan (`ai_judge.md:86-91`) now selects discover for the actor and each named person. It says explicitly that Vik's page cannot show Rosa's blocker. A2's expected result in `acceptance-criteria.json` puts "sign release: blocked" under Rosa's moves. The stage effect is "untested".

**Review 2 notes**
- **Cost:** fixed. The rules review is now `computed` at $0.49, with the earlier $0.29 figure shown as a comparison. The `cheapest_design` text states that Decided 3 does not require the model review and gives the cheaper option, with the reason it is kept.
- **Sawmill case:** fixed. It is recorded as a failure against Decided 4.
- **Canonical example, steps 3-6:** reworded in the plan. I read only steps 1-3 and did not re-verify steps 4-6.
- **Review page:** unchanged and still a note. It draws in JavaScript (0 `<svg>` in the HTML), and its file links point at `main`, so the new files open only after the merge. I did not render it.

**Cost totals are consistent.** I recomputed them:
- Interpreter: 0.009.
- Judge: 20 × (15,000 × $0.10/M + 1,300 × $0.50/M) = $0.043.
- Rules review: 10 × 12,263 tokens × $4/M = $0.4905.
- Total: $0.542, shown as $0.54 in `ai_judge.md:430`, `body.html:129-130` and the manifest.
- Without the model review: $0.052, shown as about $0.05.

The registry's single $4.00 figure for `gemini-4-argon` is a blended price and is labelled as such. `scripts/review_rules.py:1-8` confirms the review returns findings only, with no pass mark.

**Checks rerun**
- **Validator**
  - The validator printed 8 of 10 parts ok, 1 failing (`cold_review` missing, accepted) and 1 pending.
  - Substance checks: 8 of 11 ok, 0 failing, 3 pending. The pending ones are stage effects (1 shown, 3 untested), route and spectrum.
  - Coverage: 11 of 12 covered, with the 12th a planning-process item. Freshness is ok at bcebb76 with 0 commits since.
  - Cost basis: 3 AI steps (1 measured, 2 computed). Citations: 224 resolved.
  - I did not capture the validator's own exit status, because my `exit=0` came from `tail`. The `Verdict: not compliant (1 parts)` line is the accepted `cold_review` gap.
- **Evidence**
  - I read `sawmill-test-run.json` and the script, and recomputed the cost lines.
  - I did not re-run the script, because it would overwrite the evidence file.
  - `checks.txt` shows the durable-docs failure the brief says is identical on origin/main (Q77).

**Notes (not blocking)**
- `ai_judge.md:130-ish` repeats the $0.29 comparison in two places. The plain figure is also the only "measured" one for the 36-attempt airfield run. Both are labelled.
- The "tray on counter" wording in `ai_judge.md:459` ("the carry move needs the tray held by the waiter, and it is on the counter") merges the model's text with the engine's. That is acceptable.

I am least sure of two judgments: the steps 4-6 rewrite, which I did not read in full, and the "from" rejection cause, which I took from the finding text without opening `rules-check.json`.

Verdict: pass
