"""M6: a second reference world, sharing no content with Castaway.

The point of this world is not the chair. It is to find out which parts of
"the substrate" are substrate and which are freshwater content wearing a
neutral name. Every check here runs the workshop through shared machinery that
was written before the workshop existed.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.workshop.mechanics import AttachAction, PickUpAction
from reference_worlds.workshop.probe import build_engine, build_registry
from world_substrate.assay import (
    assay_declared_readers,
    assay_undeclared_component_reads,
)
from world_substrate.policy import apply_choice, present, resolve_choice
from world_substrate.profile import MechanicProfile, retrofit_package


def _equip(engine):
    engine.apply(PickUpAction("mira", "wrench-1", engine.world.revision, "test"))
    return engine


class WorkshopBehaviourTests(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = build_engine(REPO)

    def test_the_world_builds_and_offers_affordances(self) -> None:
        page = self.engine.discover("mira")

        self.assertTrue(page["available"])
        self.assertTrue(
            all(row["action"]["kind"] == "pick_up" for row in page["available"])
        )

    def test_attaching_without_the_required_tool_is_refused(self) -> None:
        self.engine.apply(PickUpAction("mira", "leg-1", self.engine.world.revision, "t"))

        result = self.engine.apply(
            AttachAction("mira", "leg-1", "frame-a", self.engine.world.revision, "t")
        )

        self.assertEqual(result["status"], "precondition_failed")
        failed = [c["label"] for c in result["event"]["checks"] if not c["ok"]]
        self.assertIn("Worker holds a usable required tool", failed)

    def test_a_part_the_assembly_does_not_need_is_refused(self) -> None:
        _equip(self.engine)
        self.engine.apply(
            PickUpAction("mira", "shelf-1", self.engine.world.revision, "t")
        )

        result = self.engine.apply(
            AttachAction("mira", "shelf-1", "frame-a", self.engine.world.revision, "t")
        )

        self.assertEqual(result["status"], "precondition_failed")
        failed = [c["label"] for c in result["event"]["checks"] if not c["ok"]]
        self.assertIn("Assembly needs this part kind", failed)

    def test_a_chair_can_be_assembled_and_the_trace_replays(self) -> None:
        _equip(self.engine)
        for part in ("leg-1", "leg-2", "seat-1"):
            self.engine.apply(
                PickUpAction("mira", part, self.engine.world.revision, "t")
            )
            self.engine.apply(
                AttachAction("mira", part, "frame-a", self.engine.world.revision, "t")
            )
            self.engine.advance(1)

        attached = sorted(
            entity.component("part").part_kind
            for entity in self.engine.world.entities.values()
            if entity.component("part")
            and entity.component("part").attached_to == "frame-a"
        )
        self.assertEqual(attached, ["leg", "leg", "seat"])
        # Exact replay transferred to a new world with no work at all.
        self.assertTrue(self.engine.replay()["ok"])

    def test_processes_run_on_registered_components(self) -> None:
        _equip(self.engine)
        self.engine.advance(3)

        self.assertEqual(self.engine.world.entities["mira"].component("worker").fatigue, 9)
        self.assertEqual(self.engine.world.entities["wrench-1"].component("tool").wear, 21)


class SharedMachineryTransferTests(unittest.TestCase):
    """Each of these exercises machinery written before this world existed."""

    def setUp(self) -> None:
        self.engine = build_engine(REPO)
        self.registry = build_registry()
        self.rules = [
            self.registry.action(kind) for kind in self.registry.action_kinds()
        ] + list(self.registry.processes())

    def test_the_mechanic_profile_installer_accepts_workshop_mechanics(self) -> None:
        profile = MechanicProfile()
        for rule in self.rules:
            findings = profile.install(retrofit_package(rule, "workshop"), rule)
            self.assertEqual(
                [f for f in findings if f.severity == "reject"], [], rule.rule_id
            )

        self.assertEqual(len(profile.packages), 4)
        self.assertTrue(profile.freeze())

    def test_the_assays_run_on_workshop_mechanics(self) -> None:
        self.assertEqual(assay_undeclared_component_reads(self.rules), [])

        profile = MechanicProfile()
        for rule in self.rules:
            profile.install(retrofit_package(rule, "workshop"), rule)
        attach = profile.packages["workshop.assembly.attach"]
        others = {k: v for k, v in profile.packages.items() if k != attach.mechanic_id}

        findings = assay_declared_readers(attach, others)

        named = {f.detail.split()[0] for f in findings}
        self.assertIn("workshop.inventory.pick-up", named)

    def test_the_policy_seam_holds_in_a_world_it_was_not_written_for(self) -> None:
        page = self.engine.discover("mira")
        before = self.engine.world.material_hash()

        refused = resolve_choice(page, "not-a-real-id", "hallucinated")
        self.assertEqual(refused.kind, "refused")
        self.assertIsNone(apply_choice(self.engine, refused, controller="test"))
        self.assertEqual(self.engine.world.material_hash(), before)

        real = resolve_choice(page, page["available"][0]["action_id"], "legit")
        result = apply_choice(self.engine, real, controller="test")
        self.assertEqual(result["status"], "accepted")

    def test_the_policy_view_describes_a_world_it_knows_nothing_about(self) -> None:
        page = self.engine.discover("mira")

        context = present(self.engine, "mira", page)

        # No health, no hydration, no vessels anywhere.
        self.assertIn("fatigue", context["actor_state"])
        self.assertNotIn("health", context["actor_state"])
        self.assertIn("assembly", context["visible"])

    def test_write_scope_enforcement_binds_workshop_action_vocabulary(self) -> None:
        # The guard's placeholder binding originally used Castaway's action key
        # names, so a correctly declared workshop write looked out of scope.
        result = self.engine.apply(
            PickUpAction("mira", "leg-1", self.engine.world.revision, "test")
        )

        self.assertEqual(result["status"], "accepted")
        self.assertEqual(
            self.engine.world.entities["leg-1"].ownership.owner_ref, "actor:mira"
        )


if __name__ == "__main__":
    unittest.main()
