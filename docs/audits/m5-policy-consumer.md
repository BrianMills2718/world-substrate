---
role: audit
status: active
reviewed_through: 2026-09-04
authority_refs:
  - ../decisions/001-project-scope.md
  - ../../roadmap/README.md
---

# M5: a policy drives the world

Success criterion 2 requires that the same semantic action interface be
exercisable by scripted, human, or LLM policies *without giving policy prose
consequence authority*. Until this run, only the first had ever happened: every
trace in the repository was a scripted controller selecting from `discover()`.

Authorized with a $2 spend cap. Actual spend: **$0.005** across 16 model calls
(`openrouter/openai/gpt-5.6-luna`, `reasoning_effort=low`).

Evidence: [`evidence/m5/llm-policy-v0.json`](../../evidence/m5/llm-policy-v0.json).
Reproduce the seam without spending anything: `python -m pytest tests/test_policy_seam.py`.
Re-run the comparison: `python scripts/run_llm_policy.py --compare --turns 16`.

## The seam

A policy returns one thing: an `action_id` string. `resolve_choice` matches it
against the ids the engine itself produced for the current revision, and
anything unmatched is refused and recorded. Nothing anywhere parses policy text
into an action, so a model cannot describe an effect into existence. Accepted
choices go through `Engine.submit` — the untrusted-envelope path — rather than
a privileged one.

The model calls go through the approved shared `llm_client` with its required
`task`/`trace_id`/`max_budget` contract; no provider SDK is imported anywhere in
this repository.

## Result: same world, same rules, two policies

| | baseline (no foresight) | LLM |
| --- | --- | --- |
| final health | **4** | **60** |
| final hydration | 99 | 97 |
| accepted actions | 16 | 12 |
| answers refused | 0 | 0 |

The baseline drinks whatever is to hand. Sixteen turns of untreated water took
it from 100 health to 4. Nothing in its prompt punished it — `DrinkRule` did,
because untreated water carries pathogens and pathogens cost health.

The LLM boiled first, and did better. It is the first evidence in this project
that the action/observation seam is usable by something that was not written
against it.

## The interesting part: it was wrong, and the world won

The LLM did not escape clean. Its health went 100 → 60 in a single step at turn
14, and the trace says exactly why:

- **t10** — `fill 250ml`: *"Add a small amount of unsafe water to the pot already
  heating on the fire."*
- **t12** — `fill 255ml`: *"Fill the heated clay pot to its likely 1500 ml
  capacity."*
- **t14** — `drink 1000ml`: *"Drink 1000 ml of the **already treated** water."*

It re-contaminated its own pot and then drank it believing it was safe. Its
stated belief and the world's state had diverged, and the world did not care
what it believed. Had policy prose carried consequence authority, that water
would have been treated because the model said so. Instead the mechanic
computed 40 points of harm.

That is the entire architectural thesis, demonstrated by an actual model making
an actual mistake rather than argued in a document.

**Correction, 2026-09-04: the harm was not the re-contamination.** Replaying the
recorded actions deterministically shows the pot held **zero pathogens** at t14
-- the fills at t10 and t12 did re-contaminate it, and continued boiling cleaned
it again before the drink. The water was 80.5C against
`DrinkRule.safe_drinking_temperature_c = 45`, and the damage was
`hot_harm_per_250ml = 10` across four portions: exactly the 40 observed.
Pathogen harm would have been 12 a portion, or 48. The model was scalded, not
poisoned.

The thesis stands unchanged -- a stated belief did not move the world -- but the
belief that was wrong was about temperature, not treatment. This audit asserted
the wrong mechanism until a replay of already-committed evidence checked it.

**And the engine had already written the warning.** `DrinkRule` attaches
`Warning: Too hot to drink safely` to that affordance with `ok=True`, because
the action stays possible and simply causes rule-defined harm. It was on the
`discover()` page at t14. `policy.present()` rendered `describe_action` alone and
dropped every check, so the model was never shown a sentence the world had
already composed for it. Both runs lost health to that omission. It is rendered
now.

## Two real weaknesses this exposed

**The observation does not communicate progress.** Turns 3–9 are a
heat/unheat/heat/unheat oscillation. Boiling kills pathogens only after two
consecutive ticks at temperature, and nothing in the observation says how long a
vessel has been boiling or how far it has to go — `container.boiling_ticks`
exists in state and is not surfaced. The policy could see temperature and a
treated/untreated flag, but not the *process*, so it kept pulling the pot early.
An interface that cannot express "this is partway through" invites exactly this
churn.

**Nothing warns that filling a treated vessel untreats it.** The mixing rule is
correct and the policy had no way to anticipate it. This is not a request for
the world to be kinder; it is an observation that the affordance list presents
`fill` identically whether or not it destroys the value of the vessel's current
contents.

Both are seam findings, not mechanic findings, and neither is visible from a
scripted controller — which is the argument for having done this at all.

## Re-run after the seam was repaired (2026-09-04)

Both weaknesses above were fixed in the observation seam: a process that
accumulates toward a threshold now declares its progress, and an action that
destroys the value of a vessel's contents is marked in the affordance list. The
obvious question is whether the model still walks into the trap, so the same
comparison was re-run against the repaired seam. Same model, same world, same
16 turns. Cost: **$0.0045**. Evidence:
[`evidence/m5/llm-policy-postfix-v1.json`](../../evidence/m5/llm-policy-postfix-v1.json).

| | original | after the fixes |
| --- | --- | --- |
| final health | 60 | **80** |
| baseline final health | 4 | 4 |
| heat / unheat churn | 4 heats, 4 unheats | 2 heats, 1 unheat |
| refilled its own treated vessel | twice | **never** |

Both fixes did exactly what they were built to do. The oscillation is gone: at
t3-t6 the policy issues four consecutive `wait`s -- "let the clay pot continue
boiling" -- instead of pulling the pot off the fire and putting it back. It
never re-contaminated its own water.

**And it still lost 20 health, to the same underlying failure one step
downstream.** At t9 and t10 it reasoned that "the treated water is currently
too hot to drink safely, so waiting allows it to cool", waited twice, and drank
at t11. Reproduced deterministically: two ticks after pouring, the cup is at
**66C** against `DrinkRule.safe_drinking_temperature_c = 45`. The damage was
`hot_harm_per_250ml = 10` over two portions -- exactly the 20 observed -- and
the water carried zero pathogens. It was scalded, not poisoned.

That is the same shape as the boiling gap -- and, per the correction above, the
same *threshold* that took 40 points in the original run. Both failures were
temperature. The policy reasons about a limit
the world enforces and the observation does not expose, guesses how long to
wait, and is wrong. `ThermalProcess.progress` reports vessels *accumulating*
toward treatment -- it selects on `heat_source_id is not None` and
`pathogens > 0` -- and says nothing about a vessel *descending* toward a safe
drinking temperature. One instance of the class was closed and the next
instance appeared immediately.

The useful conclusion is not that the fixes failed. They worked, and the score
moved 60 to 80. It is that **this failure is structural rather than anecdotal**:
it regenerates at every threshold the world checks and the observation omits, so
it is a property of the seam design, not a memorable one-off. Anything built on
the assumption that a fixed seam stops producing it should expect otherwise.

## Three runs, one variable: what the policy was shown

Rendering the engine's own warnings turned the re-run into the third point of a
controlled series. Same world, same model, same 16 turns; the only thing that
changed between them is how much of what the world already knew reached the
policy.

| run | what the affordance list showed | final health | turns where belief contradicted state |
| --- | --- | --- | --- |
| [v0](../../evidence/m5/llm-policy-v0.json) | action names only | 60 | 5 |
| [v1](../../evidence/m5/llm-policy-postfix-v1.json) | + process progress, + value destroyed | 80 | 2 |
| [v2](../../evidence/m5/llm-policy-warned-v2.json) | + the rule's own warnings | **100** | 2 |

The no-foresight baseline is 4 in all three.

In v2 the policy drinks at 41C, 36C, 32C and 30C -- every one under the 45C
limit -- because it was finally told which offers were too hot. It takes no
damage at all. Nothing about the world, the mechanics or the model changed
across the three runs.

That is a stronger result than the original single trace. The interesting claim
is not "an agent made a mistake"; it is that **the entire difference between a
policy losing 96 health and losing none was how much of the world's own
knowledge the observation surfaced.** The mechanics were correct throughout and
never moved.

Cost: $0.0045 for v1, $0.0043 for v2.

Rendered side by side, belief against replayed world state, by
`scripts/render_belief_vs_truth.py`:
[v0](../../evidence/renders/belief-vs-truth-v0.html),
[v1](../../evidence/renders/belief-vs-truth-v1.html),
[v2](../../evidence/renders/belief-vs-truth-v2.html). No model is called to
build those; the engine is deterministic, so replaying the recorded actions
recovers exact state at every turn.

## Two agents in one world (2026-09-04)

The three-run series has an uncomfortable implication: shown everything the
world knew, the policy played perfectly. A demonstration built on an agent
getting things wrong would therefore have to withhold information deliberately,
which is manufacturing the phenomenon rather than finding it.

A second agent cannot be handled that way. An affordance page is computed at a
revision; each row was true when rendered and may be false by the time the
actor commits, because the other one moved. At render time there is nothing to
warn about yet.

The substrate has carried `base_revision`, `stale_revision` refusal and atomic
commit since M1 and no two live policies had ever exercised any of it. Both
Castaway actors were seated with the same model, deciding independently from
their own pages, with no channel between them but the world. Ten turns,
**$0.00598**. Evidence:
[`evidence/m5/contested-llm-v0.json`](../../evidence/m5/contested-llm-v0.json),
rendered at
[`evidence/renders/two-agents-one-world.html`](../../evidence/renders/two-agents-one-world.html).

**Turn 1.** Both independently decide to fill the pot. Robinson commits first.
Friday's plan — *"Fill the clay pot with a substantial amount of unsafe water so
it can be heated"* — is now impossible, so it looks again and **heats the pot
Robinson just filled**: *"Heat the untreated water to kill pathogens."* Being
beaten to an action produced the complementary next one. Nothing coordinated
that.

**Turn 6.** Both decide to unheat the finished pot. Robinson wins again.
Friday's intent was correct and simply gone; it re-decides to wait for the water
to cool. **Turn 8**, having lost twice, Friday *takes* the pot.

Both end at 100 health. Two agents with no way to talk divided the work through
commit ordering alone.

| | |
| --- | --- |
| turns | 10 |
| accepted actions | 5 of 20 opportunities |
| plans invalidated by the other actor | 2 |
| refused after retry | 1 (nothing left to do) |
| turns where both waited | 6 |

**The honest limit is that last row.** Six of ten turns are both agents
correctly waiting for water to boil or cool, which is not worth watching. The
interesting events are real, legible and unscripted, and there are two of them.
This world has one pot, one cup and one fire; it cannot sustain contention
because there is almost nothing to contend over. That is a specific,
actionable requirement for any world built to show this off, rather than a
verdict against the idea.

## Limits

- **The refusal path was never exercised by the model.** The response schema
  constrains `action_id` to an enum of currently-offered ids, so all 16 answers
  were valid by construction. That is the right engineering choice and it means
  the real run proves the *happy* path only. The refusal path — invented ids,
  blocked ids, and prose shaped like an action — is covered by
  `tests/test_policy_seam.py` with scripted policies and no spend.
- One model, one prompt, one world, 16 turns. This establishes the seam is
  usable, not that the model is good at the world, and certainly not that the
  substrate generalises.
- The baseline is a deliberately unsophisticated comparator. It shows the world
  punishing a bad policy mechanically; it is not a competitive benchmark.
- The evidence file records a live trace and cost, so it is a retained
  observation receipt, not a deterministic probe. It is deliberately not wired
  into a `--check` gate.
