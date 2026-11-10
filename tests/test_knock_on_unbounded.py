"""ai-judge plan J0 (docs/plans/ai_judge.md): knock-on chains of any length run to the end in one moment.

A1: 50 chains of 100 links fall in one moment, every step names the step that caused it; a loop still ends; a step
a failed check stops is recorded with its blocker. A7: a run recorded under the old cap of 32 replays under it.
"""
from __future__ import annotations

import time

import pytest

from scripts.run_authored_world import build_engine, run_world
from tests.knock_on_worlds import fifty_chains, loop, truck_without_fuel
from world_substrate.engine import LEGACY_REACTION_LIMIT, Engine, recorded_reaction_limit


def _pull(engine):
    offered = engine.discover("sam", kind="pull")["available"]
    return engine.submit(dict(offered[0]["action"], controller="test"))


@pytest.mark.req("transition-engine/fifty-chains-of-a-hundred-links-finish-in-one-moment")
@pytest.mark.req("information-delivery/a-knock-on-step-names-the-step-that-caused-it")
def test_fifty_chains_of_a_hundred_links_finish_in_one_moment():
    engine, _, _ = build_engine(*fifty_chains(50, 100))
    # CPU time, not wall time: the bound is on the engine's work, and wall time on a shared machine measures the
    # load (2026-11-10: 26.6s alone, 128s inside a full suite while two other suites ran, load average 63 on 20 cores).
    started = time.process_time()
    result = _pull(engine)
    elapsed = time.process_time() - started
    assert result["status"] == "accepted"
    steps = [step for event in result["reactions"] for step in event["reaction_steps"]]
    assert len(steps) == 5000
    assert len({step["it"] for step in steps}) == 5000
    ids = {result["event"]["event_id"]} | {e["event_id"] for e in result["reactions"]}
    assert all(step["caused_by"] and set(step["caused_by"]) <= ids for step in steps)
    entities = engine.world.material_dict()["entities"]
    assert all(entities[f"c{c}-{n}"]["components"]["link"]["fallen"] for c in range(1, 51) for n in range(1, 101))
    # One moment: one command, no tick passed.
    assert len(engine.world.commands) == 1 and {e["tick"] for e in engine.world.events} == {0}
    # Link n's step names the event that made link n-1 fall: the chain is followed back step by step.
    by_event = {e["event_id"]: e for e in result["reactions"]}
    wave_of = {step["it"]: e["reaction_wave"] for e in result["reactions"] for step in e["reaction_steps"]}
    for e in result["reactions"]:
        for step in e["reaction_steps"]:
            c, n = step["it"][1:].split("-")
            # The step names the thing it read that its cause changed: the run page opens it to that step.
            assert step["via"] == (["lever"] if n == "1" else [f"c{c}-{int(n) - 1}"])
            if n != "1":
                parent = by_event[step["caused_by"][0]]
                assert f"c{c}-{int(n) - 1}" in {s["it"] for s in parent["reaction_steps"]}
                assert wave_of[step["it"]] == wave_of[f"c{c}-{int(n) - 1}"] + 1
    assert elapsed < 120, f"5,000 steps took {elapsed:.1f}s of CPU time"


@pytest.mark.req("transition-engine/a-loop-still-ends")
def test_a_loop_still_ends_with_each_rule_firing_once_per_thing():
    engine, _, _ = build_engine(*loop(40))
    result = _pull(engine)
    assert result["status"] == "accepted"
    steps = [(e["rule_id"], s["it"]) for e in result["reactions"] for s in e["reaction_steps"]]
    assert len(steps) == len(set(steps)) == 40  # d2..d40, then d1 once more, then nothing is new
    knocks = {k: v["components"]["link"]["knocks"] for k, v in engine.world.material_dict()["entities"].items()
              if k.startswith("d")}
    assert set(knocks.values()) == {1}
    assert engine.replay()["ok"]


@pytest.mark.req("transition-engine/a-blocked-knock-on-step-is-recorded-with-its-blocker")
@pytest.mark.req("information-delivery/a-stopped-step-is-recorded-with-its-blocker")
def test_a_blocked_step_is_recorded_with_its_blocker_and_nothing_follows():
    engine, _, _ = build_engine(*truck_without_fuel(40))
    result = _pull(engine)
    assert result["status"] == "accepted"
    assert [s["it"] for e in result["reactions"] for s in e["reaction_steps"]][-1] == "step-40"
    assert len(result["reactions"]) == 40
    [blocked] = result["blocked_reactions"]
    assert blocked["rule_id"] == "truck-leaves" and blocked["it"] == "truck"
    assert [f["label"] for f in blocked["failed"]] == ["the truck has fuel"]
    assert blocked["failed"][0]["actual"] == 0
    assert blocked["after"] == result["reactions"][-1]["event_id"]  # the step-40 event led to it
    assert engine.world.material_dict()["entities"]["truck"]["components"]["truck"]["left_yard"] is False


@pytest.mark.req("transition-engine/a-blocked-knock-on-step-is-recorded-with-its-blocker")
def test_run_record_summarises_each_moment_and_its_blocked_step():
    trace, _, _ = run_world(*truck_without_fuel(40), policy="scripted", max_turns=1)
    turn = trace["transcript"][0]
    [moment] = turn["knock_on"]
    assert moment == {"trigger": "r1-e00001", "trigger_rule": "pull-lever", "steps": 40, "with_cause": 40,
                      "blocked": 1}
    [blocked] = turn["blocked_reactions"]
    assert blocked["after"] == "r1-e00041" and blocked["failed"][0]["check"] == "the truck has fuel"
    assert trace["reaction_limit"] is None


@pytest.mark.req("transition-engine/a-run-saved-under-the-old-limit-replays-under-it")
def test_a_record_without_a_limit_ran_under_32_and_replays_refused():
    assert recorded_reaction_limit({}) == LEGACY_REACTION_LIMIT == 32
    assert recorded_reaction_limit({"reaction_limit": None}) is None
    bundle, rules = loop(40)
    old, _, _ = build_engine(bundle, rules, reaction_limit=recorded_reaction_limit({}))
    refused = _pull(old)
    assert refused["status"] == "reaction_limit"
    assert [c["label"] for c in refused["event"]["checks"] if not c["ok"]] == [
        "Knock-on effects settle within 32 reactions"]
    # The recorded commands replay under the recorded limit (the default for a record that names none).
    replayed = Engine.replay_commands(initial_snapshot=old.initial_snapshot(), commands=old.world.commands,
                                      registry=old.registry, component_types=old._component_types)
    assert replayed.world.commands[-1]["status"] == "reaction_limit"
    with pytest.raises(ValueError, match="status differs"):
        Engine.replay_commands(initial_snapshot=old.initial_snapshot(), commands=old.world.commands,
                               registry=old.registry, component_types=old._component_types,
                               reaction_limit=None)
    # A new run of the same world has no such limit.
    new, _, _ = build_engine(bundle, rules)
    assert _pull(new)["status"] == "accepted"


@pytest.mark.req("transition-engine/a-run-saved-under-the-old-limit-replays-under-it")
def test_a_round_refused_at_the_old_limit_says_so_in_its_record_and_share():
    from scripts.world_builder_service import _mark_refused_world_changes
    from tests.knock_on_worlds import wind_chain

    label = "Knock-on effects settle within 32 reactions"
    old, _, _ = run_world(*wind_chain(40), policy="scripted", max_turns=1, reaction_limit=32)
    [refused] = [e for e in old["transcript"][0]["world_events"] if e.get("refused")]
    assert refused["rule_id"] == "wind-topples-the-first" and refused["refused"] == label
    assert old["reaction_limit"] == 32
    # A round logged before J0 has no "refused" in its world events; the share link reads it from the engine events.
    turn = {"world_events": [{k: v for k, v in refused.items() if k != "refused"}]}
    _mark_refused_world_changes([turn], [{"event_id": refused["event_id"], "status": "reaction_limit",
                                          "checks": [{"label": label, "ok": False}]}])
    assert turn["world_events"][0]["refused"] == label
    # The same world run now: the wind's push runs all 39 dominoes after it, in one moment.
    new, _, _ = run_world(*wind_chain(40), policy="scripted", max_turns=1)
    assert not any(e.get("refused") for e in new["transcript"][0]["world_events"])
    assert sum(m["steps"] for m in new["transcript"][0]["knock_on"]) == 39


@pytest.mark.req("transition-engine/a-run-saved-under-the-old-limit-replays-under-it")
def test_a_share_link_made_before_j0_shows_the_refusal_when_opened(tmp_path, monkeypatch):
    import json

    from scripts import world_builder_service as service

    label = "Knock-on effects settle within 32 reactions"
    trace_id = "world-builder-live/run/old"
    row = {"trace_id": trace_id, "status": 200, "path": "/run", "result": {"engine_events": [
        {"event_id": "r1-e00001", "status": "accepted"},
        {"event_id": "r1-e00002", "status": "reaction_limit", "checks": [{"label": label, "ok": False}]}]}}
    (tmp_path / "runs_2026-11-10.jsonl").write_text(json.dumps(row) + "\n")
    monkeypatch.setenv("WORLD_BUILDER_RUN_LOG_DIR", str(tmp_path))
    # As a share made before J0 stored it: the refused world change listed with no word of the refusal.
    record = {"runs": [{"trace_id": trace_id}], "rounds": [
        {"turn": 1, "world_events": [{"event_id": "r1-e00002", "rule_id": "wind-topples-the-first", "changes": []}]}]}
    service._mark_old_share_refusals(record)
    assert record["rounds"][0]["world_events"][0]["refused"] == label
    # A share made since J0 was marked when made, so opening it reads no run log.
    marked = {"refusals_marked": True, "runs": [{"trace_id": trace_id}],
              "rounds": [{"turn": 1, "world_events": [{"event_id": "r1-e00002", "changes": []}]}]}
    service._mark_old_share_refusals(marked)
    assert "refused" not in marked["rounds"][0]["world_events"][0]


@pytest.mark.req("transition-engine/a-run-saved-under-the-old-limit-replays-under-it")
def test_an_old_share_keeps_its_refusal_once_its_runs_leave_the_run_log(tmp_path, monkeypatch):
    """Opening an old share while its runs are in the run log writes the refusal into the stored share, so the link
    still shows it after those log days pass out of the share window (cold review of #363, B1)."""
    import json

    from scripts import world_builder_service as service

    label = "Knock-on effects settle within 32 reactions"
    trace_id = "world-builder-live/run/old"
    row = {"trace_id": trace_id, "status": 200, "path": "/run", "result": {"engine_events": [
        {"event_id": "r1-e00002", "status": "reaction_limit", "checks": [{"label": label, "ok": False}]}]}}
    log = tmp_path / "logs"
    log.mkdir()
    (log / "runs_2026-11-10.jsonl").write_text(json.dumps(row) + "\n")
    monkeypatch.setenv("WORLD_BUILDER_RUN_LOG_DIR", str(log))
    monkeypatch.setenv("WORLD_BUILDER_SHARE_DB", str(tmp_path / "shares.sqlite"))
    record = {"created": "2026-11-10T00:00:00Z", "runs": [{"trace_id": trace_id}], "rounds": [
        {"turn": 1, "world_events": [{"event_id": "r1-e00002", "rule_id": "wind-topples-the-first", "changes": []}]}]}
    share_id = service._save_share("client", record)
    opened = service._open_share(share_id)
    assert opened["rounds"][0]["world_events"][0]["refused"] == label
    # Three more days of runs: the run that held the refusal is no longer read, and the share still says so.
    for day in ("11", "12", "13"):
        (log / f"runs_2026-11-{day}.jsonl").write_text("")
    (log / "runs_2026-11-10.jsonl").unlink()
    later = service._open_share(share_id)
    assert later["refusals_marked"] is True
    assert later["rounds"][0]["world_events"][0]["refused"] == label
    # A share whose runs are already gone from the log is left as stored: nothing is marked that was not read.
    gone = service._save_share("client", {**record, "runs": [{"trace_id": "world-builder-live/run/gone"}]})
    assert "refusals_marked" not in service._open_share(gone)
