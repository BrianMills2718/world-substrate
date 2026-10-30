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

from scripts.run_authored_world import build_engine, mark_only_fillers, run_world
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

    def _run_with_unreadable(self, error_name):
        """The second attempt's reading fails with llm_client's `error_name`; the rest read as in the test above."""
        fake = types.ModuleType("llm_client")
        fake.LLMError = type("LLMError", (Exception,), {})
        fake.LLMBudgetExceededError = type("LLMBudgetExceededError", (fake.LLMError,), {})
        fake.render_prompt = lambda path, **kwargs: [{"role": "user", "content": json.dumps(
            {"prompt": Path(path).name, **{k: v for k, v in kwargs.items() if k == "attempt"}}, default=str)}]
        said = iter(ATTEMPTS)

        def call_llm_json_schema(model, messages, schema, **kwargs):
            sent = json.loads(messages[0]["content"])
            if kwargs["task"] == "world-builder-concordia-resident":
                return ({"belief": "I am in the office.", "attempt": next(said), "expected_effect": "something",
                         "work": "none", "reasoning": "my goal"}, types.SimpleNamespace(cost=0.001))
            if sent["attempt"] == ATTEMPTS[1]:
                raise getattr(fake, error_name)("Empty content from LLM (native JSON schema structured)")
            return READINGS[sent["attempt"]], types.SimpleNamespace(cost=0.0005)

        fake.call_llm_json_schema = call_llm_json_schema
        import scripts.concordia_residents  # noqa: F401
        with patch.dict(sys.modules, {"llm_client": fake}):
            return run_world(self.bundle, self.rules, policy="resident", model_name="fixture-model", max_turns=3,
                             trace_id="fixture-trace", open_attempts=True)

    def test_an_attempt_the_reader_cannot_read_is_listed_and_the_round_goes_on(self):
        # Pencil nEEW93EirxNe (evidence/declared-laws/s2-pencil-3/TRACE_READ.md): one unread attempt failed 4 rounds.
        trace, engine, _ = self._run_with_unreadable("LLMError")
        rows = [t["actors"]["sam"] for t in trace["transcript"]]
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[1]["did"]["kind"], open_attempt.UNMATCHED_KIND)
        self.assertTrue(rows[1]["attempt"]["reading"]["unread"])
        self.assertIn("could not be read: Empty content", rows[1]["attempt"]["reading"]["why"])
        self.assertEqual(rows[2]["did"]["kind"], open_attempt.UNMATCHED_KIND)  # round 3 still ran
        self.assertEqual(engine.world.entities["sam"].location.location_id, "office")

    def test_running_out_of_allowance_still_stops_the_run(self):
        with self.assertRaises(Exception) as caught:
            self._run_with_unreadable("LLMBudgetExceededError")
        self.assertEqual(type(caught.exception).__name__, "LLMBudgetExceededError")

    def test_open_attempts_are_only_for_residents(self):
        with self.assertRaisesRegex(ValueError, "open_attempts needs the resident policy"):
            run_world(self.bundle, self.rules, policy="scripted", open_attempts=True)


if __name__ == "__main__":
    unittest.main()


# --- Slice S2: knock-on effects (plan piece 2, checks A5 and A6) -----------------------------------------------
# The glass world below is a declared fixture, written here because it exercises the engine's settle loop (waves,
# parents, cap), not generation; the canonical run uses the rules writer's own output.

def _lit(v):
    return {"literal": v}


def _it(path):
    return {"participant": {"name": "it", "path": path}}


GLASS_BUNDLE = {
    "schema_version": "world-substrate-authoring-bundle/v0",
    "world": {"id": "glass-desk", "label": "A glass on a desk", "location": "study",
              "summary": "Sam can push a glass of water off a desk; the neighbour next door can hear it break."},
    "components": [
        {"name": "glass", "fields": [
            {"name": "on_desk", "type": "boolean", "default": True},
            {"name": "height", "type": "integer", "default": 1},
            {"name": "fragile", "type": "boolean", "default": True},
            {"name": "fell", "type": "boolean", "default": False},
            {"name": "broken", "type": "boolean", "default": False},
            {"name": "water", "type": "integer", "default": 1},
            {"name": "sound", "type": "entity_ref", "default": "crash-sound"},
        ]},
        {"name": "floor", "fields": [{"name": "wet", "type": "boolean", "default": False}]},
        {"name": "information", "fields": [
            {"name": "content", "type": "string", "default": "a sound"},
            {"name": "source_id", "type": "string", "default": "unknown"},
            {"name": "channel_id", "type": "string", "default": "air"},
            {"name": "visibility", "type": "string", "default": "public"},
            {"name": "active", "type": "boolean", "default": False},
        ]},
    ],
    "actions": [{"kind": "push", "description": "Push something.", "fields": [{"name": "thing", "type": "entity_ref"}]}],
    "entities": [
        {"id": "study", "label": "Study", "categories": ["place"], "components": {}},
        {"id": "next-door", "label": "Next door", "categories": ["place"], "components": {}},
        {"id": "sam", "label": "Sam", "categories": ["actor"], "components": {}, "location": "study"},
        {"id": "neighbour", "label": "Neighbour", "categories": ["actor"], "components": {}, "location": "next-door"},
        {"id": "glass", "label": "Glass of water", "categories": ["glass"], "location": "study",
         "components": {"glass": {"on_desk": True, "height": 1, "fragile": True, "fell": False, "broken": False,
                                  "water": 1, "sound": "crash-sound"}}},
        {"id": "study-floor", "label": "Study floor", "categories": ["floor"], "location": "study",
         "components": {"floor": {"wet": False}}},
        # The crash carries through the wall: a public information item next door, silent until the glass breaks.
        {"id": "crash-sound", "label": "Crash of breaking glass", "categories": ["sound"], "location": "next-door",
         "components": {"information": {"content": "a crash of breaking glass", "source_id": "glass",
                                        "channel_id": "through-the-wall", "visibility": "public",
                                        "active": False}}},
    ],
    "presentation": {"assets": {}, "category_assets": {}, "station_roles": {}},
}

GLASS_SELECTOR = {"categories": ["glass"], "components": ["glass"]}


def _process(pid, checks, effects, participants=None, timing="immediately", selector=GLASS_SELECTOR):
    row = {"process_id": pid, "rationale": pid, "selector": selector, "checks": checks, "effects": effects,
           "timing": timing}
    if participants:
        row["participants"] = participants
    return row


GLASS_RULES = {
    "schema_version": "world-substrate-causal-model/v0",
    "mechanics": [{
        "schema_version": "world-substrate-action-mechanic/v0",
        "mechanic_id": "push-thing", "version": "1", "action_kind": "push",
        "rationale": "Pushing a glass slides it off the desk.",
        "actor_selector": {"categories": ["actor"], "components": []},
        "participants": {"thing": GLASS_SELECTOR}, "parameters": {},
        "checks": [{"label": "the glass is on the desk", "left": {"participant": {"name": "thing",
                    "path": "components.glass.on_desk"}}, "op": "eq", "right": _lit(True)}],
        "effects": [{"participant": "thing", "path": "components.glass.on_desk", "op": "set", "value": _lit(False)}],
        "limits": ["Only a glass on the desk can be pushed."],
        "tests": ["Pushing the glass leaves it off the desk."], "semantic_bindings": ["thing is what is pushed"],
    }],
    "terminal": None,
    "processes": [
        _process("falls", [
            {"label": "nothing holds it up", "left": _it("components.glass.on_desk"), "op": "eq", "right": _lit(False)},
            {"label": "it is above the floor", "left": _it("components.glass.height"), "op": "gt", "right": _lit(0)},
        ], [
            {"participant": "it", "path": "components.glass.height", "op": "set", "value": _lit(0)},
            {"participant": "it", "path": "components.glass.fell", "op": "set", "value": _lit(True)},
        ]),
        _process("breaks", [
            {"label": "it is fragile", "left": _it("components.glass.fragile"), "op": "eq", "right": _lit(True)},
            {"label": "it fell", "left": _it("components.glass.fell"), "op": "eq", "right": _lit(True)},
            {"label": "it is whole", "left": _it("components.glass.broken"), "op": "eq", "right": _lit(False)},
        ], [{"participant": "it", "path": "components.glass.broken", "op": "set", "value": _lit(True)}]),
        _process("spills", [
            {"label": "it broke", "left": _it("components.glass.broken"), "op": "eq", "right": _lit(True)},
            {"label": "it held water", "left": _it("components.glass.water"), "op": "gt", "right": _lit(0)},
        ], [
            {"participant": "it", "path": "components.glass.water", "op": "set", "value": _lit(0)},
            {"participant": "floor", "path": "components.floor.wet", "op": "set", "value": _lit(True)},
        ], participants={"floor": {"link": "co_located", "selector": {"categories": ["floor"],
                                                                      "components": ["floor"]}}}),
        _process("crash-sound", [
            {"label": "it broke", "left": _it("components.glass.broken"), "op": "eq", "right": _lit(True)},
        ], [{"participant": "noise", "path": "components.information.active", "op": "set", "value": _lit(True)}],
            participants={"noise": {"link": "ref:glass.sound", "selector": {"categories": ["sound"],
                                                                         "components": ["information"]}}}),
    ],
}


def _push(engine):
    offered = engine.discover("sam", kind="push")["available"]
    return engine.submit(dict(offered[0]["action"], controller="test"))


class KnockOnEffectTests(unittest.TestCase):
    def test_glass_chain_completes_in_one_moment(self):  # A5 (declared fixture)
        engine, _, _ = build_engine(GLASS_BUNDLE, GLASS_RULES)
        result = _push(engine)
        self.assertEqual(result["status"], "accepted")
        push = result["event"]
        by_rule = {e["rule_id"]: e for e in result["reactions"]}
        self.assertEqual([e["rule_id"] for e in result["reactions"]], ["falls", "breaks", "spills", "crash-sound"])
        self.assertEqual(by_rule["falls"]["causal_parent_event_ids"], [push["event_id"]])
        self.assertEqual(by_rule["breaks"]["causal_parent_event_ids"], [by_rule["falls"]["event_id"]])
        self.assertEqual(by_rule["spills"]["causal_parent_event_ids"], [by_rule["breaks"]["event_id"]])
        self.assertEqual(by_rule["crash-sound"]["causal_parent_event_ids"], [by_rule["breaks"]["event_id"]])
        # One moment: one command, no tick passed, every event caused by that command.
        self.assertEqual(len(engine.world.commands), 1)
        self.assertEqual({e["cause"] for e in engine.world.events}, {push["cause"]})
        self.assertEqual({e["tick"] for e in engine.world.events}, {0})
        floor = engine.world.entities["study-floor"].as_dict()["components"]["floor"]
        self.assertTrue(floor["wet"])
        # Judged separately: the neighbour hears it through information, an observation and not a sixth event.
        heard = engine.observe("neighbour")
        self.assertIn("crash-sound", json.dumps(heard))
        self.assertEqual(len(engine.world.events), 5)
        self.assertTrue(engine.replay()["ok"])

    def test_run_record_and_round_picture_show_each_reaction_with_its_cause(self):
        from scripts.run_authored_world import render_run
        trace, _, compiled = run_world(GLASS_BUNDLE, GLASS_RULES, policy="scripted", max_turns=1)
        reactions = trace["transcript"][0]["reactions"]
        self.assertEqual([(r["rule_id"], r["caused_by_rule"]) for r in reactions],
                         [("falls", ["push-thing"]), ("breaks", ["falls"]), ("spills", ["breaks"]),
                          ("crash-sound", ["breaks"])])
        self.assertEqual(trace["transcript"][0]["world_changes"], [])
        kept = {e["event_id"] for e in trace["engine_events"]}
        self.assertLessEqual({p for r in reactions for p in r["caused_by"]}, kept)
        html = render_run(GLASS_BUNDLE, trace, compiled)
        frames = json.loads(html.split("const FRAMES=", 1)[1].split(";const PROFILE=", 1)[0])
        self.assertEqual(frames[0]["reactions"][1], {"rule": "breaks", "after": ["falls"]})
        self.assertIn("(after ", html)

    def test_state_panel_lists_each_reaction_in_its_moment_with_its_cause(self):
        import tempfile
        sys.path.insert(0, str(REPO / "spikes/any-scenario-2026-10"))
        from render_run import state_rounds
        engine, _, _ = build_engine(GLASS_BUNDLE, GLASS_RULES)
        _push(engine)
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp)
            (run_dir / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in engine.world.events))
            (run_dir / "attempts.jsonl").write_text("")
            (run_dir / "summary.json").write_text("{}")
            rows = state_rounds(run_dir, GLASS_BUNDLE, 1)[0]["events"]
        self.assertEqual([r["rule"] for r in rows], ["push-thing", "falls", "breaks", "spills", "crash-sound"])
        self.assertNotIn("after", rows[0])
        self.assertEqual([p["rule"] for p in rows[2]["after"]], ["falls"])
        self.assertEqual([p["rule"] for p in rows[4]["after"]], ["breaks"])

    def test_reactions_do_not_run_each_round(self):
        engine, _, _ = build_engine(GLASS_BUNDLE, GLASS_RULES)
        engine.world.entities["glass"].components["glass"].on_desk = False
        self.assertEqual(engine.advance(1)["events"], [])

    def _domino_engine(self, wind=False):
        # A row of 40 glasses where each one's fall knocks over the next: more than 32 reactions in one moment.
        bundle = json.loads(json.dumps(GLASS_BUNDLE))
        bundle["components"][0]["fields"].append({"name": "next", "type": "entity_ref", "default": "glass-00"})
        glasses = [f"glass-{i:02d}" for i in range(40)]
        bundle["entities"] = [e for e in bundle["entities"] if e["id"] != "glass"] + [
            {"id": g, "label": g, "categories": ["glass"], "location": "study",
             "components": {"glass": {"on_desk": True, "height": 1, "fragile": False, "fell": False, "broken": False,
                                      "water": 0, "sound": "crash-sound",
                                      "next": glasses[(i + 1) % len(glasses)]}}}
            for i, g in enumerate(glasses)]
        rules = json.loads(json.dumps(GLASS_RULES))
        rules["processes"] = [_process("knocks-over-next", [
            {"label": "it fell", "left": _it("components.glass.on_desk"), "op": "eq", "right": _lit(False)},
            {"label": "the next one stands", "left": {"participant": {"name": "next", "path": "components.glass.on_desk"}},
             "op": "eq", "right": _lit(True)},
        ], [{"participant": "next", "path": "components.glass.on_desk", "op": "set", "value": _lit(False)}],
            participants={"next": {"link": "ref:glass.next", "selector": GLASS_SELECTOR}})]
        if wind:
            next(e for e in bundle["entities"] if e["id"] == "glass-00")["categories"].append("by-window")
            rules["processes"].insert(0, _process("wind-topples-first", [
                {"label": "it stands", "left": _it("components.glass.on_desk"), "op": "eq", "right": _lit(True)},
            ], [{"participant": "it", "path": "components.glass.on_desk", "op": "set", "value": _lit(False)}],
                timing="each_round", selector={"categories": ["glass", "by-window"], "components": ["glass"]}))
        return build_engine(bundle, rules)

    def test_a_chain_past_the_reaction_limit_is_refused_whole(self):  # A6
        engine, _, _ = self._domino_engine()
        before = engine.world.material_dict()
        offered = [o for o in engine.discover("sam", kind="push")["available"]
                   if o["action"]["thing"] == "glass-00"]
        result = engine.submit(dict(offered[0]["action"], controller="test"))
        self.assertEqual(result["status"], "reaction_limit")
        failed = [c for c in result["event"]["checks"] if not c["ok"]]
        self.assertEqual([c["label"] for c in failed], ["Knock-on effects settle within 32 reactions"])
        after = engine.world.material_dict()
        after.pop("revision"), before.pop("revision")
        self.assertEqual(after, before)
        self.assertEqual(len(engine.world.events), 1)
        self.assertTrue(engine.replay()["ok"])

    def test_a_reaction_that_keeps_itself_due_fires_once_per_moment(self):  # R4 once-per-pair
        rules = json.loads(json.dumps(GLASS_RULES))
        rules["processes"].append(_process("settles-on-floor", [
            {"label": "it fell", "left": _it("components.glass.on_desk"), "op": "eq", "right": _lit(False)},
        ], [{"participant": "it", "path": "components.glass.height", "op": "set", "value": _lit(0)}]))
        engine, _, _ = build_engine(GLASS_BUNDLE, rules)
        result = _push(engine)
        self.assertEqual(result["status"], "accepted")
        fired = [e for e in engine.world.events if e.get("rule_id") == "settles-on-floor"]
        self.assertEqual(len(fired), 1)  # still due after it fires; the once-per-pair rule stops it
        self.assertEqual(engine.world.entities["glass"].as_dict()["components"]["glass"]["height"], 0)
        self.assertTrue(engine.replay()["ok"])

    def test_a_round_whose_reactions_do_not_settle_is_undone(self):
        engine, _, _ = self._domino_engine(wind=True)
        before = engine.world.material_dict()
        result = engine.advance(1)
        self.assertEqual(result["status"], "reaction_limit")
        self.assertEqual([e["rule_id"] for e in result["events"]], ["wind-topples-first"])
        self.assertEqual(engine.world.material_dict(), before)
        self.assertEqual(engine.world.commands[-1]["status"], "reaction_limit")
        self.assertTrue(engine.replay()["ok"])

    def test_timing_must_be_known(self):
        rules = json.loads(json.dumps(GLASS_RULES))
        rules["processes"][0]["timing"] = "later"
        with self.assertRaisesRegex(Exception, "timing must be one of"):
            build_engine(GLASS_BUNDLE, rules)


class SpeakerSelfReferenceTests(unittest.TestCase):
    """2026-10-27 pencil iMrL2U84cLCS: "I try to sell one pencil" was refused in 9 of 15 rounds because the reader
    quoted the shop's id for the shop field instead of "I"."""

    SIGNATURES = [{"kind": "sell", "description": "sell one pencil",
                   "fields": [{"name": "shop", "type": "entity_ref"}, {"name": "customer", "type": "entity_ref"}]}]
    TEXT = "I try to sell one pencil to the Pencil customer."

    def _reading(self, shop_span):
        return {"kind": "sell", "why": "", "nearest_kind": "sell", "fields": [
            {"field": "shop", "value": "pencil-shop", "quoted_span": shop_span},
            {"field": "customer", "value": "customer", "quoted_span": "Pencil customer"}]}

    def test_the_speakers_own_id_needs_no_quoted_words(self):
        got = open_attempt.read_interpretation(self._reading("pencil-shop"), self.TEXT, self.SIGNATURES,
                                               {"pencil-shop", "customer"}, actor="pencil-shop")
        self.assertEqual(got.get("kind"), "sell")
        self.assertEqual(got["fields"], {"shop": "pencil-shop", "customer": "customer"})

    def test_someone_else_still_needs_their_words_in_the_attempt(self):
        got = open_attempt.read_interpretation(self._reading("pencil-shop"), self.TEXT, self.SIGNATURES,
                                               {"pencil-shop", "customer"}, actor="customer")
        self.assertTrue(got.get("unmatched"))


class OnlyFillerTests(unittest.TestCase):
    """s4w Waltzman, 2026-10-29: 7 of 20 attempts were lost because the reader had to quote words for fields only one
    thing can fill ("the meeting pace", "the time until the deadline"), which no one says when they speak."""

    def setUp(self):
        self.world = json.loads((REPO / "tests/fixtures/waltzman-s4-kept.json").read_text())
        engine, model, _ = build_engine(self.world["bundle"], self.world["causal_model"])
        self.plain = open_attempt.signatures_for(self.world["bundle"], model.mechanics)
        self.marked = mark_only_fillers(engine, model, json.loads(json.dumps(self.plain)))
        self.ids = set(engine.world.entities)

    def _read(self, signatures, row):
        return open_attempt.read_interpretation(row["reply"], row["attempt"], signatures, self.ids, row["actor"])

    def test_the_recorded_replies_all_read_once_the_only_filler_is_given(self):
        rows = self.world["attempt_replies"]
        self.assertEqual(sum(bool(self._read(self.plain, r).get("unmatched")) for r in rows), 7)
        self.assertEqual([r["call_id"] for r in rows if self._read(self.marked, r).get("unmatched")], [])
        pace = next(r for r in rows if r["call_id"] == 22712)
        self.assertEqual(self._read(self.marked, pace)["fields"]["meeting_pace"], "meeting-pace")

    def test_a_field_with_a_choice_still_needs_the_persons_words(self):
        open_fields = [f for s in self.marked for f in s["fields"] if f.get("type") == "entity_ref" and "only" not in f]
        self.assertTrue(open_fields)
        signatures = [{"kind": "tell", "fields": [{"name": "to", "type": "entity_ref"}]}]
        reply = {"kind": "tell", "why": "", "nearest_kind": "tell",
                 "fields": [{"field": "to", "value": "country-two", "quoted_span": ""}]}
        self.assertTrue(open_attempt.read_interpretation(reply, "I tell them", signatures, self.ids, "partnership")
                        .get("unmatched"))


class UnstatedAmountTests(unittest.TestCase):
    """2026-10-27 pencil c_SrKPfa3rpE: "I try to make leads from my clay and graphite" was refused in 3 rounds because
    the reader gave quantity='' or 'unspecified', or left quantity out."""

    SIGNATURES = [{"kind": "make-leads", "description": "make pencil leads",
                   "fields": [{"name": "to", "type": "entity_ref"}, {"name": "quantity", "type": "integer"}]}]
    TEXT = "I try to make leads from my clay and graphite."

    def _read(self, rows):
        reading = {"kind": "make-leads", "why": "", "nearest_kind": "make-leads", "fields": rows}
        return open_attempt.read_interpretation(reading, self.TEXT, self.SIGNATURES, {"lead-maker"}, actor="lead-maker")

    def test_an_amount_never_said_is_one(self):
        me = {"field": "to", "value": "lead-maker", "quoted_span": "my"}
        for amount in ({"field": "quantity", "value": "", "quoted_span": ""},
                       {"field": "quantity", "value": "unspecified", "quoted_span": ""},
                       # the reader prompt's own instruction for no amount: pencil czt5uoGw5t3L refused this 5 times
                       {"field": "quantity", "value": "1", "quoted_span": ""}, None):
            got = self._read([me] + ([amount] if amount else []))
            self.assertEqual(got.get("fields"), {"to": "lead-maker", "quantity": 1}, amount)

    def test_an_amount_said_in_words_the_reader_cannot_count_is_still_refused(self):
        got = self._read([{"field": "to", "value": "lead-maker", "quoted_span": "my"},
                          {"field": "quantity", "value": "some", "quoted_span": "my clay"}])
        self.assertTrue(got.get("unmatched"))
