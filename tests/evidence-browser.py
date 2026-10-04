#!/usr/bin/env python3
"""Exact HTML, controlled Chromium, synthetic response/camera fixtures; no hardware claims."""
from pathlib import Path
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0],globals())
APP='document.querySelector("[x-data]")._x_dataStack[0]'
def tools(h):
 h.workspace('session');d=h.page.locator('#session-evidence-tools')
 if not d.evaluate('(e)=>e.open'):d.locator(':scope>summary').click()
def enable(h):tools(h);h.page.locator('#retain-evidence').check();assert h.call('return a.retentionStatus.enabled')
def finish(h):
 tx=h.call('return a.variants[0].txHex');h.accept(tx);assert h.call('return a.resultState')=='match'
def unchanged(h):return h.call('return JSON.stringify([a.stateSignature,a.walletSession,a.sessionSummary,a.resultState,a.signingPolicy])')
def close(h):assert not h.errors,h.errors;assert not h.requests,h.requests;h.close()
def fits(h):
 assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
 for el in h.page.locator('#session-evidence-tools button,#session-evidence-tools input').all():
  if el.is_visible():
   b=el.bounding_box();assert b['x']>=-1 and b['x']+b['width']<=h.page.viewport_size['width']+1
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width in [320,390,768,1440]:
  def layout(width=width):
   h=Harness(browser,width=width,height=900);assert not h.page.locator('#session-evidence-tools').is_visible();before=unchanged(h);tools(h)
   assert not h.page.locator('#retain-evidence').is_checked();assert unchanged(h)==before;fits(h)
   if width in [390,1440]:h.page.screenshot(path=str(SHOTS/f'evidence-session-{width}.png'),full_page=True)
   h.workspace('test');assert not h.page.locator('#session-evidence-tools').is_visible();assert unchanged(h)==before;close(h)
  test(f'EB01 optional Session-only controls preserve calm default at {width}px',layout)
 def download():
  h=Harness(browser);h.config();enable(h);h.workspace('test');finish(h);original=h.call('return a.exportEvidence()');h.call("a.randomizeTransaction('small')");finish(h);tools(h)
  with h.page.expect_download() as d:h.page.get_by_role('button',name='Save session evidence',exact=True).click()
  bundle=json.loads(Path(d.value.path()).read_text());assert bundle['coverage']['retained']==2
  assert json.loads(bundle['events'][0]['evidenceJson'])==original
  for slot in bundle['events']:
   text=slot['evidenceJson'].encode();assert hashlib.sha256(text).hexdigest()==slot['sha256'];assert len(text)==slot['bytes']
  assert 'current original response' not in d.value.suggested_filename
  (SHOTS/'browser-session-evidence.json').write_text(json.dumps(bundle));close(h)
 test('EB02 actual two-response session JSON download retains original immutable evidence',download)
 def toggle():
  h=Harness(browser);h.config();finish(h);enable(h);h.call("a.randomizeTransaction('small')");finish(h);tools(h)
  assert h.page.locator('#evidence-coverage').inner_text().startswith('1 of 2');assert 'Incomplete' in h.page.locator('#evidence-coverage').inner_text()
  h.page.locator('#retain-evidence').uncheck();assert h.call('return a.retentionStatus.retained')==1;close(h)
 test('EB03 enabling later reports missing earlier evidence and disabling does not delete',toggle)
 def secretfree():
  h=Harness(browser);h.config();finish(h);tools(h);h.page.locator('#session-evidence-tools details>summary').click()
  with h.page.expect_download() as d:h.page.locator('#session-evidence-tools').get_by_role('button',name='Save diagnostics',exact=True).click()
  doc=json.loads(Path(d.value.path()).read_text());assert doc['includedResponse'] is False;assert 'evidence' not in doc;assert h.call('return a.seed.value') not in json.dumps(doc)
  h.page.locator('#diagnostic-response').check()
  with h.page.expect_download() as d:h.page.locator('#session-evidence-tools').get_by_role('button',name='Save diagnostics',exact=True).click()
  doc=json.loads(Path(d.value.path()).read_text());assert doc['includedResponse'] is True;assert doc['evidence']==h.call('return a.exportEvidence()');close(h)
 test('EB04 diagnostics default excludes bytes; explicit inclusion preserves current evidence',secretfree)
 def capture():
  h=Harness(browser,media=True);h.config();enable(h);h.workspace('test')
  h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="scanning"');h.call('a.stopScan();a.stopScan()')
  entries=h.call('return a.sessionHistory');assert len(entries)==1 and entries[0]['outcome']=='stopped';assert h.call('return a.sessionSummary.checked')==0;assert h.call('return a.retentionStatus.captures')==1
  assert h.page.evaluate('mediaCalls')==1;close(h)
 test('EB05 one terminal capture record, no duplicate on stop and no signature-count inflation',capture)
 def capture_error():
  h=Harness(browser,media=True);h.config();enable(h);h.workspace('test')
  h.page.evaluate("() => {navigator.mediaDevices.getUserMedia=async()=>{throw new DOMException('synthetic denial','NotAllowedError')};}")
  h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="failed"')
  entries=h.call('return a.sessionHistory');assert len(entries)==1 and entries[0]['outcome']=='failed';assert h.call('return a.recordedOperationFailureCount')==1
  assert h.call('return a.sessionSummary.checked')==0;assert 'synthetic denial' not in json.dumps(h.call('return a.diagnosticPackage()'));close(h)
 test('EB06 denied synthetic permission recorded without auto-retry or untrusted error-text export',capture_error)
 def capture_success():
  h=Harness(browser,media=True);data=h.config();enable(h);h.workspace('test');h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="scanning"')
  h.call("a.acceptArtifact(arg,{method:'camera',transport:{frames:1,family:'binary'}})",data['tx'])
  entries=h.call('return a.sessionHistory');assert entries[0]['outcome']=='received';assert entries[1]['type']=='check';assert h.call('return a.sessionSummary.checked')==1
  assert h.call('return a.retentionStatus.retained')==1;assert not h.call('return a.scan.active');close(h)
 test('EB07 received capture and signature result are separate events with one retained response',capture_success)
 def replacement():
  h=Harness(browser);h.config();enable(h);h.workspace('test');finish(h);h.page.locator('.stepper button').first.click();h.page.locator('#new-test-wallet').click()
  d=h.page.locator('#wallet-replacement');d.wait_for(state='visible')
  with h.page.expect_download() as download:d.get_by_role('button',name='Save session evidence',exact=True).click()
  saved=json.loads(Path(download.value.path()).read_text());assert saved['coverage']['retained']==1;old=h.call('return a.walletSession')
  d.get_by_role('button',name='Keep this wallet',exact=True).click();assert h.call('return a.walletSession')==old;assert h.call('return a.retentionStatus.retained')==1;close(h)
 test('EB08 full-session export is available before confirming wallet replacement',replacement)
 def exportfailure():
  h=Harness(browser);h.config();enable(h);h.workspace('test');finish(h);before=unchanged(h)
  h.page.evaluate("() => {URL.createObjectURL=()=>{throw Error('synthetic download failure')};}");h.call('a.downloadSessionEvidence()')
  assert 'download failed' in h.call('return a.notice');assert unchanged(h)==before;assert h.call('return a.retentionStatus.retained')==1;close(h)
 test('EB09 download failure leaves retained responses and main result intact',exportfailure)
 def largefont():
  h=Harness(browser,width=320);tools(h);h.page.add_style_tag(content='#session-evidence-tools{font-size:200%} #session-evidence-tools input{max-width:100%}')
  fits(h);h.page.keyboard.press('Tab');close(h)
 test('EB10 Session evidence controls reflow at narrow width with enlarged text',largefont)
 def reset():
  h=Harness(browser);h.config();enable(h);h.workspace('test');finish(h);h.page.locator('.stepper button').first.click();h.page.locator('#new-test-wallet').click();h.page.locator('#confirm-new-wallet').click()
  h.page.wait_for_function('('+APP+').retentionStatus.retained===0');assert h.call('return a.retentionStatus.enabled') is False;assert h.call('return a.diagnosticIncludeResponse') is False;close(h)
 test('EB11 confirmed new wallet clears the tab evidence and resets explicit consent',reset)
 def absence():
  html=re.sub(r'<details class="details" id="session-evidence-tools">.*?</div></details>(?=<div class="history-list")','',HTML,flags=re.S)
  h=Harness(browser,html=html);h.config();finish(h);assert h.call('return a.sessionSummary.matched')==1;close(h)
 test('EB12 optional evidence-control absence cannot block core signature verification',absence)
 def paired_guided_capture():
  h=Harness(browser,media=True);h.config();enable(h);h.call("a.sessionCount='2';a.startGuidedSession()");h.workspace('test')
  h.page.evaluate("() => {navigator.mediaDevices.getUserMedia=async()=>{throw new DOMException('synthetic denial','NotAllowedError')};}")
  h.call('a.startScan()');h.page.wait_for_function('('+APP+').guidedStatus.phase==="halted"')
  entries=h.call('return a.sessionHistory');assert [e['type'] for e in entries]==['capture-attempt','capture-error']
  assert h.call('return a.recordedOperationFailureCount')==1;assert h.call('return a.retentionStatus.captures')==1
  assert h.call('return a.sessionSummary.checked')==0;h.call('a.endGuidedSession()');assert h.call('return a.recordedOperationFailureCount')==1;close(h)
 test('EB13 guided capture diagnostic and halt retain both events but count one stopped operation',paired_guided_capture)
 def visible_limit():
  # Labelled fault copy with a one-byte logical quota, not changed release bytes.
  token='bytes:16*1024*1024';assert HTML.count(token)==1
  h=Harness(browser,html=HTML.replace(token,'bytes:1',1));h.config();enable(h);h.workspace('test');finish(h)
  assert h.call('return a.resultState')=='match' and h.call('return a.retentionStatus.fault')=='byte-limit'
  for view in ['test','advanced','session']:
   h.workspace(view);h.page.locator('#retention-warning').wait_for(state='visible')
   assert 'retention stopped' in h.page.locator('#retention-warning').inner_text()
  tools(h);assert 'Incomplete' in h.page.locator('#evidence-coverage').inner_text()
  h.page.locator('#retain-evidence').uncheck();assert h.page.locator('#retain-evidence').is_disabled()
  assert h.call('return a.retentionStatus.fault')=='byte-limit';assert h.call('return a.exportEvidence().report.completed') is True;close(h)
 test('EB14 retention failure remains visible across views without changing a signature match or resetting its latch',visible_limit)
 def diagnostic_surface_default():
  h=Harness(browser);h.config();finish(h);tools(h);h.page.locator('#session-evidence-tools details>summary').click()
  h.page.locator('#diagnostic-response').check();h.workspace('test');h.open_evidence()
  with h.page.expect_download() as d:h.page.locator('#result-tools').get_by_role('button',name='Save diagnostics',exact=True).click()
  package=json.loads(Path(d.value.path()).read_text());assert package['includedResponse'] is False and 'evidence' not in package
  assert h.call('return a.diagnosticIncludeResponse') is True;close(h)
 test('EB15 diagnostic action outside Session stays response-free despite an earlier Session inclusion choice',diagnostic_surface_default)
 browser.close()
r={'suite':'Session evidence and diagnostic browser workflows','complete':True,'total_defined':test_index,'test_range':':'.join(TEST_RANGE),'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results}
OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
