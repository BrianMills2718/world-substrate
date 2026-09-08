#!/usr/bin/env python3
"""Package the local visual world-authoring builder as one standalone HTML file."""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_EXAMPLE = ROOT / "examples/world_authoring/orchard-v0.json"
DEFAULT_OUTPUT = ROOT / "evidence/renders/world-builder-v0.html"

CSS = r'''
:root{--bg:#0f1417;--panel:#151c20;--panel2:#1b2429;--line:#314047;--text:#edf1f2;--muted:#a9b5ba;--accent:#f1e8d5;--ink:#1c2326;--good:#63ba78;--bad:#e37a6c;--warn:#dca942}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.4 system-ui,-apple-system,sans-serif}.shell{min-height:100vh;display:grid;grid-template-columns:230px minmax(480px,1fr) minmax(320px,420px)}.side{border-right:1px solid var(--line);padding:22px 16px;position:sticky;top:0;height:100vh;background:#11171a}.brand{font-size:20px;font-weight:900;letter-spacing:-.03em}.side p{color:var(--muted);font-size:12px}.world-title{margin:22px 0 2px;font-weight:850}.counts{font-size:11px;color:var(--muted);margin-bottom:18px}.nav{display:grid;gap:5px}.nav button{border:1px solid transparent;background:transparent;color:var(--text);padding:9px 10px;border-radius:9px;text-align:left;font-weight:700}.nav button.active{background:var(--panel2);border-color:var(--line)}.side-actions{display:grid;gap:8px;margin-top:20px;padding-top:18px;border-top:1px solid var(--line)}button{font:inherit;cursor:pointer}.side-actions button,.primary,.secondary,.danger,.icon{border-radius:9px;padding:8px 11px;border:1px solid var(--line)}.side-actions button,.secondary{background:#172025;color:var(--text)}.primary{background:var(--accent);color:var(--ink);border-color:var(--accent);font-weight:850}.danger{background:transparent;color:#ffada2}.icon{padding:5px 8px;align-self:end}.main{padding:24px 28px 70px;min-width:0}.main-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:18px}.main-top h1{font-size:28px;margin:0;letter-spacing:-.04em}.status{border:1px solid var(--line);border-radius:999px;padding:6px 10px;font-size:12px;font-weight:850}.status.ok{color:#bfecc9;border-color:#3a7d49}.status.bad{color:#ffc0b7;border-color:#8d4c43}.section-head{display:flex;justify-content:space-between;align-items:end;gap:16px;margin:8px 0 14px}.section-head h2{margin:0;font-size:22px}.section-head p{margin:3px 0 0;max-width:700px}.muted{color:var(--muted)}.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;margin-bottom:12px}.card h3{margin:0 0 12px}.card-top{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.card-top h3{margin:0}.field{display:grid;gap:5px;margin-bottom:10px}.field-label{font-size:11px;text-transform:uppercase;letter-spacing:.07em;color:var(--muted);font-weight:800}.input{width:100%;background:#0f1518;border:1px solid #3a494f;color:var(--text);border-radius:8px;padding:9px 10px;outline:none}.input:focus{border-color:#8ba1ab}.input.invalid{border-color:var(--bad)}textarea.input{min-height:76px;resize:vertical;font-family:inherit}select.input{appearance:auto}.rows{display:grid;gap:8px}.row-grid{display:grid;gap:8px;align-items:end;border-top:1px solid #28363b;padding-top:10px}.component-row{grid-template-columns:1.2fr 1fr 1.3fr 38px}.action-row{grid-template-columns:1.2fr 1fr 38px}.presentation-row{grid-template-columns:1.1fr .8fr 1.2fr 38px}.boundary{border:1px solid #705f31;background:#272313;color:#ecd99f;border-radius:12px;padding:12px 14px;margin:0 0 12px}.empty{border:1px dashed var(--line);border-radius:12px;padding:18px;color:var(--muted)}.steps{margin:0;padding-left:20px}.steps li{margin:8px 0}.preview{border-left:1px solid var(--line);height:100vh;position:sticky;top:0;background:#0c1113;padding:18px;display:flex;flex-direction:column;gap:12px;min-width:0}.preview h2{font-size:15px;margin:0}.validation{max-height:160px;overflow:auto}.validation-error{font-size:11px;color:#ffc0b7;margin:3px 0}.validation-ok{font-size:11px;color:#bfecc9}.preview pre{flex:1;overflow:auto;margin:0;background:#080c0e;border:1px solid #263238;border-radius:10px;padding:12px;font:11px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;color:#cbd6da;white-space:pre}.export-actions{display:grid;grid-template-columns:1fr 1fr;gap:8px}.export-actions button{border:1px solid var(--line);border-radius:9px;padding:9px;background:#172025;color:var(--text)}.export-actions button:first-child{grid-column:1/-1;background:var(--accent);color:var(--ink);font-weight:850}.export-actions button:disabled{opacity:.35;cursor:not-allowed}.preview-note{font-size:11px;color:var(--muted)}.live-message{border:1px solid var(--line);border-radius:10px;padding:11px 12px;margin:10px 0;color:var(--muted);background:#11181b}.live-message.warn{border-color:#745f2c;color:#f0d98d;background:#282311}.receipt{font:12px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace;color:#cbd6da}.authority-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px}.authority-block{margin:12px 0}.code-list{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}.code-list code{background:#0c1215;border:1px solid #2d3b41;border-radius:6px;padding:4px 6px;font-size:11px;color:#d8e1e4}.mini-json{white-space:pre-wrap;background:#0c1215;border:1px solid #2d3b41;border-radius:8px;padding:9px;font:11px/1.45 ui-monospace,SFMono-Regular,Menlo,monospace;color:#cad5d9;overflow:auto}.mechanic-rationale{color:var(--muted)}.run-frame{display:block;width:100%;height:min(74vh,760px);border:1px solid var(--line);border-radius:14px;background:#111;margin-top:14px}button:disabled{opacity:.45;cursor:not-allowed}@media(max-width:900px){.authority-grid{grid-template-columns:1fr}}@media(max-width:1100px){.shell{grid-template-columns:200px 1fr}.preview{position:relative;height:560px;grid-column:1/-1;border-left:0;border-top:1px solid var(--line)}.side{grid-row:1/2}.main{grid-column:2}}@media(max-width:720px){.shell{display:block}.side{position:relative;height:auto;border-right:0;border-bottom:1px solid var(--line)}.nav{grid-template-columns:repeat(2,1fr)}.main{padding:18px}.row-grid,.component-row,.action-row,.presentation-row{grid-template-columns:1fr}.preview{height:600px}.section-head{align-items:start;flex-direction:column}}
'''

BODY = r'''
<div class="shell">
  <aside class="side">
    <div class="brand">World Authoring Studio</div>
    <p>Define represented state visually. Export the same bundle used by the code-first starter.</p>
    <div class="world-title" id="world-name"></div>
    <div class="counts" id="counts"></div>
    <nav class="nav">
      <button data-section="world">1 · World</button>
      <button data-section="components">2 · Components</button>
      <button data-section="entities">3 · Entities</button>
      <button data-section="actions">4 · Action signatures</button>
      <button data-section="mechanics">5 · Causal mechanics</button>
      <button data-section="presentation">6 · Presentation</button>
      <button data-section="run">7 · Run</button>
      <button data-section="export">8 · Review & export</button>
    </nav>
    <div class="side-actions">
      <button id="import-bundle">Import bundle JSON</button>
      <button id="reset-example">Reset Orchard example</button>
      <input id="file-input" type="file" accept="application/json,.json" hidden>
    </div>
  </aside>
  <main class="main">
    <div class="main-top"><h1>Build a world</h1><div class="status" id="validation-badge"></div></div>
    <div id="editor"></div>
  </main>
  <aside class="preview">
    <h2>Bundle preview</h2>
    <div class="validation" id="validation-errors"></div>
    <pre id="json-preview"></pre>
    <div class="export-actions">
      <button id="download-bundle">Download authoring bundle</button>
      <button id="copy-json">Copy JSON</button>
      <button id="copy-command">Copy scaffold command</button>
    </div>
    <div class="preview-note">Action signatures are intent shapes only. Generated mechanics are a separate compiler-validated layer and require explicit approval before a run.</div>
  </aside>
</div>
'''


def render(example_path: Path = DEFAULT_EXAMPLE) -> str:
    example = json.loads(example_path.read_text())
    core = (ROOT / "scripts/world_builder_core.js").read_text()
    app = (ROOT / "scripts/world_builder_app.js").read_text()
    payload = json.dumps(example, separators=(",", ":")).replace("</", "<\\/")
    return f"""<!doctype html><html lang='en'><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'><title>World Authoring Studio</title><style>{CSS}</style></head><body>{BODY}<script>{core}</script><script>window.INITIAL_BUNDLE={payload};</script><script>{app}</script></body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--example", type=Path, default=DEFAULT_EXAMPLE)
    ap.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = ap.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(args.example))
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
