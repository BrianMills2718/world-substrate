import asyncio,json
from pathlib import Path
from playwright.async_api import async_playwright
D=Path('/tmp/ws-visible-browser-20261113')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/home/brian/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome',headless=True,args=['--no-sandbox'])
  c=await b.new_context(viewport={'width':1440,'height':1000})
  net=[]; errors=[]
  async def route(r):
   q=r.request
   if q.method not in ['GET','HEAD','OPTIONS']:
    net.append({'blocked':True,'method':q.method,'url':q.url}); await r.abort(); return
   await r.continue_()
  await c.route('**/*',route)
  page=await c.new_page()
  page.on('console',lambda m:errors.append({'type':m.type,'text':m.text}))
  page.on('pageerror',lambda e:errors.append({'type':'pageerror','text':str(e)}))
  page.on('response',lambda r:net.append({'status':r.status,'url':r.url,'method':r.request.method}))
  await page.goto('https://brianmills.dev/world-builder/?run=T-e9dYLdIi61',wait_until='networkidle')
  await page.screenshot(path=str(D/'initial-desktop.png'),full_page=True)
  (D/'initial-text.txt').write_text(await page.locator('body').inner_text())
  (D/'initial-aria.txt').write_text(await page.locator('body').aria_snapshot())
  (D/'initial-network.json').write_text(json.dumps(net,indent=2)); (D/'initial-console.json').write_text(json.dumps(errors,indent=2))
  print(await page.locator('body').inner_text())
  await b.close()
asyncio.run(main())
