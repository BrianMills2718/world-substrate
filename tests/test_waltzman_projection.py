"""The living client consumes canonical snapshot/event data, not a second sim."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.render_waltzman_demo import render_html
from scripts.run_waltzman_demo import build_demo_runs
from world_substrate.projection import projection_sse_messages, replay_projection


class WaltzmanProjectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.runs = build_demo_runs()

    def test_snapshot_plus_event_deltas_reconstruct_each_canonical_branch_exactly(self):
        for name, run in self.runs.items():
            with self.subTest(branch=name):
                reconstructed = replay_projection(run["initial_snapshot"], run["events"])
                self.assertEqual(reconstructed, run["projection_final"])
                self.assertTrue(run["verification"]["projection_matches_world"])
                self.assertEqual(
                    run["projection_final_hash"],
                    run["verification"]["canonical_material_hash"],
                )

    def test_projection_preserves_stable_event_ids_and_branch_prefix(self):
        baseline = self.runs["baseline"]
        intervention = self.runs["intervention"]
        baseline_ids = [event["event_id"] for event in baseline["events"]]
        intervention_ids = [event["event_id"] for event in intervention["events"]]
        self.assertEqual(len(baseline_ids), len(set(baseline_ids)))
        self.assertEqual(intervention_ids[: len(baseline_ids)], baseline_ids)
        self.assertEqual(intervention["fork"]["shared_event_count"], len(baseline_ids))

    def test_sse_is_snapshot_then_canonical_events_then_completion(self):
        run = self.runs["baseline"]
        messages = projection_sse_messages(run)
        self.assertIn("event: snapshot", messages[0])
        self.assertIn("world-substrate-snapshot/v1", messages[0])
        self.assertEqual(sum("event: world-event" in message for message in messages), len(run["events"]))
        self.assertIn(f"id: baseline:{run['events'][0]['event_id']}", messages[1])
        self.assertIn("event: complete", messages[-1])

    def test_renderer_is_data_driven_by_projection_bundles(self):
        html = render_html(self.runs)
        self.assertIn("Waltzman Coordination Lab", html)
        self.assertIn("waltzman-coordination-lab-v0", html)
        self.assertIn("e00021", html)
        self.assertIn("baseline", html)
        self.assertIn("intervention", html)
        self.assertNotIn("const stages=", html.lower())
        self.assertIn("initial_snapshot", html)
        self.assertIn("causal_parent_event_ids", html)
        self.assertIn("information_context", html)
        self.assertIn("deck.gl@9.4.0", html)
        self.assertIn("OrthographicView", html)


if __name__ == "__main__":
    unittest.main()
