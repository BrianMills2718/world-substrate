"""The engine keeps a world's declared laws (docs/plans/declared_laws.md, S2, check L2).

The world is the kept pencil13 build (tests/fixtures/pencil13-kept.json); the laws are written here because they
exercise the Engine contract, not the designer (the designer is checked live, evidence/declared-laws/). pencil13's
buy-boxed-pencils hands the factory's boxed pencils to a shipment and takes no money from the shop: a pairing law
for that sale names the breach.
"""
from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts.run_authored_world import build_engine  # noqa: E402
from world_substrate.engine import ScopeViolation  # noqa: E402
from world_substrate.laws import law_breaches  # noqa: E402

PENCIL13 = json.loads((REPO / "tests/fixtures/pencil13-kept.json").read_text())

RESOURCES = [
    {"resource_id": "cash", "says": "Money.", "kept_in": [{"component": "business", "field": "cash"},
                                                           {"component": "customer", "field": "cash"}]},
    {"resource_id": "boxed", "says": "Boxed pencils.", "kept_in": [{"component": "inventory", "field": "packed_pencils"}]},
    {"resource_id": "cedar", "says": "Standing cedar.", "kept_in": [{"component": "inventory", "field": "cedar"}]},
    {"resource_id": "erasers", "says": "Erasers.", "kept_in": [{"component": "inventory", "field": "erasers"}]},
]
SALE = {"law_id": "boxed-sale", "says": "A shop pays the factory for the boxed pencils it gets.",
        "move": "buy-boxed-pencils", "gives": {"resource": "boxed", "from": "seller", "to": "buyer"},
        "pays": {"resource": "cash", "from": "buyer", "to": "seller"}}
BOXED_MADE_BY_PACKING = {"law_id": "boxed-total", "says": "Boxed pencils are made only by packing.",
                         "resource": "boxed", "may_change_by": ["pack-pencils"]}
CEDAR_ONLY_CUT = {"law_id": "cedar-total", "says": "Cedar changes only by cutting.",
                  "resource": "cedar", "may_change_by": ["cut-cedar"]}
ERASERS_FIXED = {"law_id": "erasers-total", "says": "Erasers never appear from nowhere.",
                 "resource": "erasers", "may_change_by": []}
# A knock-on effect of packing that conjures an eraser: it breaks ERASERS_FIXED inside the move's moment.
ERASER_ON_PACK = {
    "process_id": "eraser-on-pack", "timing": "immediately",
    "rationale": "test: a reaction that breaks a law",
    "selector": {"categories": ["factory"], "components": ["inventory"]},
    "checks": [{"label": "boxed pencils are on hand", "op": "gt",
                "left": {"participant": {"name": "it", "path": "components.inventory.packed_pencils"}},
                "right": {"literal": 0}}],
    "effects": [{"participant": "it", "path": "components.inventory.erasers", "op": "add", "value": {"literal": 1}}],
}
SHOP_ORDER = {"actor": "country-shop", "kind": "buy-boxed-pencils", "controller": "test", "buyer": "country-shop",
              "seller": "pennsylvania-factory", "carrier": "truck-carrier", "shipment": "pencil-shipment",
              "quantity": 1, "rounds": 1}
PACK = {"actor": "pennsylvania-factory", "kind": "pack-pencils", "controller": "test", "quantity": 1}


def _engine(laws, processes=None):
    bundle = deepcopy(PENCIL13["bundle"])
    factory = next(e for e in bundle["entities"] if e["id"] == "pennsylvania-factory")
    factory["components"]["inventory"].update(pencils=5, boxes=5, packed_pencils=5)
    # Below the reserve's cap of 20, so renew-cedar-reserve is due on the first tick.
    next(e for e in bundle["entities"] if e["id"] == "oregon-loggers")["components"]["inventory"]["cedar"] = 10
    bundle["resources"], bundle["laws"] = deepcopy(RESOURCES), deepcopy(laws)
    causal = deepcopy(PENCIL13["causal_model"])
    if processes is not None:
        causal["processes"] = processes
    engine, _, _ = build_engine(bundle, causal)
    return engine


def _submit(engine, action):
    return engine.submit({**action, "base_revision": engine.world.revision})


def _failed(event):
    return [c for c in event["checks"] if not c["ok"]]


class MoveTests(unittest.TestCase):
    def test_a_sale_that_takes_no_money_is_refused_and_names_the_law(self):
        engine = _engine([SALE])
        before = engine.world.material_hash()
        result = _submit(engine, SHOP_ORDER)
        self.assertEqual(result["status"], "law_breach")
        self.assertEqual(engine.world.material_hash(), before)
        (check,) = _failed(result["event"])
        self.assertIn(SALE["says"], check["label"])
        self.assertEqual(check["required"], "boxed-sale")
        self.assertIn("pays cash from country-shop to pennsylvania-factory", check["actual"])

    def test_a_move_outside_may_change_by_is_refused(self):
        engine = _engine([BOXED_MADE_BY_PACKING])
        result = _submit(engine, SHOP_ORDER)
        self.assertEqual(result["status"], "law_breach")
        self.assertIn("buy-boxed-pencils changed the world's total boxed by -1", _failed(result["event"])[0]["actual"])

    def test_a_listed_move_commits(self):
        engine = _engine([BOXED_MADE_BY_PACKING])
        self.assertEqual(_submit(engine, PACK)["status"], "accepted")

    def test_a_knock_on_effect_that_breaks_a_law_refuses_the_whole_move(self):
        engine = _engine([ERASERS_FIXED], processes=[ERASER_ON_PACK])
        before = engine.world.material_hash()
        result = _submit(engine, PACK)
        self.assertEqual(result["status"], "law_breach")
        self.assertEqual(result["event"]["rule_id"], "pack-pencils")
        self.assertEqual(engine.world.material_hash(), before)
        (check,) = _failed(result["event"])
        self.assertIn("eraser-on-pack", check["label"])
        self.assertIn(ERASERS_FIXED["says"], check["label"])

    def test_no_laws_keeps_the_world_as_it_was(self):
        engine = _engine([])
        self.assertEqual(_submit(engine, SHOP_ORDER)["status"], "accepted")


class ProcessTests(unittest.TestCase):
    def test_a_tick_process_that_breaks_a_law_undoes_the_round(self):
        engine = _engine([CEDAR_ONLY_CUT])
        before = engine.world.material_hash()
        result = engine.advance(3)
        self.assertEqual(result["status"], "law_breach")
        (event,) = result["events"]
        self.assertEqual(event["rule_id"], "renew-cedar-reserve")
        self.assertIn(CEDAR_ONLY_CUT["says"], _failed(event)[0]["label"])
        self.assertEqual(engine.world.material_hash(), before)
        # The advance stops at the refused round: one advance command, one event.
        self.assertEqual([c["status"] for c in engine.world.commands], ["law_breach"])

    def test_a_process_listed_by_id_runs(self):
        law = {**CEDAR_ONLY_CUT, "may_change_by": ["cut-cedar", "process:renew-cedar-reserve"]}
        engine = _engine([law])
        self.assertEqual(engine.advance(1)["status"], "accepted")

    def test_a_scope_breach_by_a_process_still_raises(self):
        engine = _engine([CEDAR_ONLY_CUT])
        process = engine.registry.processes()[0]
        process.write_paths = ()
        with self.assertRaises(ScopeViolation):
            engine.advance(1)


class BuildFindingTests(unittest.TestCase):  # L3's free half: a test-run breach reaches the rules writer by name
    def test_a_scripted_test_run_reports_the_breach_and_the_advice_names_the_law(self):
        from scripts import world_builder_service as service
        from scripts.run_authored_world import run_world

        bundle = deepcopy(PENCIL13["bundle"])
        next(e for e in bundle["entities"] if e["id"] == "oregon-loggers")["components"]["inventory"]["cedar"] = 10
        bundle["resources"], bundle["laws"] = deepcopy(RESOURCES), [deepcopy(CEDAR_ONLY_CUT)]
        trace, _, _ = run_world(bundle, deepcopy(PENCIL13["causal_model"]), policy="scripted", max_turns=2)
        rows = trace["summary"]["law_breaches"]
        self.assertEqual([(r["rule_id"], r["law_id"]) for r in rows], [("renew-cedar-reserve", "cedar-total")])
        advice = service._law_breach_guidance(rows, 2)
        self.assertIn("renew-cedar-reserve broke cedar-total", advice)
        self.assertIn(CEDAR_ONLY_CUT["says"], advice)
        self.assertIn("may_change_by", advice)

    def test_the_breach_survives_the_guidance_caps_and_ranks_a_tied_attempt_lower(self):
        # Pencil COc7JzUGIXXn: the breach was appended after 4000 characters of other findings and cut off, and the
        # retry revised a tied attempt that broke no law (evidence/declared-laws/s2-pencil-2/TRACE_READ.md).
        from scripts import world_builder_service as service

        rows = [{"rule_id": "cedar-regrowth", "law_id": "cedar-total", "law": "Cedar is cut into logs.",
                 "found": "process:cedar-regrowth changed the world's total cedar by 1; only cut-cedar may change it"}]
        guidance = service._law_breaches_first(" These moves were never possible: " + "x" * 5000, rows, 24)
        self.assertIn("cedar-regrowth broke cedar-total", guidance[:3000])
        clean, broken = {"never_offered": ["a"]}, {"never_offered": [], "law_breaches": rows}
        self.assertGreater(service._attempt_rank(2, clean), service._attempt_rank(2, broken))
        self.assertGreater(service._attempt_rank(3, broken), service._attempt_rank(2, clean))


class FunctionTests(unittest.TestCase):
    def test_amounts_spread_over_two_fields_are_summed(self):
        state = lambda a, b: {"entities": {"x": {"components": {"business": {"cash": a}}},
                                           "y": {"components": {"customer": {"cash": b}}}}}
        law = {"law_id": "money", "says": "Money is kept.", "resource": "cash", "may_change_by": []}
        self.assertEqual(law_breaches([law], RESOURCES, state(10, 0), state(9, 1), "sell"), [])
        self.assertEqual(len(law_breaches([law], RESOURCES, state(10, 0), state(10, 1), "sell")), 1)


if __name__ == "__main__":
    unittest.main()
