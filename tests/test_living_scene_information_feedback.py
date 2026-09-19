"""Information visibility and action-outcome presentation remain evidence-bound."""

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

from world_substrate.information import information_visible_in_material_world
from world_substrate.living_scene import build_living_scene_frames, load_scene_contract

spec = importlib.util.spec_from_file_location("living_renderer", REPO / "scripts/render_living_scene.py")
living_renderer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(living_renderer)


def profile() -> dict:
    value = json.loads((REPO / "tests/fixtures/living_scene/neutral-render-profile-v1.json").read_text())
    value["world"] = "information-lab"
    value["scene_id"] = "information-lab-v1"
    value["title"] = "Information lab"
    value["event_visuals"] = {
        "neutral.info.deliver": {
            "label": "message delivered",
            "operations": [
                {"op": "information.transmit", "delivery_from_changed_entities": True}
            ],
        },
        "neutral.action.try": {
            "label": "attempt resource transfer",
            "operations": [{"op": "action.feedback", "label": "resource transfer"}],
        },
    }
    return value


def bundle() -> dict:
    base = json.loads((REPO / "tests/fixtures/living_scene/neutral-render-projection-v0.json").read_text())
    world = base["initial_snapshot"]["world"]
    world["world_id"] = "information-lab"
    base["world_id"] = "information-lab"
    entities = world["entities"]
    entities["info-private"] = {
        "entity_id": "info-private",
        "label": "Private message",
        "category_ids": ["information"],
        "components": {
            "information": {
                "content": "Private payload <b>must not become markup</b>",
                "source_id": "actor-a",
                "channel_id": "spoken",
                "visibility": "direct",
                "topic": "coordination",
                "derived_from_info_id": None,
                "active": False,
            }
        },
    }
    entities["delivery-private"] = {
        "entity_id": "delivery-private",
        "label": "Private delivery",
        "category_ids": ["delivery"],
        "components": {
            "delivery": {
                "info_id": "info-private",
                "recipient_id": "actor-b",
                "channel_id": "spoken",
                "status": "pending",
                "delivered_tick": None,
            }
        },
    }
    base["events"] = [
        {
            "event_id": "e-info",
            "rule_id": "neutral.info.deliver",
            "rule_version": "1",
            "status": "accepted",
            "tick": 1,
            "world_revision": 1,
            "observation": {
                "actor_id": "actor-a",
                "private_scratch": "actor-only observation secret",
            },
            "information_context": [{"content": "private cognition context"}],
            "changes": [
                {"path": "revision", "before": 0, "after": 1},
                {"path": "tick", "before": 0, "after": 1},
                {
                    "path": "entities.info-private.components.information.active",
                    "before": False,
                    "after": True,
                },
                {
                    "path": "entities.delivery-private.components.delivery.status",
                    "before": "pending",
                    "after": "delivered",
                },
                {
                    "path": "entities.delivery-private.components.delivery.delivered_tick",
                    "before": None,
                    "after": 1,
                },
            ],
        },
        {
            "event_id": "e-reject",
            "rule_id": "neutral.action.try",
            "rule_version": "1",
            "status": "rejected",
            "tick": 1,
            "world_revision": 1,
            "checks": [
                {"label": "Base revision is current", "ok": True},
                {"label": "Required slot is available", "ok": False},
            ],
            "changes": [],
        },
    ]
    return base


def checked_profile() -> dict:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "profile.json"
        path.write_text(json.dumps(profile()))
        return load_scene_contract(path)


class LivingSceneInformationFeedbackTests(unittest.TestCase):
    def test_material_visibility_matches_direct_delivery_semantics(self):
        value = bundle()
        before = value["initial_snapshot"]["world"]
        self.assertTrue(information_visible_in_material_world(before, "actor-a", "info-private"))
        self.assertFalse(information_visible_in_material_world(before, "actor-b", "info-private"))
        delivered = deepcopy(before)
        for change in value["events"][0]["changes"]:
            from world_substrate.projection import apply_changes
            apply_changes(delivered, [change])
        self.assertTrue(information_visible_in_material_world(delivered, "actor-b", "info-private"))
        self.assertFalse(information_visible_in_material_world(delivered, "actor-c", "info-private"))

    def test_transmission_appears_only_after_canonical_delivery(self):
        frames = build_living_scene_frames(bundle(), checked_profile())
        self.assertEqual(frames[0]["presentation_effects"], [])
        effects = frames[1]["presentation_effects"]
        self.assertEqual(len(effects), 1)
        self.assertEqual(effects[0]["kind"], "information_transmission")
        self.assertEqual(effects[0]["source_id"], "actor-a")
        self.assertEqual(effects[0]["recipient_id"], "actor-b")
        self.assertFalse(effects[0]["content_visible"])
        self.assertIsNone(effects[0]["content"])

    def test_authorized_observer_sees_content_and_unauthorized_observer_does_not(self):
        value = bundle()
        cfg = checked_profile()
        recipient = build_living_scene_frames(value, cfg, observer_actor_id="actor-b")[1]
        outsider = build_living_scene_frames(value, cfg, observer_actor_id="actor-c")[1]
        self.assertTrue(recipient["presentation_effects"][0]["content_visible"])
        self.assertIn("Private payload", recipient["presentation_effects"][0]["content"])
        self.assertFalse(outsider["presentation_effects"][0]["content_visible"])
        self.assertIsNone(outsider["presentation_effects"][0]["content"])

    def test_public_scene_payload_does_not_embed_actor_scoped_observation_or_private_content(self):
        value = bundle()
        cfg = checked_profile()
        frame = build_living_scene_frames(value, cfg)[1]
        encoded = json.dumps(frame, sort_keys=True)
        self.assertNotIn("actor-only observation secret", encoded)
        self.assertNotIn("private cognition context", encoded)
        self.assertNotIn("Private payload", encoded)
        public_html = living_renderer.render_html(value, cfg, REPO / "tests/fixtures/living_scene")
        self.assertNotIn("actor-only observation secret", public_html)
        self.assertNotIn("private cognition context", public_html)
        self.assertNotIn("Private payload", public_html)
        recipient_html = living_renderer.render_html(
            value, cfg, REPO / "tests/fixtures/living_scene", observer_actor_id="actor-b"
        )
        self.assertIn("Private payload", recipient_html)
        self.assertNotIn("innerHTML='<strong>'+effect.source_id", recipient_html)

    def test_information_context_does_not_become_causal_parentage(self):
        value = bundle()
        value["events"][0]["information_context"] = [{"content": "context only"}]
        value["events"][0].pop("causal_parent_event_ids", None)
        frame = build_living_scene_frames(value, checked_profile(), observer_actor_id="actor-b")[1]
        self.assertNotIn("causal_parent_event_ids", frame["event"])
        transmission = frame["presentation_effects"][0]
        self.assertNotIn("causal_parent_event_ids", transmission)
        self.assertNotIn("information_context", transmission)

    def test_rejected_action_feedback_uses_retained_failed_check_label(self):
        frame = build_living_scene_frames(bundle(), checked_profile())[2]
        self.assertEqual(frame["presentation_effects"], [{
            "kind": "action_feedback",
            "status": "rejected",
            "label": "resource transfer",
            "reasons": ["Required slot is available"],
        }])

    def test_feedback_supports_retained_statuses_without_generating_reasons(self):
        cfg = checked_profile()
        for status in (
            "accepted",
            "rejected",
            "refused",
            "blocked",
            "precondition_failed",
            "stale_revision",
            "invalid_action",
            "unsupported_action",
            "scope_violation",
        ):
            value = bundle()
            value["events"] = [{
                "event_id": f"e-{status}",
                "rule_id": "neutral.action.try",
                "status": status,
                "tick": 0,
                "world_revision": 0,
                "checks": [],
                "changes": [],
            }]
            frame = build_living_scene_frames(value, cfg)[1]
            effect = frame["presentation_effects"][0]
            self.assertEqual(effect["status"], status)
            self.assertEqual(effect["reasons"], [])

    def test_feedback_degrades_unknown_status_to_unknown(self):
        value = bundle()
        value["events"] = [{
            "event_id": "e-future-status",
            "rule_id": "neutral.action.try",
            "status": "future_unrecognized_status",
            "tick": 0,
            "world_revision": 0,
            "checks": [],
            "changes": [],
        }]
        frame = build_living_scene_frames(value, checked_profile())[1]
        effect = frame["presentation_effects"][0]
        self.assertEqual(effect["status"], "unknown")
        self.assertEqual(effect["reasons"], [])

    def test_scrubbing_rebuild_has_no_stale_transmission_or_feedback(self):
        value = bundle()
        cfg = checked_profile()
        frames = build_living_scene_frames(value, cfg, observer_actor_id="actor-b")
        self.assertEqual(frames[0]["presentation_effects"], [])
        self.assertEqual(frames[1]["presentation_effects"][0]["kind"], "information_transmission")
        self.assertEqual(frames[2]["presentation_effects"][0]["kind"], "action_feedback")


if __name__ == "__main__":
    unittest.main()
