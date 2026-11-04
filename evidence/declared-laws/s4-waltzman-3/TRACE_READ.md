# Trace read: Waltzman rebuild with the concern-filling fix (s4w3)

Run: owner allowance, deployed `096c129`, pressed 2026-11-04T15:52:50Z by the page driver with the same pasted Waltzman
text as `s4-waltzman-2` (Brian's "yes" of 2026-11-04 to one rebuild). Share `jyVbywXT8N8F`, saved afterwards from the
server's own log with no AI call, so it has no readout. 12 server rows, $0.2269 (quoted about $0.15). 216 model calls, ids
23034-23249, 0 with an error: 110 world-builder-concordia-resident, 97 world-builder-attempt-interpreter, 2 world-substrate-scenario-spec, 2 world-substrate-action-signatures, 2 world-substrate-mechanic-authoring, 1 world-builder-world-kind, 1 world-builder-people-laws, 1 world-substrate-rules-review.

Trace ids: `world-builder-live/people/cf10fac9fa53400eaffadddaa6bb0de4`, `world-builder-live/kind/83994cdb4fc548b2a38310f8273615e9`, `world-builder-live/run/da13615c588b4a62a1952b4a447edcf3`, `world-builder-live/run/6c08b69b11b248e396d740b31e44c1a4`, `world-builder-live/run/d28c6feb86844ca8a335cce274806339`, `world-builder-live/run/9fadb81141d84a9ab8f10e6fc4acaa1e`, `world-builder-live/run/eb700b75dcb2434087d5eda9ee412bf1`, `world-builder-live/run/5cb9f600ad8c459994b57bc4f4d16d63`, `world-builder-live/run/01899ee527524e64bccaf7935a905794`, `world-builder-live/run/0879b7156aa343aba4d66930a83f9c2c`, `world-builder-live/run/230cae437916470296151b5f3e2dd668`, `world-builder-live/run/1a748a442808424fb81bb3f52fcb7562`, `world-builder-live/run/14e3d5dc5d3b465db9b223feb3584931`. How far each was opened: every round row was read person by person, with
each person's stated reason, status and reading. The kind and build traces were read only by call counts per task.

## Findings

1. **The fix held on a live run.** All five attempts to restore support went through (r4-e00003, r5-e00001, r5-e00005,
   r6-e00003, r10-e00009), none unread or misread. In `s4-waltzman-2` Country B failed this six times. This shows the
   filling works on one live run; it does not show that every such move in every world will.
2. **The two builds are not like for like.** The rules are written afresh. Here the decision needs 5 of 5 and allows no
   postponement (`needed` 5, `max_postponements` 0); the earlier build needed 4 of 5 and allowed one. Comparing outcomes
   between them says nothing about the fix alone.
3. **The rejection comes from the world's own moves.** Support reached 4 of 5 at round 5. In round 6 Country One restored
   (r6-e00003) but Country Two reopened its own settled concern (r6-e00007), so support stayed 4. In round 8 the Technical
   Group raised a new concern (r8-e00017) that made Country One conditional (r8-e00021), and the deadline fell the same
   round with 3 of 5: rejected (r8-e00023). Country Four brought it back in round 9 (r9-e00001). Round 10 repeated the
   pattern: Country Two restored and the Community Group's new concern (r10-e00001) took Country Four out (r10-e00023).
4. **Reopening without new evidence is a question for the rules, unanswered here.** Country Two's stated reason for
   reopening is that it should not treat the concern as settled, not that anything new came up. Whether a world should
   allow that is not settled by this read.
5. **Many refusals are people trying a closed door.** `discuss-local-concern-at-meeting` was refused 12 times, mostly
   because the concern was no longer open. Why they kept trying was not traced. The Legal Group's attempts failed its
   holder checks. The four refused `bring-decision-back` tries in round 9 lost to Country Four acting first, which is
   correct.
6. **The driver died on a page freeze this project shipped.** #333 laid out the focused Network with ELK every round; the
   page stopped answering for over 20 s and the driver's call timed out after round 11, before its readout and share.
   Measured on this share: stalls past 20 s with #333, about 1 s after #338. Nothing was lost; the rounds were on the server.

## Round 1

`community-group` allowed communicate (r1-e00001); `country-four` allowed put-matter-on-agenda (r1-e00003); `country-one` allowed discuss-local-concern-at-meeting (r1-e00005); `country-three` allowed discuss-local-concern-at-meeting (r1-e00007); `country-two` allowed discuss-local-concern-at-meeting (r1-e00009); `legal-group` allowed communicate (r1-e00011); `logistics-group` allowed communicate (r1-e00013); `partnership` allowed put-matter-on-agenda (r1-e00015); `regional-health-network` allowed put-matter-on-agenda (r1-e00017); `technical-group` allowed communicate (r1-e00019).
By itself: moment-countdown (r1-e00020), moment-occurs (r1-e00021), concern-makes-support-conditional (r1-e00022).

## Round 2

`community-group` allowed discuss-local-concern-at-meeting (r2-e00001); `country-four` allowed discuss-local-concern-at-meeting (r2-e00003); `country-one` allowed resolve-own-concern (r2-e00005); `country-three` allowed resolve-own-concern (r2-e00007); `country-two` waited; `legal-group` allowed discuss-local-concern-at-meeting (r2-e00009); `logistics-group` refused discuss-local-concern-at-meeting (r2-e00011); `partnership` refused discuss-local-concern-at-meeting (r2-e00013); `regional-health-network` refused discuss-local-concern-at-meeting (r2-e00015); `technical-group` refused discuss-local-concern-at-meeting (r2-e00017).
By itself: moment-passes (r2-e00018), moment-countdown (r2-e00019), moment-occurs (r2-e00020), remedy-progresses (r2-e00021).
Under way: country-one resolve-own-concern from r2-e00005; country-three resolve-own-concern from r2-e00007.

## Round 3

`community-group` allowed put-matter-on-agenda (r3-e00001); `country-four` allowed resolve-own-concern (r3-e00003); `country-one` waited; `country-three` allowed put-matter-on-agenda (r3-e00005); `country-two` allowed resolve-own-concern (r3-e00007); `legal-group` refused resolve-own-concern (r3-e00009); `logistics-group` allowed prepare-implementation-plan (r3-e00011); `partnership` allowed settle-agenda-matter (r3-e00013); `regional-health-network` refused discuss-local-concern-at-meeting (r3-e00015); `technical-group` allowed object-to-remedy (r3-e00017).
By itself: moment-passes (r3-e00018), moment-countdown (r3-e00019), moment-occurs (r3-e00020), remedy-completes (r3-e00021), remedy-progresses (r3-e00022).
Under way: country-one resolve-own-concern from r2-e00005; country-three resolve-own-concern from r2-e00007; country-four resolve-own-concern from r3-e00003; country-two resolve-own-concern from r3-e00007.

## Round 4

`community-group` waited; `country-four` waited; `country-one` allowed resolve-own-concern (r4-e00001); `country-three` allowed restore-full-support (r4-e00003); `country-two` waited; `legal-group` allowed draft-cross-border-arrangement (r4-e00005); `logistics-group` allowed put-matter-on-agenda (r4-e00007); `partnership` refused discuss-local-concern-at-meeting (r4-e00009); `regional-health-network` refused discuss-local-concern-at-meeting (r4-e00011); `technical-group` refused discuss-local-concern-at-meeting (r4-e00013).
By itself: moment-passes (r4-e00014), moment-countdown (r4-e00015), moment-occurs (r4-e00016), remedy-completes (r4-e00017), remedy-progresses (r4-e00018), work-cycle-restarts (r4-e00019).
Under way: country-four resolve-own-concern from r3-e00003; country-two resolve-own-concern from r3-e00007; country-one resolve-own-concern from r4-e00001.

## Round 5

`community-group` waited; `country-four` allowed restore-full-support (r5-e00001); `country-one` waited; `country-three` allowed put-matter-on-agenda (r5-e00003); `country-two` allowed restore-full-support (r5-e00005); `legal-group` waited; `logistics-group` allowed settle-agenda-matter (r5-e00007); `partnership` allowed settle-agenda-matter (r5-e00009); `regional-health-network` allowed settle-agenda-matter (r5-e00011); `technical-group` allowed assess-early-warning-system (r5-e00013).
By itself: moment-passes (r5-e00014), moment-countdown (r5-e00015), moment-occurs (r5-e00016), remedy-completes (r5-e00017).
Under way: country-one resolve-own-concern from r4-e00001.

## Round 6

`community-group` waited; `country-four` allowed settle-agenda-matter (r6-e00001); `country-one` allowed restore-full-support (r6-e00003); `country-three` allowed settle-agenda-matter (r6-e00005); `country-two` allowed reopen-concern (r6-e00007); `legal-group` allowed draft-cross-border-arrangement (r6-e00009); `logistics-group` waited; `partnership` allowed put-matter-on-agenda (r6-e00011); `regional-health-network` allowed put-matter-on-agenda (r6-e00013); `technical-group` allowed put-matter-on-agenda (r6-e00015).
By itself: moment-passes (r6-e00016), moment-countdown (r6-e00017), moment-occurs (r6-e00018), concern-makes-support-conditional (r6-e00019).

## Round 7

`community-group` allowed put-matter-on-agenda (r7-e00001); `country-four` allowed discuss-local-concern-at-meeting (r7-e00003); `country-one` allowed settle-agenda-matter (r7-e00005); `country-three` allowed discuss-local-concern-at-meeting (r7-e00007); `country-two` allowed discuss-local-concern-at-meeting (r7-e00009); `legal-group` refused resolve-concern (r7-e00011); `logistics-group` allowed discuss-local-concern-at-meeting (r7-e00013); `partnership` refused discuss-local-concern-at-meeting (r7-e00015); `regional-health-network` allowed discuss-local-concern-at-meeting (r7-e00017); `technical-group` refused raise-new-concern (r7-e00019).
By itself: moment-passes (r7-e00020), moment-countdown (r7-e00021), moment-occurs (r7-e00022).

## Round 8

`community-group` allowed discuss-local-concern-at-meeting (r8-e00001); `country-four` allowed put-matter-on-agenda (r8-e00003); `country-one` allowed discuss-local-concern-at-meeting (r8-e00005); `country-three` waited; `country-two` allowed resolve-own-concern (r8-e00007); `legal-group` refused resolve-concern (r8-e00009); `logistics-group` allowed prepare-implementation-plan (r8-e00011); `partnership` refused discuss-local-concern-at-meeting (r8-e00013); `regional-health-network` refused settle-agenda-matter (r8-e00015); `technical-group` allowed raise-new-concern (r8-e00017).
By itself: moment-passes (r8-e00018), moment-countdown (r8-e00019), moment-occurs (r8-e00020), concern-makes-support-conditional (r8-e00021), remedy-progresses (r8-e00022), decision-rejected-at-deadline (r8-e00023), work-cycle-restarts (r8-e00024).
Under way: country-two resolve-own-concern from r8-e00007.

## Round 9

`community-group` waited; `country-four` allowed bring-decision-back (r9-e00001); `country-one` refused bring-decision-back (r9-e00003); `country-three` refused bring-decision-back (r9-e00005); `country-two` refused bring-decision-back (r9-e00007); `legal-group` waited; `logistics-group` allowed discuss-local-concern-at-meeting (r9-e00009); `partnership` allowed discuss-local-concern-at-meeting (r9-e00011); `regional-health-network` refused bring-decision-back (r9-e00013); `technical-group` allowed discuss-local-concern-at-meeting (r9-e00015).
By itself: moment-passes (r9-e00016), moment-countdown (r9-e00017), moment-occurs (r9-e00018), remedy-completes (r9-e00019), decision-back-on-table (r9-e00020).
Under way: country-two resolve-own-concern from r8-e00007.

## Round 10

`community-group` allowed raise-new-concern (r10-e00001); `country-four` allowed settle-agenda-matter (r10-e00003); `country-one` allowed settle-agenda-matter (r10-e00005); `country-three` allowed put-matter-on-agenda (r10-e00007); `country-two` allowed restore-full-support (r10-e00009); `legal-group` allowed draft-cross-border-arrangement (r10-e00011); `logistics-group` allowed settle-agenda-matter (r10-e00013); `partnership` allowed put-matter-on-agenda (r10-e00015); `regional-health-network` allowed discuss-local-concern-at-meeting (r10-e00017); `technical-group` allowed assess-early-warning-system (r10-e00019).
By itself: moment-passes (r10-e00020), moment-countdown (r10-e00021), moment-occurs (r10-e00022), concern-makes-support-conditional (r10-e00023).

## Round 11

`community-group` allowed discuss-local-concern-at-meeting (r11-e00001); `country-four` allowed discuss-local-concern-at-meeting (r11-e00003); `country-one` allowed resolve-own-concern (r11-e00005); `country-three` refused discuss-local-concern-at-meeting (r11-e00007); `country-two` refused discuss-local-concern-at-meeting (r11-e00009); `legal-group` not understood raise-new-concern (r11-e00010); `logistics-group` allowed prepare-implementation-plan (r11-e00012); `partnership` allowed settle-agenda-matter (r11-e00014); `regional-health-network` allowed put-matter-on-agenda (r11-e00016); `technical-group` allowed put-matter-on-agenda (r11-e00018).
By itself: moment-passes (r11-e00019), moment-countdown (r11-e00020), moment-occurs (r11-e00021), remedy-progresses (r11-e00022).
Under way: country-one resolve-own-concern from r11-e00005.
