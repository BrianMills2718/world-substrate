#!/usr/bin/env python3
"""Copy the Smallville map and sprites the static viewer needs from a local clone of generative_agents.

Smallville's art is by paid artists and is for private use only (its README); this script keeps it out of the
repository: it writes into `viewer/smallville/assets/`, which is git-ignored. Usage:
    python3 scripts/setup_smallville_viewer.py ~/code2/generative_agents
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "viewer" / "smallville" / "assets"


def main() -> int:
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    static = Path(sys.argv[1]).expanduser() / "environment/frontend_server/static_dirs/assets"
    visuals = static / "the_ville/visuals"
    tile_map = json.loads((visuals / "the_ville_jan7.json").read_text())
    (OUT / "tiles").mkdir(parents=True, exist_ok=True)
    (OUT / "characters").mkdir(parents=True, exist_ok=True)
    shutil.copy(visuals / "the_ville_jan7.json", OUT / "map.json")
    for tileset in tile_map["tilesets"]:
        shutil.copy(visuals / tileset["image"], OUT / "tiles" / Path(tileset["image"]).name)
    for sprite in (static / "characters").iterdir():
        if sprite.is_file():
            shutil.copy(sprite, OUT / "characters" / sprite.name)
    print(f"copied {len(tile_map['tilesets'])} tilesets and the characters to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
