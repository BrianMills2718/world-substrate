"""ai-judge plan J1 (docs/plans/ai_judge.md): the consequence report the judge will read, in two passes.

Pass 1, before any rule exists: the moves and checks open to the person acting and to each person the attempt names,
plus the current values of the people and things it names. Pass 2: a proposed rule goes through the rules check and is
test-run on a copy of the world, giving its net changes, blockers, chain length and stopping point, with the full
chain kept. Checked on the canonical example's port (tests/judge_worlds.py) and the J0 truck world; the model is faked
where a run needs one, so nothing here is paid.
"""
from __future__ import annotations

import json
import sys
import types
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

import pytest

from scripts import consequence_report as report
from scripts.run_authored_world import build_engine, run_world
from tests.judge_worlds import BRIBE, coin_rule, port, shove_rule, unwritable_rule
from tests.knock_on_worlds import truck_without_fuel
from world_substrate import attempt as open_attempt

REPO = Path(__file__).resolve().parents[1]
PEOPLE = {"vik", "rosa"}


def _failed(row):
    return [(c["label"], c.get("actual")) for c in row["checks"] if not c["ok"]]


class PassOneTests(unittest.TestCase):
    def setUp(self):
        self.engine, _, _ = build_engine(*port())

    @pytest.mark.req("ai-judge/pass-1-lists-the-moves-of-the-person-acting-and-each-person-named")
    def test_pass_1_lists_the_moves_of_the_person_acting_and_each_person_named(self):
        before = deepcopy(self.engine.world.material_dict())
        one = report.pass_one(self.engine, "vik", ["rosa", "crate"], people=PEOPLE)
        # Vik's own page cannot show Rosa's blocker: discover lists only the moves of the person asked.
        self.assertEqual(list(one["moves"]), ["vik", "rosa"])
        [sign] = [r for r in one["moves"]["rosa"]["blocked"] if r["action"]["kind"] == "sign-release"]
        self.assertEqual(sign["action"]["crate"], "crate")
        self.assertEqual(_failed(sign), [("the crate is inspected", False)])
        self.assertNotIn("sign-release", {r["action"]["kind"] for r in one["moves"]["vik"]["available"]
                                          + one["moves"]["vik"]["blocked"]})
        self.assertIn("inspect-crate", {r["action"]["kind"] for r in one["moves"]["rosa"]["available"]})
        # The facts: Vik holds 40 coins; Rosa and Vik are both at the customs desk; the crate is not inspected.
        self.assertEqual(list(one["values"]), ["vik", "rosa", "crate"])
        self.assertEqual(one["values"]["vik"]["components"]["purse"]["coins"], 40)
        self.assertEqual(one["values"]["vik"]["location"], one["values"]["rosa"]["location"])
        self.assertEqual(one["values"]["rosa"]["location"], "customs-desk")
        self.assertFalse(one["values"]["crate"]["components"]["cargo"]["inspected"])
        # Nothing to propagate yet, and nothing changed.
        self.assertEqual(self.engine.world.material_dict(), before)
        self.assertEqual(self.engine.world.events, [])

    @pytest.mark.req("ai-judge/pass-1-lists-the-moves-of-the-person-acting-and-each-person-named")
    def test_names_not_in_the_world_and_the_speaker_are_left_out(self):
        one = report.pass_one(self.engine, "vik", ["rosa", "vik", "no-such-thing", "rosa"], people=PEOPLE)
        self.assertEqual(one["named"], ["rosa"])
        self.assertEqual(list(one["values"]), ["vik", "rosa"])


class ReadingNamesTests(unittest.TestCase):
    def setUp(self):
        engine, model, _ = build_engine(*port())
        self.signatures = open_attempt.signatures_for(port()[0], model.mechanics)
        self.entities = set(engine.world.entities)

    @pytest.mark.req("ai-judge/an-unmatched-reading-names-who-and-what-the-attempt-names")
    def test_an_unmatched_reading_names_who_and_what_the_attempt_names(self):
        schema = open_attempt.interpreter_schema(self.signatures)
        self.assertIn("names", schema["required"])
        value = {"kind": "none", "fields": [], "nearest_kind": "none", "asks": "rosa",
                 "names": ["rosa", "crate", "vik", "the-harbour", "crate"], "why": "no kind hands over coins"}
        reading = open_attempt.read_interpretation(value, BRIBE, self.signatures, self.entities, "vik")
        self.assertEqual(reading["names"], ["rosa", "crate"])
        sent = open_attempt.envelope(reading, actor="vik", attempt=BRIBE, base_revision=0, controller="test")
        self.assertEqual((sent["kind"], sent["names"], sent["asks"]), (open_attempt.UNMATCHED_KIND, ["rosa", "crate"], "rosa"))

    @pytest.mark.req("ai-judge/an-unmatched-reading-names-who-and-what-the-attempt-names")
    def test_a_reply_recorded_before_names_existed_still_reads(self):
        value = {"kind": "none", "fields": [], "nearest_kind": "none", "asks": "rosa", "why": "older reply"}
        reading = open_attempt.read_interpretation(value, BRIBE, self.signatures, self.entities, "vik")
        self.assertEqual(reading["names"], ["rosa"])  # the one asked is named
        matched = open_attempt.read_interpretation(
            {"kind": "declare-crate", "fields": [{"field": "crate", "value": "crate", "quoted_span": "my crate"}],
             "nearest_kind": "declare-crate", "asks": "none", "names": ["crate"], "why": "declaring"},
            BRIBE, self.signatures, self.entities, "vik")
        self.assertNotIn("names", matched)  # a matched move is its typed fields only
        self.assertNotIn("names", open_attempt.envelope(matched, actor="vik", attempt=BRIBE, base_revision=0,
                                                        controller="test"))


class PassTwoTests(unittest.TestCase):
    @pytest.mark.req("ai-judge/the-coin-rule-moves-the-coins-and-nothing-else-follows")
    def test_the_coin_rule_moves_the_coins_and_nothing_else_follows(self):
        bundle, rules = port()
        engine, _, _ = build_engine(bundle, rules)
        two = report.pass_two(bundle, rules, engine, coin_rule(),
                              {"actor": "vik", "kind": "hand-coins", "to": "rosa", "amount": 40})
        self.assertEqual(two["rules_check"], {"ok": True})
        run = two["test_run"]
        self.assertEqual(run["status"], "accepted")
        self.assertEqual(run["net_changes"], [
            {"entity": "rosa", "path": "components.purse.coins", "before": 0, "after": 40},
            {"entity": "vik", "path": "components.purse.coins", "before": 40, "after": 0},
        ])
        self.assertEqual((run["blockers"], run["chain_length"]), ([], 0))
        self.assertEqual(run["stopping_point"], {"kind": "settled", "after_step": 0})
        self.assertEqual([e["rule_id"] for e in run["chain"]], ["hand-coins"])

    @pytest.mark.req("ai-judge/a-test-run-that-sets-off-a-blocked-chain-says-where-it-stopped")
    def test_a_test_run_that_sets_off_a_blocked_chain_says_where_it_stopped(self):
        bundle, rules = truck_without_fuel(40)
        engine, _, _ = build_engine(bundle, rules)
        two = report.pass_two(bundle, rules, engine, shove_rule(),
                              {"actor": "sam", "kind": "shove-lever", "thing": "lever"})
        run = two["test_run"]
        self.assertEqual((run["status"], run["chain_length"]), ("accepted", 40))
        stop = run["stopping_point"]
        self.assertEqual((stop["kind"], stop["after_step"], stop["rule_id"], stop["it"]),
                         ("blocked", 40, "truck-leaves", "truck"))
        self.assertEqual(stop["failed"], [{"check": "the truck has fuel", "actual": 0, "required": 0}])
        self.assertEqual(run["blockers"], [stop["blocker"]])
        # The full chain is kept: the move, then 40 knock-on steps in one moment, each citing its cause.
        steps = [s for e in run["chain"][1:] for s in e["reaction_steps"]]
        self.assertEqual([s["it"] for s in steps], [f"step-{n}" for n in range(1, 41)])
        self.assertTrue(all(s["caused_by"] for s in steps))
        # The truck never left: its fields are not among the net changes.
        self.assertNotIn("truck", {c["entity"] for c in run["net_changes"]})
        self.assertEqual(len(run["net_changes"]), 41)  # the lever and the 40 loading steps fell
        self.assertNotIn("chain", report.summary(two)["test_run"])

    @pytest.mark.req("ai-judge/a-rule-the-check-rejects-is-reported-and-not-run")
    def test_a_rule_the_check_rejects_is_reported_and_not_run(self):
        bundle, rules = port()
        engine, _, _ = build_engine(bundle, rules)
        two = report.pass_two(bundle, rules, engine, unwritable_rule(),
                              {"actor": "vik", "kind": "hand-coins", "from": "rosa", "amount": 40})
        self.assertFalse(two["rules_check"]["ok"])
        self.assertIn("from", two["rules_check"]["error"])
        self.assertIsNone(two["test_run"])

    @pytest.mark.req("ai-judge/a-rule-the-check-rejects-is-reported-and-not-run")
    def test_a_move_the_proposed_rule_refuses_is_reported_with_its_failed_checks(self):
        bundle, rules = port()
        engine, _, _ = build_engine(bundle, rules)
        two = report.pass_two(bundle, rules, engine, coin_rule(),
                              {"actor": "vik", "kind": "hand-coins", "to": "rosa", "amount": 50})
        run = two["test_run"]
        self.assertEqual((run["status"], run["net_changes"], run["chain_length"]), ("precondition_failed", [], 0))
        self.assertEqual(run["stopping_point"]["kind"], "refused")
        self.assertEqual([f["check"] for f in run["stopping_point"]["failed"]], ["the giver holds that many coins"])
        self.assertEqual(run["blockers"], [run["stopping_point"]["blocker"]])

    @pytest.mark.req("ai-judge/the-test-run-leaves-the-real-world-unchanged")
    def test_the_test_run_leaves_the_real_world_unchanged(self):
        bundle, rules = port()
        engine, _, _ = build_engine(bundle, rules)
        engine.submit({"actor": "rosa", "kind": "inspect-crate", "crate": "crate", "controller": "test",
                       "base_revision": 0})
        before = (deepcopy(engine.world.material_dict()), len(engine.world.events), engine.world.revision)
        bundle_before, rules_before = deepcopy(bundle), deepcopy(rules)
        two = report.pass_two(bundle, rules, engine, coin_rule(),
                              {"actor": "vik", "kind": "hand-coins", "to": "rosa", "amount": 40})
        self.assertEqual(two["test_run"]["status"], "accepted")
        # The copy starts from the world as it is now (after the inspection), not from the start.
        self.assertEqual(two["test_run"]["from_revision"], engine.world.revision)
        self.assertEqual((engine.world.material_dict(), len(engine.world.events), engine.world.revision), before)
        self.assertEqual((bundle, rules), (bundle_before, rules_before))
        self.assertNotIn("hand-coins", engine.registry.action_kinds())


class RunRecordTests(unittest.TestCase):
    """A run records pass 1 with each unmatched attempt, at the moment it was tried."""

    def _run(self):
        bundle, rules = port()
        fake = types.ModuleType("llm_client")
        fake.render_prompt = lambda path, **kwargs: [{"role": "user", "content": "{}"}]

        def call_llm_json_schema(model, messages, schema, **kwargs):
            if kwargs["task"] == open_attempt.TASK:
                return ({"kind": "none", "fields": [], "nearest_kind": "none", "asks": "rosa",
                         "names": ["rosa", "crate"], "why": "no kind hands over coins"},
                        types.SimpleNamespace(cost=0.0))
            return ({"belief": "b", "attempt": "wait", "expected_effect": "e", "work": "none", "reasoning": "r"},
                    types.SimpleNamespace(cost=0.0))

        fake.call_llm_json_schema = call_llm_json_schema
        from scripts import concordia_residents as cr

        real_choose = cr.Residents.choose

        def choose(self_, actor, available, context):
            out = real_choose(self_, actor, available, context)
            return {**out, "attempt": BRIBE} if actor == "vik" else out

        with patch.dict(sys.modules, {"llm_client": fake}), patch.object(cr.Residents, "choose", choose):
            trace, engine, _ = run_world(bundle, rules, policy="resident", model_name="fixture-model", max_turns=1,
                                         trace_id="fixture-trace", open_attempts=True)
        return trace, engine

    @pytest.mark.req("ai-judge/a-run-records-pass-1-with-each-unmatched-attempt")
    def test_a_run_records_pass_1_with_each_unmatched_attempt(self):
        trace, engine = self._run()
        row = trace["transcript"][0]["actors"]["vik"]
        self.assertEqual(row["did"]["kind"], open_attempt.UNMATCHED_KIND)
        self.assertEqual(row["did"]["names"], ["rosa", "crate"])
        one = row["consequence"]["pass_one"]
        [sign] = [r for r in one["moves"]["rosa"]["blocked"] if r["action"]["kind"] == "sign-release"]
        self.assertEqual(_failed(sign), [("the crate is inspected", False)])
        self.assertEqual(one["values"]["vik"]["components"]["purse"]["coins"], 40)
        [listed] = trace["summary"]["unmatched_attempts"]
        self.assertEqual(listed["names"], ["rosa", "crate"])
        self.assertEqual(listed["event_id"], row["event_id"])
        # The run record is JSON, and replay needs no model.
        json.dumps(trace)
        with patch.dict(sys.modules, {"llm_client": None}):
            self.assertTrue(engine.replay()["ok"])


if __name__ == "__main__":
    unittest.main()
