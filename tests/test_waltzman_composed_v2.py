from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from world_substrate.living_scene import load_scene_contract

spec = importlib.util.spec_from_file_location("waltzman_composed_v2", REPO / "scripts/build_waltzman_living_replay_v2.py")
build = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(build)


class WaltzmanComposedV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = load_scene_contract(build.PROFILE)
        cls.bundles, _, cls.manifest = build.verify()

    def test_all_residents_use_project_owned_image_assets_not_letter_tokens(self) -> None:
        for actor_id, actor in self.profile["actors"].items():
            asset = self.profile["assets"][actor["asset"]]
            self.assertEqual(asset["kind"], "image", actor_id)
            self.assertIn("assets-v2/resident-", asset["path"])
            self.assertEqual(actor["render"]["display"], "character")

    def test_debug_zone_scaffolding_is_hidden_in_v2(self) -> None:
        self.assertTrue(self.profile["zones"])
        self.assertTrue(all((zone.get("presentation") or {}).get("visible") is False for zone in self.profile["zones"].values()))

    def test_world_objects_and_central_activity_use_composed_assets(self) -> None:
        expected = {"validation-capacity": "validation", "clinical-staff": "staff", "shared-reserve": "reserve", "safeguard-record": "safeguard", "stabilization-package": "package"}
        for entity_id, asset in expected.items():
            self.assertEqual(self.profile["entities"][entity_id]["asset"], asset)
            self.assertEqual(self.profile["entities"][entity_id]["render"]["display"], "world")
        self.assertEqual(self.profile["activities"]["coordination-meeting"]["asset"], "meeting")
        self.assertEqual(self.profile["institutions"]["coalition-hub"]["asset"], "coalition")

    def test_package_has_declarative_available_to_delivered_motion(self) -> None:
        render = self.profile["entities"]["stabilization-package"]["render"]
        self.assertEqual(render["position_state_binding"], "state")
        self.assertNotEqual(render["position_by_state"]["available"], render["position_by_state"]["delivered"])
        self.assertNotEqual(render["mobile_position_by_state"]["available"], render["mobile_position_by_state"]["delivered"])

    def test_key_story_events_declaratively_emphasize_world_objects(self) -> None:
        mappings = {"waltzman.process.validation-failure": "validation-capacity", "waltzman.process.staffing-shortfall": "clinical-staff", "waltzman.process.reserve-conflict": "shared-reserve", "waltzman.process.safeguard-gap": "safeguard-record", "waltzman.activity.start-meeting": "coordination-meeting", "waltzman.institution.coalition-gate": "coalition-hub", "waltzman.intervention.deliver-package": "stabilization-package"}
        for rule_id, entity_id in mappings.items():
            operations = self.profile["event_visuals"][rule_id]["operations"]
            self.assertTrue(any(op.get("op") == "presentation.emphasize" and op.get("entity") == entity_id for op in operations))

    def test_v2_preserves_exact_retained_branch_outcomes_and_history(self) -> None:
        self.assertEqual(self.manifest["shared_history_event_count"], 21)
        self.assertEqual(self.manifest["checkpoints"]["blocked"]["event_id"], "e00021")
        self.assertEqual(self.manifest["checkpoints"]["intervention_applied"]["event_id"], "e00022")
        self.assertEqual(self.manifest["checkpoints"]["ready"]["event_id"], "e00028")
        self.assertEqual(self.manifest["provider_spend_usd"], 0)

    def test_generic_composed_renderers_remain_free_of_waltzman_ids(self) -> None:
        source = "\n".join((REPO / path).read_text().lower() for path in ("scripts/render_composed_living_scene.py", "scripts/render_composed_living_scene_branches.py"))
        for word in ("waltzman", "mara", "validation-capacity", "coalition-hub"):
            with self.subTest(word=word):
                self.assertNotIn(word, source)


if __name__ == "__main__":
    unittest.main()
