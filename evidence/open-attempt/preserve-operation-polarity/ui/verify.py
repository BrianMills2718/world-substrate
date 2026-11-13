import asyncio, hashlib, json, subprocess
from pathlib import Path
from playwright.async_api import async_playwright

ROOT=Path('/home/brian/code2/worktrees/ws-intent-polarity-20261113')
OUT=Path('/tmp/ws-polarity-browser-20261113')
EVIDENCE=ROOT/'evidence/open-attempt/preserve-operation-polarity'
CASES=['bo-negative-r1','ari-role-r1','bo-negative-r3','bo-withdraw-r2','ari-assent-r6','mara-concern-r4','uncertain-positive','quoted-negative','foreign-authority']
records={c:json.loads((EVIDENCE/(c+'.json')).read_text()) for c in CASES}
checks=[]
def check(name,ok,detail):
    checks.append(dict(name=name,passed=bool(ok),detail=detail))

async def main():
    report=dict(scope='Read-only rendered presentation verification of recorded native interpreter/judge/Engine case checks. Not a new autonomous run, model evaluation, live-site or deployment claim.',root=str(ROOT),commit=subprocess.check_output(['git','-C',str(ROOT),'rev-parse','HEAD'],text=True).strip(),source_hashes={},scenarios=[],checks=checks)
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='/home/brian/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome',headless=True)
        report['browser']=browser.version
        for who in ['bo','ari']:
            src=ROOT/f'proposals/open-attempt/review-page/polarity-{who}.html'
            report['source_hashes'][src.name]=hashlib.sha256(src.read_bytes()).hexdigest()
            primary=records['bo-negative-r1' if who=='bo' else 'ari-role-r1']
            for width,height in [(1440,1000),(390,844)]:
                name=f'{who}-{width}'
                context=await browser.new_context(viewport=dict(width=width,height=height),device_scale_factor=1)
                page=await context.new_page()
                console=[]; errors=[]; failed=[]; requests=[]
                page.on('console',lambda m:console.append(dict(type=m.type,text=m.text)))
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('requestfailed',lambda r:failed.append(dict(url=r.url,failure=r.failure)))
                page.on('request',lambda r:requests.append(dict(method=r.method,url=r.url)))
                async def guard(route):
                    if route.request.method not in ['GET','HEAD']:
                        await route.abort()
                    else:
                        await route.continue_()
                await context.route('**/*',guard)
                await page.goto(src.as_uri(),wait_until='load')
                await page.screenshot(path=str(OUT/f'{name}-first.png'))
                quote=page.locator('aside blockquote')
                check(name+' original exact',await quote.inner_text()==primary['attempt'],await quote.inner_text())
                box=await quote.bounding_box()
                check(name+' original in first viewport',box and box['x']>=0 and box['x']+box['width']<=width and box['y']>=0 and box['y']+box['height']<=height,box)
                aside=await page.locator('aside').inner_text()
                if who=='bo':
                    check(name+' visible negative/no change','No matching installed operation.' in aside and 'Bo remains not assenting.' in aside and 'no world state changes' in aside,aside)
                else:
                    rows=await page.locator('aside tbody tr').all_inner_texts()
                    check(name+' authority separate from actor', 'authority\ttechnical-role-ari\tI try to perform a technical repair' in rows and 'The actor is ari; the authority object is technical-role-ari.' in aside,rows)
                    check(name+' condition failing to passing','Only the technical condition changes from failing to passing.' in aside,aside)
                scene=await page.locator('.shell').inner_text()
                check(name+' replay consequence',('Technical condition: passing: yes (was passing: no)' in scene if who=='ari' else 'not understood' in scene and 'nothing changed' in scene.lower()),scene)
                # Keyboard uses visible controls without following external links.
                await page.locator('#restart').focus()
                focused=[]
                for control in ['restart','prev','toggle','next']:
                    active=await page.evaluate('document.activeElement.id')
                    focused.append(active)
                    if control!='next':
                        await page.keyboard.press('Tab')
                check(name+' replay keyboard traversal',focused==['restart','prev','toggle','next'],focused)
                await page.locator('#restart').focus()
                await page.keyboard.press('Enter')
                check(name+' keyboard replay remains round one','1' in await page.locator('#turn').inner_text(),await page.locator('#turn').inner_text())
                await page.locator('.controls').scroll_into_view_if_needed()
                await page.screenshot(path=str(OUT/f'{name}-replay.png'))
                section=page.locator('section').filter(has=page.get_by_role('heading',name='Nine native checks'))
                contrast=await section.evaluate('''e=>{
                  const rgb=s=>s.match(/[\\d.]+/g).slice(0,3).map(Number);
                  const fg=getComputedStyle(e).color;
                  let bg='';for(let n=e;n;n=n.parentElement){let c=getComputedStyle(n).backgroundColor;if(c!=='rgba(0, 0, 0, 0)'&&c!=='transparent'){bg=c;break}}
                  const lum=c=>rgb(c).map(v=>{v/=255;return v<=.04045?v/12.92:((v+.055)/1.055)**2.4}).reduce((a,v,i)=>a+v*[.2126,.7152,.0722][i],0);
                  let a=lum(fg),b=lum(bg);return {foreground:fg,background:bg,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
                }''')
                check(name+' table readable contrast',contrast['ratio']>=4.5,contrast)
                rows=section.locator('tbody tr')
                check(name+' nine actual rows',await rows.count()==9,await rows.count())
                rowtexts=await rows.all_inner_texts()
                links=section.get_by_role('link',name='Recorded evidence',exact=True)
                hrefs=await links.evaluate_all('(els)=>els.map(e=>e.getAttribute("href"))')
                check(name+' case membership and exact wording', all(records[c]['attempt'] in rowtexts[i] and hrefs[i].endswith('/'+c+'.json') for i,c in enumerate(CASES)),dict(cases=CASES,rows=rowtexts,hrefs=hrefs))
                await section.scroll_into_view_if_needed()
                await page.screenshot(path=str(OUT/f'{name}-cases.png'))
                focuslinks=[]
                focused_bounds=[]
                await links.first.focus()
                for i in range(9):
                    focuslinks.append(await page.evaluate('({tag:document.activeElement.tagName,href:document.activeElement.getAttribute("href"),text:document.activeElement.innerText})'))
                    focused_bounds.append(await links.nth(i).bounding_box())
                    if i<8:
                        await page.keyboard.press('Tab')
                check(name+' nine evidence links keyboard accessible',len(focuslinks)==9 and all(x['tag']=='A' and x['href'].endswith('/'+c+'.json') for x,c in zip(focuslinks,CASES)),focuslinks)
                check(name+' focused evidence links fully visible',all(b and b['x']>=0 and b['x']+b['width']<=width for b in focused_bounds),focused_bounds)
                await page.screenshot(path=str(OUT/f'{name}-last-case-focus.png'))
                overflow=await page.evaluate('({viewport:innerWidth,document:document.documentElement.scrollWidth,containers:[...document.querySelectorAll("aside div,section")].map(e=>({tag:e.tagName,client:e.clientWidth,scroll:e.scrollWidth,overflow:getComputedStyle(e).overflowX}))})')
                check(name+' no document horizontal overflow',overflow['document']<=width,overflow)
                check(name+' runtime errors absent',not errors and not failed and not any(x['type']=='error' for x in console),dict(page_errors=errors,request_failures=failed,console=console))
                check(name+' no write requests',not any(x['method'] not in ['GET','HEAD'] for x in requests),requests)
                report['scenarios'].append(dict(name=name,viewport=dict(width=width,height=height),first_frame_text=aside,scene_text=scene,case_links=hrefs,overflow=overflow,console=console,page_errors=errors,failed_requests=failed,requests=requests))
                await context.close()
        await browser.close()
    report['primary_source_summaries']={key:dict(attempt=records[key]['attempt'],actual_kind=records[key]['actual_kind'],wanted=records[key]['row']['wanted'],status=records[key]['row']['status'],changes=records[key]['row']['changes']) for key in ['bo-negative-r1','ari-role-r1']}
    report['counts']=dict(checks=len(checks),passed=sum(c['passed'] for c in checks),failed=sum(not c['passed'] for c in checks),scenarios=len(report['scenarios']))
    (OUT/'receipt.json').write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(report['counts']))
    for c in checks:
        if not c['passed']:
            print(json.dumps(c,ensure_ascii=False))
    return report['counts']['failed']

raise SystemExit(asyncio.run(main()))
