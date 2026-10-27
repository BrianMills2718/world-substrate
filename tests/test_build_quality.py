"""Build-quality fixes found by the 2026-10-26 airfield run (evidence/open-attempt/s2-airfield/): #253, #254, #255
and the build record's knock-on line."""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import scripts.generate_causal_model as gcm
import scripts.world_builder_service as service

REPO = Path(__file__).resolve().parents[1]
BUNDLE = json.loads((REPO / "examples/world_authoring/orchard-v0.json").read_text())
CAUSAL = json.loads((REPO / "examples/world_authoring/orchard-causal-v0.json").read_text())
CAUSAL.pop("review", None)


def _with_effect(effect: dict) -> dict:
    causal = json.loads(json.dumps(CAUSAL))
    causal["mechanics"][0]["effects"].append(effect)
    return causal


class NoOpEffectTests(unittest.TestCase):
    """#254: an effect that cannot change anything is sent back to the rules writer."""

    def test_add_zero_and_set_to_itself_are_found(self):
        zero = _with_effect({"participant": "fruit", "path": "components.fruit.stage", "op": "add",
                             "value": {"literal": 0}})
        itself = _with_effect({"participant": "fruit", "path": "components.fruit.stage", "op": "set",
                               "value": {"participant": {"name": "fruit", "path": "components.fruit.stage"}}})
        self.assertEqual(len(gcm.no_op_effects(zero)), 1)
        self.assertIn("by 0", gcm.no_op_effects(zero)[0])
        self.assertIn("to its own value", gcm.no_op_effects(itself)[0])

    def test_real_effects_are_not_flagged(self):
        self.assertEqual(gcm.no_op_effects(CAUSAL), [])
        # Setting a field from a different participant's field is a real change.
        other = _with_effect({"participant": "fruit", "path": "location.location_id", "op": "set",
                              "value": {"participant": {"name": "actor", "path": "location.location_id"}}})
        self.assertEqual(gcm.no_op_effects(other), [])
        # False is not 0.
        flag = _with_effect({"participant": "fruit", "path": "components.fruit.stage", "op": "add",
                             "value": {"literal": False}})
        self.assertEqual(gcm.no_op_effects(flag), [])

    def test_saved_worlds_have_none(self):
        # The check runs only when rules are written, so a saved world never stops loading because of it; none of
        # the saved fixtures has one anyway.
        for path in sorted((REPO / "tests/fixtures").glob("*.json")):
            world = json.loads(path.read_text())
            causal = world.get("causal_model") or (world.get("build") or {}).get("causal_model")
            if isinstance(causal, dict):
                self.assertEqual(gcm.no_op_effects(causal), [], path.name)

    def test_the_rules_writer_gets_one_repair_naming_the_effect(self):
        bad = _with_effect({"participant": "fruit", "path": "components.fruit.stage", "op": "set",
                            "value": {"participant": {"name": "fruit", "path": "components.fruit.stage"}}})
        answers = [SimpleNamespace(content=json.dumps(bad)), SimpleNamespace(content=json.dumps(CAUSAL))]
        calls = []

        def fake_call(model, messages, **kwargs):
            calls.append(messages)
            return answers[len(calls) - 1]

        # llm_client is imported inside the call; a stand-in module keeps this test free of the real client.
        fake = SimpleNamespace(call_llm=fake_call, safe_json_loads=json.loads)
        with patch.dict("sys.modules", {"llm_client": fake}):
            out, _ = gcm.generate_causal_model(BUNDLE)
        self.assertEqual(len(calls), 2)
        self.assertIn("change nothing", calls[1][-1]["content"])
        self.assertIn("orchard.action.pick", calls[1][-1]["content"])
        self.assertEqual(gcm.no_op_effects(out), [])


class AttemptRankTests(unittest.TestCase):
    """#253: on a score tie the builder keeps a test run that did not circle and offered every move."""

    def test_circling_loses_to_more_stalled_people(self):
        circling = {"circling": True, "never_offered": ["move"], "stalled_actors": ["mechanic"],
                    "idle_actors": ["mechanic"]}
        moving = {"circling": False, "never_offered": [], "stalled_actors": ["dispatcher", "sam"]}
        self.assertGreater(service._attempt_rank(2, moving), service._attempt_rank(2, circling))
        # The score still comes first.
        self.assertGreater(service._attempt_rank(3, circling), service._attempt_rank(2, moving))

    def test_never_offered_comes_before_idle_counts(self):
        offers_all = {"never_offered": [], "stalled_actors": ["a", "b"]}
        misses_one = {"never_offered": ["fly"], "stalled_actors": []}
        self.assertGreater(service._attempt_rank(2, offers_all), service._attempt_rank(2, misses_one))


class KnockOnRecordTests(unittest.TestCase):
    """The build record says which knock-on processes the rules have, or that there are none."""

    def test_sentence_names_knock_on_processes_or_their_absence(self):
        row = {"ok": True, "accepted_actions": 4, "turns": 3, "active_at_end": True}
        self.assertNotIn("knock-on", service._dry_run_sentence(row, "ongoing"))
        self.assertIn("nothing sets off a knock-on effect",
                      service._dry_run_sentence({**row, "knock_on_processes": []}, "ongoing"))
        self.assertIn("knock-on effects: glass breaks",
                      service._dry_run_sentence({**row, "knock_on_processes": ["glass-breaks"]}, "ongoing"))

    def test_only_immediately_processes_count(self):
        causal = {"processes": [{"process_id": "dries", "timing": "each_round"}, {"process_id": "regrows"},
                                {"process_id": "glass-breaks", "timing": "immediately"}]}
        self.assertEqual(service._knock_on_processes(causal), ["glass-breaks"])

    def test_prompt_asks_for_knock_on_processes(self):
        rules = " ".join(gcm._context(BUNDLE)["authority_rules"])
        self.assertIn("timing immediately", rules)
        self.assertIn("never add or subtract 0", rules)
        self.assertIn("using them is not an assumption", rules)

    def test_state_flips_read_from_effects(self):
        causal = {"mechanics": [
            {"action_kind": "tip-stack", "effects": [{"op": "set", "value": {"literal": False}}]},
            {"action_kind": "stack-chairs", "effects": [{"op": "set", "value": {"action_field": "tables"}}]},
            {"action_kind": "prepare", "effects": [{"op": "add", "value": {"literal": 1}}]},
        ]}
        self.assertEqual(service._state_flips(causal), ["tip-stack"])

    def test_knock_on_breaks_a_tie_but_does_not_outrank_score(self):
        row = {"circling": False, "never_offered": [], "idle_actors": []}
        with_k, without = {**row, "knock_on_processes": ["spill-wets"]}, {**row, "knock_on_processes": []}
        self.assertGreater(service._attempt_rank(3, with_k), service._attempt_rank(3, without))
        self.assertGreater(service._attempt_rank(3, without), service._attempt_rank(2, with_k))


class RetryWordingTests(unittest.TestCase):
    """#255: the progress line claims a stronger model only when the retry uses a different one."""

    def test_label_follows_the_configured_model(self):
        with patch.object(service, "RULES_RETRY_MODEL", "openrouter/x/same"):
            self.assertEqual(service._retry_label("openrouter/x/same"), "Rewriting the rules")
            self.assertEqual(service._retry_label("openrouter/x/cheap"), "Rewriting the rules with a stronger model")


if __name__ == "__main__":
    unittest.main()


class UnsourcedInputTests(unittest.TestCase):
    """2026-10-26 pencil build NZD33sh3iX29: inputs nobody makes and nobody holds are named to the next attempt."""

    def test_names_inputs_that_nothing_makes_or_holds(self):
        bundle = {"entities": [{"components": {"stock": {"logs": 0, "clay": 0, "slats": 0, "cash": 5}}}]}
        causal = {
            "mechanics": [
                {"action_kind": "make", "effects": [
                    {"path": "components.stock.clay", "op": "subtract"},
                    {"path": "components.stock.slats", "op": "subtract"},
                    {"path": "components.stock.cash", "op": "subtract"}]},
                {"action_kind": "deliver-clay", "effects": [
                    {"path": "components.stock.clay", "op": "subtract"},
                    {"path": "components.stock.clay", "op": "add"}]},
                {"action_kind": "saw", "effects": [
                    {"path": "components.stock.logs", "op": "subtract"},
                    {"path": "components.stock.slats", "op": "add"}]},
            ],
            "processes": [{"effects": [{"path": "components.stock.logs", "op": "add"}]}],
        }
        # clay is only moved between holders; slats are made; logs renew; cash is held.
        self.assertEqual(service._unsourced_inputs(bundle, causal), ["clay"])

    def test_saved_worlds_have_no_unsourced_inputs(self):
        for name in ("cafe1-live", "garden-luna-r3", "pencil-c4-run17", "c1r18_waltzman_world"):
            world = json.loads((Path(__file__).parent / "fixtures" / f"{name}.json").read_text())
            self.assertEqual(service._unsourced_inputs(world["bundle"], world["causal_model"]), [], name)

    def test_priced_move_hands_over_one_unit(self):
        rules = " ".join(gcm._context(BUNDLE)["authority_rules"])
        self.assertIn("hands over exactly one unit", rules)

    def test_pencil_live_world_names_its_missing_inputs(self):
        world = json.loads((Path(__file__).parent / "fixtures" / "pencil2-live.json").read_text())
        self.assertEqual(service._unsourced_inputs(world["bundle"], world["causal_model"]),
                         ["clay", "erasers", "ferrules", "paint"])


class VanishingAndUnansweredTests(unittest.TestCase):
    """2026-10-26 live builds at 809984e: pencil 4VmgkXIVWn4p packed pencils into nothing; cafe eFmPomcnsyQq let
    orders pile up because serving never lowered them."""

    @staticmethod
    def _world(name):
        return json.loads((Path(__file__).parent / "fixtures" / f"{name}.json").read_text())

    def test_vanishing_needs_two_things_used_and_nothing_made(self):
        causal = {"mechanics": [
            {"action_kind": "pack", "effects": [{"path": "a.x", "op": "subtract"}, {"path": "a.y", "op": "subtract"}]},
            {"action_kind": "drink", "effects": [{"path": "a.coffee", "op": "subtract"}]},
            {"action_kind": "make", "effects": [{"path": "a.x", "op": "subtract"}, {"path": "a.y", "op": "subtract"},
                                                {"path": "a.z", "op": "add"}]},
        ]}
        self.assertEqual(service._vanishing_moves(causal), ["pack"])

    def test_unanswered_demand_only_counts_each_round_growth_nothing_lowers(self):
        causal = {
            "mechanics": [{"action_kind": "serve", "effects": [{"path": "components.p.served", "op": "subtract"}]}],
            "processes": [
                {"timing": "each_round", "effects": [{"path": "components.p.orders", "op": "add"},
                                                      {"path": "components.p.served", "op": "add"}]},
                {"timing": "immediately", "effects": [{"path": "components.p.mess", "op": "add"}]},
            ],
        }
        self.assertEqual(service._unanswered_demand(causal), ["orders"])

    def test_live_worlds_name_what_broke_them(self):
        self.assertEqual(service._vanishing_moves(self._world("pencil3-live")["causal_model"]), ["pack-pencils"])
        self.assertEqual(service._unanswered_demand(self._world("cafe2-live")["causal_model"]), ["orders_waiting"])

    def test_saved_worlds_are_not_named(self):
        for name in ("airfield-s1-live", "c1r18_waltzman_world", "cafe1-live", "firefighting-luna-r1",
                     "garden-luna-r3", "pencil-c4-run17", "pencil2-live"):
            world = self._world(name)
            causal = world.get("causal_model") or world.get("causal") or {}
            self.assertEqual(service._vanishing_moves(causal), [], name)
            self.assertEqual(service._unanswered_demand(causal), [], name)

    def test_world_writer_asks_for_made_and_counted_fields(self):
        import scripts.generate_world_bundle as gwb
        text = " ".join(gwb.SIZE_RULES) if isinstance(gwb.SIZE_RULES, (list, tuple)) else str(gwb.SIZE_RULES)
        self.assertIn("packed_pencils", text)
        self.assertIn("so the move can lower it", text)
        self.assertIn("declare a buy move the receiver starts", text)

    def test_live_cafe_knock_over_breaks_a_fragile_thing_at_once(self):
        # A free local replay of the live cafe world: knocking a fragile thing over sets off fallen-fragile-breaks
        # in the same moment (Decision 009). No person in the live run chose to knock anything over.
        from scripts.run_authored_world import build_engine
        world = self._world("cafe2-live")
        engine, _, _ = build_engine(world["bundle"], world["causal_model"])
        actors = [e["id"] for e in world["bundle"]["entities"] if "actor" in (e.get("categories") or [])]
        fragile = {e["id"] for e in world["bundle"]["entities"] if "fragile" in (e.get("categories") or [])}
        for actor in actors:
            offered = [o for o in engine.discover(actor, kind="knock-over")["available"]
                       if o["action"].get("object") in fragile]
            if offered:
                result = engine.submit(dict(offered[0]["action"], controller="test"))
                break
        else:
            self.fail("no actor was offered knock-over on a fragile thing")
        self.assertEqual(result["status"], "accepted")
        self.assertIn("fallen-fragile-breaks", [e["rule_id"] for e in result["reactions"]])


class MissingComponentTests(unittest.TestCase):
    """2026-10-27 pencil build iMrL2U84cLCS: shipping needed a `shipment` component no entity had."""

    def test_live_pencil_names_the_part_nobody_has(self):
        world = json.loads((Path(__file__).parent / "fixtures" / "pencil4-live.json").read_text())
        self.assertEqual(service._missing_components(world["bundle"], world["causal_model"]),
                         ["ship-pencil-boxes needs shipment"])

    def test_saved_worlds_are_not_named(self):
        for name in ("airfield-s1-live", "c1r18_waltzman_world", "cafe1-live", "cafe2-live", "firefighting-luna-r1",
                     "garden-luna-r3", "pencil-c4-run17", "pencil2-live", "pencil3-live"):
            world = json.loads((Path(__file__).parent / "fixtures" / f"{name}.json").read_text())
            self.assertEqual(service._missing_components(world["bundle"], world["causal_model"]), [], name)

    def test_a_move_nobody_can_take_part_in_loses_the_tie(self):
        everyone_acts = {"never_offered": ["a", "b"], "idle_actors": []}
        truck_never_ships = {"never_offered": ["ship"], "idle_actors": ["truck"],
                             "missing_components": ["ship needs shipment"]}
        self.assertGreater(service._attempt_rank(2, everyone_acts), service._attempt_rank(2, truck_never_ships))


class DeadEndStockTests(unittest.TestCase):
    """2026-10-27 pencil iMrL2U84cLCS: the supplier's goods piled up and nothing carried them to the factory."""

    @staticmethod
    def _world(name):
        return json.loads((Path(__file__).parent / "fixtures" / f"{name}.json").read_text())

    def test_live_pencil_names_what_piles_up_at_the_supplier(self):
        world = self._world("pencil4-live")
        self.assertEqual(service._dead_end_stock(world["bundle"], world["causal_model"]), [
            f"{good} piles up at materials-supplier (supply-materials)"
            for good in ("boxes", "clay", "erasers", "ferrules", "paint")])

    def test_pencils_nobody_carries_from_the_factory(self):
        world = self._world("pencil2-live")
        self.assertEqual(service._dead_end_stock(world["bundle"], world["causal_model"]),
                         ["pencils piles up at pencil-factory (assemble-pencils)"])

    def test_tallies_hand_overs_and_bought_goods_are_not_named(self):
        # flights flown, times a concern was raised, pencils a customer bought
        for name in ("airfield-s1-live", "c1r18_waltzman_world", "cafe1-live", "cafe2-live", "firefighting-luna-r1",
                     "garden-luna-r3", "pencil-c4-run17", "pencil3-live"):
            world = self._world(name)
            self.assertEqual(service._dead_end_stock(world["bundle"], world["causal_model"]), [], name)


class NeverTogetherTests(unittest.TestCase):
    """2026-10-27 pencil czt5uoGw5t3L: buying leads and slats required the factory to be with suppliers on other
    continents, and nothing moved anyone, so the factory waited from round 6 to round 17."""

    @staticmethod
    def _world(name):
        return json.loads((Path(__file__).parent / "fixtures" / f"{name}.json").read_text())

    def test_live_pencil_names_the_buys_across_places(self):
        world = self._world("pencil7-live")
        self.assertEqual(service._never_together(world["bundle"], world["causal_model"]), [
            "buy-leads needs actor and seller in one place: pencil-factory is in pennsylvania, lead-maker in sri-lanka",
            "buy-slats needs actor and seller in one place: pencil-factory is in pennsylvania, sawmill in oregon"])

    def test_a_truck_parked_where_no_source_is(self):
        world = self._world("pencil5-live")
        self.assertEqual(service._never_together(world["bundle"], world["causal_model"]),
                         ["carry-boxes needs actor and source in one place: truck-driver is in united-states, logger in oregon"])

    def test_worlds_whose_parties_meet_are_not_named(self):
        # a place counts as where it is (cafe), things with no place match each other (firefighting), and a buy whose
        # seller is in the same place passes (pencil7's buy-logs)
        for name in ("airfield-s1-live", "c1r18_waltzman_world", "cafe1-live", "cafe2-live", "firefighting-luna-r1",
                     "garden-luna-r3", "pencil-c4-run17", "pencil2-live", "pencil3-live", "pencil4-live"):
            world = self._world(name)
            self.assertEqual(service._never_together(world["bundle"], world["causal_model"]), [], name)
