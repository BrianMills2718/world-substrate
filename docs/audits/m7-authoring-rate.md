---
role: audit
status: active
reviewed_through: 2026-09-04
authority_refs:
  - ./m3-overheat-authoring-experiment.md
  - ./m4-spill-experiment.md
  - ../contracts/mechanic-profile-v0.md
  - ../../roadmap/README.md
---

# M7: can an agent author a mechanic it was not handed?

The roadmap's central hypothesis is that agent teams can add useful, coherent
mechanics faster than interaction risk grows. M3 and M4 measured the risk half —
whether bad mechanics get caught — using mechanics whose author also wrote the
checks. This measures the other half.

A model was shown the workshop world, its component types, the mechanics already
installed, and one example declaration. It was **not** told which mechanic to
write, and **not** told what the installer or the assays check for. Ten
attempts, graded against criteria fixed before any attempt ran.

Evidence: [`evidence/m7/authoring-attempts-v0.json`](../../evidence/m7/authoring-attempts-v0.json).
Cost: **$0.0147** for ten attempts on `openrouter/openai/gpt-5.6-luna`.

Nothing the model produced was executed as code. It returns a declaration,
compiled by `world_substrate.authoring` into an ordinary `ProcessRule`, so the
engine's write-scope guard, causal trace, installer and assays all applied
without knowing the mechanic was authored.

## Results

| | count |
| --- | --- |
| valid declarations | 9 / 10 |
| installed with no findings | 9 / 9 |
| **write-scope violations** | **0** |
| fired in the graded assembly run | 6 / 9 |
| distinct ideas | 9 |
| had undeclared consequential readers flagged by the assay | 8 / 9 |

The one rejection was refused by the declaration language, not by a safety
property: it proposed an effect on `portable`, which names a component rather
than a field. That is arguably a limit of the language rather than a fault in
the proposal.

## The dominant failure mode is triviality, not danger

Nothing dangerous was proposed. Zero scope violations across nine installed
mechanics, and the safety machinery built over M3–M6 had nothing to catch.

What it caught instead is that four of nine proposals are bounds or slow decay
on quantities that already exist — `tool-wear-cap`, `fatigue-cap`,
`unheld-tool-maintenance`, `tool-wear-maintenance`. Two of those are outright
no-ops: `tool-wear-cap` sets wear to 100 when wear is already ≥ 100, and
`fatigue-cap` does the same for fatigue, but both existing processes already
clamp with `min(100, ...)`, so the condition is unreachable. They install
cleanly, declare their scope correctly, and do nothing.

Five proposals add real behaviour: fatigue recovery, a fatigue penalty on skill,
skill improvement through work, releasing parts on attachment, and withdrawing a
worn-out tool. Those are reasonable mechanics a person might have written.

## The sharpest finding: an undeclared world convention

Two proposals (`release-attached-parts`, `worn-tool-withdrawal`) set
`ownership.owner_ref` to the **empty string**.

This world encodes ownership as a prefixed reference — `actor:mira`,
`place:bench`, `assembly:frame-a`. An empty string matches none of those. With
`release-attached-parts` installed, a leg that `AttachRule` had marked
`assembly:frame-a` becomes `''`: the provenance saying which assembly holds it
is destroyed, and the mechanic is redundant with `AttachRule`, which already
sets ownership on attachment.

Nothing catches this. It stays inside its declared write scope, so the engine
accepts it. `World.validate()` passes, because `owner_ref` is typed as `str` and
`''` is a valid `str`. The installer passes. Only the interaction assay noticed
anything, and what it flagged was the *dependency* miss, not the malformed
value.

**The convention was never declared, so nothing could check it.** M3 framed the
residual risk as consequential state *an author* failed to declare. This is the
inverse: state the *world* failed to declare about itself. `owner_ref` should be
a typed reference rather than a bare string, and that is now an open obligation.

## The assay earned its keep

Every author declared some dependencies — most named one — and the assay flagged
one or two real consequential readers each had missed. Spot-checked:

- `fatigue-recovery` declared `workshop.process.fatigue` and missed that both
  actions read worker state.
- `release-attached-parts` declared `workshop.assembly.attach` and missed that
  `pick-up` reads `ownership.owner_ref` — a genuine interaction, since clearing
  an owner changes what can be picked up.
- `tool-wear-maintenance` declared `workshop.process.tool-wear` and missed that
  `attach` gates on tool wear, so healing wear changes whether attaching
  succeeds.

These are true positives. An author reasoning about their own mechanic's causal
story reliably missed who else reads what they write, which is exactly the gap
the assay was built for and the first time it has been tested against authors
who did not know it existed.

## Answering the question

For this model, this world, and ten attempts:

- useful new behaviour: **5 of 10**
- actively harmful: **0 of 10**
- incoherent but passing every check: **2 of 10** (the empty-owner pair)
- trivial or no-op: **2 of 10**

Risk did not outrun usefulness. But usefulness is modest, and the interesting
cost is not dangerous mechanics — it is a steady supply of plausible-looking
ones that are redundant, inert, or quietly violate a convention nobody wrote
down. Review effort scales with proposals, not with their quality.

## Limits

- One model, one world, ten attempts, one prompt. Not a benchmark.
- I wrote the assays, the grading criteria and the declaration language, so a
  clean result deserves a sceptical read. What is *not* self-serving is that the
  model did not know any of them existed.
- `fires` is scenario-dependent. A sound mechanic guarding a state the graded
  assembly run never reaches reads as not firing.
- The declaration language is small. A richer one would allow better mechanics
  and more ways to go wrong; both directions are untested.
- Diversity came from telling the model what had already been proposed, because
  the shared client strips `temperature` for this model. That is weaker than
  independent sampling.
