import json, threading, functools
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from playwright.sync_api import sync_playwright
ROOT=Path('/home/brian/code2/worktrees/ws-compound-integration-20261113'); OUT=Path('/tmp/ws-coverage-ui-20261113')
MSG='No part of this attempt was carried out. Choose one concrete operation and try again.'
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*a): pass
srv=ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT))); threading.Thread(target=srv.serve_forever,daemon=True).start();base=f'http://127.0.0.1:{srv.server_port}'
receipt={'scope':'Local recorded-input replay; native interpreter output and engine trace, resident choices recorded, no fresh resident policy and no paid calls. Main-page share fixture retains original authored bundle.','cases':[]}
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='/home/brian/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome',headless=True,args=['--no-sandbox'])
 for case in ['compound','mara']:
  trace=json.loads((ROOT/f'evidence/open-attempt/whole-attempt-coverage/engine-{case}.json').read_text())['trace']
  share=json.loads((ROOT/'evidence/i0-i1/deployed-integration-5/share.json').read_text());share.update(rounds=trace['transcript'],actor_inputs=trace['actor_inputs'],actor_information_mode=trace['actor_information_mode'],replay_html=(ROOT/f'evidence/open-attempt/whole-attempt-coverage/engine-{case}.html').read_text(),runs=[])
  for width,height in [(1440,1000),(390,844)]:
   for kind in ['homepage','picture']:
    context=browser.new_context(viewport={'width':width,'height':height});page=context.new_page();errors=[];console=[];failed=[];responses=[]
    page.on('pageerror',lambda e:errors.append(str(e)));page.on('console',lambda m:console.append({'type':m.type,'text':m.text}) if m.type in ['error','warning'] else None);page.on('requestfailed',lambda r:failed.append({'url':r.url,'failure':r.failure}));page.on('response',lambda r:responses.append({'url':r.url,'status':r.status}) if r.status>=400 else None)
    page.route('**/api/health',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps({'ok':True,'owner':False,'llm_daily_budget_usd':3,'llm_daily_committed_usd':0})))
    page.route('**/graph-viewer.js',lambda route:route.fulfill(status=200,content_type='text/javascript',body=(ROOT/'scripts/vendor/graph-viewer.js').read_text()))
    page.route('**/api/share/**',lambda route:route.fulfill(status=200,content_type='application/json',body=json.dumps(share)))
    url=base+('/scripts/world_builder_home.html?run=recorded-input-'+case if kind=='homepage' else f'/evidence/open-attempt/whole-attempt-coverage/engine-{case}.html')
    page.goto(url,wait_until='networkidle');page.wait_for_timeout(500)
    row={'case':case,'kind':kind,'viewport':[width,height],'console':console,'page_errors':errors,'failed_requests':failed,'http_errors':responses}
    if kind=='homepage':
     page.locator('#attempts > summary').click();buttons=page.locator('#strip button');row['frames']=[{'url':f.url,'text':f.locator('body').inner_text()[:1000]} for f in page.frames];row['srcdoc_length']=len(page.locator('#replay').get_attribute('srcdoc') or '');row['attempt_count']=buttons.count();row['attempt_labels']=buttons.evaluate_all('(els)=>els.map(e=>e.getAttribute("aria-label"))')
     target=page.get_by_role('button',name='Round 2: Ari tried:',exact=False) if case=='compound' else page.locator('#strip button[aria-label*="Mara — express stance"]')
     if target.count()!=1:target=page.locator('#strip button[aria-label*="Mara"]') if case=='mara' else buttons.first
     target.focus();page.keyboard.press('Enter');row['keyboard_detail_visible']=page.locator('#detail').is_visible();row['detail']=page.locator('#detail').inner_text();row['judge_panel_hidden']=not page.locator('#judge-panel').is_visible();row['message_present']=MSG in row['detail'];row['misleading_missing_rule_claim']='No installed rule covers' in row['detail'];row['body_text']=page.locator('body').inner_text();page.locator('#attempts').scroll_into_view_if_needed()
    else:
     row['body_text']=page.locator('body').inner_text();row['message_visible']=page.get_by_text(MSG,exact=False).count()>0;row['mara_did']=page.locator('[data-actor="mara"] .did').inner_text();row['story_text']=page.locator('#ws-story').inner_text()
    row['horizontal_overflow']=page.evaluate('document.documentElement.scrollWidth>innerWidth');shot=OUT/f'{case}-{kind}-{width}.png';page.screenshot(path=str(shot),full_page=True);row['screenshot']=str(shot);receipt['cases'].append(row);context.close()
 browser.close()
srv.shutdown();(OUT/'receipt.json').write_text(json.dumps(receipt,indent=2));print(json.dumps({'artifact':str(OUT/'receipt.json'),'cases':len(receipt['cases']),'errors':sum(len(r['page_errors'])+len(r['failed_requests'])+len(r['http_errors']) for r in receipt['cases'])}))
