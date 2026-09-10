#!/usr/bin/env python3
"""Wrap multiple retained Living Scene branches in one self-contained player."""
from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "src"))

from scripts.render_living_scene import render_html
from world_substrate.living_scene import load_live_projection_bundle, load_scene_contract


def render_branching_html(
    bundles: dict[str, dict[str, Any]], profile: dict[str, Any], profile_dir: Path
) -> str:
    if not bundles:
        raise ValueError("branch player requires at least one retained branch")
    world_ids = {bundle.get("world_id") for bundle in bundles.values()}
    if world_ids != {profile.get("world")}:
        raise ValueError("all retained branches must match the Living Scene profile world")
    documents = {
        name: render_html(bundle, profile, profile_dir)
        for name, bundle in sorted(bundles.items())
    }
    docs_json = json.dumps(documents, separators=(",", ":")).replace("</", "<\\/")
    names = list(sorted(documents))
    options = "".join(
        f"<option value='{html.escape(name, quote=True)}'>{html.escape(name.replace('_', ' ').title())}</option>"
        for name in names
    )
    title = html.escape(str(profile.get("title") or profile.get("scene_id") or "Living Scene"))
    return f"""<!doctype html>
<html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>{title} · World Substrate</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;background:#0d151d;color:white;font:14px/1.4 system-ui,-apple-system,sans-serif}}.bar{{display:flex;align-items:center;gap:12px;padding:10px 16px;border-bottom:1px solid #ffffff20;position:sticky;top:0;background:#0d151df2;z-index:3}}.brand{{font-weight:850}}.hint{{color:#aebdca;flex:1}}select{{background:#182838;color:white;border:1px solid #ffffff30;border-radius:9px;padding:8px 10px;font-weight:750}}iframe{{display:block;width:100%;height:930px;border:0;background:#101820}}@media(max-width:760px){{.bar{{flex-wrap:wrap;padding:8px}}.hint{{order:3;flex-basis:100%;font-size:11px}}iframe{{height:900px}}}}
</style></head><body><div class='bar'><span class='brand'>World Substrate</span><span class='hint'>Switching branches selects a retained history; it never rewrites the baseline.</span><label>Branch <select id='branch'>{options}</select></label></div><iframe id='scene' title='{title} living world'></iframe>
<script>const DOCS={docs_json};const select=document.getElementById('branch'),frame=document.getElementById('scene'),q=new URLSearchParams(location.search);let requestedFrame=Math.max(0,parseInt(q.get('frame')||'0',10)||0);function syncInner(){{try{{const w=frame.contentWindow;if(typeof w.render==='function'){{w.playing=false;const toggle=w.document.getElementById('toggle');if(toggle)toggle.textContent='Play';if(typeof w.schedule==='function')w.schedule();w.render(requestedFrame)}}}}catch(_e){{}}}}function show(name,updateUrl=true){{if(!DOCS[name])name=Object.keys(DOCS)[0];select.value=name;frame.onload=syncInner;frame.srcdoc=DOCS[name];if(updateUrl)history.replaceState(null,'','?branch='+encodeURIComponent(name)+'&frame='+requestedFrame)}}select.onchange=e=>{{requestedFrame=0;show(e.target.value)}};show(q.get('branch')||Object.keys(DOCS)[0],false);</script></body></html>"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", type=Path, required=True)
    parser.add_argument("--branch", action="append", required=True, help="name=projection.json")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    profile = load_scene_contract(args.profile)
    bundles: dict[str, dict[str, Any]] = {}
    for item in args.branch:
        name, sep, raw_path = item.partition("=")
        if not sep or not name or not raw_path or name in bundles:
            raise ValueError("--branch must be unique name=projection.json")
        bundles[name] = load_live_projection_bundle(Path(raw_path))
    args.output.write_text(render_branching_html(bundles, profile, args.profile.parent))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
