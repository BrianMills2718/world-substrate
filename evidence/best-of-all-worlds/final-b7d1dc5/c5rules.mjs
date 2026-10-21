// C5 forced rules rejection with no AI spend: the build answer is the saved c4-run20 world (mocked in the browser,
// so no build call reaches the server), and every /run the page sends to the live server has one rule rewritten to
// change a part the world does not have. Records what the page says.
import { chromium } from '/home/brian/.npm/_npx/e41f203b7505f1fb/node_modules/playwright/index.mjs';
import fs from 'fs';
const share = JSON.parse(fs.readFileSync(process.argv[2], 'utf8')); const out = process.argv[3] || 'c5-rules.json';
const t0 = Date.now(); const s = () => ((Date.now() - t0) / 1000).toFixed(1); const log = (m) => console.log(`[${s()}s] ${m}`);
const rec = { started: new Date().toISOString(), source_share: process.argv[2], runs: [], tampered: [] };
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1280, height: 900 } });
await p.route('**/world-builder/api/generate-world', (route) => {
  rec.build_mocked_at = s(); log('build mocked from saved world');
  route.fulfill({ status: 200, contentType: 'application/json', body: JSON.stringify({ ok: true, ...share.world }) });
});
await p.route('**/world-builder/api/run', async (route) => {
  const body = JSON.parse(route.request().postData());
  body.causal_model.mechanics[0].effects[0].path = 'components.no_such_part.value';
  rec.tampered.push({ at: s(), mechanic: body.causal_model.mechanics[0].mechanic_id, policy: body.policy, keys: Object.keys(body) });
  log('tampered /run: ' + body.causal_model.mechanics[0].mechanic_id + ' policy=' + body.policy);
  await route.continue({ postData: JSON.stringify(body) });
});
p.on('response', async (r) => {
  const u = r.url(); if (!u.includes('/world-builder/api/')) return;
  let j; try { j = await r.json(); } catch { j = null; }
  if (u.endsWith('/run') || u.includes('/jobs/')) { rec.runs.push({ at: s(), url: u.replace(/.*\/api/, ''), status: r.status(), body: j }); log(u.replace(/.*\/api/, '') + ' ' + r.status() + ' ' + JSON.stringify(j).slice(0, 300)); }
  if (u.endsWith('/health')) rec.health = j;
});
await p.goto('https://brianmills.dev/world-builder/', { waitUntil: 'networkidle' });
const aiBox = p.locator('#ai-moves'); rec.ai_moves_before = await aiBox.isChecked().catch(() => null);
await p.fill('#desc', share.world.description || 'a pencil logistics and supply network');
await p.getByRole('button', { name: 'Create simulation', exact: true }).click();
for (let i = 0; i < 90; i++) {
  const st = ((await p.textContent('#live-status').catch(() => '')) || '').trim();
  if (rec.runs.length && /refused|internal|Paused|rule|could not/i.test(st)) break;
  await p.waitForTimeout(1000);
}
await p.waitForTimeout(2000);
rec.ai_moves_at_run = await aiBox.isChecked().catch(() => null);
rec.c5_rules_message = ((await p.textContent('#live-status').catch(() => '')) || '').trim();
const text = await p.evaluate(() => document.body.innerText);
rec.c5_page_has_internal_error = text.includes('internal world-builder error');
log('C5 page message: ' + rec.c5_rules_message + ' | internal error text on page: ' + rec.c5_page_has_internal_error);
await p.screenshot({ path: 'c5-rules-rejection-b7d1dc5.png', fullPage: false });
if (((await p.textContent('#play-btn').catch(() => '')) || '').includes('Pause')) await p.click('#play-btn');
rec.finished = new Date().toISOString(); fs.writeFileSync(out, JSON.stringify(rec, null, 1)); log('saved ' + out);
await b.close();
