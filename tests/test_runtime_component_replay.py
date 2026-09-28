from __future__ import annotations

import unittest
from dataclasses import dataclass

from world_substrate.engine import Engine
from world_substrate.information import InformationState
from world_substrate.model import COMPONENT_TYPES, Entity, World
from world_substrate.rules import RuleRegistry


@dataclass
class LocalInformationState:
    content: str


class RuntimeComponentReplayTests(unittest.TestCase):
    def test_engine_replay_uses_world_local_component_type_without_global_registration(self):
        self.assertIs(COMPONENT_TYPES["information"], InformationState)
        registry = RuleRegistry()
        world = World(
            world_id="runtime-component-replay",
            revision=0,
            tick=0,
            entities={
                "note": Entity(
                    entity_id="note",
                    label="Local note",
                    category_ids=("note",),
                    components={
                        "information": LocalInformationState(content="local payload")
                    },
                )
            },
            engine_id="world-substrate-core@1",
            content_id="runtime-component-replay@1",
            rule_versions=registry.versions(),
        )
        engine = Engine(world, registry)

        replay = engine.replay()

        self.assertTrue(replay["ok"])
        self.assertTrue(replay["event_match"])
        self.assertEqual(replay["steps"], 0)
        self.assertIs(COMPONENT_TYPES["information"], InformationState)
        restored = World.from_snapshot(
            engine.initial_snapshot(),
            component_types={"information": LocalInformationState},
        )
        self.assertIsInstance(
            restored.entities["note"].component("information"),
            LocalInformationState,
        )
        self.assertEqual(restored.material_dict(), engine.world.material_dict())


if __name__ == "__main__":
    unittest.main()
