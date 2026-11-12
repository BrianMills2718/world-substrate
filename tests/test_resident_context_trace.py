"""The retained actor call is the call actually sent, including failed calls."""
import sys
import types
from unittest.mock import patch
import pytest
from scripts.concordia_residents import ResidentAct

def test_resident_retains_exact_input_and_failure():
    messages = [{"role": "user", "content": "actor evidence only"}]
    client = types.SimpleNamespace(render_prompt=lambda *a, **k: messages,
        call_llm_json_schema=lambda *a, **k: (_ for _ in ()).throw(RuntimeError("backend unavailable")))
    act = ResidentAct("mara", model="test", trace_id="trace", max_budget=0)
    act.request = {"offered": [], "context": {"provenance": [{"source": "report-1"}]}}
    with patch.dict(sys.modules, {"llm_client": client}):
        with pytest.raises(RuntimeError, match="backend unavailable"):
            act.get_action_attempt({"memory": "received report"}, None)
    assert act.calls[0]["messages"] == messages
    assert act.calls[0]["actor"] == "mara"
    assert act.calls[0]["memory"] == "received report"
    assert act.calls[0]["error"] == "RuntimeError"
    assert act.calls[0]["context"]["provenance"] == [{"source": "report-1"}]

@pytest.mark.parametrize("policy", ["llm", "resident"])
def test_runner_uses_declaration_instead_of_omniscient_context(policy):
    import json
    from pathlib import Path
    from scripts.run_authored_world import run_world, build_engine, actor_ids
    root = Path(__file__).resolve().parents[1]
    bundle = json.loads((root / "examples/world_authoring/orchard-v0.json").read_text())
    causal = json.loads((root / "examples/world_authoring/orchard-causal-v0.json").read_text())
    engine, model, _ = build_engine(bundle, causal)
    actors = actor_ids(engine, model)
    bundle["world"]["summary"] = "HIDDEN analyst hypothesis"
    bundle["actor_information"] = {
        "version": 1, "public_summary": "Public orchard", "public_entities": [
            {"id": row["id"], "label": "Known identity", "fields": []} for row in bundle["entities"]],
        "actors": {a: {"brief": "Own role", "initial_knowledge": [], "observable_fields": []} for a in actors},
        "public_actions": [{"kind": bundle["actions"][0]["kind"], "description": "Known attempt",
                            "fields": {f["name"]: actors[0] if f["type"] == "entity_ref" else 1 if f["type"] in {"integer", "number"} else False if f["type"] == "boolean" else "value" for f in bundle["actions"][0]["fields"]}}]}
    captured = []
    def render(*a, **kw):
        captured.append(kw)
        return [{"role": "user", "content": json.dumps(kw)}]
    def call(*a, **kw):
        return {"action_id": "wait", "belief": "uncertain", "expected_effect": "none", "work": "none", "reasoning": "wait"}, types.SimpleNamespace(cost=0)
    client = types.SimpleNamespace(render_prompt=render, call_llm_json_schema=call)
    with patch.dict(sys.modules, {"llm_client": client}):
        trace, _, _ = run_world(bundle, causal, policy=policy, max_turns=1,
                               briefs={a: "HIDDEN raw brief" for a in actors},
                               prior_recent=[{"actor": actors[0], "action": "HIDDEN global event"}])
    assert captured
    assert "HIDDEN" not in json.dumps(captured)
    assert trace["actor_information_mode"] == "declared-v1"
    assert any(trace["actor_inputs"].values())


def test_interpreter_does_not_autofill_hidden_singleton_or_derived_argument():
    from scripts.run_authored_world import _read_attempt
    boundary = {"actor_information": {"public_actions": [{"kind": "unlock", "description": "Try unlocking"}]}}
    engine = types.SimpleNamespace(actor_information_bundle=boundary)
    signatures = [{"kind": "unlock", "description": "HIDDEN canonical label", "fields": [
        {"name": "key", "type": "entity_ref", "only": "secret-key", "from": {"path": "secret.value"}}]}]
    def interpret(text, **kwargs):
        field = kwargs["signatures"][0]["fields"][0]
        assert "only" not in field and "from" not in field
        assert kwargs["entities"] == {"mara": "Mara"}
        assert "HIDDEN" not in str(kwargs["signatures"])
        return {"kind": "unlock", "fields": {}, "unmatched": True}, 0
    with patch.dict(sys.modules, {"llm_client": types.SimpleNamespace()}), \
         patch("scripts.run_authored_world.actor_info.actor_observation", return_value={"entities": {"mara": {"label": "Mara"}}}), \
         patch("scripts.run_authored_world.open_attempt.interpret", side_effect=interpret):
        reading, _ = _read_attempt(engine, "mara", "I try unlocking", signatures,
                                  model="test", trace_id="t", max_budget=0)
    assert reading["fields"] == {}
