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
  if (R.title) { document.getElementById("title").textContent = R.title + " replay"; document.title = R.title + " Replay"; }
  const names = R.meta.persona_names, last = R.meta.step, GEN = !!R.grid;
  const q = new URLSearchParams(location.search);  // ?step=N&paused=1 opens a given step (for links and tests)
  let step = Math.min(+q.get("step") || 0, last), playing = !q.has("paused"), timer = null, scene = null;
  if (!playing) { $("play").textContent = "Play"; $("play").classList.remove("on"); }
  const people = {}, doorGfx = {};
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
        c.setZoom(Math.min(c.width / (v.w * T), c.height / (v.h * T)));
        L = Math.min(2.2, Math.max(1, 0.95 / c.zoom));
        names.forEach(n => { people[n].emoji.setScale(L); people[n].chat.setScale(L); });
        if (step !== null && people[names[0]].tile) show(step, false);
        c.setScroll((v.x + v.w / 2) * T - c.width / 2, (v.y + v.h / 2) * T - c.height / 2);
      };
      this.scale.on("resize", fit); fit();
      show(step, false); if (playing) loop();
    }
  }
  new Phaser.Game({ type: Phaser.AUTO, parent: "game", pixelArt: true, scene: Replay,
    scale: { mode: Phaser.Scale.RESIZE, width: "100%", height: "100%" } });

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
    drawDoors(s); panel(frame); $("slider").value = s;
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
