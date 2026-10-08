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


PIPELINE1 = SPIKE / "evidence/waltzman-spec/pipeline1"  # pipeline run waltzman-spec-20261008T163904 (audit 2026-10-08)


class RecordedPipelineRepairTests(unittest.TestCase):
    """Defects the audit found in that run, checked against its recorded files."""

    def setUp(self):
        sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "scripts")]
        from compile_spec import compile_spec
        self.spec = ScenarioSpecV1.model_validate_json((PIPELINE1 / "scenario_spec.json").read_text())
        _, self.compiled, self.coverage = compile_spec(self.spec)
        self.recorded = json.loads((PIPELINE1 / "causal.json").read_text())
        self.model = json.loads((PIPELINE1 / "model.json").read_text())

    def test_generated_rules_may_not_write_moment_countdowns(self):
        from spec_pipeline import merge_causal
        generated = {**self.recorded,
                     "mechanics": [m for m in self.recorded["mechanics"] if m["action_kind"] != "communicate"],
                     "processes": [p for p in self.recorded["processes"]
                                   if p["process_id"] not in ("moment-countdown", "moment-occurs")]}
        merged, dropped = merge_causal(self.compiled, generated)
        writers = [p["process_id"] for p in merged["processes"]
                   if any(e["path"].startswith("components.moment.") for e in p["effects"])]
        self.assertEqual(writers, ["moment-countdown", "moment-occurs"])
        self.assertIn("generated process advance-scheduled-moments dropped: it writes what a compiled rule owns",
                      dropped)

    def test_actions_get_fields_for_their_behaviors_records(self):
        from spec_pipeline import record_fields
        sigs = {a["kind"]: [f["name"] for f in a["fields"]] for a in record_fields(self.spec,
                                                                                   self.model["action_signatures"])}
        self.assertIn("member_support", sigs["make-support-conditional"])
        self.assertIn("meeting_progress", sigs["reopen-settled-issue"])

    def test_coverage_counts_rules_that_change_records_not_names(self):
        from spec_pipeline import behavior_coverage
        cov = behavior_coverage(self.spec, self.model["action_signatures"], self.recorded, deepcopy(self.coverage))
        rows = {r["request_id"]: r for r in cov["rows"]}
        self.assertEqual(rows["raise_local_concerns"]["classification"], "exact")
        self.assertEqual(rows["make_support_conditional"]["classification"], "unsupported")  # was reported coarse
        self.assertIn("member_support", rows["make_support_conditional"]["why"])


RUN2 = SPIKE / "evidence/waltzman-spec/run2"  # pipeline run waltzman-spec-20261008T174927, agent run run-20261008T184545


def _run2_events():
    import gzip
    with gzip.open(RUN2 / "run/events.jsonl.gz", "rt") as fh:
        return [json.loads(line) for line in fh if line.strip()]


class RecordedWaltzmanRunTests(unittest.TestCase):  # S5/S6: claims in the Assessment, against the recorded run
    def setUp(self):
        self.events = _run2_events()
        self.attempts = [json.loads(x) for x in (RUN2 / "run/attempts.jsonl").read_text().splitlines() if x.strip()]

    def _changes(self, event_id):
        e = next(e for e in self.events if e["event_id"] == event_id)
        return {c["path"]: (c["before"], c["after"]) for c in e["changes"]}

    def test_each_group_delivers_its_concern_to_exactly_one_country(self):
        sends = [e for e in self.events if e["rule_id"] == "coordination.action.communicate"]
        self.assertEqual(len(sends), 4)
        for e in sends:
            aware = [p for p in self._changes(e["event_id"]) if p.endswith(".components.member.aware")]
            self.assertEqual(len(aware), 1, e["event_id"])
        self.assertEqual(self._changes("e00006")["entities.delivery-info-legal-concern-to-country-two.components.delivery.status"],
                         ("pending", "delivered"))

    def test_country_two_makes_support_conditional_citing_the_concern_only_it_received(self):
        a = next(x for x in self.attempts if (x.get("performed") or {}).get("event_id") == "e00015")
        self.assertEqual(a["actor"], "country-two")
        self.assertTrue(any("to country_two" in c for c in a["cited_observations"]))
        self.assertEqual(self._changes("e00015")["entities.member-support.components.member_support.conditional_support_count"],
                         (1, 2))

    def test_reopened_issue_sets_progress_back(self):
        ch = self._changes("e00025")
        self.assertEqual(ch["entities.meeting-progress.components.meeting_progress.progress_percent"], (60, 50))
        self.assertEqual(ch["entities.meeting-progress.components.meeting_progress.settled_issues_reopened"], (0, 1))

    def test_every_agent_was_briefed_with_its_own_profile(self):
        briefed = {x["actor"] for x in self.attempts if x.get("brief")}
        self.assertEqual(briefed, {x["actor"] for x in self.attempts})
        legal = next(x for x in self.attempts if x["actor"] == "legal-group")
        self.assertIn("Legal", legal["brief"])

    def test_the_recorded_block_used_the_weekly_meeting_as_its_deadline(self):
        e = next(e for e in self.events if e["event_id"] == "e00047")
        check = next(c for c in e["checks"] if c["label"] == "the decision deadline has occurred")
        self.assertEqual(check["actual"], 5)  # occurrences of the weekly meeting; the deadline had occurred 0 times

    def test_pinned_slots_refuse_the_meeting_as_the_deadline(self):
        sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "scripts")]
        from compile_spec import compile_spec
        from scripts.run_authored_world import build_engine
        from spec_pipeline import pin_named_slots
        spec = ScenarioSpecV1.model_validate_json((RUN2 / "scenario_spec.json").read_text())
        bundle, _, _ = compile_spec(spec)
        recorded = json.loads((RUN2 / "run/bundle_after_run.json").read_text())
        bundle["actions"] = recorded["actions"]
        bundle["components"] = recorded["components"]
        causal, pinned = pin_named_slots(spec, json.loads((RUN2 / "run/causal_after_run.json").read_text()))
        self.assertIn("block-at-deadline-for-missing-support.activation_decision_deadline -> activation-decision-deadline",
                      pinned)
        engine, _, _ = build_engine(bundle, causal)
        page = engine.discover("partnership", kind="block-deployment")
        slots = {r["action"]["activation_decision_deadline"] for r in page["available"] + page["blocked"]}
        self.assertEqual(slots, {"activation-decision-deadline"})


if __name__ == "__main__":
    unittest.main(verbosity=2)
