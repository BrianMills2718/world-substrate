---
role: audit
status: active
reviewed_through: 2026-09-04
authority_refs:
  - ../decisions/003-semantic-mechanical-boundary.md
  - ../contracts/mechanic-profile-v0.md
  - ./m3-overheat-authoring-experiment.md
  - ../../roadmap/README.md
---

# M4: an honestly-authored mechanic, and where the assays go quiet

[M3](m3-overheat-authoring-experiment.md) authored a mechanic with a planted
omission and asked whether the assays caught it. That result is capped by an
obvious problem: the same author planted the omission and wrote the assays.

M4 is the complement. `process.material.vessel-failure-spill` is authored
without a planted omission — a failed vessel cannot retain its contents — and
the question is what the assays say about an honestly-authored mechanic: what
they add, and where they go silent.

Evidence: [`evidence/m4/spill-assay-v0.json`](../../evidence/m4/spill-assay-v0.json),
reproduced by `python scripts/run_spill_assay_probe.py --check`.

## The mechanic

A vessel at condition 0 that still holds liquid loses it: volume and heat go to
`physical_ledger.spilled_ml` and `physical_ledger.heat_lost`, and every liquid
field is zeroed. Order 26, immediately after overheat damage at 25, so failure
and spill resolve in the same tick.

Like the M3 mechanic it revives dead state. `physical_ledger.spilled_ml` and
`physical_ledger.overflow_ml` were declared in the ledger, present as zero in
every committed fixture, and **written by nothing**. `spilled_ml` gained its
first writer here; `overflow_ml` gained none, and the package said so. Both
were settled on 2026-09-04 -- `spilled_ml` became the full `spilled` vector,
and `overflow_ml` was removed rather than populated.

It installed with zero findings and froze as profile `7b49326b80e3258b`.

## It closes M3's residual

| | condition | liquid held |
| --- | --- | --- |
| overheat only (M3) | 0 | 459ml |
| with spill (M4) | 0 | 0ml |

And volume still balances: 5500 in-world + 459 spilled + 41 evaporated +
0 drunk = 6000, the world's starting volume.

## The three assays behaved completely differently

| Assay | Basis | Result on this mechanic |
| --- | --- | --- |
| `assay_declared_readers` | declarations | **5 findings** — drink, fill, pour, take, give |
| `assay_affordance_changes` | behaviour | **0 findings** |
| `assay_conservation` | goal-relative accounting | **0 findings** (correctly — see the control below) |

Two of these are worth recording carefully.

### The declaration assay saw take and give this time

In M3 it missed `take` and `give` because they read `condition` without
declaring it. Here it names them, because they *do* declare their
`entities.<vessel>.liquid` read. Same assay, same two mechanics, opposite
result — determined entirely by whether the declaration it consumes happens to
be complete. That is the ceiling on a declaration-based check, visible in a
single comparison.

### The behavioural assay went completely silent, and that was not designed in

The spill removes 459ml from the world. Nothing an actor may attempt changes,
so the assay reports nothing at all.

The reason: by the time the spill fires, the vessel is already at condition 0,
and every affordance on it is already blocked by `Vessel is intact` from the
overheat mechanic. Emptying an object nobody can touch changes no action set.

**A behavioural assay goes quiet exactly when a consequence lands on state
everyone has already been refused access to.** This is a genuine blind spot
that emerged from running the experiment rather than one built into it, and it
is the sharpest result in M4 — it means the M3 pairing was not a general
solution. Two mechanics arriving in sequence can hide the second one's
consequences behind the first one's refusals.

## Negative control: a green conservation check that can go red

A conservation assay that only ever passes proves nothing. The control is a
spill variant that empties the vessel and never records the loss:

- it stays inside its declared write scope — under-writing a declared path is
  not a violation, and the engine's scope guard correctly does not fire;
- every event commits with status `accepted`;
- `World.validate()` passes;
- both interaction assays report nothing; and
- **only `assay_conservation` catches it**: `in-world 5500 + spilled 0 +
  evaporated 41 + drunk 0 = 5541, but the world started with 6000`.

459ml left the world with no record, and every other check in the repository
stayed green.

## What M3 and M4 together establish

- Installation validates internal consistency and never completeness.
- No single assay basis is sufficient, and **no pair is either**. Declarations,
  behaviour, and accounting each caught something the other two missed, across
  two mechanics:
  - M3: behaviour caught `take`, declarations could not see it.
  - M4: declarations caught five readers, behaviour saw nothing at all.
  - M4 control: only accounting caught a destroyed quantity.
- Each basis has a stateable blind spot: declarations inherit their inputs'
  omissions; behaviour is blind behind an existing refusal; accounting only
  covers quantities the ledger models — at the time of this experiment spilled
  salt and pathogens left the world unaccounted, because `spilled_ml` was a
  bare integer while `evaporated` was a full liquid vector. That asymmetry was
  closed on 2026-09-04; the blind spot it illustrates is not.

The honest limit remains: two mechanics, one world, one author. What M4 adds
over M3 is that the second mechanic was not built to be caught, and the most
useful finding — the behavioural assay's silence — was not anticipated.

## Consequent findings for the roadmap

1. **Resolved 2026-09-04.** `physical_ledger` was asymmetric: `evaporated`
   tracked the full liquid vector, `spilled_ml` tracked volume only, and
   spilled salt and pathogens vanished unaccounted. `spilled` is now a
   `LiquidState`, and `assay_conservation` balances any quantity the caller
   states an initial total for rather than volume alone.
2. **Resolved 2026-09-04.** `physical_ledger.overflow_ml` was written by
   nothing and is removed rather than populated: a ledger field no mechanic
   maintains is a false accounting guarantee.
3. A mechanic that under-writes a path it declared is invisible to the scope
   guard by design. Conservation caught it here; that will not generalise to
   quantities the ledger does not model.
4. **Resolved 2026-09-04.** The under-declared M1 read scopes are repaired.
   The count cited here and in M3 was originally seven; four were false
   positives in the assay's own text matching, and the real figure is three
   (`take`, `give`, and `process.thermal.vessels`, all reading `condition`).
   See the follow-up in [the M3 audit](m3-overheat-authoring-experiment.md).
   M4's own finding stands: this audit's point was that the same assay's reach
   flips depending on declaration completeness, and the repair demonstrates
   that directly — the assay now reaches `take` and `give` for `condition` as
   well as for `liquid`.
