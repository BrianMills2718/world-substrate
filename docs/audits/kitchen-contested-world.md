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

## The churn was not the agents. They were choosing blind.

`policy.describe_action` listed Castaway's participant vocabulary -- vessel,
source, destination, target, volume_ml -- and rendered nothing else. Every
kitchen action names `item`, `burner` or `order` instead, so all five of a
cook's opening moves rendered as the bare word **"take"**: five distinct action
ids, one description. The policy could not tell the knife from a potato.

Everything written above about courteous churn was a description of agents
picking at random between identical labels.

This is the third place that hardcoded vocabulary was found. `assay._subject`
and `assay._component_names` were the first two, repaired earlier the same day
without sweeping for the rest. A test now asserts that distinct action ids get
distinct descriptions, in both worlds.

## Which change did what

Three runs, 14 turns each, same world and model, changing one thing at a time.

| run | orders filled | stale retries | accepted actions | cost |
| --- | --- | --- | --- | --- |
| indistinguishable actions, Castaway prompt | 0 of 2 | 14 | 28 / 28 | $0.0202 |
| **distinguishable actions**, Castaway prompt | **1 of 2** | 14 | 28 / 28 | $0.0116 |
| distinguishable actions, **kitchen prompt** | 1 of 2 | **4** | 17 / 28 | $0.0085 |

Cleanly separated, and they do different jobs. **Making the actions
distinguishable is what let an order be finished at all** -- the prompt did not
cause that. **The situational prompt is what stopped the thrashing** -- stale
retries fall from 14 to 4, and accepted actions fall from 28 of 28 to 17,
because the blocked cook now deliberately waits instead of taking and putting
down. Cost falls with each fix because less of the run is wasted.

The prompt tells each cook the situation -- another cook is here, it cannot be
talked to, ingredients are scarce and unreplaceable, and this is your order. It
does not say whether to cooperate or compete, so what follows is the agents'.

## What the good run looks like

- **t1** Both immediately take the ingredient only *they* need -- Ama the single
  carrot, Bo the single potato -- explicitly leaving the two shared onions
  alone. *"Take the unique carrot needed for my stew, leaving both onions
  available."*
- **t2** Both want the knife. Bo gets it.
- **t3-t9** Ama waits seven turns holding what it needs: *"Bo currently holds
  the only knife, so putting either ingredient down would risk losing it."*
  Bo runs the whole pipeline twice and **fills its order at t9**.
- **t10** Bo, finished, puts the knife down unprompted: *"My order is complete,
  so putting down the knife avoids blocking the other cook."*
- **t11-t14** Ama takes the knife immediately and starts working. The run ends
  before it can finish.

Nothing instructed any of that. Two agents that cannot communicate partitioned
the scarce ingredients on the first turn, one waited rather than thrashing
while blocked, and the winner handed over the bottleneck when it no longer
needed it.

Fourteen turns is not enough for the second cook to finish, which is the next
thing to change.

## Limits

- One run per configuration, one model driving both seats, 14 turns. The
  three-way comparison changes one thing at a time but is n=1 per cell.
- The kitchen prompt names the situation but no strategy. A prompt that told
  either cook to cooperate would make the t10 handover an instruction rather
  than an observation, and that was the point of not writing one.
- The deadlock that `put_down` fixes was found by running the world, not by
  designing it: with take and no release, whoever grabbed the knife and the
  ingredients first froze both cooks permanently. Its absence is now a test.
