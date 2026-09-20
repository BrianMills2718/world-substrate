from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from scripts.native_coordination_authoring import (
    DRAFT_SCHEMA_VERSION,
    SUPPORTED_FAMILY,
    draft_review,
    draft_to_bundle,
    validate_native_coordination_draft,
)
from scripts.run_authored_world import build_engine

REPO = Path(__file__).resolve().parents[1]
CAUSAL = json.loads(
    (REPO / "examples/native_coordination/coordination-causal-v0.json").read_text()
)


def draft() -> dict:
    return {
        "schema_version": DRAFT_SCHEMA_VERSION,
        "family": SUPPORTED_FAMILY,
        "draft_version": 1,
        "source_description": (
            "Mara, Ivo, Chen and Sol must approve a handoff. Sol can restore "
            "the missing token. Mara and Ivo receive private status reports. "
            "I also want probabilistic delays."
        ),
        "proposal": {
            "schema_version": "world-substrate-native-coordination-proposal/v0",
            "world": {
                "id": "handoff-review",
                "label": "Handoff review",
                "summary": "Four members coordinate a gated handoff.",
                "location": "handoff-room",
            },
            "members": [
                {"id": "mara", "label": "Mara", "role": "lead", "authorized": False},
                {"id": "ivo", "label": "Ivo", "role": "receiver", "authorized": False},
                {"id": "chen", "label": "Chen", "role": "observer", "authorized": False},
                {"id": "sol", "label": "Sol", "role": "operator", "authorized": True},
            ],
            "resources": [
                {
                    "id": "handoff-token",
                    "label": "Handoff token",
                    "current": 0,
                    "required": 1,
                    "unit": "token",
                    "restorable": True,
                },
                {
                    "id": "capacity",
                    "label": "Queue capacity",
                    "current": 1,
                    "required": 1,
                    "unit": "slot",
                    "restorable": False,
                },
                {
                    "id": "link",
                    "label": "Link health",
                    "current": 1,
                    "required": 1,
                    "unit": "state",
                    "restorable": False,
                },
                {
                    "id": "window",
                    "label": "Safety window",
                    "current": 1,
                    "required": 1,
                    "unit": "state",
                    "restorable": False,
                },
            ],
            "gate": {
                "id": "handoff-gate",
                "label": "Handoff gate",
                "required_approvals": 2,
            },
            "reports": [
                {
                    "id": "token-report",
                    "label": "Token report",
                    "source_id": "sol",
                    "recipient_id": "mara",
                    "channel_id": "ops-chat",
                    "topic": "token",
                    "content": "The handoff token is missing.",
                },
                {
                    "id": "link-report",
                    "label": "Link report",
                    "source_id": "sol",
                    "recipient_id": "ivo",
                    "channel_id": "radio",
                    "topic": "link",
                    "content": "The represented link is healthy.",
                },
            ],
            "requirement_coverage": [
                {
                    "text": "Sol alone can restore the missing handoff token.",
                    "surface": "authorization",
                },
                {
                    "text": "Two informed members must approve before finalization.",
                    "surface": "approval_threshold",
                },
                {
                    "text": "Private status reports go to Mara and Ivo.",
                    "surface": "information_delivery",
                },
                {
                    "text": "Use probabilistic delivery delays.",
                    "surface": "unsupported",
                },
            ],
            "assumptions": [
                "The handoff token is the only initially unhealthy prerequisite."
            ],
            "unsupported_requests": ["Use probabilistic delivery delays."],
        },
    }


class NativeCoordinationAuthoringTests(unittest.TestCase):
    def test_draft_compiles_to_existing_authoring_bundle_and_shared_mechanics(self):
        value = draft()
        checked = validate_native_coordination_draft(value)
        self.assertEqual(checked["source_description"], value["source_description"])

        bundle = draft_to_bundle(value)
        self.assertEqual(bundle["schema_version"], "world-substrate-authoring-bundle/v0")
        self.assertEqual(
            [row["kind"] for row in bundle["actions"]],
            ["communicate", "approve", "intervene", "finalize"],
        )
        restorable = next(
            row for row in bundle["entities"] if "restorable" in row["categories"]
        )
        self.assertIn("prereq-a", restorable["categories"])

        engine, model, profile_id = build_engine(bundle, CAUSAL)
        self.assertTrue(profile_id)
        self.assertEqual(
            [mechanic.action_kind for mechanic in model.mechanics],
            ["communicate", "approve", "intervene", "finalize"],
        )
        self.assertEqual(engine.world.world_id, "handoff-review-live")

    def test_review_separates_requirements_assumptions_and_unsupported_requests(self):
        review = draft_review(draft())
        self.assertEqual(
            review["schema_version"],
            "world-substrate-native-coordination-draft-review/v0",
        )
        self.assertTrue(review["narrowing_is_explicit"])
        self.assertIn(
            "Use probabilistic delivery delays.",
            review["unsupported_requests"],
        )
        approval = next(
            row for row in review["requirements"]
            if row["surface"] == "approval_threshold"
        )
        self.assertEqual(approval["status"], "represented")
        self.assertEqual(
            approval["implemented_by"],
            ["coordination.action.approve", "coordination.action.finalize"],
        )
        unsupported = next(
            row for row in review["requirements"]
            if row["surface"] == "unsupported"
        )
        self.assertEqual(unsupported["status"], "unsupported")
        self.assertEqual(unsupported["implemented_by"], [])
        self.assertEqual(len(review["assumptions"]), 1)
        self.assertEqual(len(review["mechanics"]["mechanics"]), 4)

    def test_validation_refuses_multiple_authorized_members(self):
        value = draft()
        value["proposal"]["members"][0]["authorized"] = True
        with self.assertRaisesRegex(ValueError, "exactly one member"):
            validate_native_coordination_draft(value)

    def test_validation_refuses_hidden_second_unhealthy_resource(self):
        value = draft()
        value["proposal"]["resources"][1]["current"] = 0
        with self.assertRaisesRegex(ValueError, "only the one restorable"):
            validate_native_coordination_draft(value)

    def test_validation_refuses_duplicate_report_recipient_below_real_voter_count(self):
        value = draft()
        value["proposal"]["reports"][1]["recipient_id"] = "mara"
        with self.assertRaisesRegex(ValueError, "recipients must be unique"):
            validate_native_coordination_draft(value)

    def test_bundle_is_editable_without_mutating_the_draft(self):
        value = draft()
        frozen = deepcopy(value)
        bundle = draft_to_bundle(value)
        bundle["world"]["label"] = "Edited in builder"
        self.assertEqual(value, frozen)


if __name__ == "__main__":
    unittest.main()
