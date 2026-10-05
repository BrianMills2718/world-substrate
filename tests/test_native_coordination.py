from __future__ import annotations

import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from scripts.run_native_coordination import (
    evaluate_acceptance,
    load_acceptance,
    run_diagnostic,
    run_native_coordination,
)
from scripts.scaffold_world import load_bundle
from world_substrate.information import information_visible_in_material_world
from world_substrate.living_scene import load_scene_contract

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
        cls.causal = json.loads(CAUSAL.read_text())
        cls.acceptance = load_acceptance()
        cls.bundles = {name: load_bundle(path) for name, path in FIXTURES.items()}
        cls.results = {
            name: run_native_coordination(bundle, cls.causal)
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

    def test_executable_acceptance_matrix_passes_for_both_worlds(self):
        for name, result in self.results.items():
            with self.subTest(name=name):
                evaluated = evaluate_acceptance(
                    self.bundles[name], result, self.acceptance
                )
                self.assertTrue(evaluated["passed"], evaluated["failed_check_ids"])
                self.assertEqual(evaluated["failed_check_ids"], [])
                self.assertTrue(evaluated["checks"])
                self.assertTrue(
                    {
                        "input",
                        "compiler",
                        "mechanic_check",
                        "authority",
                        "engine",
                        "information_visibility",
                        "projection",
                        "renderer",
                    }
                    .issubset({row["category"] for row in evaluated["checks"]})
                )

    def test_diagnostic_bundle_retains_exact_artifacts_and_hash_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "diagnostic"
            summary = run_diagnostic(
                self.bundles["distributed"],
                self.causal,
                acceptance=self.acceptance,
                output_dir=output,
                run_id="test/native-coordination/distributed",
            )
            self.assertEqual(summary["status"], "passed")
            required = {
                "summary.json",
                "input-bundle.json",
                "causal-model.json",
                "acceptance-matrix.json",
                "mechanics-review.json",
                "initial-snapshot.json",
                "commands.json",
                "events.json",
                "trace.json",
                "projection.json",
                "living-profile.json",
                "living-frames.json",
                "render.html",
                "acceptance.json",
                "manifest.json",
            }
            self.assertTrue(required.issubset({path.name for path in output.iterdir()}))
            manifest = json.loads((output / "manifest.json").read_text())
            self.assertEqual(
                manifest["schema_version"],
                "world-substrate-native-coordination-diagnostic-manifest/v0",
            )
            self.assertEqual(
                manifest["run_id"], "test/native-coordination/distributed"
            )
            for name, row in manifest["artifacts"].items():
                self.assertEqual(
                    hashlib.sha256((output / name).read_bytes()).hexdigest(),
                    row["sha256"],
                )
            retained_profile = json.loads((output / "living-profile.json").read_text())
            self.assertEqual(
                load_scene_contract(output / "living-profile.json"),
                retained_profile,
            )
            events = json.loads((output / "events.json").read_text())
            blocked = next(
                event for event in events if event["status"] == "precondition_failed"
            )
            self.assertIsNotNone(blocked["observation"])
            self.assertIn(
                "Prerequisite A is healthy",
                {row["label"] for row in blocked["checks"] if not row["ok"]},
            )

    def test_diagnostic_refuses_nonempty_directory_without_discarding_it(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "diagnostic"
            output.mkdir()
            sentinel = output / "keep-me.txt"
            sentinel.write_text("pre-existing evidence\n")
            with self.assertRaises(FileExistsError):
                run_diagnostic(
                    self.bundles["distributed"],
                    self.causal,
                    acceptance=self.acceptance,
                    output_dir=output,
                    run_id="test/native-coordination/refuse-reuse",
                )
            self.assertEqual(sentinel.read_text(), "pre-existing evidence\n")
            self.assertEqual(
                {path.name for path in output.iterdir()},
                {"keep-me.txt"},
            )

    def test_compiler_failure_still_leaves_diagnostic_summary(self):
        broken = json.loads(json.dumps(self.causal))
        broken["mechanics"][0]["effects"][0]["path"] = (
            "components.information.nonexistent"
        )
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "diagnostic"
            summary = run_diagnostic(
                self.bundles["distributed"],
                broken,
                acceptance=self.acceptance,
                output_dir=output,
                run_id="test/native-coordination/compiler-failure",
            )
            self.assertEqual(summary["status"], "failed")
            self.assertEqual(summary["stage"], "compiler")
            self.assertEqual(summary["failure_category"], "compiler")
            self.assertEqual(summary["error"]["type"], "ActionDeclarationError")
            self.assertTrue((output / "summary.json").exists())
            self.assertTrue((output / "manifest.json").exists())
            self.assertTrue((output / "input-bundle.json").exists())
            self.assertTrue((output / "causal-model.json").exists())

    def test_each_run_retains_block_then_recovery_with_zero_provider_spend(self):
        for name, result in self.results.items():
            with self.subTest(name=name):
                trace = result["trace"]
                self.assertEqual(trace["cost_usd"], 0.0)
                self.assertTrue(trace["summary"]["terminal_reached"])
                replay = result["engine"].replay()
                self.assertTrue(replay["ok"])
                self.assertTrue(replay["event_match"])

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
            for row in context:
                self.assertTrue(
                    information_visible_in_material_world(
                        blocked["observation"], actor, row["info_id"]
                    )
                )

    def test_automatic_living_ui_exposes_state_timeline_and_inspection(self):
        for name, result in self.results.items():
            with self.subTest(name=name):
                profile = result["profile"]
                self.assertEqual(profile["schema_version"], "world-substrate-living-scene/v1")
                self.assertEqual(profile["title"], self.bundles[name]["world"]["label"])
                self.assertEqual(profile["activities"], {})
                self.assertIn("coordination.action.communicate", profile["event_visuals"])

                html = result["html"]
                self.assertIn(self.bundles[name]["world"]["label"], html)
                self.assertIn("id='inspector'", html)
                self.assertIn("id='scrub'", html)
                self.assertIn("Represented deliveries", html)
                for member in _component_rows(self.bundles[name], "member"):
                    self.assertIn(member["label"], html)
                for resource in _component_rows(self.bundles[name], "resource"):
                    self.assertIn(resource["label"], html)

                final = result["frames"][-1]
                gate = _component_rows(self.bundles[name], "gate")[0]
                gate_view = final["views"]["institutions"][gate["id"]]["bindings"]
                self.assertEqual(gate_view["status"], "ready")
                self.assertGreaterEqual(gate_view["support"], gate_view["required"])

                resource = _component_rows(self.bundles[name], "resource")[0]
                resource_view = final["views"]["entities"][resource["id"]]["bindings"]
                self.assertIn("current", resource_view)
                self.assertIn("required", resource_view)

    def test_living_ui_projects_information_movement_and_rule_checks(self):
        for name, result in self.results.items():
            with self.subTest(name=name):
                transmissions = [
                    effect
                    for frame in result["frames"]
                    for effect in frame.get("presentation_effects", [])
                    if effect.get("kind") == "information_transmission"
                ]
                self.assertTrue(transmissions)
                self.assertTrue(all(effect["content_visible"] is False for effect in transmissions))

                blocked_id = result["trace"]["summary"]["blocked_event_id"]
                blocked_frame = next(
                    frame
                    for frame in result["frames"]
                    if (frame.get("event") or {}).get("event_id") == blocked_id
                )
                feedback = next(
                    effect
                    for effect in blocked_frame["presentation_effects"]
                    if effect.get("kind") == "action_feedback"
                )
                self.assertIn("Prerequisite A is healthy", feedback["reasons"])
                self.assertIn(
                    {"label": "Prerequisite A is healthy", "ok": False},
                    feedback["checks"],
                )
                self.assertTrue(
                    any(check["ok"] is True for check in feedback["checks"]),
                    feedback["checks"],
                )
                self.assertIn(
                    "Base revision is current",
                    {check["label"] for check in feedback["checks"] if check["ok"] is True},
                )


if __name__ == "__main__":
    unittest.main()
