from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))
spec = importlib.util.spec_from_file_location("scene_replay", REPO / "scripts/render_scene_replay.py")
scene = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scene)


def lab_profile() -> dict:
    return {
        "schema_version": "world-substrate-scene-profile/v0",
        "scene_id": "lab-v0",
        "world": "lab",
        "title": "Lab replay",
        "subtitle": "One sample moves through a scanner.",
        "assets": {
            "rhea": {"kind": "emoji", "value": "🧑‍🔬"},
            "sol": {"kind": "emoji", "value": "🤖"},
            "sample": {"kind": "emoji", "value": "🧪"},
            "scan": {"kind": "emoji", "value": "✨"},
        },
        "actors": {
            "rhea": {"asset": "rhea", "home": [10, 50], "carry_offset": [5, 3], "carry_spacing": [0, 5]},
            "sol": {"asset": "sol", "home": [80, 50], "carry_offset": [-5, 3], "carry_spacing": [0, 5]},
        },
        "stations": {
            "bench": {"presentation_only": True, "label": "Bench", "role": "surface", "rect": [35, 40, 30, 20], "actor_anchor": [35, 45], "item_anchor": [50, 50]},
            "scanner": {"presentation_only": True, "label": "Scanner", "role": "workstation", "rect": [42, 10, 16, 15], "actor_anchor": [50, 25], "item_anchor": [50, 17], "active_asset": "scan"},
            "result": {"presentation_only": True, "label": "Result", "role": "goal", "rect": [70, 72, 24, 20], "progress_actor": "rhea", "item_anchor": [82, 82]},
        },
        "entities": {
            "sample-1": {"asset": "sample", "home": [50, 50], "label": "sample", "initial_state": "raw"},
        },
        "action_visuals": {
            "take": {"item_field": "item", "actor_target": {"station": "bench"}, "ownership": "take", "clear_item_station": True},
            "scan": {"item_field": "item", "actor_target": {"station": "scanner"}, "set_state": "analyzed", "activate_station_from": "station", "item_target": {"station": "scanner"}},
        },
        "state_styles": {"raw": {"scale": 1}, "analyzed": {"scale": 1.15, "saturation": 1.2}},
        "progress_assets": {"sample": "sample"},
        "moment_rules": [{"id": "terminal", "when": "all_progress_filled", "label": "done", "terminal": True}],
    }


def lab_trace() -> dict:
    return {
        "schema_version": "world-substrate-contested-run/v3",
        "world": "lab",
        "actors": ["rhea", "sol"],
        "model": "scripted",
        "cost_usd": 0,
        "transcript": [
            {
                "turn": 1,
                "committed_first": "rhea",
                "actors": {
                    "rhea": {"status": "accepted", "did": {"actor": "rhea", "kind": "take", "item": "sample-1"}, "wanted": {"actor": "rhea", "kind": "take", "item": "sample-1"}, "said": "Secure the sample."},
                    "sol": {"status": "no_action", "did": None, "wanted": None, "said": "Observe."},
                },
                "progress": {"rhea": {"filled": False, "plated": [], "still_wants": ["sample"]}, "sol": {"filled": True, "plated": [], "still_wants": []}},
            },
            {
                "turn": 2,
                "committed_first": "rhea",
                "actors": {
                    "rhea": {"status": "accepted", "did": {"actor": "rhea", "kind": "scan", "item": "sample-1", "station": "scanner"}, "wanted": {"actor": "rhea", "kind": "scan", "item": "sample-1", "station": "scanner"}, "said": "Scan the sample."},
                    "sol": {"status": "no_action", "did": None, "wanted": None, "said": "Observe."},
                },
                "progress": {"rhea": {"filled": True, "plated": ["sample"], "still_wants": []}, "sol": {"filled": True, "plated": [], "still_wants": []}},
            },
        ],
    }


class GenericSceneReplay(unittest.TestCase):
    def test_non_domain_profile_drives_custom_action_and_state(self):
        profile = lab_profile()
        frames = scene.build_frames(lab_trace(), profile)
        self.assertEqual(frames[0]["holders"]["sample-1"], "rhea")
        self.assertEqual(frames[1]["items"]["sample-1"]["state"], "analyzed")
        self.assertEqual(frames[1]["active_stations"], ["scanner"])
        self.assertIn("terminal", frames[1]["moments"])

    def test_generic_html_comes_entirely_from_profile_and_trace(self):
        profile = lab_profile()
        html = scene.render_html(lab_trace(), profile, {}, REPO)
        self.assertIn("Lab replay", html)
        self.assertIn("🧪", html)
        self.assertIn("Scanner", html)
        self.assertIn("scan sample-1 / scanner", html)

    def test_generic_renderer_has_no_flagship_domain_ids(self):
        source = (REPO / "scripts/render_scene_replay.py").read_text().lower()
        for word in ("kitchen", "knife", "carrot", "onion", "potato", "order-stew", "order-hash"):
            with self.subTest(word=word):
                self.assertNotIn(word, source)


    def test_actor_can_target_visual_entity_position_from_declared_field(self):
        profile = lab_profile()
        profile["action_visuals"]["take"]["actor_target"] = {"entity_field": "item"}
        frames = scene.build_frames(lab_trace(), profile)
        self.assertEqual(frames[0]["actor_positions"]["rhea"], [50, 50])

    def test_profile_world_must_match_trace_world(self):
        profile = lab_profile()
        trace = lab_trace()
        trace["world"] = "other"
        with self.assertRaises(ValueError):
            scene.build_frames(trace, profile)


    def test_station_item_layout_uses_relative_slots_and_grid_overflow(self):
        profile = lab_profile()
        profile["entities"].update({
            "sample-2": {"asset": "sample", "home": [52, 50], "label": "sample 2"},
            "sample-3": {"asset": "sample", "home": [54, 50], "label": "sample 3"},
        })
        profile["stations"]["scanner"]["item_layout"] = {
            "slots": [[0.25, 0.5]],
            "overflow": "grid",
        }
        state = {
            "sample-1": {"state": "analyzed", "placed_at": "scanner"},
            "sample-2": {"state": "analyzed", "placed_at": "scanner"},
            "sample-3": {"state": "analyzed", "placed_at": "scanner"},
        }
        positions = scene._station_layout_positions(profile, state)
        self.assertEqual(positions["sample-1"], [46.0, 17.5])
        self.assertEqual(len({tuple(point) for point in positions.values()}), 3)

    def test_station_item_layout_rejects_out_of_range_slots(self):
        profile = lab_profile()
        profile["stations"]["scanner"]["item_layout"] = {"slots": [[1.2, 0.5]]}
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profile.json"
            path.write_text(json.dumps(profile))
            with self.assertRaisesRegex(ValueError, "relative 0..1 coordinates"):
                scene.load_scene_profile(path)

    def test_image_assets_are_embedded_for_single_file_replays(self):
        profile = lab_profile()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            # One valid 1x1 transparent PNG.
            png = root / "dot.png"
            import base64
            png.write_bytes(base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="))
            profile["assets"]["sample"] = {"kind": "image", "path": "dot.png"}
            html = scene.render_html(lab_trace(), profile, {}, root)
            self.assertIn("data:image/png;base64,", html)


if __name__ == "__main__":
    unittest.main()
