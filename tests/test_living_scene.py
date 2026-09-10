from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

from world_substrate.living_scene import (
    LIVING_SCENE_SCHEMA_VERSION,
    build_living_scene_frames,
    load_scene_contract,
    normalized_frame_json,
    rebuild_living_scene_frame,
)

spec = importlib.util.spec_from_file_location("legacy_scene_replay", REPO / "scripts/render_scene_replay.py")
legacy_scene = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy_scene)


def living_profile() -> dict:
    return {
        "schema_version": LIVING_SCENE_SCHEMA_VERSION,
        "scene_id": "neutral-lab-v1",
        "world": "neutral-lab",
        "title": "Neutral lab",
        "assets": {},
        "scene": {"animation_ms": 400},
        "zones": {"room": {"label": "Room", "rect": [0, 0, 100, 100], "anchor": [50, 50]}},
        "actors": {
            "actor-a": {
                "home": [20, 50],
                "bindings": {"stance": "components.commitment.stance"},
            }
        },
        "entities": {
            "resource-a": {
                "home": [80, 30],
                "bindings": {
                    "current": "components.resource.current",
                    "required": "components.resource.required",
                },
            }
        },
        "activities": {
            "activity-a": {
                "anchor": [50, 40],
                "bindings": {
                    "status": "components.activity.status",
                    "started_tick": "components.activity.started_tick",
                    "end_tick": "components.activity.end_tick",
                },
            }
        },
        "institutions": {
            "institution-a": {
                "anchor": [50, 75],
                "bindings": {"status": "components.institution.status"},
            }
        },
        "event_visuals": {
            "neutral.resource.drop": {
                "label": "resource changed",
                "operations": [
                    {
                        "op": "event.emphasize",
                        "target": "resource-a",
                        "read_paths": {"current": "components.resource.current"},
                        "animation_ms": 500,
                    }
                ],
            }
        },
        "state_styles": {},
        "presentation": {},
    }


def live_bundle() -> dict:
    entities = {
        "actor-a": {
            "entity_id": "actor-a",
            "components": {"commitment": {"stance": "support"}},
        },
        "resource-a": {
            "entity_id": "resource-a",
            "components": {"resource": {"current": 10, "required": 8}},
        },
        "activity-a": {
            "entity_id": "activity-a",
            "components": {
                "activity": {"status": "pending", "started_tick": None, "end_tick": None}
            },
        },
        "institution-a": {
            "entity_id": "institution-a",
            "components": {"institution": {"status": "ready"}},
        },
    }
    return {
        "schema_version": "world-substrate-live-projection/v0",
        "branch_id": "baseline",
        "world_id": "neutral-lab",
        "initial_snapshot": {
            "schema_version": "world-substrate-snapshot/v1",
            "world": {"world_id": "neutral-lab", "revision": 0, "tick": 0, "entities": entities},
        },
        "events": [
            {
                "event_id": "e1",
                "rule_id": "neutral.resource.drop",
                "status": "accepted",
                "tick": 1,
                "world_revision": 1,
                "changes": [
                    {"path": "revision", "before": 0, "after": 1},
                    {"path": "tick", "before": 0, "after": 1},
                    {
                        "path": "entities.resource-a.components.resource.current",
                        "before": 10,
                        "after": 6,
                    },
                ],
            },
            {
                "event_id": "e2",
                "rule_id": "neutral.activity.start",
                "status": "accepted",
                "tick": 2,
                "world_revision": 2,
                "changes": [
                    {"path": "revision", "before": 1, "after": 2},
                    {"path": "tick", "before": 1, "after": 2},
                    {
                        "path": "entities.activity-a.components.activity.status",
                        "before": "pending",
                        "after": "active",
                    },
                    {
                        "path": "entities.activity-a.components.activity.started_tick",
                        "before": None,
                        "after": 2,
                    },
                    {
                        "path": "entities.activity-a.components.activity.end_tick",
                        "before": None,
                        "after": 4,
                    },
                ],
            },
        ],
    }


def validated_profile(value: dict | None = None) -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "scene.json"
        path.write_text(json.dumps(value or living_profile()))
        return load_scene_contract(path)


class LivingSceneContractTests(unittest.TestCase):
    def test_frozen_neutral_fixture_matches_expected_frames(self):
        root = REPO / "tests/fixtures/living_scene"
        profile = load_scene_contract(root / "neutral-profile-v1.json")
        bundle = json.loads((root / "neutral-projection-v0.json").read_text())
        expected = json.loads((root / "neutral-frames-v1.json").read_text())
        self.assertEqual(build_living_scene_frames(bundle, profile), expected)

    def test_v1_profile_projects_canonical_bindings(self):
        profile = validated_profile()
        frames = build_living_scene_frames(live_bundle(), profile)
        self.assertEqual([frame["boundary_index"] for frame in frames], [-1, 0, 1])
        self.assertEqual(frames[0]["views"]["entities"]["resource-a"]["bindings"]["current"], 10)
        self.assertEqual(frames[1]["views"]["entities"]["resource-a"]["bindings"]["current"], 6)
        self.assertEqual(frames[2]["views"]["activities"]["activity-a"]["bindings"]["status"], "active")

    def test_direct_rebuild_matches_sequential_frames(self):
        profile = validated_profile()
        bundle = live_bundle()
        sequential = build_living_scene_frames(bundle, profile)
        for boundary in (-1, 0, 1):
            with self.subTest(boundary=boundary):
                direct = rebuild_living_scene_frame(bundle, profile, boundary)
                self.assertEqual(normalized_frame_json(direct), normalized_frame_json(sequential[boundary + 1]))

    def test_build_and_rebuild_do_not_mutate_canonical_inputs(self):
        profile = validated_profile()
        bundle = live_bundle()
        original_bundle = deepcopy(bundle)
        original_profile = deepcopy(profile)
        build_living_scene_frames(bundle, profile)
        rebuild_living_scene_frame(bundle, profile, 1)
        self.assertEqual(bundle, original_bundle)
        self.assertEqual(profile, original_profile)

    def test_unknown_event_has_neutral_visual_and_no_guessed_effect(self):
        profile = validated_profile()
        frames = build_living_scene_frames(live_bundle(), profile)
        self.assertEqual(frames[2]["event_visual"], {
            "kind": "generic_event",
            "rule_id": "neutral.activity.start",
            "operations": [],
        })
        self.assertEqual(frames[2]["views"]["actors"]["actor-a"]["home"], [20.0, 50.0])

    def test_animation_duration_cannot_change_canonical_boundary_state(self):
        fast = living_profile()
        slow = living_profile()
        fast["event_visuals"]["neutral.resource.drop"]["operations"][0]["animation_ms"] = 1
        slow["event_visuals"]["neutral.resource.drop"]["operations"][0]["animation_ms"] = 100000
        bundle = live_bundle()
        fast_frame = rebuild_living_scene_frame(bundle, validated_profile(fast), 0)
        slow_frame = rebuild_living_scene_frame(bundle, validated_profile(slow), 0)
        self.assertEqual(fast_frame["tick"], slow_frame["tick"])
        self.assertEqual(fast_frame["revision"], slow_frame["revision"])
        self.assertEqual(fast_frame["views"], slow_frame["views"])

    def test_invalid_or_authority_bearing_profile_fields_fail_loud(self):
        cases = []
        unsupported = living_profile()
        unsupported["schema_version"] = "world-substrate-living-scene/v2"
        cases.append((unsupported, "unsupported scene contract schema"))
        unknown = living_profile()
        unknown["canonical_state"] = {}
        cases.append((unknown, "unknown fields"))
        bad_point = living_profile()
        bad_point["actors"]["actor-a"]["home"] = [1]
        cases.append((bad_point, "must be [x, y]"))
        authority = living_profile()
        authority["event_visuals"]["neutral.resource.drop"]["operations"][0]["after"] = {"status": "delivered"}
        cases.append((authority, "cannot carry canonical authority fields"))
        for value, message in cases:
            with self.subTest(message=message):
                with tempfile.TemporaryDirectory() as tmp:
                    path = Path(tmp) / "scene.json"
                    path.write_text(json.dumps(value))
                    with self.assertRaisesRegex(ValueError, message.replace("[", r"\[").replace("]", r"\]")):
                        load_scene_contract(path)

    def test_legacy_kitchen_and_castaway_profiles_remain_unchanged_and_renderable(self):
        fixtures = [
            (
                REPO / "reference_worlds/kitchen/scene-profile-v0.json",
                REPO / "evidence/kitchen/full-service-replication-v1-run1.json",
            ),
            (
                REPO / "reference_worlds/castaway/scene-profile-v0.json",
                REPO / "evidence/castaway/scene-profile-portability-v0.json",
            ),
        ]
        for profile_path, trace_path in fixtures:
            with self.subTest(profile=profile_path.name, world=profile_path.parent.name):
                raw = json.loads(profile_path.read_text())
                compatible = load_scene_contract(profile_path)
                self.assertEqual(compatible, raw)
                legacy_profile, world_entities = legacy_scene.load_scene_profile(profile_path)
                trace = legacy_scene.load_trace(trace_path, expected_world=legacy_profile["world"])
                self.assertTrue(legacy_scene.build_frames(trace, legacy_profile, world_entities))

    def test_generic_runtime_contains_no_waltzman_special_cases(self):
        source = (REPO / "src/world_substrate/living_scene.py").read_text().lower()
        source += (REPO / "scripts/render_scene_replay.py").read_text().lower()
        for word in (
            "waltzman", "mara", "selene", "validation-capacity",
            "clinical-staff", "shared-reserve", "safeguard-record",
        ):
            with self.subTest(word=word):
                self.assertNotIn(word, source)


if __name__ == "__main__":
    unittest.main()
