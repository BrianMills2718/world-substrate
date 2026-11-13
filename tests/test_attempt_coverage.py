"""Structural coverage checks; scripted readings do not prove model semantics."""
import sys
import types
from pathlib import Path
from unittest.mock import patch

import pytest

from world_substrate import attempt as api

pytestmark = pytest.mark.req("semantic-binding/whole-attempt-coverage")
TEXT = 'I record "withdraw support" and leave'
SIGNATURES = [{"kind": "record", "fields": [{"name": "text", "type": "string"}]}]


def response(status="complete", actions=None, remaining=None, kind="record"):
    return {"kind": kind, "fields": [{"field": "text", "value": "withdraw support",
            "quoted_span": '"withdraw support"'}], "nearest_kind": "record", "asks": "other",
            "names": ["other"], "why": "private reasoning", "coverage": {
                "status": status, "action_spans": actions if actions is not None else [TEXT],
                "unrepresented_spans": remaining if remaining is not None else []}}


def read(value, text=TEXT, strict=True):
    return api.read_interpretation(value, text, SIGNATURES, {"actor", "other"}, "actor",
                                   require_coverage=strict)


def test_schema_requires_closed_coverage():
    schema = api.interpreter_schema(SIGNATURES)
    assert "coverage" in schema["required"]
    coverage = schema["properties"]["coverage"]
    assert coverage["additionalProperties"] is False
    assert set(coverage["required"]) == {"status", "action_spans", "unrepresented_spans"}


@pytest.mark.parametrize("coverage", [None, {}, {"status": "complete"},
    {"status": "complete", "action_spans": [], "unrepresented_spans": []},
    {"status": "complete", "action_spans": ["absent"], "unrepresented_spans": []},
    {"status": "complete", "action_spans": [" "], "unrepresented_spans": []},
    {"status": "complete", "action_spans": [TEXT], "unrepresented_spans": ["leave"]},
    {"status": "partial", "action_spans": [TEXT], "unrepresented_spans": []},
    {"status": "other", "action_spans": [TEXT], "unrepresented_spans": []},
    {"status": "complete", "action_spans": [TEXT], "unrepresented_spans": [], "extra": True},
    {"status": "complete", "action_spans": TEXT, "unrepresented_spans": []}])
def test_malformed_explicit_coverage_rejected_even_in_legacy_mode(coverage):
    for strict in (False, True):
        reading = read({**response(), "coverage": coverage}, strict=strict)
        assert reading["unmatched"]
        assert reading["interpretation_rejection"] == "invalid_coverage"
        assert "coverage" not in reading
        assert "asks" not in reading


def test_strict_missing_coverage_and_legacy_compatibility():
    value = response()
    del value["coverage"]
    assert read(value)["interpretation_rejection"] == "invalid_coverage"
    legacy = read(value, strict=False)
    assert legacy["kind"] == "record"
    assert "coverage" not in legacy


@pytest.mark.parametrize("status", ["requires_decomposition", "partial", "ambiguous"])
def test_rejections_precede_wait_and_cannot_relay_requests(status):
    value = response(status, [] if status == "ambiguous" else ["record"], ["leave"], kind="wait")
    reading = read(value)
    assert reading["unmatched"]
    assert reading["interpretation_rejection"] == status
    assert reading["coverage"] == value["coverage"]
    assert "asks" not in reading
    command = api.envelope(reading, actor="actor", attempt=TEXT, base_revision=1, controller="test")
    assert command["kind"] == api.UNMATCHED_KIND
    assert command["attempt"] == TEXT
    assert command["interpretation_rejection"] == status
    assert command["coverage"] == value["coverage"]
    assert "private reasoning" not in api.rejection_message(reading)
    assert "no part" in api.rejection_message(reading).lower()


def test_quoted_content_single_action_and_metadata_not_action_fields():
    text = 'I record "withdraw support"'
    value = response(actions=[text])
    reading = read(value, text)
    assert reading["kind"] == "record"
    assert reading["coverage"] == value["coverage"]
    assert api.rejection_message(reading) is None
    command = api.envelope(reading, actor="actor", attempt=text, base_revision=0, controller="test")
    assert set(command) == {"actor", "kind", "base_revision", "controller", "text"}


def test_complete_unsupported_still_ordinary_gap():
    reading = read(response(kind="none"))
    assert reading["unmatched"]
    assert "interpretation_rejection" not in reading
    assert reading["asks"] == "other"


def test_complete_single_move_keeps_default_integer_and_only_fields():
    signatures = [{"kind": "record", "fields": [{"name": "quantity", "type": "integer"},
                   {"name": "target", "type": "entity_ref", "only": "other"}]}]
    reading = api.read_interpretation({**response(), "fields": []}, TEXT, signatures,
                                     {"actor", "other"}, "actor", require_coverage=True)
    assert reading["fields"] == {"quantity": 1, "target": "other"}


def test_derived_failure_retains_coverage():
    reading = {"kind": "record", "fields": {}, "quoted_spans": {}, "coverage": response()["coverage"]}
    signatures = [{"kind": "record", "fields": [{"name": "target", "type": "entity_ref",
                   "from": {"participant": "person", "path": "support.concern"}}]}]
    result = api.fill_derived(reading, signatures, lambda *_: None, {"actor"})
    assert result["unmatched"]
    assert result["coverage"] == reading["coverage"]


def test_interpret_requires_coverage_in_existing_single_model_call():
    value = response()
    del value["coverage"]
    calls = []
    fake = types.ModuleType("llm_client")
    fake.render_prompt = lambda *args, **kwargs: []
    def call(*args, **kwargs):
        calls.append(kwargs)
        return value, types.SimpleNamespace(cost=0)
    fake.call_llm_json_schema = call
    with patch.dict(sys.modules, {"llm_client": fake}):
        reading, _ = api.interpret(TEXT, actor="actor", signatures=SIGNATURES,
                                   entities={"actor": "Actor"}, model="fake", trace_id="fake", max_budget=0)
    assert len(calls) == 1
    assert reading["interpretation_rejection"] == "invalid_coverage"


def test_rejected_compound_envelope_is_persisted_and_replays_without_model():
    from reference_worlds.castaway.probe import build_transfer_engine

    engine = build_transfer_engine(Path(__file__).resolve().parents[1])
    before = engine.world.material_dict()
    reading = read(response("requires_decomposition", ["record"], ["leave"]))
    command = api.envelope(reading, actor="robinson", attempt=TEXT,
                           base_revision=engine.world.revision, controller="test")
    result = engine.submit(command)
    assert result["status"] == "unsupported_action"
    assert engine.world.material_dict() == before
    assert engine.world.commands[-1]["action"] == command
    with patch.dict(sys.modules, {"llm_client": None}):
        assert engine.replay()["ok"]


def test_installed_composite_can_represent_whole_attempt():
    signatures = [{"kind": "record-and-leave", "fields": []}]
    reading = api.read_interpretation({**response(kind="record-and-leave"), "fields": []},
                                     TEXT, signatures, {"actor"}, "actor", require_coverage=True)
    assert reading["kind"] == "record-and-leave"
    assert not reading.get("unmatched")
