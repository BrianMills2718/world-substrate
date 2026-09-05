"""M4: close the incoherence M3 left open, and test the assays' specificity.

M3 authored a mechanic with a planted omission and asked whether the assays
caught it. That result is capped by the fact that the same author planted the
omission and wrote the assays. M4 is the complement: the spill mechanic is
authored without a planted omission, and the question is what the assays say
about an honestly-authored mechanic -- what they add, and where they go quiet.

The first three tests are the ones VESSEL_FAILURE_SPILL_PACKAGE names in its
own `tests` field.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.overheat import (
    build_overheat_engine,
    build_spill_engine,
    installed_profile,
)
from world_substrate.assay import (
    assay_affordance_changes,
    assay_conservation,
    assay_declared_readers,
)
from world_substrate.engine import Engine
from world_substrate.mechanisms.damage import (
    VESSEL_FAILURE_SPILL_PACKAGE,
    VesselFailureSpillProcess,
)
from world_substrate.rules import FillAction, HeatAction

VESSEL = "gourd-flask"
INITIAL_VOLUME_ML = 6000


def _stage(engine: Engine) -> Engine:
    engine.apply(
        FillAction("robinson", VESSEL, "unsafe-pool", 500, engine.world.revision, "test")
    )
    engine.apply(
        HeatAction("robinson", VESSEL, "fire-camp", engine.world.revision, "test")
    )
    return engine


class ForgetfulSpillProcess(VesselFailureSpillProcess):
    """Empties the vessel but never records it. Same declared scope."""

    def apply(self, world) -> None:
        for entity in sorted(world.entities.values(), key=lambda item: item.entity_id):
            if not self._failed_and_holding(entity):
                continue
            entity.liquid.volume_ml = 0
            entity.liquid.salt_mg = 0
            entity.liquid.pathogens = 0
            entity.liquid.heat_units = 0


def test_failed_vessel_loses_its_contents() -> None:
    engine = _stage(build_spill_engine())
    engine.advance(5)
    vessel = engine.world.entities[VESSEL]

    assert vessel.condition.value == 0
    assert vessel.liquid.volume_ml == 0
    assert vessel.liquid.heat_units == 0
    assert engine.world.physical_ledger.spilled.volume_ml == 459


def test_intact_vessel_keeps_its_contents() -> None:
    engine = _stage(build_spill_engine())
    engine.advance(1)
    vessel = engine.world.entities[VESSEL]

    # Still at condition 100 after one tick: nothing is emptied.
    assert vessel.condition.value == 100
    assert vessel.liquid.volume_ml == 500
    assert engine.world.physical_ledger.spilled.volume_ml == 0


def test_volume_is_conserved_against_the_ledger() -> None:
    engine = _stage(build_spill_engine())
    engine.advance(5)

    assert assay_conservation(engine, INITIAL_VOLUME_ML) == []


class SpillExperimentTests(unittest.TestCase):
    def test_installation_is_clean(self) -> None:
        _, findings = installed_profile(True, True)

        self.assertEqual(findings, [])

    def test_it_closes_the_incoherence_m3_left_open(self) -> None:
        # M3's uncaught residual was a destroyed vessel still holding liquid.
        before = _stage(build_overheat_engine())
        before.advance(5)
        after = _stage(build_spill_engine())
        after.advance(5)

        self.assertEqual(before.world.entities[VESSEL].condition.value, 0)
        self.assertGreater(before.world.entities[VESSEL].liquid.volume_ml, 0)

        self.assertEqual(after.world.entities[VESSEL].condition.value, 0)
        self.assertEqual(after.world.entities[VESSEL].liquid.volume_ml, 0)

    def test_declaration_assay_names_the_liquid_readers(self) -> None:
        base, _ = installed_profile(True, False)

        findings = assay_declared_readers(VESSEL_FAILURE_SPILL_PACKAGE, base.packages)

        named = {
            token.rstrip(",")
            for finding in findings
            for token in finding.detail.split()
            if token.startswith(("mechanism.", "process."))
        }
        self.assertIn("mechanism.liquid.drink", named)
        # take/give declare their liquid read, unlike their condition read, so
        # this assay sees them here where it could not in M3.
        self.assertIn("mechanism.ownership.take", named)

    def test_affordance_assay_is_silent_because_the_vessel_was_already_refused(
        self,
    ) -> None:
        # The M4 discovery, and it was not designed in. The spill has a real
        # consequence -- 459ml leaves the world -- but every affordance on the
        # vessel was already blocked by "Vessel is intact" from the overheat
        # mechanic, so nothing an actor can attempt changes. A behavioural
        # assay goes quiet exactly when a consequence lands on state everyone
        # has already been refused.
        findings = assay_affordance_changes(
            _stage(build_overheat_engine()),
            _stage(build_spill_engine()),
            ["robinson", "friday"],
            5,
            VESSEL_FAILURE_SPILL_PACKAGE,
        )

        self.assertEqual(findings, [])

    def test_conservation_assay_catches_a_mechanic_that_forgets_the_ledger(
        self,
    ) -> None:
        # Negative control. A green conservation check is worth nothing unless
        # it can go red, and nothing else in the repository catches this:
        # the forgetful mechanic stays inside its declared write scope, the
        # engine accepts every event, and World.validate() passes.
        engine = build_spill_engine()
        for index, process in enumerate(engine.registry._processes):
            if process.rule_id == VesselFailureSpillProcess.rule_id:
                engine.registry._processes[index] = ForgetfulSpillProcess()
        _stage(engine)
        engine.advance(5)

        self.assertTrue(all(event["status"] == "accepted" for event in engine.world.events))
        engine.world.validate()

        findings = assay_conservation(engine, INITIAL_VOLUME_ML)

        self.assertTrue(findings)
        self.assertEqual({finding.code for finding in findings}, {"quantity_not_conserved"})
        self.assertTrue(all(finding.severity == "reject" for finding in findings))
        self.assertTrue(
            any("volume_ml" in finding.detail for finding in findings),
            [finding.detail for finding in findings],
        )

    def test_the_assay_now_catches_a_quantity_other_than_volume(self) -> None:
        """The M4 gap: only volume was recorded for a spill, so only volume
        could ever be balanced. Pathogens are the quantity this world actually
        moves, and they now balance -- and stop balancing when destroyed."""
        base = build_spill_engine()
        initial_pathogens = sum(
            entity.liquid.pathogens
            for entity in base.world.entities.values()
            if entity.liquid is not None
        )
        self.assertGreater(initial_pathogens, 0)

        engine = build_spill_engine()
        _stage(engine)
        engine.advance(5)
        self.assertEqual(
            assay_conservation(
                engine, INITIAL_VOLUME_ML, initial_pathogens=initial_pathogens
            ),
            [],
        )

        # Destroy pathogens without recording them anywhere.
        holding = next(
            entity
            for entity in engine.world.entities.values()
            if entity.liquid is not None and entity.liquid.pathogens > 0
        )
        holding.liquid.pathogens -= 100

        findings = assay_conservation(
            engine, INITIAL_VOLUME_ML, initial_pathogens=initial_pathogens
        )
        self.assertTrue(findings)
        self.assertTrue(any("pathogens" in f.detail for f in findings))
        # Volume is untouched: this is the new check firing on its own.
        self.assertFalse(any("volume_ml" in f.detail for f in findings))

    def test_a_spill_now_records_what_it_destroys(self) -> None:
        """Before `spilled` was a full vector this could not be asserted: a
        failed vessel's pathogens were zeroed and written nowhere."""
        engine = build_spill_engine()
        # Fill and break a vessel while its water is still untreated, so the
        # spill carries pathogens rather than volume alone.
        vessel = next(
            entity
            for entity in engine.world.entities.values()
            if entity.container is not None and entity.condition is not None
        )
        vessel.liquid.volume_ml = 400
        vessel.liquid.pathogens = 160
        vessel.liquid.salt_mg = 0
        vessel.liquid.heat_units = 0
        vessel.condition.value = 0
        engine.world.rule_versions = engine.registry.versions()

        before = engine.world.physical_ledger.spilled.as_dict()
        engine.advance(1)
        after = engine.world.physical_ledger.spilled.as_dict()

        self.assertEqual(after["volume_ml"] - before["volume_ml"], 400)
        self.assertEqual(after["pathogens"] - before["pathogens"], 160)
        self.assertEqual(engine.world.entities[vessel.entity_id].liquid.pathogens, 0)


if __name__ == "__main__":
    unittest.main()
