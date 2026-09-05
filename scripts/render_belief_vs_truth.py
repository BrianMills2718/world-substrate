#!/usr/bin/env python3
"""Render a retained policy trace as belief against truth, turn by turn.

The interesting thing in this project's policy runs is not the score. It is
that a model states what it believes about the world, acts on it, and the world
computes consequences from its own state without consulting that belief. M5
produced this once by accident and the M5 re-run showed it regenerates.

Until now that only existed as JSON someone had to narrate. This puts the two
columns side by side.

Nothing here calls a model. The retained trace records each turn's chosen
action and the reasoning the model gave for it; the engine is deterministic, so
replaying those actions recovers the exact world state at every turn. Belief
comes from the trace, truth comes from the replay.
"""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import build_transfer_engine
from scripts._display import display_path
from world_substrate.mechanisms.liquid import DrinkRule

SAFE_TEMPERATURE_C = DrinkRule.safe_drinking_temperature_c

# Claims the model makes about the world, and the state that would refute each.
#
# Deliberately conservative and deliberately a heuristic: it reads the model's
# own words for an assertion about safety, and checks the vessel that assertion
# is about. It will miss a claim phrased in a way this does not match, and it
# is not a general belief extractor. It exists to point a reader at turns worth
# reading, not to score the model.
TREATED_CLAIM = re.compile(r"\b(already treated|treated|safe to drink|sterilized|purified)\b", re.IGNORECASE)
UNTREATED_CLAIM = re.compile(r"\b(untreated|unsafe|contaminat)\w*", re.IGNORECASE)
COOLED_CLAIM = re.compile(r"\b(cool(ed)?|cooled enough|safe (drinking )?temperature)\b", re.IGNORECASE)


def policy_turns(payload: dict) -> list[dict]:
    """The model-driven half of a comparison run, in order."""
    def walk(node):
        if isinstance(node, dict):
            if "turn" in node and "choice" in node:
                yield node
            for value in node.values():
                yield from walk(value)
        elif isinstance(node, list):
            for value in node:
                yield from walk(value)

    rows = list(walk(payload))
    # The scripted baseline's reasons are fixed strings; the model's are not.
    return [
        row
        for row in rows
        if not str(row["choice"].get("reasoning", "")).startswith(
            ("thirsty:", "nothing to drink")
        )
    ]


def world_facts(engine, vessel_id: str | None) -> dict:
    actor = engine.world.entities["robinson"]
    facts = {
        "health": actor.actor.health,
        "hydration": actor.actor.hydration,
        "tick": engine.world.tick,
    }
    if vessel_id and vessel_id in engine.world.entities:
        vessel = engine.world.entities[vessel_id]
        if vessel.liquid is not None:
            facts["vessel"] = vessel_id
            facts["volume_ml"] = vessel.liquid.volume_ml
            facts["pathogens"] = vessel.liquid.pathogens
        if vessel.thermal is not None:
            facts["temperature_c"] = round(vessel.thermal.temperature_c)
    return facts


def divergence(reasoning: str, facts: dict) -> str | None:
    """Where the model's stated belief contradicts the world it acted in."""
    if "pathogens" not in facts or facts.get("volume_ml", 0) <= 0:
        return None
    says_treated = TREATED_CLAIM.search(reasoning) and not UNTREATED_CLAIM.search(reasoning)
    if says_treated and facts["pathogens"] > 0:
        return (
            f"called it treated; {facts['vessel']} still carries "
            f"{facts['pathogens']} pathogens"
        )
    temperature = facts.get("temperature_c")
    if COOLED_CLAIM.search(reasoning) and temperature and temperature > SAFE_TEMPERATURE_C:
        return (
            f"called it cool enough; {facts['vessel']} is {temperature}C against a "
            f"{SAFE_TEMPERATURE_C}C safe limit"
        )
    return None


def replay(payload: dict) -> list[dict]:
    """Pair each turn's stated belief with the world state it acted on."""
    engine = build_transfer_engine(REPO)
    steps = []
    for row in policy_turns(payload):
        action = row["choice"].get("action") or {}
        reasoning = str(row["choice"].get("reasoning", "")).strip()
        vessel = action.get("vessel") or action.get("destination")
        before = world_facts(engine, vessel)
        status = "wait"
        if action:
            result = engine.submit({**action, "base_revision": engine.world.revision})
            status = result["status"]
        engine.advance(1)
        after = world_facts(engine, vessel)
        steps.append(
            {
                "turn": row["turn"],
                "action": action.get("kind", "wait"),
                "detail": {
                    k: v for k, v in action.items()
                    if k in ("vessel", "source", "destination", "target", "volume_ml")
                },
                "reasoning": reasoning,
                "status": status,
                "before": before,
                "after": after,
                "harm": before["health"] - after["health"],
                "divergence": divergence(reasoning, before),
            }
        )
    return steps


def as_text(steps: list[dict]) -> str:
    lines = []
    for s in steps:
        head = f"t{s['turn']:>2}  {s['action']}"
        if s["detail"]:
            head += " " + " ".join(f"{k}={v}" for k, v in sorted(s["detail"].items()))
        lines.append(head)
        lines.append(f"      believed : {s['reasoning'][:100]}")
        b = s["before"]
        truth = f"health {b['health']}"
        if "vessel" in b:
            truth += (
                f" | {b['vessel']} {b.get('volume_ml', 0)}ml "
                f"pathogens={b.get('pathogens', 0)} {b.get('temperature_c', '?')}C"
            )
        lines.append(f"      world was: {truth}")
        if s["harm"]:
            lines.append(f"      >>> cost {s['harm']} health")
        if s["divergence"]:
            lines.append(f"      >>> DIVERGED: {s['divergence']}")
        lines.append("")
    return "\n".join(lines)


def as_html(steps: list[dict], title: str, source: str) -> str:
    rows = []
    for s in steps:
        cls = "diverged" if s["divergence"] else ("harm" if s["harm"] else "")
        b = s["before"]
        truth = f"<b>health {b['health']}</b>"
        if "vessel" in b:
            treated = "treated" if b.get("pathogens", 0) == 0 else f"{b['pathogens']} pathogens"
            truth += (
                f"<br><span class=v>{html.escape(b['vessel'])}</span>: "
                f"{b.get('volume_ml', 0)}ml, {treated}, {b.get('temperature_c', '?')}&deg;C"
            )
        note = ""
        if s["divergence"]:
            note = f"<div class=note>&#9888; {html.escape(s['divergence'])}</div>"
        if s["harm"]:
            note += f"<div class=cost>cost {s['harm']} health</div>"
        detail = " ".join(f"{k}={v}" for k, v in sorted(s["detail"].items()))
        rows.append(
            f"<tr class='{cls}'><td class=t>t{s['turn']}</td>"
            f"<td class=a><b>{html.escape(s['action'])}</b><br>"
            f"<span class=d>{html.escape(detail)}</span></td>"
            f"<td class=say>{html.escape(s['reasoning'])}{note}</td>"
            f"<td class=truth>{truth}</td></tr>"
        )
    diverged = sum(1 for s in steps if s["divergence"])
    total_harm = sum(s["harm"] for s in steps if s["harm"] > 0)
    return f"""<!doctype html><meta charset=utf-8><title>{html.escape(title)}</title>
<style>
body{{font:15px/1.5 -apple-system,Segoe UI,sans-serif;margin:2rem auto;max-width:1000px;color:#1a1a1a}}
h1{{font-size:1.4rem;margin-bottom:.2rem}}
p.sub{{color:#555;margin-top:0}}
table{{border-collapse:collapse;width:100%;margin-top:1.2rem}}
td{{border-top:1px solid #e3e3e3;padding:.6rem .5rem;vertical-align:top}}
th{{text-align:left;padding:.4rem .5rem;font-size:.8rem;text-transform:uppercase;letter-spacing:.04em;color:#666}}
.t{{width:2.5rem;color:#888;font-variant-numeric:tabular-nums}}
.a{{width:9rem}} .d{{color:#777;font-size:.85rem}}
.say{{width:44%;color:#333}} .truth{{width:26%;font-size:.9rem}}
.v{{color:#666}}
tr.diverged{{background:#fff6f4}}
tr.harm{{background:#fffdf0}}
.note{{margin-top:.4rem;color:#a3301c;font-size:.88rem;font-weight:600}}
.cost{{margin-top:.25rem;color:#8a6d00;font-size:.88rem}}
.legend{{margin-top:1.5rem;font-size:.85rem;color:#666;border-top:1px solid #eee;padding-top:.8rem}}
</style>
<h1>{html.escape(title)}</h1>
<p class=sub>What the agent said it believed, beside what the world actually was.
{diverged} turn(s) where the two contradicted each other; {total_harm} health lost in total.</p>
<table><tr><th></th><th>did</th><th>said it believed</th><th>world actually was</th></tr>
{''.join(rows)}
</table>
<p class=legend>Belief is the model's own reasoning, recorded in
<code>{html.escape(source)}</code>. Truth is recovered by replaying the recorded
actions through the engine, which is deterministic &mdash; no model was called to
build this page. Divergence detection is a conservative keyword heuristic over the
model's words: it points at turns worth reading and is not a general belief
extractor, so it under-reports.</p>
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("--title", default="Belief against truth")
    parser.add_argument("--html", type=Path)
    args = parser.parse_args()

    payload = json.loads(args.trace.read_text())
    steps = replay(payload)
    print(as_text(steps))
    diverged = [s for s in steps if s["divergence"]]
    print(f"{len(steps)} turns, {len(diverged)} with a stated belief the world contradicted")
    if args.html:
        args.html.parent.mkdir(parents=True, exist_ok=True)
        args.html.write_text(
            as_html(steps, args.title, display_path(args.trace, REPO))
        )
        print(f"wrote {display_path(args.html, REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
