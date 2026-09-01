"""Negative controls for fail-closed M1 evidence and maturity receipts."""

from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))
sys.path.insert(0, str(REPO / "scripts"))

from run_freshwater_probe import evidence_outputs, render_markdown
from validate_e2e_receipt import validate_receipt


class EvidenceGateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.freshwater = json.loads(
            (REPO / "evidence/m1/freshwater-v0.json").read_text()
        )
        self.receipt = json.loads(
            (REPO / "evidence/m1/end-to-end-observation-v1.json").read_text()
        )

    def test_rejected_probe_cannot_be_encoded_as_canonical_evidence(self) -> None:
        rejected = {**self.freshwater, "accepted": False}

        with self.assertRaisesRegex(ValueError, "did not accept"):
            evidence_outputs(rejected)
        markdown = render_markdown(rejected).decode()
        self.assertIn("**Result:** FAIL", markdown)
        self.assertNotIn("**Result:** PASS", markdown)

    def test_current_maturity_receipt_satisfies_the_complete_contract(self) -> None:
        self.assertEqual(validate_receipt(self.receipt), [])

    def test_missing_required_receipt_field_is_rejected(self) -> None:
        incomplete = deepcopy(self.receipt)
        del incomplete["outcome"]

        errors = validate_receipt(incomplete)

        self.assertTrue(any("missing required fields" in error for error in errors))

    def test_pass_cannot_hide_an_unobserved_required_surface(self) -> None:
        false_green = deepcopy(self.receipt)
        persistence = next(
            row
            for row in false_green["surface_observations"]
            if row["surface"] == "persistence"
        )
        persistence.clear()
        persistence.update(
            {
                "surface": "persistence",
                "status": "missing",
                "limitation": "no durable replay observation",
            }
        )

        errors = validate_receipt(false_green)

        self.assertIn(
            "missing or unavailable surfaces require status=inconclusive", errors
        )


if __name__ == "__main__":
    unittest.main()
