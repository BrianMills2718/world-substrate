#!/usr/bin/env python3
"""Generate or verify the complete M1 freshwater evidence pair."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scripts._display import display_path

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
    accepted = payload.get("accepted") is True
    result = (
        "PASS — the scripted neutral freshwater journey and all three "
        "discriminating negative paths are accepted."
        if accepted
        else "FAIL — the executable freshwater probe rejected this evidence."
    )
    lines = [
        "# M1 freshwater review",
        "",
        f"**Result:** {result}",
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


def evidence_outputs(payload: dict[str, object]) -> tuple[bytes, bytes]:
    """Encode only accepted evidence so a failing probe cannot become canonical."""
    if payload.get("accepted") is not True:
        raise ValueError("freshwater executable probe did not accept the evidence")
    return encoded(payload), render_markdown(payload)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = run_freshwater_probe(REPO)
    try:
        expected_json, expected_markdown = evidence_outputs(payload)
    except ValueError as error:
        print(str(error), file=sys.stderr)
        return 1
    if args.check:
        drift = []
        if not JSON_OUTPUT.exists() or JSON_OUTPUT.read_bytes() != expected_json:
            drift.append(display_path(JSON_OUTPUT, REPO))
        if (
            not MARKDOWN_OUTPUT.exists()
            or MARKDOWN_OUTPUT.read_bytes() != expected_markdown
        ):
            drift.append(display_path(MARKDOWN_OUTPUT, REPO))
        if drift:
            print("freshwater evidence drift: " + ", ".join(map(str, drift)), file=sys.stderr)
            return 1
        print("freshwater machine and human evidence match the executable probe")
        return 0
    JSON_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    JSON_OUTPUT.write_bytes(expected_json)
    MARKDOWN_OUTPUT.write_bytes(expected_markdown)
    print(f"wrote {display_path(JSON_OUTPUT, REPO)}")
    print(f"wrote {display_path(MARKDOWN_OUTPUT, REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
