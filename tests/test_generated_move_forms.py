"""Generated moves whose fields are text are still offered to residents (#488).

The case is the saved Waltzman build s4w5 (2026-11-20): its 9 generated moves take only text fields plus at most a
decision referent, the build declared no form for any of them, and no resident was ever offered one in 31 rounds.
"""
import json
from pathlib import Path

import pytest

from scripts import actor_information as info
from scripts.people_world import offer_generated_moves
from scripts.run_authored_world import build_engine

ROOT = Path(__file__).resolve().parents[1]
GENERATED = {"raise-local-concern", "assess-technical-risk", "review-legal-requirements", "develop-logistics-plan",
             "consult-community", "reopen-settled-issue", "reconsider-issue", "make-support-conditional",
             "restore-unconditional-support"}


def saved():
    data = json.loads((ROOT / "tests/fixtures/waltzman-s4w5-build.json").read_text())
    return data["bundle"], data["causal_model"]


def offered(engine, bundle, actor):
    return {row["action"]["kind"]: row for row in info.actor_page(engine, bundle, actor)["available"]}


@pytest.mark.req("information-delivery/a-move-with-only-text-fields-is-offered-with-its-text-left-open")
def test_a_move_with_only_text_fields_is_offered_with_its_text_left_open():
    bundle, causal = saved()
    engine, _, _ = build_engine(bundle, causal)
    assert GENERATED.isdisjoint(offered(engine, bundle, "country-one"))  # the bug as built

    fixed = offer_generated_moves(bundle, causal, {"communicate"})
    info.validate_actor_information(fixed)
    engine, _, _ = build_engine(fixed, causal)
    country = offered(engine, fixed, "country-one")
    assert GENERATED <= set(country)
    assert country["reopen-settled-issue"]["open_fields"] == ["issue", "reason"]
    assert {k: v for k, v in country["make-support-conditional"]["action"].items() if k == "decision"} == {
        "decision": "activation-question"}
    assert country["make-support-conditional"]["open_fields"] == ["condition"]
    # The resident's prompt names the move by its own description and asks for the text in its own words.
    lines = [a["description"] for a in info.actor_context(engine, fixed, "technical-group")["actions"]]
    [line] = [x for x in lines if x.startswith("Raise a concern through the group's own channel")]
    assert "concern=<in your own words>" in line
    # The existing delivery forms are unchanged.
    assert [f for f in fixed["actor_information"]["public_actions"] if f["kind"] == "communicate"] == \
        bundle["actor_information"]["public_actions"]


@pytest.mark.req("information-delivery/a-move-with-only-text-fields-is-offered-with-its-text-left-open")
def test_an_open_field_must_be_a_text_field_of_the_move():
    bundle, causal = saved()
    fixed = offer_generated_moves(bundle, causal, {"communicate"})
    form = next(f for f in fixed["actor_information"]["public_actions"] if f["kind"] == "make-support-conditional")
    form["open_fields"] = ["condition", "decision"]
    form["fields"] = {}
    with pytest.raises(info.ActorInformationError, match="open_fields"):
        info.validate_actor_information(fixed)


@pytest.mark.req("information-delivery/a-move-whose-referent-no-one-can-name-gets-no-form")
def test_a_move_whose_referent_no_one_can_name_gets_no_form():
    bundle, causal = saved()
    rule = next(m for m in causal["mechanics"] if m["action_kind"] == "make-support-conditional")
    rule["participants"]["decision"]["categories"] = ["no-such-category"]
    fixed = offer_generated_moves(bundle, causal, {"communicate"})
    kinds = {f["kind"] for f in fixed["actor_information"]["public_actions"]}
    assert "make-support-conditional" not in kinds
    assert "restore-unconditional-support" in kinds
