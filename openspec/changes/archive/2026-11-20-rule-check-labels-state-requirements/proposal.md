# Rule check labels state the requirement

## Why

A refused move shows the failed check's label as the reason. Sam's refused request-training showed `you are the
dispatcher`, meaning "only the dispatcher can request training"; a person reading the page saw a false statement
about Sam (world-substrate#245, evidence `s1-airfield` Finding 4). The label is written by the rule writer's prompt,
which asked for a "condition", so the fix is at the origin: ask for a requirement. Rewriting labels at refusal time
would need prose interpretation, which is an AI call or a regex, and neither is wanted here.

Source: inferred by agent from issue #245's expected text ("refusal text states the unmet requirement"), under
Brian, 2026-11-16: "stop stopping for my decsion on stuff that isnt irreversibly and significantly dagnerous".

## What changes

- `scripts/generate_causal_model.py`: the label rule asks for a short requirement ("the watering can must be free",
  "only the dispatcher can request training") and forbids wording a label as a claim about the person trying.
- `world-builder-page` requirement "Rule checks read as plain English": one added scenario.
- Not changed: saved worlds keep their existing labels; they change only when rebuilt.
