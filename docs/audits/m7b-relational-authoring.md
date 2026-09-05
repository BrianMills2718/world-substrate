---
role: audit
status: active
reviewed_through: 2026-09-04
authority_refs:
  - ./m7-authoring-rate.md
  - ../contracts/mechanic-profile-v0.md
  - ../../roadmap/README.md
---

# M7b: was the triviality the model's, or the language's?

[M7](./m7-authoring-rate.md) concluded that "triviality, not danger, is the
bottleneck": nine installable mechanics, zero write-scope violations, five with
real behaviour, two inert. Its Limits section named the declaration language as
small. Nothing connected the two.

They needed connecting, because the language could express exactly one shape of
mechanic. Selection and effects were confined to a single entity, so no
proposal could say "the worker holding this tool" — every expressible mechanic
was a field update on one entity, which is to say a clamp or a decay. A
language that cannot express anything else cannot distinguish a model with
nothing to say from a model with no way to say it. The zero-violation result
had the same problem from the other side: confined to one entity, a declaration
had to contradict itself to violate scope at all.

So the language was widened by exactly one thing — a selected entity may bind
one related entity it names through its own string field, and read and write
that entity — and the experiment was re-run with the same model, prompt shape,
world, grading criteria and attempt count. The model was told the relation
exists. It was still not told which mechanic to write or what the checks look
for.

Evidence: [`evidence/m7/authoring-attempts-relational-v1.json`](../../evidence/m7/authoring-attempts-relational-v1.json).
Cost: **$0.0166** for ten attempts on `openrouter/openai/gpt-5.6-luna`.
Grading is deterministic and replays with no spend:
`python scripts/run_authoring_experiment.py --check --output evidence/m7/authoring-attempts-relational-v1.json`.

## Result

| | M7 (one entity) | M7b (one relation) |
| --- | --- | --- |
| valid declarations | 9 / 10 | 8 / 10 |
| installed | 9 / 9 | 8 / 8 |
| **write-scope violations** | **0** | **0** |
| refused by a world invariant | n/a — nothing could catch it | **2** |
| used a relation | not expressible | **4 / 8** |
| fired in the graded run | 6 / 9 | 4 / 8 |

## The answer: partly the language, and less than expected

The prediction going in was that the ceiling was mostly the language. It was
not. Given the ability to express a relation, the model used it in four of
eight valid declarations — real uptake, not noise — and two of those fired and
did something no mechanic in this project could previously express:

- **`worn-tool-strain`** — a tool past its wear limit tires the worker holding
  it. Selects tools, binds the holder through `ownership.owner_ref`, adds
  fatigue to the holder.
- **`tool-practice`** — a worker gains skill from using a worn tool. Same
  binding, writes the holder's skill.

Those are ordinary mechanics a person would write, and they are the first
authored mechanics in this repository where the cause is on one entity and the
effect is on another.

But triviality did not go away. `tool-wear-clamp` and `fatigue-clamp` are the
same two inert no-ops M7 got — clamping a value that existing processes already
clamp with `min(100, ...)`, so the condition is unreachable. The model proposed
them again with a strictly richer language available. That is the part of the
finding that survives: **the language ceiling was real and it was not the main
driver.** M7's headline stands, with its cause now measured rather than
assumed.

## Risk still did not outrun usefulness — and this time that means something

Zero write-scope violations again. Unlike M7, that is now a real result rather
than an artifact: a relational mechanic *can* violate scope, by declaring only
its own paths and reaching through the binding to the other entity, and the
engine refuses it, rolls the tick back, and names the exact path it reached
(`tests/test_relational_mechanics.py::test_an_undeclared_relational_write_is_refused`).
The machinery was load-bearing for the first time and nothing loaded it.

Notably, both relational mechanics that fired declared their cross-entity write
correctly, one of them inventing the placeholder `entities.<holder>.…` to do it.

## The sharpest finding: the same defect class recurred, and was caught

Two of ten proposals set `ownership.owner_ref` to the empty string —
`attached-part-release` and `worn-tool-drop`. That is the *exact* defect M7
found, at the same rate, from the same model, one language generation later.

The difference is what happened next. In M7 it installed cleanly, passed
`World.validate()`, destroyed the attachment provenance and nothing anywhere
could catch it. Here it is refused by a canonical-state invariant, the tick
rolls back, and the grade records `refused_by_invariant`. This is the clearest
evidence available that the typed-reference work does real work: the population
of proposals did not improve, and the substrate stopped caring.

It also exposes a gap the refusal makes visible rather than creates.
`worn-tool-drop` is a *good* idea — a tool worn past its limit should leave the
worker's hands — and the model had no way to express "no owner" except by
emptying the reference. The world has no vocabulary for unowned. Refusing the
empty string is right; leaving the author no way to say what they meant is a
missing capability, now recorded as an open obligation.

## Limits

- One model, one world, ten attempts, one prompt, one relation. Not a
  benchmark, and n=10 against n=10 is a comparison of two small samples.
- I wrote the language, the grading criteria and the assays. What is not
  self-serving is that the model was told none of them, and that the headline
  result contradicts the prediction I recorded before running it.
- `fired` remains scenario-dependent: a sound mechanic guarding a state the
  graded assembly run never reaches reads as not firing. Four of eight is not
  four of eight *good* mechanics.
- Two attempts were rejected for proposing an effect on `portable`, which names
  a component rather than a field — the same rejection M7 got once. The model
  keeps wanting to change portability and the language keeps refusing; that is
  a language gap being reported twice, not two independent failures.
- Diversity still comes from telling the model what has already been proposed,
  because the shared client strips `temperature` for this model.
