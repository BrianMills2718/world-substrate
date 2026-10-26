"""Build-quality fixes found by the 2026-10-26 airfield run (evidence/open-attempt/s2-airfield/): #253, #254, #255
and the build record's knock-on line."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import scripts.generate_causal_model as gcm
import scripts.world_builder_service as service

REPO = Path(__file__).resolve().parents[1]
BUNDLE = json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text())
CAUSAL = json.loads((REPO / "examples/world_authoring/orchard-causal-v0.json").read_text())
CAUSAL.pop("review", None)


def _with_effect(effect: dict) -> dict:
    causal = json.loads(json.dumps(CAUSAL))
    causal["mechanics"][0]["effects"].append(effect)
    return causal


class NoOpEffectTests(unittest.TestCase):
    """#254: an effect that cannot change anything is sent back to the rules writer."""

    def test_add_zero_and_set_to_itself_are_found(self):
        zero = _with_effect({"participant": "fruit", "path": "components.fruit.stage", "op": "add",
                             "value": {"literal": 0}})
        itself = _with_effect({"participant": "fruit", "path": "components.fruit.stage", "op": "set",
                               "value": {"participant": {"name": "fruit", "path": "components.fruit.stage"}}})
        self.assertEqual(len(gcm.no_op_effects(zero)), 1)
        self.assertIn("by 0", gcm.no_op_effects(zero)[0])
        self.assertIn("to its own value", gcm.no_op_effects(itself)[0])

    def test_real_effects_are_not_flagged(self):
        self.assertEqual(gcm.no_op_effects(CAUSAL), [])
        # Setting a field from a different participant's field is a real change.
        other = _with_effect({"participant": "fruit", "path": "location.location_id", "op": "set",
                              "value": {"participant": {"name": "actor", "path": "location.location_id"}}})
        self.assertEqual(gcm.no_op_effects(other), [])
        # False is not 0.
        flag = _with_effect({"participant": "fruit", "path": "components.fruit.stage", "op": "add",
                             "value": {"literal": False}})
        self.assertEqual(gcm.no_op_effects(flag), [])

    def test_saved_worlds_have_none(self):
        # The check runs only when rules are written, so a saved world never stops loading because of it; none of
        # the saved fixtures has one anyway.
        for path in sorted((REPO / "tests/fixtures").glob("*.json")):
            world = json.loads(path.read_text())
            causal = world.get("causal_model") or (world.get("build") or {}).get("causal_model")
            if isinstance(causal, dict):
                self.assertEqual(gcm.no_op_effects(causal), [], path.name)

    def test_the_rules_writer_gets_one_repair_naming_the_effect(self):
        bad = _with_effect({"participant": "fruit", "path": "components.fruit.stage", "op": "set",
                            "value": {"participant": {"name": "fruit", "path": "components.fruit.stage"}}})
        answers = [SimpleNamespace(content=json.dumps(bad)), SimpleNamespace(content=json.dumps(CAUSAL))]
        calls = []

        def fake_call(model, messages, **kwargs):
            calls.append(messages)
            return answers[len(calls) - 1]

        # llm_client is imported inside the call; a stand-in module keeps this test free of the real client.
        fake = SimpleNamespace(call_llm=fake_call, safe_json_loads=json.loads)
        with patch.dict("sys.modules", {"llm_client": fake}):
            out, _ = gcm.generate_causal_model(BUNDLE)
        self.assertEqual(len(calls), 2)
        self.assertIn("change nothing", calls[1][-1]["content"])
        self.assertIn("orchard.action.pick", calls[1][-1]["content"])
        self.assertEqual(gcm.no_op_effects(out), [])


class AttemptRankTests(unittest.TestCase):
    """#253: on a score tie the builder keeps a test run that did not circle and offered every move."""

    def test_circling_loses_to_more_stalled_people(self):
        circling = {"circling": True, "never_offered": ["move"], "stalled_actors": ["mechanic"],
                    "idle_actors": ["mechanic"]}
        moving = {"circling": False, "never_offered": [], "stalled_actors": ["dispatcher", "sam"]}
        self.assertGreater(service._attempt_rank(2, moving), service._attempt_rank(2, circling))
        # The score still comes first.
        self.assertGreater(service._attempt_rank(3, circling), service._attempt_rank(2, moving))

    def test_never_offered_comes_before_idle_counts(self):
        offers_all = {"never_offered": [], "stalled_actors": ["a", "b"]}
        misses_one = {"never_offered": ["fly"], "stalled_actors": []}
        self.assertGreater(service._attempt_rank(2, offers_all), service._attempt_rank(2, misses_one))


class KnockOnRecordTests(unittest.TestCase):
    """The build record says which knock-on processes the rules have, or that there are none."""

    def test_sentence_names_knock_on_processes_or_their_absence(self):
        row = {"ok": True, "accepted_actions": 4, "turns": 3, "active_at_end": True}
        self.assertNotIn("knock-on", service._dry_run_sentence(row, "ongoing"))
        self.assertIn("nothing sets off a knock-on effect",
                      service._dry_run_sentence({**row, "knock_on_processes": []}, "ongoing"))
        self.assertIn("knock-on effects: glass breaks",
                      service._dry_run_sentence({**row, "knock_on_processes": ["glass-breaks"]}, "ongoing"))

    def test_only_immediately_processes_count(self):
        causal = {"processes": [{"process_id": "dries", "timing": "each_round"}, {"process_id": "regrows"},
                                {"process_id": "glass-breaks", "timing": "immediately"}]}
        self.assertEqual(service._knock_on_processes(causal), ["glass-breaks"])

    def test_prompt_asks_for_knock_on_processes(self):
        rules = " ".join(gcm._context(BUNDLE)["authority_rules"])
        self.assertIn("timing immediately", rules)
        self.assertIn("never add or subtract 0", rules)


class RetryWordingTests(unittest.TestCase):
    """#255: the progress line claims a stronger model only when the retry uses a different one."""

    def test_label_follows_the_configured_model(self):
        with patch.object(service, "RULES_RETRY_MODEL", "openrouter/x/same"):
            self.assertEqual(service._retry_label("openrouter/x/same"), "Rewriting the rules")
            self.assertEqual(service._retry_label("openrouter/x/cheap"), "Rewriting the rules with a stronger model")


if __name__ == "__main__":
    unittest.main()
