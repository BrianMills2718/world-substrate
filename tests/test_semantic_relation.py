from __future__ import annotations

from world_substrate.semantic import GIVE_BINDING, SEMANTIC_BINDINGS
from world_substrate.semantic_relation import GRAMMAR_REF, project, project_kind, schema


def _role_map(assertion):
    return {row["role_definition_id"]: row["filler"]["filler_id"] for row in assertion["bindings"]}


def test_schema_matches_consumer_owned_ws_relation_shape() -> None:
    value = schema()
    assert value["relation_schema_id"] == "ws:semantic_binding"
    assert value["owner_namespace"] == "ws"
    assert [item["local_name"] for item in value["roles"]] == [
        "sense", "participant_profile", "specialization", "causal_class",
        "causal_bearer", "mechanic", "interpretation_limit",
    ]
    assert value["roles"][-1]["max_count"] is None


def test_give_binding_projects_without_changing_runtime_serialization() -> None:
    before = GIVE_BINDING.as_dict()
    view = project(GIVE_BINDING)
    after = GIVE_BINDING.as_dict()
    assert before == after
    assert "role_definition_ids" not in after
    assert view["read_only"] is True
    assert view["grammar_ref"] == GRAMMAR_REF
    bundle = view["relation_bundle"]
    assert bundle["schema_version"] == "relation-assertion-bundle.v1"
    assertion = bundle["assertions"][0]
    roles = _role_map(assertion)
    assert roles["ws.roledef.semantic_binding.sense"] == "lc:give_transfer"
    assert roles["ws.roledef.semantic_binding.mechanic"] == "mechanism.ownership.give"


def test_participant_profile_preserves_global_and_local_role_identity() -> None:
    view = project(GIVE_BINDING)
    profile = view["reference_catalog"]["ws.profile:binding.give.v0"]
    assert profile["roles"] == GIVE_BINDING.roles
    assert profile["role_definition_ids"] == GIVE_BINDING.role_definition_ids


def test_interpretation_limits_are_preserved_in_reference_catalog() -> None:
    view = project(GIVE_BINDING)
    catalog = view["reference_catalog"]
    observed = [catalog[f"ws.interpretation_limit:binding.give.v0:{i}"]["text"] for i in range(len(GIVE_BINDING.interpretation_limits))]
    assert tuple(observed) == GIVE_BINDING.interpretation_limits


def test_all_bound_kinds_project_and_unheat_remains_unbound() -> None:
    assert set(SEMANTIC_BINDINGS) == {"give", "drink", "heat", "fill", "take", "pour"}
    for kind in SEMANTIC_BINDINGS:
        assert project_kind(kind)["source_binding_id"] == SEMANTIC_BINDINGS[kind].binding_id
    assert project_kind("unheat") is None
