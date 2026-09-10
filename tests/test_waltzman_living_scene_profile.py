from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from world_substrate.living_scene import build_living_scene_frames, load_live_projection_bundle, load_scene_contract

spec = importlib.util.spec_from_file_location("living_renderer", REPO / "scripts/render_living_scene.py")
renderer = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(renderer)

PROFILE_PATH = REPO / "reference_worlds/waltzman/living-scene-v1.json"
BASELINE_PATH = REPO / "evidence/waltzman/demo-baseline-v0.json"
INTERVENTION_PATH = REPO / "evidence/waltzman/demo-intervention-v0.json"


class WaltzmanLivingSceneProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.profile = load_scene_contract(PROFILE_PATH)
        cls.baseline = load_live_projection_bundle(BASELINE_PATH)
        cls.intervention = load_live_projection_bundle(INTERVENTION_PATH)
        cls.baseline_frames = build_living_scene_frames(cls.baseline, cls.profile)
        cls.intervention_frames = build_living_scene_frames(cls.intervention, cls.profile)

    def test_profile_declares_all_six_residents_and_major_world_objects(self):
        self.assertEqual(set(self.profile["actors"]), {"mara", "ari", "selene", "tomas", "nira", "idris"})
        self.assertEqual(
            set(self.profile["entities"]),
            {"validation-capacity", "clinical-staff", "shared-reserve", "safeguard-record", "stabilization-package"},
        )
        self.assertEqual(set(self.profile["activities"]), {"coordination-meeting"})
        self.assertEqual(set(self.profile["institutions"]), {"coalition-hub"})

    def test_profile_state_is_bound_to_canonical_components_not_duplicated(self):
        for actor in self.profile["actors"].values():
            self.assertEqual(actor["bindings"]["stance"], "components.commitment.stance")
        self.assertEqual(
            self.profile["institutions"]["coalition-hub"]["bindings"]["status"],
            "components.institution.status",
        )
        self.assertEqual(
            self.profile["activities"]["coordination-meeting"]["bindings"]["status"],
            "components.activity.status",
        )
        for entity_id in ("validation-capacity", "clinical-staff", "shared-reserve"):
            bindings = self.profile["entities"][entity_id]["bindings"]
            self.assertEqual(bindings["current"], "components.resource.current")
            self.assertEqual(bindings["required"], "components.resource.required")

    def test_baseline_visibly_reaches_retained_blocked_state(self):
        frame = self.baseline_frames[-1]
        gate = frame["views"]["institutions"]["coalition-hub"]["bindings"]
        self.assertEqual((gate["status"], gate["support"], gate["conditional"]), ("blocked", 2, 4))
        self.assertEqual(frame["views"]["entities"]["validation-capacity"]["bindings"]["current"], 2)
        self.assertEqual(frame["views"]["entities"]["clinical-staff"]["bindings"]["current"], 18)
        self.assertEqual(frame["views"]["entities"]["shared-reserve"]["bindings"]["current"], 61)
        self.assertEqual(frame["views"]["entities"]["safeguard-record"]["bindings"]["state"], "pending")

    def test_meeting_active_state_persists_by_canonical_ticks_until_completion(self):
        # frame list includes the initial frame, so retained event indexes are +1.
        for frame_index in (17, 18, 19):
            activity = self.baseline_frames[frame_index]["views"]["activities"]["coordination-meeting"]["bindings"]
            self.assertEqual(activity["status"], "active")
            self.assertEqual(activity["started_tick"], 4)
            self.assertEqual(activity["end_tick"], 6)
        completed = self.baseline_frames[20]["views"]["activities"]["coordination-meeting"]["bindings"]
        self.assertEqual(completed["status"], "completed")

    def test_intervention_repairs_prerequisites_before_resident_reassessment(self):
        frame = self.intervention_frames[22]  # event e00022 / retained index 21
        self.assertEqual(frame["event"]["event_id"], "e00022")
        self.assertEqual(frame["views"]["entities"]["validation-capacity"]["bindings"]["current"], 4)
        self.assertEqual(frame["views"]["entities"]["clinical-staff"]["bindings"]["current"], 42)
        self.assertEqual(frame["views"]["entities"]["shared-reserve"]["bindings"]["current"], 90)
        self.assertEqual(frame["views"]["entities"]["safeguard-record"]["bindings"]["state"], "clear")
        self.assertEqual(frame["views"]["entities"]["stabilization-package"]["bindings"]["state"], "delivered")
        self.assertEqual(frame["views"]["actors"]["mara"]["bindings"]["stance"], "conditional")

    def test_intervention_reaches_retained_ready_state(self):
        frame = self.intervention_frames[-1]
        gate = frame["views"]["institutions"]["coalition-hub"]["bindings"]
        self.assertEqual((gate["status"], gate["support"], gate["conditional"]), ("ready", 6, 0))
        for actor_id in self.profile["actors"]:
            self.assertEqual(frame["views"]["actors"][actor_id]["bindings"]["stance"], "support")

    def test_declared_information_binding_uses_retained_delivery_events(self):
        frame = build_living_scene_frames(self.baseline, self.profile, observer_actor_id="ari")[4]
        transmissions = [effect for effect in frame["presentation_effects"] if effect["kind"] == "information_transmission"]
        self.assertEqual(len(transmissions), 1)
        tx = transmissions[0]
        self.assertEqual((tx["source_id"], tx["recipient_id"]), ("mara", "ari"))
        self.assertTrue(tx["content_visible"])

    def test_renderer_uses_canonical_labels_and_state_styles(self):
        html = renderer.render_html(self.baseline, self.profile, PROFILE_PATH.parent)
        self.assertIn("Mara Ellison", html)
        self.assertIn("Coalition decision gate", html)
        self.assertIn("state-positive", html)
        self.assertIn("state-warning", html)

    def test_generic_runtime_contains_no_waltzman_identifiers(self):
        sources = [
            REPO / "src/world_substrate/living_scene.py",
            REPO / "scripts/render_living_scene.py",
        ]
        forbidden = ("waltzman", "mara", "selene", "validation-capacity", "coalition-hub", "deliver-package")
        for source in sources:
            text = source.read_text().lower()
            for token in forbidden:
                with self.subTest(source=source.name, token=token):
                    self.assertNotIn(token, text)


if __name__ == "__main__":
    unittest.main()
