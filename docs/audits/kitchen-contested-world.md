---
role: audit
status: active
reviewed_through: 2026-09-07
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

## A complete service

Thirty turns, both cooks driven by the same model, $0.0179. Evidence:
`evidence/kitchen/full-service-v0.json`, rendered at
`evidence/renders/kitchen-full-service.html`.

**Both orders filled.** Bo at turn 9, Ama at turn 17. 29 of 60 opportunities
taken, 9 stale retries, 1 plan genuinely taken by the other cook.

The fourteen-turn run had stopped one cook short of finishing; the shape only
appears when it runs long enough to complete.

- **t1** Each takes the ingredient only they need, leaving the two shared
  onions.
- **t2** Both want the knife. Bo gets it.
- **t3-t9** Ama holds its ingredients and waits, seven turns, reasoning each
  time that putting either down risks losing it. Bo runs the pipeline twice and
  fills its order.
- **t10** Bo puts the knife down, and names why: *"Put down the knife so Ama can
  use it to chop the remaining ingredients."* Not "I am finished" -- an act
  aimed at the other cook.
- **t11-t17** Ama takes the knife and works. Bo repeatedly declines to
  interfere: *"My order is already complete, so I should not take ingredients
  needed by the other cook."* Ama fills the stew at t17.
- **t18-t19** Ama, finished, puts the knife down *"so it is available for the
  other cook"*. The courtesy is reciprocated without either having seen the
  other's reasoning.

Two agents with no channel between them partitioned a scarce resource, took
turns on the bottleneck, handed it over on completion, stayed out of each
other's way, and both finished. Nothing in the prompt mentions cooperating,
sharing, or waiting; it states the situation and nothing else.

**The weakness this exposed at the time:** after t17 both orders were filled
and the runner had no world-defined reason to stop, so thirteen turns of
aimless taking and putting down followed. That observation is intentionally
retained in the v2 trace. The defect is now closed: the kitchen derives service
completion from the `filled` state its order entities already carry, and the
v3 contested runner treats its requested turn count as a ceiling.

## Replication after the terminal-state fix

On 2026-09-07 the complete service was repeated **three fresh times** under the
same world, model and prompt, using World Substrate runtime revision
`78c205c531033a3264a8be0b42a06fac90988c45`. The prompt was
`prompts/kitchen_policy.yaml` at SHA-256
`8f3ac0a29b1ee67935646dd59796e9849c5ca6331db8ad6e8464a441bcbe408c`.
Each run requested a 30-turn ceiling and ended when the world terminal predicate
became true.

| fresh run | Bo fills | Bo releases knife for Ama | Ama takes knife | Ama fills / terminal | actual contention | stale retries | cost |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | t9 | **t10** | t11 | **t17** | 1 | 4 | $0.009512 |
| 2 | t9 | **t10** | t11 | **t17** | 1 | 3 | $0.010153 |
| 3 | t9 | **t10** | t11 | **t17** | 1 | 2 | $0.009120 |

The central behavior reproduced **3 of 3**. Every run has the same causal
shape: Bo acquires the knife at t2, fills its order at t9, deliberately puts the
knife down at t10 *for Ama*, Ama takes it at t11, and both orders are filled at
t17. There were zero refusals after retry. The surface retry count varied, but
the resource handoff and completion sequence did not.

The three t10 reasons are independently worded and explicitly other-directed:

- run 1: *"My order is complete, so putting down the knife lets Ama use it to advance her stew."*
- run 2: *"Put down the knife so Ama can use it to prepare the remaining stew ingredients."*
- run 3: *"Put down the knife so Ama can use it to chop ingredients for the stew."*

Raw v3 traces and renders are retained as
`evidence/kitchen/full-service-replication-v1-run{1,2,3}.json` and
`evidence/renders/kitchen-full-service-replication-v1-run{1,2,3}.html`.
`evidence/kitchen/full-service-replication-v1-summary.json` records their
hashes and execution metadata. The three service runs cost **$0.028785**. A
one-turn compatibility probe cost $0.00079; the current observability ledger
records **$0.029571** for this session's `world-substrate-castaway-policy`
calls.

**Execution caveat.** World Substrate pins `llm_client` at
`d7a9395a1935010119f5d42a6baf55b9d707443b`, but that exact object was not
available in the authorized machine's local Git object stores. The current
local client had changed Luna's registry capability from the pinned revision's
`native_structured_output: true` to `false`, which caused the first attempted
call to refuse before model execution. For the replication only, an uncommitted
model-registry override restored that single pinned capability bit. A one-turn
probe then confirmed that current OpenRouter still accepts the same strict
native JSON-schema route. No repository was modified by the override. This
keeps the model/world/prompt/schema path comparable while making the client
source-revision difference explicit rather than pretending it does not exist.

Taken together with the original full-service run, four observed services show
the same handoff shape. The formal replication claim is narrower: **under this
fixed world, model and prompt, the t10 knife handoff is no longer an n=1
anecdote.** It is not evidence that arbitrary models, prompts or worlds will
cooperate, and it is not a claim about private cognition; it is repeated,
observable behavior through the shared world.

## Limits

- The earlier three-way diagnosis remains one run per configuration and n=1
  per cell; the later full-service replication adds three fresh runs only to
  the final fixed configuration.
- The replication holds the world, prompt, model and two-seat model identity
  fixed. It establishes repeatability under that configuration, not
  cross-model or prompt robustness.
- The kitchen prompt names the situation but no strategy. A prompt that told
  either cook to cooperate would make the t10 handover an instruction rather
  than an observation, and that was the point of not writing one.
- The deadlock that `put_down` fixes was found by running the world, not by
  designing it: with take and no release, whoever grabbed the knife and the
  ingredients first froze both cooks permanently. Its absence is now a test.
