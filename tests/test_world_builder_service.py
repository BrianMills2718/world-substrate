from __future__ import annotations

import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch

import scripts.world_builder_service as service

REPO = Path(__file__).resolve().parents[1]
BUNDLE = json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text())
CAUSAL = json.loads((REPO / "examples/world_authoring/orchard-causal-v0.json").read_text())


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
        with patch.object(service, "_daily_cost", side_effect=[0.49, 0.491]), patch.object(
            service, "_trace_cost", return_value=0.001
        ), patch.object(
            service, "generate_causal_model", return_value=(fake_generated, FakeResult())
        ) as generate:
            status, _ = self.post("/generate-mechanics", {"bundle": BUNDLE})
        self.assertEqual(status, 200)
        self.assertAlmostEqual(generate.call_args.kwargs["max_budget"], 0.01, places=6)

    def test_generate_endpoint_returns_compiler_review_not_unchecked_model_output(self):
        fake_generated = json.loads(json.dumps(CAUSAL))
        with patch.object(service, "_daily_cost", return_value=0.0), patch.object(
            service, "_trace_cost", return_value=0.001
        ), patch.object(
            service,
            "generate_causal_model",
            return_value=(fake_generated, FakeResult()),
        ):
            status, payload = self.post("/generate-mechanics", {"bundle": BUNDLE})
        self.assertEqual(status, 200)
        self.assertEqual(payload["causal_model"]["schema_version"], "world-substrate-causal-model/v0")
        self.assertIn("writes", payload["review"]["mechanics"][0])
        self.assertEqual(payload["model"], "fake-model")


if __name__ == "__main__":
    unittest.main()
