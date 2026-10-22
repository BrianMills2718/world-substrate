"""Scenario replay (docs/model/VIEW_COVERAGE.md G12, G15, G16) on the retained Waltzman pipeline run.

No model calls: the page is rebuilt from spikes/any-scenario-2026-10/evidence/waltzman/run.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "spikes/any-scenario-2026-10"))

from render_run import build_page, load_world, state_rounds, to_trace  # noqa: E402

RUN = REPO / "spikes/any-scenario-2026-10/evidence/waltzman/run"


def page_data(html: str, name: str):
    start = html.index(f"const {name}=") + len(f"const {name}=")
    return json.JSONDecoder().raw_decode(html[start:])[0]


class ScenarioReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle, cls.causal = load_world(RUN)
        cls.trace = to_trace(RUN, cls.bundle)
        cls.html = build_page(RUN)[1]

    def test_g15_a_refusal_names_the_check_that_failed(self):
        row = self.trace["transcript"][1]["actors"]["country-b"]
        self.assertEqual(row["refused_because"], ["Registered action rule"])
        event = next(e for e in state_rounds(RUN, self.bundle, 2)[1]["events"] if e["event_id"] == "e00008")
        self.assertEqual([c["label"] for c in event["failed_checks"]], ["Registered action rule"])
        self.assertIn("Registered action rule", json.dumps(page_data(self.html, "WS_STATE")))

    def test_g16_continue_is_not_shown_as_waiting(self):
        row = self.trace["transcript"][1]["actors"]["country-a"]
        self.assertEqual(row["status"], "continue")
        self.assertEqual(row["did"]["kind"], "continue")  # the picture says "continue", not "wait"

    def test_g16_each_attempt_is_shown_in_full_with_the_game_masters_ruling(self):
        attempts = page_data(self.html, "WS_STATE")[1]["attempts"]
        b = next(a for a in attempts if a["actor"] == "Country B")
        self.assertTrue(b["intent"].startswith("Propose a time-boxed cross-country review"))
        self.assertTrue(b["ruling"].startswith("No rule could be added"))
        self.assertTrue(b["expected_effect"])
        self.assertTrue(b["cited_observations"])
        first = page_data(self.html, "WS_STATE")[0]["attempts"][0]
        self.assertEqual(first["observed_effect"], "no categorical change")
        self.assertEqual(first["decision"], "offered")

    def test_g12_the_page_shows_the_whole_built_world(self):
        world = page_data(self.html, "WS_WORLD")
        self.assertEqual(world["label"], "Cross-Border Surveillance Decision")
        self.assertTrue(world["summary"].startswith("Four countries"))
        self.assertIn("governance_participant", world["components"])
        actions = {a["kind"]: a["attempted"] for a in world["actions"]}
        self.assertEqual(actions["submit-concern"], 0)
        self.assertEqual(actions["hold-meeting"], 0)
        self.assertGreater(actions["cast-vote"], 0)
        processes = {p["id"]: p["fired"] for p in world["processes"]}
        self.assertEqual(processes["apply-weekly-unresolved-concern-pressure"], 0)
        self.assertGreater(processes["tally-country-approval"], 0)


if __name__ == "__main__":
    unittest.main()
