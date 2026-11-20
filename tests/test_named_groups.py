"""A draft keeps every group the description names (world-builder-page/the-draft-keeps-every-named-group)."""
import json
import sys
from types import SimpleNamespace

import pytest

from scripts import people_world

DESC = "Ten groups (four countries, a health network, a partnership, technical, legal, logistics and community groups) decide by a deadline."


def _stub(monkeypatch, replies):
    calls = []
    def fake(model, messages, **kw):
        calls.append(messages)
        return SimpleNamespace(content=replies.pop(0))
    monkeypatch.setitem(sys.modules, "llm_client", SimpleNamespace(call_llm=fake, safe_json_loads=json.loads))
    return calls


@pytest.mark.req("world-builder-page/the-draft-keeps-every-named-group")
def test_the_check_returns_what_the_description_names_and_what_the_draft_left_out(monkeypatch):
    calls = _stub(monkeypatch, ['{"named": ["Country A", "Legal group"], "missing": ["Legal group"]}'])
    named, missing = people_world.check_named_groups(DESC, ["Country A"], trace_id="t", max_budget=1)
    assert named == ["Country A", "Legal group"] and missing == ["Legal group"]
    assert "Country A" in calls[0][1]["content"] and "four countries" in calls[0][0]["content"]


@pytest.mark.req("world-builder-page/the-draft-keeps-every-named-group")
def test_a_missing_group_makes_the_builder_ask_again_with_the_missing_names(monkeypatch):
    import scripts.generate_world_bundle as gwb
    monkeypatch.setattr(gwb, "is_recorded_authoring_replay", lambda: False)
    monkeypatch.setattr(people_world, "HEDGE_COPIES", 1)
    people = [SimpleNamespace(label="Country A")]
    full = [SimpleNamespace(label="Country A"), SimpleNamespace(label="Legal group")]
    feedbacks = []
    def scenario_spec(description, **kw):
        feedbacks.append(kw.get("feedback"))
        return SimpleNamespace(people=people if len(feedbacks) == 1 else full, public_summary="s", information_items=[], scheduled_moments=[], unsupported=[]), None
    monkeypatch.setattr(people_world, "_pipeline", lambda: (SimpleNamespace(compile_spec=lambda spec: (_ for _ in ()).throw(StopIteration)), SimpleNamespace(scenario_spec=scenario_spec)))
    _stub(monkeypatch, ['{"named": ["Country A", "Legal group"], "missing": ["Legal group"]}', '{"named": ["Country A", "Legal group"], "missing": []}'])
    notes = []
    with pytest.raises(StopIteration):
        people_world.prepare_people_world(DESC, trace_id="t", max_budget=1, progress=lambda *a, **k: notes.append(a))
    assert feedbacks[0] is None and "Legal group" in feedbacks[1]
    assert any("2 of 2 named groups are in the draft" in str(n) for n in notes)


def _bare_pipeline(monkeypatch, labels):
    """A draft with `labels` people and everything after the check stubbed, so prepare_people_world returns."""
    import scripts.generate_world_bundle as gwb
    monkeypatch.setattr(gwb, "is_recorded_authoring_replay", lambda: False)
    monkeypatch.setattr(people_world, "HEDGE_COPIES", 1)
    spec = SimpleNamespace(people=[SimpleNamespace(label=x) for x in labels], public_summary="s", information_items=[],
                           scheduled_moments=[], unsupported=[], independent_decision=None)
    compile_spec = SimpleNamespace(compile_spec=lambda s: ({"actions": []}, {}, {}), add_work_cycle=lambda *a, **k: None)
    sp = SimpleNamespace(scenario_spec=lambda description, **kw: (spec, None), action_signatures=lambda *a, **k: ([], None),
                         record_fields=lambda s, sigs: sigs)
    monkeypatch.setattr(people_world, "_pipeline", lambda: (compile_spec, sp))


@pytest.mark.req("world-builder-page/the-draft-keeps-every-named-group")
def test_a_check_that_could_not_run_is_recorded_with_its_error_not_only_shown_as_a_passing_note(monkeypatch):
    """#474: s4w4 has no named-groups call and no record of why; the note only reached the page while it was open."""
    _bare_pipeline(monkeypatch, ["Country A"])
    def broken(*a, **k):
        raise RuntimeError("budget refused before the call")
    monkeypatch.setitem(sys.modules, "llm_client", SimpleNamespace(call_llm=broken, safe_json_loads=json.loads))
    prepared = people_world.prepare_people_world(DESC, trace_id="t", max_budget=1, progress=lambda *a, **k: None)
    record = prepared["group_check"]
    assert record["checked"] is False and "RuntimeError: budget refused before the call" in record["error"]


@pytest.mark.req("world-builder-page/the-draft-keeps-every-named-group")
def test_a_check_that_ran_records_what_it_found_and_one_that_was_skipped_says_so(monkeypatch):
    _bare_pipeline(monkeypatch, ["Country A", "Legal group"])
    _stub(monkeypatch, ['{"named": ["Country A", "Legal group"], "missing": []}'])
    ran = people_world.prepare_people_world(DESC, trace_id="t", max_budget=1, progress=lambda *a, **k: None)["group_check"]
    assert ran == {"checked": True, "named": ["Country A", "Legal group"], "missing": [], "error": ""}
    import scripts.generate_world_bundle as gwb
    monkeypatch.setattr(gwb, "is_recorded_authoring_replay", lambda: True)
    skipped = people_world.prepare_people_world(DESC, trace_id="t", max_budget=1, progress=lambda *a, **k: None)["group_check"]
    assert skipped["checked"] is False and "recorded replay" in skipped["error"]
