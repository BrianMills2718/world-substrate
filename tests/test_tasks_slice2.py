"""Tasks that can really fail part-way (#128 slice 2, docs/plans/waltzman-tasks-slice2.goal.md E1-E4).

All on saved worlds with no AI calls (tests/AGENTS.md, #215). The c1r20 build (tests/fixtures/c1r20_waltzman_build.json)
holds the AI answers the live build used on 2026-10-23; tests/replay_build.py runs them through today's pipeline, so
the compiled rules under test are today's and the generated ones are exactly what the rules writer wrote. The saved
c1r18 and c1r20 worlds keep the rules they ran with, which is what the build check must catch.
"""
from __future__ import annotations

import json
import sys
import unittest
from functools import lru_cache
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src"), str(REPO / "spikes/any-scenario-2026-10"), str(REPO / "tests")]

from replay_build import replay  # noqa: E402
from scripts import attempts  # noqa: E402
from scripts.run_authored_world import WORLD, build_engine, run_world  # noqa: E402

FIXTURES = Path(__file__).resolve().parent / "fixtures"
C1R20_BUILD = FIXTURES / "c1r20_waltzman_build.json"
C1R18 = FIXTURES / "c1r18_waltzman_world.json"
PENCIL = FIXTURES / "pencil-c4-run17.json"
TRUCK = REPO / "spikes/any-scenario-2026-10/evidence/truck"
LEGAL = "info-legal-local-concern-to-country-two"


@lru_cache(maxsize=1)
def _built() -> str:
    return json.dumps(replay(C1R20_BUILD))


def built() -> dict:
    return json.loads(_built())


@lru_cache(maxsize=1)
def _replayed() -> str:
    """45 scripted rounds of the rebuilt world, as the page plays them (30, then 15 more from the snapshot)."""
    world = built()
    first, _, _ = run_world(world["bundle"], world["causal_model"], policy="scripted", max_turns=30)
    more, _, _ = run_world(world["bundle"], world["causal_model"], policy="scripted", max_turns=15,
                           start_snapshot=first["final_snapshot"], turn_offset=30, underway=first["underway"])
    return json.dumps({"first": first, "more": more})


def replayed() -> tuple[dict, dict]:
    runs = json.loads(_replayed())
    return runs["first"], runs["more"]


def _saved(path: Path) -> tuple[dict, dict]:
    world = json.loads(path.read_text())
    return world["bundle"], world["causal_model"]


def _truck() -> tuple[dict, dict]:
    return json.loads((TRUCK / "bundle.json").read_text()), json.loads((TRUCK / "causal.json").read_text())


class PartWayCheckTests(unittest.TestCase):
    """E1: the build finds a world whose people's tasks can only finish."""

    def test_the_saved_waltzman_worlds_are_caught(self):
        for bundle, causal in (_saved(C1R18),):
            findings = attempts.part_way_findings(causal)
            self.assertEqual(len(findings), 1)
            self.assertIn("resolve-concern", findings[0]["finding"])
            self.assertIn("remedy_under_way", findings[0]["finding"])

    def test_the_rebuilt_c1r20_world_lets_a_remedy_end_two_ways(self):
        world = built()
        self.assertEqual(attempts.part_way_findings(world["causal_model"]), [])
        person = [t for t in attempts.long_tasks(world["causal_model"], world["bundle"]) if t["started_by"] == "person"]
        self.assertEqual({t["action"] for t in person}, {"resolve-concern", "resolve-own-concern"})
        self.assertTrue(all(t["can_fail_part_way"] for t in person))

    def test_worlds_that_already_could_fail_or_have_no_long_tasks_pass(self):
        self.assertEqual(attempts.part_way_findings(_truck()[1]), [])  # driving runs dry or arrives
        _, pencil = _saved(PENCIL)
        self.assertEqual([t for t in attempts.long_tasks(pencil) if t["started_by"] == "person"], [])
        self.assertEqual(attempts.part_way_findings(pencil), [])

    def test_the_finding_reaches_the_build_record_sentence(self):
        from scripts.world_builder_service import _dry_run_sentence
        row = {"ok": True, "accepted_actions": 9, "turns": 8, "active_at_end": True,
               "long_tasks": [{"action": "resolve-concern", "started_by": "person", "can_fail_part_way": False},
                              {"action": "decision-authorized-at-deadline", "started_by": "world",
                               "can_fail_part_way": True}]}
        sentence = _dry_run_sentence(row, "ongoing")
        self.assertIn("no task a person starts can fail part-way", sentence)
        self.assertIn("followed as the world's own tasks: decision authorized at deadline", sentence)


class RemedyCarriesItsAnswerTests(unittest.TestCase):
    """E2: a finished remedy says it answered the question, and who carried it out; the loop is bounded."""

    def setUp(self):
        world = built()
        self.engine, _, _ = build_engine(world["bundle"], world["causal_model"])
        self.causal = world["causal_model"]

    def _offered(self, actor, kind):
        return [a["action"] for a in self.engine.discover(actor)["available"]
                if a["action"]["kind"] == kind and a["action"].get("matter", LEGAL) == LEGAL]

    def _do(self, actor, kind):
        offered = self._offered(actor, kind)
        self.assertTrue(offered, f"{actor} is not offered {kind}")
        result = self.engine.submit(dict(offered[0], controller="test"))
        self.assertEqual(result["status"], "accepted", result)
        return result

    def _concern(self):
        return self.engine.world.entities[LEGAL].as_dict()["components"]["concern"]

    def test_a_finished_remedy_records_the_answer_and_a_dispute_is_allowed_once(self):
        self._do("legal-group", "communicate")
        self._do("country-two", "resolve-own-concern")
        self.assertEqual((self._concern()["remedy_by"], self._concern()["answered"]), ("country-two", False))
        for _ in range(3):
            self.engine.advance(1)
        self.assertEqual((self._concern()["status"], self._concern()["answered"]), ("resolved", True))
        self._do("country-two", "reopen-concern")
        self.assertEqual((self._concern()["status"], self._concern()["answered"]), ("open", False))
        self._do("country-two", "resolve-own-concern")
        for _ in range(3):
            self.engine.advance(1)
        self.assertEqual(self._concern()["status"], "resolved")
        self.assertEqual(self._offered("country-two", "reopen-concern"), [])  # the second answer stands

    def test_the_holder_can_stop_someone_elses_remedy_part_way(self):
        self._do("legal-group", "communicate")
        self.assertEqual(self._offered("legal-group", "object-to-remedy"), [])  # nothing under way
        result = self._do("country-two", "resolve-own-concern")
        self.assertEqual(self._offered("country-two", "object-to-remedy"), [])  # not one's own remedy
        task = attempts.started(attempts.task_watchers(self.causal), "country-two", "resolve-own-concern",
                                [c for c in result["event"]["changes"] if c["path"].endswith(".status")], 1, "r1-e1")
        self.assertEqual(len(task), 1)
        stop = self._do("legal-group", "object-to-remedy")
        self.assertEqual((self._concern()["status"], self._concern()["remedy_ticks_left"]), ("open", 0))
        changes = [c for c in stop["event"]["changes"] if ".components.concern." in c["path"]]
        ended = attempts.ended(task[0], stop["event"], "r1-e2", 1, changes)
        self.assertEqual((ended["status"], ended["ended_by"], ended["ended_by_person"]),
                         ("failed", "object-to-remedy", "legal-group"))

    def test_no_concern_is_answered_more_than_four_times_in_a_long_free_replay(self):
        _, more = replayed()
        entities = more["final_snapshot"]["world"]["entities"]
        entities = entities if isinstance(entities, dict) else {e["entity_id"]: e for e in entities}
        resolved = {eid: e["components"]["concern"]["times_resolved"] for eid, e in entities.items()
                    if "concern" in (e.get("components") or {})}
        self.assertEqual(len(resolved), 4)
        self.assertLessEqual(max(resolved.values()), 4, resolved)


class FinishedTaskNoticeTests(unittest.TestCase):
    """E2: when a remedy finishes, the concern's holder is told who did it and what they said it would do."""

    def test_the_holder_and_the_recipient_hear_what_the_remedy_did(self):
        trace, _ = replayed()
        turn = next(t for t in trace["transcript"] for u in t["underway"]
                    if u["status"] == "finished" and u["person"] != WORLD and u["action"].startswith("resolve"))
        task = next(u for u in turn["underway"] if u["status"] == "finished" and u["person"] != WORLD)
        said = "a 90-day retention period is added to the shared draft"
        built_world = built()
        engine, _, _ = build_engine(built_world["bundle"], built_world["causal_model"])
        entities = engine.world.material_dict()["entities"]
        concern = entities[task["entity"]]["components"]
        holder, recipient = concern["information"]["source_id"], concern["concern"]["recipient_id"]
        actors = sorted({holder, recipient, task["person"], "country-dune"})
        notices = attempts.finished_notices([{**task, "expects": said}], entities, actors, turn["turn"])
        told = {actor for actor, _ in notices}
        self.assertEqual(told, {holder, recipient} - {task["person"]})
        self.assertNotIn("country-dune", told)
        self.assertTrue(all(said in text and task["person"] in text for _, text in notices))
        # nothing for a stopped remedy, a world task, or a remedy started without words
        self.assertEqual(attempts.finished_notices([{**task, "expects": said, "status": "failed"}], entities, actors, 1), [])
        self.assertEqual(attempts.finished_notices([{**task, "expects": None}], entities, actors, 1), [])


class WorldTasksTests(unittest.TestCase):
    """E3: the rollout a deadline rule starts is followed from its start to its ending event."""

    def test_the_rollout_is_a_task_the_world_starts_and_can_end_two_ways(self):
        world = built()
        tasks = [t for t in attempts.long_tasks(world["causal_model"], world["bundle"]) if t["started_by"] == "world"]
        self.assertEqual({t["action"] for t in tasks},
                         {"decision-authorized-at-deadline", "decision-authorized-at-last-deadline"})
        self.assertTrue(all(t["value"] == "authorized" and t["can_fail_part_way"] for t in tasks))
        # a meeting being on and a decision open again are not tasks (one way to end; where the world rests)
        watched = attempts.world_watchers(world["causal_model"], world["bundle"])
        self.assertEqual(set(watched), {("components.group_decision.status", "'authorized'")})

    def test_a_free_replay_follows_the_rollout_to_its_ending_event(self):
        trace, _ = replayed()
        rollout = [(t["turn"], u) for t in trace["transcript"] for u in t["underway"] if u["person"] == WORLD]
        self.assertTrue(rollout, "the rollout was never followed")
        ended = [(turn, u) for turn, u in rollout if u["status"] != "underway"]
        self.assertTrue(ended)
        turn, last = ended[0]
        self.assertEqual(last["field"], "components.group_decision.status")
        self.assertRegex(last["started_event_id"], r"^r\d+-e\d+$")
        self.assertRegex(last["ending_event_id"], rf"^r{turn}-e\d+$")
        self.assertIn(last["ended_by"], {"deployment-completes", "authorization-withdrawn"})
        events = {e["event_id"]: e for t in trace["transcript"] for e in t["world_events"]}
        self.assertEqual(events[last["started_event_id"]]["rule_id"], last["action"])
        self.assertEqual(events[last["ending_event_id"]]["rule_id"], last["ended_by"])

    def test_a_world_task_carried_by_the_page_survives_validation(self):
        trace, _ = replayed()
        open_world = [t for t in trace["underway"] if t["person"] == WORLD]
        for task in open_world:
            self.assertEqual(set(task), attempts.TASK_KEYS)


class DecisionCopyTests(unittest.TestCase):
    """E4: no record says the decision's subject is in effect while the decision says otherwise."""

    def test_the_saved_c1r20_copy_is_found_and_removed(self):
        from spec_pipeline import drop_decision_copies
        world = built()
        dropped = [d for d in world["dropped_generated_rules"] if "copied the decision's status" in d]
        self.assertEqual(len(dropped), 1)
        self.assertIn("deploy-early-warning-system", dropped[0])
        self.assertIn("activation_state", dropped[0])
        mech = next(m for m in world["causal_model"]["mechanics"] if m["action_kind"] == "deploy-early-warning-system")
        self.assertNotIn("components.system_readiness.activation_state", [e["path"] for e in mech["effects"]])
        _, c1r18 = _saved(C1R18)
        _, again = drop_decision_copies(json.loads(json.dumps(c1r18)))
        self.assertEqual(drop_decision_copies(json.loads(json.dumps(world["causal_model"])))[1], [])
        for line in again:  # whatever the c1r18 writer copied is caught the same way
            self.assertIn("copied the decision's status", line)

    def test_a_record_that_rules_set_back_is_not_a_copy(self):
        from spec_pipeline import drop_decision_copies
        world = built()
        causal = world["causal_model"]
        # readiness is set to several values by several moves, so no single value is a one-way copy
        _, found = drop_decision_copies(json.loads(json.dumps(causal)))
        self.assertFalse([d for d in found if "readiness to" in d])

    def test_nothing_reads_activated_while_the_decision_is_not_deployed_in_a_free_replay(self):
        trace, _ = replayed()
        for turn in trace["transcript"]:
            for row in turn["actors"].values():
                for change in row.get("changes") or []:
                    self.assertNotEqual(change.get("after"), "activated", (turn["turn"], change))


if __name__ == "__main__":
    unittest.main()
