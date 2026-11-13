"""Report exposure is a recorded event, independent of truth, stance and assent."""
import json
from copy import deepcopy

import pytest
from pydantic import ValidationError

from test_independent_rule_authority import world_and_rule
from scenario_spec import ScenarioSpecV1
from compile_spec import compile_spec
from scripts.actor_information import actor_context, actor_observation
from scripts.run_authored_world import build_engine
from world_substrate.action_authoring import CausalModel


@pytest.mark.req("native-coordination/independent-generated-concern-procedure")
def test_new_actor_report_records_exposure_without_persuasion_or_physical_effect():
    bundle, causal, _ = world_and_rule()
    engine, _, _ = build_engine(bundle, causal)
    before = deepcopy(engine.world.material_dict())
    action = {"actor": "validator", "controller": "test", "kind": "send-report", "recipient": "decider",
              "content": "The equipment is passing. This is my claim.", "base_revision": engine.world.revision}
    result = engine.submit(action)
    assert result["status"] == "accepted"
    seen = actor_observation(engine, bundle, "decider")["entities"]
    entries = seen["decider"]["components"]["report_log"]["entries"]
    record = json.loads(entries[0])
    assert record["source_id"] == "validator" and record["recipient_id"] == "decider"
    assert record["delivery_status"] == "delivered"
    assert record["lineage_status"] == "not_declared"
    assert record["source_lineage"] is None
    assert "my claim" in actor_context(engine, bundle, "decider")["actor_state"]
    assert "my claim" not in actor_context(engine, bundle, "validator")["visible"]
    after = engine.world.material_dict()
    for eid in ["condition-activation", "activation", "position-decider"]:
        assert after["entities"][eid]["components"] == before["entities"][eid]["components"]


def received_spec():
    from test_scenario_spec import _minimal
    raw = _minimal(public_summary="Participants discuss a proposal.")
    raw["information_items"][0].update(holder_id="country_b", source_id="legal_group", initially_delivered=True)
    return raw


@pytest.mark.req("information-delivery/complete-actor-input-boundary")
def test_initial_exposure_names_source_separately_from_holder_and_changes_no_beliefs():
    spec = ScenarioSpecV1.model_validate(received_spec())
    bundle, causal, _ = compile_spec(spec)
    engine, _, _ = build_engine(bundle, causal)
    seen = actor_observation(engine, bundle, "country-b")["entities"]
    report = seen["info-clause-conflict-to-country-b"]["components"]["information"]
    assert report["source_id"] == "legal-group"
    assert report["active"] is True
    assert seen["delivery-info-clause-conflict-to-country-b"]["components"]["delivery"]["status"] == "delivered"
    assert seen["country-b"]["components"] == {"member": {"role": "Member"}}
    assert bundle["actor_information"]["actors"]["country-b"]["initial_knowledge"] == []


@pytest.mark.req("information-delivery/complete-actor-input-boundary")
def test_initial_exposure_does_not_invent_a_sender():
    raw = received_spec()
    del raw["information_items"][0]["source_id"]
    bundle, causal, _ = compile_spec(ScenarioSpecV1.model_validate(raw))
    engine, _, _ = build_engine(bundle, causal)
    report = actor_observation(engine, bundle, "country-b")["entities"]["info-clause-conflict-to-country-b"]
    assert report["components"]["information"]["source_id"] == "unspecified-source-clause-conflict"


def test_absent_generated_mapping_does_not_claim_compiled_behavior_is_missing():
    from spec_pipeline import behavior_coverage
    from test_initial_actor_knowledge import _world
    from types import SimpleNamespace
    _, causal = _world()
    spec = SimpleNamespace(independent_decision=object(), world_records=[], scheduled_moments=[],
                           behaviors=[SimpleNamespace(request_id="assent", subject_refs=["bo"])])
    result = behavior_coverage(spec, [], causal, {"rows": [{"request_id": "assent", "classification": "to_generate"}]})
    assert result["rows"][0]["classification"] == "unverified"
    assert result["rows"][0]["by"] is None


@pytest.mark.req("information-delivery/complete-actor-input-boundary")
def test_canonical_lineage_does_not_disclose_private_batch_inside_an_identifier():
    raw = received_spec()
    raw["information_items"][0]["source_lineage"] = "validation_batch_v17"
    def context(value):
        bundle, causal, _ = compile_spec(ScenarioSpecV1.model_validate(value))
        engine, _, _ = build_engine(bundle, causal)
        return actor_context(engine, bundle, "country-b")
    before = context(raw)
    assert "validation_batch_v17" not in json.dumps(before)
    raw["information_items"][0]["source_lineage"] = "validation_batch_v18"
    assert context(raw) == before
    raw["information_items"][0]["lineage_visible_to_actor_ids"] = ["country_b"]
    assert "validation_batch_v18" in json.dumps(context(raw))
