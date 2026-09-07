#!/usr/bin/env python3
"""Render a retained kitchen service trace as a self-explanatory flagship view.

This is a detachable analytic/presentation surface. It reads a persisted v3
contested-run trace and never imports or mutates the engine. Order progress is
read directly from the trace. Holdings and knife ownership are reconstructed
from accepted `take` / `put_down` actions because those are the kitchen actions
that change ownership.
"""

from __future__ import annotations

import argparse
import html
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class TurnView:
    turn: int
    actors: dict[str, dict[str, Any]]
    progress: dict[str, dict[str, Any]]
    holdings: dict[str, tuple[str, ...]]
    knife_owner: str | None
    moments: tuple[str, ...]
    committed_first: str


def load_trace(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if value.get("schema_version") != "world-substrate-contested-run/v3":
        raise ValueError("flagship renderer requires a v3 contested-run trace")
    if value.get("world") != "kitchen":
        raise ValueError("flagship renderer requires a kitchen trace")
    actors = value.get("actors")
    if not isinstance(actors, list) or len(actors) != 2 or any(
        not isinstance(actor, str) or not actor for actor in actors
    ):
        raise ValueError("kitchen trace must name exactly two actors")
    transcript = value.get("transcript")
    if not isinstance(transcript, list) or not transcript:
        raise ValueError("kitchen trace must contain a transcript")
    return value


def _commit_order(turn: dict[str, Any], actors: list[str]) -> list[str]:
    first = turn.get("committed_first")
    if first not in actors:
        raise ValueError(f"turn {turn.get('turn')} has invalid committed_first")
    return [first, *[actor for actor in actors if actor != first]]


def reconstruct_turns(trace: dict[str, Any]) -> list[TurnView]:
    """Reconstruct presentation-only ownership state from committed actions."""
    actors = list(trace["actors"])
    holders: dict[str, str] = {}
    last_knife_releaser: str | None = None
    rows: list[TurnView] = []

    for raw in trace["transcript"]:
        turn_number = raw.get("turn")
        if type(turn_number) is not int:
            raise ValueError("each transcript row needs an integer turn")
        records = raw.get("actors")
        progress = raw.get("progress")
        if not isinstance(records, dict) or not isinstance(progress, dict):
            raise ValueError(f"turn {turn_number} lacks actors/progress")

        moments: list[str] = []
        if any(
            isinstance(records.get(actor), dict)
            and records[actor].get("retried")
            and records[actor].get("plan_still_available") is False
            for actor in actors
        ):
            moments.append("contention")

        for actor in _commit_order(raw, actors):
            record = records.get(actor) or {}
            action = record.get("did")
            if record.get("status") != "accepted" or not isinstance(action, dict):
                continue
            kind = action.get("kind")
            item = action.get("item")
            if not isinstance(item, str):
                continue
            if kind == "take":
                holders[item] = actor
                if item == "knife" and last_knife_releaser not in (None, actor):
                    moments.append("takeover")
            elif kind == "put_down":
                holders.pop(item, None)
                if item == "knife":
                    actor_progress = progress.get(actor) or {}
                    if actor_progress.get("filled") is True:
                        moments.append("handoff")
                        last_knife_releaser = actor

        if all((progress.get(actor) or {}).get("filled") is True for actor in actors):
            moments.append("terminal")

        holdings = {
            actor: tuple(sorted(item for item, holder in holders.items() if holder == actor))
            for actor in actors
        }
        rows.append(
            TurnView(
                turn=turn_number,
                actors={actor: dict(records.get(actor) or {}) for actor in actors},
                progress={actor: dict(progress.get(actor) or {}) for actor in actors},
                holdings=holdings,
                knife_owner=holders.get("knife"),
                moments=tuple(dict.fromkeys(moments)),
                committed_first=str(raw["committed_first"]),
            )
        )
    return rows


def action_label(action: object) -> str:
    if not isinstance(action, dict):
        return "wait"
    kind = str(action.get("kind", "act")).replace("_", " ")
    item = action.get("item") or action.get("vessel") or action.get("order")
    label = kind if item is None else f"{kind} {item}"
    if action.get("burner"):
        label += f" on {action['burner']}"
    if action.get("order") and action.get("kind") != "plate":
        label += f" for {action['order']}"
    return label


def _esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def _chips(items: list[str] | tuple[str, ...], empty: str = "none") -> str:
    if not items:
        return f"<span class='muted'>{_esc(empty)}</span>"
    return "".join(f"<span class='chip'>{_esc(item)}</span>" for item in items)


def _actor_card(actor: str, record: dict[str, Any]) -> str:
    status = record.get("status", "unknown")
    wanted = record.get("wanted")
    did = record.get("did")
    reasoning = record.get("said") or ""
    retry_reasoning = record.get("said_on_retry")

    if record.get("retried"):
        action_html = (
            f"<div class='intent'><span>initial intent</span><b>{_esc(action_label(wanted))}</b></div>"
            f"<div class='commit'><span>after world changed</span><b>{_esc(action_label(did))}</b></div>"
        )
    else:
        action_html = f"<div class='commit'><span>{_esc(status)}</span><b>{_esc(action_label(did or wanted))}</b></div>"

    retry = ""
    if retry_reasoning:
        retry = f"<p class='retry'><b>On retry:</b> {_esc(retry_reasoning)}</p>"
    return (
        f"<section class='actor-card'><div class='actor-name'>{_esc(actor)}</div>"
        f"{action_html}<p class='reasoning'>{_esc(reasoning)}</p>{retry}</section>"
    )


def _order_progress(progress: dict[str, Any]) -> str:
    plated = list(progress.get("plated") or [])
    wants = list(progress.get("still_wants") or [])
    total = len(plated) + len(wants)
    filled = progress.get("filled") is True
    status = "complete" if filled else f"{len(plated)}/{total} plated"
    detail = (
        f"<div class='order-line'><b>{_esc(status)}</b></div>"
        f"<div class='mini-label'>plated</div>{_chips(plated)}"
        f"<div class='mini-label'>still needs</div>{_chips(wants, 'nothing')}"
    )
    return detail


def _moment_badges(moments: tuple[str, ...]) -> str:
    labels = {
        "contention": "contention",
        "handoff": "knife released for other cook",
        "takeover": "knife takeover",
        "terminal": "service complete",
    }
    return "".join(
        f"<span class='moment {name}'>{_esc(labels[name])}</span>"
        for name in moments
        if name in labels
    )


def _milestones(rows: list[TurnView], actors: list[str]) -> dict[str, Any]:
    completed: dict[str, int | None] = {actor: None for actor in actors}
    handoff = takeover = terminal = None
    for row in rows:
        for actor in actors:
            if completed[actor] is None and row.progress[actor].get("filled") is True:
                completed[actor] = row.turn
        if handoff is None and "handoff" in row.moments:
            handoff = row.turn
        if takeover is None and "takeover" in row.moments:
            takeover = row.turn
        if terminal is None and "terminal" in row.moments:
            terminal = row.turn
    return {
        "completed": completed,
        "handoff": handoff,
        "takeover": takeover,
        "terminal": terminal,
    }


def render_html(trace: dict[str, Any]) -> str:
    actors = list(trace["actors"])
    rows = reconstruct_turns(trace)
    milestones = _milestones(rows, actors)
    summary = trace.get("summary") or {}
    cost = trace.get("cost_usd")

    first_finisher = min(
        ((turn, actor) for actor, turn in milestones["completed"].items() if turn is not None),
        default=(None, "?"),
    )
    final_turn = milestones["terminal"] or len(rows)

    timeline: list[str] = []
    for row in rows:
        knife = row.knife_owner or "available"
        world = (
            "<section class='world-card'>"
            f"<div class='turn-line'><b>Turn {row.turn}</b><span>committed first: {_esc(row.committed_first)}</span></div>"
            f"<div class='badges'>{_moment_badges(row.moments)}</div>"
            f"<div class='knife'><span>knife</span><b>{_esc(knife)}</b></div>"
            f"<div class='holdings'><div><span>{_esc(actors[0])} holds</span>{_chips(row.holdings[actors[0]])}</div>"
            f"<div><span>{_esc(actors[1])} holds</span>{_chips(row.holdings[actors[1]])}</div></div>"
            f"<div class='orders'><div><span>{_esc(actors[0])} order</span>{_order_progress(row.progress[actors[0]])}</div>"
            f"<div><span>{_esc(actors[1])} order</span>{_order_progress(row.progress[actors[1]])}</div></div>"
            "</section>"
        )
        classes = "timeline-row " + " ".join(row.moments)
        timeline.append(
            f"<article class='{classes}' id='turn-{row.turn}'>"
            f"{_actor_card(actors[0], row.actors[actors[0]])}{world}{_actor_card(actors[1], row.actors[actors[1]])}"
            "</article>"
        )

    cost_text = f"${cost:.5f}" if isinstance(cost, (int, float)) else "not recorded"
    return f"""<!doctype html>
<html lang='en'>
<head>
<meta charset='utf-8'>
<meta name='viewport' content='width=device-width,initial-scale=1'>
<title>Kitchen service — two cooks, one knife</title>
<style>
:root{{--ink:#17202a;--muted:#66727d;--line:#dfe5e9;--paper:#f6f7f8;--card:#fff;--accent:#5b3fd0;--warm:#fff5df;--green:#eaf8ef;--red:#fff0ed;--blue:#eef5ff}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:15px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}}
main{{max-width:1320px;margin:auto;padding:32px 22px 64px}} h1{{font-size:clamp(32px,5vw,58px);line-height:1.02;margin:0;letter-spacing:-.035em}}
.kicker{{text-transform:uppercase;letter-spacing:.12em;font-size:12px;font-weight:700;color:var(--accent)}} .lede{{max-width:830px;font-size:18px;color:#44515d;margin:14px 0 22px}}
.metrics{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:24px 0}} .metric{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px 16px}}
.metric span,.mini-label,.holdings>div>span,.orders>div>span,.commit span,.intent span,.knife span{{display:block;color:var(--muted);font-size:11px;text-transform:uppercase;letter-spacing:.08em;font-weight:700}}
.metric b{{font-size:22px}} .context{{display:flex;gap:12px;flex-wrap:wrap;margin:0 0 28px;color:var(--muted)}} .context span{{background:white;border:1px solid var(--line);padding:6px 10px;border-radius:999px}}
.legend{{background:#fff;border:1px solid var(--line);border-radius:16px;padding:14px 16px;margin-bottom:16px}} .legend b{{margin-right:8px}}
.timeline-row{{display:grid;grid-template-columns:minmax(0,1fr) minmax(280px,.8fr) minmax(0,1fr);gap:10px;padding:10px 0;border-top:1px solid var(--line)}}
.actor-card,.world-card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:15px;min-width:0}} .actor-name{{font-weight:800;font-size:18px;margin-bottom:9px;text-transform:capitalize}}
.commit,.intent{{display:flex;align-items:baseline;justify-content:space-between;gap:10px;border-radius:10px;padding:8px 10px;background:var(--blue)}} .intent{{background:var(--red);margin-bottom:6px}} .commit b,.intent b{{text-align:right}}
.reasoning,.retry{{margin:10px 1px 0;color:#3f4a54}} .retry{{padding-top:8px;border-top:1px dashed var(--line);font-size:13px}} .turn-line{{display:flex;justify-content:space-between;gap:10px;align-items:baseline}} .turn-line span{{font-size:12px;color:var(--muted)}}
.badges{{min-height:28px;margin:8px 0}} .moment{{display:inline-block;font-size:11px;font-weight:800;padding:4px 7px;border-radius:999px;margin:0 5px 4px 0;text-transform:uppercase;letter-spacing:.045em;background:#eee}}
.moment.contention{{background:var(--red)}} .moment.handoff,.moment.takeover{{background:var(--warm)}} .moment.terminal{{background:var(--green)}}
.knife{{display:flex;justify-content:space-between;align-items:center;background:#f2efff;border-radius:10px;padding:9px 10px;margin-bottom:10px}} .knife b{{font-size:17px;text-transform:capitalize}}
.holdings,.orders{{display:grid;grid-template-columns:1fr 1fr;gap:8px}} .holdings>div,.orders>div{{border-top:1px solid var(--line);padding-top:8px;min-width:0}} .orders{{margin-top:9px}} .chip{{display:inline-block;background:#eef1f3;padding:3px 6px;border-radius:6px;margin:3px 3px 0 0;font-size:12px}} .muted{{color:#9aa3aa;font-size:12px}} .mini-label{{margin-top:5px}} .order-line b{{font-size:13px}}
.timeline-row.handoff .world-card{{border:2px solid #d49300;background:#fffdf7}} .timeline-row.takeover .world-card{{border:2px solid #8c6ae8}} .timeline-row.terminal .world-card{{border:2px solid #3c9b60;background:#fbfffc}}
.footer{{margin-top:28px;padding-top:18px;border-top:1px solid var(--line);color:var(--muted);font-size:13px}} code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
@media(max-width:900px){{.metrics{{grid-template-columns:1fr 1fr}} .timeline-row{{grid-template-columns:1fr}} .world-card{{order:-1}}}}
</style>
</head>
<body><main>
<div class='kicker'>World Substrate · retained causal trace</div>
<h1>Two cooks. One knife.<br>No communication.</h1>
<p class='lede'>Both cooks need the same bottleneck, cannot see each other's reasoning, and receive no instruction to cooperate. This view places each decision beside the shared world state so the handoff is visible rather than narrated.</p>
<section class='metrics'>
<div class='metric'><span>first order complete</span><b>{_esc(first_finisher[1])} · t{_esc(first_finisher[0])}</b></div>
<div class='metric'><span>knife released</span><b>t{_esc(milestones['handoff'])}</b></div>
<div class='metric'><span>other cook takes it</span><b>t{_esc(milestones['takeover'])}</b></div>
<div class='metric'><span>service complete</span><b>t{_esc(final_turn)}</b></div>
</section>
<div class='context'><span>model: {_esc(trace.get('model','unknown'))}</span><span>cost: {_esc(cost_text)}</span><span>actual contention: {_esc(summary.get('plan_actually_taken_by_the_other','?'))}</span><span>terminal: {_esc(summary.get('terminal_reached',False))}</span></div>
<div class='legend'><b>Read left → world → right.</b> The center column is reconstructed presentation state after the committed actions for that turn. Order progress comes directly from the retained trace. Highlighted rows mark genuine contention, the deliberate knife release, the takeover, and service completion.</div>
{''.join(timeline)}
<div class='footer'>This renderer is read-only. It consumes <code>world-substrate-contested-run/v3</code> evidence and cannot mutate canonical world state or reapply effects.</div>
</main></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    trace = load_trace(args.trace)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render_html(trace))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
