#!/usr/bin/env python3
"""C5: render a run's recorded Engine events with the World Builder's existing automatic replay.

Converts one run folder (attempts.jsonl + ticks.json + summary.json) into the World Builder trace
format (world-substrate-contested-run/v3) and calls scripts.run_authored_world.render_run, which
bootstraps a scene profile from the world itself (no hand-authored scene). Rules written mid-run are
included via bundle_after_run.json / causal_after_run.json. Writes frames.html next to the run.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
sys.path[:0] = [str(REPO), str(REPO / "src")]

from scripts.run_authored_world import render_run  # noqa: E402
from world_substrate.action_authoring import CausalModel  # noqa: E402


def to_trace(run_dir: Path, bundle: dict[str, Any]) -> dict[str, Any]:
    summary = json.loads((run_dir / "summary.json").read_text())
    attempts = [json.loads(line) for line in (run_dir / "attempts.jsonl").read_text().splitlines() if line.strip()]
    if (run_dir / "ticks.json").exists():
        ticks = {row["tick"]: row for row in json.loads((run_dir / "ticks.json").read_text())}
    else:  # derive rounds from the recorded Engine events
        evs = [json.loads(x) for x in (run_dir / "events.jsonl").read_text().splitlines() if x.strip()]
        ticks = {t: {"tick": t, "world_changes": []} for t in range(summary["final_tick"])}
        for ev in evs:
            t = int(ev.get("tick") or 0)
            t -= 1  # process events carry the next tick number (clock first)
            if t in ticks and ev.get("causal_bearer", {}).get("kind") == "process" and ev["rule_id"] != "system.clock.advance":
                ticks[t]["world_changes"].append(ev["rule_id"])
    actors = sorted({a["actor"] for a in attempts}) or [e["id"] for e in bundle["entities"] if "actor" in e.get("categories", [])]
    transcript = []
    for tick in sorted(ticks):
        rows = {}
        for a in [x for x in attempts if x["tick"] == tick]:
            perf = a.get("performed") or {}
            did = perf.get("action_record")
            if not did and a.get("decision") == "unlisted":  # show the off-menu attempt, not "wait"
                kind = perf.get("action_kind") or ("gm-ruling" if perf.get("status") == "ruling" else "unlisted")
                did = {"actor": a["actor"], "kind": kind}
            rows[a["actor"]] = {
                "wanted": did, "did": did, "status": perf.get("status") if did else "no_action",
                "retried": False, "said": a.get("belief"), "refused_because": [],
                "lost_what_it_wanted": False, "changed": perf.get("status") == "accepted", "blocked_by_rules": [],
                "written_mid_run": bool(perf.get("written_mid_run")),
            }
        for actor in actors:
            rows.setdefault(actor, {"wanted": None, "did": None, "status": "no_action", "retried": False,
                                    "said": None, "refused_because": [], "lost_what_it_wanted": False,
                                    "changed": False, "blocked_by_rules": []})
        transcript.append({"turn": tick + 1, "world_changes": ticks[tick]["world_changes"],
                           "revision_when_decided": None, "committed_first": actors[0], "actors": rows,
                           "progress": {}})
    return {"schema_version": "world-substrate-contested-run/v3", "world": bundle["world"]["id"], "actors": actors,
            "model": "llm-resident (Concordia)", "cost_usd": summary.get("cost"),
            "mechanic_profile_id": summary.get("profile_id"),
            "summary": {"turns": len(transcript), "terminal_reached": summary.get("ended") == "terminal"},
            "transcript": transcript}


def state_rounds(run_dir: Path, bundle: dict[str, Any], rounds: int) -> list[dict[str, Any]]:
    """Per round: committed Engine events (id, rule, status, changes) and every entity's fields after the round,
    replayed only from the run's recorded events (events.jsonl)."""
    labels = {e["id"]: e.get("label", e["id"]) for e in bundle["entities"]}
    state = {e["id"]: {f"{k}": v for c in (e.get("components") or {}).values() if isinstance(c, dict) for k, v in c.items()}
             for e in bundle["entities"]}
    events = [json.loads(x) for x in (run_dir / "events.jsonl").read_text().splitlines() if x.strip()]
    by_tick: dict[int, list[dict[str, Any]]] = {}
    for ev in events:  # the clock runs first in each advance, so process events carry the next tick number
        t = int(ev.get("tick") or 0)
        if (ev.get("causal_bearer") or {}).get("kind") == "process":
            t -= 1
        by_tick.setdefault(t, []).append(ev)
    out = []
    for t in range(rounds):
        rows = []
        for ev in by_tick.get(t, []):
            if ev.get("rule_id") == "system.clock.advance":
                continue
            changes = []
            for c in ev.get("changes", []):
                parts = c["path"].split(".")
                if len(parts) >= 5 and parts[0] == "entities" and parts[2] == "components":
                    state[parts[1]][parts[4]] = c["after"]
                    changes.append(f"{labels.get(parts[1], parts[1])}.{parts[4]}: {c['before']} → {c['after']}")
            rows.append({"event_id": ev["event_id"], "rule": ev.get("rule_id"), "status": ev.get("status"),
                         "changes": changes})
        out.append({"events": rows, "state": {labels[k]: dict(v) for k, v in state.items()}})
    return out


def add_state_panel(html: str, run_dir: Path, bundle: dict[str, Any], trace: dict[str, Any]) -> str:
    data = json.dumps(state_rounds(run_dir, bundle, len(trace["transcript"])))
    panel = """
<style>#ws-state{max-width:1200px;margin:12px auto;background:#fff;color:#222;border-radius:10px;padding:12px 16px;
font:13px/1.45 system-ui,sans-serif}#ws-state h3{margin:4px 0 6px;font-size:14px}#ws-state code{font-size:12px}
#ws-state table{border-collapse:collapse}#ws-state td{padding:1px 10px 1px 0;vertical-align:top}</style>
<div id="ws-state"><h3>Engine events this round</h3><div id="ws-ev"></div><h3>State after this round</h3><div id="ws-st"></div></div>
<script>const WS_STATE=__DATA__;(function(){const orig=window.render;window.render=function(i){orig(i);
const r=WS_STATE[i]||{events:[],state:{}};document.getElementById('ws-ev').innerHTML=r.events.length?r.events.map(e=>
'<div><code>'+e.event_id+'</code> '+e.rule+' <b>'+e.status+'</b>'+(e.changes.length?': '+e.changes.join('; '):'')+'</div>').join(''):'<i>none</i>';
document.getElementById('ws-st').innerHTML='<table>'+Object.entries(r.state).map(([k,v])=>'<tr><td><b>'+k+'</b></td><td>'+
Object.entries(v).map(([f,x])=>f+'='+(typeof x==='number'?Math.round(x*100)/100:x)).join(', ')+'</td></tr>').join('')+'</table>';};
window.render(typeof idx==='number'?idx:0);})();</script>
""".replace("__DATA__", data)
    return html.replace("</body>", panel + "</body>")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_dir", type=Path)
    args = ap.parse_args()
    run_dir = args.run_dir
    model_dir = run_dir.parent
    bpath = run_dir / "bundle_after_run.json"
    cpath = run_dir / "causal_after_run.json"
    bundle = json.loads((bpath if bpath.exists() else model_dir / "bundle.json").read_text())
    causal = json.loads((cpath if cpath.exists() else model_dir / "causal.json").read_text())
    causal.pop("review", None)
    summary = json.loads((run_dir / "summary.json").read_text())
    for cond in summary.get("conditions_changed", []):  # initial state as the run actually started
        eid, comp, field = cond["field"].split(".")
        next(e for e in bundle["entities"] if e["id"] == eid)["components"][comp][field] = cond["to"]
    trace = to_trace(run_dir, bundle)
    (run_dir / "trace.json").write_text(json.dumps(trace, indent=2))
    html = render_run(bundle, trace, CausalModel.from_dict(causal, bundle=bundle))
    html = add_state_panel(html, run_dir, bundle, trace)
    (run_dir / "frames.html").write_text(html)
    print(f"[done] {run_dir / 'frames.html'} turns={len(trace['transcript'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
