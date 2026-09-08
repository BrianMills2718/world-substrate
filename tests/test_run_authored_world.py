from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.run_authored_world import build_engine, render_run, run_world
from scripts.scaffold_world import load_bundle
from world_substrate.action_authoring import ActionDeclarationError

REPO = Path(__file__).resolve().parents[1]
BUNDLE_PATH = REPO / "examples/world_authoring/orchard-v0.json"
CAUSAL_PATH = REPO / "examples/world_authoring/orchard-causal-v0.json"


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


if __name__ == "__main__":
    unittest.main()
