#!/usr/bin/env python3
"""Build World Substrate's metamodel: the kinds of things its rules relate, from one table.

The metamodel is the type-level view of the substrate (what an entity, a component, an action kind, a
check, a process, an event, an affordance or an observation is, and how they connect), not the
service-level system model in ODD.md. Each type cites the code or contract that defines it and says
how it maps onto the shared hypergraph kernel (scientific-hypergraph `hypergraph-kernel-v2.json`), as
bounded-design's typed-relational-metamodels reference requires (rule 1: reuse before minting).

Writes, from TYPES and LINKS below:
  docs/model/metamodel.graph.json    typed-graph/v1, drawn by Representation Router's graph viewer
  docs/model/metamodel-mapping.json  each type's relation to the kernel, read by the planning validator
  docs/model/METAMODEL.md            the glossary: definition, code, kernel mapping

  python3 scripts/build_metamodel.py          # write the three files
  python3 scripts/build_metamodel.py --check  # exit 1 when a file is out of date or a citation is wrong
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KERNEL_CLONE = Path.home() / "code2" / "scientific-hypergraph"
KERNEL = {"repository": "BrianMills2718/scientific-hypergraph",
          "revision": "7b0638fe0aef41c772bb181996516f98be479597",
          "path": "wiki/reference/metamodel/hypergraph-kernel-v2.json"}

# id, label, layer, built, definition, code (path:line), kernel relation, kernel term, why
TYPES = [
    ("world", "World", "state", True,
     "The one canonical world of a run: entities, a tick, a revision and the events so far.",
     "src/world_substrate/model.py:382", "specializes", "scientific-hypergraph-v2 document",
     "a world is one model document of elements and relation instances, plus a clock the kernel lacks"),
    ("category", "Category (kind of thing)", "state", True,
     "What kind of thing an entity is (person, place, door, helicopter); rules select by category.",
     "schemas/world-authoring-bundle-v0.schema.json:55", "same", "sci:instanceOf type",
     "an entity's category is the type it is an instance of"),
    ("entity", "Entity (thing)", "state", True,
     "Any thing in the world, a person, a wall or a glass alike, with a stable id and typed components.",
     "src/world_substrate/model.py:223", "specializes", "sci:ModelElement",
     "every entity is a model element; World Substrate adds components"),
    ("component", "Component (state field)", "state", True,
     "A typed field on an entity (location, water level, passable, role); the only thing effects change. "
     "A disposition (a wall cannot be walked through) is a component value plus the checks that read it. "
     "Held in Entity.components; each component type is registered by register_component (model.py:188).",
     "src/world_substrate/model.py:241", "composes", "sci:RelationInstance (holder, value)",
     "a component value is a binary relation instance between an entity and a value"),
    ("place", "Place", "state", True,
     "An entity of category place; every other entity's location names the place it is in.",
     "scripts/generate_world_bundle.py:96", "specializes", "sci:ModelElement",
     "a place is a model element like any entity; location components point at it"),
    ("way", "Way between places", "state", True,
     "What lies between two places (a door, a brick wall): an entity naming both places with a passable "
     "field; moving names its way and needs it passable. Until fix F6 lands (Q25, settled by argument), a "
     "way works from its first place to its second only.",
     "scripts/generate_causal_model.py:430", "specializes", "sci:ModelElement",
     "a way is an entity, so a model element like a place; its two place references compose relation "
     "instances (way, from place) and (way, to place), and passable is a component on it"),
    ("action-kind", "Action kind (effector)", "rules", True,
     "Something an actor can try, with named participant roles, checks and effects, compiled before use "
     "(a generated DeclaredActionMechanic) or hand-written (FillRule and the other mechanisms); either way "
     "the Engine runs it through the action-rule interface.",
     "src/world_substrate/action_authoring.py:61", "specializes", "sci:RelationType",
     "an action kind is an n-ary relation type whose roles are its participants; the kernel has no effects"),
    ("rule-interface", "Action and process rule interface", "rules", True,
     "What the Engine actually runs: an action rule discovers, checks and applies one action kind; a process "
     "rule says when it is due and applies; both declare read and write paths. Generated mechanics and the "
     "hand-written mechanisms library (FillRule, VesselFailureSpillProcess) both implement it.",
     "src/world_substrate/rules.py:317", "no_counterpart", "",
     "an executable interface; the kernel holds no code"),
    ("registry", "Rule registry", "rules", True,
     "The sole lookup surface for the action and process rules installed in one world, in a fixed order.",
     "src/world_substrate/rules.py:428", "no_counterpart", "",
     "a runtime table of executable rules, outside the kernel"),
    ("causal-parent", "Hard causal parent", "acting", True,
     "An earlier event a rule declares as mechanically supporting this one (opt-in, DeclaresCausalParents); "
     "kept apart from information a person merely had in mind. S2's reactions cite their trigger this way.",
     "src/world_substrate/rules.py:383", "specializes", "sci:RelationInstance (event, parent event)",
     "a directed relation instance between two applied events"),
    ("role", "Participant role", "rules", True,
     "A named slot of an action kind (actor, to, way, aircraft) and the categories that may fill it.",
     "src/world_substrate/action_authoring.py:67", "same", "sci:RoleType",
     "a participant role is a declared role of the relation type, with a participant-type constraint"),
    ("sense", "Sense binding", "rules", True,
     "The meaning and participant roles Linguistic Core gives an action kind; never its effects.",
     "src/world_substrate/semantic.py:15", "composes", "sci:declaresRole",
     "a sense supplies the role declarations the relation type carries"),
    ("check", "Check (precondition)", "rules", True,
     "A test a move or process must pass against current state (the way is passable, the trainee "
     "can fly); a failed check refuses the move with the check named.",
     "src/world_substrate/action_authoring.py:69", "no_counterpart", "",
     "the kernel stores relations, not evaluable conditions"),
    ("effect", "Effect", "rules", True,
     "A change to one component path that runs when every check holds, inside the declared write scope.",
     "src/world_substrate/action_authoring.py:70", "no_counterpart", "",
     "the kernel stores relations, not changes to state, so it has no evaluable effects"),
    ("write-scope", "Declared write scope", "rules", True,
     "The paths a rule may change; the Engine refuses any change outside them.",
     "src/world_substrate/engine.py:120", "no_counterpart", "",
     "authority derived from the declaration; the kernel has no authority model"),
    ("process", "Process (knock-on rule)", "rules", True,
     "A rule the world runs by itself for every matching entity whose checks hold, each round by "
     "default or at once when its timing is immediately; this is how effects propagate (plants dry out, a glass breaks).",
     "src/world_substrate/action_authoring.py:245", "no_counterpart", "",
     "an actorless effectful rule; the kernel has none"),
    ("knock-on-now", "Same-moment knock-on", "rules", True,
     "A process with timing immediately, run in waves inside the same moment as the move or round step "
     "that triggered it until nothing more is due; each process and thing pair fires once per moment, and "
     "more than 32 reactions refuses the whole moment (slice S2 of docs/plans/open_attempt.md, ODD 8.20).",
     "src/world_substrate/engine.py:938", "no_counterpart", "",
     "a timing rule over effectful processes; the kernel has none"),
    ("skill-roll", "Skill roll", "rules", False,
     "A seeded roll on an action kind so a move can partly succeed or fail by skill (planned slice S3).",
     "docs/plans/open_attempt.md:182", "no_counterpart", "",
     "a stochastic effect; the kernel has none"),
    ("terminal", "Terminal condition", "rules", True,
     "A state-derived stop: when its checks hold over the selected entities, the task ends one way.",
     "src/world_substrate/action_authoring.py:195", "no_counterpart", "",
     "an evaluable condition; the kernel has none"),
    ("profile", "Frozen mechanic profile", "rules", True,
     "The validated rules of one world frozen under an id before any run.",
     "src/world_substrate/profile.py:249", "no_counterpart", "",
     "a versioned package of executable rules, outside the kernel"),
    ("affordance", "Affordance (offered move)", "acting", True,
     "A move an actor can make now: an action kind with participants bound and its checks holding, "
     "as Engine.discover lists it.",
     "src/world_substrate/engine.py:352", "no_counterpart", "",
     "a query result derived from rules and state, not a stored relation"),
    ("decider", "Decider (policy)", "acting", True,
     "What chooses an actor's next move: scripted, an AI menu chooser or a Concordia resident.",
     "src/world_substrate/policy.py:50", "no_counterpart", "",
     "cognition outside the world; the kernel does not model agents"),
    ("attempt", "Attempt (free text)", "acting", True,
     "What a resident says it tries, in its own words; never executable.",
     "src/world_substrate/attempt.py:149", "no_counterpart", "",
     "natural language outside the world"),
    ("attempt-reading", "Attempt reading", "acting", True,
     "The interpreter's typed reading of an attempt: an action kind and participants, with no outcome "
     "field, a wait, or no match.",
     "src/world_substrate/attempt.py:81", "specializes", "sci:RelationInstance (proposed)",
     "a proposed instance of an action-kind relation type, not yet applied"),
    ("unmatched", "Unmatched attempt", "acting", True,
     "An attempt no action kind covers; it changes nothing and is listed in the run's build record.",
     "src/world_substrate/attempt.py:25", "no_counterpart", "",
     "a recorded refusal with no relation type to instantiate"),
    ("typed-action", "Typed action (command)", "acting", True,
     "The envelope submitted to the Engine: actor, action kind, bound participants, base revision.",
     "src/world_substrate/rules.py:307", "specializes", "sci:RelationInstance with sci:RoleBinding",
     "a typed action is a relation instance whose role bindings are its participants"),
    ("event", "Event", "acting", True,
     "The record of one attempt or process step: status, every check and its result, the changes, "
     "the cause and an id like r14-e00012.",
     "src/world_substrate/engine.py:529", "specializes", "sci:RelationInstance",
     "an event is an applied relation instance plus check results, changes and causal parents"),
    ("observation", "Observation (sensor)", "noticing", True,
     "What one actor can see of the world now, filtered by place and by information delivery.",
     "src/world_substrate/engine.py:235", "no_counterpart", "",
     "a per-actor view derived from state, not a stored relation"),
    ("information", "Information and delivery (channel)", "noticing", True,
     "An information entity and its delivery rows: who has been told what, by which channel, and when; "
     "a word said across the world reaches no one without a delivery.",
     "src/world_substrate/information.py:21", "specializes", "sci:RelationInstance (information, recipient)",
     "a delivery is a relation instance between a piece of information and a recipient"),
]

# source, label, target
LINKS = [
    ("world", "holds", "entity"), ("entity", "is a", "category"), ("entity", "has", "component"),
    ("place", "is an", "entity"), ("way", "is an", "entity"), ("way", "joins", "place"), ("action-kind", "declares", "role"), ("sense", "names", "role"),
    ("role", "filled by", "category"), ("action-kind", "requires", "check"), ("action-kind", "produces", "effect"),
    ("process", "requires", "check"), ("process", "produces", "effect"), ("effect", "changes", "component"),
    ("effect", "bounded by", "write-scope"), ("rule-interface", "runs", "action-kind"), ("rule-interface", "runs", "process"),
    ("registry", "installs", "rule-interface"), ("event", "cites", "causal-parent"), ("knock-on-now", "cites", "causal-parent"), ("check", "reads", "component"), ("knock-on-now", "is a timing of", "process"),
    ("skill-roll", "varies", "effect"), ("terminal", "requires", "check"), ("profile", "freezes", "action-kind"),
    ("profile", "freezes", "process"), ("affordance", "offers", "action-kind"), ("decider", "chooses from", "affordance"),
    ("decider", "says", "attempt"), ("attempt", "read as", "attempt-reading"), ("attempt", "or", "unmatched"),
    ("attempt-reading", "becomes", "typed-action"), ("decider", "submits", "typed-action"),
    ("typed-action", "recorded as", "event"), ("process", "recorded as", "event"), ("event", "changes", "component"),
    ("observation", "shows", "entity"), ("observation", "filtered by", "information"), ("observation", "feeds", "decider"),
]

LAYERS = {
    "state": ("World state", "#3b6fb6", "What exists: things, their kinds and their typed fields."),
    "rules": ("Rules", "#c26a1b", "What can change and how: action kinds, checks, effects, processes."),
    "acting": ("Acting", "#6b7280", "How a decider's choice becomes a recorded event."),
    "noticing": ("Noticing", "#2f8f9d", "How an actor comes to know what happened."),
}


def graph() -> dict:
    return {
        "schema": "typed-graph/v1",
        "kinds": {k: {"label": label, "color": color, "explain": explain}
                  for k, (label, color, explain) in LAYERS.items()},
        "nodes": [{"id": i, "label": label, "kind": layer, **({} if built else {"dashed": True}),
                   "explain": definition + ("" if built else " Planned, not built.")}
                  for i, label, layer, built, definition, *_ in TYPES],
        "edges": [{"id": f"m{n + 1}", "source": s, "target": t, "label": label}
                  for n, (s, label, t) in enumerate(LINKS)],
    }


def mapping() -> dict:
    return {
        "record_type": "metamodel_mapping", "schema_version": "1.0",
        "metamodel": "docs/model/metamodel.graph.json", "kernel": KERNEL,
        "mappings": [{"node": i, "relation": rel, **({"maps_to": term} if term else {}), "why": why}
                     for i, _l, _y, _b, _d, _c, rel, term, why in TYPES],
    }


def glossary() -> str:
    rows = "\n".join(
        f"| **{label}** (`{i}`) | {LAYERS[layer][0]} | {'built' if built else 'planned'} | {definition} | "
        f"`{code}` | {rel}{f': {term}' if term else ''} |"
        for i, label, layer, built, definition, code, rel, term, _w in TYPES)
    return f"""---
description: World Substrate metamodel, the kinds of things its rules relate, each with its code and its kernel mapping.
---

# World Substrate metamodel

Generated by `scripts/build_metamodel.py` from one table; edit the table, not this page.

The [system model](ODD.md) describes the service: what is stored, who writes it, what the page shows.
This page describes the world's own types: what an entity, an action kind, a check, a process or an
event is, and how a decider's choice becomes a recorded change. The graph is
[metamodel.graph.json](metamodel.graph.json) (`typed-graph/v1`); the kernel mapping is
[metamodel-mapping.json](metamodel-mapping.json), onto `{KERNEL['repository']}` at
`{KERNEL['revision'][:12]}` (`{KERNEL['path']}`).

One example runs through it. Sam (an entity of category person) tries "walk through the brick wall".
The interpreter reads that as the action kind `move` with `to: hangar` and `way: brick-wall`. The
check "the way is passable" reads the wall's `passable` component, which is false, so the Engine
records an event with that check failed and changes nothing. Sam's next observation shows Sam still
in the office.

| Type | Layer | Status | Definition | Code | Kernel |
| --- | --- | --- | --- | --- | --- |
{rows}

`no_counterpart` marks what the kernel cannot hold: anything evaluable (checks, effects, processes,
terminals, write scopes) and anything derived per actor (affordances, observations) or outside the
world (deciders, attempts). That is the part World Substrate adds to the shared typed-relation shape.

## Reuse gate

Company Planning's typed-relational reference (bounded-design `references/typed-relational-metamodels.md`,
rule 1) asks which existing formalisms were checked before these types were minted, and why each
cannot express them. Checked:

| Formalism | Result |
| --- | --- |
| scientific-hypergraph kernel v2 | The carrier: every structural type maps onto it in the table above. It has no evaluable part, so checks, effects and processes stay here. |
| onto-canon6 | Governs packs of claims (author, derive, review, promote); it does not run effects on a world state. Not a carrier for rules that change state. |
| PDDL and PDDL+ | Closest prior art: an action kind is a PDDL action schema (typed parameters = roles, checks = preconditions, effects), and PDDL+ adds processes that run by themselves and events that fire when their condition holds, which is what a process and the planned same-moment knock-on are (the survey cites PDDL+ processes and events, [flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md) lines 32 and 36). Composed with, not replaced, in `spikes/replacement-2026-10/` (Decision 006): PDDL+ has no declared write scopes, no per-actor observation and no recorded refusal naming its failed precondition, and it is a planning language with no runtime commit. |
| Linguistic Core `relation-schema.v1` | Already used: `src/world_substrate/semantic_relation.py:5-20` projects each sense binding read-only onto Linguistic Core's relation schema (roles sense, participant profile, causal class, causal bearer, mechanic). It is the outward meaning view of the `sense` type above, which maps onto the kernel's role declarations; neither carries effects, and the projection marks the mechanic role "consumer-owned consequence authority". |
| Event Calculus and action languages (C+) | Source of the planned same-moment knock-on (ramification), [flexible-simulator-prior-art-2026-10.md](../research/flexible-simulator-prior-art-2026-10.md). A reasoning formalism, not a runtime. |
| SBML, CellML, bond graphs, Modelica, Decapodes | Not checked further: they hold continuous rate laws and equations; these rules are discrete checks and effects on component values. |
| FMI, SED-ML, OpenMath | Not checked further: a black-box model interface, an experiment description and an expression language; none declares typed participants with effects. |
| Petri nets (transition semantics) | Partly checked: [linked_process_participants.md](../plans/linked_process_participants.md) (prior-art table, line 136) already reuses Petri-net transition semantics for linked process participants (one firing, several places, atomic). A process is close to a transition that fires when enabled, and output arcs are close to a write scope; a typed Petri net (AlgebraicPetri) has no guards over component data, coloured Petri nets have guards, and no Petri net models per-actor noticing or a refusal that names its failed check, so the answer is compose (open question Q24, resolved by argument). |
| TypeDB | Relations with role players are the nearest outside shape for action kinds and attempt readings, but TypeDB runs no state-changing effects, so it could hold the structural types only, which the kernel already does (Q24, resolved: compose). |
"""


def outputs() -> dict[Path, str]:
    model = ROOT / "docs" / "model"
    return {model / "metamodel.graph.json": json.dumps(graph(), indent=1) + "\n",
            model / "metamodel-mapping.json": json.dumps(mapping(), indent=1) + "\n",
            model / "METAMODEL.md": glossary()}


def kernel_pin_status() -> tuple[str, bool]:
    """Whether the pinned kernel revision exists in a local scientific-hypergraph clone, or 'not checked'."""
    if not (KERNEL_CLONE / ".git").exists():
        return f"kernel pin {KERNEL['revision'][:12]} not checked ({KERNEL_CLONE} absent)", True
    found = subprocess.run(["git", "-C", str(KERNEL_CLONE), "cat-file", "-e", f"{KERNEL['revision']}^{{commit}}"],
                           capture_output=True).returncode == 0
    return (f"kernel pin {KERNEL['revision'][:12]} {'exists' if found else 'NOT FOUND'} in {KERNEL_CLONE}", found)


def citation_problems() -> list[str]:
    problems = []
    pin_note, pin_ok = kernel_pin_status()
    print(f"metamodel: {pin_note}")
    if not pin_ok:
        problems.append(f"kernel revision {KERNEL['revision']} is not a commit in {KERNEL_CLONE}")
    for i, *_rest in TYPES:
        code = _rest[4]
        path, _, line = code.partition(":")
        target = ROOT / path
        if not target.is_file():
            problems.append(f"{i}: {path} does not exist")
        elif line and int(line) > len(target.read_text(encoding="utf-8").splitlines()):
            problems.append(f"{i}: {code} is past the end of {path}")
    ids = {t[0] for t in TYPES}
    problems += [f"link {s} -> {t}: unknown type" for s, _l, t in LINKS if s not in ids or t not in ids]
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    problems = citation_problems()
    stale = [p for p, text in outputs().items() if not p.is_file() or p.read_text(encoding="utf-8") != text]
    if args.check:
        problems += [f"{p.relative_to(ROOT)} is out of date: run scripts/build_metamodel.py" for p in stale]
    else:
        for p, text in outputs().items():
            p.write_text(text, encoding="utf-8")
    for p in problems:
        print(f"metamodel: {p}")
    print(f"metamodel: {len(TYPES)} types ({sum(t[3] for t in TYPES)} built), {len(LINKS)} links, "
          f"{len(problems)} problems, exit {1 if problems else 0}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
