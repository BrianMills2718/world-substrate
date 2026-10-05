from __future__ import annotations

import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import scripts.native_coordination_authoring as coordination
import scripts.world_builder_service as service
from world_substrate.action_authoring import CausalModel

REPO = Path(__file__).resolve().parents[1]
BUNDLE = json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text())
CAUSAL = json.loads((REPO / "examples/world_authoring/orchard-causal-v0.json").read_text())
DRAFT = json.loads((REPO / "examples/native_coordination/one-shot-draft-v0.json").read_text())
DRAFT_BUNDLE = coordination.draft_to_bundle(DRAFT)
DRAFT_REVIEW = coordination.draft_review(DRAFT)


class FakeResult:
    model = "fake-model"
    cost = 0.001


class WorldBuilderServiceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), service.WorldBuilderHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}/world-builder/api"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def setUp(self):
        service._REQUESTS.clear()
        service._LLM_REQUESTS.clear()
        service._DIALOGUE_REQUESTS.clear()
        self.state_tmp = tempfile.TemporaryDirectory()
        self.budget_path = Path(self.state_tmp.name) / "budget.json"
        self.path_patch = patch.object(service, "BUDGET_STATE_PATH", self.budget_path)
        self.path_patch.start()

    def tearDown(self):
        self.path_patch.stop()
        self.state_tmp.cleanup()

    def write_budget(self, *, spent: float = 0.0, reserved: float = 0.0, day: str | None = None):
        self.budget_path.write_text(json.dumps({
            "schema_version": service.BUDGET_STATE_SCHEMA,
            "date": day or service.date.today().isoformat(),
            "spent_usd": spent,
            "reserved_usd": reserved,
        }))

    def post(self, path: str, body: dict, *, origin: str | None = None, extra_headers: dict[str, str] | None = None):
        headers = {"Content-Type": "application/json"}
        if origin is not None:
            headers["Origin"] = origin
        headers.update(extra_headers or {})
        request = urllib.request.Request(
            self.base + path,
            data=json.dumps(body).encode(),
            headers=headers,
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=5) as response:
                return response.status, json.loads(response.read())
        except urllib.error.HTTPError as error:
            return error.code, json.loads(error.read())

    def test_health_reports_build_commit_and_persistent_budget(self):
        self.write_budget(spent=0.125)
        with patch.dict(service.os.environ, {"WORLD_SUBSTRATE_BUILD_COMMIT": "abc123"}):
            with urllib.request.urlopen(self.base + "/health", timeout=5) as response:
                payload = json.loads(response.read())
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["build_commit"], "abc123")
        self.assertEqual(payload["llm_daily_committed_usd"], 0.125)

    def test_generate_draft_returns_editable_bundle_and_explicit_review(self):
        with patch.object(service, "_trace_cost", return_value=0.002), patch.object(
            service,
            "generate_native_coordination_draft",
            return_value=(DRAFT, DRAFT_BUNDLE, DRAFT_REVIEW, FakeResult()),
        ) as generate:
            status, payload = self.post(
                "/generate-draft",
                {"description": DRAFT["source_description"]},
            )
        self.assertEqual(status, 200)
        self.assertEqual(payload["draft"]["schema_version"], DRAFT["schema_version"])
        self.assertEqual(payload["bundle"]["world"]["id"], "handoff-review")
        self.assertEqual(
            [row["action_kind"] for row in payload["causal_model"]["mechanics"]],
            ["communicate", "approve", "intervene", "finalize"],
        )
        self.assertTrue(payload["review"]["narrowing_is_explicit"])
        self.assertIn("Use probabilistic delivery delays.", payload["review"]["unsupported_requests"])
        self.assertTrue(payload["trace_id"].startswith(service.TRACE_ROOT + "/draft/"))
        self.assertAlmostEqual(generate.call_args.kwargs["max_budget"], service.DRAFT_BUDGET)
        self.assertAlmostEqual(payload["daily_cost_usd"], 0.002, places=6)

    def test_generate_world_returns_structure_mechanics_and_passing_dry_run(self):
        with patch.object(service, "_trace_cost", return_value=0.004), patch.object(
            service, "generate_world_bundle", return_value=(BUNDLE, ["a deadline"], FakeResult()),
        ) as world, patch.object(
            service, "generate_causal_model", return_value=(CAUSAL, FakeResult()),
        ) as mechanics:
            status, payload = self.post("/generate-world", {"description": "One worker picks a ripe apple."})
        self.assertEqual(status, 200, payload)
        self.assertEqual(payload["bundle"]["world"]["id"], "orchard")
        self.assertEqual([m["action_kind"] for m in payload["review"]["mechanics"]], ["pick"])
        self.assertTrue(payload["dry_run"]["ok"])
        self.assertGreater(payload["dry_run"]["accepted_actions"], 0)
        self.assertEqual(payload["not_modeled"], ["a deadline"])
        self.assertEqual(mechanics.call_count, 1)
        self.assertTrue(payload["trace_id"].startswith(service.TRACE_ROOT + "/world/"))
        self.assertAlmostEqual(world.call_args.kwargs["max_budget"], service.WORLD_BUDGET)
        self.assertAlmostEqual(payload["daily_cost_usd"], 0.004, places=6)
        # Generation alone never runs a world for real: /run still requires approval.
        status, refused = self.post("/run", {"bundle": payload["bundle"], "causal_model": payload["causal_model"]})
        self.assertEqual(status, 409)

    def test_generate_world_retries_mechanics_once_when_dry_run_has_no_actions(self):
        impossible = json.loads(json.dumps(CAUSAL))
        impossible["mechanics"][0]["checks"].append(
            {"label": "Fruit is rotten", "left": {"participant": {"name": "fruit", "path": "components.fruit.stage"}},
             "op": "eq", "right": {"literal": "rotten"}}
        )
        with patch.object(service, "_trace_cost", return_value=0.006), patch.object(
            service, "generate_world_bundle", return_value=(BUNDLE, ["a deadline"], FakeResult()),
        ), patch.object(
            service, "generate_causal_model", side_effect=[(impossible, FakeResult()), (CAUSAL, FakeResult())],
        ) as mechanics:
            status, payload = self.post("/generate-world", {"description": "One worker picks a ripe apple."})
        self.assertEqual(status, 200, payload)
        self.assertEqual(mechanics.call_count, 2)
        self.assertIn("dry run", mechanics.call_args_list[1].kwargs["guidance"])
        self.assertIn("Fruit is rotten", mechanics.call_args_list[1].kwargs["guidance"])
        self.assertEqual([a["ok"] for a in payload["dry_run_attempts"]], [False, True])
        self.assertTrue(payload["dry_run"]["ok"])

    def test_generate_world_retries_when_dry_run_never_finishes_and_keeps_best(self):
        stuck = {"summary": {"turns": 12, "terminal_reached": False, "accepted_actions": 24}}
        done = {"summary": {"turns": 1, "terminal_reached": True, "accepted_actions": 1}}
        with patch.object(service, "_trace_cost", return_value=0.006), patch.object(
            service, "generate_world_bundle", return_value=(BUNDLE, [], FakeResult()),
        ), patch.object(
            service, "generate_causal_model", return_value=(CAUSAL, FakeResult()),
        ) as mechanics, patch.object(
            service, "run_world", side_effect=[(stuck, None, None), (done, None, None)],
        ):
            status, payload = self.post("/generate-world", {"description": "orchard"})
        self.assertEqual(status, 200, payload)
        self.assertEqual(mechanics.call_count, 2)
        self.assertIn("never reached the terminal", mechanics.call_args_list[1].kwargs["guidance"])
        self.assertEqual(mechanics.call_args_list[0].kwargs["model"], service.DEFAULT_MODEL)
        self.assertIsNone(mechanics.call_args_list[0].kwargs["model_justification"])
        self.assertEqual(mechanics.call_args_list[1].kwargs["model"], service.RULES_RETRY_MODEL)
        self.assertTrue(mechanics.call_args_list[1].kwargs["model_justification"])
        self.assertTrue(payload["dry_run"]["terminal_reached"])

    def test_generate_world_keeps_first_attempt_when_retry_is_worse(self):
        stuck = {"summary": {"turns": 12, "terminal_reached": False, "accepted_actions": 24}}
        with patch.object(service, "_trace_cost", return_value=0.006), patch.object(
            service, "generate_world_bundle", return_value=(BUNDLE, [], FakeResult()),
        ), patch.object(
            service, "generate_causal_model", return_value=(CAUSAL, FakeResult()),
        ), patch.object(
            service, "run_world", side_effect=[(stuck, None, None), ValueError("run produced no actions")],
        ):
            status, payload = self.post("/generate-world", {"description": "orchard"})
        self.assertEqual(status, 200, payload)
        self.assertTrue(payload["dry_run"]["ok"])
        self.assertFalse(payload["dry_run"]["terminal_reached"])
        self.assertEqual([a["ok"] for a in payload["dry_run_attempts"]], [True, False])

    def test_compiler_rejection_goes_to_the_stronger_retry(self):
        with patch.object(service, "_trace_cost", return_value=0.006), patch.object(
            service, "generate_world_bundle", return_value=(BUNDLE, [], FakeResult()),
        ), patch.object(
            service, "generate_causal_model",
            side_effect=[ValueError("causal model selects no actors in this world"), (CAUSAL, FakeResult())],
        ) as mechanics:
            status, payload = self.post("/generate-world", {"description": "orchard"})
        self.assertEqual(status, 200, payload)
        self.assertEqual(mechanics.call_args_list[1].kwargs["model"], service.RULES_RETRY_MODEL)
        self.assertIn("selects no actors", mechanics.call_args_list[1].kwargs["guidance"])
        self.assertEqual([a["ok"] for a in payload["dry_run_attempts"]], [False, True])
        self.assertTrue(payload["dry_run"]["terminal_reached"])

    def test_two_compiler_rejections_fail_with_the_reason(self):
        with patch.object(service, "_trace_cost", return_value=0.006), patch.object(
            service, "generate_world_bundle", return_value=(BUNDLE, [], FakeResult()),
        ), patch.object(
            service, "generate_causal_model", side_effect=ValueError("causal model selects no actors in this world"),
        ):
            status, payload = self.post("/generate-world", {"description": "orchard"})
        self.assertEqual(status, 422)
        self.assertIn("selects no actors", payload["error"])

    def test_generate_world_reports_failed_dry_run_plainly_after_one_retry(self):
        impossible = json.loads(json.dumps(CAUSAL))
        impossible["mechanics"][0]["checks"].append(
            {"label": "Fruit is rotten", "left": {"participant": {"name": "fruit", "path": "components.fruit.stage"}},
             "op": "eq", "right": {"literal": "rotten"}}
        )
        with patch.object(service, "_trace_cost", return_value=0.006), patch.object(
            service, "generate_world_bundle", return_value=(BUNDLE, ["a deadline"], FakeResult()),
        ), patch.object(
            service, "generate_causal_model", return_value=(impossible, FakeResult()),
        ) as mechanics:
            status, payload = self.post("/generate-world", {"description": "One worker picks a ripe apple."})
        self.assertEqual(status, 200, payload)
        self.assertEqual(mechanics.call_count, 2)
        self.assertFalse(payload["dry_run"]["ok"])
        self.assertIn("no actions", payload["dry_run"]["error"])

    def test_failed_generation_charges_recorded_cost_not_whole_reservation(self):
        with patch.object(service, "_trace_cost", return_value=0.004), patch.object(
            service, "generate_world_bundle", side_effect=ValueError("world proposal remained invalid after 2 repairs: x"),
        ):
            status, payload = self.post("/generate-world", {"description": "orchard"})
        self.assertEqual(status, 422)
        self.assertAlmostEqual(service._daily_cost(), 0.004, places=6)

    def test_failed_generation_with_no_recorded_cost_stays_fail_closed(self):
        with patch.object(service, "_trace_cost", return_value=0.0), patch.object(
            service, "generate_world_bundle", side_effect=ValueError("provider failed"),
        ):
            status, _ = self.post("/generate-world", {"description": "orchard"})
        self.assertEqual(status, 422)
        self.assertAlmostEqual(service._daily_cost(), service.WORLD_BUDGET, places=6)

    def test_clarify_returns_one_dialogue_turn_and_charges_the_ledger(self):
        reply = {"reply": "ok", "questions": [{"question": "How many?", "options": ["2", "3"]}],
                 "description": "Ava picks two apples.", "ready": False}
        with patch.object(service, "_trace_cost", return_value=0.001), patch.object(
            service, "clarify", return_value=(reply, FakeResult()),
        ) as call:
            status, payload = self.post("/clarify", {"messages": [{"role": "user", "content": "an orchard"}]})
        self.assertEqual(status, 200, payload)
        self.assertEqual(payload["questions"][0]["options"], ["2", "3"])
        self.assertEqual(payload["description"], "Ava picks two apples.")
        self.assertAlmostEqual(call.call_args.kwargs["max_budget"], service.DIALOGUE_BUDGET)
        self.assertAlmostEqual(payload["daily_cost_usd"], 0.001, places=6)
        self.assertTrue(payload["trace_id"].startswith(service.TRACE_ROOT + "/clarify/"))

    def test_clarify_rejects_a_bad_conversation_before_spend(self):
        with patch.object(service, "clarify") as call:
            status, _ = self.post("/clarify", {"messages": [{"role": "assistant", "content": "hi"}]})
        self.assertEqual(status, 422)
        call.assert_not_called()
        self.assertFalse(self.budget_path.exists())

    def test_dialogue_has_its_own_allowance(self):
        service._LLM_REQUESTS["127.0.0.1"].extend([__import__("time").time()] * service.LLM_REQUESTS_PER_HOUR)
        with patch.object(service, "_trace_cost", return_value=0.001), patch.object(
            service, "surprise_description", return_value=({"theme": "t", "description": "d"}, FakeResult()),
        ):
            status, payload = self.post("/surprise", {})
        self.assertEqual(status, 200, payload)
        self.assertEqual(payload["description"], "d")

    def test_unapproved_model_is_refused_before_spend(self):
        with patch.object(service, "generate_world_bundle") as world:
            status, payload = self.post("/generate-world", {"description": "orchard", "model": "openrouter/some/expensive-model"})
        self.assertEqual(status, 422)
        self.assertIn("model must be", payload["error"])
        world.assert_not_called()
        self.assertFalse(self.budget_path.exists())

    def test_generate_world_rejects_empty_description_before_spend(self):
        with patch.object(service, "generate_world_bundle") as world:
            status, payload = self.post("/generate-world", {"description": "   "})
        self.assertEqual(status, 422)
        world.assert_not_called()
        self.assertFalse(self.budget_path.exists())

    def test_generate_draft_rejects_empty_description_before_spend(self):
        with patch.object(service, "generate_native_coordination_draft") as generate:
            status, payload = self.post("/generate-draft", {"description": "  "})
        self.assertEqual(status, 422)
        self.assertIn("description", payload["error"])
        generate.assert_not_called()
        self.assertFalse(self.budget_path.exists())

    def test_scripted_fresh_run_returns_graphical_replay_without_llm(self):
        status, payload = self.post(
            "/run",
            {
                "bundle": BUNDLE,
                "causal_model": CAUSAL,
                "approved": True,
                "policy": "scripted",
                "turns": 5,
            },
        )
        self.assertEqual(status, 200)
        self.assertTrue(payload["summary"]["terminal_reached"])
        self.assertEqual(payload["cost_usd"], 0.0)
        self.assertIn("Scene replay", payload["replay_html"])

    def test_native_coordination_run_uses_native_runner_and_living_scene(self):
        shared = json.loads(coordination.DEFAULT_CAUSAL.read_text())
        compiled = CausalModel.from_dict(shared, bundle=DRAFT_BUNDLE)
        fake_trace = {
            "schema_version": "world-substrate-contested-run/v3",
            "summary": {
                "turns": 7,
                "terminal_reached": True,
                "accepted_actions": 6,
                "blocked_event_id": "e0003",
            },
            "cost_usd": 0.0,
        }
        with patch.object(
            service,
            "run_native_coordination",
            return_value={
                "trace": fake_trace,
                "causal_model": compiled,
                "html": "<html>Living Scene native coordination</html>",
            },
        ) as run_native:
            status, payload = self.post(
                "/run",
                {
                    "bundle": DRAFT_BUNDLE,
                    "causal_model": shared,
                    "approved": True,
                    "execution_mode": "native_coordination",
                    "policy": "scripted",
                },
            )
        self.assertEqual(status, 200)
        self.assertEqual(payload["execution_mode"], "native_coordination")
        self.assertEqual(payload["cost_usd"], 0.0)
        self.assertIn("Living Scene native coordination", payload["replay_html"])
        run_native.assert_called_once()

    def test_native_coordination_run_refuses_modified_law(self):
        shared = json.loads(coordination.DEFAULT_CAUSAL.read_text())
        modified = json.loads(json.dumps(shared))
        modified["mechanics"][0]["rationale"] += " Modified."
        with patch.object(service, "run_native_coordination") as run_native:
            status, payload = self.post(
                "/run",
                {
                    "bundle": DRAFT_BUNDLE,
                    "causal_model": modified,
                    "approved": True,
                    "execution_mode": "native_coordination",
                    "policy": "scripted",
                },
            )
        self.assertEqual(status, 422)
        self.assertIn("shared coordination mechanics", payload["error"])
        run_native.assert_not_called()

    def test_native_comparison_endpoint_changes_one_condition_and_runs_native(self):
        shared = json.loads(coordination.DEFAULT_CAUSAL.read_text())
        comparison_bundle = json.loads(json.dumps(DRAFT_BUNDLE))
        gate = next(row for row in comparison_bundle["entities"] if "gate" in row["categories"])
        gate["components"]["gate"]["required_approvals"] = 1
        compiled = CausalModel.from_dict(shared, bundle=comparison_bundle)
        fake_trace = {
            "schema_version": "world-substrate-contested-run/v3",
            "summary": {
                "turns": 6,
                "terminal_reached": True,
                "accepted_actions": 5,
                "blocked_event_id": "e0003",
            },
            "cost_usd": 0.0,
        }
        with patch.object(
            service,
            "run_native_coordination",
            return_value={
                "trace": fake_trace,
                "causal_model": compiled,
                "html": "<html>Comparison Living Scene</html>",
            },
        ) as run_native:
            status, payload = self.post(
                "/compare-native-coordination",
                {
                    "baseline_bundle": DRAFT_BUNDLE,
                    "causal_model": shared,
                    "approved": True,
                    "required_approvals": 1,
                },
            )
        self.assertEqual(status, 200)
        self.assertEqual(payload["execution_mode"], "native_coordination_comparison")
        self.assertEqual(payload["change"]["before"], 2)
        self.assertEqual(payload["change"]["after"], 1)
        self.assertEqual(payload["cost_usd"], 0.0)
        self.assertIn("Comparison Living Scene", payload["replay_html"])
        returned_gate = next(
            row for row in payload["comparison_bundle"]["entities"]
            if "gate" in row["categories"]
        )
        self.assertEqual(returned_gate["components"]["gate"]["required_approvals"], 1)
        run_native.assert_called_once()

    def test_native_comparison_requires_explicit_mechanics_approval(self):
        shared = json.loads(coordination.DEFAULT_CAUSAL.read_text())
        with patch.object(service, "run_native_coordination") as run_native:
            status, payload = self.post(
                "/compare-native-coordination",
                {
                    "baseline_bundle": DRAFT_BUNDLE,
                    "causal_model": shared,
                    "required_approvals": 1,
                },
            )
        self.assertEqual(status, 409)
        self.assertIn("approved", payload["error"])
        run_native.assert_not_called()

    def test_native_comparison_refuses_modified_law(self):
        shared = json.loads(coordination.DEFAULT_CAUSAL.read_text())
        modified = json.loads(json.dumps(shared))
        modified["mechanics"][0]["rationale"] += " Modified."
        with patch.object(service, "run_native_coordination") as run_native:
            status, payload = self.post(
                "/compare-native-coordination",
                {
                    "baseline_bundle": DRAFT_BUNDLE,
                    "causal_model": modified,
                    "approved": True,
                    "required_approvals": 1,
                },
            )
        self.assertEqual(status, 422)
        self.assertIn("shared coordination mechanics", payload["error"])
        run_native.assert_not_called()

    def test_run_requires_explicit_mechanic_approval(self):
        status, payload = self.post(
            "/run",
            {"bundle": BUNDLE, "causal_model": CAUSAL, "policy": "scripted"},
        )
        self.assertEqual(status, 409)
        self.assertIn("approved", payload["error"])

    def test_public_post_requires_same_origin(self):
        status, _ = self.post(
            "/run",
            {"bundle": BUNDLE, "causal_model": CAUSAL, "approved": True},
            origin="https://attacker.example",
        )
        self.assertEqual(status, 403)

    def test_forwarded_public_request_without_origin_is_rejected(self):
        status, _ = self.post(
            "/run",
            {"bundle": BUNDLE, "causal_model": CAUSAL, "approved": True},
            extra_headers={"CF-Connecting-IP": "203.0.113.4"},
        )
        self.assertEqual(status, 403)

    def test_daily_budget_caps_next_llm_request_instead_of_overshooting(self):
        fake_generated = json.loads(json.dumps(CAUSAL))
        self.write_budget(spent=0.49)
        with patch.object(service, "_trace_cost", return_value=0.001), patch.object(
            service, "generate_causal_model", return_value=(fake_generated, FakeResult())
        ) as generate:
            status, payload = self.post("/generate-mechanics", {"bundle": BUNDLE})
        self.assertEqual(status, 200)
        self.assertAlmostEqual(generate.call_args.kwargs["max_budget"], 0.01, places=6)
        self.assertAlmostEqual(payload["daily_cost_usd"], 0.491, places=6)
        state = json.loads(self.budget_path.read_text())
        self.assertAlmostEqual(state["spent_usd"], 0.491, places=6)
        self.assertEqual(state["reserved_usd"], 0.0)

    def test_generate_endpoint_returns_compiler_review_not_unchecked_model_output(self):
        fake_generated = json.loads(json.dumps(CAUSAL))
        with patch.object(service, "_trace_cost", return_value=0.001), patch.object(
            service,
            "generate_causal_model",
            return_value=(fake_generated, FakeResult()),
        ):
            status, payload = self.post("/generate-mechanics", {"bundle": BUNDLE})
        self.assertEqual(status, 200)
        self.assertEqual(payload["causal_model"]["schema_version"], "world-substrate-causal-model/v0")
        self.assertIn("writes", payload["review"]["mechanics"][0])
        self.assertEqual(payload["model"], "fake-model")
        self.assertTrue(payload["trace_id"].startswith(service.TRACE_ROOT + "/mechanics/"))
        self.assertAlmostEqual(payload["daily_cost_usd"], 0.001, places=6)

    def test_failed_draft_request_charges_full_reservation_and_clears_reserved(self):
        with patch.object(
            service,
            "generate_native_coordination_draft",
            side_effect=RuntimeError("provider failed"),
        ):
            status, _ = self.post(
                "/generate-draft", {"description": DRAFT["source_description"]}
            )
        self.assertEqual(status, 500)
        state = json.loads(self.budget_path.read_text())
        self.assertAlmostEqual(state["spent_usd"], service.DRAFT_BUDGET, places=6)
        self.assertEqual(state["reserved_usd"], 0.0)

    def test_failed_llm_request_charges_full_reservation_and_clears_reserved(self):
        with patch.object(service, "generate_causal_model", side_effect=RuntimeError("provider failed")):
            status, _ = self.post("/generate-mechanics", {"bundle": BUNDLE})
        self.assertEqual(status, 500)
        state = json.loads(self.budget_path.read_text())
        self.assertAlmostEqual(state["spent_usd"], service.MECHANICS_BUDGET, places=6)
        self.assertEqual(state["reserved_usd"], 0.0)

    def test_persisted_reservation_reduces_next_available_budget_after_restart(self):
        fake_generated = json.loads(json.dumps(CAUSAL))
        self.write_budget(spent=0.03, reserved=0.45)
        with patch.object(service, "_trace_cost", return_value=0.001), patch.object(
            service, "generate_causal_model", return_value=(fake_generated, FakeResult())
        ) as generate:
            status, payload = self.post("/generate-mechanics", {"bundle": BUNDLE})
        self.assertEqual(status, 200)
        self.assertAlmostEqual(generate.call_args.kwargs["max_budget"], 0.02, places=6)
        self.assertAlmostEqual(payload["daily_cost_usd"], 0.481, places=6)

    def test_old_budget_day_resets_without_carrying_stale_reservations(self):
        self.write_budget(spent=0.3, reserved=0.2, day="2000-01-01")
        self.assertEqual(service._daily_cost(), 0.0)

    def test_corrupt_budget_ledger_fails_closed_before_model_call(self):
        self.budget_path.write_text("not-json")
        with patch.object(service, "generate_causal_model") as generate:
            status, _ = self.post("/generate-mechanics", {"bundle": BUNDLE})
        self.assertEqual(status, 500)
        generate.assert_not_called()


if __name__ == "__main__":
    unittest.main()
