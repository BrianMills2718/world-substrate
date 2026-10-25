# Cold review: open-attempt planning package

Reviewer: `company-planning:planning-compliance-reviewer` subagent, 2026-10-25. Two rounds.

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
