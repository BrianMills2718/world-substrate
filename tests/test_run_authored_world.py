from __future__ import annotations

import json
import sys
import types
import unittest
from unittest.mock import patch
from pathlib import Path

from scripts.bootstrap_scene_profile import _entity_binding
from scripts.run_authored_world import _llm_choice, _runtime_catalog, build_engine, render_run, run_world
from scripts.scaffold_world import load_bundle
from world_substrate.action_authoring import ActionDeclarationError

REPO = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO / "examples/world_authoring/orchard-v0.json"
CAUSAL_PATH = REPO / "examples/world_authoring/orchard-causal-v0.json"
REPAIR_BUNDLE_PATH = REPO / "examples/world_authoring/repair-bay-v0.json"
REPAIR_CAUSAL_PATH = REPO / "examples/world_authoring/repair-bay-causal-v0.json"


class AuthoredWorldRunTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle(BUNDLE_PATH)
        self.causal = json.loads(CAUSAL_PATH.read_text())

    def test_scripted_run_uses_compiled_mechanics_and_reaches_terminal(self):
        trace, engine, model = run_world(
            self.bundle, self.causal, policy="scripted", max_turns=5
        )
        self.assertEqual(trace["model"], "scripted-first-available")
        self.assertEqual(trace["cost_usd"], 0.0)
        self.assertEqual(trace["summary"]["turns"], 1)
        self.assertTrue(trace["summary"]["terminal_reached"])
        self.assertEqual(engine.world.entities["apple-1"].ownership.owner_ref, "actor:ava")
        self.assertEqual(engine.world.entities["apple-1"].component("fruit").stage, "picked")
        self.assertTrue(model.terminal and model.terminal.reached(engine.world))

    def test_run_records_distinct_rule_refusals_with_their_failed_checks(self):
        bundle = load_bundle(REPAIR_BUNDLE_PATH)
        causal = json.loads(REPAIR_CAUSAL_PATH.read_text())
        trace, _, _ = run_world(bundle, causal, policy="scripted", max_turns=5)
        rows = [row for turn in trace["transcript"] for row in turn["actors"].values()]
        self.assertTrue(all("blocked_by_rules" in row for row in rows))
        refusals = [b for row in rows for b in row["blocked_by_rules"]]
        self.assertTrue(refusals, "Repair Bay should show at least one refused action")
        for row in rows:
            keys = [(b["action"]["kind"], b["reason"]) for b in row["blocked_by_rules"]]
            self.assertEqual(len(keys), len(set(keys)))
            self.assertLessEqual(len(keys), 3)
        self.assertTrue(all(b["reason"] for b in refusals))

    def test_compiled_profile_is_frozen_before_run(self):
        engine, _, profile_id = build_engine(self.bundle, self.causal)
        self.assertTrue(profile_id)
        self.assertEqual(engine.world.rule_versions, {"orchard.action.pick": "1"})

    def test_rendered_fresh_run_is_graphical_and_self_contained(self):
        trace, _, compiled = run_world(self.bundle, self.causal, policy="scripted", max_turns=5)
        html = render_run(self.bundle, trace, compiled)
        self.assertIn("Scene replay", html)
        self.assertIn("Apple", html)
        self.assertIn("Ava", html)
        self.assertIn("document.getElementById(\'turn\')", html)

    def test_fresh_world_entity_id_does_not_inherit_reference_world_asset_binding(self):
        bundle = json.loads(json.dumps(self.bundle))
        bundle["entities"][0]["id"] = "bo"
        bundle["entities"][0]["label"] = "New-world Bo"
        trace, _, compiled = run_world(bundle, self.causal, policy="scripted", max_turns=5)
        html = render_run(bundle, trace, compiled)
        self.assertIn("New-world Bo", html)
        self.assertIn("Scene replay", html)

    def test_unreviewable_mechanic_never_reaches_runtime(self):
        causal = json.loads(json.dumps(self.causal))
        causal["mechanics"][0]["effects"][0]["path"] = "components.fruit.nonexistent"
        with self.assertRaises(ActionDeclarationError):
            run_world(self.bundle, causal, policy="scripted", max_turns=5)

    def test_live_runner_caps_turns_and_policy_modes(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 30"):
            run_world(self.bundle, self.causal, max_turns=31)
        with self.assertRaisesRegex(ValueError, "scripted or llm"):
            run_world(self.bundle, self.causal, policy="random")


class RepairBayLiveProofTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle(REPAIR_BUNDLE_PATH)
        self.causal = json.loads(REPAIR_CAUSAL_PATH.read_text())

    def test_scripted_baseline_reaches_terminal_through_contention_and_retries(self):
        initial, _, _ = build_engine(self.bundle, self.causal)
        self.assertEqual([initial.discover(a)["total"] for a in ("ava", "bo", "cam", "dee")], [48] * 4)

        trace, engine, model = run_world(
            self.bundle, self.causal, policy="scripted", max_turns=12
        )
        self.assertEqual(
            trace["summary"],
            {"turns": 5, "terminal_reached": True, "accepted_actions": 10},
        )
        accepted_kinds = [
            row["did"]["kind"]
            for turn in trace["transcript"]
            for row in turn["actors"].values()
            if row.get("did") and row.get("status") == "accepted"
        ]
        self.assertEqual(accepted_kinds.count("claim-tool"), 3)
        self.assertEqual(accepted_kinds.count("diagnose"), 3)
        self.assertEqual(accepted_kinds.count("repair"), 3)
        self.assertEqual(accepted_kinds.count("handoff-tool"), 1)
        self.assertEqual(
            sum(bool(row.get("retried")) for turn in trace["transcript"] for row in turn["actors"].values()),
            6,
        )
        self.assertEqual(
            sum(row.get("status") == "nothing_left" for turn in trace["transcript"] for row in turn["actors"].values()),
            1,
        )
        for machine_id in ("pump-1", "generator-1", "conveyor-1"):
            self.assertEqual(engine.world.entities[machine_id].component("machine").status, "working")
        self.assertEqual(engine.world.entities["scanner-1"].ownership.owner_ref, "actor:dee")
        self.assertTrue(model.terminal and model.terminal.reached(engine.world))


    def test_policy_view_shows_installed_authored_effects(self):
        from world_substrate.policy import present

        engine, _, _ = build_engine(self.bundle, self.causal)
        page = engine.discover("ava")
        context = present(engine, "ava", page)
        claim = next(row for row in context["actions"] if "claim-tool" in row["description"])
        self.assertIn("effects:", claim["description"])
        self.assertIn("ownership.owner_ref set 'actor:ava'", claim["description"])
        self.assertIn("hands_free set False", claim["description"])

    def test_live_policy_caps_structured_output_tokens(self):
        engine, _, _ = build_engine(self.bundle, self.causal)
        page = engine.discover("ava")
        captured = {}
        fake = types.ModuleType("llm_client")

        def render_prompt(*args, **kwargs):
            return [{"role": "user", "content": "fixture"}]

        def call_llm_json_schema(model, messages, schema, **kwargs):
            captured.update(kwargs)
            action_id = schema["properties"]["action_id"]["enum"][0]
            result = types.SimpleNamespace(cost=0.001)
            return {"action_id": action_id, "reasoning": "choose offered action"}, result

        fake.render_prompt = render_prompt
        fake.call_llm_json_schema = call_llm_json_schema
        with patch.dict(sys.modules, {"llm_client": fake}):
            action, reasoning, cost = _llm_choice(
                engine,
                "ava",
                page,
                world_summary=self.bundle["world"]["summary"],
                model="fixture-model",
                trace_id="fixture-trace",
                max_budget=0.01,
                recent=[],
            )

        self.assertIsNotNone(action)
        self.assertEqual(reasoning, "choose offered action")
        self.assertEqual(cost, 0.001)
        self.assertEqual(captured["max_tokens"], 512)

    def test_repair_bay_fresh_replay_is_graphical(self):
        trace, _, compiled = run_world(self.bundle, self.causal, policy="scripted", max_turns=12)
        html = render_run(self.bundle, trace, compiled)
        self.assertIn("Scene replay", html)
        self.assertIn("Coolant Pump", html)
        self.assertIn("Diagnostic Scanner", html)
        self.assertIn("Parts Conveyor", html)


if __name__ == "__main__":
    unittest.main()
