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
