"""Ownership references are checked, not merely conventional.

`owner_ref` encodes a kind and a target — "actor:robinson", "place:camp",
"assembly:frame-a" — and until M7 that convention lived only in the eighteen
f-strings that built it. Every layer treated it as a bare string, so `""` was
accepted by the type system, the engine's write-scope guard, `World.validate()`
and the mechanic installer alike.

The closure evidence here is not hypothetical: it replays the exact declaration
a model produced in the M7 authoring experiment, read from that experiment's
retained evidence file.
"""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from reference_worlds.workshop.mechanics import AttachAction, PickUpAction
from reference_worlds.workshop.probe import build_engine
from world_substrate.authoring import CompiledMechanic, DeclaredMechanic
from world_substrate.model import owner_ref, parse_owner_ref

M7_EVIDENCE = REPO / "evidence/m7/authoring-attempts-v0.json"


class OwnerReferenceTests(unittest.TestCase):
    def test_valid_references_round_trip(self) -> None:
        for kind, target in (
            ("actor", "robinson"),
            ("place", "camp"),
            ("assembly", "frame-a"),
        ):
            with self.subTest(kind=kind):
                reference = owner_ref(kind, target)
                self.assertEqual(reference, f"{kind}:{target}")
                self.assertEqual(parse_owner_ref(reference), (kind, target))

    def test_malformed_references_are_refused_at_the_source(self) -> None:
        for kind, target in (("", "x"), ("actor", ""), ("Actor", "x"), ("a b", "x")):
            with self.subTest(kind=kind, target=target), self.assertRaises(ValueError):
                owner_ref(kind, target)

    def test_an_empty_reference_cannot_be_committed(self) -> None:
        engine = build_transfer_engine(REPO)
        engine.world.entities["clay-pot"].ownership.owner_ref = ""

        with self.assertRaisesRegex(ValueError, "invalid ownership reference"):
            engine.world.validate()


class M7ClosureTests(unittest.TestCase):
    """The defect this fix exists for, replayed from the experiment's evidence."""

    def _m7_declaration(self) -> dict:
        attempts = json.loads(M7_EVIDENCE.read_text())["attempts"]
        for attempt in attempts:
            declaration = attempt.get("declaration") or {}
            for effect in declaration.get("effects") or []:
                if effect.get("path") == "ownership.owner_ref" and effect.get("value") == "":
                    return declaration
        raise AssertionError("no M7 attempt set owner_ref to an empty string")

    def test_the_authored_mechanic_that_destroyed_provenance_is_now_refused(
        self,
    ) -> None:
        declaration = self._m7_declaration()
        engine = build_engine(REPO)
        engine.registry.register_process(
            CompiledMechanic(DeclaredMechanic.from_dict(declaration))
        )
        engine.world.rule_versions = engine.registry.versions()
        engine.apply(PickUpAction("mira", "wrench-1", engine.world.revision, "t"))
        engine.apply(PickUpAction("mira", "leg-1", engine.world.revision, "t"))
        engine.apply(AttachAction("mira", "leg-1", "frame-a", engine.world.revision, "t"))

        with self.assertRaisesRegex(ValueError, "invalid ownership reference"):
            engine.advance(2)

        # The provenance AttachRule established survives the refusal.
        self.assertEqual(
            engine.world.entities["leg-1"].ownership.owner_ref, "assembly:frame-a"
        )


if __name__ == "__main__":
    unittest.main()
