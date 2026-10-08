"""ScenarioSpecV1, ported from Cybernetic Influence v3 (docs/plans/scenario_spec_adoption.md, check S1).

Input is the recorded Cybernetic Influence pencil draft (draft_49524bf20017, approved 2026-10-07), copied from the
VPS to spikes/any-scenario-2026-10/evidence/scenario-spec/pencil_draft.json; its people are invented.
"""
from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SPIKE = REPO / "spikes/any-scenario-2026-10"
sys.path.insert(0, str(SPIKE))

from pydantic import ValidationError  # noqa: E402
from scenario_spec import ScenarioSpecV1, from_donor_scenario  # noqa: E402

DRAFT = json.loads((SPIKE / "evidence/scenario-spec/pencil_draft.json").read_text())
DONOR = DRAFT["proposal"]["scenario"]


def _minimal(**over):
    spec = {
        "scenario_id": "concern_demo", "title": "Concern demo", "description": "A group raises a concern.",
        "people": [
            {"entity_id": "legal_group", "label": "Legal group", "position": "Legal advisers",
             "disposition": "Careful", "memories": ["Saw a data-sharing clause conflict."],
             "behavioral_profile": {"goals": ["Get the clause fixed before activation."]}},
            {"entity_id": "country_b", "label": "Country B", "position": "Member", "disposition": "Supportive",
             "memories": ["Voted for the pilot."], "behavioral_profile": {}},
        ],
        "information_items": [
            {"representation_id": "clause_conflict", "content": "Clause 4 conflicts with national law.",
             "apparent_source": "Legal group", "holder_id": "legal_group", "channel_id": "legal_channel",
             "recipient_ids": ["country_b"]},
        ],
        "behaviors": [{"request_id": "raise_concern", "subject_refs": ["legal_group", "clause_conflict"],
                       "behavior_description": "The legal group sends its concern.",
                       "desired_effects": ["Country B knows the concern."], "fidelity_need": "exact",
                       "causally_material": True}],
        "fidelity_assumptions": ["One concern."],
    }
    spec.update(over)
    return spec


class DonorDraftTests(unittest.TestCase):
    def test_recorded_pencil_draft_reads_with_people_and_profiles(self):
        spec = from_donor_scenario(DONOR)
        self.assertEqual([p.entity_id for p in spec.people], ["maya_chen", "elena_ruiz", "owen_brooks"])
        maya = spec.people[0]
        self.assertTrue(maya.behavioral_profile.goals and maya.behavioral_profile.decision_tendencies)
        self.assertEqual(len(spec.world_records), len(DONOR["world_records"]))

    def test_unported_donor_parts_are_listed_not_dropped(self):
        spec = from_donor_scenario(DONOR)
        self.assertIn("donor part not ported: resource_extension", spec.unsupported)
        self.assertTrue(any(u.startswith("behavior transport_pencils_request: subjects in unported parts")
                            for u in spec.unsupported))


class ContractTests(unittest.TestCase):
    def test_minimal_concern_scenario_is_valid(self):
        spec = ScenarioSpecV1.model_validate(_minimal())
        self.assertEqual(spec.information_items[0].recipient_ids, ["country_b"])

    def test_undeclared_recipient_is_refused(self):
        bad = _minimal()
        bad["information_items"][0]["recipient_ids"] = ["country_z"]
        with self.assertRaisesRegex(ValidationError, "undeclared recipients"):
            ScenarioSpecV1.model_validate(bad)

    def test_item_sent_to_its_own_holder_is_refused(self):
        bad = _minimal()
        bad["information_items"][0]["recipient_ids"] = ["legal_group"]
        with self.assertRaisesRegex(ValidationError, "sent to its own holder"):
            ScenarioSpecV1.model_validate(bad)

    def test_unknown_field_is_refused(self):
        bad = _minimal()
        bad["people"] = deepcopy(bad["people"])
        bad["people"][0]["mood"] = "tense"
        with self.assertRaises(ValidationError):
            ScenarioSpecV1.model_validate(bad)


if __name__ == "__main__":
    unittest.main(verbosity=2)
