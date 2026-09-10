from __future__ import annotations

import copy
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def load_script(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


renderer = load_script("living_renderer_branch_test", REPO / "scripts/render_living_scene.py")
brancher = load_script("living_brancher_test", REPO / "scripts/render_living_scene_branches.py")


class LivingSceneBranchPlayerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile_path = REPO / "tests/fixtures/living_scene/neutral-render-profile-v1.json"
        cls.bundle_path = REPO / "tests/fixtures/living_scene/neutral-render-projection-v0.json"
        cls.profile = renderer.load_scene_contract(cls.profile_path)
        cls.bundle = renderer.load_live_projection_bundle(cls.bundle_path)

    def test_single_scene_has_arbitrary_canonical_boundary_scrubber(self):
        html = renderer.render_html(self.bundle, self.profile, self.profile_path.parent)
        self.assertIn("id='scrub'", html)
        self.assertIn("type='range'", html)
        self.assertIn("oninput=e=>", html)
        self.assertIn(f"max='{len(renderer.build_living_scene_frames(self.bundle, self.profile)) - 1}'", html)

    def test_branch_wrapper_selects_retained_documents_without_world_logic(self):
        alternate = copy.deepcopy(self.bundle)
        alternate["branch_id"] = "alternate"
        html = brancher.render_branching_html(
            {"baseline": self.bundle, "alternate": alternate}, self.profile, self.profile_path.parent
        )
        self.assertIn("Branch", html)
        self.assertIn("Baseline", html)
        self.assertIn("Alternate", html)
        self.assertIn("frame.srcdoc=DOCS[name]", html)
        self.assertIn("requestedFrame", html)

    def test_mobile_layout_overrides_are_validated_but_remain_presentation_only(self):
        profile = copy.deepcopy(json.loads(self.profile_path.read_text()))
        profile["actors"]["actor-a"]["mobile_home"] = [22, 18]
        profile["zones"]["lab"]["mobile_rect"] = [2, 3, 96, 94]
        profile["activities"]["activity-a"]["mobile_anchor"] = [50, 48]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "profile.json"
            path.write_text(json.dumps(profile))
            loaded = renderer.load_scene_contract(path)
        self.assertEqual(loaded["actors"]["actor-a"]["mobile_home"], [22.0, 18.0])
        self.assertEqual(loaded["zones"]["lab"]["mobile_rect"], [2.0, 3.0, 96.0, 94.0])

    def test_generic_branch_and_scene_renderers_contain_no_waltzman_ids(self):
        for path in (REPO / "scripts/render_living_scene.py", REPO / "scripts/render_living_scene_branches.py"):
            text = path.read_text().lower()
            for token in ("waltzman", "mara", "selene", "coalition-hub"):
                with self.subTest(path=path.name, token=token):
                    self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
