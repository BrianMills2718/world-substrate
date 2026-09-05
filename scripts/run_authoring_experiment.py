#!/usr/bin/env python3
"""Can an agent author a useful mechanic it was not handed?

M3 and M4 measured whether bad mechanics get caught, using mechanics whose
author also wrote the checks. This measures the other half of the roadmap's
central hypothesis -- whether useful mechanics arrive faster than problems --
by asking a model for a mechanic the workshop world needs, without telling it
which one and without telling it what the installer or the assays look for.

Nothing the model produces is executed as code. It returns a declaration, which
`world_substrate.authoring` compiles into an ordinary ProcessRule, so the
engine's write-scope guard, causal trace, installer and assays all apply
without knowing the mechanic was authored.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from dataclasses import fields as dataclass_fields
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.workshop.components import (
    AssemblyState,
    PartState,
    ToolState,
    WorkerState,
)
from reference_worlds.workshop.probe import build_engine, build_registry
from world_substrate.assay import assay_declared_readers
from world_substrate.authoring import (
    MECHANIC_SCHEMA,
    CompiledMechanic,
    DeclarationError,
    DeclaredMechanic,
)
from world_substrate.engine import ScopeViolation
from world_substrate.profile import MechanicProfile, retrofit_package

OUTPUT = REPO / "evidence/m7/authoring-attempts-v0.json"
DEFAULT_MODEL = "openrouter/openai/gpt-5.6-luna"

EXAMPLE = json.dumps(
    {
        "mechanic_id": "workshop.process.tool-wear",
        "rationale": "A tool held and used by a worker wears out over time.",
        "order": 20,
        "selector": {
            "has_component": "tool",
            "where": [{"path": "components.tool.wear", "op": "lt", "value": 100}],
        },
        "effects": [{"path": "components.tool.wear", "op": "add", "value": 7}],
        "reads": ["entities.<x>.components.tool", "entities.<x>.ownership"],
        "writes": ["entities.<x>.components.tool.wear"],
        "dependencies": [],
        "invariants": ["wear never exceeds wear_limit"],
        "limits": ["Wear is uniform; it does not depend on what the tool is used for."],
    },
    indent=2,
)


def _world_context() -> dict[str, object]:
    engine = build_engine(REPO)
    registry = build_registry()
    rules = [registry.action(k) for k in registry.action_kinds()]
    rules += list(registry.processes())
    return {
        "world_id": engine.world.world_id,
        "entities": [
            {
                "entity_id": entity.entity_id,
                "label": entity.label,
                "components": sorted(entity.components) or "none",
            }
            for entity in sorted(engine.world.entities.values(), key=lambda e: e.entity_id)
        ],
        "component_types": {
            name: [f.name for f in dataclass_fields(cls)]
            for name, cls in (
                ("worker", WorkerState),
                ("part", PartState),
                ("tool", ToolState),
                ("assembly", AssemblyState),
            )
        },
        "installed": [
            {
                "mechanic_id": rule.rule_id,
                "order": getattr(rule, "order", "action"),
                "reads": list(rule.read_paths),
                "writes": list(rule.write_paths),
            }
            for rule in rules
        ],
        "example": EXAMPLE,
    }


def _exercise(engine) -> None:
    """Run the bench through a full assembly so mechanics have a fair chance."""
    from reference_worlds.workshop.mechanics import AttachAction, PickUpAction

    engine.apply(PickUpAction("mira", "wrench-1", engine.world.revision, "grading"))
    for part in ("leg-1", "leg-2", "seat-1"):
        engine.apply(PickUpAction("mira", part, engine.world.revision, "grading"))
        engine.apply(
            AttachAction("mira", part, "frame-a", engine.world.revision, "grading")
        )
        engine.advance(2)


def _grade(value: dict) -> dict[str, object]:
    """Score one attempt against criteria fixed before any attempt was made.

    `fires` is scenario-dependent, not a verdict on the mechanic: it means the
    mechanic produced at least one causal event in a 30-tick run of the bench
    scenario. A sound mechanic guarding a state this scenario never reaches
    will read as not firing.
    """
    grade: dict[str, object] = {
        "declaration_valid": False,
        "installs": False,
        "fires": False,
        "scope_clean": None,
        "novel": None,
        "relational": False,
        "refused_by_invariant": None,
        "assay_findings": None,
        "note": "",
    }
    try:
        declared = DeclaredMechanic.from_dict(value)
    except (DeclarationError, TypeError, ValueError, KeyError) as error:
        grade["note"] = f"declaration rejected: {error}"
        return grade
    grade["declaration_valid"] = True
    grade["mechanic_id"] = declared.mechanic_id
    grade["rationale"] = declared.rationale
    # The one dimension that changed between this run and the first: whether
    # the proposal reaches a second entity at all. Everything else is graded
    # exactly as before so the two runs stay comparable.
    grade["relational"] = bool(declared.selector.get("related"))

    registry = build_registry()
    existing = {rule.rule_id for rule in registry.processes()}
    existing |= {registry.action(k).rule_id for k in registry.action_kinds()}
    grade["novel"] = declared.mechanic_id not in existing

    profile = MechanicProfile()
    rules = [registry.action(k) for k in registry.action_kinds()]
    rules += list(registry.processes())
    for rule in rules:
        profile.install(retrofit_package(rule, "workshop"), rule)
    compiled = CompiledMechanic(declared)
    findings = profile.install(declared.package(), compiled)
    rejects = [f for f in findings if f.severity == "reject"]
    if rejects:
        grade["note"] = f"installer rejected: {rejects[0].code}"
        return grade
    grade["installs"] = True

    others = {k: v for k, v in profile.packages.items() if k != declared.mechanic_id}
    grade["assay_findings"] = len(assay_declared_readers(declared.package(), others))

    engine = build_engine(REPO)
    engine.registry.register_process(CompiledMechanic(declared))
    engine.world.rule_versions = engine.registry.versions()
    try:
        # Actually build the chair. An idle bench holds no tool, so tool wear
        # never runs and anything keyed to a worn tool cannot fire however good
        # it is -- grading against an idle scenario measures the scenario.
        _exercise(engine)
        engine.advance(30)
        grade["scope_clean"] = True
    except ScopeViolation as error:
        grade["scope_clean"] = False
        grade["note"] = f"wrote outside declared scope: {str(error)[:120]}"
        return grade
    except ValueError as error:
        # A canonical-state invariant refused the write. That is the substrate
        # doing its job, not the harness failing, and it must not be recorded
        # as a grading error -- two attempts in the relational run set
        # `owner_ref` to "", the exact defect M7 found and nothing could then
        # catch, and grading them as harness faults would have hidden the one
        # result that shows the fix works.
        grade["scope_clean"] = True
        grade["refused_by_invariant"] = str(error)[:160]
        grade["note"] = f"refused by a world invariant: {str(error)[:120]}"
        return grade
    grade["fires"] = any(
        event["rule_id"] == declared.mechanic_id for event in engine.world.events
    )
    return grade


def _regrade(args) -> int:
    """Replay grading over stored declarations. No model call, no spend."""
    source = args.regrade or args.output
    payload = json.loads(Path(source).read_text())
    stored = [a["grade"] for a in payload["attempts"]]
    regraded = []
    for attempt in payload["attempts"]:
        value = attempt["declaration"]
        regraded.append(_grade(value if isinstance(value, dict) else {}))
    if args.check:
        differing = [
            attempt["attempt"]
            for attempt, before, after in zip(payload["attempts"], stored, regraded)
            if {k: v for k, v in before.items() if k != "note"}
            != {k: v for k, v in after.items() if k != "note"}
        ]
        if differing:
            print(f"regraded verdicts differ from the stored ones: {differing}")
            return 1
        print(f"stored grades reproduce from the declarations: {source}")
        return 0
    for attempt, grade in zip(payload["attempts"], regraded):
        attempt["grade"] = grade
    payload["summary"] = _summarise(payload["attempts"])
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        Path(source).write_text(text)
        print(f"rewrote {source}")
    print(json.dumps(payload["summary"], indent=2))
    return 0


def _summarise(attempts: list[dict]) -> dict[str, object]:
    return {
        "declaration_valid": sum(a["grade"]["declaration_valid"] for a in attempts),
        "installed": sum(a["grade"]["installs"] for a in attempts),
        "fired": sum(bool(a["grade"]["fires"]) for a in attempts),
        "scope_violations": sum(a["grade"]["scope_clean"] is False for a in attempts),
        "refused_by_invariant": sum(
            a["grade"].get("refused_by_invariant") is not None for a in attempts
        ),
        "relational": sum(bool(a["grade"].get("relational")) for a in attempts),
        "usable": sum(
            bool(a["grade"]["installs"] and a["grade"]["fires"] and a["grade"]["scope_clean"])
            for a in attempts
        ),
        "distinct_mechanic_ids": len(
            {a["grade"].get("mechanic_id") for a in attempts} - {None}
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--attempts", type=int, default=10)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-budget", type=float, default=1.00)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--write", action="store_true")
    parser.add_argument(
        "--regrade",
        type=Path,
        help=(
            "Re-grade the declarations stored in an existing evidence file "
            "instead of calling a model. Grading is deterministic, so this "
            "replays the experiment's verdicts for free -- the property every "
            "other probe in this repository already has."
        ),
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Re-grade and require the stored grades to match.",
    )
    args = parser.parse_args()

    if args.regrade or args.check:
        return _regrade(args)

    from llm_client import call_llm_json_schema, get_cost, render_prompt

    trace_id = f"world-substrate-authoring-{uuid.uuid4().hex[:10]}"
    context = _world_context()
    attempts = []
    proposed: list[str] = []
    for index in range(1, args.attempts + 1):
        # This model has `temperature` stripped by the client's parameter
        # policy, so repeated calls converge on the same proposal. Listing what
        # has already been proposed buys diversity without telling the model
        # which mechanic to write or what the checks look for.
        messages = render_prompt(
            str(REPO / "prompts/mechanic_author.yaml"),
            already_proposed=proposed,
            **context,
        )
        value, _ = call_llm_json_schema(
            args.model,
            messages,
            MECHANIC_SCHEMA,
            schema_name="declared_mechanic",
            task="world-substrate-mechanic-authoring",
            trace_id=trace_id,
            max_budget=args.max_budget,
            reasoning_effort="medium",
        )
        try:
            grade = _grade(value if isinstance(value, dict) else {})
        except (
            DeclarationError,
            AttributeError,
            IndexError,
            KeyError,
            TypeError,
            ValueError,
        ) as error:
            # Declaration-shaped failures only: one unusable proposal must not
            # end a ten-attempt experiment, and it is recorded rather than
            # swallowed. Anything else still propagates.
            grade = {
                "declaration_valid": True,
                "installs": False,
                "fires": False,
                "scope_clean": None,
                "novel": None,
                "assay_findings": None,
                "mechanic_id": str((value or {}).get("mechanic_id", "?")),
                "note": f"grading harness error: {type(error).__name__}: {error}",
            }
        if isinstance(value, dict) and value.get("mechanic_id"):
            proposed.append(str(value["mechanic_id"]))
        attempts.append({"attempt": index, "declaration": value, "grade": grade})
        print(
            f"  attempt {index:>2}: "
            f"{grade.get('mechanic_id', '(invalid)')} | "
            f"installs={grade['installs']} fires={grade['fires']} "
            f"scope_clean={grade['scope_clean']} "
            f"relational={grade.get('relational')} assay={grade['assay_findings']}"
        )

    # `usable` is computed by _summarise, which both the live and regrade
    # paths share so the two can never disagree about what a run scored.
    payload = {
        "schema_version": "world-substrate-authoring-experiment/v0",
        "claim": (
            "A model was asked for one mechanic the workshop world needs, without "
            "being told which one or what the installer and assays check. Each "
            "attempt was graded against criteria fixed before any attempt ran."
        ),
        "model": args.model,
        "trace_id": trace_id,
        "attempts_run": len(attempts),
        "cost_usd": round(get_cost(trace_id=trace_id), 6),
        "summary": _summarise(attempts),
        "attempts": attempts,
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.write:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
        print(f"wrote {args.output}")
    print(json.dumps(payload["summary"], indent=2))
    print(f"cost: ${payload['cost_usd']:.5f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
