"""The flagship kitchen view is derived from retained evidence, not a second world."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
TRACE = REPO / "evidence/kitchen/full-service-replication-v1-run1.json"

_spec = importlib.util.spec_from_file_location(
    "render_kitchen_service", REPO / "scripts/render_kitchen_service.py"
)
renderer = importlib.util.module_from_spec(_spec)
sys.modules["render_kitchen_service"] = renderer
_spec.loader.exec_module(renderer)


class TheViewerReconstructsOnlyPresentationState(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.trace = renderer.load_trace(TRACE)
        cls.rows = renderer.reconstruct_turns(cls.trace)

    def row(self, turn: int):
        return next(row for row in self.rows if row.turn == turn)

    def test_it_tracks_the_shared_knife_handoff(self):
        self.assertEqual(self.row(2).knife_owner, "bo")
        self.assertIsNone(self.row(10).knife_owner)
        self.assertIn("handoff", self.row(10).moments)
        self.assertEqual(self.row(11).knife_owner, "ama")
        self.assertIn("takeover", self.row(11).moments)

    def test_it_uses_recorded_order_progress_for_completion(self):
        self.assertTrue(self.row(9).progress["bo"]["filled"])
        self.assertFalse(self.row(9).progress["ama"]["filled"])
        self.assertTrue(self.row(17).progress["bo"]["filled"])
        self.assertTrue(self.row(17).progress["ama"]["filled"])
        self.assertIn("terminal", self.row(17).moments)

    def test_it_keeps_holdings_separate_from_order_progress(self):
        # Plating does not secretly erase ownership in the world. The renderer
        # reconstructs holdings only from take/put_down, rather than guessing
        # from the order's plated list.
        self.assertIn("carrot-1", self.row(10).holdings["ama"])
        self.assertIn("onion-1", self.row(10).holdings["ama"])
        self.assertNotIn("knife", self.row(10).holdings["bo"])


class TheFlagshipArtifactExplainsTheRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.trace = renderer.load_trace(TRACE)
        cls.html = renderer.render_html(cls.trace)

    def test_the_four_key_moments_are_visible(self):
        self.assertIn("first order complete", self.html)
        self.assertIn("knife released", self.html)
        self.assertIn("other cook takes it", self.html)
        self.assertIn("service complete", self.html)
        self.assertIn("Turn 10", self.html)
        self.assertIn("Turn 11", self.html)
        self.assertIn("Turn 17", self.html)

    def test_the_other_directed_reason_is_visible(self):
        self.assertIn(
            "My order is complete, so putting down the knife lets Ama use it to advance her stew.",
            self.html,
        )

    def test_the_view_says_what_is_authoritative(self):
        self.assertIn("Order progress comes directly from the retained trace", self.html)
        self.assertIn("This renderer is read-only", self.html)

    def test_non_v3_input_is_refused(self):
        value = dict(self.trace)
        value["schema_version"] = "world-substrate-contested-run/v2"
        with self.assertRaises(ValueError):
            # Validation is intentionally on loading rather than render_html,
            # so write a tiny temporary record through the public loader.
            import json
            import tempfile

            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "trace.json"
                path.write_text(json.dumps(value))
                renderer.load_trace(path)


if __name__ == "__main__":
    unittest.main()
