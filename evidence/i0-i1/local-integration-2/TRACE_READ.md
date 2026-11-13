# Authentic local integration 2 — failed acceptance, retained evidence

Independent trace reader: Claude reviewer session d5af443f-5840-4c27-b0e6-927b1e3f4360. Read all 22 model calls, 6 actual actor input records, full protocol and canonical transitions. Root read this report and inspected the input/event artifacts. This is defect-discovery evidence, not a clean I0/I1 acceptance run.

Trace ids: world-builder-live/people/7bc4a910a73c4b63bf319187af0396a9 (build, calls 9686058–9686065, 9686069),
world-builder-live/run/00ee75df020147cea410e2f3f343c34f (round 1, 9686066–9686072),
world-builder-live/run/3e22fbdfd98c438a829e6c062a27fe89 (round 2 + judge, 9686073–9686079).
Cost (run-log cost_usd, measured): build $0.0717, round 1 $0.0014, round 2 $0.0044.

Build: two parallel scenario-spec copies (9686058 won; 9686059 lost). Both first attempts were rejected ("information item
mara_failure_report is sent to its own holder"); the retry moved the holder to Ari, so the report compiled as a pending delivery.
Action-signature copies 9686060 (used: request-evidence, investigate-claim, author-report) and 9686062 (unused: author-report with
free content, issue-warning). Laws 9686061 returned none. Rule writing 9686063 installed; copy 9686064 failed to compile
(unknown component 'location'); its fix 9686069 finished after the run had started, unused. Rules review 9686065: 2 findings
(no delivery to Bo; author-report creates nothing), not acted on.

## Round 1
- ari (9686066 → reader 9686070): repair-condition, accepted, r1-e00001; technical_condition.passing false→true.
  The validation-passes reaction was blocked (review "idle", not "completed"): repair alone does not clear the hold.
- bo (9686067 → 9686071): request-review, accepted, r1-e00003; review idle→requested. No condition, stance or assent change.
- mara (9686068 → 9686072): request-review, precondition_failed, r1-e00005 ("a review is not already requested");
  her memory says "not carried out", no reason given.
- process: moment-countdown r1-e00006.
Inputs: Ari's profile and memory contain V17/C/8; Mara's and Bo's contain none of these values. Both Mara and Bo see the
"Private validation measurement detail" entity. Bo's profile implies an undelivered failure report exists. Mara's profile
claims she received a report that is pending in the world and not visible to her.

## Round 2

Continuation:
The request (protocol line 57) has continue_from equal to the round-1 final snapshot, continue_seal 6a214f…
(equal to the round-1 snapshot_seal), and actor_state equal to the round-1 actor_state. Prompt diffs from round 1 to round 2,
per actor: turn number, the actor's own memory lines, and pump-activation.review "requested". No other actor's history and
no "recent" list appears.
- ari (9686075 → 9686078): complete-validation, accepted, r2-e00001; immediate validation-passes r2-e00002 changed
  validation failed→passed, hold true→false, review completed→idle. No change to assent, stance or active.
- bo (9686074 → 9686076): state-concerned, accepted, r2-e00004; only actor_position.stance changed (decided at
  revision 3, while the hold was still true; committed at revision 5).
- mara (9686073 → 9686077): "request evidence … from Ari", reader returned kind none (request-evidence missing from the kinds
  it was given), unsupported_action r2-e00005; game master 9686079 ruled no_rule. Relay lines went into Mara's and Ari's
  memory with no delivery record.
- process: moment-countdown r2-e00006.
End state: condition passing, validation passed, hold false, assents 0, Bo concerned, Mara unexpressed, report undelivered,
not activated. No ending is required by the scenario.

## Findings
(Defects 1–8 above.) Separations that held: condition hidden from every actor's view and changed only by r1-e00001;
review request and completion never repaired anything; the hold was cleared only by passing revalidation and nothing
else changed with it; stance changed independently of assent; no rule forced stance or assent.

### Exact defects observed


**1. High (I1): three installed moves can never be used.**
- **What:** `request-evidence`, `investigate-claim` and `author-report` are installed in `causal_model`, but they are not in `actor_information.public_actions`. That list is built only from the decision rules plus `communicate` (`compile_spec.py` ~806–826).
- **Why the reader misses them too:** the attempt reader only gets the kinds in that list (`run_authored_world.py:395-396`).
- **Evidence:**
  - All six reader calls (9686070–72 and 9686076–78) list exactly 10 kinds.
  - Both round files report `never_offered` for all three: "it was never put to anyone".
  - The build's own dry run reported `never_offered: {}`, so the dry run and the live run disagree.
  - Mara's and Bo's profiles say "Can request evidence". Mara tried it (9686073), and the reader (9686077) returned `kind: none`: "no action kind describes requesting evidence".
  - The game-master call 9686079 then stated as a fact: "The installed request-evidence move records Mara's request…".

**2. High (I1): Ari can't tell Bo anything or pass on the private detail.**
- **What:**
  - Only one delivery entity exists, Ari to Mara. There is no information item for the channel C / batch V17 detail.
  - `author-report` only sets a done flag to true.
- **The review caught it:** rules review 9686065 reported both problems. The build shipped anyway with `dry_run.ok: true`, so review findings don't stop a build.
- **Consequence:** "Ari may choose whether and whom to tell" can't happen. The "a different report to Bo" stage of the scenario contract can't happen either.

**3. High/Medium (I0/I1): Mara's initial exposure is forced into a contradiction.**
- **What happened:**
  - The source says Mara "receives a short report". In both parallel drafts, the first attempt recorded Mara as holder and recipient.
  - The check at `scenario_spec.py:168-169` ("sent to its own holder") rejected both.
  - The retry moved the holder to Ari. The report was then compiled as `delivery.status: pending` with `information.active: false`.
- **Result:**
  - Mara's profile says she received the report, but the world records it as undelivered.
  - Her knowledge has no delivery source; its only source is `scenario-profile:mara`.
  - Ari believes "Mara has not yet received my report" (9686066, 9686075).
  - If Ari delivers it, Mara gets a second copy of the same report.
- **Wrong sender:** the compiler set `information.source_id: "ari"`, but `apparent_source` is "Unspecified report source". The chosen draft's own assumption says the sender is unspecified. The compiler invented the attribution, and `source_id` is a field Mara would see once the report is delivered.

**4. Medium (I0): Mara and Bo see that a private record exists.**
- **What:** `private-validation-detail`, labelled "Private validation measurement detail", appears in Mara's and Bo's "What you can see". This is in calls 9686067, 9686068, 9686073 and 9686074, and in the entity lists given to the attempt reader (9686071/72/76/77).
- **Why it counts:** the contract counts existence and labels as visibility.
- **Fix status:** the uncommitted `actor_ids` change appears to target this. I didn't verify it.

**5. Medium (I0): profiles tell recipients what they were not told.** The contract forbids "telling a recipient a hidden exposure was suppressed".
- **Bo's profile** says "Has received no validation-failure report" and "Has not received the failure report at scenario start". Both imply that a failure report exists.
- **Mara's profile** says "it did not include the private channel or batch detail". That reveals the private detail is indexed by channel and batch.
- **Values:** none leaked. "V17", "channel C", "drift" and "8 units" occur 0 times in all of Mara's and Bo's inputs.
- **Cause:** the model wrote this wording from the source's narrator-style sentences, and no check exists.

**6. Medium (I0): nothing checks for hidden values in other people's profiles.**
- **What:** the losing parallel draft (9686059, call `cf9820e9`) gave Mara the memory "Has not been given the channel C or batch V17 detail." It also declared an item carrying the private detail, addressed to Mara and Bo.
- **It passed:** that draft passed the scenario-spec checks (`scenario_spec.py:144-198`).
- **Why it wasn't used:** the winning draft (9686058) simply finished first (34:47.99 vs 34:51.75; the first good answer is taken in `people_world.py:193-208`).
- **Consequence:** in this run, the protection was a timing accident.

**7. Low/Medium: an unrecorded speech channel.**
- **What:** Mara's unmatched request (event r2-e00005, reader `asks: ari`) put a line in each memory:
  - Mara's: "your request was delivered to Ari".
  - Ari's: "Mara asked: …".
- **What's missing:** there is no delivery entity and no delivery status for it.
- **Not checked:** what Ari does with it, because there was no round 3.

**8. Low: the "not modeled" list is wrong.** `build.json` coverage and `not_modeled` mark these as "no rule for this behavior":
- `file_validation_hold`
- `review_does_not_repair`
- `repair_and_revalidate`
- `activation_requires_separate_assents`
- `interpret_claims_and_assent`

In fact the compiled `decision.action.*` rules and `validation-fails`/`validation-passes` implement them. Anyone reading the build summary is misled.

**9. Low:**
- Each actor prompt contains the profile twice: it is rendered once as the brief and once as `initial_knowledge` (6 calls).
- Some profile text is in the third person ("A report she received…").
- The request said `world_kind: "task"`; it was silently replaced with `"ongoing"` (`people_world.py:366`, `world_builder_service.py:2403`).

**10. Information only (not a correctness defect):** call 9686069 (`d8c273b5`) was the losing rule-writing copy. It kept fixing its own compiler error until 01:35:44.6, after round 1 had started at 01:35:41. This is by design (`keep_until_settled`). It cost $0.0031 and its output was not used.



## Publication redaction

Credential fingerprint metadata was omitted from exported native records; model inputs, outputs, failure details and measured costs are unchanged. See redactions.json. Original native records remain in the private shared ledger.
