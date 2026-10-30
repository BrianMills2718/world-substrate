// A dense world must not freeze the page (2026-10-30 s4 hang: ELK laid out a 77-box, 464-link Network on the
// page's only thread for 16 s, again each round someone moved, and Playwright could not read the Play button).
// Free: the page, the viewer and every API answer are served by page.route from tests/fixtures/c1r18_waltzman_world.json
// (84 boxes, 542 links); nothing leaves the machine and no AI is called.
//
//   node dense_world_e2e.mjs        (PLAYWRIGHT=<path to playwright/index.mjs> if it is not installed here)
//
// Checks: the run stage shows, two mocked rounds play (the second repoints a link, so the Network lays out again),
// #play-btn answers within 3 s after each, and the Network finishes laying out.
// Prints one line per check and `RESULT passed=N failed=M`; exits 1 on any failure.
import fs from 'fs';
const { chromium } = await import(process.env.PLAYWRIGHT || 'playwright');
const repo = new URL('../../', import.meta.url).pathname;
const world = JSON.parse(fs.readFileSync(repo + 'tests/fixtures/c1r18_waltzman_world.json', 'utf8'));
// Round 2 repoints one entity's link (cycle_id: work-cycle -> another entity), so the Network's links change.
const ents = world.bundle.entities, ids = new Set(ents.map((e) => e.id));
const ref = ents.flatMap((e) => Object.entries(e.components || {}).flatMap(([c, f]) => Object.entries(f || {})
  .filter(([, v]) => typeof v === 'string' && ids.has(v)).map(([k, v]) => ({ e, path: `entities.${e.id}.components.${c}.${k}`, v }))))[0];
const mover = ref.e, to = [...ids].find((id) => id !== ref.v && id !== mover.id);
const round = (n, changes) => ({ ok: true, status: 'done', summary: { last_turn: n, terminal_reached: false, turns: 1 }, snapshot_seal: 'mock', approval: {},
  trace_id: 'mock/run' + n, trace: { final_snapshot: {}, transcript: [{ turn: n, world_changes: [], world_events: [],
    actors: { [mover.id]: { status: 'accepted', did: { actor: mover.id, kind: 'move' }, changed: !!changes.length, changes } } }] } });
const answers = {
  g: { ok: true, status: 'done', bundle: world.bundle, causal_model: world.causal_model, review: { mechanics: [], processes: [] }, dry_run: { ok: true }, trace_id: 'mock/build' },
  r1: round(1, []),
  r2: round(2, [{ path: ref.path, before: ref.v, after: to }]),
};
const browser = await chromium.launch();
const p = await browser.newPage({ viewport: { width: 1200, height: 900 } });
const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
let runs = 0, layouts = 0; p.on('console', (m) => { if (m.text() === 'gv-layout') layouts++; });
await p.route('**/*', (route) => {
  const u = new URL(route.request().url()), path = u.pathname;
  if (u.host !== 'wb.test') return route.abort();
  if (path === '/world-builder/') return route.fulfill({ contentType: 'text/html', body: fs.readFileSync(repo + 'scripts/world_builder_home.html') });
  if (path === '/world-builder/graph-viewer.js') return route.fulfill({ contentType: 'text/javascript', body: fs.readFileSync(repo + 'scripts/vendor/graph-viewer.js', 'utf8')
    // Counts finished layouts without changing what the page sees.
    + ';(()=>{const m=GraphViewer.mount;GraphViewer.mount=(el,o)=>m(el,{...o,onLayout:(d)=>{console.log("gv-layout");return o.onLayout&&o.onLayout(d)}})})();' });
  if (path === '/world-builder/api/health') return route.fulfill({ json: { ok: true, llm_daily_budget_usd: 1, llm_daily_committed_usd: 0 } });
  if (path === '/world-builder/api/generate-world') return route.fulfill({ status: 202, json: { ok: true, job_id: 'g' } });
  if (path === '/world-builder/api/run') { runs++; return runs > 2 ? route.fulfill({ status: 503, json: { ok: false, error: 'mock: two rounds only' } })
    : route.fulfill({ status: 202, json: { ok: true, job_id: 'r' + runs } }); }
  if (path.startsWith('/world-builder/api/jobs/')) return route.fulfill({ json: answers[path.split('/').pop()] });
  return route.fulfill({ status: 404, json: { ok: false, error: 'not mocked' } });
});
let passed = 0, failed = 0;
const check = (name, ok, detail) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}: ${String(detail).replace(/\s+/g, ' ').slice(0, 220)}`); ok ? passed++ : failed++; };
const readPlay = async () => { const t = Date.now(); const label = (await p.textContent('#play-btn', { timeout: 3000 })).trim(); return [label, Date.now() - t]; };
try {
  await p.goto('http://wb.test/world-builder/');
  await p.fill('#desc', 'dense world');
  await p.getByRole('button', { name: 'Create simulation', exact: true }).click();
  await p.locator('#stage-run').waitFor({ state: 'visible', timeout: 15000 });
  check('run stage shows', true, 'visible');
  await p.waitForFunction(() => /^Round 2/.test(document.querySelector('#outcome').textContent), null, { timeout: 15000, polling: 200 });
  const [label, ms] = await readPlay();
  check('two rounds play and #play-btn answers within 3 s', ms < 3000, `${label} read in ${ms} ms; ${await p.textContent('#outcome')}`);
  await p.waitForFunction(() => /Paused/.test(document.querySelector('#live-status').textContent), null, { timeout: 15000 });
  const [label2, ms2] = await readPlay();
  check('#play-btn still answers after the round that repointed a link', ms2 < 3000 && /Play/.test(label2), `${label2} read in ${ms2} ms`);
  check('the Network finished laying out', layouts >= 1, `${layouts} layouts`);
} catch (e) { check('flow', false, e.message.split('\n')[0]); }
check('no page errors', errs.length === 0, errs.join(' | ') || 'none');
await browser.close();
console.log(`RESULT passed=${passed} failed=${failed}`);
process.exit(failed ? 1 : 0);
