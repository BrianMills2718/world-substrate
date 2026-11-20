"""Declared-laws plan S1: a world bundle may state its own resources and laws (docs/plans/declared_laws.md)."""
from __future__ import annotations

import json
import unittest

import pytest
from copy import deepcopy
from pathlib import Path

from scripts.generate_causal_model import _context
from scripts.scaffold_world import BundleError, pairing_starter_problems, validate_bundle

REPO = Path(__file__).resolve().parents[1]
ORCHARD = json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text())

SHOP = {
    "schema_version": "world-substrate-authoring-bundle/v0",
    "world": {"id": "pencil-shop", "label": "Pencil shop", "summary": "A shop sells pencils.", "location": "street", "content_version": 1},
    "components": [{"name": "holdings", "fields": [{"name": "money", "type": "integer", "default": 0}, {"name": "pencils", "type": "integer", "default": 0}]}],
    "entities": [
        {"id": "shop", "label": "Shop", "categories": ["shop"], "components": {"holdings": {"money": 0, "pencils": 5}}},
        {"id": "ana", "label": "Ana", "categories": ["customer"], "components": {"holdings": {"money": 10, "pencils": 0}}},
    ],
    "actions": [
        {"kind": "sell-pencil", "description": "Sell one pencil to a customer.", "fields": [{"name": "customer", "type": "entity_ref"}]},
        {"kind": "make-pencil", "description": "Make one pencil.", "fields": []},
    ],
    "presentation": {"assets": {}, "category_assets": {}, "station_roles": {}},
    "resources": [
        {"resource_id": "money", "says": "Coins people hold.", "kept_in": [{"component": "holdings", "field": "money"}]},
        {"resource_id": "pencils", "says": "Pencils in stock.", "kept_in": [{"component": "holdings", "field": "pencils"}]},
    ],
    "laws": [
        {"law_id": "money-is-kept", "says": "Money is never made or lost, only handed over.", "resource": "money", "may_change_by": []},
        {"law_id": "pencils-are-made", "says": "Pencils appear only when someone makes one.", "resource": "pencils", "may_change_by": ["make-pencil", "process:wear-out"]},
        {"law_id": "a-sale-is-paid", "says": "A sale hands a pencil to the customer for money.", "move": "sell-pencil",
         "gives": {"resource": "pencils", "from": "actor", "to": "customer"}, "pays": {"resource": "money", "from": "customer", "to": "actor"}},
    ],
}


def broken(path: list, value) -> dict:
    bundle = deepcopy(SHOP)
    target = bundle
    for key in path[:-1]:
        target = target[key]
    target[path[-1]] = value
    return bundle


class DeclaredLawsTests(unittest.TestCase):
    @pytest.mark.req("world-authoring-bundle/a-world-declares-resources-and-laws")
    def test_a_world_with_laws_validates_and_keeps_them(self):
        bundle = validate_bundle(SHOP)
        self.assertEqual(bundle["laws"], SHOP["laws"])
        self.assertEqual(bundle["resources"], SHOP["resources"])

    @pytest.mark.req("world-authoring-bundle/a-world-declares-resources-and-laws")
    def test_a_world_without_laws_is_unchanged(self):
        # L7: bundles from before S1 load exactly as they did.
        self.assertEqual(validate_bundle(ORCHARD), ORCHARD)
        self.assertNotIn("laws", validate_bundle(ORCHARD))

    @pytest.mark.req("world-authoring-bundle/a-world-declares-resources-and-laws")
    def test_bad_laws_are_refused_with_the_reason(self):
        cases = {
            "must be a numeric field": broken(["resources", 0, "kept_in"], [{"component": "holdings", "field": "nope"}]),
            "unknown component": broken(["resources", 0, "kept_in"], [{"component": "purse", "field": "money"}]),
            "names unknown resource": broken(["laws", 0, "resource"], "gold"),
            "unknown move 'buy'": broken(["laws", 1, "may_change_by"], ["buy"]),
            "unknown move 'teleport'": broken(["laws", 2, "move"], "teleport"),
            "gives.to must be one of": broken(["laws", 2, "gives", "to"], "shopkeeper"),
            "whoever gives must be paid": broken(["laws", 2, "pays"], {"resource": "money", "from": "actor", "to": "customer"}),
            "duplicate law": broken(["laws", 1, "law_id"], "money-is-kept"),
            "says must be nonempty": broken(["laws", 0, "says"], " "),
        }
        for reason, bundle in cases.items():
            with self.subTest(reason=reason), self.assertRaisesRegex(BundleError, reason):
                validate_bundle(bundle)

    def test_the_rules_writer_is_given_the_laws_and_told_to_keep_them(self):
        context = _context(validate_bundle(SHOP))
        self.assertEqual(context["laws"], SHOP["laws"])
        self.assertEqual(context["resources"], SHOP["resources"])
        self.assertTrue(any("keep the world's laws" in rule for rule in context["authority_rules"]))
        self.assertEqual(_context(validate_bundle(ORCHARD))["laws"], [])

    @pytest.mark.req("world-authoring-bundle/a-seller-started-sale-is-refused")
    def test_a_seller_started_sale_is_named_by_the_starter_check(self):
        problems = pairing_starter_problems(validate_bundle(SHOP))
        self.assertEqual(len(problems), 1)
        self.assertIn("a-sale-is-paid", problems[0])

    @pytest.mark.req("world-authoring-bundle/a-buyer-started-purchase-is-accepted")
    def test_a_buyer_started_purchase_passes_the_starter_check(self):
        bundle = deepcopy(SHOP)
        bundle["actions"][0] = {"kind": "sell-pencil", "description": "Buy one pencil from the shop.", "fields": [{"name": "seller", "type": "entity_ref"}]}
        bundle["laws"][2] = {"law_id": "a-sale-is-paid", "says": "A purchase hands a pencil over for money.", "move": "sell-pencil",
                             "gives": {"resource": "pencils", "from": "seller", "to": "actor"}, "pays": {"resource": "money", "from": "actor", "to": "seller"}}
        self.assertEqual(pairing_starter_problems(validate_bundle(bundle)), [])

    @pytest.mark.req("world-authoring-bundle/saved-worlds-still-load")
    def test_saved_worlds_still_load(self):
        saved = json.loads((REPO / "tests/fixtures/pencil-s3-kept.json").read_text())
        validate_bundle(saved["bundle"])

    @pytest.mark.req("world-authoring-bundle/a-seller-started-sale-is-refused")
    def test_the_designer_is_asked_again_when_the_seller_starts_a_sale(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        import scripts.generate_world_bundle as gwb
        fixed = deepcopy(SHOP)
        fixed["actions"][0] = {"kind": "sell-pencil", "description": "Buy one pencil from the shop.", "fields": [{"name": "seller", "type": "entity_ref"}]}
        fixed["laws"][2] = {"law_id": "a-sale-is-paid", "says": "A purchase hands a pencil over for money.", "move": "sell-pencil",
                            "gives": {"resource": "pencils", "from": "seller", "to": "actor"}, "pays": {"resource": "money", "from": "actor", "to": "seller"}}
        answers = [SimpleNamespace(content=json.dumps(SHOP)), SimpleNamespace(content=json.dumps(fixed))]
        calls = []

        def fake_call(model, messages, **kwargs):
            calls.append(messages)
            return answers[len(calls) - 1]

        fake = SimpleNamespace(call_llm=fake_call, safe_json_loads=json.loads)
        with patch.dict("sys.modules", {"llm_client": fake}), patch.object(gwb, "is_recorded_authoring_replay", return_value=True):
            bundle, _, _ = gwb.generate_world_bundle("a pencil shop", world_kind="ongoing")
        self.assertEqual(len(calls), 2)
        self.assertIn("a-sale-is-paid", calls[1][-1]["content"])
        self.assertEqual(bundle["laws"][2]["pays"]["from"], "actor")

    @pytest.mark.req("causal-model-authoring/the-rules-writer-is-told-who-acts-in-a-trade")
    def test_the_rules_writer_is_told_the_payer_is_the_actor(self):
        rules = _context(validate_bundle(SHOP))["authority_rules"]
        self.assertTrue(any("actor selector" in r and "pays" in r for r in rules))

    def test_the_designer_is_asked_for_laws(self):
        from scripts.generate_world_bundle import _messages
        contract = json.loads(_messages("a pencil shop", "ongoing")[1]["content"])["contract"]
        self.assertIn("laws", contract)
        self.assertIn("resources", contract)

    def test_the_build_record_names_the_laws(self):
        from scripts.world_builder_service import _result_summary
        summary = _result_summary("/generate-world", 200, {"ok": True, "bundle": SHOP, "review": {}})
        self.assertEqual(summary["laws"], ["money-is-kept", "pencils-are-made", "a-sale-is-paid"])
        self.assertEqual(summary["bundle"]["laws"], SHOP["laws"])


if __name__ == "__main__":
    unittest.main()
