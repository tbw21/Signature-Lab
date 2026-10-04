#!/usr/bin/env python3
"""Onboarding/contents/layout simulation with the actual release DOM and existing demo."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())
def help_home(h):
 h.page.get_by_role('link',name='Help',exact=True).click();h.page.wait_for_timeout(40)
def topic(h,id):
 link=h.page.locator('.help-contents a[href="#'+id+'"]')
 group=link.locator('xpath=ancestor::details[1]')
 if not group.evaluate('(e)=>e.open'):group.locator(':scope > summary').click()
 link.click();h.page.wait_for_timeout(40)
def unchanged(h):return h.call('return JSON.stringify([a.stateSignature,a.psbtBase64,a.variants,a.walletSession,a.walletFingerprint,a.preparedRevision,a.sessionChecks,a.guidedStatus,a.resultState,a.completedAt,a.signingPolicy])')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 environment={'browser':browser.version,'mode':'exact HTML in offline Chromium harness','hardware':False,'optical':False}
 for width in [320,390,438,768,1440]:
  def first(w=width):
   h=Harness(browser,width=w,height=1000);before=unchanged(h)
   assert h.page.locator('#test-purpose').is_visible();assert h.page.locator('#try-example').is_visible()
   assert h.call('return a.demonstration.analysis') is None
   assert h.page.locator('#try-example').get_attribute('aria-haspopup')=='dialog'
   layout(h)
   h.page.locator('#try-example').click();assert h.page.locator('#attack-example').is_visible()
   assert h.page.locator('#attack-example').evaluate('(e)=>e.open')
   assert h.call('return a.demonstration.analysis.evidence.signaturesVerified')==2
   assert 'not a device test' in h.page.locator('#attack-example').inner_text()
   assert unchanged(h)==before;layout(h)
   h.page.get_by_role('button',name='Close example',exact=True).click();assert unchanged(h)==before
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'onboarding-wallet-{w}.png'),full_page=True)
   h.page.locator('#wallet-loaded').click();h.page.locator('#try-example').wait_for(state='hidden');assert h.call('return a.transactionReady')
   layout(h);close(h)
  test(f'Onboarding optional Step-1 example and state-preserving return at {width}px',first)
 for width in [320,390,1440]:
  def links(w=width):
   h=Harness(browser,width=w,height=1100);before=unchanged(h);help_home(h)
   ids=h.page.locator('.help-contents a').evaluate_all('(es)=>es.map(e=>e.getAttribute("href").slice(1))')
   assert len(ids)==22 and len(set(ids))==22
   for id in ids:
    topic(h,id);assert h.page.locator('#'+id).evaluate('(e)=>e.open');assert h.page.evaluate('document.activeElement.parentElement.id')==id
    assert unchanged(h)==before;layout(h)
    h.page.locator('#'+id+' > .help-answer-nav a').click()
    assert h.page.evaluate('document.activeElement.id')=='help-title'
   if w in [390,1440]:
    # Keep one useful category open in the review captures.
    h.page.locator('.help-topic').evaluate_all('(es)=>es.forEach((e,i)=>e.open=i===1)')
    h.page.screenshot(path=str(SHOTS/f'onboarding-help-{w}.png'),full_page=False)
   h.page.get_by_role('link',name='Back to test',exact=True).click();assert unchanged(h)==before;close(h)
  test(f'Help all 22 contents links focus/return without changing test at {width}px',links)
 def keyboard():
  h=Harness(browser,width=390);h.page.locator('#try-example').focus();h.page.keyboard.press('Enter')
  assert h.call('return !!a.demonstration.analysis?.ok')
  h.page.keyboard.press('Escape');help_home(h)
  g=h.page.locator('.help-topic').nth(1);g.locator('summary').focus();h.page.keyboard.press('Enter');assert g.evaluate('(e)=>e.open')
  link=h.page.locator('.help-contents a[href="#orange-result-help"]');link.focus();h.page.keyboard.press('Enter')
  assert h.page.locator('#orange-result-help').evaluate('(e)=>e.open');close(h)
 test('Onboarding keyboard-only example and Help contents work',keyboard)
 for width in [320,1440]:
  def text(w=width):
   h=Harness(browser,width=w,height=1000);h.call('a.selectSeedLength(24)');h.page.wait_for_function('document.querySelectorAll(".seed-grid li").length===24')
   h.page.evaluate(ENLARGE);layout(h);h.page.get_by_role('button',name='Enlarge QR',exact=True).click();layout(h)
   help_home(h)
   for i in range(5):h.page.locator('.help-topic').nth(i).locator('summary').click();layout(h)
   topic(h,'orange-result-help');layout(h);close(h)
  test(f'Onboarding 24 words and enlarged QR/Help with doubled text at {width}px',text)
 def spacing():
  h=Harness(browser,width=390);h.page.add_style_tag(content=TEXT_SPACE);layout(h);help_home(h)
  for i in range(5):h.page.locator('.help-topic').nth(i).locator('summary').click();layout(h)
  close(h)
 test('Help contents and intro reflow with increased text spacing',spacing)
 def result_review():
  h=Harness(browser,width=390);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());before=unchanged(h)
  assert h.call('return a.resultDisplayState')=='review';report=h.call('return a.report()');help_home(h);topic(h,'orange-result-help')
  content=h.page.locator('#orange-result-help').inner_text()
  for phrase in ['File changes need review','Could not complete','not a malware verdict','Save result','More green matches do not erase']:assert phrase in content
  h.page.get_by_role('link',name='Back to test',exact=True).click();assert unchanged(h)==before;assert h.call('return a.report()')==report
  assert h.page.locator('.file-review-action').is_visible();close(h)
 test('Orange-result guidance distinguishes outcomes and never clears real file findings',result_review)
 def incomplete():
  h=Harness(browser,width=390);h.config();h.accept('bad');before=unchanged(h);help_home(h);topic(h,'orange-result-help')
  h.page.get_by_role('link',name='Back to test',exact=True).click();assert unchanged(h)==before;assert h.call('return a.resultState')=='incomplete';close(h)
 test('Help cannot turn an incomplete import into a matching result',incomplete)
 def optional_absence():
  h=Harness(browser);h.page.evaluate('document.querySelector("#help").remove();document.querySelector("#try-example").remove();document.querySelector("#attack-example").remove()')
  d=h.config();h.accept(d['tx']);assert h.call('return a.resultState')=='match';assert h.call('return a.sessionSummary.checked')==1;close(h)
 test('Normal signature check works with optional Help and demo entry absent',optional_absence)
 def history():
  h=Harness(browser,width=390);h.workspace('advanced');before=unchanged(h);help_home(h);topic(h,'known-example')
  h.page.evaluate('history.back()');h.page.wait_for_timeout(50);assert h.page.locator('#help').is_visible()
  h.page.get_by_role('link',name='Back to test',exact=True).click();assert h.call('return a.workspaceView')=='advanced';assert unchanged(h)==before;close(h)
 test('Contents browser history and return preserve Advanced workspace',history)
 def camera():
  h=Harness(browser,width=390,media=True);h.config();h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="scanning"')
  before=h.page.evaluate('mediaCalls');help_home(h);assert not h.call('return a.scan.active');assert h.page.evaluate('testStreams.every(s=>s.getTracks().every(t=>t.readyState==="ended"))')
  topic(h,'known-example');h.page.get_by_role('button',name='Check example',exact=True).click();h.page.get_by_role('button',name='Close example',exact=True).click();h.page.get_by_role('link',name='Back to test',exact=True).click()
  assert not h.call('return a.scan.active');assert h.page.evaluate('mediaCalls')==before;close(h)
 test('Optional example and Help stop capture without reacquiring camera on return',camera)
 def forced():
  h=Harness(browser,width=390);h.page.emulate_media(forced_colors='active');help_home(h);topic(h,'known-example');layout(h);close(h)
 test('Help contents remain navigable in forced-colour mode',forced)
 browser.close()
out={'suite':'Onboarding/help/demo browser integration','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results}
OUT.write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['suite','total_defined','passed','failed']},indent=2));sys.exit(bool(out['failed']))
