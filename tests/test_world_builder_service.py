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
