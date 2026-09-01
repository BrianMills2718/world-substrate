"""Submission-boundary evidence for invalid and unsupported actions."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine


class ActionEnvelopeTests(unittest.TestCase):
    def test_valid_unregistered_pressure_action_is_unsupported_and_replayable(
        self,
    ) -> None:
        engine = build_transfer_engine(REPO)
        before = engine.world.material_dict()
        result = engine.submit(
            {
                "actor": "robinson",
                "kind": "apply_pressure",
                "target": "clay-pot",
                "pressure_kpa": 200,
                "base_revision": engine.world.revision,
                "controller": "verification_script",
            }
        )
        self.assertEqual(result["status"], "unsupported_action")
        self.assertEqual(before, engine.world.material_dict())
        self.assertEqual(engine.world.commands[-1]["status"], "unsupported_action")
        self.assertTrue(engine.replay()["ok"])

    def test_malformed_envelope_is_invalid_atomic_and_replayable(self) -> None:
        engine = build_transfer_engine(REPO)
        before = engine.world.material_dict()
        result = engine.submit(
            {
                "actor": "robinson",
                "kind": "fill",
                "source": "unsafe-pool",
                "volume_ml": 1000,
                "base_revision": engine.world.revision,
                "controller": "verification_script",
            }
        )
        self.assertEqual(result["status"], "invalid_action")
        self.assertEqual(before, engine.world.material_dict())
        self.assertEqual(engine.world.commands[-1]["op"], "invalid_action")
        self.assertTrue(engine.replay()["ok"])

    def test_valid_registered_envelope_uses_the_same_typed_rule_path(self) -> None:
        engine = build_transfer_engine(REPO)
        row = next(
            item
            for item in engine.discover("robinson", kind="fill")["available"]
            if item["action"]["vessel"] == "clay-pot"
            and item["action"]["source"] == "unsafe-pool"
            and item["action"]["volume_ml"] == 1000
        )
        result = engine.submit(
            {**row["action"], "controller": "verification_script"}
        )
        self.assertEqual(result["status"], "accepted")
        self.assertTrue(engine.replay()["ok"])


if __name__ == "__main__":
    unittest.main()
