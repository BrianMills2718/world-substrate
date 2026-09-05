"""The two things the M5 policy could not see.

M5's run oscillated heat/unheat for seven turns because nothing said how far
boiling had got, and then filled its own treated pot and drank it because
`fill` was presented identically whether or not it destroyed the treatment.
Both are seam findings: the mechanics were correct and the affordance page was
not telling a policy what it needed.

Neither test calls a model. They drive the engine to the state and read the
page a policy would read.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_freshwater_engine
from reference_worlds.workshop.probe import build_engine as build_workshop
from world_substrate.policy import present


def accept(engine, kind, **fields):
    result = engine.submit(
        {
            "actor": "robinson",
            "kind": kind,
            "base_revision": engine.world.revision,
            "controller": "test",
            **fields,
        }
    )
    assert result["status"] == "accepted", (kind, result["status"])
    return result


def boiling_pot():
    """A pot of untreated water on the fire, partway to treatment."""
    engine = build_freshwater_engine()
    accept(engine, "fill", vessel="clay-pot", source="unsafe-pool", volume_ml=1000)
    accept(engine, "heat", vessel="clay-pot", target="fire-camp")
    return engine


class ProcessProgressIsVisible(unittest.TestCase):
    def test_a_pot_partway_through_boiling_reports_how_far(self):
        engine = boiling_pot()
        engine.advance(4)
        pot = engine.world.entities["clay-pot"]
        # Precondition: genuinely partway, not done and not unstarted.
        self.assertEqual(pot.container.boiling_ticks, 1)
        self.assertGreater(pot.liquid.pathogens, 0)

        rows = engine.discover("robinson")["progress"]
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(row["entity_id"], "clay-pot")
        self.assertEqual(row["rule_id"], "process.thermal.vessels")
        self.assertEqual((row["current"], row["required"]), (1, 2))

    def test_progress_ends_when_the_water_is_treated(self):
        engine = boiling_pot()
        engine.advance(5)
        self.assertEqual(engine.world.entities["clay-pot"].liquid.pathogens, 0)
        self.assertEqual(engine.discover("robinson")["progress"], [])

    def test_nothing_in_flight_reports_nothing(self):
        engine = build_freshwater_engine()
        self.assertEqual(engine.discover("robinson")["progress"], [])

    def test_a_policy_actually_reads_it(self):
        engine = boiling_pot()
        engine.advance(4)
        page = engine.discover("robinson")
        view = present(engine, "robinson", page)
        self.assertIn("boiling to kill pathogens 1/2", view["progress"])

    def test_a_world_whose_processes_declare_none_is_unaffected(self):
        # The substrate cannot know which of a world's fields count toward
        # something, so progress is declared. The workshop declares none.
        self.assertEqual(build_workshop().discover("mira")["progress"], [])


class ValueDestroyingActionsAreMarked(unittest.TestCase):
    def treated_pot(self):
        engine = boiling_pot()
        engine.advance(5)
        assert engine.world.entities["clay-pot"].liquid.pathogens == 0
        return engine

    def fills(self, engine, vessel):
        page = engine.discover("robinson")
        return [
            row
            for row in page["available"] + page["blocked"]
            if row["action"]["kind"] == "fill" and row["action"]["vessel"] == vessel
        ]

    def test_filling_a_treated_vessel_is_marked_destructive(self):
        engine = self.treated_pot()
        rows = self.fills(engine, "clay-pot")
        self.assertTrue(rows)
        for row in rows:
            self.assertTrue(row["consequences"])
            self.assertIn("re-contaminates", row["consequences"][0])

    def test_filling_an_empty_vessel_is_not(self):
        engine = self.treated_pot()
        rows = self.fills(engine, "cup-robinson")
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["consequences"], [])

    def test_filling_an_already_untreated_vessel_is_not(self):
        # Nothing of value is destroyed: it was already contaminated.
        engine = build_freshwater_engine()
        accept(engine, "fill", vessel="clay-pot", source="unsafe-pool", volume_ml=250)
        for row in self.fills(engine, "clay-pot"):
            self.assertEqual(row["consequences"], [])

    def test_the_warning_reaches_the_policy_view(self):
        engine = self.treated_pot()
        view = present(engine, "robinson", engine.discover("robinson"))
        marked = [
            row for row in view["actions"] if "destroys:" in row["description"]
        ]
        self.assertTrue(marked)
        self.assertIn("re-contaminates", marked[0]["description"])

    def test_a_rule_that_declares_no_consequences_reports_none(self):
        engine = self.treated_pot()
        page = engine.discover("robinson")
        others = [
            row
            for row in page["available"] + page["blocked"]
            if row["action"]["kind"] != "fill"
        ]
        self.assertTrue(others)
        for row in others:
            self.assertEqual(row["consequences"], [])


if __name__ == "__main__":
    unittest.main()
