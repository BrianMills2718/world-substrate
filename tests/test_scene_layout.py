"""A world's layout declaration: validated against a prepared map, and enough to export a replay with no hand-made config.

Implements: scene-viewer/world-layout-declaration
"""
from __future__ import annotations

import json
import sys
from copy import deepcopy
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import scene_layout  # noqa: E402
from scripts.scaffold_world import BundleError, validate_bundle  # noqa: E402

BUNDLE = json.loads((ROOT / "examples/world_authoring/pump-facility-v0.json").read_text())
VILLE = Path.home() / "code2/generative_agents/environment/frontend_server/static_dirs/assets/the_ville/matrix"


def with_layout(**changes):
    bundle = deepcopy(BUNDLE)
    bundle["layout"].update(changes)
    return bundle


@pytest.mark.req("scene-viewer/world-layout-declaration")
def test_the_pump_facility_layout_resolves_to_rooms_doors_people_and_sprites():
    got = scene_layout.resolve(validate_bundle(BUNDLE))
    assert got["rooms"]["corridor"] == "Dorm for Oak Hill College|common room"
    assert got["people"] == {"ari": "Ari", "mara": "Mara", "bo": "Bo"} and got["sprites"]["Ari"] == "Abigail_Chen"
    assert got["labels"]["lab-door-in"] == "laboratory door" and got["labels"]["ari"] == "Ari"
    assert set(got["doors"]) == {"laboratory-door", "control-room-door"}


@pytest.mark.req("scene-viewer/world-layout-declaration")
@pytest.mark.parametrize("change,message", [
    ({"map": "no-such-map"}, "not a prepared map"),
    ({"rooms": {"laboratory": "zzz", "corridor": "hub", "control-room": "b"}}, "uses slot 'zzz'"),
    ({"rooms": {"laboratory": "a", "corridor": "a", "control-room": "b"}}, "share one map slot"),
    ({"rooms": {"laboratory": "a", "corridor": "hub", "control-room": "c", "ghost": "b"}}, "not a declared public entity"),
    ({"doors": {"x": {"between": ["laboratory", "control-room"], "halves": ["lab-door-out"]}}}, "not connected"),
    ({"people": {"nobody": {"start": "corridor"}}}, "not a declared actor"),
    ({"people": {"ari": {"start": "attic"}}}, "not laid out"),
])
def test_a_layout_that_cannot_be_drawn_is_refused_with_its_reason(change, message):
    with pytest.raises(BundleError, match=message):
        validate_bundle(with_layout(**change))


@pytest.mark.req("scene-viewer/world-layout-declaration")
def test_places_with_no_door_between_them_are_refused():
    with pytest.raises(BundleError, match="not joined"):
        validate_bundle(with_layout(doors={"laboratory-door": BUNDLE["layout"]["doors"]["laboratory-door"]}))


@pytest.mark.req("scene-viewer/world-layout-declaration")
def test_a_world_without_a_layout_still_validates_and_a_second_map_accepts_the_same_story():
    plain = deepcopy(BUNDLE)
    del plain["layout"]
    validate_bundle(plain)
    college = with_layout(map="ville-college")
    for person in college["layout"]["people"].values():
        person.pop("sprite")
    got = scene_layout.resolve(validate_bundle(college))
    assert got["rooms"]["corridor"] == "Oak Hill College|hallway" and got["sprites"]["Ari"] == "Latoya_Williams"


@pytest.mark.req("scene-viewer/world-layout-declaration")
@pytest.mark.skipif(not VILLE.exists(), reason="needs the local Smallville clone (art and map are not in this repository)")
@pytest.mark.parametrize("map_id", sorted(scene_layout.prepared_maps()))
def test_every_connection_a_prepared_map_declares_is_walkable_with_a_doorway(map_id):
    from scripts import export_smallville_replay as ex
    maze = ex.load_maze(VILLE)
    prepared = scene_layout.prepared_maps()[map_id]
    for a, b in prepared["connections"]:
        start, goal = ex.anchor(maze, prepared["slots"][a]), ex.anchor(maze, prepared["slots"][b])
        assert ex.doorway(maze, [start] + ex.walk(maze, start, goal))


@pytest.mark.req("scene-viewer/owner-run-viewer")
def test_a_run_log_alone_gives_the_same_replay_as_the_hand_exported_one():
    """The first saved round carries the bundle, so the run log is enough: no separate bundle file."""
    from scripts import open_scene_viewer as viewer
    run_log = ROOT / "evidence/ui/inhabited-facility-20261113/run-log.jsonl"
    rows = [json.loads(line) for line in run_log.read_text().splitlines() if line.strip()]
    rows[0]["request"]["bundle"]["layout"] = BUNDLE["layout"]  # this saved run predates layouts
    rows.insert(0, {**rows[0], "ts": "0", "path": "/other"})  # a non-run row is ignored
    chain, bundle = viewer.pick_run(rows, "Pump Facility")
    assert len(chain) == 6 and bundle["layout"]["map"] == "ville-dorm"
    with pytest.raises(SystemExit, match="no saved run"):
        viewer.pick_run(rows, "No Such World")


@pytest.mark.req("scene-viewer/owner-run-viewer")
@pytest.mark.skipif(not VILLE.exists(), reason="needs the local Smallville clone")
def test_the_owner_export_reproduces_the_viewer_replay():
    from scripts import open_scene_viewer as viewer
    from scripts.export_smallville_replay import export_from_rows
    rows = [json.loads(line) for line in (ROOT / "evidence/ui/inhabited-facility-20261113/run-log.jsonl").read_text().splitlines() if line.strip()]
    rows[0]["request"]["bundle"]["layout"] = BUNDLE["layout"]
    chain, bundle = viewer.pick_run(rows, None)
    got = export_from_rows(chain, bundle, VILLE)
    assert got == json.loads((ROOT / "viewer/smallville/replay.json").read_text())
