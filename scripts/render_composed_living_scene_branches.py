#!/usr/bin/env python3
"""Wrap retained Living Scene branches in the composed-world product shell."""
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

from scripts.render_composed_living_scene import render_html
from world_substrate.living_scene import load_live_projection_bundle, load_scene_contract


def render_branching_html(
    bundles: dict[str, dict[str, Any]], profile: dict[str, Any], profile_dir: Path
) -> str:
    if not bundles:
        raise ValueError("branch player requires at least one retained branch")
    if {bundle.get("world_id") for bundle in bundles.values()} != {profile.get("world")}:
        raise ValueError("all retained branches must match the Living Scene profile world")
    documents = {name: render_html(bundle, profile, profile_dir) for name, bundle in sorted(bundles.items())}
    docs_json = json.dumps(documents, separators=(",", ":")).replace("</", r"<\/")
    options = "".join(
        f"<option value='{html.escape(name, quote=True)}'>{html.escape(name.replace('_', ' ').title())}</option>"
        for name in sorted(documents)
    )
    title = html.escape(str(profile.get("title") or profile.get("scene_id") or "Living Scene"))
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>{title} · World Substrate</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;background:#071015;color:#f4f7f5;font:13px/1.35 Inter,ui-sans-serif,system-ui,-apple-system,sans-serif;overflow:hidden}}.branch-control{{position:fixed;right:18px;top:16px;z-index:9;display:flex;align-items:center;gap:8px;padding:6px 8px 6px 10px;border-radius:12px;background:#071016d9;border:1px solid #ffffff1f;box-shadow:0 8px 28px #0007;backdrop-filter:blur(12px)}}.brand{{font-weight:830;font-size:11px;color:#cce2df}}label{{display:flex;align-items:center;gap:6px;color:#9eb2b2;font-size:10px}}select{{appearance:none;background:#172a32;color:white;border:1px solid #ffffff20;border-radius:9px;padding:7px 28px 7px 9px;font-weight:760;background-image:linear-gradient(45deg,transparent 50%,#b7cfcc 50%),linear-gradient(135deg,#b7cfcc 50%,transparent 50%);background-position:calc(100% - 13px) 50%,calc(100% - 9px) 50%;background-size:4px 4px,4px 4px;background-repeat:no-repeat}}iframe{{display:block;width:100vw;height:100vh;border:0;background:#071015}}@media(max-width:760px){{.branch-control{{right:8px;top:8px;padding:5px 6px}}.brand{{display:none}}select{{padding-top:6px;padding-bottom:6px}}}}
</style></head><body><div class='branch-control'><span class='brand'>World Substrate</span><label>History <select id='branch'>{options}</select></label></div><iframe id='scene' title='{title} living world'></iframe><script>
const DOCS={docs_json};const select=document.getElementById('branch'),frame=document.getElementById('scene'),q=new URLSearchParams(location.search);let requestedFrame=Math.max(0,parseInt(q.get('frame')||'0',10)||0);function syncInner(){{try{{const w=frame.contentWindow;if(typeof w.render==='function'){{w.playing=false;const toggle=w.document.getElementById('toggle');if(toggle)toggle.textContent='Play';if(typeof w.schedule==='function')w.schedule();w.render(requestedFrame)}}}}catch(_e){{}}}}function show(name,updateUrl=true){{if(!DOCS[name])name=Object.keys(DOCS)[0];select.value=name;frame.onload=syncInner;frame.srcdoc=DOCS[name];if(updateUrl)history.replaceState(null,'','?branch='+encodeURIComponent(name)+'&frame='+requestedFrame)}}select.onchange=e=>{{requestedFrame=0;show(e.target.value)}};show(q.get('branch')||Object.keys(DOCS)[0],false);
</script></body></html>"""


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
