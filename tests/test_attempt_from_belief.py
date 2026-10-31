"""Attempts from belief (#128): tasks that take several rounds, followed from start to ending. No AI calls.

The truck world (spikes/any-scenario-2026-10/evidence/truck) is Decision 007's example: driving starts on an
empty tank and the world stops it. The saved Waltzman world (tests/fixtures/c1r18_waltzman_world.json) has
remedies that take two rounds.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

REPO = Path(__file__).resolve().parents[1]
TRUCK = REPO / "spikes/any-scenario-2026-10/evidence/truck"
WALTZMAN = Path(__file__).resolve().parent / "fixtures/c1r18_waltzman_world.json"
PENCIL = Path(__file__).resolve().parent / "fixtures/pencil-c4-run17.json"
sys.path[:0] = [str(REPO / "spikes/any-scenario-2026-10")]

from scripts import attempts, check_trace_reads  # noqa: E402
from scripts.run_authored_world import run_world  # noqa: E402
from spec_pipeline import merge_causal  # noqa: E402


def _truck(fuel: float | None = None) -> tuple[dict, dict]:
    bundle = json.loads((TRUCK / "bundle.json").read_text())
    if fuel is not None:
        next(e for e in bundle["entities"] if e["id"] == "delivery-vehicle")["components"]["vehicle"]["fuel"] = fuel
    return bundle, json.loads((TRUCK / "causal.json").read_text())


def _tasks(trace: dict) -> list[dict]:
    return [u for t in trace["transcript"] for u in t["underway"]]


class TruckTests(unittest.TestCase):
    def test_driving_on_an_empty_tank_starts_and_the_world_stops_it(self):
        trace, _, _ = run_world(*_truck(fuel=0), policy="scripted", max_turns=3)
        drive = next(u for u in _tasks(trace) if u["action"] == "drive")
        self.assertEqual((drive["status"], drive["ended_by"], drive["ended_with"]),
                         ("failed", "stop-delivery-vehicle-without-fuel", "stopped"))
        self.assertNotEqual(drive["started_event_id"], drive["ending_event_id"])

    def test_driving_with_fuel_finishes_a_leg(self):
        trace, _, _ = run_world(*_truck(), policy="scripted", max_turns=2)
        drive = next(u for u in _tasks(trace) if u["action"] == "drive")
        self.assertEqual((drive["status"], drive["ended_by"]), ("finished", "advance-driving-delivery-vehicle"))

    def test_driving_can_end_two_ways(self):
        self.assertEqual([(t["action"], t["can_fail_part_way"]) for t in attempts.long_tasks(_truck()[1])],
                         [("drive", True)])


class WaltzmanTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world = json.loads(WALTZMAN.read_text())

    def test_a_remedy_is_followed_across_one_round_requests(self):
        """Live play asks for one round at a time; the open task goes back with the next request."""
        bundle, causal = self.world["bundle"], self.world["causal_model"]
        trace, _, _ = run_world(bundle, causal, policy="scripted", max_turns=1)
        seen: dict[str, dict] = {}
        for _ in range(8):
            for task in _tasks(trace):
                seen[task["started_event_id"]] = task
            trace, _, _ = run_world(bundle, causal, policy="scripted", max_turns=1,
                                    start_snapshot=trace["final_snapshot"], turn_offset=trace["summary"]["last_turn"],
                                    underway=trace["underway"])
        finished = [t for t in seen.values() if t["status"] == "finished"]
        self.assertTrue(finished, "a remedy must finish within nine rounds")
        task = finished[0]
        self.assertEqual(task["ended_by"], "remedy-completes")
        self.assertGreater(int(task["ending_event_id"].split("-")[0][1:]), task["started_round"])

    def test_remedies_cannot_fail_part_way_in_this_saved_world(self):
        """Why the slice lets the rules writer add a stop: only a compiled countdown ever ends a remedy here."""
        rows = [r for r in attempts.long_tasks(self.world["causal_model"], self.world["bundle"])
                if r["started_by"] == "person"]
        self.assertEqual({r["action"] for r in rows}, {"resolve-concern", "resolve-own-concern"})
        self.assertFalse(any(r["can_fail_part_way"] for r in rows))

    def test_a_generated_process_may_stop_a_remedy_part_way_and_nothing_else(self):
        stop = {"process_id": "remedy-stalls-without-power", "rationale": "test",
                "selector": {"categories": ["information"], "components": ["concern"]},
                "checks": [{"label": "a remedy is under way", "op": "eq", "right": {"literal": "remedy_under_way"},
                            "left": {"participant": {"name": "it", "path": "components.concern.status"}}}],
                "effects": [{"op": "set", "participant": "it", "path": "components.concern.status",
                             "value": {"literal": "open"}},
                            {"op": "set", "participant": "it", "path": "components.concern.remedy_ticks_left",
                             "value": {"literal": 0}}]}
        resolves = deepcopy(stop)
        resolves["process_id"] = "remedy-resolves-early"
        resolves["effects"][0]["value"] = {"literal": "resolved"}
        compiled = {k: self.world["causal_model"][k] for k in ("schema_version", "mechanics", "processes")}
        merged, dropped = merge_causal(compiled, {"processes": [stop, resolves]})
        kept = {p["process_id"] for p in merged["processes"]}
        self.assertIn("remedy-stalls-without-power", kept)
        self.assertNotIn("remedy-resolves-early", kept)
        self.assertTrue(any("remedy-resolves-early" in d for d in dropped))
        self.assertTrue(all(r["can_fail_part_way"] for r in attempts.long_tasks(merged)))

    def test_the_person_remembers_starting_and_later_sees_their_expectation_beside_the_field(self):
        import scripts.concordia_residents as concordia

        def choose(residents, actor, offered, context):
            pick = next((a["action_id"] for a in context["actions"] if "resolve" in a["description"]), offered[0] if offered else None)
            return {"belief": f"{actor} believes the fix will hold.", "action_id": pick or "wait",
                    "expected_effect": "The concern is resolved.", "reasoning": "test"}

        bundle, causal = self.world["bundle"], self.world["causal_model"]
        briefs = {a: f"You are {a}." for a in ("country-one", "country-two", "country-three", "country-four")}
        with patch.object(concordia.Residents, "choose", choose):
            trace, _, _ = run_world(bundle, causal, policy="resident", max_turns=6, briefs=briefs)
        notes = [n for items in trace["resident_memory"].values() for n in items]
        self.assertTrue(any("you started it; it is now under way" in n for n in notes), notes[:6])
        self.assertTrue(any("You expected: The concern is resolved. What you see now:" in n for n in notes))
        started = [u for u in _tasks(trace) if u["expects"] == "The concern is resolved."]
        self.assertTrue(started)

    def test_each_person_is_told_the_round_not_the_worlds_tick(self):
        """An authored world has no clock process, so its tick stays 0; live play asks one round at a time, and on
        round 11 the pencil shop read "Turn 0" beside memory saying "Round 10" (2026-10-30 s3p4, call 22648)."""
        import scripts.concordia_residents as concordia

        told: list[int] = []

        def choose(residents, actor, offered, context):
            told.append(context["tick"])
            return {"belief": "b", "action_id": "wait", "expected_effect": "e", "reasoning": "test"}

        bundle, causal = self.world["bundle"], self.world["causal_model"]
        with patch.object(concordia.Residents, "choose", choose):
            first, _, _ = run_world(bundle, causal, policy="resident", max_turns=2)
            self.assertEqual(sorted(set(told)), [1, 2])
            told.clear()
            run_world(bundle, causal, policy="resident", max_turns=1, start_snapshot=first["final_snapshot"],
                      turn_offset=first["summary"]["last_turn"], underway=first["underway"])
        self.assertEqual(set(told), {3})


class BuildCheckTests(unittest.TestCase):
    def test_a_fuel_gate_on_driving_is_flagged(self):
        bundle, causal = _truck()
        self.assertEqual(attempts.attempt_findings(bundle, causal), [])
        drive = next(m for m in causal["mechanics"] if m["action_kind"] == "drive")
        drive["checks"].append({"label": "the vehicle has fuel", "op": "gt", "right": {"literal": 0},
                                "left": {"participant": {"name": "vehicle", "path": "components.vehicle.fuel"}}})
        self.assertEqual([f["rule"] for f in attempts.attempt_findings(bundle, causal)], [drive["mechanic_id"]])

    def test_possession_checks_on_one_step_transfers_are_rules_of_the_game(self):
        """The spike's version flagged all 7 transfers in this saved pencil world (loading a log needs a log)."""
        world = json.loads(PENCIL.read_text())
        self.assertEqual(attempts.attempt_findings(world["bundle"], world["causal_model"]), [])


class CarriedTests(unittest.TestCase):
    TASK = {"person": "p", "action": "fix", "entity": "c", "field": "components.concern.status",
            "value": "remedy_under_way", "before": "open", "started_round": 3, "started_event_id": "r3-e00001",
            "expects": None}

    def test_kept_only_while_the_world_still_shows_it(self):
        under = {"c": {"components": {"concern": {"status": "remedy_under_way"}}}}
        done = {"c": {"components": {"concern": {"status": "resolved"}}}}
        self.assertEqual(attempts.carried([self.TASK], under), [self.TASK])
        self.assertEqual(attempts.carried([self.TASK], done), [])

    def test_bad_shapes_are_refused(self):
        with self.assertRaises(ValueError):
            attempts.carried([{**self.TASK, "extra": 1}], {})
        with self.assertRaises(ValueError):
            attempts.carried([self.TASK] * 25, {})


class TraceReadTests(unittest.TestCase):
    def test_a_read_through_must_name_each_tasks_start_and_end(self):
        task = {"person": "country-one", "action": "resolve-own-concern", "started_round": 1,
                "started_event_id": "r1-e00002", "status": "underway"}
        rows = [{"trace_id": "t1", "result": {"transcript": [
            {"turn": 1, "actors": {"country-one": {"status": "accepted", "event_id": "r1-e00002"}},
             "underway": [task]},
            {"turn": 2, "actors": {"country-one": {"status": "no_action"}},
             "underway": [{**task, "status": "finished", "ending_event_id": "r2-e00005"}]}]}}]
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp)
            (folder / "run-log.jsonl").write_text("\n".join(json.dumps(r) for r in rows) + "\n")
            read = "# Trace read\n\nt1\n\n## Findings\n\nok\n\n## Round 1\n\ncountry-one r1-e00002\n\n## Round 2\n\n{}\n"
            (folder / "TRACE_READ.md").write_text(read.format("nothing"))
            self.assertTrue(any("r2-e00005" in p for p in check_trace_reads.check_run(folder)))
            (folder / "TRACE_READ.md").write_text(read.format("remedy finished at r2-e00005"))
            self.assertEqual(check_trace_reads.check_run(folder), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
