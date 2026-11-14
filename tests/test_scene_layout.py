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
    return {"world": {"bundle": validate_bundle(deepcopy(BUNDLE)), "causal_model": CAUSAL}, "rounds": rounds}


@pytest.mark.req("scene-viewer/public-generated-map")
def test_a_share_replay_uses_the_generated_map_withholds_report_words_and_keeps_them_for_the_owner():
    from scripts.world_builder_service import _public_replay
    share = _share_of_the_scripted_pump_run()
    public, owner = _public_replay(share), _public_replay(share, owner=True)
    assert public["ok"] and public["grid"]["sheet"] == "tinydungeon.png" and public["map"].startswith("public-hub")
    chats = lambda r: [c[1] for f in r["steps"].values() for who in f.values() for c in (who.get("chat") or [])]
    assert chats(owner) and all("words not shown" in c for c in chats(public)) and len(chats(public)) == len(chats(owner))
    assert not any(c in " ".join(chats(public)) for c in [t.split(": ", 1)[1] for t in chats(owner)])
    assert [r["kind"] for r in public["rules"]] == ["open-door", "move", "calibrate-pump", "send-report"]  # the rules ride with the share
    assert "ville" not in json.dumps(public).lower().replace("the_ville", "")  # no private map name in the public payload


@pytest.mark.req("scene-viewer/public-generated-map")
def test_a_world_with_no_layout_has_no_public_room_map():
    from scripts.world_builder_service import _public_replay
    share = _share_of_the_scripted_pump_run()
    del share["world"]["bundle"]["layout"]
    with pytest.raises(scene_layout.LayoutError):
        _public_replay(share)


CAUSAL = json.loads((ROOT / "examples/world_authoring/pump-facility-causal-v0.json").read_text())


@pytest.mark.req("scene-viewer/rules-overlay")
def test_a_replay_carries_the_worlds_rules_and_the_rule_each_attempt_met():
    from scripts.export_smallville_replay import export_from_rows
    rows = [json.loads(line) for line in (ROOT / "evidence/ui/inhabited-facility-20261113/scripted-run-log.jsonl").read_text().splitlines() if line.strip()]
    bundle = deepcopy(BUNDLE)
    bundle["layout"] = scene_layout.public_layout(bundle["layout"])
    replay = export_from_rows(rows, validate_bundle(bundle), Path("/nope"), causal=CAUSAL)
    rules = {r["kind"]: r for r in replay["rules"]}
    assert set(rules) == {"open-door", "move", "calibrate-pump", "send-report"}
    assert rules["open-door"]["at_doors"] and rules["move"]["at_doors"] and not rules["calibrate-pump"]["at_doors"]
    assert rules["calibrate-pump"]["needs"] == ["you are where it is"] and "sets the pump's status to calibrated" in rules["calibrate-pump"]["changes"]
    met = [(who["rule"]["kind"], who["rule"]["ok"], tuple(who["rule"]["why"]), who["rule"]["door"])
           for frame in replay["steps"].values() for who in frame.values() if who.get("rule")]
    assert ("move", False, ("the door must be open",), "laboratory-door") in met  # Ari is refused at the closed door
    assert ("open-door", True, (), "laboratory-door") in met  # then the door opens
    assert "rules" not in export_from_rows(rows, validate_bundle(bundle), Path("/nope"))  # no causal model, no overlay


@pytest.mark.req("scene-viewer/rules-overlay")
def test_the_public_map_is_the_smallest_that_holds_the_rooms_used():
    three = scene_layout.public_layout(BUNDLE["layout"])
    assert three["map"] == "public-hub-3" and all("sprite" not in p for p in three["people"].values())
    wide = deepcopy(BUNDLE["layout"]); wide["rooms"]["control-room"] = "d"
    assert scene_layout.public_layout(wide)["map"] == "public-hub-5"


@pytest.mark.req("scene-viewer/rules-overlay")
def test_the_published_demo_replays_are_what_the_builder_script_makes():
    import subprocess
    before = {n: (ROOT / f"viewer/smallville/replay-{n}.json").read_bytes() for n in ("public", "resident")}
    subprocess.run([sys.executable, str(ROOT / "scripts/build_public_demos.py")], check=True, capture_output=True)
    assert before == {n: (ROOT / f"viewer/smallville/replay-{n}.json").read_bytes() for n in ("public", "resident")}
    assert "(words not shown)" in before["resident"].decode() and "Is the pump ready" not in before["resident"].decode()


class _Reply:
    def __init__(self, content):
        self.content = content


def _fake_llm(monkeypatch, replies):
    import types
    calls = []

    def call_llm(model, messages, **kw):
        calls.append(messages)
        return _Reply(replies[min(len(calls) - 1, len(replies) - 1)])
    module = types.SimpleNamespace(call_llm=call_llm, safe_json_loads=json.loads)
    monkeypatch.setitem(sys.modules, "llm_client", module)
    return calls


def _bundle_without_layout():
    bundle = deepcopy(BUNDLE)
    bundle.pop("layout")
    return bundle


@pytest.mark.req("scene-viewer/builder-proposes-layout")
def test_a_valid_proposed_layout_is_attached(monkeypatch):
    from scripts.layout_proposal import propose_layout
    layout = {"version": 1, "map": "public-hub-3", "rooms": {"laboratory": "a", "corridor": "hub", "control-room": "b"},
              "doors": {"d1": {"between": ["laboratory", "corridor"], "halves": []}, "d2": {"between": ["corridor", "control-room"], "halves": []}},
              "people": {"ari": {"start": "corridor"}}}
    _fake_llm(monkeypatch, [json.dumps({"layout": layout})])
    out = propose_layout(_bundle_without_layout(), trace_id="t")
    assert out["layout"] == layout and "layout" not in _bundle_without_layout()


@pytest.mark.req("scene-viewer/builder-proposes-layout")
def test_a_world_with_no_places_gets_no_layout_and_a_bad_layout_is_repaired_once_then_dropped(monkeypatch):
    from scripts.layout_proposal import propose_layout
    _fake_llm(monkeypatch, [json.dumps({"layout": None})])
    assert propose_layout(_bundle_without_layout(), trace_id="t") is None
    calls = _fake_llm(monkeypatch, [json.dumps({"layout": {"version": 1, "map": "nowhere", "rooms": {}, "doors": {}, "people": {}}})])
    assert propose_layout(_bundle_without_layout(), trace_id="t") is None
    assert len(calls) == 2 and "rejected" in calls[1][-1]["content"]  # one repair, with the validator's reason


@pytest.mark.req("scene-viewer/builder-proposes-layout")
def test_the_build_step_never_fails_the_build_and_has_its_own_allowance(monkeypatch, capsys):
    from scripts import layout_proposal, world_builder_service as service
    bundle = _bundle_without_layout()
    monkeypatch.setattr(service, "_trace_cost", lambda trace_id: 0.0)
    _fake_llm(monkeypatch, ["not json at all"])
    assert service._with_layout(bundle, "t", 0.2) == bundle  # unparseable reply: world kept as built
    assert "layout step" in capsys.readouterr().err  # and the skip is logged, not hidden
    assert service._with_layout(deepcopy(BUNDLE), "t", 0.2) == BUNDLE  # already has a layout: left alone
    seen = {}
    monkeypatch.setattr(service, "_trace_cost", lambda trace_id: 0.199)  # the build used nearly all of its budget
    monkeypatch.setattr(layout_proposal, "propose_layout", lambda b, **kw: seen.update(kw) or None)
    service._with_layout(bundle, "t", 0.2)
    assert seen["max_budget"] == pytest.approx(0.199 + layout_proposal.MAX_BUDGET)  # its own allowance on top


@pytest.mark.req("scene-viewer/builder-proposes-layout")
def test_a_doorway_with_no_halves_is_always_open_in_the_replay():
    from scripts.export_smallville_replay import export_from_rows
    bundle = deepcopy(BUNDLE)
    bundle["layout"] = scene_layout.public_layout(bundle["layout"])
    for door in bundle["layout"]["doors"].values():
        door["halves"] = []
    rows = [json.loads(line) for line in (ROOT / "evidence/ui/inhabited-facility-20261113/scripted-run-log.jsonl").read_text().splitlines() if line.strip()]
    replay = export_from_rows(rows, validate_bundle(bundle), Path("/nope"))
    assert {c["state"] for c in replay["door_changes"] if c["step"] == 0} == {"open"}
