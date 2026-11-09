# Plan: an AI judge fed by automatic propagation (draft)

**Status:** draft, being planned with Brian. Not adopted; nothing is built. The planning package is rebuilt once,
when the open questions below are settled, after the documentation cleanup (branch `docs/cleanup-2026-11-09`)
lands.

## Why

Brian, 2026-11-09: "an ai adjudicator doesnt really scale and that we need to facts to have implications and
blockers. like 50 things could propagate down a causal chain 100 links deep taht the llm would not be able to
understand so we need that causal chain to automaticlaly rpogate and to deliver the resutls of that propagation to
he ai judge along with blockers."

## Decided

Source: Brian, 2026-11-09, "yes i aprpove all those except for whether the bribe works seems like should be a
deicsion made by the person being bribed. that is not a rule as much as a decision. maybe we need to discuss the
difference between rules/constraints and ddecisions?"

1. **Goal.** The project goal gains scale: a simulation platform for plausible worlds "that stays faithful as worlds
   grow too big for an AI to track: the engine works out every knock-on effect and blocker, and an AI judge decides
   using those results."
2. **What the judge decides: gaps only.** The judge decides attempts that no rule covers. The rulebook keeps deciding
   everything it covers. The judge never overrides a blocker the engine found.
3. **Rulings become rules.** A judge ruling is written down as a new rule, passes the World Builder's existing rules
   check, applies to everyone from then on, and the engine propagates its effects.
4. **Exception: another person's choice is a decision, not a rule.** Whether a bribe works is decided by the person
   being bribed, not by the judge and not by a rule.

## Open: constraints, rules and decisions (discussing with Brian)

Agent proposal, 2026-11-09, awaiting Brian:

- **Constraint:** what the world makes possible or impossible. Nobody can break it. Examples: you cannot hand over
  coins you do not have; a truck with no fuel does not move; only the customs officer can sign the inspection
  release. The engine owns these (checks, declared laws in `src/world_substrate/laws.py`, propagation).
- **Decision:** what a person chooses among the things the constraints leave possible. Examples: the trader offers
  40 coins; the officer accepts or refuses; the officer then signs or does not. People (Concordia residents) own
  these. An attempt that needs another person's choice goes to that person to decide; today only plain requests do
  this (#326).
- **Norm (society's rule):** what people expect or forbid, which can be broken. Example: bribery is illegal. It has
  consequences only when someone notices and decides to act (an inspector reports it, a court fines). A norm must
  not be written as a declared law, because the engine refuses every step that breaks a declared law, so nobody
  could ever take a bribe.
- **The judge's job** is then narrow: when the rulebook is silent, rule on constraints only (can coins change hands
  here? what actually opens the gate?), write the ruling as a rule, and route every choice to the person whose
  choice it is.

Brian's refinement, 2026-11-09: "there is a ddifference between as igned release clearing the cargo as a norm and
like some programmatic enry with abar code or whateve.r this was deiscussed pretty extneively in the form of hte
idea of a password managed comptuer where only 1 person was supped to use it with ehir password but if they could
be social engineered for exampel to get a password then someone else woul eb abel to sue it. i liek the ostrom
stuff". So authority splits three ways:

- **What the mechanism checks** (constraint): the computer logs in whoever types the right password; a barcode
  gate opens for whatever valid code it reads. A gate a guard opens is not a mechanism: it opens when the guard
  decides to.
- **Who holds the credential** (a fact in the world): Alice knows the password; the trader holds a signed release.
  A credential can be told, overheard, copied, forged or phished.
- **Who is supposed to use it** (norm): only Alice should log in; only signed cargo should pass. Breakable.

Writing "only Alice can log in" as a constraint would make social engineering impossible, which is wrong. The
earlier Cybernetic Influence work discussed this at length (password-comparison fixture with a protected
verifier, `cybernetic_influence_v3/src/cybernetic_influence/causal_core/fixtures.py:81`); its conclusions are
being retrieved so they are reused, not re-derived.

## Agent technical calls (to confirm in the full plan)

- Remove the 32-reaction cap per moment ([Decision 009](../decisions/009-same-moment-knock-on-effects.md)):
  each process and thing pair already fires at most once per moment (`src/world_substrate/engine.py`, `_settle`
  docstring), so a chain cannot loop without it, and Brian's example (50 chains, 100 links deep) needs thousands.
- The judge is Concordia's own game master (`concordia/components/game_master/event_resolution.py`, `EventResolution`),
  conditioned on a component that supplies the engine's results and blockers, not a judge of our own
  (Decision 006).
