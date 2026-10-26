# Cold review: open-attempt planning package

Reviewer: `company-planning:planning-compliance-reviewer` subagent, 2026-10-25 and 2026-10-26. Rounds 1–2 reviewed the first draft; rounds 3–5 reviewed the package after the plan was revised and re-adopted (S1 built). Round 4 and later are re-reviews: each was given the previous report and marked each finding fixed, not fixed or fix wrong, and only blocking findings hold the verdict at revise.

## Round 1 (commit 5b6814d): revise, 8 findings

1. `subject_revision` was 6a8e37e, not the reviewed commit.
2. The plan said a roll changes `Engine._progress`, which only reports thresholds.
3. The glass chain said "each citing the one before", but spill and sound both follow break; the neighbour hearing is an observation.
4. Kind names were inconsistent (`walk`/`move`), and no generated world has places, ways or walls (`scripts/generate_causal_model.py`).
5. Q23 blocked A3 but S1 was marked fully specifiable.
6. The page showed the wall refusal as settled and had an unsourced observation text.
7. The page's plan link (blob/main) does not resolve before merge.
8. A8 was judged from a test count, not named replay tests.

All code citations (engine.py 321/352/452/582/749/786, rules.py:288, semantic.py:15, action_authoring.py:245, concordia_residents.py:81) and the "Current truth" table were confirmed true.

## Round 2 (commit 1bdf40b): pass

All eight resolved: subject revision set; roll writes the counter field a process reads; glass causes stated exactly with the neighbour judged separately; required kinds of the canonical airfield world named and Q23 made S1's first step (S1 conditional, A3 depends on Q23); wall example marked as depending on it; A8 names four existing replay tests. Finding 7 accepted as is: the page is served only from main after merge, when the link resolves.

Verdict: pass

## Round 3 (commit 048520c): revise, 11 findings

Q13 and Q27 cited the wrong lines; Q14 asked a question Decision 008 had already settled; the spike's mid-run AI game master was missing as prior art for Q22; the ledger was missing #241, #128, the silent `wait` reading, and roll authority; Q27 had been settled by the plan's author when it is Brian's call; Q28 cited the wrong registry; Q3's paid run named no decision; the metamodel used an unsourced phrase; the interpreter output in Piece 1 did not match the code; `relies_on` lacked approval and fingerprint; links to main 404 until merge; the domain map is tangled. Full report: `~/code/.scratch/ws-cold-review/round3-open-attempt.md`. All but the last were fixed in `fdaf2ed` and `c028b4b`. The tangled map is filed upstream as brianmills-spec/representation-router#149, because the shared graph viewer has no grouped layout.

## Round 4 (commit c028b4b): revise, 1 blocking finding and 4 notes

Ten earlier findings were marked fixed; O11 was accepted as filed upstream. Validator 8 of 8 parts ok, and every rerun check count matched the manifest: 718 tests exit 0, 11 trace reads, 0 problems.

1. Blocking: the page's "One choice for you" panel showed only D2 and gave a default ("slices 2 and 3 go ahead") that contradicts the plan, where S2 waits on Brian's Q27. Fixed: the panel now shows both choices with their defaults, and the slice table marks S2 as waiting on Q27.
2. Note: Q36's proposed check (list readings whose kind differs from nearest_kind) would catch nothing, because `attempt.py:122` sets nearest_kind to the matched kind. Fixed: the clause is dropped and the reason is given.
3. Note: Q39 cited `attempt.py:99`. Fixed: it now cites `:94` and `:129`.
4. Note: the metamodel's "Attempt reading" omitted the `wait` reading. Fixed in `scripts/build_metamodel.py`.
5. Note: this file recorded only rounds 1–2. Fixed: rounds 3–5 are added here.
