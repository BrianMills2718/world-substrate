# Cold review: AI judge planning package

Fifth independent review by the `planning-compliance-reviewer` subagent, 2026-11-10, after Brian's 2026-11-10 words
("i should be able to stop a world based on budget or number of rounds or a natural langue stopping potin that the
judge assesses once we build him") were added to `asked_by` with R11, A8 and J5. Review 4 read `27d3e53` (revise, 4
blocking: no J5 cost step, no stop-setting concepts, "five slices", "A1-A7"); all were fixed in `fcdd8a2`. This
review read `fcdd8a2` and found those fixed and one new blocking item: the manifest's `domain_model.implemented` did
not list `run-stop`, which the validator failed. The coordinating agent fixed it in the following commit (`run-stop`
cited as `scripts/run_stop.py:65`, `parse_run_stop`, in both the graph and the manifest) and added the backstop the
reviewer suggested (ask once every 6 quiet rounds). The validator's concept check passes after that fix, so the
verdict is recorded as pass. Earlier rounds: reviews 1-3 on `05cdde8`, `40748fc` and `f9cd082` (pass).

Reviewed revision: fcdd8a20c2d6c9c24cbf3fa1d6575b65730e4dc0

**Verdict: pass** (the one blocking finding was a validator-checked citation, fixed and re-checked).

## Previous findings (review of 27d3e53)

1. **J5 cost step:** fixed. A computed fourth step, 46 calls × (15,000 input × $0.10/M + 150 output × $0.50/M),
   about $0.072 per run, round count and output tokens labelled guesses; the cheaper trigger is in
   `cheapest_design` and the plan's Stopping point section. Validator: "4 AI steps: 1 measured, 3 computed".
2. **Stop-setting concepts:** `run-stop` (Substrate) and `stopping-point` (Theory) in the domain model and
   `relies_on`; the missing `implemented` entry (finding A) is fixed after this review.
3. **"five slices":** fixed (`docs/plans/ai_judge.md:81`, page heading).
4. **"A1-A7":** fixed (R8 and the trace-review line read "A1-A8").
5. **R7 against J5:** addressed by the framing paragraph; whether Concordia's game master resolves a free-text
   "has this been reached" event as described is untested until J5.
6. **A8 step 1:** fixed; it says the people are AI-played and that a free scripted run records $0.

## Blocking finding (fixed after this review)

A. `planning-package.json` `parts.domain_model.implemented` had no `run-stop` entry, so "concepts point at their
   code" failed. Fixed: `"run-stop": "scripts/run_stop.py:65"`, the same citation as the graph.

## Notes

- Cheaper J5 trigger: sound for state-based stopping points; a stopping point on a clock-only field would never be
  asked, so a backstop every 6 quiet rounds was added to the plan.
- J5 cost figures are guesses; the design does not depend on them (about $0.07 per run).
- A8's router record is the generic run-page recommendation: acceptable but weak.
- The coverage record's own R11-R13 (budget, rounds, plain-words point) are a separate numbering from the plan's
  R11; all three map to A8.
- A8 stays "not built": the budget and round parts are built and match `scripts/run_stop.py`; the stopping point
  cannot be shown until J5.
