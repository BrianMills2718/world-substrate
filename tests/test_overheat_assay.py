"""M3: the first offline mechanics-authoring experiment, run adversarially.

The authored mechanic (`process.material.overheat-damage`) is real and useful,
and its package deliberately omits a consequential dependency. The question is
not whether the mechanic works -- it does -- but whether installation and the
interaction assays surface what its author failed to declare.

The first three tests are the ones OVERHEAT_DAMAGE_PACKAGE names in its own
`tests` field; the installer requires a package to declare them and they must
therefore exist under exactly these names.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.overheat import (
    build_baseline_engine,
    build_overheat_engine,
    installed_profile,
)
from world_substrate.assay import (
    assay_affordance_changes,
    assay_declared_readers,
    assay_undeclared_component_reads,
)
from world_substrate.engine import Engine
from world_substrate.mechanisms.damage import (
    OVERHEAT_DAMAGE_PACKAGE,
    OverheatDamageProcess,
)
from world_substrate.rules import FillAction, HeatAction

VESSEL = "gourd-flask"


def _stage(engine: Engine) -> Engine:
    engine.apply(
        FillAction("robinson", VESSEL, "unsafe-pool", 500, engine.world.revision, "test")
    )
    engine.apply(
        HeatAction("robinson", VESSEL, "fire-camp", engine.world.revision, "test")
    )
    return engine


def test_vessel_over_its_heat_limit_degrades_and_fails() -> None:
    engine = _stage(build_overheat_engine())
    # advance() commits onto a clone, so re-read the entity after every tick
    # rather than holding a reference across one.
    engine.advance(1)
    vessel = engine.world.entities[VESSEL]
    # 62C, still under the gourd's 80C limit.
    assert vessel.thermal.temperature_c == 62.0
    assert vessel.condition.value == 100

    engine.advance(3)
    vessel = engine.world.entities[VESSEL]
    # Boiling water is above the pitch seal's limit: 40 damage per tick.
    assert vessel.thermal.temperature_c > 80
    assert vessel.condition.value == 0


def test_vessel_within_its_heat_limit_is_undamaged() -> None:
    # The clay pot's limit is 240C and it never leaves ambient in this run.
    engine = _stage(build_overheat_engine())
    engine.advance(5)

    assert engine.world.entities["clay-pot"].condition.value == 100


def test_damage_stops_at_zero_and_never_repairs() -> None:
    engine = _stage(build_overheat_engine())
    engine.advance(10)
    assert engine.world.entities[VESSEL].condition.value == 0
    engine.advance(10)
    assert engine.world.entities[VESSEL].condition.value == 0


class AuthoringExperimentTests(unittest.TestCase):
    def test_the_authored_mechanic_installs_with_no_findings(self) -> None:
        # This is the experiment's premise: a package that omits a real
        # dependency still passes every check the installer can make from the
        # declaration alone.
        _, findings = installed_profile(True)

        self.assertEqual(findings, [])

    def test_the_mechanic_stays_inside_its_declared_write_scope(self) -> None:
        # A newly authored mechanic is exactly the case the engine's scope
        # guard exists for. It writes only condition.value, as declared.
        engine = _stage(build_overheat_engine())
        engine.advance(5)

        overheat_events = [
            event
            for event in engine.world.events
            if event["rule_id"] == OverheatDamageProcess.rule_id
        ]
        self.assertTrue(overheat_events)
        for event in overheat_events:
            changed = {
                change["path"] for change in event["changes"] if change["path"] != "revision"
            }
            self.assertTrue(
                all(path.endswith(".condition.value") for path in changed),
                f"unexpected write: {changed}",
            )

    def test_declaration_assay_names_readers_of_the_written_state(self) -> None:
        base_profile, _ = installed_profile(False)

        findings = assay_declared_readers(
            OVERHEAT_DAMAGE_PACKAGE, base_profile.packages
        )

        named = {
            token.rstrip(",")
            for finding in findings
            for token in finding.detail.split()
            if token.startswith(("mechanism.", "process."))
        }
        self.assertIn("mechanism.liquid.drink", named)
        self.assertIn("mechanism.thermal.heat", named)
        # At the M3 revision this assay could NOT see take/give: both gated on
        # vessel.condition without declaring the read, so there was nothing for
        # a declaration-based check to match. Those three declarations
        # (take, give, process.thermal.vessels) have since been repaired, and
        # the same assay now reaches them. The before/after is the clearest
        # evidence of the ceiling M3 identified: see
        # docs/audits/m3-overheat-authoring-experiment.md.
        self.assertIn("mechanism.ownership.take", named)
        self.assertIn("mechanism.ownership.give", named)

    def test_affordance_assay_catches_take_which_the_declaration_assay_misses(
        self,
    ) -> None:
        # The two assays are complementary, which is the point of running both.
        findings = assay_affordance_changes(
            _stage(build_baseline_engine()),
            _stage(build_overheat_engine()),
            ["robinson", "friday"],
            5,
            OVERHEAT_DAMAGE_PACKAGE,
        )

        kinds = {finding.detail.split()[0] for finding in findings}
        self.assertIn("take", kinds)
        # And it stays specific rather than reporting every downstream
        # difference between two diverged worlds.
        self.assertLessEqual(len(findings), 8)

    def test_every_registered_rule_declares_the_components_it_reads(self) -> None:
        registry = build_baseline_engine().registry
        rules = [registry.action(kind) for kind in registry.action_kinds()]
        rules += list(registry.processes())

        findings = assay_undeclared_component_reads(rules)

        # Regression guard on the repair. Every registered rule now declares
        # the components it reads; if a future mechanic reintroduces an
        # undeclared read, the declaration-based assay silently loses reach
        # again, which is exactly the failure this audit exists to prevent.
        self.assertEqual(
            [finding.detail for finding in findings],
            [],
            "a registered rule reads a component it does not declare",
        )

    def test_no_assay_catches_the_destroyed_vessel_still_holding_liquid(self) -> None:
        # The honest residual. A destroyed vessel retains its contents: no
        # mechanic spills it, no affordance reveals it, conservation still
        # balances, and world.validate() passes. Decision 003 predicts exactly
        # this class of omission survives an author's own declaration.
        engine = _stage(build_overheat_engine())
        engine.advance(5)
        vessel = engine.world.entities[VESSEL]

        self.assertEqual(vessel.condition.value, 0)
        self.assertGreater(vessel.liquid.volume_ml, 0)
        engine.world.validate()

        findings = assay_affordance_changes(
            _stage(build_baseline_engine()),
            _stage(build_overheat_engine()),
            ["robinson", "friday"],
            5,
            OVERHEAT_DAMAGE_PACKAGE,
        )
        self.assertFalse(
            [item for item in findings if "liquid" in item.detail or "spill" in item.detail]
        )


if __name__ == "__main__":
    unittest.main()
