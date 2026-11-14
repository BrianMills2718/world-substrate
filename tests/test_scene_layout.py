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
@pytest.mark.parametrize("map_id", sorted(k for k, v in scene_layout.prepared_maps().items() if v.get("kind") != "generated"))
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


@pytest.mark.req("scene-viewer/public-generated-map")
@pytest.mark.parametrize("map_id", ["public-hub-3", "public-hub-5"])
def test_a_generated_map_connects_every_declared_slot_through_a_two_tile_doorway(map_id):
    from scripts import export_smallville_replay as ex
    from scripts.generated_map import build
    prepared = scene_layout.prepared_maps()[map_id]
    built = build(map_id, list(prepared["slots"]))
    maze = built["maze"]
    for a, b in prepared["connections"]:
        start, goal = ex.anchor(maze, prepared["slots"][a]), ex.anchor(maze, prepared["slots"][b])
        gap = ex.doorway(maze, [start] + ex.walk(maze, start, goal))
        assert len(gap) == 2
    assert all(0 <= t < 132 for row in built["grid"]["data"] for t in row)  # inside the 12 x 11 Tiny Dungeon sheet
    assert all(0 <= t < 132 for _, _, t in built["grid"]["props"])


@pytest.mark.req("scene-viewer/public-generated-map")
def test_the_pump_story_exports_on_a_generated_map_with_no_clone_and_no_private_art():
    from scripts.export_smallville_replay import export_from_rows
    bundle = deepcopy(BUNDLE)
    bundle["layout"]["map"] = "public-hub-3"
    bundle["layout"]["rooms"] = {"laboratory": "a", "corridor": "hub", "control-room": "b"}
    for person in bundle["layout"]["people"].values():
        person.pop("sprite")
    rows = [json.loads(line) for line in (ROOT / "evidence/ui/inhabited-facility-20261113/scripted-run-log.jsonl").read_text().splitlines() if line.strip()]
    replay = export_from_rows(rows, validate_bundle(bundle), Path("/does/not/exist"))
    assert replay["grid"]["sheet"] == "tinydungeon.png" and set(replay["sprites"].values()) <= {"td-85", "td-99", "td-97"}
    assert len(replay["doors"]["laboratory-door"]["tiles"]) == 2
    walk = [replay["steps"][k]["Ari"]["movement"] for k in sorted(replay["steps"], key=int)]
    assert all(abs(a[0] - b[0]) + abs(a[1] - b[1]) <= 1 for a, b in zip(walk, walk[1:]))


def _share_of_the_scripted_pump_run():
    rows = [json.loads(line) for line in (ROOT / "evidence/ui/inhabited-facility-20261113/scripted-run-log.jsonl").read_text().splitlines() if line.strip()]
    rounds = [t for r in rows for t in r["result"]["transcript"]]
    return {"world": {"bundle": validate_bundle(deepcopy(BUNDLE))}, "rounds": rounds}


@pytest.mark.req("scene-viewer/public-generated-map")
def test_a_share_replay_uses_the_generated_map_withholds_report_words_and_keeps_them_for_the_owner():
    from scripts.world_builder_service import _public_replay
    share = _share_of_the_scripted_pump_run()
    public, owner = _public_replay(share), _public_replay(share, owner=True)
    assert public["ok"] and public["grid"]["sheet"] == "tinydungeon.png" and public["map"].startswith("public-hub")
    chats = lambda r: [c[1] for f in r["steps"].values() for who in f.values() for c in (who.get("chat") or [])]
    assert chats(owner) and all("words not shown" in c for c in chats(public)) and len(chats(public)) == len(chats(owner))
    assert not any(c in " ".join(chats(public)) for c in [t.split(": ", 1)[1] for t in chats(owner)])
    assert "ville" not in json.dumps(public).lower().replace("the_ville", "")  # no private map name in the public payload


@pytest.mark.req("scene-viewer/public-generated-map")
def test_a_world_with_no_layout_has_no_public_room_map():
    from scripts.world_builder_service import _public_replay
    share = _share_of_the_scripted_pump_run()
    del share["world"]["bundle"]["layout"]
    with pytest.raises(scene_layout.LayoutError):
        _public_replay(share)
