from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
spec = importlib.util.spec_from_file_location("spatial", REPO / "scripts/render_kitchen_spatial_replay.py")
spatial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(spatial)

TRACE = REPO / "evidence/kitchen/full-service-replication-v1-run1.json"


class SpatialReplayUsesRetainedTruth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.trace = json.loads(TRACE.read_text())
        cls.frames = spatial.build_frames(cls.trace)
        cls.html = spatial.render_html(cls.trace)

    def test_all_terminal_trace_turns_are_frames(self):
        self.assertEqual([f["turn"] for f in self.frames], list(range(1, 18)))

    def test_handoff_and_takeover_are_preserved(self):
        self.assertIn("handoff", self.frames[9]["moments"])
        self.assertIsNone(self.frames[9]["knife_owner"])
        self.assertIn("takeover", self.frames[10]["moments"])
        self.assertEqual(self.frames[10]["knife_owner"], "ama")

    def test_item_preparation_progresses_from_actions(self):
        self.assertEqual(self.frames[2]["items"]["potato-1"]["prep"], "chopped")
        self.assertEqual(self.frames[3]["items"]["potato-1"]["prep"], "cooked")
        self.assertEqual(self.frames[4]["items"]["potato-1"]["prep"], "plated")

    def test_terminal_orders_are_trace_authoritative(self):
        self.assertTrue(self.frames[-1]["progress"]["ama"]["filled"])
        self.assertTrue(self.frames[-1]["progress"]["bo"]["filled"])
        self.assertIn("terminal", self.frames[-1]["moments"])

    def test_output_is_a_graphical_autoplay_replay(self):
        self.assertIn("class='stage'", self.html)
        self.assertIn("setInterval", self.html)
        self.assertIn("Kitchen replay: two cooks, one knife", self.html)
        self.assertIn("kitchen geometry is illustrative", self.html.lower())
        self.assertNotIn("world_substrate", Path(REPO / "scripts/render_kitchen_spatial_replay.py").read_text())


if __name__ == "__main__":
    unittest.main()
