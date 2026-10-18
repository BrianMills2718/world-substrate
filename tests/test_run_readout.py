"""The "What happened" readout keeps only claims the recording supports (scripts/run_readout.py)."""

import unittest

from scripts import run_readout

ROUNDS = [
    {"turn": 1, "actors": {
        "ana": {"status": "accepted", "event_id": "e00004", "did": {"kind": "raise-concern"}, "said": "worried",
                "changes": [{"path": "entities.concern.components.concern.open", "before": False, "after": True}]},
        "ben": {"status": "accepted", "event_id": "e00005", "did": {"kind": "wait"}, "changes": []},
        "cy": {"status": "refused", "event_id": "e00006", "did": {"kind": "approve"}, "changes": []},
    }, "world_events": [{"event_id": "e00007", "rule_id": "deadline-passes",
                         "changes": [{"path": "entities.deadline.components.moment.ticks_until", "before": 1, "after": 0}]}]},
]


class ReadoutTest(unittest.TestCase):
    def test_evidence_is_every_event_that_changed_the_world(self):
        events = run_readout.evidence_events(ROUNDS)
        self.assertEqual([e["event_id"] for e in events], ["e00004", "e00007"])
        self.assertIn("False -> True", events[0]["changed"].replace("false", "False").replace("true", "True"))
        self.assertEqual(events[1]["by"], "the world (a rule)")

    def test_long_change_lists_are_cut_at_whole_changes(self):
        changes = [{"path": f"entities.info-logistics-concern-{i}.components.concern.status", "before": "resolved",
                    "after": "open"} for i in range(9)]
        text = run_readout._change_text(changes)
        kept = text.split("; and ")[0].split("; ")
        self.assertTrue(all(k.endswith("resolved -> open") for k in kept))
        self.assertTrue(text.endswith(f"; and {9 - len(kept)} more changes"))

    def test_claims_without_a_recorded_event_are_missing(self):
        events = run_readout.evidence_events(ROUNDS)
        parsed = {"summary": "s", "mechanisms": [
            {"id": "separate-channels", "status": "present", "event_ids": ["e00004", "e00005"], "explanation": "x"},
            {"id": "slowed-meetings", "status": "present", "event_ids": [], "explanation": "y"},
            {"id": "reopened-issues", "status": "missing", "missing_reason": "nothing was undone"},
        ]}
        out = {m["id"]: m for m in run_readout.validate_readout("coordination", parsed, events)["mechanisms"]}
        self.assertEqual(out["separate-channels"]["status"], "present")
        self.assertEqual(out["separate-channels"]["event_ids"], ["e00004"])  # e00005 changed nothing
        self.assertEqual(out["separate-channels"]["dropped_event_ids"], ["e00005"])
        self.assertEqual(out["slowed-meetings"]["status"], "missing")
        self.assertIn("named no event", out["slowed-meetings"]["missing_reason"])
        self.assertEqual(out["reopened-issues"]["missing_reason"], "nothing was undone")
        self.assertEqual(out["conditional-support"]["status"], "missing")  # the model skipped it
        self.assertEqual(len(out), 4)

    def test_prompt_names_every_mechanism_and_event(self):
        messages = run_readout.readout_prompt("coordination", [{"id": "ana", "label": "Ana", "position": "chair"}],
                                              run_readout.evidence_events(ROUNDS))
        text = messages[1]["content"]
        for m in run_readout.LENSES["coordination"]["mechanisms"]:
            self.assertIn(m["id"], text)
        self.assertIn("e00007", text)
        self.assertIn("Ana", text)


if __name__ == "__main__":
    unittest.main()
