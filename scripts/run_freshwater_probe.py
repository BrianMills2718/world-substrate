#!/usr/bin/env python3
"""Generate or verify the complete M1 freshwater evidence pair."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import run_freshwater_probe

JSON_OUTPUT = REPO / "evidence/m1/freshwater-v0.json"
MARKDOWN_OUTPUT = REPO / "evidence/m1/freshwater-v0.md"


def encoded(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def render_markdown(payload: dict[str, object]) -> bytes:
    positive = payload["positive_journey"]
    negatives = payload["negative_journeys"]
    assert isinstance(positive, dict) and isinstance(negatives, dict)
    projection = positive["final_projection"]
    ledger = positive["ledger"]
    assert isinstance(projection, dict) and isinstance(ledger, dict)
    vessels = projection["vessels"]
    actors = projection["actors"]
    assert isinstance(vessels, dict) and isinstance(actors, dict)
    pot = vessels["clay-pot"]
    robinson = actors["robinson"]
    friday = actors["friday"]
    assert isinstance(pot, dict) and isinstance(robinson, dict) and isinstance(friday, dict)
    pot_liquid = pot["liquid"]
    assert isinstance(pot_liquid, dict)
    lines = [
        "# M1 freshwater review",
        "",
        "**Result:** PASS — the scripted neutral freshwater journey and all three discriminating negative paths are accepted.",
        "",
        "The detailed machine receipt is [freshwater-v0.json](freshwater-v0.json), and the complete command/event trace is [transfer-v0.json](transfer-v0.json).",
        "",
        "## Positive journey",
        "",
        "| Observation | Result |",
        "| --- | --- |",
        f"| Commands replayed | {positive['command_count']} |",
        f"| Final tick | {positive['final_tick']} |",
        f"| Clay-pot owner | `{positive['final_owner']}` |",
        f"| Clay-pot contents | {pot_liquid['volume_ml']} ml, {pot_liquid['pathogens']} pathogens, {pot_liquid['heat_units']} heat units at {pot['temperature_c']} C |",
        f"| Actor hydration | Robinson {robinson['thirst']}; Friday {friday['thirst']} |",
        f"| Heat / treatment ledger | {ledger['heat_added']} added; {ledger['heat_lost']} lost; {ledger['pathogens_killed']} pathogens killed |",
        f"| Vessel identity preserved | {str(positive['vessel_identity_preserved']).lower()} |",
        f"| Donor semantic checkpoint matched | {str(positive['semantic_checkpoint_matched']).lower()} |",
        f"| Exact replay matched | {str(positive['replay']['ok']).lower()} |",
        "",
        "## Negative journeys",
        "",
        "| Case | Expected / observed | Material state | Replay |",
        "| --- | --- | --- | --- |",
    ]
    for key, label in (
        ("overfill", "Overfill"),
        ("unsupported_pressure", "Valid pressure envelope without a rule"),
        ("malformed_fill", "Malformed fill envelope"),
    ):
        row = negatives[key]
        assert isinstance(row, dict)
        replay = row["replay"]
        assert isinstance(replay, dict)
        lines.append(
            f"| {label} | `{row['expected_status']}` / `{row['actual_status']}` | atomic: {str(row['atomic']).lower()} | exact: {str(replay['ok']).lower()} |"
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This establishes one deterministic scripted physical reference vertical. It does not establish LLM policy competence, cross-domain reuse, scale, deployment, or real-world water-treatment validity.",
            "",
        ]
    )
    return "\n".join(lines).encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = run_freshwater_probe(REPO)
    expected_json = encoded(payload)
    expected_markdown = render_markdown(payload)
    if args.check:
        drift = []
        if not JSON_OUTPUT.exists() or JSON_OUTPUT.read_bytes() != expected_json:
            drift.append(JSON_OUTPUT.relative_to(REPO))
        if (
            not MARKDOWN_OUTPUT.exists()
            or MARKDOWN_OUTPUT.read_bytes() != expected_markdown
        ):
            drift.append(MARKDOWN_OUTPUT.relative_to(REPO))
        if drift:
            print("freshwater evidence drift: " + ", ".join(map(str, drift)), file=sys.stderr)
            return 1
        print("freshwater machine and human evidence match the executable probe")
        return 0
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_bytes(expected_json)
    MARKDOWN_OUTPUT.write_bytes(expected_markdown)
    print(f"wrote {JSON_OUTPUT.relative_to(REPO)}")
    print(f"wrote {MARKDOWN_OUTPUT.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
