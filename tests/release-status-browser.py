"""Version-aware release provenance and Help truthfulness in document-context Chromium.
Unlike historical UI tests, this follows actual visible navigation; no certificate inferred.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
html=Path(sys.argv[1]).read_text();out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
release=json.loads((Path(__file__).resolve().parents[1]/'release.json').read_text());rows=[]
def check(label,fn):
 try:fn();rows.append({'name':label,'status':'passed'})
 except Exception as e:rows.append({'name':label,'status':'failed','reason':repr(e)})
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width in (390,1440):
  ctx=browser.new_context(viewport={'width':width,'height':860},offline=True)
  page=ctx.new_page();page.set_default_timeout(3000);errors=[];requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda req:requests.append(req.url))
  page.set_content(html,wait_until='domcontentloaded',timeout=30000)
  check(f'{width}: startup',lambda:page.locator('html[data-app-ready="true"]').wait_for(timeout=20000))
  def release_visible():
   chip=page.locator('.tbw-version-chip');assert chip.is_visible()
   assert ('v'+release['version']) in chip.inner_text()
   assert 'Preview' in chip.inner_text() and release['status']=='development-ui-preview-unqualified'
   assert release['publisherAuthenticated'] is False
   page.locator('#tbw-settings summary').click()
   text=page.locator('.tbw-drawer-about').inner_text()
   assert 'Development UI preview' in text and 'Publisher authentication has not been verified' in text
  check(f'{width}: unsigned preview identity',release_visible)
  def help_truth():
   page.locator('.tbw-close-settings').click() if page.locator('#tbw-settings').evaluate('(e)=>e.open') else None
   page.locator('.help-control').click()
   qa=page.locator('#release-status-help')
   qa.wait_for(state='visible',timeout=4000)
   if not qa.evaluate('(e)=>e.open'):qa.locator('summary').click()
   text=qa.inner_text()
   assert 'not an approved public release' in text
   assert 'Physical signing-device and optical-scanning acceptance remain pending' in text
   assert 'Publisher authentication and independent security review are not complete' in text
  check(f'{width}: Help release safety disclosure',help_truth)
  check(f'{width}: no network or runtime errors',lambda: (_ for _ in ()).throw(AssertionError({'errors':errors,'requests':requests})) if errors or requests else None)
  check(f'{width}: no page-level overflow',lambda: (_ for _ in ()).throw(AssertionError('overflow')) if page.evaluate('document.documentElement.scrollWidth>innerWidth+2') else None)
  ctx.close()
 browser.close()
result={'suite':'Version-aware unsigned provenance browser contract','passed':sum(x['status']=='passed' for x in rows),'failed':sum(x['status']=='failed' for x in rows),'results':rows,'scope':'Controlled set_content only; not native file/browser origin'}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result));sys.exit(bool(result['failed']))
