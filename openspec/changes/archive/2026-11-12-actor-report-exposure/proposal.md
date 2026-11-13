# Recorded actor-authored reports and initial exposure

Source: Brian's I0/I1 implementation goal, 2026-11-12; concrete failures retained in evidence/i0-i1/local-integration-2/TRACE_READ.md.

## Why

The real generated path could only deliver preallocated reports, misrepresented initial exposure, and allowed actor profiles to disclose withheld facts. These break the adopted independent-choice example.

## What Changes

Add one action-only append operation to the existing rules language. Independent worlds compile direct actor-authored report delivery into recipient-owned immutable records. Initial information can explicitly be already delivered, with actual source separate from holder and unspecified source preserved. Reuse the existing source-grounded build review to check the actual initial actor inputs and reject missing or unsafe privacy verdicts.

## Impact

Authoring schema/compiler, existing action effect language, actor projection and existing build review. No engine, scheduler or cognition framework. Historical pending information defaults remain unchanged.
