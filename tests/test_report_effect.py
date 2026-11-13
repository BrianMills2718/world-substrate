"""The action-only `append_report` effect: one immutable report record into a participant's string_list field.

Every test drives the real compiler (`CausalModel`), the real installer (`scripts.run_authored_world.build_engine`)
and the real engine (`engine.submit`); nothing here calls a model.  A report records the evidence that one entity
told another something -- who, to whom, what, when -- and never a belief, norm or stance.
"""
from __future__ import annotations

import json
from copy import deepcopy
from typing import Any

import pytest

from scripts.run_authored_world import build_engine
from world_substrate.action_authoring import (
    ACTION_EFFECT_OPS,
    EFFECT_OPS,
    REPORT_OP,
    REPORT_RECORD_KEYS,
    ActionDeclarationError,
    CausalModel,
    encode_report_record,
    report_record,
)

REQ = "causal-model-authoring/an-action-appends-one-report-record-to-a-participants-list"
REPORTS = "components.inbox.reports"


def bundle() -> dict[str, Any]:
    return {
        "schema_version": "world-substrate-authoring-bundle/v0",
        "world": {"id": "office", "label": "Office", "summary": "Three colleagues pass reports.", "location": "office", "content_version": 1},
        "components": [
            {"name": "member", "fields": [{"name": "role", "type": "string", "default": "clerk"}]},
            {"name": "inbox", "fields": [
                {"name": "reports", "type": "string_list", "default": []},
                {"name": "notes", "type": "string_list", "default": []},
                {"name": "title", "type": "string", "default": "clerk"},
            ]},
        ],
        "entities": [
            {"id": who, "label": who.title(), "categories": ["member"],
             "components": {"member": {"role": "clerk"}, "inbox": {"reports": [], "notes": ["keep me"], "title": "clerk"}}}
            for who in ("ana", "ben", "cai")
        ],
        "actions": [{
            "kind": "send-report", "description": "Tell one colleague something.",
            "fields": [{"name": "recipient", "type": "entity_ref"}, {"name": "content", "type": "string"}],
        }],
    }


def mechanic(**overrides: Any) -> dict[str, Any]:
    row = {
        "schema_version": "world-substrate-action-mechanic/v0",
        "mechanic_id": "office.action.send-report",
        "version": "1",
        "action_kind": "send-report",
        "rationale": "A member tells another member something; the words are filed in the recipient's inbox.",
        "actor_selector": {"categories": ["member"], "components": ["inbox"]},
        "participants": {"recipient": {"categories": ["member"], "components": ["inbox"]}},
        "parameters": {"content": ["The pump is dry."]},
        "checks": [{
            "label": "A member does not report to themselves",
            "left": {"entity_id": "actor"}, "op": "ne", "right": {"entity_id": "recipient"},
        }],
        "effects": [{
            "participant": "recipient", "path": REPORTS, "op": REPORT_OP,
            "value": {"action_field": "content"},
        }],
        "limits": ["Records that words were delivered; says nothing about whether they are true or believed."],
        "tests": ["a report appends one record to the recipient's inbox and nothing else"],
    }
    row.update(overrides)
    return row


def causal(*mechanics: dict[str, Any], processes: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    value: dict[str, Any] = {
        "schema_version": "world-substrate-causal-model/v0",
        "mechanics": list(mechanics or [mechanic()]),
        "terminal": None,
    }
    if processes is not None:
        value["processes"] = processes
    return value


def fresh():
    engine, model, _profile = build_engine(bundle(), causal())
    return engine, model


def send(engine, actor: str, recipient: str, content: Any, *, revision: int | None = None) -> dict[str, Any]:
    return engine.submit({
        "actor": actor, "kind": "send-report", "controller": "test",
        "base_revision": engine.world.revision if revision is None else revision,
        "recipient": recipient, "content": content,
    })


def reports(engine, who: str) -> list[str]:
    return engine.world.entities[who].component("inbox").reports


# ---------------------------------------------------------------------------
# What a committed report is


@pytest.mark.req(REQ)
def test_two_reports_append_in_order_and_keep_the_older_entry_byte_for_byte():
    engine, _ = fresh()
    first = send(engine, "ana", "ben", "The pump is dry.")
    assert first["status"] == "accepted"
    older = reports(engine, "ben")[0]
    assert isinstance(older, str)

    second = send(engine, "cai", "ben", 'Ana said "dry" -- is it?')
    assert second["status"] == "accepted"
    assert reports(engine, "ben")[0] == older  # the older entry is the same string, untouched
    assert len(reports(engine, "ben")) == 2

    one, two = (json.loads(entry) for entry in reports(engine, "ben"))
    assert one == {
        "id": one["id"], "source_id": "ana", "recipient_id": "ben", "content": "The pump is dry.",
        "source_revision": 0, "source_event_id": first["event"]["event_id"],
        "channel": "direct", "delivery_status": "delivered", "source_lineage": None, "lineage_status": "not_declared",
    }
    assert two["source_id"] == "cai" and two["recipient_id"] == "ben"
    assert two["content"] == 'Ana said "dry" -- is it?'
    assert two["source_revision"] == 1 and two["source_event_id"] == second["event"]["event_id"]
    assert one["id"] != two["id"] and one["id"].startswith("rpt-")


@pytest.mark.req(REQ)
def test_each_entry_is_one_json_string_with_exactly_the_declared_keys():
    engine, _ = fresh()
    result = send(engine, "ana", "ben", "Ünï — ok")
    (entry,) = reports(engine, "ben")
    record = json.loads(entry)
    assert isinstance(entry, str) and tuple(sorted(record)) == tuple(sorted(REPORT_RECORD_KEYS))
    assert set(record) == set(REPORT_RECORD_KEYS)
    assert entry == encode_report_record(record)  # sorted keys, compact, unescaped text
    assert record["content"] == "Ünï — ok"
    # No belief, norm or stance is recorded, and no independent provenance is inferred.
    assert record["source_lineage"] is None and record["lineage_status"] == "not_declared"
    assert record["channel"] == "direct" and record["delivery_status"] == "delivered"
    assert result["event"]["status"] == "accepted"


@pytest.mark.req(REQ)
def test_the_id_comes_from_world_revision_and_event_and_is_stable_across_fresh_worlds():
    first, _ = fresh()
    again, _ = fresh()
    one = send(first, "ana", "ben", "same words")
    two = send(again, "ana", "ben", "same words")
    assert reports(first, "ben") == reports(again, "ben")
    record = json.loads(reports(first, "ben")[0])
    assert record["id"] == report_record(
        world_id=first.world.world_id, revision=0, event_id=one["event"]["event_id"],
        source_id="ana", recipient_id="ben", content="same words",
    )["id"]
    assert one["event"]["event_id"] == two["event"]["event_id"]
    # A different event (or revision) gives a different id even for the same words.
    send(first, "ana", "ben", "same words")
    assert len({json.loads(entry)["id"] for entry in reports(first, "ben")}) == 2


@pytest.mark.req(REQ)
def test_only_the_recipients_list_and_cause_change_and_the_sender_is_the_real_actor():
    engine, _ = fresh()
    before = deepcopy(engine.world.material_dict())
    result = send(engine, "ana", "ben", "hello")
    event = result["event"]
    assert {change["path"] for change in event["changes"] if not change["path"].startswith("revision")} == {
        f"entities.ben.{REPORTS}", "entities.ben.last_cause_event_id",
    }
    assert event["causal_bearer"]["id"] == "ana"
    assert json.loads(reports(engine, "ben")[0])["source_id"] == "ana"
    assert reports(engine, "ana") == [] and reports(engine, "cai") == []
    assert engine.world.entities["ben"].component("inbox").notes == ["keep me"]  # a sibling list is not touched
    after = engine.world.material_dict()
    assert after["entities"]["cai"] == before["entities"]["cai"]
    assert after["entities"]["ana"] == before["entities"]["ana"]


# ---------------------------------------------------------------------------
# Authority


@pytest.mark.req(REQ)
def test_compiler_derives_exact_read_and_write_scope_for_the_target_append():
    engine, model = fresh()
    declared = model.mechanics[0]
    assert declared.write_paths == (
        f"entities.<recipient>.{REPORTS}",
        "entities.<recipient>.last_cause_event_id",
    )
    # Like `add`, appending reads the field it extends; selectors read their category and components.
    assert declared.read_paths == (
        "entities.<actor>.category_ids",
        "entities.<actor>.components.inbox",
        "entities.<recipient>.category_ids",
        "entities.<recipient>.components.inbox",
        f"entities.<recipient>.{REPORTS}",
    )
    event = send(engine, "ana", "ben", "hi")["event"]
    assert event["declared_write_paths"] == list(declared.write_paths)
    assert event["declared_read_paths"] == list(declared.read_paths)


@pytest.mark.req(REQ)
def test_engine_refuses_the_append_when_the_installed_scope_does_not_cover_it():
    engine, _ = fresh()
    rule = engine.registry.action("send-report")
    rule.write_paths = ("entities.<recipient>.last_cause_event_id",)  # a defective install: the list is not declared
    before = deepcopy(engine.world.material_dict())
    result = send(engine, "ana", "ben", "hi")
    assert result["status"] == "scope_violation"
    violation = next(check for check in result["event"]["checks"] if not check["ok"])
    assert violation["actual"] == [f"entities.ben.{REPORTS}"]
    assert engine.world.material_dict() == before


@pytest.mark.req(REQ)
def test_the_new_op_is_action_only_and_the_legacy_ops_are_unchanged():
    assert EFFECT_OPS == {"set", "add", "subtract"}
    assert ACTION_EFFECT_OPS == ("set", "add", "subtract", "append_report")
    process = {
        "process_id": "office.process.auto-report", "rationale": "A process must not file reports.",
        "selector": {"categories": ["member"], "components": ["inbox"]}, "checks": [],
        "effects": [{"participant": "it", "path": REPORTS, "op": REPORT_OP, "value": {"literal": "x"}}],
    }
    with pytest.raises(ActionDeclarationError, match="action-only"):
        CausalModel.from_dict(causal(processes=[process]), bundle=bundle())


# ---------------------------------------------------------------------------
# Declarations that are refused when compiled


def compile_with(**effect_changes: Any) -> CausalModel:
    effect = {"participant": "recipient", "path": REPORTS, "op": REPORT_OP, "value": {"action_field": "content"}}
    effect.update(effect_changes)
    return CausalModel.from_dict(causal(mechanic(effects=[effect])), bundle=bundle())


@pytest.mark.req(REQ)
def test_a_well_formed_declaration_compiles():
    assert compile_with().mechanics[0].effects[0]["op"] == REPORT_OP


@pytest.mark.req(REQ)
@pytest.mark.parametrize("changes, message", [
    ({"path": "components.inbox.title"}, "string_list target"),
    ({"path": "components.inbox.missing"}, "unsupported or unknown state path"),
    ({"value": {"literal": "x"}}, "action_field naming a string field"),
    ({"value": {"action_field": "recipient"}}, "action_field naming a string field"),
    ({"value": {"participant": {"name": "recipient", "path": REPORTS}}}, "action_field naming a string field"),
    ({"participant": "actor"}, "other than the actor"),
    ({"participant": "nobody"}, "unknown participant"),
])
def test_declarations_that_do_not_target_a_list_from_actor_text_are_refused(changes, message):
    with pytest.raises(ActionDeclarationError, match=message):
        compile_with(**changes)


@pytest.mark.req(REQ)
def test_one_action_declares_at_most_one_report():
    effect = {"participant": "recipient", "path": REPORTS, "op": REPORT_OP, "value": {"action_field": "content"}}
    with pytest.raises(ActionDeclarationError, match="at most one append_report"):
        CausalModel.from_dict(causal(mechanic(effects=[effect, dict(effect, path="components.inbox.notes")])), bundle=bundle())


@pytest.mark.req(REQ)
def test_the_target_must_belong_to_the_participants_declared_components():
    narrow = mechanic(participants={"recipient": {"categories": ["member"], "components": ["member"]}})
    with pytest.raises(ActionDeclarationError, match="does not require component 'inbox'"):
        CausalModel.from_dict(causal(narrow), bundle=bundle())


# ---------------------------------------------------------------------------
# Refused moves leave the world exactly as it was


def assert_refused_without_mutation(engine, result: dict[str, Any], status: str, before: dict[str, Any], events_before: int) -> dict[str, Any]:
    assert result["status"] == status
    assert engine.world.material_dict() == before  # no state, revision or tick moved
    assert len(engine.world.events) == events_before + 1  # but the refusal itself is on record
    assert result["event"]["status"] == status
    return result["event"]


@pytest.mark.req(REQ)
@pytest.mark.parametrize("content", [123, 1.5, True, None, ["a"], {"a": 1}, ""])
def test_nonstring_or_empty_content_is_refused_visibly_and_nothing_is_written(content):
    engine, _ = fresh()
    send(engine, "ana", "ben", "kept")
    before, events = deepcopy(engine.world.material_dict()), len(engine.world.events)
    result = send(engine, "cai", "ben", content)
    event = assert_refused_without_mutation(engine, result, "invalid_action", before, events)
    assert "content does not match string" in event["checks"][0]["actual"][0]
    assert len(reports(engine, "ben")) == 1


@pytest.mark.req(REQ)
@pytest.mark.parametrize("corrupt", ["not a list", None, 7, [1], ["fine", 2]])
def test_a_target_that_is_not_a_list_of_strings_is_refused_and_nothing_is_written(corrupt):
    engine, _ = fresh()
    engine.world.entities["ben"].component("inbox").reports = corrupt
    before, events = deepcopy(engine.world.material_dict()), len(engine.world.events)
    result = send(engine, "ana", "ben", "hello")
    event = assert_refused_without_mutation(engine, result, "precondition_failed", before, events)
    failed = [check for check in event["checks"] if not check["ok"]]
    assert [check["label"] for check in failed] == [f"the recipient's {REPORTS} holds a list of text records"]
    assert failed[0]["required"] == "list of strings"
    assert engine.world.entities["ben"].component("inbox").reports == corrupt


@pytest.mark.req(REQ)
def test_missing_recipient_and_self_report_are_refused_by_the_ordinary_checks():
    engine, _ = fresh()
    before, events = deepcopy(engine.world.material_dict()), len(engine.world.events)
    ghost = assert_refused_without_mutation(engine, send(engine, "ana", "ghost", "hello"), "precondition_failed", before, events)
    assert "the recipient named exists" in [check["label"] for check in ghost["checks"] if not check["ok"]]
    events += 1
    own = assert_refused_without_mutation(engine, send(engine, "ana", "ana", "hello"), "precondition_failed", before, events)
    assert [check["label"] for check in own["checks"] if not check["ok"]] == ["A member does not report to themselves"]


@pytest.mark.req(REQ)
def test_a_stale_revision_is_refused_and_a_refused_report_leaves_no_trace_in_the_list():
    engine, _ = fresh()
    send(engine, "ana", "ben", "first")
    before, events = deepcopy(engine.world.material_dict()), len(engine.world.events)
    result = send(engine, "cai", "ben", "second", revision=0)
    assert_refused_without_mutation(engine, result, "stale_revision", before, events)
    assert [json.loads(entry)["content"] for entry in reports(engine, "ben")] == ["first"]
