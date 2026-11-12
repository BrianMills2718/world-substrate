"""Judge proposal/install/restore cannot replace compiled independent actor authority."""
import sys
from copy import deepcopy
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "spikes/any-scenario-2026-10")]
from scenario_spec import ScenarioSpecV1
from compile_spec import compile_spec, _mechanic, _check, _ref, _effect
from scripts import consequence_report, rulings
from scripts.run_authored_world import build_engine


def world_and_rule():
    spec = ScenarioSpecV1.model_validate({"scenario_id": "authority", "title": "Authority", "description": "Private source description",
        "public_summary": "Public activation procedure", "people": [
            {"entity_id": actor, "label": actor, "position": "participant", "disposition": "independent", "behavioral_profile": {}}
            for actor in ["validator", "decider"]],
        "behaviors": [{"request_id": "activate", "subject_refs": ["decider"], "behavior_description": "May activate",
                       "desired_effects": ["record a decision"], "fidelity_need": "exact", "causally_material": True}],
        "fidelity_assumptions": ["Declared bounded technical intervention"],
        "independent_decision": {"decision_id": "activation", "question": "Activate", "required_actor_ids": ["decider"],
            "validator_ids": ["validator"], "repairer_ids": ["validator"], "condition_initially_passing": False,
            "initial_validation": "failed"}})
    bundle, causal, _ = compile_spec(spec)
    mechanic = _mechanic("persuade", "Persuade", {"position": {"categories": ["actor-position"], "components": ["actor_position"]}},
        [_check("not assented", _ref("position", "components.actor_position.assent"), "eq", False)],
        [_effect("position", "components.actor_position.assent", "set", True)])
    rule = {"action": {"kind": "persuade", "description": "Persuade", "fields": [{"name": "position", "type": "entity_ref"}]},
            "mechanic": mechanic}
    return bundle, causal, rule


@pytest.mark.req("native-coordination/proposed-rules-cannot-replace-actor-owned-assent")
def test_proposed_rule_is_refused_for_preview_install_and_restoration():
    bundle, causal, rule = world_and_rule()
    engine, _, _ = build_engine(bundle, causal)
    before = engine.world.material_dict()
    result = consequence_report.pass_two(bundle, causal, engine, rule,
        {"actor": "validator", "kind": "persuade", "position": "position-decider"})
    assert not result["rules_check"]["ok"]
    assert result["test_run"] is None
    book = rulings.Rulebook(bundle, causal, [], rulings.CREATE)
    entry = book.new(status=rulings.HELD, round_no=1, actor="validator", attempt="persuade", event_id=None, record={"rule": rule})
    result = book.install(engine, entry, 1)
    assert not result["ok"]
    assert engine.world.material_dict() == before
    entry["status"] = rulings.INSTALLED
    with pytest.raises(consequence_report.IndependentRuleAuthorityError):
        rulings.effective(bundle, causal, [entry])


@pytest.mark.req("native-coordination/proposed-rules-cannot-replace-actor-owned-assent")
def test_raw_candidate_check_rejects_spoofed_writer_but_accepts_installed_procedure():
    bundle, causal, rule = world_and_rule()
    assert consequence_report.rules_check(bundle, causal)[0]["ok"]
    raw_bundle, raw_causal = deepcopy(bundle), deepcopy(causal)
    raw_bundle["actions"].append(rule["action"])
    raw_causal["mechanics"].append(rule["mechanic"])
    assert not consequence_report.rules_check(raw_bundle, raw_causal)[0]["ok"]
    # A trusted-looking identifier is insufficient: the declaration itself must be exactly compiler-owned.
    raw_causal["mechanics"][-1]["mechanic_id"] = "decision.action.record-assent"
    assert not consequence_report.rules_check(raw_bundle, raw_causal)[0]["ok"]
    safe = {"action": {"kind": "record-note", "description": "Record a note", "fields": [{"name": "person", "type": "entity_ref"}]},
        "mechanic": _mechanic("record-note", "Record a note", {"person": {"categories": ["member"], "components": ["member"]}},
            [_check("not aware", _ref("person", "components.member.aware"), "eq", False)],
            [_effect("person", "components.member.aware", "set", True)])}
    expanded_bundle, expanded_causal = consequence_report.with_rule(bundle, causal, safe)
    assert expanded_bundle["actions"][-1]["kind"] == "record-note"
    assert consequence_report.rules_check(expanded_bundle, expanded_causal)[0]["ok"]
