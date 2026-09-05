---
role: audit
status: active
reviewed_through: 2026-09-04
authority_refs:
  - ./m5-policy-consumer.md
  - ./m6-second-world.md
  - ../../roadmap/README.md
---

# A third world, built against a measurement

The two-agent Castaway run spent **six of ten turns with both agents correctly
waiting**, because that world has one pot, one cup and one fire: almost nothing
to contend over and long processes to wait through. That is a requirement, not
a complaint, so this world was built against it.

**The kitchen.** Two cooks with *different* orders — stew wants onion and
carrot, hash wants potato and onion. One knife. Two burners. Four ingredients
for two dishes needing two each, so **zero slack**: waste one and a dish is
lost. Every stage is a single action (chop, cook, plate), so nobody waits
several turns for a process.

Evidence: `evidence/kitchen/contested-kitchen-v1.json`, rendered at
`evidence/renders/kitchen-two-cooks.html`. Cost **$0.0202** for 14 turns with
both cooks driven by the same model.

## What the world achieved

| | Castaway | kitchen |
| --- | --- | --- |
| turns where both agents idled | 6 / 10 | **0 / 14** |
| accepted actions | 5 of 20 | **28 of 28** |
| plans genuinely taken by the other actor, same scripted policy, 12 turns | 0 | **6** |

The design goal was met on activity. The kitchen never idles, and under an
identical scripted policy it produces real contention where Castaway produces
none at all.

## Two defects this run found in the harness, not the world

**The loop was picking the winner.** In the first kitchen run Ama retried 0
turns out of 14 and Bo retried 14 out of 14; Ama filled her order and Bo plated
nothing. `for actor in actors` iterates in a fixed order, so Ama committed
first every single turn and Bo's decision was always stale. Commit order now
alternates by turn, and the burden splits exactly 7/7.

**The headline metric was measuring turn order.** `lost_what_it_wanted` read
14 of 14, which looks like ferocious contention and is an artifact: whoever
commits second is stale *by construction*. The number that means something is
whether the plan was still on offer after the other actor moved. Computed over
the same run:

- retried because stale: **14 of 14**
- plan actually taken by the other actor: **1 of 14**

Seven percent, not a hundred. Thirteen of the fourteen retries were plans still
perfectly available; the policy simply chose differently on a second look. The
runner now reports both numbers separately.

## What the world did not achieve

**Neither order was filled in fourteen turns.** Ama plated a carrot and still
wanted an onion; Bo plated nothing. Both models spent much of the run taking an
ingredient, putting it down, and taking another, each move individually
reasonable — *"put down the onion so it is available for the hash order"* — and
collectively going nowhere.

So the kitchen is a better arena and not yet a good demonstration. Under greedy
scripted policies it contends properly (6 of 12); under two reasoning agents
the contention mostly dissolves into courteous churn, because `put_down` lets
either of them defuse a conflict and they keep doing so. That is a real result
about these agents in this world, and it is the next thing to fix.

## Limits

- One run per configuration, one model driving both seats, 14 turns.
- Both cooks share a prompt written for Castaway survival, not for service.
  Neither is told the other exists, that the ingredients are scarce, or that
  the orders compete. A prompt naming any of that would likely change the
  churn, and none was tried.
- The deadlock that `put_down` fixes was found by running the world, not by
  designing it: with take and no release, whoever grabbed the knife and the
  ingredients first froze both cooks permanently. Its absence is now a test.
