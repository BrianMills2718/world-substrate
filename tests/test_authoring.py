"""The declarative authoring path: compile a declaration, never run author code.

An authored mechanic is compiled into an ordinary ProcessRule, so it inherits
the engine's write-scope guard, the causal trace, the installer and the assays
without any of them knowing it was authored. These tests fix that property with
hand-written declarations and no model calls; whether a *model* produces good
declarations is measured by scripts/run_authoring_experiment.py.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.workshop.probe import build_engine, build_registry
from world_substrate.authoring import (
    CompiledMechanic,
    DeclarationError,
    DeclaredMechanic,
)
from world_substrate.engine import ScopeViolation
from world_substrate.profile import MechanicProfile, retrofit_package

VALID = {
    "mechanic_id": "workshop.process.fatigue-dulls-skill",
    "rationale": "A tired worker works less well.",
    "order": 30,
    "selector": {
        "has_component": "worker",
        "where": [{"path": "components.worker.fatigue", "op": "gte", "value": 6}],
    },
    "effects": [{"path": "components.worker.skill", "op": "subtract", "value": 1}],
    "reads": [
        "entities.<x>.components.worker.fatigue",
        "entities.<x>.components.worker.skill",
    ],
    "writes": ["entities.<x>.components.worker.skill"],
    "dependencies": ["workshop.process.fatigue"],
    "invariants": ["skill never rises through this mechanic"],
    "limits": ["No recovery is modelled."],
}


def _install(engine, declaration: dict) -> CompiledMechanic:
    compiled = CompiledMechanic(DeclaredMechanic.from_dict(declaration))
    engine.registry.register_process(compiled)
    engine.world.rule_versions = engine.registry.versions()
    return compiled


class DeclarationTests(unittest.TestCase):
    def test_a_valid_declaration_compiles_installs_and_fires(self) -> None:
        engine = build_engine(REPO)
        _install(engine, VALID)

        engine.advance(3)

        worker = engine.world.entities["mira"].component("worker")
        self.assertEqual(worker.fatigue, 9)
        self.assertEqual(worker.skill, 0)
        self.assertTrue(
            any(
                event["rule_id"] == VALID["mechanic_id"]
                for event in engine.world.events
            )
        )

    def test_an_authored_mechanic_passes_the_installer(self) -> None:
        registry = build_registry()
        profile = MechanicProfile()
        rules = [registry.action(k) for k in registry.action_kinds()]
        rules += list(registry.processes())
        for rule in rules:
            profile.install(retrofit_package(rule, "workshop"), rule)
        declared = DeclaredMechanic.from_dict(VALID)

        findings = profile.install(declared.package(), CompiledMechanic(declared))

        self.assertEqual([f for f in findings if f.severity == "reject"], [])

    def test_writing_outside_the_declaration_is_refused(self) -> None:
        # The whole reason declarative authoring is safe to install: the
        # engine's guard does not care that the mechanic was authored.
        sneaky = dict(VALID)
        sneaky["mechanic_id"] = "workshop.process.sneaky"
        sneaky["effects"] = [
            {"path": "components.worker.skill", "op": "subtract", "value": 1},
            {"path": "components.worker.fatigue", "op": "set", "value": 0},
        ]
        engine = build_engine(REPO)
        _install(engine, sneaky)
        # The mechanic only fires once fatigue reaches 6, so tick 1 commits
        # normally and tick 2 is the one that must roll back. Engine.advance
        # restores the failing tick, not the whole call -- that is the
        # documented per-tick atomicity, so this asserts the state at the start
        # of the failing tick rather than the state before advance() was called.
        engine.advance(1)
        before = engine.world.material_hash()
        fatigue_before = engine.world.entities["mira"].component("worker").fatigue

        with self.assertRaises(ScopeViolation) as raised:
            engine.advance(3)

        self.assertIn("components.worker.fatigue", str(raised.exception))
        self.assertEqual(engine.world.material_hash(), before)
        # The undeclared write set fatigue to 0; it did not survive.
        self.assertEqual(
            engine.world.entities["mira"].component("worker").fatigue, fatigue_before
        )

    def test_malformed_declarations_are_rejected_before_anything_runs(self) -> None:
        for broken, reason in (
            ({k: v for k, v in VALID.items() if k != "writes"}, "missing"),
            ({**VALID, "effects": []}, "nonempty"),
            ({**VALID, "effects": [{"path": "x", "op": "detonate", "value": 1}]}, "op"),
            ({**VALID, "selector": {"where": []}}, "has_component"),
        ):
            with self.subTest(reason=reason), self.assertRaises(DeclarationError):
                DeclaredMechanic.from_dict(broken)

    def test_no_author_supplied_code_is_executed(self) -> None:
        # A declaration is data. Anything that would only matter if it were
        # evaluated as code is simply an unknown field or an unknown op.
        with self.assertRaises(DeclarationError):
            DeclaredMechanic.from_dict(
                {
                    **VALID,
                    "effects": [
                        {"path": "components.worker.skill", "op": "__import__", "value": 1}
                    ],
                }
            )


if __name__ == "__main__":
    unittest.main()
