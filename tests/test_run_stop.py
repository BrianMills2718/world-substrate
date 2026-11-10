"""A World Builder run stops by itself once nothing is changing (Q12; Brian, 2026-11-10: "stop condition should be
configurable"). All free: scripted runs and the recorded Waltzman run of 2026-10-23; no AI call."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from scripts import run_stop
from scripts.run_authored_world import run_world
from scripts.scaffold_world import load_bundle
from scripts.world_builder_service import validate_bundle
from world_substrate.action_authoring import CausalModel

REPO = Path(__file__).resolve().parents[1]
BUNDLE = load_bundle(REPO / "examples/world_authoring/orchard-v0.json")
CAUSAL = json.loads((REPO / "examples/world_authoring/orchard-causal-v0.json").read_text())
C1R24 = REPO / "evidence/waltzman-tasks-slice2/c1r24/run-log.jsonl"


def _no_finish_line() -> dict:
    """The orchard without its finish line: the apples are picked in round 1 and then nothing can change.

    It keeps one world process that never fires, since a scripted run with no process ends by itself once nobody
    can act (run_authored_world.py: "every later round would be identical")."""
    return {**CAUSAL, "terminal": None, "processes": [{
        "process_id": "frost", "rationale": "Frost spoils fruit, but this orchard never freezes.",
        "selector": {"categories": ["fruit"], "components": ["fruit"]},
        "checks": [{"label": "the fruit is frozen", "left": {"participant": {"name": "it", "path": "components.fruit.stage"}},
                    "op": "eq", "right": {"literal": "frozen"}}],
        "effects": [{"participant": "it", "path": "components.fruit.stage", "op": "set", "value": {"literal": "spoiled"}}],
    }]}


@pytest.mark.req("world-builder-page/a-world-without-the-setting-runs-every-round")
def test_a_run_without_the_setting_runs_every_round_and_records_nothing_new():
    trace, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=10)
    assert trace["summary"]["turns"] == 10
    assert "stopped" not in trace["summary"]
    assert "stop_history" not in trace


@pytest.mark.req("world-builder-page/a-run-stops-after-n-quiet-rounds")
def test_a_run_stops_once_nothing_has_changed_for_n_rounds():
    trace, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=10,
                            run_stop={"mode": "quiet", "quiet_rounds": 3})
    # Round 1 picks the apples; rounds 2-4 change nothing, so the run stops at round 4.
    assert trace["summary"]["turns"] == 4
    stopped = trace["summary"]["stopped"]
    assert stopped["reason"] == "quiet_rounds" and stopped["round"] == 4 and stopped["quiet_rounds"] == 3
    assert stopped["decision"] is None
    assert stopped["why"] == "Stopped at round 4: nothing had changed for 3 rounds."
    assert len(trace["stop_history"]) == 4


@pytest.mark.req("world-builder-page/a-run-stops-after-n-quiet-rounds")
def test_the_quiet_count_carries_across_one_round_requests():
    # Live play asks for one round at a time and sends back stop_history, as it sends back resident memory.
    first, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=2,
                            run_stop={"mode": "quiet", "quiet_rounds": 3})
    assert first["summary"]["stopped"] == {"reason": "round_cap", "round": 2}
    second, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=5,
                             run_stop={"mode": "quiet", "quiet_rounds": 3}, start_snapshot=first["final_snapshot"],
                             turn_offset=2, stop_history=first["stop_history"])
    assert second["summary"]["stopped"]["round"] == 4
    assert second["summary"]["turns"] == 2


@pytest.mark.req("world-builder-page/a-run-stops-after-n-quiet-rounds")
def test_a_world_without_a_decision_keeps_going_while_people_still_change_things():
    # Ava picks the apple every round and it grows back: the state at each round's end is the same, but a person's
    # move changed something every round, so a world without a group decision is not quiet.
    regrow = {**_no_finish_line(), "processes": [{
        "process_id": "regrow", "rationale": "Picked fruit grows back.",
        "selector": {"categories": ["fruit"], "components": ["fruit"]},
        "checks": [{"label": "the fruit has been picked",
                    "left": {"participant": {"name": "it", "path": "components.fruit.stage"}},
                    "op": "eq", "right": {"literal": "picked"}}],
        "effects": [{"participant": "it", "path": "components.fruit.stage", "op": "set", "value": {"literal": "ripe"}},
                    {"participant": "it", "path": "ownership.owner_ref", "op": "set", "value": {"literal": "place:orchard"}}],
    }]}
    trace, _, _ = run_world(BUNDLE, regrow, policy="scripted", max_turns=9, run_stop={"mode": "quiet", "quiet_rounds": 2})
    assert trace["summary"]["turns"] == 9
    assert trace["summary"]["stopped"] == {"reason": "round_cap", "round": 9}


@pytest.mark.req("world-builder-page/always-run-every-round")
def test_always_run_every_round_records_the_round_cap():
    trace, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=7,
                            run_stop={"mode": "every_round"})
    assert trace["summary"]["turns"] == 7
    assert trace["summary"]["stopped"] == {"reason": "round_cap", "round": 7}


@pytest.mark.req("world-builder-page/a-run-stops-after-n-quiet-rounds")
def test_a_finish_line_is_recorded_as_the_reason():
    trace, _, _ = run_world(BUNDLE, CAUSAL, policy="scripted", max_turns=5, run_stop=run_stop.DEFAULT_RUN_STOP)
    assert trace["summary"]["terminal_reached"]
    assert trace["summary"]["stopped"] == {"reason": "finish_line", "round": 1}


@pytest.mark.req("world-builder-page/a-group-decision-must-be-settled")
def test_an_open_decision_keeps_a_quiet_run_going():
    hist = ["a", "b", "a"]
    assert run_stop.check({"mode": "quiet", "quiet_rounds": 2}, hist, "open:authorized", 9) is None
    stopped = run_stop.check({"mode": "quiet", "quiet_rounds": 2}, hist, "settled:rejected", 9)
    assert stopped["why"] == ("Stopped at round 9: nothing had changed for good for 2 rounds after the decision was "
                              "rejected (the moves made in them were undone again).")


@pytest.mark.req("world-builder-page/a-group-decision-must-be-settled")
def test_the_recorded_waltzman_run_would_have_stopped_at_round_30_not_46():
    # evidence/waltzman-tasks-slice2/c1r24: the decision was deployed in round 14, the operating review reopened
    # concerns in round 19 and the last was resolved in round 22; after that only the agenda churn (Q3) and the
    # world's clocks moved. Judged on each logged round's final state, the default setting stops at round 30.
    rows = [json.loads(line) for line in C1R24.read_text().splitlines()]
    runs = [r for r in rows if r.get("path") == "/run"]
    request = runs[0]["request"]
    fields = run_stop.movable_fields(CausalModel.from_dict(request["causal_model"],
                                                           bundle=validate_bundle(request["bundle"])))
    assert "components.moment.ticks_until" not in fields  # a clock only the world's processes move
    assert "components.group_decision.agenda_items" in fields
    history, first = [], None
    for row in runs:
        world = row["result"]["final_snapshot"]["world"]
        history.append(run_stop.state_key(world, fields))
        stopped = run_stop.check(run_stop.DEFAULT_RUN_STOP, history, run_stop.decision_status(world),
                                 row["result"]["summary"]["last_turn"])
        first = first or stopped
    assert runs[-1]["result"]["summary"]["last_turn"] == 46
    assert first["round"] == 30 and first["decision"] == "deployed"


@pytest.mark.req("world-builder-page/a-run-stops-after-n-quiet-rounds")
def test_the_setting_is_checked():
    assert run_stop.parse_run_stop(None) is None
    assert run_stop.parse_run_stop(None, default=run_stop.DEFAULT_RUN_STOP) == {"mode": "quiet", "quiet_rounds": 6}
    assert run_stop.parse_run_stop({"mode": "quiet"}) == {"mode": "quiet", "quiet_rounds": 6}
    assert run_stop.parse_run_stop({"mode": "every_round"}) == {"mode": "every_round"}
    for bad in ({"mode": "quiet", "quiet_rounds": 0}, {"mode": "quiet", "quiet_rounds": 2.5}, {"mode": "never"},
                {"mode": "every_round", "quiet_rounds": 3}, "quiet"):
        with pytest.raises(ValueError):
            run_stop.parse_run_stop(bad)


# Round and spending limits (Brian, 2026-11-10: "i should be able to stop a world based on budget or number of rounds
# or a natural langue stopping potin that the judge assesses once we build him"). The recorded cost is faked: no AI.

class FakeCost:
    """Stands in for llm_client's recorded cost of this request's trace: each round adds `per_round` dollars."""

    def __init__(self, per_round: float):
        self.per_round, self.calls = per_round, 0

    def __call__(self) -> float:
        self.calls += 1
        return self.per_round * (self.calls - 1)


@pytest.mark.req("world-builder-page/a-run-stops-at-the-round-limit-you-set")
def test_a_run_stops_at_the_round_limit_you_set():
    trace, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=10,
                            run_stop={"mode": "every_round", "max_rounds": 5})
    assert trace["summary"]["turns"] == 5
    assert trace["summary"]["stopped"] == {"reason": "round_limit", "round": 5, "max_rounds": 5,
                                           "why": "Stopped at round 5: the limit of 5 rounds you set."}


@pytest.mark.req("world-builder-page/a-run-stops-at-the-round-limit-you-set")
def test_the_round_limit_counts_the_whole_live_run_across_one_round_requests():
    stop = {"mode": "every_round", "max_rounds": 3}
    first, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=2, run_stop=stop)
    assert first["summary"]["stopped"] == {"reason": "round_cap", "round": 2}
    second, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=1, run_stop=stop,
                             start_snapshot=first["final_snapshot"], turn_offset=2)
    assert second["summary"]["stopped"]["reason"] == "round_limit" and second["summary"]["stopped"]["round"] == 3
    # A request past the limit plays nothing and says so again.
    third, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=1, run_stop=stop,
                            start_snapshot=second["final_snapshot"], turn_offset=3)
    assert third["summary"]["turns"] == 0 and third["summary"]["stopped"]["reason"] == "round_limit"


@pytest.mark.req("world-builder-page/a-run-stops-once-it-has-spent-its-limit")
def test_a_run_stops_once_its_recorded_spending_reaches_the_limit():
    # $0.15 recorded per round against a $0.40 limit: after round 3 the run has spent $0.45, so round 4 never starts.
    cost = FakeCost(0.15)
    trace, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=10,
                            run_stop={"mode": "every_round", "max_spend_usd": 0.40}, spent=cost)
    assert trace["summary"]["turns"] == 3
    stopped = trace["summary"]["stopped"]
    assert stopped["reason"] == "budget" and stopped["round"] == 3
    assert stopped["spent_usd"] == pytest.approx(0.45) and stopped["max_spend_usd"] == 0.40
    assert stopped["why"] == ("Stopped at round 3: this run had spent $0.45 of its $0.40 limit. A round already under "
                              "way always finishes, so it went a little over.")
    assert trace["run_spent_usd"] == pytest.approx(0.45)


@pytest.mark.req("world-builder-page/a-run-stops-once-it-has-spent-its-limit")
def test_spending_carries_across_one_round_requests_and_a_spent_run_plays_no_more():
    stop = {"mode": "every_round", "max_spend_usd": 0.40}
    # Earlier requests of this live run spent $0.30; this round's calls are recorded at $0.10.
    first, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=1, run_stop=stop,
                            run_spent_usd=0.30, spent=FakeCost(0.10))
    assert first["summary"]["stopped"]["reason"] == "budget"
    assert first["summary"]["stopped"]["why"] == "Stopped at round 1: this run had spent $0.40 of its $0.40 limit."
    again, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=1, run_stop=stop,
                            start_snapshot=first["final_snapshot"], turn_offset=1,
                            run_spent_usd=first["run_spent_usd"], spent=lambda: 0.0)
    assert again["summary"]["turns"] == 0
    assert again["summary"]["stopped"]["reason"] == "budget" and again["summary"]["stopped"]["round"] == 1


@pytest.mark.req("world-builder-page/whichever-stop-fires-first-wins")
def test_whichever_stop_fires_first_wins():
    # Quiet after round 4 (round 1 picks the apples, rounds 2-4 change nothing) beats a 6-round limit and a budget.
    quiet_first, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=10, spent=FakeCost(0.01),
                                  run_stop={"mode": "quiet", "quiet_rounds": 3, "max_rounds": 6, "max_spend_usd": 1})
    assert quiet_first["summary"]["stopped"]["reason"] == "quiet_rounds"
    assert quiet_first["summary"]["stopped"]["round"] == 4
    limit_first, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=10, spent=FakeCost(0.01),
                                  run_stop={"mode": "quiet", "quiet_rounds": 3, "max_rounds": 2, "max_spend_usd": 1})
    assert limit_first["summary"]["stopped"]["reason"] == "round_limit"
    assert limit_first["summary"]["stopped"]["round"] == 2
    money_first, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=10, spent=FakeCost(0.5),
                                  run_stop={"mode": "quiet", "quiet_rounds": 3, "max_rounds": 6, "max_spend_usd": 1})
    assert money_first["summary"]["stopped"]["reason"] == "budget"
    assert money_first["summary"]["stopped"]["round"] == 2
    # Both limits met after the same round: the money is the reason given.
    both = run_stop.limit_check({"mode": "every_round", "max_rounds": 2, "max_spend_usd": 0.5}, 2, 0.5)
    assert both["reason"] == "budget"


@pytest.mark.req("world-builder-page/a-world-without-the-setting-runs-every-round")
def test_a_setting_without_limits_never_reads_the_spending():
    def boom() -> float:
        raise AssertionError("spending read without a spending limit")

    trace, _, _ = run_world(BUNDLE, _no_finish_line(), policy="scripted", max_turns=4,
                            run_stop={"mode": "every_round"}, spent=boom)
    assert trace["summary"]["stopped"] == {"reason": "round_cap", "round": 4}
    assert "run_spent_usd" not in trace
    assert run_stop.parse_run_stop({"mode": "quiet", "quiet_rounds": 6}) == {"mode": "quiet", "quiet_rounds": 6}


@pytest.mark.req("world-builder-page/the-stop-setting-is-checked")
def test_the_limits_are_checked():
    assert run_stop.parse_run_stop({"mode": "quiet", "max_rounds": 40, "max_spend_usd": 0.5}) == {
        "mode": "quiet", "quiet_rounds": 6, "max_rounds": 40, "max_spend_usd": 0.5}
    assert run_stop.parse_run_stop({"mode": "every_round", "max_spend_usd": 1}) == {"mode": "every_round",
                                                                                  "max_spend_usd": 1.0}
    assert run_stop.parse_run_stop({"mode": "every_round", "max_rounds": None}) == {"mode": "every_round"}
    for bad in ({"mode": "quiet", "max_rounds": 0}, {"mode": "quiet", "max_rounds": 501},
                {"mode": "quiet", "max_rounds": 4.0}, {"mode": "quiet", "max_rounds": True},
                {"mode": "quiet", "max_spend_usd": 0}, {"mode": "quiet", "max_spend_usd": 100.5},
                {"mode": "quiet", "max_spend_usd": "1"}, {"mode": "quiet", "max_spend_usd": float("nan")},
                {"mode": "every_round", "max_rounds": 3, "judge": "stop once agreed"}):
        with pytest.raises(ValueError):
            run_stop.parse_run_stop(bad)
