"""Two guards that were bound to the first world, and one that trusted the caller.

Both were found by probing the *second* world rather than by reading the code,
which is the same way M6 found its four couplings. M6 then certified the assays
as having "transferred with no edits at all" -- true only in the sense that
they did not crash.
"""

from __future__ import annotations

import inspect
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.workshop.probe import build_engine, build_registry
from world_substrate.assay import (
    _component_names,
    _reads_component,
    _subject,
    assay_undeclared_component_reads,
)
from world_substrate.engine import _action_entity_refs
from world_substrate.rules import Check


class UnderDeclaringWorkshopProcess:
    """Reads the workshop's tool component; declares only worker.

    Defined at module scope so `inspect.getsource` can reach it, which is what
    the assay's heuristic depends on.
    """

    rule_id = "workshop.process.under-declaring"
    version = "1"
    order = 99
    read_paths = ("entities.<x>.components.worker.fatigue",)
    write_paths = ("entities.<x>.components.worker.fatigue",)

    def due(self, world) -> bool:
        return True

    def apply(self, world) -> None:
        for entity in world.entities.values():
            if entity.components.get("tool") is not None:
                entity.components["worker"].fatigue += 1


class EnvelopeMetadataCannotWidenWriteScope(unittest.TestCase):
    """`controller` is a free-form string the submitter chooses.

    Counting it as a participant meant the identical defective rule was
    refused with controller="script" and accepted with controller="wrench-1".
    """

    def envelope(self, controller: str) -> dict[str, object]:
        return {
            "actor": "mira",
            "kind": "poke",
            "base_revision": 0,
            "controller": controller,
        }

    def test_controller_never_binds_a_participant(self):
        known = frozenset(build_engine().world.entities)
        named = _action_entity_refs(self.envelope("wrench-1"), known)
        unnamed = _action_entity_refs(self.envelope("script"), known)
        self.assertEqual(named, unnamed)
        self.assertNotIn("wrench-1", named)

    def test_kind_never_binds_a_participant(self):
        known = frozenset(build_engine().world.entities)
        envelope = {**self.envelope("script"), "kind": "wrench-1"}
        self.assertNotIn("wrench-1", _action_entity_refs(envelope, known))

    def test_a_real_participant_still_binds(self):
        known = frozenset(build_engine().world.entities)
        envelope = {**self.envelope("script"), "item": "wrench-1"}
        self.assertIn("wrench-1", _action_entity_refs(envelope, known))

    def test_a_third_party_write_is_refused_however_it_is_named(self):
        for controller in ("script", "wrench-1"):
            with self.subTest(controller=controller):
                engine = build_engine()
                engine.registry.register_action(_PokeRule())
                engine.world.rule_versions = engine.registry.versions()
                before = engine.world.entities["wrench-1"].components["tool"].wear
                result = engine.submit(self.envelope(controller))
                self.assertEqual(result["status"], "scope_violation")
                self.assertEqual(
                    engine.world.entities["wrench-1"].components["tool"].wear, before
                )


class _PokeAction:
    kind = "poke"

    def __init__(self, actor_id: str, base_revision: int, controller_id: str):
        self.actor_id = actor_id
        self.base_revision = base_revision
        self.controller_id = controller_id

    def as_dict(self) -> dict[str, object]:
        return {
            "actor": self.actor_id,
            "kind": self.kind,
            "base_revision": self.base_revision,
            "controller": self.controller_id,
        }


class _PokeRule:
    """Declares a placeholder write path, then reaches a third party."""

    rule_id = "workshop.action.poke"
    version = "1"
    action_kind = "poke"
    read_paths = ("entities.<x>.components.tool.wear",)
    write_paths = ("entities.<x>.components.tool.wear",)

    def discover(self, world, actor_id):
        return []

    def action_from_dict(self, value):
        return _PokeAction(
            value["actor"], value["base_revision"], value["controller"]
        )

    def checks(self, world, action):
        return [Check("actor exists", action.actor_id in world.entities)]

    def apply(self, world, action, event_id) -> None:
        world.entities["wrench-1"].components["tool"].wear = 99


class AssaysSeeTheSecondWorld(unittest.TestCase):
    def test_the_component_vocabulary_includes_registered_components(self):
        names = _component_names()
        for component in ("worker", "part", "tool", "assembly"):
            self.assertIn(component, names)
        # And still every built-in.
        for component in ("liquid", "container", "heat_source"):
            self.assertIn(component, names)

    def test_registered_components_are_read_by_key_not_attribute(self):
        # The reason a wider name list alone changed nothing: a world pack's
        # components are dict entries, so `.tool` never appears in the source.
        source = inspect.getsource(UnderDeclaringWorkshopProcess)
        self.assertNotIn(".tool", source)
        self.assertTrue(_reads_component(source, "tool"))

    def test_field_named_after_a_component_is_not_a_component_read(self):
        # `.heat_source_id` is a field of container, not a heat_source read.
        self.assertFalse(_reads_component("vessel.heat_source_id", "heat_source"))
        self.assertTrue(_reads_component("vessel.heat_source", "heat_source"))

    def test_an_under_declaring_workshop_rule_is_flagged(self):
        registry = build_registry()
        rules = list(registry._actions.values()) + list(registry.processes())
        self.assertEqual(assay_undeclared_component_reads(rules), [])

        registry.register_process(UnderDeclaringWorkshopProcess())
        rules = list(registry._actions.values()) + list(registry.processes())
        findings = assay_undeclared_component_reads(rules)
        self.assertEqual(len(findings), 1)
        self.assertIn("tool", findings[0].detail)

    def test_workshop_actions_resolve_to_a_subject(self):
        engine = build_engine()
        known = frozenset(engine.world.entities)
        cases = (
            ({"actor": "mira", "kind": "pick_up", "item": "wrench-1"}, "wrench-1"),
            (
                {
                    "actor": "mira",
                    "kind": "attach",
                    "part": "leg-1",
                    "assembly": "frame-a",
                },
                "leg-1",
            ),
        )
        for action, expected in cases:
            with self.subTest(kind=action["kind"]):
                self.assertEqual(_subject(action, known), expected)

    def test_castaway_actions_keep_the_subject_they_always_had(self):
        # The old hardcoded key list picked `vessel` for every Castaway action.
        # Changing to "first non-actor participant" must not move any of them,
        # because the M3 and M4 assay evidence is pinned.
        from reference_worlds.castaway.probe import build_freshwater_engine

        engine = build_freshwater_engine()
        known = frozenset(engine.world.entities)
        page = engine.discover("robinson")
        seen = 0
        for row in page["available"] + page["blocked"]:
            action = row["action"]
            if "vessel" in action:
                self.assertEqual(_subject(action, known), action["vessel"])
                seen += 1
        self.assertGreater(seen, 0)

    def test_the_controller_is_never_the_subject(self):
        known = frozenset(build_engine().world.entities)
        action = {"actor": "mira", "kind": "pick_up", "controller": "wrench-1"}
        self.assertEqual(_subject(action, known), "?")


if __name__ == "__main__":
    unittest.main()
