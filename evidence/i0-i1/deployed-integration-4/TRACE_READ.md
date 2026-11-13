# Deployed generated world — two rounds, scoped success with fidelity defects

Revision: `c74cdbf796713d44c7129f267ce56c8c376c9602`. Build trace: `world-builder-live/people/d6ac940f00a345898f38eac6a157eecb`; resident traces: `world-builder-live/run/690d1ff394064139abda0bb9617e79a5` and `world-builder-live/run/e9bc53c7e13e431b80f2b5ed23d01068`.

Read: all 18 complete native calls, exact prompts and responses, 17 successful structured attempts, lifecycle records, build, both rounds, continuation and server log. An independent reader checked every call and all six resident inputs; root separately read the source drafts, reviews and resident records. No tool calls or exposed native reasoning text beyond the resident structured reasoning. All 18 lifecycle records completed. Measured native cost sum: **$0.05932616**. Measured request duration: **84.144469838 seconds**. Twenty-three exact equality checks matched protocol, persisted build/run records, snapshots, seals, approvals, actor state and retained native policy I/O.

## Build

Calls 23428–23434: scenario 23428 selected, 23430 unused; action-signature drafts 23429/23431 empty; laws 23432 none. Reviews 23433/23434 approve the public context and all three actor contexts. Bo can see the public failed-validation hold without receiving a private report. Mara receives a short report with unspecified source; her context does not receive the private canonical lineage `validation_failure_v17`. Only Ari receives C/8/V17. No generated isolated request/ignore work flags are installed. Both reviews note Ari lacks a recorded stance. The second review notes there are no preallocated pending transmissions for communicate; the installed open send-report path remains independently usable.

## Round 1

All three residents decide against revision 0. Ari (`ari`, resident 23436, interpreter 23438) repairs: r1-e00001 changes technical_condition.passing from false to true, leaving validation failed and the hold intact; validation-pass propagation remains blocked until review is completed. Bo (`bo`, 23439/23440) expresses concern: stale r1-e00002 commits nothing; same-intent retry r1-e00003 changes only his own stance. Mara (`mara`, 23435/23437) requests review: stale r1-e00004 commits nothing; same-intent retry r1-e00005 changes review idle to requested. Neither required actor assents.

## Round 2

All three decisions see revision 3, before the validation commits. Ari (`ari`, 23443/23445) validates: r2-e00001 completes review, immediate r2-e00002 records validation passed, clears the hold and resets review to idle. It changes no actor stance or assent. Bo (`bo`, 23442) chooses literal wait, without an interpreter call or event. Mara (`mara`, 23441/23444) expresses concern: stale r2-e00003 commits nothing; r2-e00004 changes only her stance. Her statement that review did not change the condition is her inference at decision time, not injected canonical truth. Final authoritative condition is passing, validation passed, hold false; Mara and Bo remain concerned, both assents false, count zero, activation false. Sealed continuation preserves each actor's actual prior inputs and own memory.

## Findings

The exercised actor-input boundary and consequence distinctions pass: no private C/8/V17, canonical lineage or another actor's memory appears in Mara/Bo inputs; authorized repair and validation do not force consent or social agreement. No report delivery was chosen in these two rounds. A send-report status of never_offered describes absence of a bound menu template, not inability to submit an open attempt. Earlier resident-loop delivery tests establish that separate installed path; this run alone does not.

This is **not clean I1 acceptance**. The generated `prototype_pump.hidden_actual_validation_condition="failed"` duplicates the current technical truth and stays failed after repair, while authoritative technical_condition.passing is true. It is unused and actor-hidden in this run, so does not defeat the exercised privacy result, but contradicts the canonical state. The existing review missed that semantic alias. Also Ari lacks a recorded position because the original compiler created positions only for required assent actors. Fix the source-aware existing review/repair path and supply all actors a stance without expanding who has decision authority. Preserve this original evidence; do not relabel the stale field as historical after the fact. No social ending was prescribed and no rerun is justified merely to obtain agreement or a particular choice.

## Publication handling

The export replaces credential-fingerprint metadata, omits server client metadata and leaves model inputs/outputs unchanged. Originals remain in the private production native ledger. See redactions.json.
