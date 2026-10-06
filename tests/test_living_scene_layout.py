"""Both living-scene renderers place actors by one shared rule (gaps G9/#106 and G10)."""

from __future__ import annotations

import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "src"))

from world_substrate.living_scene import (  # noqa: E402
    build_living_scene_frames,
    load_live_projection_bundle,
    load_scene_contract,
)

FIXTURES = REPO / "tests/fixtures/living_scene"
PROFILE = FIXTURES / "neutral-render-profile-v1.json"
PROJECTION = FIXTURES / "neutral-render-projection-v0.json"


def _load_renderer(name: str):
    spec = importlib.util.spec_from_file_location(name, REPO / f"scripts/{name}.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _positions(frames, profile) -> list[dict[str, list[float]]]:
    """Run the shared JS rule in node for every frame (desktop layout)."""
    from world_substrate.living_scene_layout import ACTOR_POSITIONS_JS

    node = shutil.which("node")
    if node is None:
        raise unittest.SkipTest("node is not installed")
    script = ACTOR_POSITIONS_JS + """
const [frames, profile] = JSON.parse(require('fs').readFileSync(0, 'utf8'));
const h = {home: c => c.home, anchor: c => c.anchor, radius: r => r.gather_radius || 11,
  anchorFor: op => Array.isArray(op.anchor) ? op.anchor : op.entity ? (profile.entities[op.entity] || {}).home : null};
console.log(JSON.stringify(frames.map((_, i) => wsActorPositions(frames, i, profile, h))));
"""
    result = subprocess.run(
        [node, "-e", script], input=json.dumps([frames, profile]),
        capture_output=True, text=True, check=True,
    )
    return json.loads(result.stdout)


class LivingSceneLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profile = load_scene_contract(PROFILE)
        cls.bundle = load_live_projection_bundle(PROJECTION)
        cls.frames = build_living_scene_frames(cls.bundle, cls.profile)

    def test_both_renderers_embed_the_one_shared_rule(self) -> None:
        for name in ("render_living_scene", "render_composed_living_scene"):
            with self.subTest(renderer=name):
                html = _load_renderer(name).render_html(self.bundle, self.profile, PROFILE.parent)
                self.assertEqual(html.count("function wsActorPositions("), 1)
                self.assertIn("return wsActorPositions(FRAMES,idx,PROFILE,", html)
                # No renderer keeps a private copy of the move_to replay any more.
                self.assertEqual(html.count("op.op==='actor.move_to'"), 1)

    def test_activity_ring_wins_over_an_earlier_move_and_moves_persist(self) -> None:
        # G10: frame 1 moves actor-a to resource-a; frame 2 starts the activity.
        positions = _positions(self.frames, self.profile)
        resource = self.profile["entities"]["resource-a"]["home"]
        self.assertEqual(positions[1]["actor-a"], resource)
        anchor = self.profile["activities"]["activity-a"]["anchor"]
        statuses = [f["views"]["activities"]["activity-a"]["bindings"].get("status") for f in self.frames]
        active = [i for i, s in enumerate(statuses) if s == "active"]
        self.assertTrue(active, statuses)
        first = active[0]
        self.assertGreater(first, 1)
        a = positions[first]["actor-a"]
        self.assertAlmostEqual(a[0], anchor[0], places=6)
        self.assertAlmostEqual(a[1], anchor[1] - 11, places=6)
        # Once the activity is over the actor is back where it last went, not home.
        after = [i for i in range(first, len(self.frames)) if statuses[i] != "active"]
        for i in after:
            self.assertEqual(positions[i]["actor-a"], resource)

    def test_actors_moved_to_one_place_are_spread_not_stacked(self) -> None:
        # Issue #106: two actor.move_to to the same anchor on one event.
        profile = copy.deepcopy(self.profile)
        ops = profile["event_visuals"]["neutral.resource.drop"]["operations"]
        ops.append({**ops[0], "actor": "actor-b"})
        frames = build_living_scene_frames(self.bundle, profile)
        positions = _positions(frames, profile)
        a, b = positions[1]["actor-a"], positions[1]["actor-b"]
        self.assertNotEqual(a, b)
        resource = profile["entities"]["resource-a"]["home"]
        for p in (a, b):
            distance = ((p[0] - resource[0]) ** 2 + (p[1] - resource[1]) ** 2) ** 0.5
            self.assertAlmostEqual(distance, 11, places=6)
        # Stable order by actor id: the first id sits at the top of the ring.
        self.assertLess(a[1], b[1])

    def test_a_single_actor_keeps_the_exact_anchor(self) -> None:
        positions = _positions(self.frames, self.profile)
        for i, row in enumerate(positions):
            with self.subTest(frame=i):
                homes = {k: v["home"] for k, v in self.profile["actors"].items()}
                if i == 0:
                    self.assertEqual(row, homes)


if __name__ == "__main__":
    unittest.main()
