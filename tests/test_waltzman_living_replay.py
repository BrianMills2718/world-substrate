from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

spec = importlib.util.spec_from_file_location("waltzman_living_build", REPO / "scripts/build_waltzman_living_replay.py")
build = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(build)


class WaltzmanLivingReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundles, cls.profile, cls.manifest = build.verify()

    def test_manifest_pins_exact_retained_branch_shape_and_checkpoints(self):
        self.assertEqual(self.manifest["shared_history_event_count"], 21)
        self.assertEqual(self.manifest["branches"]["baseline"]["event_count"], 21)
        self.assertEqual(self.manifest["branches"]["intervention"]["event_count"], 28)
        self.assertEqual(self.manifest["checkpoints"]["blocked"]["event_id"], "e00021")
        self.assertEqual(self.manifest["checkpoints"]["intervention_applied"]["event_id"], "e00022")
        self.assertEqual(self.manifest["checkpoints"]["ready"]["event_id"], "e00028")
        self.assertEqual(self.manifest["provider_spend_usd"], 0)

    def test_checkpoint_frame_hashes_are_repeatable(self):
        _, _, second = build.verify()
        first_hashes = {k: v["frame_sha256"] for k, v in self.manifest["checkpoints"].items()}
        second_hashes = {k: v["frame_sha256"] for k, v in second["checkpoints"].items()}
        self.assertEqual(first_hashes, second_hashes)

    def test_branch_player_is_self_contained_and_world_first(self):
        from scripts.render_living_scene_branches import render_branching_html
        html = render_branching_html(self.bundles, self.profile, build.PROFILE.parent)
        self.assertIn("World Substrate", html)
        self.assertIn("Baseline", html)
        self.assertIn("Intervention", html)
        self.assertIn("Waltzman Coordination Lab", html)
        self.assertIn("id='scene'", html)
        self.assertNotIn("deck.gl@", html)
        self.assertNotIn("Waltzman analysis", html)

    def test_retained_manifest_matches_current_build_output(self):
        retained = json.loads(build.MANIFEST.read_text())
        self.assertEqual(retained, self.manifest)

    def test_legacy_renderer_is_explicitly_not_primary_living_path(self):
        source = (REPO / "scripts/render_waltzman_demo.py").read_text().splitlines()[:6]
        self.assertIn("Legacy Waltzman analytical renderer", "\n".join(source))
        self.assertIn("generic Living Scene v1 renderer", "\n".join(source))


if __name__ == "__main__":
    unittest.main()
