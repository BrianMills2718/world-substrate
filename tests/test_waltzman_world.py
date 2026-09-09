"""Integrated acceptance tests for the Waltzman Coordination Lab deliverable."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.waltzman.adequacy import build_adequacy_report
from reference_worlds.waltzman.analysis import analyze_material
from reference_worlds.waltzman.probe import (
    build_engine,
    build_registry,
    run_baseline,
    run_intervention,
)
from world_substrate.engine import CausalParentViolation
from world_substrate.policy import apply_choice, resolve_choice


def choose(engine, actor_id: str, kind: str, **participants: str):
    page = engine.discover(actor_id, kind=kind)
    rows = [
        row
        for row in page["available"]
        if all(row["action"].get(k) == v for k, v in participants.items())
    ]
    assert len(rows) == 1, (actor_id, kind, participants, rows)
    choice = resolve_choice(page, rows[0]["action_id"], "test")
    result = apply_choice(engine, choice, "test")
    assert result is not None and result["status"] == "accepted"
    return result["event"]


class InformationSemanticsTests(unittest.TestCase):
    def test_private_brief_is_not_visible_until_delivered_and_does_not_leak_to_ari(self):
        engine = build_engine()
        before_mara = engine.observe("mara")["entities"]
        before_ari = engine.observe("ari")["entities"]
        self.assertNotIn("brief-validation", before_mara)
        self.assertNotIn("delivery-validation-mara", before_mara)
        self.assertNotIn("brief-validation", before_ari)

        engine.advance(1)
        after_mara = engine.observe("mara")["entities"]
        after_ari = engine.observe("ari")["entities"]
        self.assertIn("brief-validation", after_mara)
        self.assertIn("delivery-validation-mara", after_mara)
        self.assertNotIn("brief-validation", after_ari)
        self.assertNotIn("delivery-validation-mara", after_ari)
        self.assertNotIn("msg-mara-validation", after_ari)

    def test_resident_message_becomes_visible_only_to_the_recipient_after_delivery(self):
        engine = build_engine()
        engine.advance(1)
        choose(
            engine,
            "mara",
            "communicate",
            information="msg-mara-validation",
            delivery="delivery-mara-ari",
        )
        ari = engine.observe("ari")["entities"]
        selene = engine.observe("selene")["entities"]
        self.assertIn("msg-mara-validation", ari)
        self.assertIn("delivery-mara-ari", ari)
        self.assertNotIn("msg-mara-validation", selene)
        self.assertNotIn("delivery-mara-ari", selene)

    def test_information_context_and_hard_causal_ancestry_are_distinct_fields(self):
        engine = run_baseline()
        meeting = next(
            event
            for event in engine.world.events
            if event["rule_id"] == "waltzman.activity.start-meeting"
        )
        self.assertEqual(
            {row["info_id"] for row in meeting["information_context"]},
            {"msg-tomas-staff", "msg-nira-reserve", "msg-idris-safeguard"},
        )
        self.assertNotIn("causal_parent_event_ids", meeting)

        mara_reassess = next(
            event
            for event in engine.world.events
            if event["rule_id"] == "waltzman.commitment.reassess"
            and event["causal_bearer"]["id"] == "mara"
        )
        validation_failure = next(
            event
            for event in engine.world.events
            if event["rule_id"] == "waltzman.process.validation-failure"
        )
        self.assertEqual(
            mara_reassess["causal_parent_event_ids"],
            [validation_failure["event_id"]],
        )
        self.assertIn(
            "brief-validation",
            {row["info_id"] for row in mara_reassess["information_context"]},
        )


    def test_engine_rejects_unknown_hard_causal_parent_ids(self):
        engine = build_engine()
        engine.advance(1)
        rule = engine.registry.action("reassess_commitment")
        assert rule is not None
        rule.causal_parents = lambda world, action: ["e99999"]  # type: ignore[attr-defined]
        page = engine.discover("mara", kind="reassess_commitment")
        choice = resolve_choice(page, page["available"][0]["action_id"], "test invalid parent")
        with self.assertRaises(CausalParentViolation):
            apply_choice(engine, choice, "test")

class WaltzmanRunTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline = run_baseline()
        cls.intervention = run_intervention(cls.baseline)

    def test_baseline_is_blocked_after_a_duration_bearing_meeting(self):
        institution = self.baseline.world.entities["coalition-hub"].component("institution")
        meeting = self.baseline.world.entities["coordination-meeting"].component("activity")
        self.assertEqual(self.baseline.world.tick, 6)
        self.assertEqual(meeting.status, "completed")
        self.assertEqual((meeting.started_tick, meeting.end_tick), (4, 6))
        self.assertEqual(institution.status, "blocked")
        self.assertEqual((institution.support_count, institution.conditional_count), (2, 4))

    def test_intervention_fork_preserves_history_then_recovers(self):
        n = len(self.baseline.world.events)
        self.assertEqual(self.intervention.world.events[:n], self.baseline.world.events)
        institution = self.intervention.world.entities["coalition-hub"].component("institution")
        package = self.intervention.world.entities["stabilization-package"].component("package")
        self.assertEqual(package.status, "delivered")
        self.assertEqual(institution.status, "ready")
        self.assertEqual((institution.support_count, institution.conditional_count), (6, 0))

    def test_both_branches_replay_exactly(self):
        self.assertTrue(self.baseline.replay()["ok"])
        self.assertTrue(self.intervention.replay()["ok"])

    def test_gate_uses_mechanical_commitment_parents_not_information_history(self):
        gate = [
            event
            for event in self.baseline.world.events
            if event["rule_id"] == "waltzman.institution.coalition-gate"
        ][-1]
        communication_ids = {
            event["event_id"]
            for event in self.baseline.world.events
            if event["rule_id"] == "waltzman.information.communicate"
        }
        self.assertTrue(gate["causal_parent_event_ids"])
        self.assertTrue(communication_ids.isdisjoint(gate["causal_parent_event_ids"]))

    def test_detachable_analysis_does_not_mutate_world(self):
        before = self.intervention.world.material_hash()
        result = analyze_material(self.intervention.world.material_dict())
        after = self.intervention.world.material_hash()
        self.assertEqual(before, after)
        self.assertFalse(result["causal"])
        self.assertEqual(result["layer"], "detachable-analysis")
        self.assertEqual(result["institution_status"], "ready")

    def test_causal_adequacy_is_bounded_and_reports_residual_risk(self):
        report = build_adequacy_report(build_registry())
        self.assertTrue(report["bounded"])
        self.assertFalse(report["global_completeness_claimed"])
        self.assertEqual(report["summary"], {"enforced": 8, "gaps": 0})
        self.assertTrue(report["residual_risk"])
        self.assertTrue(all(row["status"] == "enforced" for row in report["dependencies"]))


if __name__ == "__main__":
    unittest.main()
