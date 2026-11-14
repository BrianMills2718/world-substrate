"""Actual HTTP/catalog/scene browser walkthrough; native scripted policy, no providers.
Run: uv run --no-project --python 3.12 --with pydantic --with pyyaml --with gdm-concordia==2.4.0 --with playwright --with-editable /home/brian/code2/llm_client python evidence/ui/world-workspace-20261113/verify.py
"""
from pathlib import Path
import copy
import hashlib
import json
import os
import secrets
import sys
import tempfile
import threading
import time
import urllib.request
from http.server import ThreadingHTTPServer

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(ROOT / 'src')]
import scripts.world_builder_service as service
from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent
receipt = {'basis': 'Actual local HTTP service and SQLite catalog; scripted native policy adapter only; no provider calls. Retained pump world is opened read-only; orchard is an explicit constructed native-engine fixture.', 'checks': [], 'network': [], 'native_inputs': []}

def check(name, value):
    receipt['checks'].append({'name': name, 'passed': bool(value)})
    print(('PASS ' if value else 'FAIL ') + name, flush=True)
    (OUT/'progress.json').write_text(json.dumps(receipt,indent=2)+'\n')
    if not value:
        raise AssertionError(name)


NATIVE_RUN=service.WorldBuilderHandler._run_native

class Handler(service.WorldBuilderHandler):
    def do_GET(self):
        if self.path.split('?')[0] == '/world-builder/':
            payload = (ROOT / 'scripts/world_builder_home.html').read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        elif self.path == '/favicon.ico':
            self.send_response(204)
            self.end_headers()
        else:
            super().do_GET()

    def _run_native(self, client, body):
        # This test adapter replaces the resident policy at the execution boundary.
        # Validation, snapshots, cognition sealing, commits, logs, SQLite and HTTP are real.
        saved = {key: copy.deepcopy(body[key]) for key in ('turn_offset', 'actor_state', 'resident_memory', 'continue_from', 'rulings') if key in body}
        receipt['native_inputs'].append(saved)
        scripted = copy.deepcopy(body)
        scripted['policy'] = 'scripted'
        return NATIVE_RUN(self, client, scripted)

    def log_message(self, *args):
        pass


# Catalog dispatch names the base method explicitly; patch that exact seam.
service.WorldBuilderHandler._run_native=Handler._run_native

def main():
    with tempfile.TemporaryDirectory(prefix='ws-ui-integration-') as scratch:
        owner = secrets.token_hex(24)
        os.environ.update(LLM_CLIENT_NO_SPEND="1", WORLD_BUILDER_OWNER_PASSWORD=owner, WORLD_BUILDER_RUN_LOG_DIR=scratch+'/runs', WORLD_BUILDER_SHARE_DB=scratch+'/shares.sqlite', WORLD_BUILDER_CATALOG_DB=scratch+'/catalog.sqlite')
        service.BUDGET_STATE_PATH = Path(scratch)/'budget.json'
        service._REQUESTS.clear()
        catalog = service._catalog()
        source = ROOT/'evidence/i0-i1/visible-run-20261113/share.json'
        retained = json.loads(source.read_text())
        pump = catalog.save_world(retained['world'], service._world_fingerprint(retained['world']['bundle'], retained['world']['causal_model']))
        receipt['retained_source'] = {'path': str(source.relative_to(ROOT)), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()}
        bundle=json.loads((ROOT/'examples/world_authoring/orchard-v0.json').read_text())
        causal=json.loads((ROOT/'examples/world_authoring/orchard-causal-v0.json').read_text())
        bundle['world']['label']='Orchard interface fixture'
        for n in range(2,13):
            fruit=copy.deepcopy(bundle['entities'][-1]);fruit['id']='apple-'+str(n);bundle['entities'].append(fruit)
        bundle['actor_information']={'version':1,'public_summary':'A public orchard used only for interface verification.','public_entities':[{'id':e['id'],'label':e['label'],'fields':[]} for e in bundle['entities']], 'actors':{'ava':{'brief':'Pick fruit in this orchard.','initial_knowledge':[],'observable_fields':[]}}}
        definition={'ok':True,'bundle':bundle,'causal_model':causal,'description':'A constructed orchard interface fixture with twelve fruit. Scripted policy verifies persistence, not model behavior.','world_kind':'ongoing','run_stop':{'mode':'every_round'},'review':service.CausalModel.from_dict(causal,bundle=service.validate_bundle(bundle)).as_review()}
        orchard=catalog.save_world(definition,service._world_fingerprint(bundle,causal))
        receipt['fixture_world']=definition
        server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        base=f'http://127.0.0.1:{server.server_port}/world-builder/'
        service.ALLOWED_ORIGINS.add(f'http://127.0.0.1:{server.server_port}')
        def api(path,body=None):
            req=urllib.request.Request(base+'api'+path,headers={service.OWNER_HEADER:owner,'Content-Type':'application/json'},data=json.dumps(body).encode() if body is not None else None)
            with urllib.request.urlopen(req) as res:return json.load(res)
        try:
            try:
                urllib.request.urlopen(base+'api/worlds')
                check('private library rejects unauthenticated read',False)
            except urllib.error.HTTPError as err:
                check('private library rejects unauthenticated read',err.code==403)
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path='/home/brian/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome',headless=True)
                page=browser.new_page(viewport={'width':1440,'height':1100})
                errors=[];failures=[];receipt["console_errors"]=errors;receipt["failed_requests"]=failures
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('requestfailed',lambda req:failures.append({'path':urllib.parse.urlparse(req.url).path,'failure':req.failure}))
                page.on('response',lambda res:receipt['network'].append({'method':res.request.method,'path':urllib.parse.urlparse(res.url).path,'status':res.status}))
                page.add_init_script('(token=>{try{localStorage.setItem("wb-owner",token)}catch(e){}})('+json.dumps(owner)+')')
                page.goto(base)
                page.locator('[data-world-id="'+pump['id']+'"]').wait_for()
                check('starting page has one creation box and private saved worlds',page.locator('#desc').is_visible() and page.locator('#world-cards article').count()==2)
                page.screenshot(path=str(OUT/'library-desktop.png'))
                before=len(receipt['network']);page.locator('[data-world-id="'+pump['id']+'"]').click();page.locator('#world-scene').wait_for(state='visible')
                check('opening retained world without runs is read-only',not any(r['method']=='POST' for r in receipt['network'][before:]) and not api('/worlds/'+pump['id'])['runs'])
                check('initial scene is native composed Living Scene',page.frame_locator('#world-scene').locator('body').inner_text().find('Prototype Pump')>=0)
                page.screenshot(path=str(OUT/'retained-pump-initial.png'))
                page.locator('#workspace-home').click();page.wait_for_function('!document.querySelector("#stage-describe").hidden && !document.querySelector("#library-status").textContent.includes("Loading")');page.locator('[data-world-id="'+orchard['id']+'"]').click();page.locator('#world-scene').wait_for(state='visible')
                page.locator('#workspace-new-run').click()
                page.wait_for_function('document.querySelector("#outcome").textContent.startsWith("Round 1")')
                page.locator('#play-btn').click()
                page.wait_for_function('document.querySelector("#saved-player").hidden === false')
                parent_id=urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)['worldRun'][0]
                parent=api('/worlds/'+orchard['id']+'/runs/'+parent_id)
                check('New run persists native rounds and pause retains committed prefix',len(parent['record']['rounds'])>=1 and parent['run']['checkpoint_id'])
                prefix=len(parent['record']['rounds'])
                page.locator('#workspace-continue').click()
                page.wait_for_function('(n)=>document.querySelector("#outcome").textContent.startsWith("Round "+(n+1))',arg=prefix)
                page.locator('#play-btn').click();page.wait_for_function('document.querySelector("#saved-player").hidden === false')
                parent=api('/worlds/'+orchard['id']+'/runs/'+parent_id)
                check('Continue extends the same run with earlier prefix',len(parent['record']['rounds'])>prefix and parent['run']['id']==parent_id)
                before=len(receipt['network']);page.locator('#workspace-replay').click();page.locator('#saved-player').wait_for(state='visible');page.wait_for_timeout(200)
                check('Replay is read-only',not any(r['method']=='POST' for r in receipt['network'][before:]))
                first_event_count=page.locator('#saved-events button').count();check('only round-end event enables branching',page.locator('#workspace-branch').is_disabled() if first_event_count>1 else page.locator('#workspace-branch').is_enabled())
                cp=parent['checkpoints'][0]
                page.locator('#workspace-checkpoint').select_option(cp['id']);page.locator('#workspace-preview-checkpoint').click();page.wait_for_function('!document.querySelector("#workspace-branch").disabled')
                check('round-end preview enables exact checkpoint branching',page.locator('#saved-round-select').input_value()=='0')
                page.screenshot(path=str(OUT/'checkpoint-desktop.png'))
                prior_inputs=len(receipt['native_inputs']);page.locator('#workspace-branch').click()
                page.wait_for_function('(old)=>!location.href.includes(old)',arg=parent_id)
                page.wait_for_function('document.querySelector("#outcome").textContent.startsWith("Round 2")')
                page.locator('#play-btn').click();page.wait_for_function('document.querySelector("#saved-player").hidden === false')
                child_id=urllib.parse.parse_qs(urllib.parse.urlparse(page.url).query)['worldRun'][0]
                child=api('/worlds/'+orchard['id']+'/runs/'+child_id)
                expected=catalog.resume(parent_id,parent['run']['checkpoint_id'])
                with catalog._db() as db: original_cp=catalog._chain(db,cp['id'])[-1]
                hydrated=receipt['native_inputs'][prior_inputs]
                check('branch ancestry and parent prefix persist',child['run']['parent_run_id']==parent_id and child['run']['fork_checkpoint_id']==cp['id'] and child['record']['rounds'][0]==parent['record']['rounds'][0])
                check('branch restores exact world snapshot and actor cognition',hydrated.get('continue_from')==original_cp['response']['trace']['final_snapshot'] and hydrated.get('actor_state')==original_cp['response']['actor_state'] and hydrated['turn_offset']==1)
                check('branch leaves parent unchanged',api('/worlds/'+orchard['id']+'/runs/'+parent_id)['record']==parent['record'])
                page.frame_locator('#world-scene').locator('[data-kind][data-id]').first.click();page.wait_for_function('document.querySelector("#world-scene-selection").textContent.startsWith("Selected:")');check('scene entity selection reaches parent inspector',page.locator('#world-scene-selection').inner_text().startswith('Selected:'));page.screenshot(path=str(OUT/'branch-desktop.png'))
                # Every visible new control uses the existing styled tooltip system.
                controls=['#workspace-home','#workspace-run','#workspace-new-run','#workspace-continue','#workspace-replay','#workspace-checkpoint','#workspace-preview-checkpoint','#workspace-branch','#saved-round-select']
                for selector in controls:
                    page.locator(selector).hover();page.wait_for_timeout(190);check('styled tooltip '+selector,page.locator('#tip-bubble').is_visible())
                page.mouse.move(0,0);page.wait_for_timeout(200);page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUT/'branch-phone.png'))
                check('390px viewport has no horizontal overflow',page.evaluate('document.body.scrollWidth<=innerWidth'));check('phone first viewport reaches world scene',page.locator('#world-scene').bounding_box()['y']<700)
                page.locator('#workspace-home').click();page.locator('#library-search').fill('orchard');check('library search filters saved worlds',page.locator('#world-cards article').count()==1)
                page.screenshot(path=str(OUT/'library-phone.png'))
                receipt['console_errors']=errors;receipt['failed_requests']=failures
                check('no browser JavaScript errors',not errors);check('no failed network requests',not failures)
                receipt['parent_run']=parent;receipt['child_run']=child
                browser.close()
        finally:
            server.shutdown();server.server_close()
            # Only local fixture requests exist; auth headers are never part of this log.
            logs=Path(scratch)/'runs'
            if logs.exists():(OUT/'run-log.jsonl').write_text(''.join(f.read_text() for f in sorted(logs.glob('*.jsonl'))))
            (OUT/'report.json').write_text(json.dumps(receipt,indent=2)+'\n')

def live_read_only(base):
    """Owner library/scene smoke check. Blocks every API mutation in the browser."""
    token=os.environ.get('WORLD_BUILDER_OWNER_PASSWORD')
    if not token:raise RuntimeError('Set WORLD_BUILDER_OWNER_PASSWORD for the read-only owner check.')
    destination=Path(tempfile.mkdtemp(prefix='ws-workspace-live-readonly-'))
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/home/brian/.cache/ms-playwright/chromium-1254/chrome-linux64/chrome',headless=True)
        page=browser.new_page(viewport={'width':1440,'height':1100});errors=[];blocked=[];responses=[]
        page.on('pageerror',lambda err:errors.append(str(err)))
        page.on('response',lambda res:responses.append({'method':res.request.method,'path':urllib.parse.urlparse(res.url).path,'status':res.status}))
        def guard(route):
            if route.request.method not in ('GET','HEAD','OPTIONS'):
                blocked.append(urllib.parse.urlparse(route.request.url).path);route.abort()
            else:route.continue_()
        page.route('**/api/**',guard)
        page.add_init_script('(token=>{try{localStorage.setItem("wb-owner",token)}catch(e){}})('+json.dumps(token)+')')
        page.goto(base.rstrip('/')+'/');page.wait_for_function('!document.querySelector("#library-status").textContent.includes("Loading")')
        cards=page.locator('#world-cards article');count=cards.count()
        page.screenshot(path=str(destination/'library.png'))
        if count:
            title=cards.first.locator('h3').inner_text();page.locator('#library-search').fill(title);assert cards.count()>=1
            cards.first.get_by_role('button').click();page.locator('#world-scene').wait_for(state='visible',timeout=60000)
            page.screenshot(path=str(destination/'world-desktop.png'));page.set_viewport_size({'width':390,'height':844})
            page.evaluate('document.querySelector("#workspace-run-tools").open=false');page.screenshot(path=str(destination/'world-phone.png'))
            assert page.evaluate('document.body.scrollWidth<=innerWidth')
        browser.close()
    result={'mode':'live read-only; every API mutation blocked','world_count':count,'console_errors':errors,'blocked_mutations':blocked,'network':responses}
    (destination/'report.json').write_text(json.dumps(result,indent=2)+'\n')
    print('Live read-only report (private local output): '+str(destination),flush=True)
    if errors or blocked:raise AssertionError('Unexpected browser error or attempted mutation.')

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser();parser.add_argument('--live',metavar='URL',help='Read-only deployed owner library/scene check; all API POSTs are blocked and output stays in temporary storage.')
    args=parser.parse_args()
    if args.live:live_read_only(args.live)
    else:main()
