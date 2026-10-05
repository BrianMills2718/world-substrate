from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.native_coordination_authoring import draft_to_bundle
from scripts.native_coordination_comparison import with_approval_threshold
from scripts.run_native_coordination import run_native_coordination

REPO = Path(__file__).resolve().parents[1]
DRAFT = json.loads(
    (REPO / "examples/native_coordination/one-shot-draft-v0.json").read_text()
)
BASELINE = draft_to_bundle(DRAFT)
CAUSAL = json.loads(
    (REPO / "examples/native_coordination/coordination-causal-v0.json").read_text()
)


def gate(bundle: dict) -> dict:
    return next(row for row in bundle["entities"] if "gate" in row["categories"])


class NativeCoordinationComparisonTests(unittest.TestCase):
    def test_comparison_is_a_second_fresh_native_run_with_same_mechanics(self):
        baseline_bundle = deepcopy(BASELINE)
        frozen = deepcopy(baseline_bundle)
        comparison_bundle, change = with_approval_threshold(baseline_bundle, 1)

        baseline = run_native_coordination(baseline_bundle, CAUSAL)
        comparison = run_native_coordination(comparison_bundle, CAUSAL)

        self.assertEqual(baseline_bundle, frozen)
        self.assertEqual(change["before"], 2)
        self.assertEqual(change["after"], 1)
        self.assertTrue(baseline["trace"]["summary"]["terminal_reached"])
        self.assertTrue(comparison["trace"]["summary"]["terminal_reached"])
        self.assertEqual(baseline["trace"]["cost_usd"], 0.0)
        self.assertEqual(comparison["trace"]["cost_usd"], 0.0)
        self.assertEqual(
            baseline["trace"]["mechanic_profile_id"],
            comparison["trace"]["mechanic_profile_id"],
        )
        self.assertNotEqual(
            baseline["trace"]["summary"]["turns"],
            comparison["trace"]["summary"]["turns"],
        )
        self.assertNotEqual(
            baseline["trace"]["summary"]["accepted_actions"],
            comparison["trace"]["summary"]["accepted_actions"],
        )
        self.assertNotEqual(
            baseline["projection"]["projection_final"],
            comparison["projection"]["projection_final"],
        )

    def test_comparison_changes_only_approval_threshold_and_preserves_baseline(self):
        baseline = deepcopy(BASELINE)
        frozen = deepcopy(baseline)

        comparison, change = with_approval_threshold(baseline, 1)

        self.assertEqual(baseline, frozen)
        self.assertEqual(change["before"], 2)
        self.assertEqual(change["after"], 1)
        self.assertEqual(change["max_supported"], 2)
        self.assertEqual(
            change["path"],
            "entities.handoff-gate.components.gate.required_approvals",
        )
        self.assertEqual(
            gate(comparison)["components"]["gate"]["required_approvals"],
            1,
        )
        restored = deepcopy(comparison)
        gate(restored)["components"]["gate"]["required_approvals"] = 2
        self.assertEqual(restored, baseline)

    def test_comparison_refuses_same_threshold(self):
        with self.assertRaisesRegex(ValueError, "must differ"):
            with_approval_threshold(BASELINE, 2)

    def test_comparison_refuses_threshold_above_informed_recipient_count(self):
        with self.assertRaisesRegex(ValueError, "between 1 and 2"):
            with_approval_threshold(BASELINE, 3)

    def test_comparison_refuses_non_integer_threshold(self):
        with self.assertRaisesRegex(ValueError, "must be an integer"):
            with_approval_threshold(BASELINE, 1.5)

    def test_comparison_refuses_baseline_threshold_above_informed_recipient_count(self):
        baseline = deepcopy(BASELINE)
        gate(baseline)["components"]["gate"]["required_approvals"] = 3
        with self.assertRaisesRegex(ValueError, "baseline approval threshold must be between 1 and 2"):
            with_approval_threshold(baseline, 1)

    def test_comparison_refuses_delivery_recipient_that_is_not_a_member(self):
        baseline = deepcopy(BASELINE)
        delivery = next(
            row for row in baseline["entities"]
            if "delivery" in (row.get("components") or {})
        )
        delivery["components"]["delivery"]["recipient_id"] = "handoff-token"
        with self.assertRaisesRegex(ValueError, "recipient must be a represented member"):
            with_approval_threshold(baseline, 1)

    def test_comparison_refuses_delivery_info_that_is_not_information(self):
        baseline = deepcopy(BASELINE)
        delivery = next(
            row for row in baseline["entities"]
            if "delivery" in (row.get("components") or {})
        )
        delivery["components"]["delivery"]["info_id"] = "mara"
        with self.assertRaisesRegex(ValueError, "info_id must name represented information"):
            with_approval_threshold(baseline, 1)


if __name__ == "__main__":
    unittest.main()
