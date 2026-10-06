// Browser walkthrough of the World Builder landing page, as a visitor would use it.
//
//   cd scripts/e2e && npm install && npx playwright install chromium
//   node world_builder_e2e.mjs <base> <flow...>      e.g. node world_builder_e2e.mjs https://brianmills.dev task open
//
// Flows: tooltips (free: every visible control shows a tooltip bubble) | task | ongoing | open | pencil (build, approve, watch it play live; continuing worlds are also paused, checked to stay still, and resumed),
// lucky (Make one up for me), dialogue (Help me write it, two turns, then build).
// E2E_AI=1 also switches a playing continuing world to AI moves for two rounds (costs a few cents).
// Screenshots go to $E2E_OUT (default ./out). Spends real model money on the target.
// Prints one line per step and `RESULT passed=N failed=M`; exits 1 if any flow failed.
import { chromium } from 'playwright';
import fs from 'fs';

const [base = 'http://127.0.0.1:8898', ...flows] = process.argv.slice(2);
const out = process.env.E2E_OUT || './out';
fs.mkdirSync(out, { recursive: true });
const DESCRIPTIONS = {
  task: 'Two cooks share one knife and must finish three salad orders before closing.',
  ongoing: 'Two cooks share one knife in a busy diner where new salad orders keep coming in.',
  pencil: 'a pencil manufacturing/logistics/supply/sales/business system',
  open: 'A small village where two neighbours, Rosa and Tom, keep a shared vegetable garden and a well; they get hungry and the plants need water.',
};
const LONG = 600000;

async function buildAndRun(p, kind, log) {
  await Promise.race([p.locator('#stage-review').waitFor({ state: 'visible', timeout: LONG }), p.locator('#stage-describe .notice').waitFor({ timeout: LONG })]);
  if (!(await p.locator('#stage-review').isVisible())) throw new Error('build failed: ' + (await p.textContent('#service-status')));
  log('review', (await p.textContent('#dry-notice')).trim());
  if (!(await p.getByRole('button', { name: 'Approve rules and play' }).isEnabled())) throw new Error('approve disabled');
  await p.getByRole('button', { name: 'Approve rules and play' }).click();
  await p.locator('#stage-run').waitFor({ state: 'visible', timeout: LONG });
  // Live play: rounds appear one by one while you watch.
  const round = async () => Number(((await p.textContent('#outcome')).match(/^Round (\d+)/) || [0, 0])[1]);
  const heading = async () => (await p.textContent('#run-h')).trim();
  await p.waitForFunction(() => /^Round [3-9]|^Round \d\d/.test(document.querySelector('#outcome').textContent)
    || !/running/.test(document.querySelector('#run-h').textContent), null, { timeout: LONG });
  log('playing', `${await heading()} | ${(await p.textContent('#outcome')).trim()} | ${(await p.textContent('#live-status')).trim()}`);
  log('latest', (await p.textContent('#feed li')).trim());
  if (kind !== 'task') {
    if (!/running/.test(await heading())) throw new Error('a ' + kind + ' world stopped by itself: ' + (await p.textContent('#live-status')));
    await p.getByRole('button', { name: /Pause/ }).click();
    await p.waitForTimeout(400);
    const at = await round();
    await p.waitForTimeout(5000);
    if ((await round()) !== at) throw new Error(`still advancing after Pause (${at} -> ${await round()})`);
    if (!/paused/.test(await heading())) throw new Error('heading does not say paused: ' + (await heading()));
    log('paused', `stayed at round ${at} for 5 s`);
    await p.getByRole('button', { name: /Play/ }).click();
    await p.waitForFunction((n) => Number((document.querySelector('#outcome').textContent.match(/^Round (\d+)/) || [0, 0])[1]) > n, at, { timeout: LONG });
    log('resumed', (await p.textContent('#outcome')).trim());
    if (process.env.E2E_AI) {
      // Switch to AI moves mid-play: the next rounds are chosen by the AI.
      const before = await round();
      await p.check('#ai-live');
      await p.waitForFunction((n) => Number((document.querySelector('#outcome').textContent.match(/^Round (\d+)/) || [0, 0])[1]) >= n + 2, before, { timeout: LONG });
      log('ai rounds', `${(await p.textContent('#outcome')).trim()} | ${(await p.textContent('#feed li')).trim()}`);
    }
    await p.getByRole('button', { name: /Pause/ }).click();
  }
}

// Agent and CI runs use the owner password (WORLD_BUILDER_OWNER_PASSWORD) so tests
// never spend the shared public visitor budget.
const OWNER = process.env.WORLD_BUILDER_OWNER_PASSWORD || '';
const browser = await chromium.launch();
let passed = 0, failed = 0;
for (const flow of flows.length ? flows : ['task']) {
  const p = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  if (OWNER) await p.addInitScript((k) => { try { localStorage.setItem('wb-owner', k); } catch (e) {} }, OWNER);
  // Label agent traffic so the run log never confuses it with a person's runs.
  await p.route('**/world-builder/api/**', (route) => route.continue({ headers: { ...route.request().headers(), 'x-world-builder-client': 'e2e' } }));
  const errors = []; p.on('pageerror', (e) => errors.push(String(e)));
  const log = (step, text) => console.log(`${flow.padEnd(8)} ${step}: ${String(text).replace(/\s+/g, ' ').slice(0, 300)}`);
  try {
    await p.goto(base + '/world-builder/', { waitUntil: 'networkidle' });
    if (flow in DESCRIPTIONS) {
      await p.check(`input[name="kind"][value="${flow === 'task' ? 'task' : 'ongoing'}"]`);
      await p.fill('#desc', DESCRIPTIONS[flow]);
      await p.getByRole('button', { name: 'Build what I wrote', exact: true }).click();
      await buildAndRun(p, flow === 'task' ? 'task' : 'ongoing', log);
    } else if (flow === 'tooltips') {
      // Costs nothing: hover every visible control and require a visible tooltip bubble.
      const controls = p.locator('button:visible, a:visible, textarea:visible, label.kind:visible, summary:visible');
      const n = await controls.count();
      const missing = [];
      for (let i = 0; i < n; i++) {
        const c = controls.nth(i);
        const name = ((await c.innerText().catch(() => '')) || (await c.getAttribute('id')) || `#${i}`).trim().slice(0, 40);
        await p.mouse.move(0, 0); await p.waitForTimeout(80);
        await c.hover();
        await p.waitForTimeout(400);
        const shown = await p.locator('#tip-bubble').isVisible() && (await p.textContent('#tip-bubble')).trim().length > 10;
        if (!shown) missing.push(name);
      }
      log('hovered', `${n} controls, ${n - missing.length} showed a tooltip`);
      if (missing.length) throw new Error('no visible tooltip on: ' + missing.join(' | '));
      await p.locator('.info[data-tip-for="talk-btn"]').click();
      const tapped = (await p.textContent('#tip-bubble')).trim();
      log('tap info', tapped);
      if (!/questions/.test(tapped)) throw new Error('info button did not show the Help me write it tip');
    } else if (flow === 'lucky') {
      await p.getByRole('button', { name: 'Make one up for me', exact: true }).click();
      await p.locator('#stage-run').waitFor({ state: 'visible', timeout: LONG });
      log('surprise', await p.textContent('#lucky-note'));
      log('run', await p.textContent('#outcome'));
    } else if (flow === 'dialogue') {
      await p.fill('#desc', 'some kids and a lemonade stand');
      await p.getByRole('button', { name: 'Help me write it', exact: true }).click();
      await p.locator('#chat .bubble.ai').first().waitFor({ timeout: LONG });
      log('ai', await p.locator('#chat .bubble.ai').first().innerText());
      const chip = p.locator('#chat .bubble.ai .chip').first();
      if (await chip.count()) await chip.click(); else await p.fill('#talk-input', 'two kids, one pitcher, sell ten cups');
      await p.getByRole('button', { name: 'Send' }).click();
      await p.locator('#chat .bubble.ai').nth(1).waitFor({ timeout: LONG });
      log('draft', await p.inputValue('#so-far'));
      await p.getByRole('button', { name: 'Use this description and build' }).click();
      await buildAndRun(p, 'task', log);
    } else throw new Error('unknown flow ' + flow);
    if (errors.length) throw new Error('page errors: ' + errors.join(' | '));
    passed++; log('PASS', '');
  } catch (error) {
    failed++; log('FAIL', error.message);
  } finally {
    await p.screenshot({ path: `${out}/${flow}.png`, fullPage: true }).catch(() => {});
    await p.close();
  }
}
await browser.close();
console.log(`RESULT passed=${passed} failed=${failed}`);
process.exit(failed ? 1 : 0);
