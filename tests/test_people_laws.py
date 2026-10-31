"""People worlds declare their own laws and keep only those the compiled rules can keep (declared-laws plan, s4).

s4 Waltzman (2026-10-30, evidence/declared-laws/s4-waltzman/) was built with no laws: only a world of things was asked
for them. The fixture is that build's kept world; its compiled rules stand in for the compiled ones here.
"""
from __future__ import annotations

import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts import people_world  # noqa: E402

SAVED = json.loads((ROOT / "tests/fixtures/waltzman-s4-kept.json").read_text())
AGENDA = {"resource_id": "agenda-matter", "says": "Matters before the decision.",
          "kept_in": [{"component": "group_decision", "field": "agenda_items"}]}


def law(changers):
    return {"law_id": "agenda-changes-by-moves", "says": "Matters come and go only by being raised or settled.",
            "resource": "agenda-matter", "may_change_by": changers}


class KeepCompiledLawsTests(unittest.TestCase):
    def test_a_total_law_must_list_every_compiled_step_that_writes_its_field(self):
        bundle = {**SAVED["bundle"], "resources": [AGENDA], "laws": [law(["put-matter-on-agenda"])]}
        laws, notes = people_world.keep_compiled_laws(bundle, SAVED["causal_model"])
        self.assertEqual(laws, [])
        self.assertIn("settle-agenda-matter", notes[0])

    def test_a_total_law_listing_them_all_is_kept(self):
        bundle = {**SAVED["bundle"], "resources": [AGENDA],
                  "laws": [law(["put-matter-on-agenda", "settle-agenda-matter"])]}
        laws, notes = people_world.keep_compiled_laws(bundle, SAVED["causal_model"])
        self.assertEqual([x["law_id"] for x in laws], ["agenda-changes-by-moves"])
        self.assertEqual(notes, [])

    def test_a_pairing_law_on_a_compiled_move_is_dropped(self):
        pairing = {"law_id": "trade", "says": "x", "move": "communicate",
                   "gives": {"resource": "agenda-matter", "from": "actor", "to": "recipient"},
                   "pays": {"resource": "agenda-matter", "from": "recipient", "to": "actor"}}
        laws, notes = people_world.keep_compiled_laws({**SAVED["bundle"], "resources": [AGENDA], "laws": [pairing]},
                                                      SAVED["causal_model"])
        self.assertEqual(laws, [])
        self.assertIn("communicate is a compiled rule", notes[0])


class DeclarePeopleLawsTests(unittest.TestCase):
    def declare(self, reply):
        fake = types.SimpleNamespace(call_llm=lambda *a, **k: types.SimpleNamespace(content=json.dumps(reply)),
                                     safe_json_loads=json.loads)
        prepared = {"bundle": SAVED["bundle"], "compiled": SAVED["causal_model"]}
        with patch.dict(sys.modules, {"llm_client": fake}):
            return people_world.declare_people_laws(SAVED["description"], prepared, trace_id="t", max_budget=0.0)

    def test_a_valid_reply_is_kept_and_checked_against_the_compiled_rules(self):
        declared, notes = self.declare({"resources": [AGENDA],
                                        "laws": [law(["put-matter-on-agenda", "settle-agenda-matter"])]})
        self.assertEqual(declared["resources"], [AGENDA])
        self.assertEqual(len(declared["laws"]), 1)
        self.assertEqual(notes, [])

    def test_a_reply_naming_a_move_the_world_lacks_declares_none_and_says_why(self):
        declared, notes = self.declare({"resources": [AGENDA], "laws": [law(["vote-twice"])]})
        self.assertEqual(declared, {"resources": [], "laws": []})
        self.assertIn("vote-twice", notes[0])

    def test_nothing_kept_count_of_declares_none(self):
        declared, notes = self.declare({"resources": [], "laws": []})
        self.assertEqual(declared, {"resources": [], "laws": []})
        self.assertEqual(notes, [])


if __name__ == "__main__":
    unittest.main()
