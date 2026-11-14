"""The whole system of a world as one graph, plus what each round lit up in it.

Implements: scene-viewer/world-graph

A port of `worldNetwork` and `roundTouched` from scripts/world_builder_home.html, so the same graph can be drawn by
the room-map viewer: alone for a world with no layout (Waltzman), and over the map for a world that has one.
Boxes are who and what exists (kind actor, place, thing), each move the rules allow (action) and each change the
world makes by itself (process). Links are only labels and ids: no message words, so the graph is safe to serve
wherever the shared run already is.
"""
from __future__ import annotations

from typing import Any


def _words(text: Any) -> str:
    import re
    return re.sub(r"[-_]+", " ", str(text))


def world_graph(bundle: dict[str, Any], causal: dict[str, Any] | None) -> dict[str, Any]:
    """Every entity, move and by-itself change of the world, with the links between them."""
    entities = bundle.get("entities") or []
    ids = {e["id"] for e in entities}
    nodes: list[dict[str, str]] = []
    edges: list[dict[str, str]] = []
    seen: set[str] = set()

    def node(node_id: str, label: str, kind: str) -> None:
        if node_id not in seen:
            seen.add(node_id)
            nodes.append({"id": node_id, "label": label, "kind": kind})

    def link(source: str, target: str, label: str) -> None:
        edge_id = f"{source}>{target}:{label}"
        if source != target and edge_id not in seen:
            seen.add(edge_id)
            edges.append({"id": edge_id, "source": source, "target": target, "label": label})

    def picks(selector: dict[str, Any] | None) -> list[dict[str, Any]]:
        # A selector that names nothing would link a rule to everything; leave those links out.
        if not selector or not ((selector.get("categories") or []) or (selector.get("components") or [])):
            return []
        return [e for e in entities
                if all(c in (e.get("categories") or []) for c in selector.get("categories") or [])
                and all(c in (e.get("components") or {}) for c in selector.get("components") or [])]

    mechanics = (causal or {}).get("mechanics") or []
    acting = {e["id"] for m in mechanics for e in picks(m.get("actor_selector"))}
    for e in entities:
        cats = e.get("categories") or []
        kind = "actor" if e["id"] in acting or "actor" in cats else "place" if "place" in cats else "thing"
        node("e:" + e["id"], e.get("label") or e["id"], kind)
    for e in entities:
        if e.get("location") in ids:
            link("e:" + e["id"], "e:" + e["location"], "is in")
        owner = str(e.get("owner_ref") or "").split(":")[-1]
        if owner in ids and owner != e.get("location"):
            link("e:" + e["id"], "e:" + owner, "belongs to")
        for fields in (e.get("components") or {}).values():
            for name, value in (fields or {}).items():
                if isinstance(value, str) and value in ids:
                    link("e:" + e["id"], "e:" + value, _words(name))
    for m in mechanics:
        action = "a:" + m["action_kind"]
        node(action, _words(m["action_kind"]), "action")
        for e in picks(m.get("actor_selector")):
            link("e:" + e["id"], action, "can")
        for role, selector in (m.get("participants") or {}).items():
            for e in picks(selector):
                link(action, "e:" + e["id"], _words(role))
    for p in (causal or {}).get("processes") or []:
        process = "p:" + p["process_id"]
        node(process, _words(p["process_id"]), "process")
        for e in picks(p.get("selector")):
            link(process, "e:" + e["id"], "changes")
    return {"nodes": nodes, "edges": edges}


def _entity_of(path: str | None) -> str | None:
    import re
    found = re.match(r"^entities\.([^.]+)\.", path or "")
    return "e:" + found.group(1) if found else None


def round_lit(turn: dict[str, Any]) -> dict[str, Any]:
    """What one round did: each try (who, which move, what it used, allowed or refused and why), and which
    by-itself changes fired. `touched` lists every box and link the round lit."""
    tries: list[dict[str, Any]] = []
    touched: set[str] = set()
    for actor, row in (turn.get("actors") or {}).items():
        move = row.get("did") or row.get("wanted")
        status = row.get("status") or "no_action"
        entry: dict[str, Any] = {"actor": "e:" + actor, "status": status, "because": list(row.get("refused_because") or []),
                                 "move": None, "uses": [], "changed": []}
        touched.add(entry["actor"])
        if isinstance(move, dict) and status != "unsupported_action":
            entry["move"] = "a:" + str(move.get("kind"))
            touched.add(entry["move"])
            for key, value in move.items():
                if key not in ("kind", "actor", "base_revision", "controller") and isinstance(value, str):
                    entry["uses"].append("e:" + value)
        elif isinstance(move, dict):
            entry["nearest"] = move.get("nearest_kind")
            entry["why"] = move.get("why")
        if status == "accepted":
            for change in row.get("changes") or []:
                changed = _entity_of(change.get("path"))
                if changed and changed not in entry["changed"]:
                    entry["changed"].append(changed)
        tries.append(entry)
    world_changed: list[str] = []
    for event in [*(turn.get("world_events") or []), *(turn.get("reactions") or [])]:
        for change in event.get("changes") or []:
            changed = _entity_of(change.get("path"))
            if changed and changed not in world_changed:
                world_changed.append(changed)
    fired = list(dict.fromkeys(["p:" + str(r) for r in turn.get("world_changes") or []]
                                + ["p:" + str(e["rule_id"]) for e in turn.get("world_events") or [] if e.get("rule_id")]))
    return {"turn": turn.get("turn"), "tries": tries, "fired": fired, "world_changed": world_changed}


def graph_replay(bundle: dict[str, Any], causal: dict[str, Any] | None, rounds: list[dict[str, Any]],
                 title: str = "") -> dict[str, Any]:
    """The payload the graph page draws: the whole graph once, and what each round lit up in it."""
    graph = world_graph(bundle, causal)
    kinds = {n["id"] for n in graph["nodes"]}
    lit = [round_lit(r) for r in rounds]
    for entry in lit:  # a move or box the graph does not know is dropped, never invented
        for t in entry["tries"]:
            if t["move"] not in kinds:
                t["move"] = None
            t["uses"] = [u for u in t["uses"] if u in kinds]
            t["changed"] = [c for c in t["changed"] if c in kinds]
        entry["fired"] = [f for f in entry["fired"] if f in kinds]
        entry["world_changed"] = [c for c in entry["world_changed"] if c in kinds]
    return {"title": title or (bundle.get("world") or {}).get("label") or "", "graph": graph, "rounds": lit}
