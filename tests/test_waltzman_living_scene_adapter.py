"""Retained Waltzman branches use the generic living-scene frame source."""

from __future__ import annotations

import sys
import unittest
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from world_substrate.living_scene import (
    canonical_world_at_boundary,
    load_live_projection_bundle,
    validate_live_projection_bundle,
)
from world_substrate.projection import replay_projection

BASELINE = REPO / "evidence/waltzman/demo-baseline-v0.json"
INTERVENTION = REPO / "evidence/waltzman/demo-intervention-v0.json"


class WaltzmanLivingSceneAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = load_live_projection_bundle(BASELINE)
        cls.intervention = load_live_projection_bundle(INTERVENTION)

    def test_retained_branches_load_through_same_generic_adapter(self):
        for branch, bundle in (("baseline", self.baseline), ("intervention", self.intervention)):
            with self.subTest(branch=branch):
                self.assertEqual(bundle["branch_id"], branch)
                self.assertEqual(bundle["world_id"], "waltzman-coordination-lab-v0")
                validate_live_projection_bundle(bundle)

    def test_every_event_boundary_matches_prefix_replay(self):
        for branch, bundle in (("baseline", self.baseline), ("intervention", self.intervention)):
            for boundary in range(-1, len(bundle["events"])):
                with self.subTest(branch=branch, boundary=boundary):
                    direct = canonical_world_at_boundary(bundle, boundary)
                    prefix = bundle["events"][: boundary + 1]
                    expected = replay_projection(bundle["initial_snapshot"], prefix)
                    self.assertEqual(direct, expected)

    def test_final_material_state_matches_retained_projection_exactly(self):
        for branch, bundle in (("baseline", self.baseline), ("intervention", self.intervention)):
            with self.subTest(branch=branch):
                final = canonical_world_at_boundary(bundle, len(bundle["events"]) - 1)
                self.assertEqual(final, bundle["projection_final"])

    def test_intervention_preserves_exact_baseline_history_prefix(self):
        baseline_events = self.baseline["events"]
        intervention_events = self.intervention["events"]
        self.assertEqual(intervention_events[: len(baseline_events)], baseline_events)
        self.assertEqual(
            self.intervention["fork"]["shared_event_count"],
            len(baseline_events),
        )

    def test_adapter_preserves_event_tick_revision_and_status_identity(self):
        for bundle in (self.baseline, self.intervention):
            event_ids = [event["event_id"] for event in bundle["events"]]
            self.assertEqual(len(event_ids), len(set(event_ids)))
            for index, event in enumerate(bundle["events"]):
                world = canonical_world_at_boundary(bundle, index)
                self.assertEqual(world["tick"], event["tick"])
                self.assertEqual(world["revision"], event["world_revision"])
                self.assertIn(event["status"], {"accepted", "rejected"})

    def test_analysis_annotations_are_not_needed_for_canonical_reconstruction(self):
        for bundle in (self.baseline, self.intervention):
            stripped = deepcopy(bundle)
            stripped.pop("analysis", None)
            stripped.pop("adequacy", None)
            stripped.pop("annotations", None)
            self.assertEqual(
                canonical_world_at_boundary(stripped, len(stripped["events"]) - 1),
                canonical_world_at_boundary(bundle, len(bundle["events"]) - 1),
            )


if __name__ == "__main__":
    unittest.main()
