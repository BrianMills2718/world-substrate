#!/usr/bin/env python3
"""Generate or verify the retained neutral post-drink evidence."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))

from scripts._display import display_path

sys.path.insert(0, str(REPO / "src"))

from reference_worlds.castaway.probe import run_drink_probe

OUTPUT = REPO / "evidence/m1/drink-v0.json"


def encoded(payload: dict[str, object]) -> bytes:
    return (json.dumps(payload, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    payload = run_drink_probe(REPO)
    if payload.get("accepted") is not True:
        print("drink executable probe rejected the evidence", file=sys.stderr)
        return 1
    expected = encoded(payload)
    output = args.output.resolve()
    if args.check:
        if not output.exists() or output.read_bytes() != expected:
            print(f"drink evidence drift: {output}", file=sys.stderr)
            return 1
        print(f"drink evidence matches executable probe: {display_path(output, REPO)}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(expected)
    print(f"wrote {display_path(output, REPO)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
