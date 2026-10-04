#!/usr/bin/env python3
"""Exact-candidate click/visibility/focus tests; simulated media and signing fixtures only."""
from pathlib import Path
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0],globals())
APP='document.querySelector("[x-data]")._x_dataStack[0]'
def snapshot(h):return h.call('return JSON.stringify([a.stateSignature,a.walletSession,a.wordCount,a.testNumber,a.sessionHistory,a.guidedStatus,a.resultState,a.signingPolicy,a.psbtBase64])')
def settle(h):h.page.wait_for_timeout(90)
def clean(h):
 assert not h.errors,h.errors
 assert not h.requests,h.requests
 h.close()
def fits(h):
 assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 bad=h.page.evaluate('''()=>[...document.querySelectorAll('button,input,textarea,select')].filter(e=>e.checkVisibility()).filter(e=>{let r=e.getBoundingClientRect();return r.x< -1||r.right>innerWidth+1||e.scrollWidth>e.clientWidth+2}).map(e=>[e.id,e.textContent,e.scrollWidth,e.clientWidth])''')
 assert not bad,bad

def used(h):h.page.locator('#wallet-loaded').click();settle(h);h.page.locator('.stepper button').first.click();settle(h)
def ask(h,button='#new-test-wallet'):
 h.page.locator(button).click();h.page.wait_for_function('document.getElementById("wallet-replacement").open');settle(h)
 assert h.page.evaluate('document.activeElement===document.querySelector("[x-ref=keepWallet]")')
def guided(h,n=2):
 h.open_tools();h.page.locator('#guided-setup>summary').click();h.page.locator('#session-count').fill(str(n));h.page.locator('#start-guided-session').click();settle(h)
 assert h.call('return a.guidedStatus.phase')=='receiving'

def end(h):
 h.session_controls();h.page.locator('.guided-end>summary').click();h.page.locator('#end-guided-session').click();settle(h)
 assert h.call('return a.guidedStatus.phase')=='ended'
 assert not h.page.locator('.guided-status').is_visible()

with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for w in [320,360,390,438,768,1024,1440]:
  def wallet(w=w):
   h=Harness(browser,width=w,height=950);settle(h);assert h.page.locator('#new-test-wallet').is_visible();assert not h.page.locator('#wallet-options').count();fits(h)
   assert h.page.locator('#new-test-wallet').bounding_box()['height']>=44
   assert h.page.locator('#word-count-help').evaluate('(e)=>e.previousElementSibling.id==="word-count"')
   assert h.page.locator('.demo-launch').evaluate('(e)=>getComputedStyle(e).borderTopWidth===\"0px\" && getComputedStyle(e).borderBottomWidth===\"0px\"')
   seed=h.call('return a.walletSession');h.page.locator('#new-test-wallet').click();settle(h);assert h.call('return a.walletSession')!=seed
   assert not h.page.locator('#wallet-replacement').is_visible();assert h.call('return a.wordCount')=='12'
   h.page.locator('#word-count button').last.click();h.page.wait_for_function('('+APP+').wordCount==="24" && ('+APP+').seedQrVisible');settle(h)
   assert len(h.page.locator('.seed-grid li').all())==24;fits(h)
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'feedback-wallet-{w}.png'),full_page=True)
   clean(h)
  test(f'FB-B01 visible same-length wallet action and selector reflow at {w}px',wallet)
 for w in [320,390,1440]:
  def demo(w=w):
   h=Harness(browser,width=w,height=950);before=snapshot(h);h.page.locator('#try-example').click();settle(h)
   d=h.page.locator('#attack-example');assert d.is_visible();assert d.evaluate('(e)=>e.matches(":modal")');assert 'does not run malicious firmware' in d.inner_text()
   assert 'CHECK COMPLETE' in d.inner_text();assert '2 of 2' in d.inner_text();assert 'None' in d.inner_text();assert snapshot(h)==before
   d.locator('details>summary').click();raw=h.page.locator('#example-raw').input_value();assert len(raw)>600
   assert raw==h.call('return a.demonstration.analysis.txHex')
   assert hashlib.sha256(bytes.fromhex(raw)).hexdigest()==h.call('return a.demonstration.analysis.evidence.artifactSha256')
   assert h.page.locator('#example-raw').get_attribute('readonly') is not None
   fits(h);d.evaluate('(e)=>e.scrollTop=e.scrollHeight');h.page.keyboard.press('Escape');settle(h);h.page.locator('#try-example').click();settle(h)
   assert d.evaluate('(e)=>e.scrollTop')==0;assert h.page.evaluate('document.activeElement.id')=='example-title';assert snapshot(h)==before
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'feedback-example-{w}.png'))
   h.page.keyboard.press('Escape');settle(h);assert h.page.evaluate('document.activeElement.id')=='try-example';clean(h)
  test(f'FB-B02 one click visibly checks recorded bytes, returns focus and resets demo scroll at {w}px',demo)
 for w in [320,390,1440]:
  def confirmation(w=w):
   h=Harness(browser,width=w,height=950);used(h);s=snapshot(h);ask(h);assert snapshot(h)==s;fits(h)
   for _ in range(6):
    h.page.keyboard.press('Tab');assert h.page.evaluate('document.activeElement===document.body || !!document.activeElement.closest("#wallet-replacement")')
   h.page.keyboard.press('Escape');settle(h);assert snapshot(h)==s;assert not h.call('return a.walletChangePending')
   assert h.page.evaluate('document.activeElement.id')=='new-test-wallet'
   ask(h,'#word-count button:last-child');assert h.call('return a.wordCount')=='12';h.page.get_by_role('button',name='Keep this wallet',exact=True).click();settle(h);assert snapshot(h)==s
   ask(h);h.page.locator('#confirm-new-wallet').click();h.page.wait_for_function('!('+APP+').acknowledged && ('+APP+').step===1');settle(h)
   assert snapshot(h)!=s;assert h.call('return a.wordCount')=='12';assert not h.page.locator('#wallet-replacement').is_visible();fits(h);clean(h)
  test(f'FB-B03 safe replacement and word-length cancel/Escape preserve state at {w}px',confirmation)
 def repeated():
  h=Harness(browser);used(h)
  s=snapshot(h);h.call('a.requestWalletChange();a.cancelWalletChange();a.requestWalletChange(24)');settle(h)
  assert h.page.locator('#wallet-replacement').is_visible();assert h.call('return a.walletChangePending')
  h.page.locator('#confirm-new-wallet').click();settle(h);assert h.call('return a.wordCount')=='24';assert snapshot(h)!=s;clean(h)
 test('FB-B04 queued close event cannot cancel a newer replacement confirmation',repeated)
 for w in [390,1440]:
  def archival(w=w):
   h=Harness(browser,width=w,height=1000);guided(h,30);assert h.page.locator('.guided-status').is_visible();end(h)
   assert h.page.evaluate('document.activeElement.id')=='workspace-session';assert not h.page.locator('.notice:not(.sr-only)').filter(has_text='Session ended').is_visible()
   record=h.call('return a.exportSessionReport()');assert record['status']['notCompleted']==30
   h.workspace('session');h.page.locator('.guided-status').wait_for(state='visible');assert '0 / 30 CHECKED' in h.page.locator('.guided-status-heading').inner_text()
   assert h.page.locator('.history-item[data-finding="ended"]').is_visible()
   with h.page.expect_download() as dl:h.page.locator('#save-history').click()
   payload=json.loads(Path(dl.value.path()).read_text());assert payload['guidedSession']==record
   h.workspace('advanced');assert not h.page.locator('.guided-status').is_visible();assert h.page.locator('.ended-session-next').is_visible()
   h.page.get_by_role('button',name='Go to test wallet',exact=True).click();settle(h);assert h.page.locator('#new-test-wallet').is_visible();ask(h)
   h.page.keyboard.press('Escape');assert h.call('return a.exportSessionReport()')==record
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'feedback-ended-test-{w}.png'),full_page=True)
   clean(h)
  test(f'FB-B05 ended session leaves active workspace, preserves exact record and exposes next path at {w}px',archival)
 def halted():
  h=Harness(browser,width=390);guided(h);h.call('a.signingPolicy="plain";a.checkGuidedBinding()');settle(h)
  assert h.call('return a.guidedStatus.phase')=='halted';assert h.page.locator('.guided-status').is_visible()
  h.call('a.signingPolicy="compatible"');end(h)
  assert h.page.locator('#workspace-session .workspace-alert').is_visible();assert h.call('return a.recordedOperationFailureCount')==1
  h.workspace('session');assert h.page.locator('.history-item[data-finding="incomplete"]').count()>=1
  assert any(e['type']=='control-error' for e in h.call('return a.exportHistory().events'));clean(h)
 test('FB-B06 ended control/capture failure cannot disappear from the Session warning',halted)
 def export_current():
  h=Harness(browser,width=390);d=h.config();h.accept(d['tx']);report=h.call('return a.report()');h.call('a.goToStep(1)');settle(h);ask(h)
  with h.page.expect_download() as dl:h.page.get_by_role('button',name='Save current result',exact=True).click()
  payload=json.loads(Path(dl.value.path()).read_text());assert payload == h.call('return a.exportEvidence()')
  assert h.call('return a.report()')==report;assert h.call('return a.walletChangePending')
  h.page.get_by_role('button',name='Keep this wallet',exact=True).click();settle(h);assert h.call('return a.report()')==report;clean(h)
 test('FB-B07 actual current-evidence download from prompt preserves immutable result and intent',export_current)
 def export_fail():
  h=Harness(browser,width=390);d=h.config();h.accept(d['tx']);h.call('a.goToStep(1)');settle(h);s=snapshot(h);ask(h)
  h.call('a.downloadResult=()=>{a.notice="Download unavailable: injected blocked storage"}')
  h.page.get_by_role('button',name='Save current result',exact=True).click();settle(h)
  assert h.page.locator('#wallet-replacement .notice').is_visible();assert 'blocked storage' in h.page.locator('#wallet-replacement .notice').inner_text();assert snapshot(h)==s
  h.page.keyboard.press('Escape');clean(h)
 test('FB-B08 export failure remains visible inside confirmation instead of behind it',export_fail)
 def stale():
  h=Harness(browser);used(h);ask(h);h.call('a.fileRequest++');seed=h.call('return a.seed.value');h.page.locator('#confirm-new-wallet').click();settle(h)
  assert h.call('return a.seed.value')==seed;assert 'changed while confirmation' in h.call('return a.notice');assert not h.page.locator('#wallet-replacement').is_visible();clean(h)
 test('FB-B09 changed import generation invalidates pending wallet replacement visibly',stale)
 def pause():
  h=Harness(browser);used(h);ask(h);seed=h.call('return a.seed.value');h.page.evaluate('dispatchEvent(new PageTransitionEvent("pagehide",{persisted:true}))');settle(h)
  assert not h.call('return a.walletChangePending');assert not h.page.locator('#wallet-replacement').is_visible()
  h.page.evaluate('dispatchEvent(new PageTransitionEvent("pageshow",{persisted:true}))');settle(h);assert h.call('return a.seed.value')==seed;assert not h.call('return a.scan.active');clean(h)
 test('FB-B10 page restoration cannot revive a destructive confirmation or camera',pause)
 def missing():
  h=Harness(browser);used(h);h.page.evaluate('document.getElementById("wallet-replacement").remove()');s=snapshot(h);h.page.locator('#new-test-wallet').click();settle(h)
  assert snapshot(h)==s;assert 'confirmation is unavailable' in h.call('return a.notice');clean(h)
 test('FB-B11 absent confirmation blocks used-wallet reset rather than silently replacing it',missing)
 def demo_failure():
  h=Harness(browser);s=snapshot(h);h.call('a.runDemonstration=()=>{a.demonstration.analysis=null;a.demonstration.error="Injected verifier exception"}');h.page.locator('#try-example').click();settle(h)
  assert 'Injected verifier exception' in h.page.locator('#attack-example').inner_text();assert 'CHECK COMPLETE' not in h.page.locator('#attack-example').inner_text();assert snapshot(h)==s;h.page.keyboard.press('Escape');clean(h)
 test('FB-B12 demo error has a visible failure and never an expected-result success',demo_failure)
 def camera():
  h=Harness(browser,media=True);h.config();h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="scanning"');before=h.page.evaluate('mediaCalls');s=snapshot(h)
  assert h.call('return a.openExample()')==False;assert h.call('return a.requestWalletChange()')==False;assert snapshot(h)==s;assert h.page.evaluate('mediaCalls')==before;h.call('a.stopScan()');clean(h)
 test('FB-B13 optional overlays cannot hide a live camera or request another stream',camera)
 for w in [320,390,1440]:
  def large(w=w):
   h=Harness(browser,width=w,height=950);h.page.evaluate('''()=>{for(const e of document.querySelectorAll('body *'))if(!['STYLE','SCRIPT','TEMPLATE'].includes(e.tagName))e.style.fontSize=(parseFloat(getComputedStyle(e).fontSize)*2)+'px'}''');settle(h);fits(h)
   used(h);ask(h);fits(h);h.page.keyboard.press('Escape');h.page.locator('#try-example').click();settle(h);fits(h);h.page.keyboard.press('Escape');clean(h)
  test(f'FB-B14 doubled text fits wallet controls and both dialogs at {w}px',large)
 def themes():
  h=Harness(browser,width=390);h.page.emulate_media(forced_colors='active',reduced_motion='reduce');used(h);ask(h);fits(h);h.page.keyboard.press('Escape');h.page.locator('#try-example').click();settle(h);fits(h);h.page.keyboard.press('Escape');clean(h)
 test('FB-B15 forced colors/reduced motion preserve discernible dialogs and actions',themes)
 def completed_plan():
  h=Harness(browser);guided(h,1);h.call('a.acknowledged=true;a.acceptArtifact(a.variants[0].txHex)');settle(h);assert h.call('return a.guidedStatus.phase')=='complete'
  assert h.page.locator('.guided-status').is_visible();h.call('a.goToStep(1)');settle(h);assert h.page.locator('#new-test-wallet').is_disabled()
  end(h);assert not h.page.locator('#new-test-wallet').is_disabled();clean(h)
 test('FB-B16 completed plan retains explicit end/locks before wallet replacement is available',completed_plan)
 browser.close()
r={'suite':'Feedback outcome/replacement browser integration','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results};OUT.write_text(json.dumps(r,indent=2));print(json.dumps({k:r[k] for k in ['suite','total_defined','passed','failed']}));sys.exit(bool(r['failed']))
