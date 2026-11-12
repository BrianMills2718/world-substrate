from unittest.mock import Mock

import pytest

from scripts.probe_actor_information import inspect_generated_boundary, run_job


@pytest.mark.req("information-delivery/complete-actor-input-boundary")
@pytest.mark.parametrize("wrapped", [False, True])
def test_probe_observes_one_job_and_returns_the_actual_payload(wrapped):
    payload = {"ok": True, "bundle": {"actor_information": {"version": 1}}}
    final = {"status": "done", "http_status": 200, "payload": payload} if wrapped else payload
    request = Mock(side_effect=[{"ok": True, "job_id": "opaque"},
                                {"ok": True, "status": "running", "job_id": "opaque"}, final])
    assert run_job(request, "/generate-world", {"description": "source"}, pause=lambda _: None, report=lambda _: None) == payload
    assert request.call_count == 3
    assert request.call_args_list[0].args == ("/generate-world", {"description": "source", "async": True})
    assert [call.args for call in request.call_args_list[1:]] == [("/jobs/opaque",), ("/jobs/opaque",)]


@pytest.mark.req("information-delivery/complete-actor-input-boundary")
def test_probe_observation_timeout_never_restarts_a_paid_job():
    request = Mock(side_effect=[{"ok": True, "job_id": "opaque"}, TimeoutError("observation timeout")])
    with pytest.raises(TimeoutError, match="observation timeout"):
        run_job(request, "/run", {"policy": "resident"}, pause=lambda _: None, report=lambda _: None)
    assert [call.args[0] for call in request.call_args_list] == ["/run", "/jobs/opaque"]


@pytest.mark.req("information-delivery/complete-actor-input-boundary")
def test_probe_wrapped_job_failure_is_visible_without_a_replacement():
    request = Mock(side_effect=[{"job_id": "opaque"},
                                {"status": "done", "http_status": 422, "payload": {"ok": False, "error": "failed validation"}}])
    with pytest.raises(RuntimeError, match="failed validation"):
        run_job(request, "/generate-world", {}, pause=lambda _: None, report=lambda _: None)
    assert request.call_count == 2


@pytest.mark.req("native-coordination/independent-generated-concern-procedure")
def test_probe_refuses_a_legacy_or_forced_procedure_before_resident_calls():
    build = {"bundle": {"actor_information": {}, "entities": [{"components": {name: {} for name in
        ("validation_decision", "actor_position", "technical_condition", "technical_role")}}]},
        "causal_model": {"mechanics": [{"action_kind": kind} for kind in
            ("record-assent", "withdraw-assent", "repair-condition", "complete-validation", "activate")], "processes": []}}
    assert inspect_generated_boundary(build)["passed"]
    build["causal_model"]["processes"] = [{"process_id": "timer-repair", "effects": [
        {"path": "components.technical_condition.passing", "op": "set", "value": True}]}]
    assert not inspect_generated_boundary(build)["passed"]
    build["causal_model"]["processes"] = []
    build["bundle"]["entities"][0]["components"]["group_decision"] = {}
    assert not inspect_generated_boundary(build)["passed"]
