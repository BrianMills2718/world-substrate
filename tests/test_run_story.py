"""The plain run story keeps only sentences the recording supports (scripts/run_story.py)."""

import json
import sys
import types
import unittest
from unittest import mock

import pytest

from scripts import run_story

ROUNDS = [
    {"turn": 1, "actors": {
        "ana": {"status": "unsupported_action", "event_id": "r1-e00001", "refused_because": [],
                "did": {"kind": "unmatched-attempt", "attempt": "I tell the other groups I agree",
                        "nearest_kind": "communicate", "why": "recipient='other groups' names no entity in this world"}},
        "ben": {"status": "precondition_failed", "event_id": "r1-e00002", "said": "hello",
                "refused_because": ["Information is not active yet"], "did": {"kind": "communicate"},
                "attempt": {"text": "I tell Ana I agree"}},
        "cy": {"status": "no_action", "event_id": "r1-e00003"},
        "di": {"status": "accepted", "event_id": "r1-e00004", "did": {"kind": "wait"}, "changes": []},
    }},
    {"turn": 2, "actors": {"cy": {"status": "no_action", "event_id": "r2-e00001"}}},
]


@pytest.mark.req("world-builder-page/simple-view-story")
class RunStoryTests(unittest.TestCase):
    def test_events_carry_why_attempt_and_every_status_but_no_action(self):
        events = run_story.story_events(ROUNDS)
        self.assertEqual([e["event_id"] for e in events], ["r1-e00001", "r1-e00002", "r1-e00004"])
        self.assertIn("names no entity in this world", events[0]["why"])  # refused_because is blank for these
        self.assertEqual(events[0]["attempt"], "I tell the other groups I agree")
        self.assertIn("Information is not active yet", events[1]["checks"])
        self.assertNotIn("changed", events[2])  # an accepted move that changed nothing is still a move

    def test_prompt_shows_the_model_the_reason_and_the_attempt(self):
        events = run_story.story_events(ROUNDS)
        text = run_story.story_prompt([{"id": "ana", "label": "Ana"}], events, "Four groups decide.", [1, 2])[1]["content"]
        self.assertIn("names no entity in this world", text)
        self.assertIn("I tell the other groups I agree", text)

    def test_sentences_without_a_real_event_of_that_round_are_dropped(self):
        events = run_story.story_events(ROUNDS)
        parsed = {"rounds": [
            {"round": 1, "sentences": [{"text": "Ana tried to tell the others; the world has no such group.",
                                        "event_ids": ["r1-e00001"]},
                                       {"text": "Invented.", "event_ids": ["r9-e00001"]},
                                       {"text": "No citation.", "event_ids": []}]},
            {"round": 7, "sentences": [{"text": "Not a round of this run.", "event_ids": ["r1-e00001"]}]}]}
        out = run_story.validate_story(parsed, events, [1, 2])
        self.assertEqual([r["round"] for r in out["rounds"]], [1, 2])
        self.assertEqual(len(out["rounds"][0]["sentences"]), 1)
        self.assertEqual(out["dropped_sentences"], 2)
        # round 2 has only no_action rows: marked from the recording, not from the model's silence
        self.assertEqual(out["rounds"][1], {"round": 2, "sentences": [], "recorded": False, "told": False})

    def test_a_long_list_is_split_by_rounds_and_a_short_one_is_one_call(self):
        events = run_story.story_events(ROUNDS)
        self.assertEqual(len(run_story.slices(ROUNDS, events, [])), 1)
        many = [{"event_id": f"r{n}-e1", "round": n, "pad": "x" * 6000} for n in range(1, 41)]
        parts = run_story.slices([], many, [])
        self.assertGreater(len(parts), 1)
        self.assertEqual(sorted(e["round"] for p in parts for e in p), list(range(1, 41)))
        self.assertTrue(all(len({e["round"] for e in p}) <= run_story.SLICE_ROUNDS for p in parts))

    def test_a_failed_slice_is_reported_not_skipped(self):
        many = [{"turn": n, "actors": {"a": {"status": "accepted", "event_id": f"r{n}-e1", "did": {"kind": "k"},
                                            "said": "x" * 200, "changes": []}}} for n in range(1, 41)]
        replies = [Exception("boom"),
                   types.SimpleNamespace(content=json.dumps({"rounds": [{"round": 16, "sentences": [
                       {"text": "A moved.", "event_ids": ["r16-e1"]}]}]}))]
        calls = []

        def fake_call(model, messages, **kw):
            calls.append(kw["trace_id"])
            reply = replies[min(len(calls) - 1, 1)]
            if isinstance(reply, Exception):
                raise reply
            return reply

        fake = types.SimpleNamespace(call_llm=fake_call, safe_json_loads=json.loads)
        with mock.patch.dict(sys.modules, {"llm_client": fake}), mock.patch.object(run_story, "MAX_PROMPT_CHARS", 1500):
            story, _ = run_story.tell_run(many, people=[], world_sentence="w", model="m", trace_id="t", max_budget=0.1)
        self.assertGreater(len(calls), 1)
        self.assertEqual(story["not_told_rounds"], list(range(1, 16)))  # the first slice failed, and says so
        self.assertEqual(sum(1 for r in story["rounds"] if r["told"]), 1)


if __name__ == "__main__":
    unittest.main()
