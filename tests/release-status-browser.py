"""Controlled browser-only release-status and accessibility check. Not real file/HTTPS acceptance."""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys,traceback
html=Path(sys.argv[1]).read_text();out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
rows=[]
def check(n,fn):
 try:fn();rows.append({'name':n,'status':'passed'})
 except Exception as e:rows.append({'name':n,'status':'failed','reason':str(e)})
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width in (390,1440):
  ctx=browser.new_context(viewport={'width':width,'height':860},offline=True)
  page=ctx.new_page();errors=[];requests=[]
  page.on('pageerror',lambda e:errors.append(str(e)))
  page.on('request',lambda req:requests.append(req.url))
  page.set_content(html,wait_until='load',timeout=30000)
  check(f'{width} startup ready',lambda:page.locator('html[data-app-ready="true"]').wait_for(timeout=20000))
  def release():
   link=page.locator('.release-status a')
   assert 'development preview' in (link.get_attribute('aria-label') or '')
   assert 'not approved for public deployment' in (link.get_attribute('aria-label') or '')
   assert 'Development preview.' in (link.get_attribute('title') or '')
   assert 'v0.20.5-dev' in link.inner_text()
  check(f'{width} release status accessible',release)
  def help_state():
   link=page.locator('.release-status a');link.click()
   qa=page.locator('#release-status-help');qa.wait_for(state='visible')
   qa.locator('summary').click() if not qa.evaluate('(x)=>x.open') else None
   s=qa.inner_text()
   assert 'is a development preview, not an approved release' in s
   assert 'Publisher authentication and independent security review are not complete' in s
   assert 'Physical signing-device and optical-scanning acceptance remain pending' in s
  check(f'{width} help truthfulness',help_state)
  check(f'{width} no runtime errors or network requests',lambda: (_ for _ in ()).throw(AssertionError({'errors':errors,'requests':requests})) if errors or requests else None)
  check(f'{width} no horizontal overflow',lambda: (_ for _ in ()).throw(AssertionError('overflow')) if page.evaluate('document.documentElement.scrollWidth>innerWidth+2') else None)
  ctx.close()
 browser.close()
result={'schema':'tbw-v0205-browser-check-v1','scope':'controlled offline Chromium set_content; not native-origin/physical acceptance','passed':sum(r['status']=='passed' for r in rows),'failed':sum(r['status']=='failed' for r in rows),'results':rows}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(bool(result['failed']))
