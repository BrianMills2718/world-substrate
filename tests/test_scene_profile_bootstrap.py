from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

import bootstrap_scene_profile as bootstrap
import render_scene_replay as renderer

CATALOG = json.loads((REPO / "reference_worlds/scene-asset-catalog-v0.json").read_text())

FIXTURES = {
    "kitchen": {
        "model": REPO / "reference_worlds/kitchen/service-v0.json",
        "trace": REPO / "evidence/kitchen/full-service-replication-v1-run1.json",
        "profile": REPO / "reference_worlds/kitchen/scene-profile-v0.json",
        "review": REPO / "reference_worlds/kitchen/scene-review-v0.json",
        "model_ref": "service-v0.json",
    },
    "castaway": {
        "model": REPO / "reference_worlds/castaway/freshwater-v0.json",
        "trace": REPO / "evidence/castaway/scene-profile-portability-v0.json",
        "profile": REPO / "reference_worlds/castaway/scene-profile-v0.json",
        "review": REPO / "reference_worlds/castaway/scene-review-v0.json",
        "model_ref": "freshwater-v0.json",
    },
}


def load(path: Path):
    return json.loads(path.read_text())


def catalog_without_kitchen_action_bindings():
    catalog = json.loads(json.dumps(CATALOG))
    bindings = catalog.get("action_visual_bindings") or {}
    for kind in ("take", "put_down", "chop", "cook", "plate"):
        bindings.pop(kind, None)
    return catalog


class BootstrapOnlyInfersReviewableFacts(unittest.TestCase):
    def profile(self, world: str):
        f = FIXTURES[world]
        return bootstrap.bootstrap_profile(
            load(f["model"]), load(f["trace"]), CATALOG,
            world_model_ref=f["model_ref"],
        )

    def test_kitchen_identity_assets_stations_and_action_fields_are_inferred(self):
        p = self.profile("kitchen")
        self.assertEqual(set(p["actors"]), {"ama", "bo"})
        self.assertEqual(set(p["entities"]), {"knife", "carrot-1", "potato-1", "onion-1", "onion-2"})
        self.assertEqual(set(p["stations"]), {"burner-1", "burner-2", "order-stew", "order-hash"})
        self.assertEqual(p["stations"]["order-stew"]["progress_actor"], "ama")
        self.assertEqual(p["bootstrap"]["inferred_action_fields"]["cook"], {"item_field": "item", "station_field": "burner"})
        self.assertEqual(p["bootstrap"]["inferred_action_fields"]["plate"], {"item_field": "item", "station_field": "order"})

    def test_castaway_recovers_initial_actor_ownership_and_different_action_shape(self):
        p = self.profile("castaway")
        self.assertEqual(p["bootstrap"]["inferred_initial_owners"], {"cup-robinson": "robinson"})
        self.assertEqual(set(p["stations"]), {"unsafe-pool", "fire-camp"})
        self.assertEqual(set(p["entities"]), {"clay-pot", "cup-robinson"})
        self.assertEqual(p["bootstrap"]["inferred_action_fields"]["fill"], {"item_field": "vessel", "station_field": "source"})
        self.assertEqual(p["bootstrap"]["inferred_action_fields"]["drink"], {"item_field": "vessel", "station_field": None})



    def test_action_names_do_not_create_projection_without_explicit_binding(self):
        f = FIXTURES["kitchen"]
        trace = load(f["trace"])
        # Rename a real action to a lexical lookalike that the catalog never declared.
        trace["transcript"][0]["actors"]["ama"]["did"]["kind"] = "pick_up_like"
        catalog = json.loads(json.dumps(CATALOG))
        p = bootstrap.bootstrap_profile(
            load(f["model"]), trace, catalog, world_model_ref=f["model_ref"], auto_layout=True
        )
        todos = {todo["target"] for todo in p["bootstrap"]["todos"] if todo["kind"] == "action_projection"}
        self.assertIn("action_visuals.pick_up_like", todos)
        self.assertNotIn("pick_up_like", p["bootstrap"]["declared_action_bindings"])

    def test_catalog_binding_with_missing_placeholder_stays_unresolved(self):
        f = FIXTURES["castaway"]
        catalog = json.loads(json.dumps(CATALOG))
        catalog.setdefault("action_visual_bindings", {})["drink"] = {
            "complete": True,
            "projection": {"item_target": {"action_field": "$station_field"}},
        }
        p = bootstrap.bootstrap_profile(
            load(f["model"]), load(f["trace"]), catalog, world_model_ref=f["model_ref"], auto_layout=True
        )
        self.assertIn("drink", p["bootstrap"]["binding_resolution_errors"])
        self.assertNotIn("drink", p["bootstrap"]["declared_action_bindings"])
        self.assertTrue(any(todo["target"] == "action_visuals.drink" for todo in p["bootstrap"]["todos"]))

    def test_auto_layout_proposes_geometry_but_not_action_semantics(self):
        f = FIXTURES["kitchen"]
        p = bootstrap.bootstrap_profile(
            load(f["model"]), load(f["trace"]), catalog_without_kitchen_action_bindings(),
            world_model_ref=f["model_ref"], auto_layout=True,
        )
        self.assertIsInstance(p["actors"]["ama"].get("home"), list)
        self.assertIsInstance(p["stations"]["burner-1"].get("rect"), list)
        self.assertIsInstance(p["entities"]["knife"].get("home"), list)
        kinds = {todo["kind"] for todo in p["bootstrap"]["todos"]}
        self.assertNotIn("geometry", kinds)
        self.assertIn("action_projection", kinds)
        self.assertTrue(p["bootstrap"]["auto_layout"]["enabled"])
        self.assertIn("actors.ama.home", p["bootstrap"]["auto_layout"]["proposed_geometry"])


    def test_reviewed_action_projection_supersedes_catalog_default(self):
        f = FIXTURES["castaway"]
        p = bootstrap.bootstrap_profile(
            load(f["model"]), load(f["trace"]), CATALOG,
            world_model_ref=f["model_ref"], review=load(f["review"]),
        )
        self.assertEqual(p["action_visuals"]["drink"]["actor_target"], {"station": "pot-area"})
        self.assertNotIn("entity_field", p["action_visuals"]["drink"]["actor_target"])
        self.assertEqual(p["bootstrap"]["declared_action_bindings"], [])

    def test_review_geometry_overrides_auto_layout(self):
        f = FIXTURES["kitchen"]
        p = bootstrap.bootstrap_profile(
            load(f["model"]), load(f["trace"]), CATALOG,
            world_model_ref=f["model_ref"],
            review={"actors": {"ama": {"home": [7, 9]}}},
            auto_layout=True,
        )
        self.assertEqual(p["actors"]["ama"]["home"], [7, 9])
        self.assertNotIn("actors.ama.home", p["bootstrap"]["auto_layout"]["proposed_geometry"])

    def test_unreviewed_bootstrap_does_not_invent_geometry_or_motion(self):
        f = FIXTURES["kitchen"]
        p = bootstrap.bootstrap_profile(
            load(f["model"]), load(f["trace"]), catalog_without_kitchen_action_bindings(),
            world_model_ref=f["model_ref"],
        )
        self.assertNotIn("home", p["actors"]["ama"])
        self.assertNotIn("rect", p["stations"]["burner-1"])
        self.assertNotIn("home", p["entities"]["knife"])
        kinds = {todo["kind"] for todo in p["bootstrap"]["todos"]}
        self.assertIn("geometry", kinds)
        self.assertIn("action_projection", kinds)
        self.assertFalse(bootstrap.is_complete(p))


class ReviewedBootstrapCompilesToCurrentProfiles(unittest.TestCase):
    def test_reviewed_profiles_reproduce_current_profiles_and_pass_existing_loader(self):
        for world, f in FIXTURES.items():
            with self.subTest(world=world):
                p = bootstrap.bootstrap_profile(
                    load(f["model"]), load(f["trace"]), CATALOG,
                    world_model_ref=f["model_ref"], review=load(f["review"]),
                )
                self.assertTrue(bootstrap.is_complete(p))
                core = {k: v for k, v in p.items() if k != "bootstrap"}
                self.assertEqual(core, load(f["profile"]))
                with tempfile.NamedTemporaryFile("w", suffix=".json", dir=f["profile"].parent, delete=False) as handle:
                    temp = Path(handle.name)
                    handle.write(json.dumps(p))
                try:
                    loaded, world_entities = renderer.load_scene_profile(temp)
                    self.assertEqual(loaded["world"], world)
                    self.assertTrue(world_entities)
                finally:
                    temp.unlink(missing_ok=True)

    def test_review_overlays_materially_reduce_per_world_profile_authoring(self):
        for world, f in FIXTURES.items():
            with self.subTest(world=world):
                profile_size = len(json.dumps(load(f["profile"]), separators=(",", ":")))
                review_size = len(json.dumps(load(f["review"]), separators=(",", ":")))
                self.assertLess(review_size / profile_size, 0.70)


if __name__ == "__main__":
    unittest.main()
