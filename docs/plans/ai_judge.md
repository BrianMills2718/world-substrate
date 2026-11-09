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
  here? does a signed release clear the cargo?), write the ruling as a rule, and route every choice to the person
  whose choice it is.

## Agent technical calls (to confirm in the full plan)

- Remove the 32-reaction cap per moment ([Decision 009](../decisions/009-same-moment-knock-on-effects.md)):
  each process and thing pair already fires at most once per moment (`src/world_substrate/engine.py`, `_settle`
  docstring), so a chain cannot loop without it, and Brian's example (50 chains, 100 links deep) needs thousands.
- The judge is Concordia's own game master (`concordia/components/game_master/event_resolution.py`, `EventResolution`),
  conditioned on a component that supplies the engine's results and blockers, not a judge of our own
  (Decision 006).
