"""Ruling to rule: a confirmed ruling becomes a rule of the running world (ai-judge plan, slice J3).

Every model call is faked (see tests/test_judge.py): the game master's steps answer by schema name and the attempt
reader answers by who is trying. A run is played one round at a time with the previous round's state carried back, as
the page does.
"""
from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from unittest.mock import patch

import pytest

from scripts import judge as judge_mod
from scripts import rulings as rulings_mod
from scripts.run_authored_world import run_world
from tests.judge_worlds import BRIBE, coin_rule, port_two_traders, unwritable_rule
from tests.test_judge import FakeLlm, propose, review
from world_substrate import attempt as open_attempt

OFFER = "I hand Rosa 10 coins from my purse."
UNASKED = {"kind": "none", "fields": [], "nearest_kind": "none", "asks": "none", "names": ["rosa", "crate"],
           "why": "no kind hands over coins"}
HAND = {"kind": "hand-coins", "nearest_kind": "hand-coins", "asks": "none", "names": ["rosa"], "why": "hands coins",
        "fields": [{"field": "to", "value": "rosa", "quoted_span": "Rosa"},
                   {"field": "amount", "value": "10", "quoted_span": "10"}]}
MOVE = {"to": "rosa", "amount": 40}


class RoundsLlm(FakeLlm):
    """FakeLlm whose attempt reader answers by who is trying (`readings`, by actor)."""

    def __init__(self, *args, readings: dict | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self.readings = readings or {}

    def module(self):
        fake = super().module()
        inner, render = fake.call_llm_json_schema, fake.render_prompt

        def render_prompt(path, **kwargs):
            if "actor_id" in kwargs and "attempt" in kwargs:
                return [{"role": "user", "content": json.dumps({"actor": kwargs["actor_id"],
                                                                  "attempt": kwargs["attempt"]})}]
            return render(path, **kwargs)

        def call_llm_json_schema(model, messages, schema, **kwargs):
            if kwargs["task"] == open_attempt.TASK:
                sent = json.loads(messages[0]["content"])
                reading = {**self.readings[sent["actor"]], "coverage": {
                    "status": "complete", "action_spans": [sent["attempt"]], "unrepresented_spans": []}}
                return reading, __import__("types").SimpleNamespace(cost=0.0)
            return inner(model, messages, schema, **kwargs)

        fake.render_prompt, fake.call_llm_json_schema = render_prompt, call_llm_json_schema
        return fake

    def judge_calls(self) -> int:
        return len(self.calls)


def play(llm: RoundsLlm, rounds: list[dict], *, mode: str = "create", world=port_two_traders):
    """Play one round per entry of `rounds` ({"tries": {actor: words}, "decisions": [...]}), carrying state back.
    Returns the traces and the last engine."""
    bundle, rules = world()
    original = deepcopy((bundle, rules))
    from scripts import concordia_residents as cr

    traces, engine, last = [], None, None
    real_choose = cr.Residents.choose
    for number, step in enumerate(rounds):
        def choose(self_, actor, available, context, _tries=step.get("tries", {})):
            out = real_choose(self_, actor, available, context)
            return {**out, "attempt": _tries.get(actor, "wait")}

        carried = {} if last is None else dict(
            start_snapshot=last["final_snapshot"], turn_offset=number, resident_memory=last.get("resident_memory"),
            rulings=last.get("rulings"))
        with patch.dict(sys.modules, {"llm_client": llm.module()}), patch.object(cr.Residents, "choose", choose):
            last, engine, _ = run_world(bundle, rules, policy="resident", model_name="fixture-model", max_turns=1,
                                        trace_id="fixture-trace", open_attempts=True, judge=True,
                                        judge_rulings=mode, decisions=step.get("decisions"), **carried)
        json.dumps(last)
        traces.append(last)
    assert (bundle, rules) == original, "the world's own bundle and rules changed"
    return traces, engine


def row(trace: dict, actor: str, n: int = 0) -> dict:
    return trace["transcript"][n]["actors"][actor]


def coins(engine, who: str) -> int:
    return engine.world.material_dict()["entities"][who]["components"]["purse"]["coins"]


def confirming(move=MOVE, whose="rosa"):
    return {"propose": [propose(coin_rule(), move, whose=whose)], "review": [review("confirm")]}


class InstallTests(unittest.TestCase):
    @pytest.mark.req("ai-judge/a-confirmed-ruling-is-installed-after-the-rules-check-and-the-test-run")
    def test_a_confirmed_ruling_is_installed_after_the_rules_check_and_the_test_run(self):
        llm = RoundsLlm(confirming(), readings={"vik": UNASKED})
        [trace], engine = play(llm, [{"tries": {"vik": BRIBE}}])
        [ruling] = trace["rulings"]
        self.assertEqual((ruling["id"], ruling["status"], ruling["kind"], ruling["installed_round"]),
                         ("R1", "installed", "hand-coins", 1))
        self.assertIn("hand-coins", engine.registry.action_kinds())
        self.assertEqual(row(trace, "vik")["judge"]["tests"][0]["rules_check"], {"ok": True})
        self.assertEqual(row(trace, "vik")["judge"]["tests"][0]["test_run"]["status"], "accepted")
        self.assertEqual(row(trace, "vik")["judge"]["disposition"]["status"], "installed")
        self.assertEqual(trace["transcript"][0]["rulings"][0]["status"], "installed")
        # The world's own rules are untouched (play() checks the bundle and rules it was given) and the rule is the
        # engine's: it came through the registry, so the next round, built from the snapshot, has it (see below).
        self.assertEqual(engine.world.rule_versions, engine.registry.versions())

    @pytest.mark.req("ai-judge/a-ruling-that-needs-no-one-else-s-choice-settles-the-attempt-through-the-rule")
    def test_a_ruling_that_needs_no_one_else_s_choice_settles_the_attempt_through_the_rule(self):
        llm = RoundsLlm(confirming(whose="none"), readings={"vik": UNASKED})
        [trace], engine = play(llm, [{"tries": {"vik": BRIBE}}])
        settled = row(trace, "vik")["judge"]["disposition"]["settled"]
        self.assertEqual(settled["status"], "accepted")
        self.assertEqual([(c["path"], c["after"]) for c in settled["changes"] if c["path"].endswith("coins")],
                         [("entities.rosa.components.purse.coins", 40), ("entities.vik.components.purse.coins", 0)])
        self.assertEqual((coins(engine, "vik"), coins(engine, "rosa")), (0, 40))
        # The engine committed it under the installed rule; the judge wrote no outcome.
        self.assertEqual([e["rule_id"] for e in engine.world.events if e["rule_id"] == "hand-coins"], ["hand-coins"])
        self.assertTrue(row(trace, "vik")["changed"])

    @pytest.mark.req("ai-judge/a-ruling-that-needs-another-person-s-choice-reaches-that-person-under-the-rule")
    def test_a_ruling_that_needs_another_person_s_choice_reaches_that_person_under_the_rule(self):
        llm = RoundsLlm(confirming(), readings={"vik": UNASKED})
        [trace], engine = play(llm, [{"tries": {"vik": BRIBE}}])
        self.assertEqual((coins(engine, "vik"), coins(engine, "rosa")), (40, 0))  # nothing moved
        self.assertEqual(row(trace, "vik")["asked"], "rosa")
        self.assertTrue(any("asked you, in their words" in note for note in trace["resident_memory"]["rosa"]))
        # Her page now offers the installed rule's move, which is hers to choose.
        page = engine.discover("rosa")
        self.assertIn("hand-coins", {r["action"]["kind"] for r in page["available"] + page["blocked"]})

    @pytest.mark.req("ai-judge/a-later-attempt-the-rule-covers-is-decided-by-the-rule-and-the-judge-is-not-asked")
    def test_a_later_attempt_the_rule_covers_is_decided_by_the_rule_and_the_judge_is_not_asked(self):
        llm = RoundsLlm(confirming(), readings={"vik": UNASKED, "ines": HAND})
        traces, engine = play(llm, [{"tries": {"vik": BRIBE}}, {"tries": {"ines": OFFER}}])
        later = row(traces[1], "ines")
        self.assertEqual((later["did"]["kind"], later["status"]), ("hand-coins", "accepted"))
        self.assertNotIn("judge", later)
        self.assertEqual(llm.judge_calls(), 2)  # propose and review for Vik's offer only
        self.assertEqual((coins(engine, "ines"), coins(engine, "rosa")), (20, 10))
        # The ruling lists the later attempt it decided, so the run page links them.
        listed = traces[1]["rulings"][0]["attempts"]
        self.assertEqual([(a["actor"], a["state"], a.get("by_rule")) for a in listed],
                         [("vik", "routed", None), ("ines", "accepted", True)])
        # The same rule refuses a hand-over its own check forbids, with the judge not asked.
        llm = RoundsLlm(confirming(), readings={"vik": UNASKED, "ines": {**HAND, "fields": [
            HAND["fields"][0], {"field": "amount", "value": "99", "quoted_span": "10"}]}})
        traces, engine = play(llm, [{"tries": {"vik": BRIBE}}, {"tries": {"ines": OFFER}}])
        refused = row(traces[1], "ines")
        self.assertEqual((refused["status"], refused["refused_because"]), ("precondition_failed",
                                                                          ["the giver holds that many coins"]))
        self.assertEqual(llm.judge_calls(), 2)

    @pytest.mark.req("ai-judge/a-continued-round-keeps-the-installed-rule")
    def test_a_continued_round_keeps_the_installed_rule(self):
        llm = RoundsLlm(confirming(), readings={"vik": UNASKED})
        traces, engine = play(llm, [{"tries": {"vik": BRIBE}}, {"tries": {}}, {"tries": {}}])
        self.assertIn("hand-coins", engine.registry.action_kinds())
        self.assertEqual(engine.world.rule_versions, engine.registry.versions())
        for trace in traces:
            self.assertEqual([(r["id"], r["status"]) for r in trace["rulings"]], [("R1", "installed")])
        self.assertEqual(llm.judge_calls(), 2)  # the later rounds asked nobody


class WaitTests(unittest.TestCase):
    def held(self, rounds=None, **kwargs):
        llm = RoundsLlm(confirming(), readings={"vik": UNASKED, "ines": HAND})
        steps = rounds or [{"tries": {"vik": BRIBE}}, {"tries": {"ines": OFFER}}]
        traces, engine = play(llm, steps, mode="wait", **kwargs)
        return llm, traces, engine

    @pytest.mark.req("ai-judge/a-held-ruling-changes-nothing-and-its-attempt-waits")
    def test_a_held_ruling_changes_nothing_and_its_attempt_waits(self):
        llm, [first, _], engine = self.held()
        self.assertEqual(first["rulings"][0]["status"], "held")
        self.assertEqual(row(first, "vik")["judge"]["disposition"], {"status": "held", "ruling_id": "R1"})
        self.assertNotIn("hand-coins", engine.registry.action_kinds())
        self.assertEqual((coins(engine, "vik"), coins(engine, "rosa")), (40, 0))
        self.assertNotIn("asked", row(first, "vik"))
        self.assertFalse(any("asked you" in n for n in first["resident_memory"]["rosa"]))
        self.assertTrue(any("waits for the world's owner to approve" in n for n in first["resident_memory"]["vik"]))

    @pytest.mark.req("ai-judge/a-later-identical-attempt-joins-the-held-ruling")
    def test_a_later_identical_attempt_joins_the_held_ruling(self):
        llm, [_, second], engine = self.held()
        joined = row(second, "ines")
        self.assertEqual((joined["status"], joined["ruling"]), ("pending_ruling", {"id": "R1", "state": "held"}))
        self.assertNotIn("judge", joined)
        self.assertEqual(llm.judge_calls(), 2)
        self.assertEqual([(a["actor"], a["state"]) for a in second["rulings"][0]["attempts"]],
                         [("vik", "pending"), ("ines", "pending")])
        self.assertEqual((coins(engine, "ines"), coins(engine, "rosa")), (30, 0))

    @pytest.mark.req("ai-judge/approving-installs-the-rule-and-settles-both-waiting-attempts")
    def test_approving_installs_the_rule_and_settles_both_waiting_attempts(self):
        llm, traces, engine = self.held([{"tries": {"vik": BRIBE}}, {"tries": {"ines": OFFER}},
                                         {"decisions": [{"id": "R1", "decision": "approve"}]}])
        third = traces[2]
        self.assertEqual(third["rulings"][0]["status"], "installed")
        self.assertEqual(third["rulings"][0]["decision"], "approved")
        events = third["transcript"][0]["ruling_events"]
        self.assertEqual([(e.get("result"), e.get("actor"), e.get("to")) for e in events[1:]],
                         [("routed", "vik", "rosa"), ("routed", "ines", "rosa")])
        self.assertIn("hand-coins", engine.registry.action_kinds())
        notes = " ".join(third["resident_memory"]["rosa"])
        self.assertIn("Vik asked you", notes)
        self.assertIn("Ines asked you", notes)
        self.assertEqual(llm.judge_calls(), 2)  # no new judge call

    @pytest.mark.req("ai-judge/approving-installs-the-rule-and-settles-both-waiting-attempts")
    def test_approving_settles_an_attempt_needing_no_one_else_through_the_engine(self):
        llm = RoundsLlm(confirming(whose="none"), readings={"vik": UNASKED})
        traces, engine = play(llm, [{"tries": {"vik": BRIBE}}, {"decisions": [{"id": "R1", "decision": "approve"}]}],
                              mode="wait")
        self.assertEqual((coins(engine, "vik"), coins(engine, "rosa")), (0, 40))
        [_, settled] = traces[1]["transcript"][0]["ruling_events"]
        self.assertEqual((settled["result"], settled["status"]), ("accepted", "accepted"))

    @pytest.mark.req("ai-judge/rejecting-refuses-both-waiting-attempts-and-names-the-ruling")
    def test_rejecting_refuses_both_waiting_attempts_and_names_the_ruling(self):
        llm = RoundsLlm(confirming(), readings={"vik": UNASKED, "ines": HAND})
        traces, engine = play(llm, [{"tries": {"vik": BRIBE}}, {"tries": {"ines": OFFER}},
                                    {"decisions": [{"id": "R1", "decision": "reject"}]},
                                    {"tries": {"ines": OFFER}}], mode="wait")
        third = traces[2]["transcript"][0]["ruling_events"]
        self.assertEqual([e["result"] for e in third[1:]], ["refused", "refused"])
        self.assertTrue(all("the ruling R1" in e["why"] and "was rejected" in e["why"] for e in third[1:]))
        self.assertEqual(traces[2]["rulings"][0]["status"], "rejected")
        self.assertNotIn("hand-coins", engine.registry.action_kinds())
        self.assertEqual((coins(engine, "vik"), coins(engine, "rosa")), (40, 0))
        # A later attempt of the same kind is refused the same way, and the judge is not asked again.
        again = row(traces[3], "ines")
        self.assertEqual(again["status"], "refused_ruling")
        self.assertIn("the ruling R1", again["refused_because"][0])
        self.assertEqual(llm.judge_calls(), 2)

    @pytest.mark.req("ai-judge/approving-installs-the-rule-and-settles-both-waiting-attempts")
    def test_a_decision_about_nothing_held_is_ignored(self):
        llm = RoundsLlm(confirming(), readings={"vik": UNASKED})
        traces, _ = play(llm, [{"tries": {"vik": BRIBE}}, {"decisions": [{"id": "R1", "decision": "reject"}]}])
        [ignored] = traces[1]["transcript"][0]["ruling_events"]
        self.assertIn("no held ruling", ignored["ignored"])
        self.assertEqual(traces[1]["rulings"][0]["status"], "installed")


class GapTests(unittest.TestCase):
    @pytest.mark.req("ai-judge/a-language-gap-is-refused-and-listed")
    def test_a_language_gap_is_refused_and_listed(self):
        bad = {"from": "rosa", "amount": 40}
        llm = RoundsLlm({"propose": [propose(unwritable_rule(), bad)],
                         "review": [review("revise", unwritable_rule(), bad)]}, readings={"vik": UNASKED})
        [trace], engine = play(llm, [{"tries": {"vik": BRIBE}}])
        disposition = row(trace, "vik")["judge"]["disposition"]
        self.assertEqual((disposition["status"], disposition["reason"]), ("language_gap", "no rule could express this"))
        [ruling] = trace["rulings"]
        self.assertEqual((ruling["status"], ruling["id"]), ("language_gap", "R1"))
        self.assertIn("from", ruling["error"])
        self.assertEqual(ruling["attempts"][0]["state"], "refused")
        self.assertEqual(engine.registry.action_kinds(), ("declare-crate", "inspect-crate", "sign-release"))
        self.assertEqual((coins(engine, "vik"), coins(engine, "rosa")), (40, 0))
        self.assertTrue(any("no rule could express this" in n for n in trace["resident_memory"]["vik"]))


class SettingTests(unittest.TestCase):
    def test_the_setting_is_one_of_two_and_defaults_to_create(self):
        self.assertEqual([rulings_mod.parse_mode(v) for v in (None, "", "create", "wait")],
                         ["create", "create", "create", "wait"])
        with self.assertRaises(ValueError):
            rulings_mod.parse_mode("sometimes")

    def test_decisions_and_rulings_are_checked_before_use(self):
        self.assertEqual(rulings_mod.parse_decisions([{"id": "R1", "decision": "approve", "x": 1}]),
                         [{"id": "R1", "decision": "approve"}])
        for bad in ({"id": "R1", "decision": "maybe"}, {"decision": "approve"}, "R1"):
            with self.assertRaises(ValueError):
                rulings_mod.parse_decisions([bad])
        with self.assertRaises(ValueError):
            rulings_mod.parse_rulings([{"id": "R1", "status": "strange"}])
