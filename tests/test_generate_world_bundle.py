from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path
from types import ModuleType, SimpleNamespace
from unittest.mock import MagicMock, patch

from scripts.generate_world_bundle import generate_world_bundle

REPO = Path(__file__).resolve().parents[1]
ORCHARD = json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text())


def fake_llm(*contents: str) -> tuple[ModuleType, MagicMock]:
    module = ModuleType("llm_client")
    call = MagicMock(side_effect=[SimpleNamespace(content=c, model="fake-model", cost=0.0) for c in contents])
    module.call_llm = call
    module.safe_json_loads = json.loads
    return module, call


class GenerateWorldBundleTests(unittest.TestCase):
    def test_valid_proposal_is_returned_validated(self):
        module, call = fake_llm(json.dumps(ORCHARD))
        with patch.dict(sys.modules, {"llm_client": module}):
            bundle, _, _ = generate_world_bundle("One worker picks a ripe apple.", trace_id="t", max_budget=0.01)
        self.assertEqual(bundle["world"]["id"], "orchard")
        self.assertEqual(call.call_count, 1)
        sent = json.loads(call.call_args.args[1][1]["content"])
        self.assertEqual(sent["description"], "One worker picks a ripe apple.")

    def test_validator_error_drives_exactly_one_repair(self):
        broken = json.loads(json.dumps(ORCHARD))
        broken["entities"][2]["components"]["fruit"]["tree_id"] = "no-such-tree"
        good = dict(ORCHARD, not_modeled=["the deadline before noon"])
        module, call = fake_llm(json.dumps(broken), json.dumps(good))
        with patch.dict(sys.modules, {"llm_client": module}):
            bundle, not_modeled, _ = generate_world_bundle("orchard", trace_id="t", max_budget=0.01)
        self.assertEqual(not_modeled, ["the deadline before noon"])
        self.assertNotIn("not_modeled", bundle)
        self.assertEqual(call.call_count, 2)
        repair = call.call_args_list[1].args[1][-1]["content"]
        self.assertIn("no-such-tree", repair)
        self.assertEqual(bundle["world"]["id"], "orchard")

    def test_invalid_after_repairs_fails_loudly_naming_the_reason(self):
        no_actions = json.loads(json.dumps(ORCHARD))
        no_actions["actions"] = []
        module, call = fake_llm(*[json.dumps(no_actions)] * 3)
        with patch.dict(sys.modules, {"llm_client": module}):
            with self.assertRaisesRegex(ValueError, "invalid after 2 repairs: .*at least one action"):
                generate_world_bundle("orchard", trace_id="t", max_budget=0.01)
        self.assertEqual(call.call_count, 3)

    def test_empty_or_oversized_description_is_rejected_before_any_call(self):
        module, call = fake_llm()
        with patch.dict(sys.modules, {"llm_client": module}):
            for bad in ("  ", "x" * 2001):
                with self.assertRaises(ValueError):
                    generate_world_bundle(bad, trace_id="t", max_budget=0.01)
        call.assert_not_called()


if __name__ == "__main__":
    unittest.main()
