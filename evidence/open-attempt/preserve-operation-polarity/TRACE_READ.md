# Polarity and public-reference correction: retained-input native replay

Executed candidate:`2d2f42b`; prompt1.5. Original six-round run remains unchanged at [T-e9dYLdIi61](https://brianmills.dev/world-builder/?run=T-e9dYLdIi61). These checks restore its saved world states and supply retained actor utterances; other actors wait. They are **recorded-policy native interpretation/judge and installed-rule checks**, not a fresh autonomous resident run or new world generation.

Native root:`world-substrate-polarity-3a0ca9c2`. Read all11 native responses and rule consequences; independent reviewer separately reads full prompts/schema/public bindings, responses, lifecycle and structured histories. Native provider cost measured **$0.006166675**,60645tokens,11calls,0tools;9cases pass,exit0. Exact duration and dependency revision are in result.json/protocol.json. No retry was made to obtain a preferred answer. Free checks preceded calls:74focused tests passed;29saved worlds,13whole,16previouslypartial,0errors,0lost.

## Cases and exact traces

Every trace below has prefix `world-substrate-polarity-3a0ca9c2/`. Each artifact retains its complete runner trace and exact Engine replay result. Restored snapshot rounds are origins, not one combined new timeline.

- **bo-negative-r1**,9687610/9687611: original23481 utterance now becomes kindnone, not record-assent. Existing judge says Bo already does not assent and returns no_rule. Canonical assent remainsfalse; no new rule or world change. Trace`world-substrate-polarity-3a0ca9c2/bo-negative-r1`.
- **ari-role-r1**,9687612: exact original23480 wording binds authoritytechnical-role-ari, not personari. Acceptedrepair changes only technicalconditionfalse→true. Trace`world-substrate-polarity-3a0ca9c2/ari-role-r1`.
- **bo-negative-r3**,9687613/9687614: original23493 wording, restoredafterround2, now becomesnone. Judge returnsno_rule, with assentfalse and requiredassents0 unchanged. Trace`world-substrate-polarity-3a0ca9c2/bo-negative-r3`.
- **bo-withdraw-r2**,9687615: retainedwithdrawal still bindswithdraw-assent and commits removal of existingassent. This control restores originalround1's recordedstate, including its wrong positiveassent; it does not retroactively repair the historicalrun. Trace`world-substrate-polarity-3a0ca9c2/bo-withdraw-r2`.
- **ari-assent-r6**,9687616: retainedpositiveassent still bindsrecord-assent and commits Ari's ownassent. His weightremains0. Trace`world-substrate-polarity-3a0ca9c2/ari-assent-r6`.
- **mara-concern-r4**,9687617: retainedexplicitconcern still bindsstate-concerned and changes only Mara'sstance. Trace`world-substrate-polarity-3a0ca9c2/mara-concern-r4`.
- **uncertain-positive**,9687618: explicitly newcontrol, “I am not sure the pump is safe, but I record my assent to activation.” Uncertainty does not negate the affirmed action; positiveassent commits. Trace`world-substrate-polarity-3a0ca9c2/uncertain-positive`.
- **quoted-negative**,9687619: explicitly newcontrol sends Mara the report “I do not assent.” It binds send-report, changes only her reportlog, and leaves Bo's assentfalse. Quoted negative content is not a separate assentoperation. Trace`world-substrate-polarity-3a0ca9c2/quoted-negative`.
- **foreign-authority**,9687620: explicitly newcontrol names Ari'sauthority while Bo attemptsrepair. The reader preserves that argument; the Engine refuses Bo'slackofownership with no changes. Public examples do not decide permission or silently substitute another authority. Trace`world-substrate-polarity-3a0ca9c2/foreign-authority`.

## Findings

The observed negation inversions and wrong authority binding are corrected on these retained utterances. The existing single-call interpreter now considers full operation meaning and scope of negation and receives the same visibility-filtered public example bindings already supplied to the actor. Hidden form descriptions, singletononly and derivedfrom fillers stay out; public examples do not overwrite explicit arguments. Independent free tests reproduced lost examples and description leakage before the fix and check hidden-state invariance afterward. Native foreign-authority preserves an explicitly named foreign object that also appears in public examples; it does not test an explicit referent absent from every example. The no-override code boundary has separate deterministic coverage.

All9 actual Engine replays match. No extra model stage, regex meaning rule, newauthoritystore or sequencer was added. Schema validity still cannot prove semantic truth, and these cases do not establish general accuracy or scientific validity. Original T-e9dYLdIi61 remains failed semantic evidence. Prompt generalization and further role/utterance cases remain underQ36; do not call the historicalrun repaired or claim a new autonomousrun was performed.

Independent browser result:58/58checks,exit0 acrossBo/Ari×1440/390. Originalwords,quotedbindings,separateconsequences,nineactualcontrolsandkeyboardevidencelinks are visible. Contrast15.43:1;0console/page/networkerrors,0writes. Initialunreadable/clipped table evidence is retained withthe repaired result. Existingphone scene overlap remains. See ui/receipt.txt andhash-bound screenshots.
