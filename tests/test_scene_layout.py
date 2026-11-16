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


@pytest.mark.req("scene-viewer/a-layout-that-cannot-be-drawn-is-refused")
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


@pytest.mark.req("scene-viewer/the-same-story-on-a-second-map")
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


@pytest.mark.req("scene-viewer/a-run-log-is-enough")
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


@pytest.mark.req("scene-viewer/a-story-exports-and-draws-with-no-private-art")
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


@pytest.mark.req("scene-viewer/a-visitor-opens-a-share-link-s-room-map")
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


@pytest.mark.req("scene-viewer/a-world-with-nobody-to-draw-has-no-room-map")
def test_a_world_with_no_layout_and_no_actors_has_no_public_room_map():
    from scripts.world_builder_service import _public_replay
    share = _share_of_the_scripted_pump_run()
    del share["world"]["bundle"]["layout"]
    share["world"]["bundle"]["entities"] = [e for e in share["world"]["bundle"]["entities"] if "actor" not in (e.get("categories") or [])]
    with pytest.raises(scene_layout.LayoutError):
        _public_replay(share)


def _meeting_world():
    """A world with no places and no locations (like Waltzman's): three groups, a weekly meeting, two rounds."""
    bundle = {"entities": [{"id": g, "label": g.title(), "categories": ["actor"]} for g in ("alpha", "beta", "gamma")]
              + [{"id": "weekly", "label": "Weekly meeting", "categories": ["moment"]}], "actions": [], "world": {"label": "Meeting world"}}
    turn = lambda n, attends: {"turn": n, "actors": {
        "alpha": {"did": {"actor": "alpha", "kind": "discuss", "meeting": "weekly"}, "status": "accepted", "refused_because": []},
        "beta": {"did": {"actor": "beta", "kind": "communicate", "recipient": "gamma"}, "status": "accepted", "refused_because": []},
        "gamma": {"did": {"actor": "gamma", "kind": "discuss", "meeting": "weekly"} if attends else None, "status": "accepted" if attends else "no_action", "refused_because": []}}}
    return {"world": {"bundle": bundle, "causal_model": None}, "rounds": [turn(1, True), {"turn": 2, "actors": {n: {"did": None, "status": "no_action", "refused_because": []} for n in ("alpha", "beta", "gamma")}}]}


@pytest.mark.req("scene-viewer/every-world-has-a-map")
def test_a_world_with_no_places_gets_an_office_for_each_group_and_a_meeting_room():
    from scripts.world_builder_service import _public_replay
    replay = _public_replay(_meeting_world(), owner=True)
    assert replay["map"] == "public-offices-10"
    assert {r["label"] for r in replay["rooms"]} == {"Alpha", "Beta", "Gamma", "Meeting room"}
    assert replay["illustrative"]  # the page says the layout is drawn, not part of the world


@pytest.mark.req("scene-viewer/every-world-has-a-map")
def test_the_viewer_shows_the_note_that_a_drawn_layout_is_illustrative():
    assert 'id="note"' in (ROOT / "viewer/smallville/index.html").read_text()
    assert "R.illustrative" in (ROOT / "viewer/smallville/viewer.js").read_text()


@pytest.mark.req("scene-viewer/every-world-has-a-map")
def test_people_stay_in_their_offices_and_walk_to_the_meeting_room_only_for_a_meeting():
    from scripts.world_builder_service import _public_replay
    replay = _public_replay(_meeting_world(), owner=True)
    rooms = {r["label"]: r for r in replay["rooms"]}
    inside = lambda who, room: rooms[room]["x0"] <= who["movement"][0] <= rooms[room]["x1"] and rooms[room]["y0"] <= who["movement"][1] <= rooms[room]["y1"]
    first, last = replay["steps"]["0"], replay["steps"][str(len(replay["steps"]) - 1)]
    assert all(inside(first[n], n) for n in ("Alpha", "Beta", "Gamma"))
    mid = replay["steps"][str(replay["rounds"][0]["end"])]
    assert inside(mid["Alpha"], "Meeting room") and inside(mid["Gamma"], "Meeting room") and inside(mid["Beta"], "Beta")
    assert all(inside(last[n], n) for n in ("Alpha", "Beta", "Gamma"))  # round two: nobody attends, so everyone is back home


@pytest.mark.req("scene-viewer/every-world-has-a-map")
def test_a_message_to_another_group_shows_as_a_chat_line_and_its_words_are_withheld_from_visitors():
    from scripts.world_builder_service import _public_replay
    chats = lambda r: [c[1] for f in r["steps"].values() for who in f.values() for c in (who.get("chat") or [])]
    assert chats(_public_replay(_meeting_world(), owner=True)) and all("words not shown" in c for c in chats(_public_replay(_meeting_world())))


@pytest.mark.req("scene-viewer/every-world-has-a-map")
def test_the_office_map_connects_the_meeting_room_to_every_office_and_holds_ten():
    from scripts import export_smallville_replay as ex
    from scripts.generated_map import build
    prepared = scene_layout.prepared_maps()["public-offices-10"]
    maze = build("public-offices-10", list(prepared["slots"]))["maze"]
    assert len(prepared["sprites"]) == 10 and len(set(prepared["sprites"])) == 10
    for a, b in prepared["connections"]:
        start, goal = ex.anchor(maze, prepared["slots"][a]), ex.anchor(maze, prepared["slots"][b])
        assert len(ex.doorway(maze, [start] + ex.walk(maze, start, goal))) == 2
    assert all(len(ex.spots(maze, prepared["slots"][s], 10)) == 10 for s in prepared["slots"])  # every room has room for everyone


CAUSAL = json.loads((ROOT / "examples/world_authoring/pump-facility-causal-v0.json").read_text())


@pytest.mark.req("scene-viewer/a-refusal-shows-the-rule-that-caused-it")
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


@pytest.mark.req("scene-viewer/a-spatial-world-gets-a-layout")
def test_a_valid_proposed_layout_is_attached(monkeypatch):
    from scripts.layout_proposal import propose_layout
    layout = {"version": 1, "map": "public-hub-3", "rooms": {"laboratory": "a", "corridor": "hub", "control-room": "b"},
              "doors": {"d1": {"between": ["laboratory", "corridor"], "halves": []}, "d2": {"between": ["corridor", "control-room"], "halves": []}},
              "people": {"ari": {"start": "corridor"}}}
    _fake_llm(monkeypatch, [json.dumps({"layout": layout})])
    out = propose_layout(_bundle_without_layout(), trace_id="t")
    assert out["layout"] == layout and "layout" not in _bundle_without_layout()


@pytest.mark.req("scene-viewer/a-world-with-no-places-or-a-bad-layout-is-built-as-before")
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


@pytest.mark.req("scene-viewer/a-clinic-world-exports")
def test_a_builder_made_world_with_other_actions_exports_and_its_doors_open_when_walked_through():
    """The clinic (a live build on 2026-11-14, layout proposed by the Builder, run scripted and shared): actions the exporter was
    not written for ('check-in', 'unlock-lab-door', 'examine') still show, and a door nobody 'opens' opens when someone walks through."""
    from scripts.world_builder_service import _public_replay
    share = json.loads((ROOT / "tests/fixtures/clinic-share-20261114.json").read_text())
    replay = _public_replay(share)
    said = {f[w]["description"] for f in replay["steps"].values() for w in f}
    assert any(x.startswith("check in") for x in said) and any("examine" in x for x in said)
    assert replay["map"] == "public-hub-3" and len(replay["rules"]) >= 4
    opened = {c["door"] for c in replay["door_changes"] if c["state"] == "open"}
    assert "reception-exam-door" in opened  # Cho and Dr. Bell walk through it in round 1


# --- whole-system graph -------------------------------------------------------------------------------------------
from scripts.world_graph import graph_replay, world_graph  # noqa: E402

WALTZMAN = json.loads((ROOT / "tests/fixtures/waltzman-share-20261104.json").read_text())


@pytest.mark.req("scene-viewer/waltzman-graph-carries-every-box-and-the-round-s-tries")
def test_the_waltzman_graph_has_every_box_and_link_the_network_shows():
    graph = world_graph(WALTZMAN["world"]["bundle"], WALTZMAN["world"]["causal_model"])
    kinds = {}
    for n in graph["nodes"]:
        kinds[n["kind"]] = kinds.get(n["kind"], 0) + 1
    assert (len(graph["nodes"]), len(graph["edges"])) == (70, 411)
    assert kinds == {"actor": 10, "action": 17, "thing": 17, "process": 26}


@pytest.mark.req("scene-viewer/a-refusal-keeps-its-reason-and-no-words")
@pytest.mark.req("scene-viewer/waltzman-graph-carries-every-box-and-the-round-s-tries")
def test_a_round_lights_each_try_with_its_status_and_refusal_reason_and_no_words():
    replay = graph_replay(WALTZMAN["world"]["bundle"], WALTZMAN["world"]["causal_model"], WALTZMAN["rounds"])
    first = replay["rounds"][0]
    assert len(first["tries"]) == 10 and first["fired"]
    refused = [t for r in replay["rounds"] for t in r["tries"] if t["status"] == "precondition_failed"]
    assert refused and all(t["because"] for t in refused)
    ids = {n["id"] for n in replay["graph"]["nodes"]}
    assert all(t["actor"] in ids and (t["move"] is None or t["move"] in ids) and set(t["uses"]) <= ids
               for r in replay["rounds"] for t in r["tries"])
    assert "said" not in json.dumps(replay)


@pytest.mark.req("scene-viewer/the-replay-carries-the-graph")
def test_a_replay_carries_the_graph_and_which_person_each_graph_actor_is():
    replay = json.loads((ROOT / "viewer/smallville/replay-public.json").read_text())
    assert len(replay["graph"]["rounds"]) == len(replay["rounds"])
    assert set(replay["graph_actors"].values()) == set(replay["meta"]["persona_names"])
    refused = [t for r in replay["graph"]["rounds"] for t in r["tries"] if t["status"] == "precondition_failed"]
    assert refused and all(t["because"] for t in refused)
    assert "words" not in json.dumps(replay["graph"]).lower().replace("(words not shown)", "")


@pytest.mark.req("scene-viewer/the-pump-facility-shows-its-rooms-and-its-pump")
def test_rooms_are_named_off_the_doorways_and_the_pump_is_placed_clear_of_them():
    replay = json.loads((ROOT / "viewer/smallville/replay-public.json").read_text())
    assert {r["label"] for r in replay["rooms"]} == {"Laboratory", "Corridor", "Control room"}
    doors = [tuple(t) for d in replay["doors"].values() for t in d["tiles"]]
    for r in replay["rooms"]:
        assert not any(r["x0"] <= t[0] <= r["x1"] and t[1] == r["label_row"] for t in doors)
    (pump,) = replay["objects"]
    assert pump["room"] == "laboratory" and all(abs(pump["tile"][0] - d[0]) + abs(pump["tile"][1] - d[1]) > 3 for d in doors)


@pytest.mark.req("scene-viewer/the-viewer-wires-zoom-pan-and-reset")
def test_the_viewer_wires_wheel_zoom_drag_pan_and_a_reset_button_that_refit_the_map():
    js = (ROOT / "viewer/smallville/viewer.js").read_text()
    page = (ROOT / "viewer/smallville/index.html").read_text()
    assert 'id="reset"' in page and "Reset view" in page
    assert 'addEventListener("wheel"' in js and '"pointermove"' in js and '$("reset").onclick' in js
    assert "userZoom" in js and js.count("fitFn()") >= 2  # each refits the map, which redraws the graph


@pytest.mark.req("scene-viewer/the-viewer-wires-the-whole-network-mode")
def test_the_viewer_has_a_whole_network_mode_that_places_every_box_and_draws_every_link():
    js = (ROOT / "viewer/smallville/viewer.js").read_text()
    html = (ROOT / "viewer/smallville/index.html").read_text()
    assert "Whole network" in html and 'id="gmode"' in html
    assert "whole = gmode" in js and "GRAPH.graph.edges.forEach" in js and "onMap" in js


@pytest.mark.req("scene-viewer/the-viewer-offers-the-styles-and-opens-one-from-a-link")
def test_the_viewer_offers_graph_styles_and_opens_one_from_a_link():
    js = (ROOT / "viewer/smallville/viewer.js").read_text()
    html = (ROOT / "viewer/smallville/index.html").read_text()
    for v in ("round", "map", "hover", "beside"):
        assert f'<option value="{v}"' in html
    assert 'q.get("graph")' in js and "focusId" in js and "beside" in js


@pytest.mark.req("scene-viewer/every-world-has-a-map")
def test_the_old_graph_page_sends_visitors_to_the_graph_beside_the_room_map():
    html = (ROOT / "viewer/smallville/graph.html").read_text()
    assert 'q.set("graph", "beside")' in html and 'location.replace(url)' in html and "index.html" in html


@pytest.mark.req("scene-viewer/a-running-world-is-drawn-on-the-map-as-it-plays")
def test_a_live_replay_is_drawn_from_the_server_run_log_without_saving_and_withholds_words_from_visitors(monkeypatch):
    import scripts.world_builder_service as svc
    share = _meeting_world()
    seen = {}
    monkeypatch.setattr(svc, "_assemble_share", lambda build, runs: seen.update(build=build, runs=runs) or share)
    monkeypatch.setattr(svc, "_save_share", lambda *a, **k: pytest.fail("a live replay must not be saved"))
    build, run = (f"{svc.TRACE_ROOT}/{kind}/{'a' * 32}" for kind in ("build", "run"))
    body = {"build_trace_id": build, "run_trace_ids": [run]}
    chats = lambda r: [c[1] for f in r["steps"].values() for who in f.values() for c in (who.get("chat") or [])]
    visitor, owner = svc._live_replay(body, owner=False), svc._live_replay(body, owner=True)
    assert seen["runs"] == [run] and visitor["map"] == "public-offices-10"
    assert chats(owner) and all("words not shown" in c for c in chats(visitor))


@pytest.mark.req("scene-viewer/a-running-world-is-drawn-on-the-map-as-it-plays")
def test_a_live_replay_of_a_private_catalog_run_needs_the_owner(monkeypatch):
    import scripts.world_builder_service as svc
    with pytest.raises(PermissionError):
        svc._live_replay({"catalog_run_id": "x"}, owner=False)


@pytest.mark.req("scene-viewer/a-running-world-is-drawn-on-the-map-as-it-plays")
def test_the_viewer_in_embed_mode_takes_a_longer_replay_by_message_and_follows_the_newest_round():
    js = (ROOT / "viewer/smallville/viewer.js").read_text()
    assert "embed" in js and "ws-replay" in js and "ws-viewer-ready" in js and "followNewest" in js


@pytest.mark.req("scene-viewer/a-running-world-is-drawn-on-the-map-as-it-plays")
def test_the_run_stage_shows_the_room_map_and_no_longer_the_old_picture_or_network_panel():
    page = (ROOT / "scripts/world_builder_home.html").read_text()
    assert "room-map/?embed=1" in page and "/live-replay" in page
    assert 'id="picture-wrap"' not in page and 'id="network"' not in page
