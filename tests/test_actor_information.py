"""Declared input checks, using no model calls."""
from dataclasses import dataclass
from types import SimpleNamespace

import pytest

from scripts.actor_information import ActorInformationError, actor_context, actor_page, validate_actor_information
from scripts.scaffold_world import validate_bundle
from world_substrate.model import Entity
from world_substrate.information import DeliveryState, InformationState


@dataclass
class Details:
    visible: str = "known"
    secret: str = "private validation"


def fixture():
    bundle = {
        "schema_version": "world-substrate-authoring-bundle/v0",
        "world": {"id": "boundary", "label": "Boundary", "summary": "PRIVILEGED", "location": "lab"},
        "components": [{"name": "details", "fields": [{"name": n, "type": "string", "default": "unspecified"} for n in ("visible", "secret")]}],
        "entities": [{"id": n, "label": "PRIVILEGED", "categories": ["person"], "components": {"details": {"visible": "known", "secret": "hidden"}}} for n in ("ari", "mara")],
        "actions": [{"kind": "inspect", "description": "PRIVILEGED", "fields": [{"name": "target", "type": "entity_ref"}]}],
        "presentation": {"assets": {}, "category_assets": {}, "station_roles": {}},
        "actor_information": {
            "version": 1, "public_summary": "A shared laboratory.",
            "public_entities": [{"id": n, "label": n.title(), "fields": []} for n in ("ari", "mara")],
            "actors": {n: {"brief": "Choose independently.", "initial_knowledge": [{"id": "k1", "text": "A claim.", "source": "profile"}], "observable_fields": [{"entity": n, "paths": ["details.visible"]}]} for n in ("ari", "mara")},
            "public_actions": [{"kind": "inspect", "description": "Request inspection.", "fields": {"target": "ari"}}],
        },
    }
    engine = SimpleNamespace(world=SimpleNamespace(revision=3, tick=0, entities={n: Entity(entity_id=n, label="PRIVILEGED", category_ids=("person",), components={"details": Details()}) for n in ("ari", "mara")}))
    return bundle, engine


@pytest.mark.req("information-delivery/hidden-state-cannot-leak-through-another-ingress")
def test_hidden_state_labels_summary_and_action_text_cannot_change_input():
    bundle, engine = fixture()
    before = actor_context(engine, bundle, "mara")
    engine.world.entities["ari"].components["details"].secret = "opposite"
    engine.world.entities["mara"].components["details"].secret = "own hidden field"
    engine.world.entities["ari"].label = "changed secret label"
    bundle["world"]["summary"] = "changed secret summary"
    bundle["actions"][0]["description"] = "changed secret description"
    assert actor_context(engine, bundle, "mara") == before
    assert "PRIVILEGED" not in str(before)
    assert "details.secret" not in str(before)
    assert "executability unknown" in before["actions"][0]["description"]


def test_observations_are_actor_specific_and_candidates_have_stable_identity():
    bundle, engine = fixture()
    first = actor_page(engine, bundle, "mara")
    assert first["observation"]["entities"]["ari"]["components"] == {}
    assert first["observation"]["entities"]["mara"]["components"] == {"details": {"visible": "known"}}
    engine.world.revision += 1
    second = actor_page(engine, bundle, "mara")
    assert first["available"][0]["action_id"] == second["available"][0]["action_id"]
    assert second["available"][0]["action"]["base_revision"] == 4
    assert second["blocked"] == []


@pytest.mark.parametrize("mutation", [
    lambda d: d.update(version=True),
    lambda d: d.update(unrecognized="bad"),
    lambda d: d["public_entities"][0].update(fields=["details.unknown"]),
    lambda d: d["public_entities"][0].update(id="unknown"),
    lambda d: d["public_entities"][0].update(id=[]),
    lambda d: d["actors"]["mara"]["observable_fields"][0].update(entity=[]),
    lambda d: d["actors"]["mara"].update(extra="bad"),
    lambda d: d["actors"]["mara"]["initial_knowledge"][0].update(source=""),
    lambda d: d["public_actions"][0]["fields"].update(target="unknown"),
])
def test_malformed_declarations_fail_closed(mutation):
    bundle, _ = fixture()
    mutation(bundle["actor_information"])
    with pytest.raises(ActorInformationError):
        validate_bundle(bundle)


def test_legacy_bundles_load_but_do_not_claim_an_authorized_projection():
    bundle, engine = fixture()
    del bundle["actor_information"]
    assert "actor_information" not in validate_bundle(bundle)
    with pytest.raises(ActorInformationError, match="legacy bundle"):
        actor_context(engine, bundle, "mara")


def test_unknown_actor_and_null_declaration_fail_closed():
    bundle, engine = fixture()
    with pytest.raises(ActorInformationError):
        actor_context(engine, bundle, "unknown")
    bundle["actor_information"] = None
    with pytest.raises(ActorInformationError):
        validate_actor_information(bundle)


def test_pending_message_and_its_action_identity_do_not_enter_recipient_input():
    bundle, engine = fixture()
    fields = [
        {"name": "content", "type": "string", "default": "unspecified"},
        {"name": "source_id", "type": "string", "default": "ari"},
        {"name": "channel_id", "type": "string", "default": "report"},
        {"name": "visibility", "type": "string", "default": "direct"},
        {"name": "topic", "type": "string", "default": "validation"},
        {"name": "derived_from_info_id", "type": "entity_ref_or_null", "default": None},
        {"name": "active", "type": "boolean", "default": False},
    ]
    bundle["components"].append({"name": "information", "fields": fields})
    info = InformationState(content="Private report", source_id="ari", channel_id="report", active=True)
    bundle["entities"].append({"id": "report", "label": "Private report", "categories": ["information"], "components": {"information": vars(info)}})
    bundle["actor_information"]["public_entities"].append({"id": "report", "label": "Report", "fields": ["information.content"]})
    bundle["actor_information"]["public_actions"][0]["fields"]["target"] = "report"
    engine.world.entities["report"] = Entity(entity_id="report", label="Private report", category_ids=("information",), components={"information": info})
    delivery = DeliveryState(info_id="report", recipient_id="mara", channel_id="report")
    engine.world.entities["delivery"] = Entity(entity_id="delivery", label="Delivery", category_ids=("delivery",), components={"delivery": delivery})
    before = actor_context(engine, bundle, "mara")
    assert "Private report" not in str(before)
    assert before["actions"] == []
    assert "Private report" in str(actor_context(engine, bundle, "ari"))
    delivery.status = "delivered"
    after = actor_context(engine, bundle, "mara")
    assert "Private report" in str(after)
    assert len(after["actions"]) == 1


def test_private_entity_identity_and_action_forms_are_recipient_scoped():
    bundle, engine = fixture()
    bundle['entities'].append({'id': 'private-note', 'label': 'PRIVILEGED', 'categories': ['record'], 'components': {'details': {'visible': 'measurement', 'secret': 'hidden'}}})
    engine.world.entities['private-note'] = Entity(entity_id='private-note', label='PRIVILEGED', category_ids=('record',), components={'details': Details()})
    bundle['actor_information']['public_entities'].append({'id': 'private-note', 'label': 'Private measurement', 'fields': ['details.visible'], 'actor_ids': ['ari']})
    bundle['actor_information']['public_actions'].append({'kind': 'inspect', 'description': 'Inspect a known record.', 'fields': {'target': 'private-note'}})
    mara = actor_context(engine, bundle, 'mara')
    assert 'private-note' not in str(mara) and 'Private measurement' not in str(mara)
    assert 'Private measurement' in str(actor_context(engine, bundle, 'ari'))
    engine.world.entities['private-note'].components['details'].visible = 'different hidden condition'
    assert actor_context(engine, bundle, 'mara') == mara
