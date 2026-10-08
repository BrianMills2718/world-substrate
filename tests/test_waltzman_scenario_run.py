"""Waltzman scenario run (docs/plans/waltzman_scenario_run.md, check W4): the assessment's claims hold in the recorded files.

Pipeline run waltzman-20261008T123134 and member run run-20261008T125239, copied to
spikes/any-scenario-2026-10/evidence/waltzman/.
"""
from __future__ import annotations

import gzip
import json
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
EV = REPO / "spikes/any-scenario-2026-10/evidence/waltzman"
CAUSAL = json.loads((EV / "causal.json").read_text())
MODEL = json.loads((EV / "model.json").read_text())
RULES = {r.get("action_kind") or r["process_id"]: r for r in CAUSAL["mechanics"] + CAUSAL["processes"]}
with gzip.open(EV / "run/events.jsonl.gz", "rt") as fh:
    EVENTS = [json.loads(line) for line in fh if line.strip()]
ATTEMPTS = [json.loads(line) for line in (EV / "run/attempts.jsonl").read_text().splitlines() if line.strip()]


def _writes(field):
    return {rid for rid, r in RULES.items() for e in r.get("effects", []) if e["path"].endswith("." + field)}


class WaltzmanAssessmentTests(unittest.TestCase):
    def test_run_ended_with_activation_and_no_concern_or_meeting_event(self):
        rules = {e["rule_id"] for e in EVENTS}
        self.assertIn("activate-unanimously-approved-system", rules)
        self.assertFalse(rules & {"submit-concern", "hold-meeting", "apply-weekly-unresolved-concern-pressure"})
        self.assertEqual(json.loads((EV / "run/summary.json").read_text())["ended"], "terminal")

    def test_concern_delivery_was_offered_but_not_chosen(self):
        first = next(a for a in ATTEMPTS if a["actor"] == "country-a" and a["tick"] == 0)
        self.assertIn("submit-concern(recipient=Country B)", first["offered"])
        self.assertTrue(first["performed"]["action"].startswith("cast-vote"))

    def test_concern_sources_are_not_modeled(self):
        self.assertIn("The technical, legal, logistics, and community groups as separate entities.", MODEL["not_modeled"])

    def test_no_rule_makes_support_conditional_or_reopens_a_vote(self):
        self.assertEqual(_writes("conditional_support"), set())
        sets_vote = {(rid, e["value"].get("literal")) for rid, r in RULES.items() for e in r.get("effects", [])
                     if e["path"].endswith(".vote")}
        self.assertFalse({v for _, v in sets_vote} & {"undecided", "reopened"})

    def test_game_master_rulings_had_no_effect(self):
        rulings = [e for e in EVENTS if e["rule_id"] == "unsupported.gm-ruling"]
        self.assertEqual([e["event_id"] for e in rulings], ["e00008", "e00009", "e00010"])
        self.assertTrue(all(not e["changes"] for e in rulings))


if __name__ == "__main__":
    unittest.main(verbosity=2)
