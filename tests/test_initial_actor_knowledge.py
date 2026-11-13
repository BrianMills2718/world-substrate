"""Source-grounded review gates the exact actor inputs, without prose heuristics."""
import json
from pathlib import Path
import sys
from types import ModuleType, SimpleNamespace
from unittest.mock import Mock, patch

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "spikes/any-scenario-2026-10"))

from compile_spec import compile_spec
from scenario_spec import ScenarioSpecV1
from spec_pipeline import SPEC_SYSTEM, merge_causal, person_briefs
from scripts.review_rules import (ActorInputPrivacyError, initial_actor_inputs,
                                  require_actor_input_review, review_rules, review_schema)


def _world():
    spec = ScenarioSpecV1.model_validate({
        "scenario_id": "private_evidence", "title": "Independent evidence",
        "description": "Ari alone knows batch V17. Bo has not received the failure report.",
        "public_summary": "Ari and Bo decide whether to activate a system.",
        "people": [
            {"entity_id": "ari", "label": "Ari", "position": "Technician", "disposition": "Careful",
             "behavioral_profile": {"beliefs": ["Batch V17 needs investigation."]}},
            {"entity_id": "bo", "label": "Bo", "position": "Member", "disposition": "Practical",
             "behavioral_profile": {"goals": ["Make an independent decision."]}}],
        "behaviors": [{"request_id": "consider", "subject_refs": ["bo"],
                       "behavior_description": "Bo can decide.", "desired_effects": ["Bo chooses independently."],
                       "fidelity_need": "coarse", "causally_material": True}],
        "fidelity_assumptions": ["No prescribed social ending."],
        "independent_decision": {"decision_id": "activate", "question": "Activate?",
                                 "required_actor_ids": ["bo"], "validator_ids": ["ari"]},
    })
    return compile_spec(spec)[:2]


def _approved():
    return {"findings": [], "canonical_state_review": {
        "consistent": True, "explanation": "The compiled technical condition owns current truth; reports retain historical evidence."}, "actor_input_review": {
        "public_summary": {"authorized": True, "explanation": "Shared activation question from the source."},
        "actors": [
            {"actor_id": "ari", "authorized": True, "explanation": "Ari owns the detailed evidence."},
            {"actor_id": "bo", "authorized": True, "explanation": "Bo sees only the public question and own goals."}]}}


def _fake_client(answer, *, messages, cost=0.0):
    """Keep offline review tests independent of the optional live client."""
    client = ModuleType("llm_client")
    client.render_prompt = Mock(return_value=messages)
    client.call_llm_json_schema = Mock(return_value=(answer, SimpleNamespace(cost=cost)))
    return client


def test_review_schema_keeps_legacy_contract_and_requires_each_modern_actor():
    legacy = review_schema(["repair"])
    modern = review_schema(["repair"], ["ari", "bo"])
    assert legacy["required"] == ["findings"]
    assert modern["required"] == ["findings", "actor_input_review"]
    rows = modern["properties"]["actor_input_review"]["properties"]["actors"]
    assert rows["minItems"] == rows["maxItems"] == 2
    assert rows["items"]["properties"]["actor_id"]["enum"] == ["ari", "bo"]


@pytest.mark.parametrize("change", [
    lambda value: value.pop("actor_input_review"),
    lambda value: value["actor_input_review"]["actors"].pop(),
    lambda value: value["actor_input_review"]["actors"][1].update(actor_id="ari"),
    lambda value: value["actor_input_review"]["actors"][1].update(authorized="true"),
    lambda value: value["actor_input_review"]["actors"][1].update(explanation=" "),
    lambda value: value["actor_input_review"]["public_summary"].update(authorized=False),
])
def test_missing_malformed_or_disallowed_review_never_approves(change):
    value = _approved()
    change(value)
    with pytest.raises(ActorInputPrivacyError):
        require_actor_input_review(value, ["ari", "bo"])


def test_all_actors_with_source_basis_pass():
    require_actor_input_review(_approved(), ["ari", "bo"])


def test_existing_review_call_reads_actual_contexts_and_rejects_narrator_negative_knowledge():
    bundle, causal = _world()
    leaked = "You have not received the failure report or channel C / batch V17 details."
    bundle["actor_information"]["actors"]["bo"]["brief"] += " " + leaked
    # A reviewer must see the actual unsafe context, not a redacted substitute.
    contexts = initial_actor_inputs(bundle, causal)
    assert leaked in contexts["bo"]["brief"]
    answer = _approved()
    answer["actor_input_review"]["actors"][1].update(
        authorized=False, explanation="Narrator's withheld-report statement discloses the report and C/V17 to Bo.")
    client = _fake_client(answer, messages=[{"role": "user", "content": "original source"}])
    with patch.dict(sys.modules, {"llm_client": client}):
        with pytest.raises(ActorInputPrivacyError) as error:
            review_rules("Ari alone knows V17; Bo has no report.", bundle, causal, trace_id="offline", max_budget=0)
    assert error.value.review == answer["actor_input_review"]
    call = client.call_llm_json_schema
    assert call.call_count == 1  # Reuses the existing rules review, no extra stage.
    messages = call.call_args.args[1]
    payload = messages[-1]["content"]
    assert "EXACT initial actor inputs" in payload
    assert "original source" == messages[0]["content"]
    assert json.loads(payload[payload.index("{\n"):])["initial_actor_inputs"] == contexts
    assert leaked in payload


def test_review_accepts_explicit_approval_and_keeps_mechanical_findings_separate():
    bundle, causal = _world()
    answer = _approved()
    answer["findings"] = [{"rule_id": "missing", "description_words": "investigate",
                           "problem": "No investigation task."}]
    client = _fake_client(answer, messages=[], cost=0.125)
    with patch.dict(sys.modules, {"llm_client": client}):
        findings, cost = review_rules("source", bundle, causal, trace_id="offline", max_budget=0)
    assert findings == answer["findings"]
    assert cost == 0.125


def test_authoring_contract_explicitly_distinguishes_withheld_and_received_information():
    assert "Do not copy narrator statements of withheld information" in SPEC_SYSTEM
    assert "initially_delivered=true" in SPEC_SYSTEM
    assert "leave source_id null rather than inventing a sender" in SPEC_SYSTEM
    assert "must not appear in an intended recipient's brief or memories" in SPEC_SYSTEM


def test_modern_reports_are_projected_from_canonical_delivery_not_narrated_twice():
    from test_scenario_spec import _minimal

    raw = _minimal(public_summary="The legal group and Country B are considering a proposal.")
    modern = ScenarioSpecV1.model_validate(raw)
    bundle, causal, _ = compile_spec(modern)
    held_content = modern.information_items[0].content
    briefs = person_briefs(modern)
    assert held_content not in briefs["legal-group"]
    assert held_content not in briefs["country-b"]
    contexts = initial_actor_inputs(bundle, causal)
    assert held_content in contexts["legal-group"]["visible"]
    assert held_content not in json.dumps(contexts["country-b"])
    raw["public_summary"] = ""
    legacy = ScenarioSpecV1.model_validate(raw)
    assert held_content in person_briefs(legacy)["legal-group"]


def test_generated_rules_cannot_overwrite_compiled_report_exposure_log():
    compiled = {"schema_version": "world-substrate-causal-model/v0", "mechanics": [], "processes": []}
    generated = {"mechanics": [{"mechanic_id": "erase", "action_kind": "erase",
                               "effects": [{"participant": "recipient", "path": "components.report_log.entries",
                                            "op": "set", "value": {"literal": []}}]}]}
    merged, drops = merge_causal(compiled, generated)
    assert merged["mechanics"] == []
    assert any("compiled components" in row for row in drops)


def test_reviewer_receives_executable_report_and_public_procedure_semantics():
    from scripts.review_rules import builtin_semantics
    from world_substrate.action_authoring import REPORT_RECORD_KEYS
    bundle, _ = _world()
    contracts = builtin_semantics(bundle)
    assert contracts["append_report"]["record_fields"] == sorted(REPORT_RECORD_KEYS)
    assert "actual acting person" in contracts["append_report"]["effect"]
    assert "public hold at initialization" in contracts["independent_decision"]["initial_state"]
    assert "compiled declaration alone does not authorize" in contracts["independent_decision"]["review_boundary"]


def test_builtin_semantics_do_not_override_a_rejected_privacy_verdict():
    from scripts.review_rules import builtin_semantics
    bundle, _ = _world()
    value = _approved()
    value["actor_input_review"]["actors"][1]["authorized"] = False
    value["builtin_semantics"] = builtin_semantics(bundle)
    with pytest.raises(ActorInputPrivacyError):
        require_actor_input_review(value, ["ari", "bo"])
