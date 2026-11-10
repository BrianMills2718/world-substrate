"""The judge: Concordia's game master rules on an attempt no installed rule covers (ai-judge plan, slice J2).

Every model call is faked: a stand-in `llm_client` module answers each resolution step by its schema name
(`world_substrate_judge_propose`, `_review`, `_final`) and records the document Concordia's EventResolution
assembled, so the tests read exactly what the game master was given.
"""
from __future__ import annotations

import json
import sys
import types
import unittest
from copy import deepcopy
from unittest.mock import patch

import pytest

from scripts import consequence_report as report
from scripts import judge as judge_mod
from scripts.run_authored_world import build_engine, run_world
from tests.judge_worlds import BRIBE, blocked_chain, coin_rule, empty_purse, long_line, port, press_rule, shove_rule, unwritable_rule
from world_substrate import attempt as open_attempt

PEOPLE = ["vik", "rosa"]


def _resident(attempt: str = "wait") -> dict:
    return {"belief": "b", "attempt": attempt, "expected_effect": "e", "work": "none", "reasoning": "r"}


class FakeLlm:
    """A stand-in llm_client: judge steps answer from `answers` (a list per step, in order); the interpreter and the
    residents answer as given. Every judge call is kept with the document it was sent."""

    def __init__(self, answers: dict | None = None, reading: dict | None = None, fail: bool = False):
        self.answers = {k: list(v) for k, v in (answers or {}).items()}
        self.reading = reading
        self.fail = fail
        self.calls: list[dict] = []
        self.texts: list[dict] = []

    def module(self) -> types.ModuleType:
        fake = types.ModuleType("llm_client")

        def render_prompt(path, **kwargs):
            if "document" in kwargs:
                return [{"role": "system", "content": f"step {kwargs['step']} for {kwargs['actor']}"},
                        {"role": "user", "content": kwargs["document"]}]
            return [{"role": "user", "content": "{}"}]

        def call_llm_json_schema(model, messages, schema, **kwargs):
            if kwargs["task"] == judge_mod.TASK:
                name = kwargs["schema_name"].removeprefix("world_substrate_judge_")
                self.calls.append({"name": name, "model": model, "messages": messages, "schema": schema, **kwargs})
                if self.fail:
                    raise RuntimeError("provider down")
                return self.answers[name].pop(0), types.SimpleNamespace(cost=0.01)
            if kwargs["task"] == open_attempt.TASK:
                return self.reading, types.SimpleNamespace(cost=0.0)
            return _resident(), types.SimpleNamespace(cost=0.0)

        def call_llm(model, messages, **kwargs):
            self.texts.append({"model": model, "messages": messages, **kwargs})
            return types.SimpleNamespace(content="The crate goes through.\nNext line", cost=0.002)

        fake.render_prompt = render_prompt
        fake.call_llm_json_schema = call_llm_json_schema
        fake.call_llm = call_llm
        return fake

    def document(self, n: int) -> str:
        return self.calls[n]["messages"][-1]["content"]


def propose(rule=None, move=None, whose="none", ruling="r"):
    return {"facts": ["vik holds 40 coins"], "blockers": ["sign-release: the crate is inspected"], "whose_choice": whose,
            "ruling": ruling, "proposed_rule": json.dumps(rule) if rule else "",
            "test_move": json.dumps(move) if move else "", "reasoning": "why"}


def review(decision, rule=None, move=None, why="the test run shows it"):
    return {"decision": decision, "why": why, "revised_rule": json.dumps(rule) if rule else "",
            "revised_test_move": json.dumps(move) if move else ""}


def _judge(llm: FakeLlm, world=port, actor="vik", attempt=BRIBE, named=("rosa", "crate"), people=PEOPLE):
    bundle, rules = world()
    engine, _, _ = build_engine(bundle, rules)
    before = (deepcopy(engine.world.material_dict()), engine.world.revision, set(engine.registry.action_kinds()))
    one = report.pass_one(engine, actor, list(named), people=set(people))
    with patch.dict(sys.modules, {"llm_client": llm.module()}):
        record = judge_mod.judge(bundle, rules, engine, actor=actor, attempt=attempt, pass_one=one, people=people,
                                 model="fixture-model", trace_id="fixture-trace", max_budget=0.5)
    # The judge only reads the world: nothing is installed and nothing changes.
    after = (engine.world.material_dict(), engine.world.revision, set(engine.registry.action_kinds()))
    assert after == before, "the judge changed the world"
    json.dumps(record)
    return record


class GameMasterTests(unittest.TestCase):
    @pytest.mark.req("ai-judge/the-game-master-reads-the-whole-world-and-pass-1-and-resolves-the-putative-event")
    def test_the_game_master_reads_the_whole_world_and_pass_1_and_resolves_the_putative_event(self):
        llm = FakeLlm({"propose": [propose(whose="rosa", ruling="Rosa decides whether to take the coins.")]})
        record = _judge(llm)
        [call] = llm.calls
        self.assertEqual((call["name"], call["model"], call["trace_id"], call["max_budget"]),
                         ("propose", "fixture-model", "fixture-trace", 0.5))
        self.assertEqual(call["schema"], judge_mod.PROPOSE_SCHEMA)
        doc = llm.document(0)
        # Concordia's EventResolution assembled it: the two context components, then the putative event.
        self.assertIn("The world:", doc)
        self.assertIn("What the engine worked out (the consequence report):", doc)
        self.assertIn(f"Putative event to resolve:  vik: {BRIBE}", doc)
        self.assertLess(doc.index("The world:"), doc.index("What the engine worked out"))
        self.assertLess(doc.index("What the engine worked out"), doc.index("Putative event to resolve"))
        # The whole world: its description, things, installed rules and current values.
        self.assertIn("Vik, a trader, has 40 coins", doc)
        self.assertIn("The officer signs the release once the crate is inspected.", doc)
        self.assertIn("Every thing and its current values (revision 0)", doc)
        self.assertIn('"rosa":{"entity_id":"rosa","label":"Rosa"', doc)
        # Pass 1: Rosa's own sign-release move, blocked because the crate is not inspected.
        self.assertIn("sign-release", doc)
        self.assertIn("the crate is inspected", doc)
        self.assertEqual(record["steps"][0]["document_chars"], len(doc))
        self.assertEqual((record["by"], record["outcome"], record["whose_choice"]), (judge_mod.BY, "no_rule", "rosa"))
        self.assertEqual(record["facts"], ["vik holds 40 coins"])
        self.assertEqual((record["cost_usd"], len(record["calls"])), (0.01, 1))

    @pytest.mark.req("ai-judge/the-game-master-reads-the-whole-world-and-pass-1-and-resolves-the-putative-event")
    def test_concordia_s_own_calls_go_through_llm_client(self):
        llm = FakeLlm({"choice": [{"choice": "no"}]})
        model = judge_mod.LlmClientModel("fixture-model", trace_id="fixture-trace", max_budget=0.5)
        with patch.dict(sys.modules, {"llm_client": llm.module()}):
            text = model.sample_text("What happens?", terminators=["\n"])
            index, answer, _ = model.sample_choice("Does it?", ["yes", "no"])
        self.assertEqual(text, "The crate goes through.")
        [sent] = llm.texts
        self.assertEqual((sent["task"], sent["trace_id"], sent["max_budget"]), (judge_mod.TASK, "fixture-trace", 0.5))
        self.assertEqual((index, answer), (1, "no"))
        self.assertEqual(llm.calls[0]["schema"]["properties"]["choice"]["enum"], ["yes", "no"])
        self.assertAlmostEqual(model.cost, 0.012)
        self.assertEqual([c["kind"] for c in model.calls], ["text", "choice"])


class RulingTests(unittest.TestCase):
    MOVE = {"to": "rosa", "amount": 40}

    @pytest.mark.req("ai-judge/a-confirmed-ruling-carries-its-rule-and-its-test-run")
    def test_a_confirmed_ruling_carries_its_rule_and_its_test_run(self):
        llm = FakeLlm({"propose": [propose(coin_rule(), self.MOVE, whose="rosa")], "review": [review("confirm")]})
        record = _judge(llm)
        self.assertEqual([c["name"] for c in llm.calls], ["propose", "review"])
        self.assertEqual(llm.calls[1]["schema"]["properties"]["decision"]["enum"], ["confirm", "revise", "withdraw"])
        # The review reads pass 2: the rules check passed and the coins moved, and nothing else followed.
        doc = llm.document(1)
        self.assertIn("Pass 2, the test run of your proposed rule", doc)
        self.assertIn('"status": "accepted"', doc)
        self.assertIn('"entity": "rosa"', doc)
        self.assertIn('"after": 40', doc)
        self.assertNotIn('"chain":', doc)  # the judge reads the summary; the chain stays in the record
        self.assertEqual((record["outcome"], record["revised"], record["whose_choice"]), ("confirmed", False, "rosa"))
        self.assertEqual(record["rule"], coin_rule())
        self.assertEqual(record["move"], {"actor": "vik", "kind": "hand-coins", "to": "rosa", "amount": 40})
        [test] = record["tests"]
        self.assertEqual(test["rules_check"], {"ok": True})
        self.assertEqual(test["test_run"]["net_changes"], [
            {"entity": "rosa", "path": "components.purse.coins", "before": 0, "after": 40},
            {"entity": "vik", "path": "components.purse.coins", "before": 40, "after": 0}])
        self.assertEqual([e["rule_id"] for e in test["test_run"]["chain"]], ["hand-coins"])
        self.assertAlmostEqual(record["cost_usd"], 0.02)

    @pytest.mark.req("ai-judge/a-ruling-is-revised-at-most-once")
    def test_a_rejected_rule_is_revised_once_and_the_revision_is_test_run(self):
        bad = {"from": "rosa", "amount": 40}
        llm = FakeLlm({"propose": [propose(unwritable_rule(), bad)],
                       "review": [review("revise", coin_rule(), self.MOVE)], "final": [review("confirm")]})
        record = _judge(llm)
        self.assertEqual([c["name"] for c in llm.calls], ["propose", "review", "final"])
        # The review read the rules check's own error; the last answer can only confirm or withdraw.
        self.assertIn('"ok": false', llm.document(1))
        self.assertIn("from", record["tests"][0]["rules_check"]["error"])
        self.assertIn("Pass 2, the test run of your revised rule", llm.document(2))
        self.assertEqual(llm.calls[2]["schema"]["properties"]["decision"]["enum"], ["confirm", "withdraw"])
        self.assertEqual((record["outcome"], record["revised"], len(record["tests"])), ("confirmed", True, 2))
        self.assertEqual(record["rule"], coin_rule())
        self.assertEqual(record["tests"][1]["test_run"]["status"], "accepted")

    @pytest.mark.req("ai-judge/a-rule-the-language-cannot-express-is-a-language-gap")
    def test_a_rule_rejected_twice_is_a_language_gap(self):
        bad = {"from": "rosa", "amount": 40}
        llm = FakeLlm({"propose": [propose(unwritable_rule(), bad)],
                       "review": [review("revise", unwritable_rule(), bad)]})
        record = _judge(llm)
        self.assertEqual([c["name"] for c in llm.calls], ["propose", "review"])  # no third question
        self.assertEqual((record["outcome"], record["rule"]), ("language_gap", None))
        self.assertTrue(record["why"].startswith(judge_mod.NO_RULE))
        self.assertTrue(all(not t["rules_check"]["ok"] and t["test_run"] is None for t in record["tests"]))

    @pytest.mark.req("ai-judge/a-ruling-is-revised-at-most-once")
    def test_a_rejected_rule_cannot_be_confirmed(self):
        llm = FakeLlm({"propose": [propose(unwritable_rule(), {"from": "rosa", "amount": 40})],
                       "review": [review("confirm")]})
        record = _judge(llm)
        self.assertEqual((record["outcome"], record["rule"]), ("withdrawn", None))
        self.assertIn("cannot be confirmed", record["why"])

    @pytest.mark.req("ai-judge/a-confirmed-ruling-carries-its-rule-and-its-test-run")
    def test_a_withdrawn_ruling_keeps_its_test_run_and_no_rule(self):
        llm = FakeLlm({"propose": [propose(coin_rule(), {"to": "rosa", "amount": 50})],
                       "review": [review("withdraw", why="Vik holds only 40 coins: the test run refused it.")]})
        record = _judge(llm)
        self.assertIn("the giver holds that many coins", llm.document(1))
        self.assertEqual((record["outcome"], record["rule"], record["move"]), ("withdrawn", None, None))
        self.assertEqual(record["tests"][0]["test_run"]["status"], "precondition_failed")

    @pytest.mark.req("ai-judge/another-person-s-choice-goes-to-that-person")
    def test_the_person_trying_is_not_whose_choice(self):
        record = _judge(FakeLlm({"propose": [propose(whose="vik")]}))
        self.assertIsNone(record["whose_choice"])
        record = _judge(FakeLlm({"propose": [propose(whose="no-such-person")]}))
        self.assertIsNone(record["whose_choice"])


class ChainTests(unittest.TestCase):
    @pytest.mark.req("ai-judge/the-review-reads-where-a-blocked-chain-stopped")
    def test_the_review_reads_where_a_blocked_chain_stopped(self):
        llm = FakeLlm({"propose": [propose(shove_rule(), {"thing": "lever"})], "review": [review("confirm")]})
        record = _judge(llm, world=blocked_chain, actor="sam", attempt="I shove the lever over",
                        named=("lever",), people=["sam"])
        # Pass 1: no move of Sam's touches the lever (his one move honks the horn).
        self.assertIn("honk-horn", llm.document(0))
        self.assertNotIn('"pull"', llm.document(0))
        doc = llm.document(1)
        self.assertIn('"kind": "blocked"', doc)
        self.assertIn("the truck has fuel", doc)
        self.assertIn('"chain_length": 40', doc)
        run = record["tests"][0]["test_run"]
        # The record keeps the whole chain: the move, then the 40 knock-on steps.
        self.assertEqual((run["stopping_point"]["after_step"], run["chain"][0]["rule_id"]), (40, "shove-lever"))

    @pytest.mark.req("ai-judge/a-long-test-run-is-read-grouped")
    def test_a_long_test_run_is_read_grouped(self):
        llm = FakeLlm({"propose": [propose(press_rule(), {"button": "button"})], "review": [review("confirm")]})
        record = _judge(llm, world=long_line, actor="sam", attempt="I press the start button", named=("button",),
                        people=["sam"])
        run = record["tests"][0]["test_run"]
        self.assertEqual((run["chain_length"], run["stopping_point"]["kind"], len(run["net_changes"])),
                         (5000, "settled", 5001))
        doc = llm.document(1)
        self.assertIn('"net_changes_grouped": true', doc)
        self.assertIn('"net_change_count": 5001', doc)
        # The review reads the whole world and the grouped report, not the 5,000-step chain.
        self.assertLess(len(doc) - llm.calls[1]["messages"][-1]["content"].index("Pass 2"), 20_000)

    @pytest.mark.req("ai-judge/a-long-test-run-is-read-grouped")
    def test_net_changes_group_by_change_and_things(self):
        rows = [{"entity": e, "path": p, "before": False, "after": True}
                for e in ("a", "b") for p in ("components.line.s1", "components.line.s2")]
        rows.append({"entity": "button", "path": "components.switch.pressed", "before": False, "after": True})
        rows.append({"entity": "a", "path": "components.purse.coins", "before": 40, "after": 0})
        self.assertEqual(report.grouped(rows), [
            {"things": ["a", "b"], "fields": ["components.line.s1", "components.line.s2"], "before": False,
             "after": True, "changes": 4},
            {"things": ["button"], "fields": ["components.switch.pressed"], "before": False, "after": True,
             "changes": 1},
            {"things": ["a"], "fields": ["components.purse.coins"], "before": 40, "after": 0, "changes": 1},
        ])


class RunTests(unittest.TestCase):
    """The judge in a run: it rules on each unmatched attempt after everyone's move, and records the ruling."""

    def _run(self, llm: FakeLlm, *, world=port, who="vik", attempt=BRIBE, judge=True):
        bundle, rules = world()
        from scripts import concordia_residents as cr

        real_choose = cr.Residents.choose

        def choose(self_, actor, available, context):
            out = real_choose(self_, actor, available, context)
            return {**out, "attempt": attempt} if actor == who else out

        with patch.dict(sys.modules, {"llm_client": llm.module()}), patch.object(cr.Residents, "choose", choose):
            trace, engine, _ = run_world(bundle, rules, policy="resident", model_name="fixture-model", max_turns=1,
                                         trace_id="fixture-trace", open_attempts=True, judge=judge)
        json.dumps(trace)
        return trace, engine

    UNASKED = {"kind": "none", "fields": [], "nearest_kind": "none", "asks": "none", "names": ["rosa", "crate"],
               "why": "no kind hands over coins"}

    @pytest.mark.req("ai-judge/another-person-s-choice-goes-to-that-person")
    def test_another_person_s_choice_goes_to_that_person(self):
        # The words name Rosa but ask no one; the judge rules that the attempt needs Rosa's choice, so it reaches her.
        llm = FakeLlm({"propose": [propose(whose="rosa", ruling="Whether to take coins is Rosa's choice.")]},
                      reading=self.UNASKED)
        trace, engine = self._run(llm)
        row = trace["transcript"][0]["actors"]["vik"]
        self.assertEqual(row["did"]["kind"], open_attempt.UNMATCHED_KIND)
        self.assertEqual((row["judge"]["outcome"], row["judge"]["whose_choice"]), ("no_rule", "rosa"))
        self.assertEqual(row["asked"], "rosa")
        [listed] = trace["summary"]["unmatched_attempts"]
        self.assertEqual(listed["judge"], {"outcome": "no_rule", "whose_choice": "rosa",
                                           "ruling": "Whether to take coins is Rosa's choice."})
        self.assertIn(f"Putative event to resolve:  vik: {BRIBE}", llm.document(0))
        # Replay needs no model, and the ruling installed nothing.
        with patch.dict(sys.modules, {"llm_client": None}):
            self.assertTrue(engine.replay()["ok"])
        self.assertNotIn("hand-coins", engine.registry.action_kinds())

    @pytest.mark.req("ai-judge/the-judge-rules-on-each-unmatched-attempt-in-a-run")
    def test_a_confirmed_ruling_is_recorded_and_not_installed(self):
        llm = FakeLlm({"propose": [propose(coin_rule(), {"to": "rosa", "amount": 40}, whose="rosa")],
                       "review": [review("confirm")]}, reading=self.UNASKED)
        trace, engine = self._run(llm)
        row = trace["transcript"][0]["actors"]["vik"]
        self.assertEqual(row["judge"]["outcome"], "confirmed")
        self.assertEqual(row["judge"]["rule"]["mechanic"]["mechanic_id"], "hand-coins")
        self.assertNotIn("hand-coins", engine.registry.action_kinds())
        self.assertEqual(engine.world.material_dict()["entities"]["vik"]["components"]["purse"]["coins"], 40)
        self.assertAlmostEqual(trace["cost_usd"], 0.02)  # the judge's two calls count toward the run's spend

    @pytest.mark.req("ai-judge/the-judge-rules-on-each-unmatched-attempt-in-a-run")
    def test_a_failed_judge_call_is_recorded_and_the_run_goes_on(self):
        trace, _ = self._run(FakeLlm(reading=self.UNASKED, fail=True))
        ruling = trace["transcript"][0]["actors"]["vik"]["judge"]
        self.assertEqual((ruling["outcome"], ruling["by"]), ("failed", judge_mod.BY))
        self.assertIn("provider down", ruling["error"])

    @pytest.mark.req("ai-judge/the-judge-rules-on-each-unmatched-attempt-in-a-run")
    def test_without_the_judge_no_ruling_is_asked(self):
        llm = FakeLlm(reading=self.UNASKED)
        trace, _ = self._run(llm, judge=False)
        self.assertEqual(llm.calls, [])
        self.assertNotIn("judge", trace["transcript"][0]["actors"]["vik"])
        with self.assertRaises(ValueError):
            run_world(*port(), policy="resident", model_name="m", max_turns=1, judge=True)

    @pytest.mark.req("ai-judge/an-attempt-an-installed-rule-covers-never-reaches-the-judge")
    def test_an_attempt_an_installed_rule_covers_never_reaches_the_judge(self):
        # Once the coin rule is installed, Ines (no coins) trying to hand Rosa 10 coins is a move the rule refuses.
        words = "I hand Rosa 10 coins"
        reading = {"kind": "hand-coins", "fields": [{"field": "to", "value": "rosa", "quoted_span": "Rosa"},
                                                    {"field": "amount", "value": "10", "quoted_span": "10"}],
                   "nearest_kind": "hand-coins", "asks": "none", "names": ["rosa"], "why": "handing coins"}
        llm = FakeLlm(reading=reading)
        trace, _ = self._run(llm, world=empty_purse, who="ines", attempt=words)
        row = trace["transcript"][0]["actors"]["ines"]
        self.assertEqual(row["did"]["kind"], "hand-coins")
        self.assertEqual(row["status"], "precondition_failed")
        self.assertIn("the giver holds that many coins", json.dumps(row))
        self.assertEqual(llm.calls, [])
        self.assertNotIn("judge", row)


class ServiceTests(unittest.TestCase):
    @pytest.mark.req("ai-judge/a-long-test-run-is-read-grouped")
    def test_the_page_gets_what_the_judge_read_and_the_run_log_the_whole_test_run(self):
        from scripts import world_builder_service as service

        changes = [{"entity": f"c{n}", "path": "components.line.s1", "before": False, "after": True} for n in range(50)]
        run = {"status": "accepted", "chain": [{"rule_id": "press-button"}] * 3, "net_changes": changes,
               "blockers": [], "chain_length": 2, "stopping_point": {"kind": "settled", "after_step": 2}}
        trace = {"transcript": [{"turn": 1, "actors": {
            "sam": {"event_id": "r1-e1", "judge": {"outcome": "confirmed",
                                                   "tests": [{"rules_check": {"ok": True}, "test_run": deepcopy(run)}]}},
            "ava": {"event_id": "r1-e2", "status": "accepted"}}}]}
        full = service._judge_test_runs(trace)
        self.assertEqual(full, {"r1-e1": [run]})
        page = trace["transcript"][0]["actors"]["sam"]["judge"]["tests"][0]["test_run"]
        self.assertNotIn("chain", page)
        self.assertEqual((page["net_changes_grouped"], page["net_change_count"], len(page["net_changes"])),
                         (True, 50, 1))


if __name__ == "__main__":
    unittest.main()
