// A real generated world that gets stuck (2026-10-06 toy workshop: Mira holds the
// glue pot and no rule lets her put it down; the only move left is re-accepting the
// recurring order). The build response is served from fixtures/, so no AI cost.
//
//   node stuck_world_e2e.mjs http://127.0.0.1:8898     (needs a running API for /run)
//
// Checks: the review warns it goes in circles, the live note names the stuck person,
// the picture shows by default, play pauses itself at 100 rounds and resumes on Play.
// Prints one line per check and `RESULT passed=N failed=M`; exits 1 on any failure.
import { chromium } from 'playwright';
import fs from 'fs';

const base = process.argv[2] || 'http://127.0.0.1:8898';
const resp = fs.readFileSync(new URL('./fixtures/toy-workshop-stuck.json', import.meta.url), 'utf8');
const browser = await chromium.launch();
const p = await browser.newPage({ viewport: { width: 1200, height: 900 } });
if (process.env.WORLD_BUILDER_OWNER_PASSWORD) await p.addInitScript((k) => { try { localStorage.setItem('wb-owner', k); } catch (e) {} }, process.env.WORLD_BUILDER_OWNER_PASSWORD);
await p.route('**/world-builder/api/generate-world', (r) => r.fulfill({ status: 200, contentType: 'application/json', body: resp }));
await p.route('**/world-builder/api/run', (route) => route.continue({ headers: { ...route.request().headers(), 'x-world-builder-client': 'e2e' } }));
const errs = []; p.on('pageerror', (e) => errs.push(String(e)));
let passed = 0, failed = 0;
const check = (name, ok, detail) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}: ${String(detail).replace(/\s+/g, ' ').slice(0, 220)}`); ok ? passed++ : failed++; };
const round = async () => Number(((await p.textContent('#outcome')).match(/^Round (\d+)/) || [0, 0])[1]);
try {
  await p.goto(base + '/world-builder/', { waitUntil: 'networkidle' });
  await p.fill('#desc', 'toy workshop');
  await p.getByRole('button', { name: 'Build my world', exact: true }).click();
  await p.locator('#stage-review').waitFor({ state: 'visible' });
  const warning = await p.textContent('#dry-notice');
  check('review warns it goes in circles', /only “accept order” was still happening/.test(warning), warning);
  await p.getByRole('button', { name: 'Approve rules and play' }).click();
  await p.waitForFunction(() => document.querySelector('#stuck-note').textContent.length > 0, null, { timeout: 120000 });
  const stuck = await p.textContent('#stuck-note');
  check('live note names the stuck person', /Mira hasn’t been able to do anything/.test(stuck), stuck);
  check('picture shows by default', await p.$eval('#replay', (f) => f.closest('details').open && (f.srcdoc || '').length > 1000), 'open with a replay');
  await p.waitForFunction(() => /Still watching/.test(document.querySelector('#live-status').textContent), null, { timeout: 400000 });
  const at = await round();
  check('pauses itself at 100 rounds', at === 100, `${await p.textContent('#run-h')} | ${await p.textContent('#live-status')}`);
  await p.waitForTimeout(4000);
  check('stays paused', (await round()) === at, `round ${await round()}`);
  await p.getByRole('button', { name: /Play/ }).click();
  await p.waitForFunction((n) => Number((document.querySelector('#outcome').textContent.match(/^Round (\d+)/) || [0, 0])[1]) > n, at, { timeout: 60000 });
  check('resumes on Play', true, await p.textContent('#outcome'));
  await p.getByRole('button', { name: /Pause/ }).click();
} catch (e) { check('flow', false, e.message); }
check('no page errors', errs.length === 0, errs.join(' | ') || 'none');
await browser.close();
console.log(`RESULT passed=${passed} failed=${failed}`);
process.exit(failed ? 1 : 0);
