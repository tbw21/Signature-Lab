from pathlib import Path
import json,sys,traceback
from playwright.sync_api import sync_playwright
html=Path(sys.argv[1]).read_text();out=Path(sys.argv[2]);report_file=out if out.suffix=='.json' else out/'browser-report.json';shots=out.parent/'privacy-browser-screenshots' if out.suffix=='.json' else out;shots.mkdir(exist_ok=True,parents=True)
report={'suite':'Privacy UX controlled Chromium set_content probe','results':[],'environment':'Chromium setContent only, not file:// or HTTPS browser acceptance'}
def check(name,action):
 try: detail=action();report['results'].append({'name':name,'status':'passed','detail':detail or ''});print('PASSED',name,flush=True)
 except Exception as exc:report['results'].append({'name':name,'status':'failed','detail':traceback.format_exc()});print('FAILED',name,exc,flush=True)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
 for width,height in [(1440,900),(390,844)]:
  ctx=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1,offline=True)
  page=ctx.new_page(); errors=[];requests=[]
  page.on('pageerror',lambda exc:errors.append(traceback.format_exc()))
  page.on('request',lambda req:requests.append(req.url))
  page.set_content(html,wait_until='load',timeout=30000)
  page.wait_for_selector('html[data-app-ready="true"]',timeout=20000)
  def test_start():
   assert page.locator('#supported-scope').is_visible()
   assert page.locator('#wallet-safety').is_visible()
   assert page.locator('.seed-grid li').count() in (12,24)
   assert page.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
   assert not errors,errors
   assert not requests,requests
   page.screenshot(path=str(shots/f'start-{width}.png'),full_page=True)
  check(f'{width}: startup/seed and support scope, no overflow/network/error',test_start)
  def test_sign():
   page.locator('#wallet-loaded').click()
   page.locator('#retain-evidence-before-sign').wait_for(state='visible',timeout=10000)
   evidence=page.locator('#retain-evidence-before-sign')
   print('Evidence visibility',width,evidence.is_visible(), 'step',page.locator('html').get_attribute('data-app-ready'),flush=True)
   assert evidence.is_visible()
   print('Initial checked',width,evidence.is_checked(),flush=True)
   assert not evidence.is_checked()
   evidence.check()
   page.locator('#workspace-session').click()
   print('Mirrored checked',width,page.locator('#retain-evidence').is_checked(),flush=True)
   assert page.locator('#retain-evidence').is_checked()
   page.locator('#finish-testing-open').wait_for(state='visible',timeout=8000)
   assert page.locator('#finish-testing-open').is_visible()
   page.screenshot(path=str(shots/f'session-{width}.png'),full_page=True)
  check(f'{width}: opt-in synchronized across signing and Session views',test_sign)
  def test_close():
   page.locator('#finish-testing-open').click()
   page.locator('#finish-testing-confirm').wait_for(state='visible')
   page.locator('#finish-testing-confirm-button').click()
   page.wait_for_timeout(250)
   assert page.url=='about:blank' or 'Signature Lab testing finished.' in page.locator('body').inner_text()
  check(f'{width}: explicit confirmation retires page',test_close)
  if errors:report['results'].append({'name':f'{width}: uncaught script errors','status':'failed','detail':errors})
  ctx.close()
 browser.close()
report['passed']=len([x for x in report['results'] if x['status']=='passed'])
report['failed']=len([x for x in report['results'] if x['status']=='failed'])
report_file.write_text(json.dumps(report,indent=2));print(json.dumps({'passed':report['passed'],'failed':report['failed']},indent=2))
sys.exit(1 if report['failed'] else 0)
