#!/usr/bin/env python3
"""Critical workflows through real navigation on each available engine, never setContent.
Missing engines / administrator-blocked origins are unavailable, not passes. Software-created
reference responses are labelled fixtures, never physical-device evidence. No permission shim.
"""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright
import threading,json,sys,hashlib,argparse
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('html',type=Path);ap.add_argument('output',type=Path)
ap.add_argument('--require-all',action='store_true',help='Return 3 when any engine/deployment is unavailable')
args=ap.parse_args();file=args.html.resolve();rows=[];expected=hashlib.sha256(file.read_bytes()).hexdigest()
APP="document.querySelector('[x-data]')._x_dataStack[0]"
class Quiet(SimpleHTTPRequestHandler):
    def log_message(self,*args):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(file.parent)))
thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
try:
    with sync_playwright() as p:
        for name in ['chromium','firefox','webkit']:
            runtime=getattr(p,name);binary=Path('/usr/bin/chromium') if name=='chromium' else Path(runtime.executable_path)
            if not binary.is_file():
                rows.append({'name':name+' workflows','status':'unavailable-tool','reason':'Required engine executable absent','workflowsExecuted':False});continue
            try:
                browser=runtime.launch(executable_path=str(binary),headless=True,**({'args':['--no-sandbox']} if name=='chromium' else {}))
            except Exception as exc:
                rows.append({'name':name+' workflows','status':'unavailable-environment','reason':str(exc),'workflowsExecuted':False});continue
            for mode,url in [('file',file.as_uri()),('loopback-http',f'http://127.0.0.1:{server.server_port}/{file.name}')]:
                context=browser.new_context(accept_downloads=True,viewport={'width':1280,'height':900})
                page=context.new_page();errors=[];requests=[];page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('request',lambda r:requests.append(r.url));page.set_default_timeout(6000)
                try:
                    response=page.goto(url,timeout=15000)
                    if response is not None:assert hashlib.sha256(response.body()).hexdigest()==expected,'Served bytes differ from candidate'
                    page.wait_for_function("document.documentElement.dataset.appReady==='true'",timeout=10000)
                    assert page.evaluate('('+APP+').transactionReady'),'Transaction not ready after startup'
                    checkpoints=['normal navigation','known-answer gate and wallet ready']
                    page.locator('#try-example').click();page.locator('#attack-example').wait_for(state='visible')
                    assert 'CHECK COMPLETE' in page.locator('#attack-example').inner_text();page.keyboard.press('Escape')
                    checkpoints.append('recorded example visible and closable')
                    page.locator('#workspace-session').click();page.locator('#session-evidence-tools>summary').click()
                    page.locator('#retain-evidence').check();page.locator('#workspace-test').click()
                    page.locator('#wallet-loaded').click();page.wait_for_function('('+APP+').step===2')
                    page.locator('.stepper button').nth(2).click()
                    assert page.get_by_role('button',name='Scan signed QR',exact=True).is_visible()
                    assert not page.evaluate('('+APP+').scan.active'),'Navigation started camera'
                    checkpoints.append('workspace and unfinished intake with camera off')
                    # This verifies the import/export workflow, NOT the origin of a device signature.
                    fixture=page.evaluate('('+APP+').variants[0].txHex')
                    page.evaluate('(x)=>('+APP+').acceptArtifact(x)',fixture)
                    page.wait_for_function('('+APP+').resultState==="match"')
                    with page.expect_download() as download:page.get_by_role('button',name='Save result',exact=True).click()
                    ev=json.loads(Path(download.value.path()).read_text());assert ev['report']['completed'] and ev['report']['build']['version']==page.evaluate('('+APP+').releaseVersion')
                    page.locator('#workspace-session').click()
                    with page.expect_download() as download:page.get_by_role('button',name='Save session evidence',exact=True).click()
                    bundle=json.loads(Path(download.value.path()).read_text());assert bundle['coverage']['retained']==1
                    checkpoints+=['synthetic signed-response import','current-result download','session-evidence download']
                    assert not errors,errors
                    assert all(r==url for r in requests),requests
                    rows.append({'name':name+'/'+mode+' critical workflows','status':'passed','workflowsExecuted':True,
                        'checkpoints':checkpoints,'browser':browser.version,'secureContext':page.evaluate('isSecureContext'),
                        'origin':url,'physicalSigner':False,'actualPermissionDialog':False,'opticalScan':False})
                except Exception as exc:
                    msg=str(exc);blocked='ERR_BLOCKED_BY_ADMINISTRATOR' in msg
                    rows.append({'name':name+'/'+mode+' critical workflows','status':'unavailable-environment' if blocked else 'failed',
                        'workflowsExecuted':not blocked,'error':msg,'pageErrors':errors,'origin':url})
                finally:context.close()
            browser.close()
finally:server.shutdown();server.server_close();thread.join(timeout=2)
r={'suite':'Normal-origin multi-engine critical workflows','complete':True,'sha256':expected,
   'passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),
   'unavailable':sum(x['status'] not in ('passed','failed') for x in rows),'results':rows,
   'scope':'Per-engine critical software workflows only. Not full retained-suite cross-engine execution, branded Safari/native phones, real camera permissions or physical signer acceptance.'}
with args.output.open('x') as f:json.dump(r,f,indent=2)
print(json.dumps(r,indent=2));sys.exit(1 if r['failed'] else 3 if args.require_all and r['unavailable'] else 0)
