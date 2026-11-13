"""Read-only saved-run UI check; --live uses deployed HTML, never model endpoints."""
import argparse, asyncio, hashlib, json
from pathlib import Path
from playwright.async_api import async_playwright
ROOT=Path(__file__).resolve().parents[3]
OUT=Path(__file__).parent
async def main():
 parser=argparse.ArgumentParser();parser.add_argument('--live',action='store_true');args=parser.parse_args()
 checks=[];errors=[];failed=[];blocked=[]
 async with async_playwright() as p:
  browser=await p.chromium.launch(executable_path='/home/brian/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome',headless=True,args=['--no-sandbox'])
  for width in (1440,390):
   context=await browser.new_context(viewport={'width':width,'height':1000})
   async def route(r):
    q=r.request
    if q.method not in ('GET','HEAD','OPTIONS'):
     blocked.append(q.url);await r.abort();return
    if not args.live and q.is_navigation_request() and q.url.startswith('https://brianmills.dev/world-builder/?'):
     await r.fulfill(body=(ROOT/'scripts/world_builder_home.html').read_text(),content_type='text/html');return
    await r.continue_()
   await context.route('**/*',route)
   page=await context.new_page()
   page.on('pageerror',lambda e:errors.append(str(e)))
   page.on('console',lambda m:errors.append(m.text) if m.type=='error' and 'ERR_FAILED' not in m.text else None)
   page.on('requestfailed',lambda q:failed.append(q.url) if '/cdn-cgi/rum' not in q.url else None)
   for share,cases in [('T-e9dYLdIi61',[('Bo','not assenting','false → true'),('Ari','technical repair','No recorded state changes.')]),('PKVERt8chzt7',[('Airfield dispatcher','request one training','Recorded state changes:'),('Flight instructor','invite him','Nearest move considered:'),('Sam','waiting training session','No recorded state changes.'),('Airfield mechanic','wait','State changes were not recorded for this attempt.')])]:
    await page.goto('https://brianmills.dev/world-builder/?run='+share,wait_until='domcontentloaded')
    await page.locator('#strip button').first.wait_for(state='attached')
    pause=page.get_by_role('button',name='⏸ Pause',exact=True)
    if await pause.is_visible():await pause.click()
    await page.locator('#attempts').evaluate('(el)=>el.open=true')
    for actor,original,result in cases:
     tick=page.locator('#strip button[aria-label^="Round 1: '+actor+' "]').first
     await tick.focus();await tick.press('Enter')
     text=await page.locator('#detail').inner_text()
     for needle in ('Original words','Interpretation','Result',original,result):
      assert needle in text,(share,width,actor,needle,text)
      checks.append(f'{share} {width} {actor}: {needle}')
     assert await page.locator('#detail').evaluate('(el)=>el.scrollWidth<=el.clientWidth'),text
     checks.append(f'{share} {width} {actor}: wraps')
     (OUT/f'{share}-{width}-{actor.lower()}.txt').write_text(text)
     if actor in ('Bo','Flight instructor'):
      await page.locator('#detail dt').first.click();await page.mouse.move(0,0)
      await page.locator('#detail').screenshot(path=str(OUT/f'{share}-{width}-{actor.lower()}.png'))
    if share=='T-e9dYLdIi61':
     await page.locator('#context-mode').select_option('actor')
     assert await page.locator('#analyst-context').is_hidden()
     assert await page.locator('#detail').is_hidden()
     checks.append(f'{share} {width}: inspector hidden in Actor context')
   if not args.live:
    # Model-free display fixture: preserve the original result separately from later settlement.
    fixture=json.loads((ROOT/'evidence/i0-i1/visible-run-20261113/share.json').read_text())
    fixture['rounds']=fixture['rounds'][:1]
    row=fixture['rounds'][0]['actors']['bo'];row['status']='unsupported_action';row['event_id']='fixture-original';row['changes']=[]
    row['judge']={'outcome':'confirmed','disposition':{'status':'installed','ruling_id':'fixture-rule','settled':{'status':'accepted','event_id':'fixture-settlement','changes':[{'path':'fixture.value','before':0,'after':1}]}}}
    await context.route('**/api/share/inspector-fixture',lambda r:r.fulfill(json=fixture))
    await page.goto('https://brianmills.dev/world-builder/?run=inspector-fixture',wait_until='domcontentloaded')
    await page.locator('#strip button').first.wait_for(state='attached')
    await page.locator('#attempts').evaluate('(el)=>el.open=true')
    await page.locator('#strip button[aria-label^="Round 1: Bo "]').first.click()
    result=await page.locator('#detail dd').nth(2).inner_text()
    settlement=await page.locator('#detail dd').nth(3).inner_text()
    assert 'fixture-original' in result and 'fixture-settlement' not in result and 'No recorded state changes.' in result
    assert 'fixture-settlement' in settlement and 'fixture.value: 0 → 1' in settlement and 'Recorded status: accepted' in settlement
    checks.extend([f'{width}: model-free original result retains original event/no changes',f'{width}: model-free settlement retains own status/event/changes'])
   await context.close()
  await browser.close()
 assert not errors,errors
 assert not failed,failed
 assert all('/cdn-cgi/rum' in url for url in blocked),blocked
 receipt={'mode':'live' if args.live else 'local HTML over actual read-only share GETs','checks':len(checks),'passed':checks,'errors':errors,'unexpected_failed_requests':failed,'blocked_analytics_posts':len(blocked),'html_sha256':hashlib.sha256((ROOT/'scripts/world_builder_home.html').read_bytes()).hexdigest(),'no_model_calls':True}
 (OUT/('live-checks.json' if args.live else 'checks.json')).write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({k:v for k,v in receipt.items() if k!='passed'}))
asyncio.run(main())
