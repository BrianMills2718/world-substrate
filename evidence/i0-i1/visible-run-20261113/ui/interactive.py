import asyncio,json,traceback
from pathlib import Path
from playwright.async_api import async_playwright
D=Path('/tmp/ws-visible-browser-20261113')
async def main():
 async with async_playwright() as p:
  b=await p.chromium.launch(executable_path='/home/brian/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome',headless=True,args=['--no-sandbox'])
  c=await b.new_context(viewport={'width':1440,'height':1000}); net=[]; errors=[]; checks=[]
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
  page.on('requestfailed',lambda q:net.append({'failed':q.failure,'url':q.url,'method':q.method}))
  await page.goto('https://brianmills.dev/world-builder/?run=T-e9dYLdIi61',wait_until='networkidle')
  print('READY',flush=True)
  while True:
   line=await asyncio.to_thread(input)
   if line=='exit':break
   try:
    result=await eval('run('+line+')',{}, {'run':lambda x:execute(x,page,D,checks)})
    print(json.dumps(result,ensure_ascii=False),flush=True)
   except Exception as e:print('ERROR '+str(e),flush=True)
  (D/'network.json').write_text(json.dumps(net,indent=2)); (D/'console.json').write_text(json.dumps(errors,indent=2)); (D/'checks.json').write_text(json.dumps(checks,indent=2)); await b.close()
async def execute(code,page,D,checks):
 async def work():
  exec('async def snippet():\n'+''.join(' '+line+'\n' for line in code.splitlines()),globals(),scope)
  return await scope['snippet']()
 scope={'page':page,'D':D,'checks':checks}
 # async function globals must include scope
 g={**globals(),**scope};exec('async def snippet():\n'+''.join(' '+line+'\n' for line in code.splitlines()),g)
 return await g['snippet']()
asyncio.run(main())
