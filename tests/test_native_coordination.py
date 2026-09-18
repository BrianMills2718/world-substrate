from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.run_native_coordination import run_native_coordination
from scripts.scaffold_world import load_bundle
from world_substrate.information import information_visible_in_material_world

REPO = Path(__file__).resolve().parents[1]
FIXTURES = {
    "distributed": REPO / "examples/native_coordination/distributed-approval-v0.json",
    "handoff": REPO / "examples/native_coordination/constrained-handoff-v0.json",
}
CAUSAL = REPO / "examples/native_coordination/coordination-causal-v0.json"


def _component_rows(bundle: dict, component: str) -> list[dict]:
    return [
        row
        for row in bundle["entities"]
        if component in (row.get("components") or {})
    ]


class NativeCoordinationVerticalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        causal = json.loads(CAUSAL.read_text())
        cls.bundles = {name: load_bundle(path) for name, path in FIXTURES.items()}
        cls.results = {
            name: run_native_coordination(bundle, causal)
            for name, bundle in cls.bundles.items()
        }

    def test_two_materially_different_configs_share_one_mechanics_profile(self):
        distributed = self.bundles["distributed"]
        handoff = self.bundles["handoff"]
        self.assertEqual(len(_component_rows(distributed, "member")), 6)
        self.assertEqual(len(_component_rows(handoff, "member")), 4)

        distributed_gate = _component_rows(distributed, "gate")[0]["components"]["gate"]
        handoff_gate = _component_rows(handoff, "gate")[0]["components"]["gate"]
        self.assertEqual(distributed_gate["required_approvals"], 4)
        self.assertEqual(handoff_gate["required_approvals"], 2)

        distributed_channels = {
            row["components"]["information"]["channel_id"]
            for row in _component_rows(distributed, "information")
        }
        handoff_channels = {
            row["components"]["information"]["channel_id"]
            for row in _component_rows(handoff, "information")
        }
        self.assertEqual(distributed_channels, {"briefing", "dashboard"})
        self.assertEqual(handoff_channels, {"ops-chat", "radio"})

        self.assertEqual(
            self.results["distributed"]["trace"]["mechanic_profile_id"],
            self.results["handoff"]["trace"]["mechanic_profile_id"],
        )

    def test_each_run_retains_block_then_recovery_with_zero_provider_spend(self):
        for name, result in self.results.items():
            with self.subTest(name=name):
                trace = result["trace"]
                self.assertEqual(trace["cost_usd"], 0.0)
                self.assertTrue(trace["summary"]["terminal_reached"])

                blocked_id = trace["summary"]["blocked_event_id"]
                blocked = next(
                    event
                    for event in result["projection"]["events"]
                    if event["event_id"] == blocked_id
                )
                self.assertEqual(blocked["status"], "precondition_failed")
                failed = {row["label"] for row in blocked["checks"] if not row["ok"]}
                self.assertIn("Prerequisite A is healthy", failed)

                gate = _component_rows(self.bundles[name], "gate")[0]
                final_gate = result["engine"].world.entities[gate["id"]].component("gate")
                self.assertEqual(final_gate.status, "ready")
                self.assertGreaterEqual(final_gate.approval_count, final_gate.required_approvals)

    def test_information_visibility_is_actor_scoped(self):
        for name, result in self.results.items():
            bundle = self.bundles[name]
            final_world = result["projection"]["projection_final"]
            members = [row["id"] for row in _component_rows(bundle, "member")]
            deliveries = {
                row["components"]["delivery"]["info_id"]: row["components"]["delivery"]["recipient_id"]
                for row in _component_rows(bundle, "delivery")
            }
            for info_row in _component_rows(bundle, "information"):
                info_id = info_row["id"]
                source = info_row["components"]["information"]["source_id"]
                recipient = deliveries[info_id]
                outsider = next(
                    actor
                    for actor in members
                    if actor not in {source, recipient}
                )
                with self.subTest(world=name, info=info_id):
                    self.assertTrue(
                        information_visible_in_material_world(final_world, recipient, info_id)
                    )
                    self.assertFalse(
                        information_visible_in_material_world(final_world, outsider, info_id)
                    )

    def test_blocked_approval_retains_only_actor_visible_information_context(self):
        for name, result in self.results.items():
            blocked_id = result["trace"]["summary"]["blocked_event_id"]
            blocked = next(
                event
                for event in result["projection"]["events"]
                if event["event_id"] == blocked_id
            )
            actor = blocked["causal_bearer"]["id"]
            context = blocked.get("information_context", [])
            self.assertTrue(context, name)
            self.assertTrue(all(row["source_id"] != actor or row["info_id"] for row in context))
            for row in context:
                self.assertTrue(
                    information_visible_in_material_world(
                        blocked["observation"], actor, row["info_id"]
                    )
                )

    def test_automatic_ui_renders_without_a_scene_review_overlay(self):
        for name, result in self.results.items():
            with self.subTest(name=name):
                profile = result["profile"]
                self.assertTrue(profile["bootstrap"]["auto_layout"]["enabled"])
                self.assertEqual(profile["bootstrap"]["reviewed_actions"], [])
                self.assertIn("Scene replay", result["html"])
                self.assertIn(self.bundles[name]["world"]["label"], result["html"])
                for member in _component_rows(self.bundles[name], "member"):
                    self.assertIn(member["label"], result["html"])


if __name__ == "__main__":
    unittest.main()
