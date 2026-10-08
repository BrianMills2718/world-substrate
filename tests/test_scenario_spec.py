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


def _two_recipient_spec():
    spec = _minimal(scheduled_moments=[{"moment_id": "weekly_meeting", "tick": 2, "every_ticks": 3,
                                        "description": "Partnership meeting"}])
    spec["people"].append({"entity_id": "country_c", "label": "Country C", "position": "Member",
                           "disposition": "Cautious", "memories": ["Asked about data rules."],
                           "behavioral_profile": {}})
    spec["information_items"][0]["recipient_ids"] = ["country_b", "country_c"]
    spec["behaviors"].append({"request_id": "concern_slows_meeting", "subject_refs": ["clause_conflict", "weekly_meeting"],
                              "behavior_description": "Considering the concern uses meeting time.",
                              "desired_effects": ["The meeting runs longer."], "fidelity_need": "coarse",
                              "causally_material": True})
    spec["behaviors"].append({"request_id": "meeting_slows", "subject_refs": ["weekly_meeting"],
                              "behavior_description": "Concerns slow the meeting.",
                              "desired_effects": ["Less time for decisions."], "fidelity_need": "coarse",
                              "causally_material": True})
    return ScenarioSpecV1.model_validate(spec)


class CompilerTests(unittest.TestCase):  # S2
    def setUp(self):
        sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "scripts")]
        from compile_spec import compile_spec
        from scaffold_world import validate_bundle
        from scripts.run_authored_world import build_engine
        self.bundle, self.causal, self.coverage = compile_spec(_two_recipient_spec())
        validate_bundle(self.bundle)
        self.engine, _, _ = build_engine(self.bundle, self.causal)

    def _status(self, eid):
        return self.engine.world.entities[eid].as_dict()["components"]["delivery"]["status"]

    def test_one_information_entity_and_pending_delivery_per_recipient(self):
        infos = [e for e in self.bundle["entities"] if "information" in e["categories"]]
        self.assertEqual(sorted(e["id"] for e in infos),
                         ["info-clause-conflict-to-country-b", "info-clause-conflict-to-country-c"])
        self.assertTrue(all(e["components"]["information"]["topic"] == "clause_conflict" for e in infos))
        self.assertEqual(self._status("delivery-info-clause-conflict-to-country-b"), "pending")

    def test_one_communicate_event_delivers_to_exactly_its_recipient(self):
        offered = [a["action"] for a in self.engine.discover("legal-group")["available"]]
        to_b = next(a for a in offered if a["recipient"] == "country-b")
        result = self.engine.submit(dict(to_b, controller="test"))
        self.assertEqual(result["status"], "accepted")
        changed = {c["path"] for c in result["event"]["changes"]}
        self.assertIn("entities.delivery-info-clause-conflict-to-country-b.components.delivery.status", changed)
        self.assertIn("entities.country-b.components.member.aware", changed)
        self.assertFalse([p for p in changed if "country-c" in p])
        self.assertEqual(self._status("delivery-info-clause-conflict-to-country-b"), "delivered")
        self.assertEqual(self._status("delivery-info-clause-conflict-to-country-c"), "pending")

    def test_only_the_holder_is_offered_communicate(self):
        self.assertEqual(self.engine.discover("country-b")["available"], [])

    def test_scheduled_moment_occurs_on_its_ticks(self):
        from world_substrate.mechanisms.time import ClockAdvanceProcess
        self.engine.registry.register_process(ClockAdvanceProcess())
        ticks = []
        for _ in range(9):
            if any(e["rule_id"] == "moment-occurs" for e in self.engine.advance(1)["events"]):
                ticks.append(self.engine.world.tick)
        self.assertEqual(ticks, [2, 5, 8])

    def test_coverage_marks_delivery_exact_and_the_rest_for_the_generator(self):
        rows = {r["request_id"]: r["classification"] for r in self.coverage["rows"]}
        # mentioning an item does not make a behavior delivery: the concern slowing a meeting needs its own rules
        self.assertEqual(rows, {"raise_concern": "exact", "concern_slows_meeting": "to_generate",
                                "meeting_slows": "to_generate"})

    def test_communicate_rule_is_the_reviewed_one_unchanged(self):
        reviewed = json.loads((REPO / "examples/native_coordination/coordination-causal-v0.json").read_text())
        self.assertEqual(self.causal["mechanics"][0], reviewed["mechanics"][0])


if __name__ == "__main__":
    unittest.main(verbosity=2)
