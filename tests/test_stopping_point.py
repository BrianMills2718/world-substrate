"""A stopping point written in plain words, assessed by the judge after each round (ai-judge plan, slice J5).

Brian, 2026-11-10: "i should be able to stop a world based on budget or number of rounds or a natural langue stopping
potin that the judge assesses once we build him". Every model call is faked: a stand-in `llm_client` answers the
game master's one resolution step (`world_substrate_judge_stopping`) from a list and records the document Concordia's
EventResolution assembled, so the tests read exactly what the game master was given. The orchard world is the one
tests/test_run_stop.py uses: Ava picks the apples in round 1 and nothing can change after that.
"""
from __future__ import annotations

import sys
import types
from unittest.mock import patch

import pytest

from scripts import judge as judge_mod
from scripts import run_stop
from scripts.run_authored_world import run_world
from tests.test_run_stop import BUNDLE, _no_finish_line

WHEN = "stop once the apples are picked"
PICKED = "Ava picked the apples."


class FakeJudge:
    """A stand-in llm_client: the stopping step answers from `answers` (the last one repeats), at $0.01 a call."""

    def __init__(self, answers: list[dict] | None = None, fail: bool = False):
        self.answers = list(answers or [{"reached": False, "reason": "not yet"}])
        self.fail = fail
        self.calls: list[dict] = []
        self.total = 0.0

    def module(self) -> types.ModuleType:
        fake = types.ModuleType("llm_client")

        def render_prompt(path, **kwargs):
            return [{"role": "system", "content": f"step {kwargs['step']} for {kwargs['actor']}"},
                    {"role": "user", "content": kwargs["document"]}]

        def call_llm_json_schema(model, messages, schema, **kwargs):
            self.calls.append({"model": model, "messages": messages, "schema": schema, **kwargs})
            if self.fail:
                raise RuntimeError("provider down")
            self.total += 0.01
            answer = self.answers.pop(0) if len(self.answers) > 1 else self.answers[0]
            return {"facts": ["the orchard's fruit stage is read"], **answer}, types.SimpleNamespace(cost=0.01)

        fake.render_prompt = render_prompt
        fake.call_llm_json_schema = call_llm_json_schema
        return fake

    def document(self, n: int = 0) -> str:
        return self.calls[n]["messages"][-1]["content"]


def play(judge: FakeJudge, run_stop_setting: dict, *, max_turns: int = 10, **kwargs):
    with patch.dict(sys.modules, {"llm_client": judge.module()}):
        return run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=max_turns,
                         run_stop=run_stop_setting, **kwargs)[0]


@pytest.mark.req("ai-judge/a-reached-stopping-point-stops-the-run")
def test_a_reached_stopping_point_stops_the_run_with_the_judge_s_reason():
    judge = FakeJudge([{"reached": True, "reason": PICKED}])
    trace = play(judge, {"mode": "every_round", "stop_when": WHEN})
    # Round 1 changed the apples, the judge was asked once and said yes: the run stops after that round.
    assert trace["summary"]["turns"] == 1 and len(judge.calls) == 1
    stopped = trace["summary"]["stopped"]
    assert stopped["reason"] == "stopping_point" and stopped["round"] == 1 and stopped["stop_when"] == WHEN
    assert stopped["why"] == "Stopped at round 1: Ava picked the apples (the judge's reading of your stopping point)."
    row = trace["transcript"][0]["stopping_point"]
    assert (row["asked"], row["reached"], row["reason"], row["because"]) == (True, True, PICKED, "changed")
    assert row["facts"] == ["the orchard's fruit stage is read"] and row["cost_usd"] == pytest.approx(0.01)
    assert row["by"] == judge_mod.BY and row["trace_id"] and row["calls"][0]["task"] == judge_mod.STOP_TASK


@pytest.mark.req("ai-judge/the-judge-reads-the-stopping-point-as-the-event-and-the-world-as-context")
def test_the_game_master_reads_the_stopping_text_as_the_event_with_the_world_as_context():
    judge = FakeJudge([{"reached": True, "reason": PICKED}])
    play(judge, {"mode": "every_round", "stop_when": WHEN})
    doc = judge.document()
    # Concordia's EventResolution assembled it: the world, what happened this round, and the putative event.
    assert "Stopping point: " + WHEN in doc
    assert "Round 1, what each person did and what it changed" in doc
    assert "Every thing and its current values (revision 1)" in doc and '"stage":"picked"' in doc
    assert "changed apple-1.fruit.stage: ripe -> picked" in doc and "Putative event to resolve" in doc
    assert judge.calls[0]["task"] == judge_mod.STOP_TASK
    assert judge.calls[0]["schema"]["required"] == ["facts", "reached", "reason"]
    assert len(judge.calls) == 1  # one typed question, one call: Concordia's own text calls are not made


@pytest.mark.req("ai-judge/the-judge-is-asked-after-a-change-and-every-6-quiet-rounds")
def test_the_judge_is_asked_after_a_change_and_once_every_6_quiet_rounds():
    judge = FakeJudge([{"reached": False, "reason": "no apples picked yet"},
                       {"reached": True, "reason": "six rounds on, the time is up"}])
    trace = play(judge, {"mode": "every_round", "stop_when": WHEN}, max_turns=12)
    # Round 1 picks the apples (asked: changed). Rounds 2-6 are quiet and not asked; round 7 is the 6th quiet round.
    assert len(judge.calls) == 2
    asked = [(t["turn"], t["stopping_point"].get("because")) for t in trace["transcript"] if t["stopping_point"]["asked"]]
    assert asked == [(1, "changed"), (7, "backstop")]
    assert [t["stopping_point"] for t in trace["transcript"][1:6]] == [{"asked": False}] * 5
    assert trace["summary"]["stopped"]["round"] == 7 and trace["summary"]["stopped"]["reason"] == "stopping_point"
    assert trace["transcript"][0]["stopping_point"]["reached"] is False  # "stopping point: not yet", with its reason
    assert trace["transcript"][0]["stopping_point"]["reason"] == "no apples picked yet"


@pytest.mark.req("ai-judge/the-judge-is-asked-after-a-change-and-every-6-quiet-rounds")
def test_the_quiet_count_and_the_last_state_carry_across_one_round_requests():
    judge = FakeJudge([{"reached": False, "reason": "not yet"}])
    stop = {"mode": "every_round", "stop_when": WHEN}
    first = play(judge, stop, max_turns=1)
    assert first["stop_history"] and len(first["stop_history"]) == 2 and first["stop_quiet"] == 0
    assert len(judge.calls) == 1
    # Live play sends them back: a quiet round with 5 quiet rounds behind it is the 6th, so it is asked.
    quiet = play(judge, stop, max_turns=1, start_snapshot=first["final_snapshot"], turn_offset=1,
                 stop_history=first["stop_history"], stop_quiet=5)
    assert len(judge.calls) == 2 and quiet["transcript"][0]["stopping_point"]["because"] == "backstop"
    assert quiet["stop_quiet"] == 0
    # With 2 quiet rounds behind it, a quiet round is not asked and the count goes on.
    later = play(judge, stop, max_turns=1, start_snapshot=first["final_snapshot"], turn_offset=1,
                 stop_history=first["stop_history"], stop_quiet=2)
    assert len(judge.calls) == 2 and later["transcript"][0]["stopping_point"] == {"asked": False}
    assert later["stop_quiet"] == 3


@pytest.mark.req("ai-judge/a-limit-that-fires-first-needs-no-judge-call")
def test_a_round_limit_that_fires_first_needs_no_judge_call():
    judge = FakeJudge([{"reached": True, "reason": PICKED}])
    trace = play(judge, {"mode": "every_round", "max_rounds": 1, "stop_when": WHEN})
    assert judge.calls == []
    assert trace["summary"]["stopped"]["reason"] == "round_limit" and trace["summary"]["stopped"]["round"] == 1
    # And the limit is checked first even when the judge would have said yes in the same round.
    both = run_stop.limit_check({"mode": "every_round", "max_rounds": 2, "stop_when": WHEN}, 2, None,
                                {"reached": True, "reason": PICKED})
    assert both["reason"] == "round_limit"
    money = run_stop.limit_check({"mode": "every_round", "max_spend_usd": 0.5, "stop_when": WHEN}, 2, 0.5,
                                 {"reached": True, "reason": PICKED})
    assert money["reason"] == "budget"


@pytest.mark.req("ai-judge/a-limit-that-fires-first-needs-no-judge-call")
def test_a_stopping_point_not_reached_leaves_the_round_limit_to_stop_the_run():
    judge = FakeJudge([{"reached": False, "reason": "the apples are still on the tree"}])
    trace = play(judge, {"mode": "every_round", "max_rounds": 3, "stop_when": WHEN})
    assert trace["summary"]["stopped"]["reason"] == "round_limit" and trace["summary"]["stopped"]["round"] == 3
    assert len(judge.calls) == 1  # asked after round 1's change; rounds 2 and 3 were quiet


@pytest.mark.req("ai-judge/the-judge-s-cost-counts-toward-the-spending-limit")
def test_the_judge_s_cost_counts_toward_the_run_s_spending():
    judge = FakeJudge([{"reached": False, "reason": "not yet"}])
    trace = play(judge, {"mode": "every_round", "max_spend_usd": 5, "stop_when": WHEN}, max_turns=2,
                 spent=lambda: judge.total)
    # The judge's $0.01 call is on the run's own trace, so it is carried to the next request and counted there.
    assert trace["cost_usd"] == pytest.approx(0.01)
    assert trace["run_spent_usd"] == pytest.approx(0.01)
    # ... and a spending limit under it stops the next request before any round (the judge's cost reached it).
    again = play(FakeJudge(), {"mode": "every_round", "max_spend_usd": 0.01, "stop_when": WHEN}, max_turns=1,
                 start_snapshot=trace["final_snapshot"], turn_offset=2, stop_history=trace["stop_history"],
                 run_spent_usd=trace["run_spent_usd"], spent=lambda: 0.0)
    assert again["summary"]["turns"] == 0 and again["summary"]["stopped"]["reason"] == "budget"


@pytest.mark.req("ai-judge/whichever-stop-fires-first-wins")
def test_the_quiet_rule_still_stops_a_world_whose_stopping_point_is_not_reached():
    judge = FakeJudge([{"reached": False, "reason": "no"}])
    trace = play(judge, {"mode": "quiet", "quiet_rounds": 3, "stop_when": WHEN})
    # Quiet after round 4 (round 1 picks the apples, rounds 2-4 change nothing); the judge was asked once, in round 1.
    assert trace["summary"]["stopped"]["reason"] == "quiet_rounds" and trace["summary"]["stopped"]["round"] == 4
    assert len(judge.calls) == 1


@pytest.mark.req("ai-judge/a-failed-stopping-point-call-is-recorded-and-the-run-goes-on")
def test_a_failed_judge_call_is_recorded_and_the_run_goes_on():
    judge = FakeJudge(fail=True)
    trace = play(judge, {"mode": "every_round", "stop_when": WHEN}, max_turns=3)
    row = trace["transcript"][0]["stopping_point"]
    assert row["asked"] and row["failed"] and not row["reached"] and "provider down" in row["error"]
    assert trace["summary"]["turns"] == 3 and trace["summary"]["stopped"]["reason"] == "round_cap"


@pytest.mark.req("ai-judge/a-world-without-a-stopping-point-asks-no-judge")
def test_a_world_without_a_stopping_point_never_calls_the_judge():
    judge = FakeJudge()
    trace = play(judge, {"mode": "every_round", "max_rounds": 4}, max_turns=6)
    assert judge.calls == [] and all("stopping_point" not in t for t in trace["transcript"])
    assert "stop_quiet" not in trace


@pytest.mark.req("world-builder-page/the-stop-setting-is-checked")
def test_the_stopping_point_text_is_checked():
    ok = run_stop.parse_run_stop({"mode": "every_round", "stop_when": "  stop once   the team\nhas agreed a budget "})
    assert ok == {"mode": "every_round", "stop_when": "stop once the team has agreed a budget"}
    assert run_stop.parse_run_stop({"mode": "quiet", "max_rounds": 3, "stop_when": WHEN}) == {
        "mode": "quiet", "quiet_rounds": 6, "max_rounds": 3, "stop_when": WHEN}
    assert run_stop.parse_run_stop({"mode": "every_round", "stop_when": None}) == {"mode": "every_round"}
    for bad in ("", "   ", "x" * 301, 5, ["stop"], True):
        with pytest.raises(ValueError):
            run_stop.parse_run_stop({"mode": "every_round", "stop_when": bad})
    assert len(run_stop.parse_run_stop({"mode": "every_round", "stop_when": "x" * 300})["stop_when"]) == 300
