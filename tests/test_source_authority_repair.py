"""Offline checks of source authority and the existing bounded build repair seam."""
from copy import deepcopy
from types import ModuleType, SimpleNamespace
import json
import sys
from unittest.mock import Mock

import pytest

from test_initial_actor_knowledge import _world
from scripts import review_rules as reviews
from scripts import world_builder_service as service


def approved():
    return {"findings": [], "actor_input_review": {
        "public_summary": {"authorized": True, "explanation": "The source shares the activation question."},
        "actors": [{"actor_id": actor, "authorized": True, "explanation": "Only source-authorized facts."}
                   for actor in ["ari", "bo"]]},
        "canonical_state_review": {"consistent": True,
            "explanation": "The source requires a repairable condition; technical_condition.passing alone owns it."}}


def call_review(monkeypatch, answer):
    client = ModuleType("llm_client")
    client.render_prompt = Mock(return_value=[{"role": "user", "content": "original description"}])
    client.call_llm_json_schema = Mock(return_value=(answer, SimpleNamespace(cost=0.01)))
    monkeypatch.setitem(sys.modules, "llm_client", client)
    bundle, causal = _world()
    return client, bundle, causal


def test_clean_independent_review_uses_one_existing_call_with_actual_contracts(monkeypatch):
    client, bundle, causal = call_review(monkeypatch, approved())
    assert reviews.review_rules("Original source", bundle, causal, trace_id="same", max_budget=0.4) == ([], 0.01)
    call = client.call_llm_json_schema
    assert call.call_count == 1
    _, messages, schema = call.call_args.args
    assert "canonical_state_review" in schema["required"]
    assert "all starting entity fields" in messages[1]["content"]
    assert "technical_condition.passing" in messages[1]["content"]
    assert "immutable historical" in messages[1]["content"]
    assert client.render_prompt.call_args.kwargs["description"] == "Original source"
    assert json.loads(client.render_prompt.call_args.kwargs["start"])["condition-activate"]["components"] == {
        "technical_condition": {"passing": False}}


@pytest.mark.parametrize("verdict,repairable", [
    (None, False), ({"consistent": "yes", "explanation": "Source"}, False),
    ({"consistent": False, "explanation": " "}, False),
    ({"consistent": False, "explanation": "Pump.current_failed duplicates technical_condition and no repair writes it."}, True)])
def test_required_canonical_verdict_fails_closed(monkeypatch, verdict, repairable):
    answer = approved()
    if verdict is None:
        del answer["canonical_state_review"]
    else:
        answer["canonical_state_review"] = verdict
    _, bundle, causal = call_review(monkeypatch, answer)
    with pytest.raises(reviews.CanonicalStateAuthorityError) as caught:
        reviews.review_rules("Original source", bundle, causal, trace_id="same", max_budget=0.4)
    assert caught.value.repairable is repairable


def test_malformed_canonical_verdict_cannot_be_repaired_as_a_privacy_negative(monkeypatch):
    answer = approved()
    answer["actor_input_review"]["actors"][0]["authorized"] = False
    del answer["canonical_state_review"]
    _, bundle, causal = call_review(monkeypatch, answer)
    with pytest.raises(reviews.SourceDraftReviewError) as caught:
        reviews.review_rules("Original source", bundle, causal, trace_id="same", max_budget=0.4)
    assert not caught.value.repairable


def test_privacy_validation_checks_entire_verdict_before_allowing_repair():
    answer = approved()
    answer["actor_input_review"]["public_summary"]["authorized"] = False
    answer["actor_input_review"]["actors"][1]["explanation"] = ""
    with pytest.raises(reviews.ActorInputPrivacyError) as caught:
        reviews.require_actor_input_review(answer, ["ari", "bo"])
    assert not caught.value.repairable


def test_legacy_review_schema_stays_unchanged():
    assert reviews.review_schema(["repair"])["required"] == ["findings"]
    assert "canonical_state_review" not in reviews.review_schema(["repair"])["properties"]


def build_harness(monkeypatch, errors):
    bundle, causal = _world()
    built = {"bundle": bundle, "causal_model": causal, "briefs": {}, "people": [], "coverage": {},
             "not_modeled": [], "dropped_generated_rules": []}
    prepared = Mock(side_effect=[{"bundle": deepcopy(bundle)}, {"bundle": deepcopy(bundle)}])
    writer = Mock(return_value=built)
    laws = Mock(return_value=({"resources": [], "laws": []}, []))
    run = Mock(return_value=({"summary": {"active_at_end": True, "moves_at_end": ["one", "two"]}}, None, None))
    review = Mock(side_effect=errors)
    for name, value in {"prepare_people_world": prepared, "write_people_rules": writer,
                        "declare_people_laws": laws, "run_world": run, "review_rules": review,
                        "_trace_cost": Mock(return_value=0.01), "_settle_daily_budget": Mock(return_value=0.01),
                        "_settle_failed_call": Mock(), "_settle_late_hedges": Mock(),
                        "_new_trace_id": Mock(return_value="same-parent")}.items():
        monkeypatch.setattr(service, name, value)
    responder = SimpleNamespace(_llm_budget=Mock(return_value=0.4), _progress=Mock(), _json=Mock())
    request = {"source_draft_reviews": []}
    token = service._REQUEST.set(request)
    return responder, prepared, writer, laws, run, review, request, token


def negative():
    return reviews.CanonicalStateAuthorityError("Duplicate current condition", {
        "consistent": False, "explanation": "prototype_pump.hidden_actual_validation_condition stays failed after repair; remove duplicate current truth."},
        repairable=True)


def test_one_source_repair_reuses_original_source_trace_reservation_and_attempt(monkeypatch):
    error = negative()
    h, prepare, writer, laws, run, review, request, token = build_harness(monkeypatch, [error, ([], 0)])
    try:
        service.WorldBuilderHandler._generate_people_world(h, "client", "ORIGINAL SOURCE")
    finally:
        service._REQUEST.reset(token)
    assert prepare.call_count == writer.call_count == laws.call_count == review.call_count == 2
    assert h._llm_budget.call_count == service._settle_daily_budget.call_count == 1
    for call in prepare.call_args_list + review.call_args_list + laws.call_args_list:
        assert call.args[0] == "ORIGINAL SOURCE"
        assert call.kwargs["trace_id"] == "same-parent"
        assert call.kwargs["max_budget"] == 0.4
    assert "feedback" not in prepare.call_args_list[0].kwargs
    assert prepare.call_args_list[1].kwargs["feedback"] == error.feedback
    payload = h._json.call_args.args[1]
    rejected = payload["dry_run_attempts"][0]
    assert rejected["rejected_candidate"]["bundle"]
    assert rejected["source_review"] == error.review
    assert rejected["source_repair_feedback"] == error.feedback
    assert request["source_draft_reviews"] == [rejected]
    assert payload["dry_run"]["actor_inputs_reviewed"] is True
    assert all(call.kwargs["policy"] == "scripted" for call in run.call_args_list)


@pytest.mark.parametrize("errors,expected", [
    ([negative(), negative()], 2),
    ([RuntimeError("provider down")], 1),
    ([reviews.CanonicalStateAuthorityError("missing verdict")], 1),
    ([reviews.ActorInputPrivacyError("malformed privacy")], 1)])
def test_second_negative_or_unavailable_review_rejects_without_resident_execution(monkeypatch, errors, expected):
    h, prepare, writer, laws, run, review, request, token = build_harness(monkeypatch, errors)
    try:
        with pytest.raises((reviews.SourceDraftReviewError, RuntimeError)):
            service.WorldBuilderHandler._generate_people_world(h, "client", "ORIGINAL SOURCE")
    finally:
        service._REQUEST.reset(token)
    assert prepare.call_count == writer.call_count == review.call_count == expected
    assert not h._json.called
    assert h._llm_budget.call_count == service._settle_failed_call.call_count == 1
    assert not service._settle_daily_budget.called
    assert all(call.kwargs["policy"] == "scripted" for call in run.call_args_list)
    if expected == 2:
        assert len(request["source_draft_reviews"]) == 2


def test_scenario_feedback_is_separate_from_original_source(monkeypatch):
    from spec_pipeline import scenario_spec
    from scenario_spec import ScenarioSpecV1
    client = ModuleType("llm_client")
    client.call_llm_structured = Mock(return_value=(SimpleNamespace(public_summary="Safe public setup"), None))
    monkeypatch.setitem(sys.modules, "llm_client", client)
    scenario_spec("ORIGINAL SOURCE", model="fake", trace_id="same", max_budget=0.4,
                  feedback="Remove duplicate current condition")
    args = client.call_llm_structured.call_args.args
    assert args[1][1] == {"role": "user", "content": "ORIGINAL SOURCE"}
    assert "Remove duplicate current condition" in args[1][2]["content"]
    assert args[2] is ScenarioSpecV1


def test_valid_typed_privacy_negative_can_use_the_same_single_source_repair(monkeypatch):
    value = approved()
    value["actor_input_review"]["actors"][1].update(
        authorized=False, explanation="Source withholds the failure report; the brief reveals it.")
    with pytest.raises(reviews.ActorInputPrivacyError) as caught:
        reviews.require_actor_input_review(value, ["ari", "bo"])
    assert caught.value.repairable
    h, prepare, writer, laws, run, review, request, token = build_harness(monkeypatch, [caught.value, ([], 0)])
    try:
        service.WorldBuilderHandler._generate_people_world(h, "client", "ORIGINAL SOURCE")
    finally:
        service._REQUEST.reset(token)
    assert prepare.call_count == 2
    assert "Source withholds the failure report" in prepare.call_args.kwargs["feedback"]
    assert h._json.call_args.args[1]["ok"] is True


def test_service_error_log_retains_the_rejected_candidate_review_and_feedback(monkeypatch, tmp_path):
    error = negative()
    h, prepare, writer, laws, run, review, request, token = build_harness(monkeypatch, [error, negative()])
    request.update(path="/generate-world", who="local", client="client", summary={})
    monkeypatch.setattr(service, "_run_log_dir", lambda: tmp_path)
    try:
        with pytest.raises(reviews.CanonicalStateAuthorityError):
            service.WorldBuilderHandler._generate_people_world(h, "client", "ORIGINAL SOURCE")
        service._record_response(422, {"ok": False, "error": "source rejected"})
    finally:
        service._REQUEST.reset(token)
    logs = list(tmp_path.glob("*.jsonl"))
    assert len(logs) == 1
    record = json.loads(logs[0].read_text())
    rows = record["result"]["source_draft_reviews"]
    assert len(rows) == 2
    assert rows[0]["source_review"] == error.review
    assert rows[0]["source_repair_feedback"] == error.feedback
    assert rows[0]["rejected_candidate"]["bundle"]


def test_prepare_forwards_feedback_without_replacing_original_description(monkeypatch):
    from scripts import people_world
    stop = RuntimeError("stop after the source-call seam")
    spec_call = Mock(side_effect=stop)
    monkeypatch.setattr(people_world, "_pipeline", lambda: (None, SimpleNamespace(scenario_spec=spec_call)))
    monkeypatch.setattr(people_world, "hedged", lambda trace, call: call())
    monkeypatch.setattr(people_world, "fast_route", lambda model: None)
    with pytest.raises(RuntimeError, match="source-call seam"):
        people_world.prepare_people_world("ORIGINAL SOURCE", trace_id="same", max_budget=0.4,
                                          progress=Mock(), feedback="Remove the duplicate current condition")
    assert spec_call.call_args.args == ("ORIGINAL SOURCE",)
    assert spec_call.call_args.kwargs["feedback"] == "Remove the duplicate current condition"
    assert spec_call.call_args.kwargs["trace_id"] == "same"
    assert spec_call.call_args.kwargs["max_budget"] == 0.4


@pytest.mark.parametrize("error", [negative(), reviews.CanonicalStateAuthorityError("missing verdict")])
def test_final_selected_candidate_review_retains_rejection_without_another_retry(monkeypatch, tmp_path, error):
    h, prepare, writer, laws, run, review, request, token = build_harness(monkeypatch, [error])
    run.side_effect = ValueError("scripted test could not run")
    request.update(path="/generate-world", who="local", client="client", summary={})
    monkeypatch.setattr(service, "_run_log_dir", lambda: tmp_path)
    try:
        with pytest.raises(reviews.CanonicalStateAuthorityError):
            service.WorldBuilderHandler._generate_people_world(h, "client", "ORIGINAL SOURCE")
        service._record_response(422, {"ok": False, "error": "source rejected"})
    finally:
        service._REQUEST.reset(token)
    assert prepare.call_count == laws.call_count == review.call_count == 1
    assert writer.call_count == run.call_count == 2
    assert h._llm_budget.call_count == service._settle_failed_call.call_count == 1
    assert not h._json.called
    assert not service._settle_daily_budget.called
    rows = request["source_draft_reviews"]
    assert len(rows) == 1
    assert rows[0]["source_review"] == error.review
    assert rows[0]["source_repair_feedback"] == error.feedback
    assert rows[0]["source_repairable"] is error.repairable
    assert rows[0]["rejected_candidate"]["bundle"]
    assert rows[0]["error"] == "scripted test could not run"
    logs = list(tmp_path.glob("*.jsonl"))
    assert len(logs) == 1
    assert json.loads(logs[0].read_text())["result"]["source_draft_reviews"] == rows
    assert all(call.kwargs["policy"] == "scripted" for call in run.call_args_list)
