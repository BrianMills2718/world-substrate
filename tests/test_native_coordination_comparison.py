from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.native_coordination_authoring import draft_to_bundle
from scripts.native_coordination_comparison import with_approval_threshold

REPO = Path(__file__).resolve().parents[1]
DRAFT = json.loads(
    (REPO / "examples/native_coordination/one-shot-draft-v0.json").read_text()
)
BASELINE = draft_to_bundle(DRAFT)


def gate(bundle: dict) -> dict:
    return next(row for row in bundle["entities"] if "gate" in row["categories"])


class NativeCoordinationComparisonTests(unittest.TestCase):
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
