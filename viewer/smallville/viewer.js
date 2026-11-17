// Static replay viewer on Phaser 3 + the Smallville tile map. No server: it reads replay.json (the substrate's export)
// and assets/ (copied from a local Smallville clone by scripts/setup_smallville_viewer.py).
// A tile is 32px; a person stands at the bottom centre of its tile. Doors are drawn here because the map has none.
const T = 32, A = "assets/", LAYERS = ["Bottom Ground", "Exterior Ground", "Exterior Decoration L1", "Exterior Decoration L2",
  "Interior Ground", "Wall", "Interior Furniture L1", "Interior Furniture L2 ", "Foreground L1", "Foreground L2"];
const $ = id => document.getElementById(id);
const fail = msg => { $("err").style.display = "block"; $("err").textContent = msg; };

const REPLAY = new URLSearchParams(location.search).get("replay");  // ?replay=scripted opens replay-scripted.json
// A replay with a `grid` is a map made from code, drawn with the CC0 Tiny Dungeon sheet (assets-cc0/); any other replay uses
// Smallville's own map and art (private use; copied by scripts/setup_smallville_viewer.py).
const CC0 = "assets-cc0/";
// ?share=<id> reads a shared run's replay from the World Builder service (generated maps only, report words withheld).
const SHARE = new URLSearchParams(location.search).get("share");
const ROW_MIN = 20;  // the least height one box in the beside-the-map columns gets, so long columns never overlap
const replayUrl = SHARE ? "/world-builder/api/share/" + encodeURIComponent(SHARE) + "/replay"
  : (REPLAY && /^https?:|^\//.test(REPLAY)) ? REPLAY : (REPLAY ? "replay-" + REPLAY + ".json" : "replay.json");
// ?embed=1: the World Builder page holds this viewer in a frame and posts each longer replay as the run plays
// ({type:"ws-replay", replay}); the viewer tells the page it is ready ({type:"ws-viewer-ready"}) and follows the newest round
// unless the person has scrubbed back. Implements: scene-viewer/a-running-world-is-drawn-on-the-map-as-it-plays
const EMBED = new URLSearchParams(location.search).get("embed") === "1";
let onReplay = null;  // set by start(): takes a longer replay of the same world
if (EMBED) {
  addEventListener("message", e => {
    if (e.origin !== location.origin || !e.data || e.data.type !== "ws-replay" || !e.data.replay || !e.data.replay.grid) return;
    if (onReplay) onReplay(e.data.replay); else start(e.data.replay, null);
  });
  parent.postMessage({ type: "ws-viewer-ready" }, location.origin);
  // Tell the page how tall the whole viewer is, so its frame can show the round slider and the whole graph instead of hiding them behind an inner scroll.
  let sentHeight = 0;
  const reportSize = () => { const h = Math.ceil(document.documentElement.scrollHeight); if (Math.abs(h - sentHeight) > 6) { sentHeight = h; parent.postMessage({ type: "ws-size", height: h }, location.origin); } };
  setInterval(reportSize, 400); addEventListener("load", reportSize);  // content grows after the replay loads and when a graph opens; the page box itself never changes, so poll
} else fetch(replayUrl).then(r => r.json())
  .then(R => R.grid ? start(R, null) : fetch(A + "map.json").then(r => r.json()).then(M => start(R, M)))
  .catch(e => fail(SHARE ? "This shared run has no room map: " + e : "Could not load the replay or map assets. For Smallville maps run scripts/setup_smallville_viewer.py first. " + e));

function start(R, M) {
  if (REPLAY === "public" || REPLAY === "resident") {  // the two published demos
    const d = $("demos"); d.style.display = "block"; d.append("Demo runs: ");
    [["public", "scripted people (refusal, then the door opens)"], ["resident", "AI residents (words not shown)"]].forEach(([k, label], i) => {
      if (i) d.append(" · "); const a = document.createElement(k === REPLAY ? "b" : "a"); a.textContent = label; if (k !== REPLAY) a.href = "?replay=" + k; d.append(a); });
  }
  if (R.title) { document.getElementById("title").textContent = R.title + " replay"; document.title = R.title + " Replay"; }
  if (R.illustrative) { const n = document.getElementById("note"); n.textContent = R.illustrative; n.style.display = "block"; }
  const names = R.meta.persona_names, GEN = !!R.grid;
  let last = R.meta.step, followNewest = true;
  const q = new URLSearchParams(location.search);  // ?step=N&paused=1 opens a given step (for links and tests)
  let step = Math.min(+q.get("step") || 0, last), playing = !q.has("paused"), timer = null, scene = null;
  if (!playing) { $("play").textContent = "Play"; $("play").classList.remove("on"); }
  const people = {}, doorGfx = {};
  let fitFn = null, graphOn = false, gmode = "beside", focusId = null, userZoom = 1, panX = 0, panY = 0;  // wheel zooms, dragging pans
  const COLW = 200, GLEFT = 2 * COLW + 76;  // the graph overlay: two columns of boxes (things, then moves) left of the map
  let L = 1;  // labels are drawn larger when the map is zoomed out so they stay readable
  const doorAt = s => { const st = {}; R.door_changes.forEach(c => { if (c.step <= s) st[c.door] = c.state; }); return st; };
  const px = (tile) => [tile[0] * T + T / 2, tile[1] * T + T];

  class Replay extends Phaser.Scene {
    preload() {
      if (GEN) { this.load.spritesheet("td", CC0 + R.grid.sheet, { frameWidth: 16, frameHeight: 16 }); return; }
      M.tilesets.forEach(t => this.load.image(t.name, A + "tiles/" + t.image.split("/").pop()));
      this.load.tilemapTiledJSON("map", A + "map.json");
      names.forEach(n => this.load.atlas(n, A + "characters/" + R.sprites[n] + ".png", A + "characters/atlas.json"));
    }
    create() {
      scene = this;
      if (GEN) {
        const map = this.make.tilemap({ data: R.grid.data, tileWidth: 16, tileHeight: 16 });
        map.createLayer(0, map.addTilesetImage("td", "td", 16, 16, 0, 0), 0, 0).setScale(T / 16);
        (R.grid.props || []).forEach(([x, y, f]) => this.add.sprite(x * T, y * T, "td", f).setOrigin(0, 0).setScale(T / 16).setDepth(1));
      } else {
        const map = this.make.tilemap({ key: "map" });
        const sets = M.tilesets.map(t => map.addTilesetImage(t.name, t.name));
        LAYERS.forEach(n => { const l = map.createLayer(n, sets, 0, 0); if (n.startsWith("Foreground")) l.setDepth(5); });
      }
      Object.entries(R.doors).forEach(([id, d]) => { doorGfx[id] = this.add.graphics().setDepth(2); });
      // Room names on the top wall of each room, and things that stand in a room as a generic prop with their name.
      (R.rooms || []).forEach(r => this.add.text((r.x0 + 0.3) * T, r.label_row * T + 6, r.label, { font: "bold 14px sans-serif", color: "#ffffff", stroke: "#16212b", strokeThickness: 4 }).setDepth(3));
      (R.objects || []).forEach(o => {
        this.add.sprite(o.tile[0] * T, o.tile[1] * T, "td", 89).setOrigin(0, 0).setScale(T / 16).setDepth(1);
        this.add.text(o.tile[0] * T + T / 2, o.tile[1] * T - 2, o.label, { font: "bold 11px sans-serif", color: "#ffffff", stroke: "#16212b", strokeThickness: 3 }).setOrigin(0.5, 1).setDepth(3);
      });
      makeRuleTags(this);
      names.forEach(n => {
        if (!GEN) ["left", "right", "down", "up"].forEach(dir => this.anims.create({ key: n + "-" + dir, frameRate: 6, repeat: -1,
          frames: this.anims.generateFrameNames(n, { prefix: dir + "-walk.", start: 0, end: 3, zeroPad: 3 }) }));
        const sprite = GEN ? this.add.sprite(0, 0, "td", +R.sprites[n].split("-")[1]).setOrigin(0.5, 1).setDepth(4).setScale(T / 16)
                           : this.add.sprite(0, 0, n, "down").setOrigin(0.5, 1).setDepth(4);
        if (!GEN) sprite.setScale(40 / 32);
        const emoji = this.add.text(0, 0, "", { font: "20px sans-serif", color: "#000", backgroundColor: "#ffffff", padding: { x: 4, y: 2 } }).setOrigin(0.5, 1).setDepth(6);
        const chat = this.add.text(0, 0, "", { font: "13px sans-serif", color: "#0b2f5b", backgroundColor: "#ffffff", padding: { x: 6, y: 4 },
          wordWrap: { width: 210 } }).setOrigin(0.5, 1).setDepth(7);
        people[n] = { sprite, emoji, chat, tile: null };
      });
      const fit = () => {
        const c = this.cameras.main, v = R.view;
        const lm = graphOn ? Math.min(gmode === "beside" ? 660 : GLEFT, c.width * (gmode === "beside" ? 0.5 : 0.45)) : 0;  // the graph overlay needs room left of the map
        c.setZoom(Math.min((c.width - lm - 8) / (v.w * T), c.height / (v.h * T)) * userZoom);
        L = Math.min(2.2, Math.max(1, 0.95 / c.zoom));
        names.forEach(n => { people[n].emoji.setScale(L); people[n].chat.setScale(L); });
        if (step !== null && people[names[0]].tile) show(step, false);
        c.setScroll((v.x + v.w / 2) * T - c.width / 2 - (lm / 2 - panX) / c.zoom, (v.y + v.h / 2) * T - c.height / 2 + panY / c.zoom);
        drawGraph(); requestAnimationFrame(drawGraph);  // the camera's midpoint updates on the next frame
      };
      fitFn = fit; this.scale.on("resize", fit); fit(); this.time.delayedCall(400, fit);  // the page settles after the first fit
      show(step, false); if (playing) loop();
    }
  }
  new Phaser.Game({ type: Phaser.AUTO, parent: "game", pixelArt: true, scene: Replay,
    scale: { mode: Phaser.Scale.RESIZE, width: "100%", height: "100%" } });

  // Rules overlay: a tag per rule, on the doors it governs or stacked in the map's corner. Grey = not tried this step;
  // blue = allowed, orange = refused, each saying so in words. Clicking a tag opens the rule's full text.
  const tags = [], RULES = R.rules || [];  // rules do not change while a run plays
  let rulesOn = false;
  function makeRuleTags(sc) {
    if (!RULES.length) return;
    $("rules").style.display = "";
    const v = R.view; let n = 0;
    RULES.forEach(rule => {
      const spots = rule.at_doors ? Object.entries(R.doors).map(([id, d]) => {
        const xs = d.tiles.map(t => t[0]), ys = d.tiles.map(t => t[1]);
        return { door: id, x: (Math.min(...xs) + Math.max(...xs) + 1) / 2 * T, y: (Math.min(...ys) + (rule.kind === "move" ? 2.6 : -0.6)) * T };
      }) : [{ door: null, x: (v.x + 0.6) * T, y: (v.y + 1.2 + n++ * 0.9) * T, left: true }]  // in the margin left of the map;
      spots.forEach(sp => {
        const t = sc.add.text(sp.x, sp.y, "", { font: "bold 13px sans-serif", color: "#fff", backgroundColor: "#586573", padding: { x: 6, y: 3 } })
          .setOrigin(sp.left ? 1 : 0.5, 0).setDepth(8).setVisible(false).setInteractive({ useHandCursor: true });
        t.on("pointerdown", () => ruleBox(rule));
        tags.push({ rule, door: sp.door, t });
      });
    });
  }
  function ruleBox(rule) {
    const b = $("rulebox"); b.innerHTML = "";
    const add = (tag, text, parent = b) => { const e = document.createElement(tag); e.textContent = text; parent.appendChild(e); return e; };
    const x = add("button", "Close"); x.className = "x"; x.onclick = () => { b.style.display = "none"; };
    add("h2", rule.kind); add("div", rule.rationale);
    [["Needs", rule.needs], ["Changes", rule.changes], ["Not modelled", rule.limits]].forEach(([h, items]) => {
      add("h3", h); if (!items.length) { add("div", "nothing"); return; }
      const ul = add("ul", ""); items.forEach(i => add("li", i, ul));
    });
    b.style.display = "block";
  }
  function drawRules(frame) {
    if (!tags.length) return;
    const met = {};  // "kind|door" -> the attempts this step that met the rule
    names.forEach(n => { const r = frame[n] && frame[n].rule; if (r) (met[r.kind + "|" + (r.door || "")] = met[r.kind + "|" + (r.door || "")] || []).push({ n, r }); });
    tags.forEach(g => {
      const hit = met[g.rule.kind + "|" + (g.door || "")];
      let text = g.rule.kind, fill = "#586573";
      if (hit) { const h = hit[hit.length - 1]; text = g.rule.kind + " - " + h.n + (h.r.ok ? " allowed" : " refused: " + (h.r.why.join("; ") || "rule not met")); fill = h.r.ok ? "#1f5fa8" : "#b4540a"; }
      g.t.setText(text).setBackgroundColor(fill).setScale(L).setVisible(rulesOn);
    });
  }
  $("rules").onclick = () => { rulesOn = !rulesOn; $("rules").textContent = rulesOn ? "Hide rules" : "Show rules"; $("rules").classList.toggle("on", rulesOn); drawRules(R.steps[String(step)]); if (!rulesOn) $("rulebox").style.display = "none"; };


  // Graph overlay (scene-viewer/world-graph): the same whole-system graph as graph.html, drawn over the map. People are
  // tagged where they stand; the moves they tried sit in the left margin and the things those moves used in the right,
  // each linked and lit for this round: blue = allowed, orange = refused, grey = no move or not used, each said in words.
  let GRAPH = R.graph, GACT = R.graph_actors || {};
  const GCOL = { ok: "#1f5fa8", no: "#b4540a", mix: "#b4540a", none: "#586573" };
  const gword = { ok: "allowed", no: "refused", mix: "mixed", none: "no move" };
  const gstate = st => st === "accepted" ? "ok" : st === "no_action" ? "none" : "no";
  const gname = id => ((GRAPH.graph.nodes.find(n => n.id === id)) || { label: id }).label;
  function drawGraph() {
    const box = $("gov"); if (!box) return; box.innerHTML = "";
    if (!graphOn || !GRAPH || !scene) return;
    const whole = gmode !== "round", beside = gmode === "beside";
    const cam = scene.cameras.main, st = $("stage").getBoundingClientRect(), gm = $("game").getBoundingClientRect();
    const ox = gm.left - st.left, oy = gm.top - st.top, W = gm.width, H = gm.height;
    const v0 = R.view, proj = (wx, wy) => [(wx - cam.midPoint.x) * cam.zoom + cam.width / 2 + ox, (wy - cam.midPoint.y) * cam.zoom + cam.height / 2 + oy];
    const ri = R.rounds.findIndex(r => step >= r.start && step <= r.end), round = ri >= 0 ? GRAPH.rounds[ri] : null;
    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg"); svg.setAttribute("width", ox + W); svg.setAttribute("height", oy + H); box.appendChild(svg);
    const CW = Math.min(COLW, (proj(v0.x * T, 0)[0] - ox - 20) / 2 - 20);
    const mapL = proj(v0.x * T, 0)[0], movesX = mapL - 10 - CW, thingsX = movesX - 40 - CW;
    const chip = (x, y, text, state, w, sub) => {
      const d = document.createElement("div"); d.className = "gchip " + state; d.style.cssText = "left:" + x + "px;top:" + y + "px;width:" + w + "px";
      d.textContent = text; if (sub) { const s2 = document.createElement("small"); s2.textContent = sub; d.appendChild(s2); }
      d.style.borderStyle = state === "none" ? "dashed" : "solid"; d.style.borderColor = GCOL[state]; box.appendChild(d); return d;
    };
    const lit = { moves: {}, things: {}, tries: [] };
    (round ? round.tries : []).forEach(t => {
      const s = gstate(t.status); lit.tries.push(t);
      if (t.move) { const m = lit.moves[t.move] || (lit.moves[t.move] = { ok: 0, no: 0, none: 0 }); m[s]++; t.uses.forEach(u => { const o = lit.things[u] || (lit.things[u] = { ok: 0, no: 0, none: 0 }); o[s]++; }); }
    });
    (round ? round.world_changed : []).forEach(c => { if (!lit.things[c]) lit.things[c] = { ok: 1, no: 0, none: 0, changed: true }; });
    const stateOf = o => o.ok && o.no ? "mix" : o.ok ? "ok" : o.no ? "no" : "none";
    const place = {}; let my = 24, ty = 24;
    const col = (id, o, isMove) => {
      const state = o ? stateOf(o) : "none", sub = o ? (state === "mix" ? o.ok + " allowed, " + o.no + " refused" : gword[state]) + (o.changed ? " · changed" : "") : "";
      const y = isMove ? my : ty, x = isMove ? movesX : thingsX;
      const d = chip(x, oy + y, gname(id), state, CW, sub);
      const h = d.offsetHeight + 6; if (isMove) my += h; else ty += h; place[id] = { x, w: CW, y: oy + y + d.offsetHeight / 2, el: d };
    };
    const head = (t, x) => { const h = document.createElement("div"); h.className = "ghead"; h.textContent = t; h.style.cssText = "left:" + x + "px;top:" + (oy + 4) + "px"; box.appendChild(h); };
    if (!whole) head("Things used", thingsX); if (!beside) head(whole ? "Moves (every one the rules allow)" : "Moves the rules allow", movesX);
    const NODES = GRAPH.graph.nodes;
    const C = (x1, y1, x2, y2, color, dash, w) => { const dx = Math.abs(x2 - x1) / 2, p = document.createElementNS("http://www.w3.org/2000/svg", "path");
      p.setAttribute("d", "M" + x1 + "," + y1 + " C" + (x1 - dx) + "," + y1 + " " + (x2 + dx) + "," + y2 + " " + x2 + "," + y2);
      p.setAttribute("fill", "none"); p.setAttribute("stroke", color); p.setAttribute("stroke-width", w || 2.5); p.setAttribute("opacity", .85); if (dash) p.setAttribute("stroke-dasharray", "5 4"); svg.appendChild(p); };
    const moveIds = NODES.filter(n => n.kind === "action").map(n => n.id);
    const procIds = NODES.filter(n => n.kind === "process").map(n => n.id);
    const thingIds = NODES.filter(n => n.kind === "thing").map(n => n.id);
    const roomOf = id => (R.rooms || []).find(r => "e:" + r.id === id);
    const homeOf = {}; GRAPH.graph.edges.forEach(e => { if (e.label === "is in" && roomOf(e.target)) homeOf[e.source] = e.target; });
    const actState = {}; (round ? round.tries : []).forEach(t => { actState[t.actor] = gstate(t.status); });
    const lines = [];
    if (beside) {  // the whole network laid out beside the map in columns; click a box to see its links and where it is on the map
      const PL = ox + 10, PW = Math.max(300, mapL - ox - 22), cols = [["People", NODES.filter(n => n.kind === "actor")], ["Moves and rules", NODES.filter(n => n.kind === "action" || n.kind === "process")],
        ["Things", NODES.filter(n => n.kind === "thing")], ["Places", NODES.filter(n => n.kind === "place")]].filter(c => c[1].length);  // no empty column
      const gap = 16, cw = (PW - gap * (cols.length - 1)) / cols.length, step = Math.min(52, Math.max(ROW_MIN, (H - 56) / Math.max(1, ...cols.map(c => c[1].length))));
      cols.forEach(([title, list], ci) => { const x = PL + ci * (cw + gap); head(title, x);
        list.forEach((n, i) => { const y = oy + 24 + i * step;
          const st = n.kind === "actor" ? (actState[n.id] || "none") : n.kind === "action" ? (lit.moves[n.id] ? stateOf(lit.moves[n.id]) : "none") : n.kind === "process" ? (round && round.fired.includes(n.id) ? "ok" : "none") : n.kind === "thing" ? (lit.things[n.id] ? stateOf(lit.things[n.id]) : "none") : "none";
          const d = chip(x, y, n.label, st, cw); d.style.fontSize = "11px"; d.style.padding = "1px 5px"; d.style.whiteSpace = "nowrap"; d.style.overflow = "hidden"; d.style.textOverflow = "ellipsis"; d.title = n.label;  // one line each; the full name on hover
          place[n.id] = { x, w: cw, y: y + d.offsetHeight / 2, col: ci, el: d }; }); });
    }
    if (!beside) moveIds.filter(id => lit.moves[id] || whole).forEach(id => col(id, lit.moves[id], true));
    const placedThings = new Set(), rowIn = {};
    if (whole && !beside) {  // the whole network: every box sits on the map where it belongs; moves and processes sit in the margin
      if (procIds.length) { head("Changes the world makes by itself", movesX); my += 20; procIds.forEach(id => col(id, lit.things[id], true)); }
      thingIds.forEach(id => {
        const o = (R.objects || []).find(q => "e:" + q.id === id), rm = roomOf(homeOf[id]); if (!o && !rm) return;
        const k = rm ? (rowIn[rm.id] = (rowIn[rm.id] || 0) + 1) - 1 : 0, w = 170;
        const [cx, cy] = o ? proj((o.tile[0] + 0.5) * T, (o.tile[1] + 1.6) * T) : proj((rm.x0 + rm.x1 + 1) / 2 * T, (rm.y1 + 0.2 - k * 0.8) * T);
        const state = lit.things[id] ? stateOf(lit.things[id]) : "none", d = chip(cx - w / 2, cy - 10, gname(id), state, w, lit.things[id] && lit.things[id].changed ? "changed" : "");
        d.style.fontSize = "11px"; d.style.padding = "1px 6px"; placedThings.add(id); place[id] = { x: cx - w / 2, w, y: cy - 10 + d.offsetHeight / 2, onMap: true, el: d };
      });
      NODES.filter(n => n.kind === "place" && roomOf(n.id)).forEach(n => {
        const r = roomOf(n.id), [cx, cy] = proj((r.x0 + r.x1 + 1) / 2 * T, (r.y0 + 1.3) * T), w = 96;
        const d = chip(cx - w / 2, cy, n.label, "none", w); d.style.fontWeight = "700"; d.style.fontSize = "11px"; d.style.padding = "1px 6px"; d.style.background = "#eef2f6";
        place[n.id] = { x: cx - w / 2, w, y: cy + d.offsetHeight / 2, onMap: true, el: d };
      });
    }
    if (!beside) thingIds.filter(id => !placedThings.has(id) && (lit.things[id] || (whole && !roomOf(homeOf[id])))).forEach(id => col(id, lit.things[id], false));
    if (whole) {  // every route, faint; this round's tries are drawn bold on top
      const at = (id, other) => { const q = place[id]; if (q && beside) { const o = place[other]; return !o || q.col < o.col ? [q.x + q.w, q.y] : [q.x, q.y]; }
        if (q) return q.onMap ? [q.x + q.w / 2, q.y] : [q.x + q.w, q.y];
        const nm = GACT[id], pp = nm && people[nm]; if (pp) { const [a, b] = proj(pp.sprite.x, pp.sprite.y); return [a, b - 20]; } return null; };
      let drawn = 0;
      GRAPH.graph.edges.forEach(e => { const a = at(e.source, e.target), b = at(e.target, e.source); if (!a || !b) return; drawn++;
        const l = document.createElementNS("http://www.w3.org/2000/svg", beside ? "path" : "line");
        if (beside) { const bow = place[e.source] && place[e.target] && place[e.source].col === place[e.target].col ? -40 : (b[0] - a[0]) / 2; l.setAttribute("d", "M" + a[0] + "," + a[1] + " C" + (a[0] + bow) + "," + a[1] + " " + (b[0] - bow) + "," + b[1] + " " + b[0] + "," + b[1]); l.setAttribute("fill", "none"); }
        else { l.setAttribute("x1", a[0]); l.setAttribute("y1", a[1]); l.setAttribute("x2", b[0]); l.setAttribute("y2", b[1]); }
        l.setAttribute("stroke", beside ? "#9db0c2" : "#2a3644"); l.setAttribute("stroke-width", 1); l.setAttribute("opacity", beside ? .6 : .4); svg.appendChild(l); lines.push({ el: l, a: e.source, b: e.target }); });
      const n = document.createElement("div"); n.className = "ghead"; n.style.cssText = "left:" + (beside ? ox + 10 : thingsX) + "px;bottom:8px";
      n.textContent = NODES.length + " boxes, " + drawn + " of " + GRAPH.graph.edges.length + " links" + (gmode === "hover" ? " (click a box to see its links)" : beside ? " (click a box to light its links and place on the map)" : " drawn here"); box.appendChild(n);
      const nb = new Set(); if (focusId) { nb.add(focusId); lines.forEach(L => { if (L.a === focusId || L.b === focusId) { nb.add(L.a); nb.add(L.b); } }); }
      lines.forEach(L => { const on = focusId && (L.a === focusId || L.b === focusId); L.el.style.display = gmode === "hover" && !on ? "none" : "";
        if (on) { L.el.setAttribute("stroke", beside ? "#ffffff" : "#16212b"); L.el.setAttribute("stroke-width", 2.4); L.el.setAttribute("opacity", .95); } });
      Object.entries(place).forEach(([id, q]) => { if (!q.el) return; q.el.style.pointerEvents = "auto"; q.el.style.cursor = "pointer";
        q.el.onclick = () => { focusId = focusId === id ? null : id; drawGraph(); };
        if (focusId) { if (nb.has(id)) q.el.style.boxShadow = beside ? "0 0 0 3px #ffffff" : "0 0 0 3px #16212b"; else q.el.style.opacity = .45; } });
      if (focusId) {  // ring the focused box where it is on the map
        const fn = NODES.find(q => q.id === focusId), nm = GACT[focusId], pp = nm && people[nm], ob = (R.objects || []).find(q => "e:" + q.id === focusId), rm = roomOf(focusId) || roomOf(homeOf[focusId]);
        const pt = pp ? (([a, b]) => [a, b - 22])(proj(pp.sprite.x, pp.sprite.y)) : ob ? proj((ob.tile[0] + 0.5) * T, (ob.tile[1] + 0.5) * T) : rm ? proj((rm.x0 + rm.x1 + 1) / 2 * T, (rm.y0 + rm.y1 + 1) / 2 * T) : null;
        const w2 = document.createElement("div"); w2.className = "ghead"; w2.style.cssText = "left:" + (beside ? ox + 10 : thingsX) + "px;bottom:26px"; w2.textContent = (fn ? fn.label : focusId) + (pt ? ": ringed on the map" : ": not a place on the map"); box.appendChild(w2);
        if (pt) { const c = document.createElementNS("http://www.w3.org/2000/svg", "circle"); c.setAttribute("cx", pt[0]); c.setAttribute("cy", pt[1]); c.setAttribute("r", rm && !pp && !ob ? 60 : 28); c.setAttribute("fill", "none"); c.setAttribute("stroke", "#ffffff"); c.setAttribute("stroke-width", 5); c.setAttribute("stroke-dasharray", "7 5"); svg.appendChild(c); }
      }
    }
    const tagged = [];
    lit.tries.forEach(t => {
      const s = gstate(t.status), name = GACT[t.actor], pp = name && people[name]; if (!pp) return;
      const [px0, py0] = proj(pp.sprite.x, pp.sprite.y);
      tagged.push({ t, s, name, x: px0, y: py0 + 6 });
    });
    tagged.sort((a, b) => a.y - b.y || a.x - b.x);
    const placed = [];
    tagged.forEach(g => {  // stagger tags so adjacent people do not hide each other
      let y = g.y; while (placed.some(q => Math.abs(q.x - g.x) < 190 && Math.abs(q.y - y) < 40)) y += 42; placed.push({ x: g.x, y });
      const text = g.name + ": " + (g.t.status === "unsupported_action" ? "no rule covers it" : gword[g.s]) + (g.t.move ? " · " + gname(g.t.move) : "");
      const tag = chip(g.x - 90, y, text, g.s, 180, g.t.because && g.t.because.length ? "refused: " + g.t.because[0] : "");
      const mv = g.t.move && place[g.t.move];
      if (mv) { C(g.x - 90, y + tag.offsetHeight / 2, mv.x + mv.w, mv.y, GCOL[g.s], g.s === "none");
        g.t.uses.forEach(u => { const th = place[u]; if (th) { if (th.onMap || beside) C(mv.x + mv.w, mv.y, th.x, th.y, GCOL[g.s], false, 1.8); else C(mv.x, mv.y, th.x + th.w, th.y, GCOL[g.s], false, 1.8); } }); }
    });
    if (!lit.tries.length) { const n = document.createElement("div"); n.className = "ghead"; n.style.cssText = "left:" + movesX + "px;top:" + (oy + 24) + "px"; n.textContent = "Nothing tried yet."; box.appendChild(n); }
  }
  if (GRAPH) { $("graphbtn").style.display = ""; $("gmode").parentElement.style.display = "none";
    // A long column (70 boxes for a big world) never squeezes its boxes together: the stage grows to hold it and the page scrolls.
    const sizeStage = () => { const longest = Math.max(0, ...["actor", "action|process", "thing", "place"].map(k => (GRAPH ? GRAPH.graph.nodes : []).filter(n => k.split("|").includes(n.kind)).length));
      $("stage").style.minHeight = graphOn && gmode === "beside" && longest ? Math.max(320, 24 + longest * ROW_MIN + 56) + "px" : ""; const refit = () => window.dispatchEvent(new Event("resize")); refit(); setTimeout(refit, 150); };  // again once the scrollbar has appeared
    $("graphbtn").onclick = () => { graphOn = !graphOn; $("graphbtn").textContent = graphOn ? "Hide graph" : "Show graph"; $("graphbtn").classList.toggle("on", graphOn);
      $("gmode").parentElement.style.display = graphOn ? "" : "none"; sizeStage(); if (fitFn) fitFn(); drawGraph(); };
    $("gmode").onchange = e => { gmode = e.target.value; focusId = null; sizeStage(); if (fitFn) fitFn(); drawGraph(); };
    const want = q.get("graph");  // ?graph=round|map|hover|beside opens the graph in that style (for links and tests)
    if (want && ["round", "map", "hover", "beside"].includes(want)) { gmode = want; $("gmode").value = want; $("graphbtn").click(); } }

  function drawDoors(s) {
    const st = doorAt(s);
    Object.entries(R.doors).forEach(([id, d]) => {
      const g = doorGfx[id]; g.clear();
      const xs = d.tiles.map(t => t[0]), ys = d.tiles.map(t => t[1]);
      const x = Math.min(...xs) * T, y = Math.min(...ys) * T, w = (Math.max(...xs) - Math.min(...xs) + 1) * T, h = (Math.max(...ys) - Math.min(...ys) + 1) * T;
      if (st[id] === "open") { g.lineStyle(3, 0xb4540a, 1); g.strokeRect(x + 2, y + 2, w - 4, h - 4); }
      else { g.fillStyle(0x8a5a2b, 1); g.fillRect(x, y, w, h); g.lineStyle(2, 0x3b2410, 1); g.strokeRect(x, y, w, h); g.fillStyle(0xf0c060, 1); g.fillCircle(x + w - 6, y + h / 2, 3); }
    });
  }

  function show(s, animate) {
    step = s; const frame = R.steps[String(s)], dur = animate ? 0.85 * 1000 / +$("speed").value : 0;
    names.forEach(n => {
      const p = people[n], f = frame[n], [x, y] = px(f.movement), prev = p.tile; p.tile = f.movement;
      const place = (xx, yy) => { p.sprite.setPosition(xx, yy); p.emoji.setPosition(xx, yy - 52); p.chat.setPosition(xx, yy - 52 - 30 * L); };
      scene.tweens.killTweensOf(p.sprite); p.sprite.anims.stop();
      const still = () => { if (!GEN) p.sprite.setFrame("down"); };
      if (dur > 0 && prev && (prev[0] !== f.movement[0] || prev[1] !== f.movement[1])) {
        const dx = f.movement[0] - prev[0], dy = f.movement[1] - prev[1];
        if (!GEN) p.sprite.anims.play(n + "-" + (Math.abs(dx) >= Math.abs(dy) ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up")));
        scene.tweens.add({ targets: p.sprite, x, y, duration: dur, onUpdate: () => place(p.sprite.x, p.sprite.y),
          onComplete: () => { p.sprite.anims.stop(); still(); } });
      } else { still(); place(x, y); }
      p.emoji.setText(f.pronunciatio);
      const line = f.chat && f.chat[0] ? f.chat[0][1] : ""; p.chat.setText(line).setVisible(!!line);
    });
    drawDoors(s); drawRules(frame); panel(frame); drawGraph(); $("slider").value = s;
    const r = R.rounds.find(r => s >= r.start && s <= r.end);
    $("label").textContent = (r ? "Round " + r.round + " · " : "Start · ") + "step " + s + "/" + last;
    if (EMBED) { baseLabel = $("label").textContent; tag(); parent.postMessage({ type: "ws-round-shown", round: r ? r.round : 0, atNewest: s >= last }, location.origin); }
  }
  // Embedded: say whether the map follows the run or shows an earlier round, and offer the way back to the newest.
  let baseLabel = "";
  function tag() {
    if (!EMBED) return;
    const atNewest = step >= last, following = followNewest || atNewest;
    $("golive").style.display = following ? "none" : "";
    $("label").textContent = baseLabel + (step >= last ? " · newest round" : following ? " · following the run" : " · earlier round");
  }

  function panel(frame) {
    $("people").innerHTML = "";
    names.forEach(n => {
      const f = frame[n], d = document.createElement("div"); d.className = "card";
      const refused = f.description.includes("refused");
      d.innerHTML = "<b></b><span></span><div class='say'></div>";
      d.querySelector("b").textContent = n + " " + f.pronunciatio;
      const span = d.querySelector("span"); span.textContent = f.description; if (refused) span.className = "no";
      d.querySelector(".say").textContent = f.chat && f.chat[0] ? f.chat[0][1] : "";
      $("people").appendChild(d);
    });
  }

  function loop() {
    clearInterval(timer);
    timer = setInterval(() => { if (!playing) return; if (step >= last) { playing = false; $("play").textContent = "Replay"; $("play").classList.remove("on"); return; } show(step + 1, true); }, 1000 / +$("speed").value);
  }
  // Zoom and pan the map (and the graph drawn over it): wheel to zoom, drag to move, the button to reset.
  const view = () => { if (fitFn) fitFn(); };
  $("game").addEventListener("wheel", e => { e.preventDefault(); userZoom = Math.min(4, Math.max(1, userZoom * (e.deltaY < 0 ? 1.15 : 1 / 1.15))); if (userZoom === 1) { panX = 0; panY = 0; } view(); }, { passive: false });
  let drag = null;
  $("game").addEventListener("pointerdown", e => { drag = { x: e.clientX, y: e.clientY, px: panX, py: panY }; });
  addEventListener("pointermove", e => { if (!drag || userZoom === 1) return; panX = drag.px + e.clientX - drag.x; panY = drag.py - (e.clientY - drag.y); view(); });
  addEventListener("pointerup", () => { drag = null; });
  $("reset").onclick = () => { userZoom = 1; panX = 0; panY = 0; view(); };
  const startOfRound = d => { const rs = R.rounds, i = rs.findIndex(r => step >= r.start && step <= r.end); const j = Math.max(0, Math.min(rs.length - 1, (i < 0 ? 0 : i) + d)); return rs[j].start; };
  $("slider").max = last;
  $("slider").oninput = e => { show(+e.target.value, false); followNewest = step >= last; tag(); };
  $("golive").onclick = () => { show(last, false); followNewest = true; tag(); };
  $("prev").onclick = () => { show(startOfRound(-1), false); followNewest = step >= last; tag(); };
  $("next").onclick = () => { show(startOfRound(1), false); followNewest = step >= last; tag(); };
  // A longer replay of the same world: keep the map and people, take the new steps, rounds and graph, and play on to the newest round.
  onReplay = next => {
    const was = last; Object.assign(R, next); GRAPH = R.graph; GACT = R.graph_actors || {}; last = R.meta.step; $("slider").max = last;
    if (last > was && followNewest) { playing = true; $("play").textContent = "Pause"; $("play").classList.add("on"); loop(); }
    else show(step, false);
  };
  $("speed").onchange = loop;
  $("play").onclick = () => {
    if (step >= last) show(0, false);
    playing = !playing; followNewest = playing || step >= last; $("play").textContent = playing ? "Pause" : "Play"; $("play").classList.toggle("on", playing); if (playing) loop();
  };
}
