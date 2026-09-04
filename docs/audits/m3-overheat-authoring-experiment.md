---
role: audit
status: active
reviewed_through: 2026-09-04
authority_refs:
  - ../decisions/003-semantic-mechanical-boundary.md
  - ../contracts/mechanic-profile-v0.md
  - ../contracts/transition-envelope-v0.md
  - ../../roadmap/README.md
---

# M3: the first offline mechanics-authoring experiment

The central project hypothesis is that agent teams can add useful mechanics
faster than interaction risk grows. The easy half of that — does a
hand-reviewed mechanic behave? — was already established by M1 and M2. This
experiment tests the hard half: **when an author omits a real consequential
dependency, does anything notice?**

It was run adversarially on purpose. The authored mechanic is genuinely useful
and its package is a good-faith declaration; the omission is the kind a
competent author actually makes, not a strawman.

Evidence: [`evidence/m3/overheat-authoring-v0.json`](../../evidence/m3/overheat-authoring-v0.json),
reproduced by `python scripts/run_overheat_assay_probe.py --check`.

## The authored mechanic

`process.material.overheat-damage` — a vessel held above its material's heat
limit loses `overheat_damage_per_tick` condition per tick and fails at zero.

It is content-adjacent, not a new subsystem. Every component it touches already
existed in the promoted M1 substrate, and two of them were dead: before this
mechanic, `material.heat_limit_c` and `material.overheat_damage_per_tick` were
declared, range-validated in `World.validate()`, and read by nothing, while
`condition.value` was read as a gate by several mechanics and written by none.
No vessel in the world could ever be damaged. That is precisely the gap
`docs/architecture.md` names as an incomplete rule.

The world (`reference_worlds/castaway/overheat-v0.json`) adds one vessel — a
pitch-sealed gourd whose seal fails at 80°C, below boiling — so the mechanic
has a reachable trigger. This is content extension in the sense the
architecture already permits: no new component type was introduced.

## What the mechanic does

Robinson fills the gourd with 500ml and puts it on the fire. Over five ticks:

| tick | temperature | condition | liquid |
| --- | --- | --- | --- |
| 1 | 62°C | 100 | 500ml |
| 2 | 100°C | 60 | 499ml |
| 3 | 100°C | 20 | 479ml |
| 4 | 100°C | 0 | 459ml |
| 5 | 80.5°C | 0 | 459ml |

Without the mechanic installed the same run leaves condition at 100. The
mechanic works, stays inside its declared write scope, and emits a causal event
per damaging tick.

## Result 1 — installation alone caught nothing

The package installed against the eleven retrofitted M1 mechanics with **zero
findings**, and froze into profile `d525940e065d8361`. Identity, path syntax,
rule/package agreement, overlapping writes, dependency resolution,
representation, and declared tests all passed.

That is the experiment's premise, confirmed: a package that omits a real
consequential dependency passes every check an installer can make from the
declaration alone. Installation validates internal consistency. It cannot
validate completeness, because the missing part is missing from the thing being
checked.

## Result 2 — the assays caught it, from two different directions

Two assays run against the same omission and catch overlapping but different
sets, which is why both exist:

| Assay | Basis | Caught | Missed |
| --- | --- | --- | --- |
| `assay_declared_readers` | declarations only | drink, fill, pour, heat, unheat | take, give |
| `assay_affordance_changes` | behaviour, with/without | drink, fill, pour, heat, **take** | unheat, give |

`assay_declared_readers` is exact but inherits every omission already present
in the *installed* mechanics' declarations. It misses `take` and `give`
because those two read `condition` without declaring the read.

`assay_affordance_changes` needs no declaration to be correct — it runs the
world twice and compares which checks block which actions — so it catches
`take`. Its own blind spot is anything that never reaches an actor's action
set.

Together they name six of the seven action mechanics the omission actually
affects. `give` escapes both, for an incidental reason: heating a vessel
transfers it to `place:camp`, so `give` is not discoverable on a vessel that
is on the fire.

## Result 3 — a third assay explains the first one's blind spot

`assay_undeclared_component_reads` audits the declarations the first assay
depends on, and finds **seven** promoted M1 rules that read a component their
declaration omits:

- `mechanism.ownership.take` and `mechanism.ownership.give` — `condition`, `heat_source`
- `mechanism.liquid.drink` and `mechanism.liquid.pour` — `heat_source`
- `mechanism.thermal.heat` and `mechanism.thermal.unheat` — `thermal`
- `process.thermal.vessels` — `condition`

This is a real, pre-existing defect in the promoted M1 code, not an artefact of
the experiment. Write scopes are now enforced by the engine; **read scopes are
not**, and these seven declarations show what that permits. It also sets a
ceiling on the declaration-based assay: it can only be as complete as the
declarations it reads.

## Result 4 — one incoherence was caught by nothing

**The destroyed gourd still holds 459ml of water.**

No mechanic spills it. No affordance reveals it — a destroyed vessel simply
refuses every action, which reads as correct. `World.validate()` passes.
Conservation still balances, because nothing was lost. The world is quietly
incoherent and every check in the repository is green.

This is exactly the class Decision 003 predicts cannot be recovered from an
author's own declaration: the author never wrote down that destruction has
anything to do with contents, so there is nothing in the package to find, no
declared reader to cross-reference, and no affordance to diverge. It is the
`architecture.md` failure mode "a broken container remaining sealed",
reproduced from a real authoring attempt rather than described.

## What this establishes, and what it does not

Established:

- an adjacent mechanic can be authored offline as a reviewable package,
  validated, frozen into a profile, and run;
- installation validates internal consistency and **does not** surface omitted
  dependencies;
- interaction assays do surface them, and complementary assays are worth
  running because each has a different blind spot; and
- a residual class survives all of them, and it is demonstrable rather than
  hypothetical.

Not established: that this generalises. One mechanic, one omission, one world.
The assays were written knowing the omission, which is the strongest caveat on
this result — an assay author who did not know what to look for might have
built neither. The honest next test is a mechanic whose omission the assay
author did not choose.

## Consequent findings for the roadmap

1. Read scopes are declared and unenforced, and seven promoted rules already
   under-declare. Enforcing reads is harder than writes (a read leaves no trace
   in state), but the declarations should at least be repaired.
2. `mechanic-profile-v0.md` installer step 3 ("reject overlapping writes
   without declared ordering, arbitration, or composition") is underspecified.
   Taken literally it rejects the promoted M1 mechanics, because `fill` and
   `drink` both write `entities.<vessel>.liquid`. Two independent *actions*
   writing one path is ordinary — the transition envelope already serialises
   them. The rule applies to mechanics that can commit on the same occasion:
   processes sharing a tick, arbitrated only by `order`. The implementation
   narrows it accordingly; the contract should say so.
3. Vessel destruction needs a contents consequence. That is a second authored
   mechanic, and a natural M4 subject.
