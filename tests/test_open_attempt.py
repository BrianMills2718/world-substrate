"""Open attempts (docs/plans/open_attempt.md, slice S1): a resident says what it tries, a typed reading names the move,
and only the installed rules decide what it does. The airfield world and its rules are the bundle and rules writers'
own output (evidence/open-attempt/q23/after-fix), not hand-written fixtures; the model is faked here so the plumbing is
checked without a paid call."""
from __future__ import annotations

import json
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.run_authored_world import build_engine, run_world
from scripts.scaffold_world import load_bundle
from world_substrate import attempt as open_attempt

REPO = Path(__file__).resolve().parents[1]
AIRFIELD = REPO / "evidence/open-attempt/q23/after-fix"

ATTEMPTS = [
    "walk through the brick wall into the hangar",
    "fly the helicopter to the coast",
    "sing to the clouds until it rains",
    "wait",
]
READINGS = {
    ATTEMPTS[0]: {"kind": "move", "fields": [{"field": "to", "value": "hangar", "quoted_span": "into the hangar"},
                                             {"field": "way", "value": "brick-wall", "quoted_span": "the brick wall"}],
                  "nearest_kind": "move", "why": "walking somewhere is a move"},
    ATTEMPTS[1]: {"kind": "fly", "fields": [{"field": "aircraft", "value": "helicopter",
                                             "quoted_span": "the helicopter"}],
                  "nearest_kind": "fly", "why": "flying the aircraft"},
    ATTEMPTS[2]: {"kind": "none", "fields": [], "nearest_kind": "none", "why": "no kind is about weather"},
}


def _keys(value):
    if isinstance(value, dict):
        return set(value) | set().union(*(_keys(v) for v in value.values())) if value else set()
    if isinstance(value, list):
        return set().union(*(_keys(v) for v in value)) if value else set()
    return set()


class OpenAttemptTests(unittest.TestCase):
    def setUp(self):
        self.bundle = load_bundle(AIRFIELD / "bundle.json")
        self.rules = json.loads((AIRFIELD / "rules3.json").read_text())
        engine, model, _ = build_engine(self.bundle, self.rules)
        self.signatures = open_attempt.signatures_for(self.bundle, model.mechanics)
        self.entities = set(engine.world.entities)

    def test_schema_has_no_outcome(self):
        # A1: the interpreter can say what is tried, never whether it succeeds.
        schema = open_attempt.interpreter_schema(self.signatures)
        words = {k.lower() for k in _keys(schema["properties"])}
        for banned in ("success", "succeeds", "outcome", "works", "possible", "allowed", "result", "effect"):
            self.assertFalse(any(banned in w for w in words), (banned, words))
        self.assertEqual(sorted(s["kind"] for s in self.signatures), ["fly", "move"])
        self.assertEqual(schema["properties"]["kind"]["enum"], ["fly", "move", "wait", "none"])

    def test_reading_that_does_not_fit_the_world_is_unmatched_not_guessed(self):
        text = ATTEMPTS[1]
        good = open_attempt.read_interpretation(READINGS[text], text, self.signatures, self.entities)
        self.assertEqual((good["kind"], good["fields"]), ("fly", {"aircraft": "helicopter"}))
        for broken in (
            {**READINGS[text], "fields": [{"field": "aircraft", "value": "jet", "quoted_span": "the helicopter"}]},
            {**READINGS[text], "fields": [{"field": "aircraft", "value": "helicopter", "quoted_span": "a jet"}]},
            {**READINGS[text], "fields": []},
            {**READINGS[text], "kind": "teleport"},
            "not an object",
        ):
            reading = open_attempt.read_interpretation(broken, text, self.signatures, self.entities)
            self.assertTrue(reading.get("unmatched"), (broken, reading))
        envelope = open_attempt.envelope({"unmatched": True, "nearest_kind": "fly", "why": "x"}, actor="sam",
                                         attempt=text, base_revision=3, controller="test")
        self.assertEqual(envelope["kind"], open_attempt.UNMATCHED_KIND)
        self.assertIsNone(open_attempt.envelope({"kind": "wait"}, actor="sam", attempt="wait", base_revision=0,
                                                controller="test"))

    def test_residents_attempt_freely_and_only_the_rules_refuse(self):
        calls = {"resident": 0, "interpreter": []}
        fake = types.ModuleType("llm_client")
        fake.render_prompt = lambda path, **kwargs: [{"role": "user", "content": json.dumps(
            {"prompt": Path(path).name, **{k: v for k, v in kwargs.items() if k in ("attempt", "actions")}},
            default=str)}]

        def call_llm_json_schema(model, messages, schema, **kwargs):
            sent = json.loads(messages[0]["content"])
            if kwargs["task"] == "world-builder-concordia-resident":
                self.assertEqual(sent["prompt"], "concordia_resident_open_attempt.yaml")
                self.assertNotIn("action_id", schema["properties"])
                text = ATTEMPTS[calls["resident"]]
                calls["resident"] += 1
                return ({"belief": "I am in the office.", "attempt": text, "expected_effect": "something",
                         "work": "none", "reasoning": "my goal"}, types.SimpleNamespace(cost=0.001))
            self.assertEqual(kwargs["task"], open_attempt.TASK)
            self.assertEqual(sent["prompt"], "attempt_interpreter.yaml")
            calls["interpreter"].append(sent["attempt"])
            return READINGS[sent["attempt"]], types.SimpleNamespace(cost=0.0005)

        fake.call_llm_json_schema = call_llm_json_schema
        import scripts.concordia_residents  # noqa: F401  (Concordia imported outside patch.dict)
        with patch.dict(sys.modules, {"llm_client": fake}):
            trace, engine, _ = run_world(self.bundle, self.rules, policy="resident", model_name="fixture-model",
                                         max_turns=4, trace_id="fixture-trace", open_attempts=True)
        rows = [t["actors"]["sam"] for t in trace["transcript"]]
        # A wait is not read by the model; the three tries are.
        self.assertEqual(calls["interpreter"], ATTEMPTS[:3])
        # A3: walking into the wall is a move, and the move's own rule refuses it by the wall.
        self.assertEqual(rows[0]["did"]["kind"], "move")
        self.assertEqual(rows[0]["status"], "precondition_failed")
        self.assertIn("the way is passable", rows[0]["refused_because"])
        # A2: flying the helicopter binds to fly, never a safer move, and the rules refuse it from the office.
        self.assertEqual(rows[1]["did"], {"actor": "sam", "kind": "fly", "aircraft": "helicopter",
                                          "base_revision": 0, "controller": "live:resident"})
        self.assertIn("the aircraft is where the trainee is", rows[1]["refused_because"])
        # A4: a try that fits no rule changes nothing, is listed, and the resident is told nothing came of it.
        self.assertEqual(rows[2]["did"]["kind"], open_attempt.UNMATCHED_KIND)
        self.assertEqual(rows[2]["refused_because"], [])
        self.assertEqual(trace["summary"]["unmatched_attempts"], [
            {"round": 3, "actor": "sam", "attempt": ATTEMPTS[2], "nearest_kind": "none",
             "why": "no kind is about weather"}])
        self.assertTrue(any("nothing came of it" in n for n in trace["resident_memory"]["sam"]))
        self.assertIsNone(rows[3]["did"])
        self.assertEqual(rows[3]["attempt"]["reading"]["kind"], "wait")
        # Nothing was accepted, so the world never moved: refusals and unmatched tries do not bump the revision.
        self.assertEqual(engine.world.revision, 0)
        unmatched_events = [e for e in trace["engine_events"] if e["rule_id"] == "unsupported.unmatched-attempt"]
        self.assertEqual([e["status"] for e in unmatched_events], ["unsupported_action"])
        self.assertEqual(rows[2]["changes"], [])
        self.assertEqual(rows[2]["event_id"], unmatched_events[0]["event_id"])
        # The words travel with the recorded command, so a reader of the run sees exactly what was tried.
        unmatched_command = [c for c in engine.world.commands if c.get("action", {}).get("kind") == "unmatched-attempt"]
        self.assertEqual(unmatched_command[0]["action"]["attempt"], ATTEMPTS[2])
        self.assertEqual(engine.world.entities["sam"].location.location_id, "office")
        # The reading went in as the recorded command, so replay rebuilds the run without any model.
        with patch.dict(sys.modules, {"llm_client": None}):
            self.assertTrue(engine.replay()["ok"])
        self.assertAlmostEqual(trace["cost_usd"], 4 * 0.001 + 3 * 0.0005)

    def test_open_attempts_are_only_for_residents(self):
        with self.assertRaisesRegex(ValueError, "open_attempts needs the resident policy"):
            run_world(self.bundle, self.rules, policy="scripted", open_attempts=True)


if __name__ == "__main__":
    unittest.main()
