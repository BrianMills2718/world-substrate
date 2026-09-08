from __future__ import annotations

import base64
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import render_replay_studio as studio

MANIFEST = REPO / "evidence/replay-studio-v0.json"
ARTIFACT = REPO / "evidence/renders/world-replay-studio-v0.html"


class ReplayStudioTests(unittest.TestCase):
    def test_manifest_exposes_all_real_replay_worlds_and_available_variants(self):
        manifest = studio.load_manifest(MANIFEST)
        self.assertEqual(manifest["default_world"], "kitchen")
        self.assertEqual([w["id"] for w in manifest["worlds"]], ["kitchen", "castaway", "workshop", "greenhouse"])
        expected_variants = {
            "kitchen": {"automatic", "polished"},
            "castaway": {"automatic", "polished"},
            "workshop": {"automatic", "polished"},
            "greenhouse": {"automatic"},
        }
        for world in manifest["worlds"]:
            self.assertEqual({v["id"] for v in world["variants"]}, expected_variants[world["id"]])

    def test_bundle_metadata_comes_from_retained_zero_review_profiles_and_traces(self):
        manifest, _ = studio.build_bundle(MANIFEST)
        by_world = {w["id"]: w for w in manifest["worlds"]}
        self.assertEqual(set(by_world["kitchen"]["metadata"]["action_kinds"]), {"take", "put_down", "chop", "cook", "plate"})
        self.assertEqual(set(by_world["castaway"]["metadata"]["action_kinds"]), {"fill", "drink"})
        self.assertEqual(set(by_world["workshop"]["metadata"]["action_kinds"]), {"pick_up", "attach"})
        self.assertEqual(set(by_world["greenhouse"]["metadata"]["action_kinds"]), {"take", "fill", "water", "put_down"})
        self.assertEqual(by_world["kitchen"]["metadata"]["turns"], 17)
        self.assertEqual(by_world["greenhouse"]["metadata"]["turns"], 7)
        self.assertTrue(all(w["metadata"]["bootstrap_todos"] == 0 for w in by_world.values()))

    def test_embedded_replays_are_byte_exact_copies_of_retained_artifacts(self):
        manifest, documents = studio.build_bundle(MANIFEST)
        for world in manifest["worlds"]:
            for variant in world["variants"]:
                with self.subTest(world=world["id"], variant=variant["id"]):
                    decoded = base64.b64decode(documents[variant["document_key"]]).decode("utf-8")
                    expected = (MANIFEST.parent / variant["replay"]).read_text()
                    self.assertEqual(decoded, expected)

    def test_studio_regenerates_exactly_as_one_standalone_html_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "studio.html"
            studio.render_file(MANIFEST, output)
            self.assertEqual(output.read_text(), ARTIFACT.read_text())
        rendered = ARTIFACT.read_text()
        self.assertIn("World Replay Studio", rendered)
        self.assertIn("sandbox='allow-scripts'", rendered)
        self.assertIn("URLSearchParams(location.search)", rendered)
        self.assertIn("Open replay alone", rendered)

    def test_studio_renderer_contains_no_world_specific_scene_logic(self):
        source = (REPO / "scripts/render_replay_studio.py").read_text().lower()
        for token in ("order-stew", "unsafe-pool", "frame-a", "wrench-1", "carrot-1"):
            with self.subTest(token=token):
                self.assertNotIn(token, source)


if __name__ == "__main__":
    unittest.main()
