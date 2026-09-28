from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.cvs_sustainment.simulate import run_scenario

FIXTURE = REPO / "tests/fixtures/cvs/sustainment_situation_ir.json"
TARGET_CAPS = {
    "cap_observe_distribution",
    "cap_override_reserve",
    "cap_transfer_authority",
}
TARGET_ACTIONS = {
    "sc_1": {"source": "stock_a", "target": "stock_b", "amount": 2},
    "sc_2": {"source": "stock_b", "target": "stock_a", "amount": 2},
    "sc_3": None,
    "sc_4": None,
    "sc_5": {"source": "stock_a", "target": "stock_b", "amount": 2},
    "sc_6": {"source": "stock_b", "target": "stock_a", "amount": 2},
}


class CvsSustainmentSimulationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.situation = json.loads(FIXTURE.read_text())

    def test_baseline_is_nonviable_in_all_pinned_scenarios_without_reimplementing_cvs_search(self):
        results = [
            run_scenario(self.situation, scenario_id=f"sc_{i}")
            for i in range(1, 7)
        ]
        self.assertEqual([r["outcome"]["viable"] for r in results], [False] * 6)
        self.assertTrue(all(r["causal_trace"] == [] for r in results))

    def test_cvs_minimum_capability_set_plus_cvs_selected_moves_is_viable_in_all_scenarios(self):
        results = [
            run_scenario(
                self.situation,
                scenario_id=scenario_id,
                enabled_capabilities=TARGET_CAPS,
                action=action,
            )
            for scenario_id, action in TARGET_ACTIONS.items()
        ]
        self.assertTrue(all(r["outcome"]["viable"] for r in results))
        for result in results:
            if result["input_action"] is None:
                self.assertEqual(result["causal_trace"], [])
            else:
                self.assertEqual(result["action_result"]["status"], "accepted")
                self.assertEqual(len(result["causal_trace"]), 1)
                self.assertEqual(result["causal_trace"][0]["rule_id"], "cvs-sustainment.transfer")

    def test_transfer_without_required_capabilities_is_refused_atomically(self):
        result = run_scenario(
            self.situation,
            scenario_id="sc_1",
            action={"source": "stock_a", "target": "stock_b", "amount": 2},
        )
        self.assertEqual(result["action_result"]["status"], "precondition_failed")
        self.assertEqual(result["initial_inventory"], result["final_inventory"])
        self.assertFalse(result["outcome"]["viable"])

    def test_reserve_override_changes_outcome_without_changing_transfer_physics(self):
        no_override = run_scenario(
            self.situation,
            scenario_id="sc_1",
            enabled_capabilities={"cap_observe_distribution", "cap_transfer_authority"},
            action={"source": "stock_a", "target": "stock_b", "amount": 2},
        )
        with_override = run_scenario(
            self.situation,
            scenario_id="sc_1",
            enabled_capabilities=TARGET_CAPS,
            action={"source": "stock_a", "target": "stock_b", "amount": 2},
        )
        self.assertEqual(no_override["action_result"]["status"], "accepted")
        self.assertEqual(with_override["action_result"]["status"], "accepted")
        self.assertFalse(no_override["outcome"]["viable"])
        self.assertTrue(with_override["outcome"]["viable"])
        self.assertEqual(no_override["outcome"]["withheld_by_pool"], {"stock_a": 1, "stock_b": 1})
        self.assertEqual(with_override["outcome"]["withheld_by_pool"], {"stock_a": 0, "stock_b": 0})

    def test_capacity_effects_fail_loudly_until_modeled(self):
        with self.assertRaisesRegex(ValueError, "does not yet implement enabled capacity"):
            run_scenario(
                self.situation,
                scenario_id="sc_1",
                enabled_capabilities={"cap_extra_a_1"},
            )


if __name__ == "__main__":
    unittest.main()
