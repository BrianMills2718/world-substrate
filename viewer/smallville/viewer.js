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
const replayUrl = SHARE ? "/world-builder/api/share/" + encodeURIComponent(SHARE) + "/replay"
  : (REPLAY && /^https?:|^\//.test(REPLAY)) ? REPLAY : (REPLAY ? "replay-" + REPLAY + ".json" : "replay.json");
fetch(replayUrl).then(r => r.json())
  .then(R => R.grid ? start(R, null) : fetch(A + "map.json").then(r => r.json()).then(M => start(R, M)))
  .catch(e => fail(SHARE ? "This shared run has no room map: " + e : "Could not load the replay or map assets. For Smallville maps run scripts/setup_smallville_viewer.py first. " + e));

function start(R, M) {
  if (REPLAY === "public" || REPLAY === "resident") {  // the two published demos
    const d = $("demos"); d.style.display = "block"; d.append("Demo runs: ");
    [["public", "scripted people (refusal, then the door opens)"], ["resident", "AI residents (words not shown)"]].forEach(([k, label], i) => {
      if (i) d.append(" · "); const a = document.createElement(k === REPLAY ? "b" : "a"); a.textContent = label; if (k !== REPLAY) a.href = "?replay=" + k; d.append(a); });
  }
  if (R.title) { document.getElementById("title").textContent = R.title + " replay"; document.title = R.title + " Replay"; }
  const names = R.meta.persona_names, last = R.meta.step, GEN = !!R.grid;
  const q = new URLSearchParams(location.search);  // ?step=N&paused=1 opens a given step (for links and tests)
  let step = Math.min(+q.get("step") || 0, last), playing = !q.has("paused"), timer = null, scene = null;
  if (!playing) { $("play").textContent = "Play"; $("play").classList.remove("on"); }
  const people = {}, doorGfx = {};
  let fitFn = null, graphOn = false, graphAll = false;
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
        const lm = graphOn ? Math.min(GLEFT, c.width * 0.45) : 0;  // the graph overlay needs room left of the map
        c.setZoom(Math.min((c.width - lm - 8) / (v.w * T), c.height / (v.h * T)));
        L = Math.min(2.2, Math.max(1, 0.95 / c.zoom));
        names.forEach(n => { people[n].emoji.setScale(L); people[n].chat.setScale(L); });
        if (step !== null && people[names[0]].tile) show(step, false);
        c.setScroll((v.x + v.w / 2) * T - c.width / 2 - (lm / 2) / c.zoom, (v.y + v.h / 2) * T - c.height / 2);
        drawGraph();
      };
      fitFn = fit; this.scale.on("resize", fit); fit(); this.time.delayedCall(400, fit);  // the page settles after the first fit
      show(step, false); if (playing) loop();
    }
  }
  new Phaser.Game({ type: Phaser.AUTO, parent: "game", pixelArt: true, scene: Replay,
    scale: { mode: Phaser.Scale.RESIZE, width: "100%", height: "100%" } });

  // Rules overlay: a tag per rule, on the doors it governs or stacked in the map's corner. Grey = not tried this step;
  // blue = allowed, orange = refused, each saying so in words. Clicking a tag opens the rule's full text.
  const tags = [], RULES = R.rules || [];
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
  const GRAPH = R.graph, GACT = R.graph_actors || {};
  const GCOL = { ok: "#1f5fa8", no: "#b4540a", mix: "#b4540a", none: "#586573" };
  const gword = { ok: "allowed", no: "refused", mix: "mixed", none: "no move" };
  const gstate = st => st === "accepted" ? "ok" : st === "no_action" ? "none" : "no";
  const gname = id => ((GRAPH.graph.nodes.find(n => n.id === id)) || { label: id }).label;
  function drawGraph() {
    const box = $("gov"); if (!box) return; box.innerHTML = "";
    if (!graphOn || !GRAPH || !scene) return;
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
      const h = d.offsetHeight + 6; if (isMove) my += h; else ty += h; place[id] = { x, w: CW, y: oy + y + d.offsetHeight / 2 };
    };
    const head = (t, x) => { const h = document.createElement("div"); h.className = "ghead"; h.textContent = t; h.style.cssText = "left:" + x + "px;top:" + (oy + 4) + "px"; box.appendChild(h); };
    head("Things used", thingsX); head("Moves the rules allow", movesX);
    const moveIds = GRAPH.graph.nodes.filter(n => n.kind === "action").map(n => n.id);
    const thingIds = GRAPH.graph.nodes.filter(n => n.kind === "thing").map(n => n.id);
    moveIds.filter(id => lit.moves[id] || graphAll).forEach(id => col(id, lit.moves[id], true));
    thingIds.filter(id => lit.things[id] || graphAll).forEach(id => col(id, lit.things[id], false));
    const C = (x1, y1, x2, y2, color, dash, w) => { const dx = Math.abs(x2 - x1) / 2, p = document.createElementNS("http://www.w3.org/2000/svg", "path");
      p.setAttribute("d", "M" + x1 + "," + y1 + " C" + (x1 - dx) + "," + y1 + " " + (x2 + dx) + "," + y2 + " " + x2 + "," + y2);
      p.setAttribute("fill", "none"); p.setAttribute("stroke", color); p.setAttribute("stroke-width", w || 2.5); p.setAttribute("opacity", .85); if (dash) p.setAttribute("stroke-dasharray", "5 4"); svg.appendChild(p); };
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
        g.t.uses.forEach(u => { const th = place[u]; if (th) C(mv.x, mv.y, th.x + th.w, th.y, GCOL[g.s], false, 1.8); }); }
    });
    if (!lit.tries.length) { const n = document.createElement("div"); n.className = "ghead"; n.style.cssText = "left:" + movesX + "px;top:" + (oy + 24) + "px"; n.textContent = "Nothing tried yet."; box.appendChild(n); }
  }
  if (GRAPH) { $("graphbtn").style.display = ""; $("graphall").parentElement.style.display = "none";
    $("graphbtn").onclick = () => { graphOn = !graphOn; $("graphbtn").textContent = graphOn ? "Hide graph" : "Show graph"; $("graphbtn").classList.toggle("on", graphOn);
      $("graphall").parentElement.style.display = graphOn ? "" : "none"; if (fitFn) fitFn(); drawGraph(); };
    $("graphall").onchange = e => { graphAll = e.target.checked; drawGraph(); }; }

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
  const startOfRound = d => { const rs = R.rounds, i = rs.findIndex(r => step >= r.start && step <= r.end); const j = Math.max(0, Math.min(rs.length - 1, (i < 0 ? 0 : i) + d)); return rs[j].start; };
  $("slider").max = last;
  $("slider").oninput = e => { show(+e.target.value, false); };
  $("prev").onclick = () => show(startOfRound(-1), false);
  $("next").onclick = () => show(startOfRound(1), false);
  $("speed").onchange = loop;
  $("play").onclick = () => {
    if (step >= last) show(0, false);
    playing = !playing; $("play").textContent = playing ? "Pause" : "Play"; $("play").classList.toggle("on", playing); if (playing) loop();
  };
}
