// Browser walkthrough of the World Builder landing page, as a visitor would use it.
//
//   cd scripts/e2e && npm install && npx playwright install chromium
//   node world_builder_e2e.mjs <base> <flow...>      e.g. node world_builder_e2e.mjs https://brianmills.dev task open
//
// Flows: task | ongoing | open (build, approve, run; ongoing/open also press Keep going),
// lucky (I'm feeling lucky), dialogue (Help me describe it, two turns, then build).
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
  open: 'A small village where two neighbours, Rosa and Tom, keep a shared vegetable garden and a well; they get hungry and the plants need water.',
};
const LONG = 600000;

async function buildAndRun(p, kind, log) {
  await Promise.race([p.locator('#stage-review').waitFor({ state: 'visible', timeout: LONG }), p.locator('#stage-describe .notice').waitFor({ timeout: LONG })]);
  if (!(await p.locator('#stage-review').isVisible())) throw new Error('build failed: ' + (await p.textContent('#service-status')));
  log('review', (await p.textContent('#dry-notice')).trim());
  if (!(await p.getByRole('button', { name: 'Approve rules and run' }).isEnabled())) throw new Error('approve disabled');
  await p.getByRole('button', { name: 'Approve rules and run' }).click();
  await p.locator('#stage-run').waitFor({ state: 'visible', timeout: LONG });
  log('run', (await p.textContent('#outcome')).trim());
  if (kind !== 'task') {
    if (await p.locator('#keep-btn').isHidden()) throw new Error('Keep going is hidden for a ' + kind + ' world');
    await p.getByRole('button', { name: /Keep going/ }).click();
    await p.waitForFunction(() => !document.querySelector('#keep-btn').disabled, null, { timeout: LONG });
    const outcome = (await p.textContent('#outcome')).trim();
    log('keep going', outcome);
    if (!/^Rounds 13/.test(outcome)) throw new Error('Keep going did not continue from round 13');
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
  const errors = []; p.on('pageerror', (e) => errors.push(String(e)));
  const log = (step, text) => console.log(`${flow.padEnd(8)} ${step}: ${String(text).replace(/\s+/g, ' ').slice(0, 300)}`);
  try {
    await p.goto(base + '/world-builder/', { waitUntil: 'networkidle' });
    if (flow in DESCRIPTIONS) {
      await p.check(`input[name="kind"][value="${flow}"]`);
      await p.fill('#desc', DESCRIPTIONS[flow]);
      await p.getByRole('button', { name: 'Build my world' }).click();
      await buildAndRun(p, flow, log);
    } else if (flow === 'lucky') {
      await p.getByRole('button', { name: 'I’m feeling lucky' }).click();
      await p.locator('#stage-run').waitFor({ state: 'visible', timeout: LONG });
      log('surprise', await p.textContent('#lucky-note'));
      log('run', await p.textContent('#outcome'));
    } else if (flow === 'dialogue') {
      await p.fill('#desc', 'some kids and a lemonade stand');
      await p.getByRole('button', { name: 'Help me describe it' }).click();
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
