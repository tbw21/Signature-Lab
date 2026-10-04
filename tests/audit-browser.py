#!/usr/bin/env python3
"""Actual current DOM/download checks with synthetic signed responses; no physical device."""
from pathlib import Path
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0],globals())
from playwright.sync_api import TimeoutError as PlaywrightTimeout

def maps(raw):
 pos=5;out=[]
 while pos<len(raw):
  pairs=[]
  while True:
   n,pos=readcompact(raw,pos)
   if n==0:break
   key=raw[pos:pos+n];pos+=n;n,pos=readcompact(raw,pos);val=raw[pos:pos+n];pos+=n;pairs.append((key,val))
  out.append(pairs)
 assert pos==len(raw)
 return out

def pack(groups):return b'psbt\xff'+b''.join(b''.join(compact(len(k))+k+compact(len(v))+v for k,v in group)+b'\0' for group in groups)
def response(h,kind='normal',version=2):
 d=h.config()
 if version==0:
  h.call("a.invalidate();a.psbtVersion='0';a.recompute()");d=h.call('return {psbt:a.psbtBase64,tx:a.variants[0].txHex}')
 m=maps(sign_psbt(d['psbt'],d['tx']))
 if kind=='reduced-sighash':
  for i in [1,2]:m[i]=[(k,v) for k,v in m[i] if k[0] in [2,14,15,16]]+[(b'\3',b'\1\0\0\0')]
  m[3]=[(k,v) for k,v in m[3] if k[0] in [3,4]]
 elif kind=='reordered':m=[list(reversed(g)) for g in m]
 elif kind=='review':m[0].append((b'\xfc\x01x\x00',b'fixture'))
 elif kind=='many-fields':m[0]+=[(b'\xfa'+i.to_bytes(2,'big'),b'\0') for i in range(4000)]
 elif kind=='long-key':m[0].append((b'\xfa'+b'a'*400000,b'fixture'))
 return pack(m)
def clean(h):
 assert not h.errors,h.errors
 assert not h.requests,h.requests
 h.close()
def fit(h):
 assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
def snapshot(h):return h.call('return JSON.stringify([a.stateSignature,a.walletSession,a.signingPolicy,a.sessionHistory,a.resultState])')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for version in [0,2]:
  def reduced(version=version):
   h=Harness(browser,width=390);b=response(h,'reduced-sighash',version);h.accept(b.hex())
   h.page.locator('.result[data-result-state="match"]').wait_for(state='visible')
   assert h.call('return a.metadataSummary.reducedResponse && a.metadataSummary.unexpected===0')
   assert h.call('return a.report().session.matched===1 && a.report().session.review===0')
   h.file_details();assert h.page.locator('.metadata-summary').inner_text()=='Reduced signing response';fit(h);clean(h)
  test(f'SA-B01 reduced plus ALL visibly matches and exports consistent counts v{version}',reduced)
 for width in [390,1440]:
  def order(width=width):
   h=Harness(browser,width=width);b=response(h,'reordered');h.accept(b.hex());assert h.call('return a.resultDisplayState')=='match'
   h.file_details();note=h.page.locator('.metadata-order-note');note.wait_for(state='visible');assert 'changed order' in note.inner_text();assert 'not proof' in note.inner_text()
   before=snapshot(h)
   with h.page.expect_download() as info:h.page.get_by_role('button',name='Save result',exact=True).click()
   report=json.loads(Path(info.value.path()).read_text());meta=report['report']['metadata'];assert meta['fieldOrderChanged']>=2;assert all('afterPosition' in f for f in meta['fields'])
   assert snapshot(h)==before;fit(h);clean(h)
  test(f'SA-B02 ordering is informational, complete positions exported at {width}px',order)
 for width in [320,390,1440]:
  def review(width=width):
   h=Harness(browser,width=width);b=response(h,'review');h.accept(b.hex());h.page.locator('.result[data-result-state="review"]').wait_for(state='visible')
   h.workspace('session');h.page.locator('#session-view').wait_for(state='visible')
   text=h.page.locator('.session-outcomes').inner_text();assert '0 matched' in text and '1 needs review' in text and '0 differed' in text,text
   with h.page.expect_download() as info:h.page.locator('#save-history').click()
   record=json.loads(Path(info.value.path()).read_text());assert record['summary']['review']==1 and record['summary']['matched']==0
   assert record['events'][0]['metadataStatus']=='unexpected';fit(h)
   if width in [390,1440]:h.page.screenshot(path=str(SHOTS/f'audit-session-{width}.png'),full_page=True)
   clean(h)
  test(f'SA-B03 metadata review is not counted as clean match in UI/download at {width}px',review)
 for width in [320,390,1440]:
  def capped(width=width):
   h=Harness(browser,width=width);b=response(h,'many-fields');h.accept(b.hex())
   assert h.call('return a.resultDisplayState')=='review';h.file_details();h.page.get_by_text('Inspect unexpected changes',exact=True).click()
   h.page.locator('.metadata-fields>p').first.wait_for(state='visible')
   assert h.page.locator('.metadata-fields>p').count()==32
   assert '32 of 4000' in h.page.locator('.metadata-display-limit').inner_text()
   assert h.call('return a.exportEvidence().report.metadata.fields.filter(f=>f.classification==="unexpected").length')==4000
   assert h.page.locator('.metadata-fields *').count()<300;fit(h)
   if width==390:h.page.screenshot(path=str(SHOTS/'audit-capped-390.png'),full_page=True)
   clean(h)
  test(f'SA-B04 four thousand hostile fields assess fully but render only 32 rows at {width}px',capped)
 def long_key():
  h=Harness(browser,width=390);b=response(h,'long-key');assert len(b)<512*1024;h.accept(b.hex());assert h.call('return a.resultDisplayState')=='review'
  h.file_details();h.page.get_by_text('Inspect unexpected changes',exact=True).click();h.page.locator('.metadata-fields>p').first.wait_for(state='visible')
  t=h.page.locator('.metadata-fields').inner_text();assert len(t)<500 and '…' in t
  with h.page.expect_download() as info:h.page.get_by_role('button',name='Save result',exact=True).click()
  r=json.loads(Path(info.value.path()).read_text());assert max(len(f['key']) for f in r['report']['metadata']['fields'])>700000
  fit(h);clean(h)
 test('SA-B05 large attacker key remains complete in evidence but bounded in rendered text',long_key)
 def hostile_text():
  h=Harness(browser,width=390);b=response(h,'review');h.accept(b.hex());before=snapshot(h)
  h.call("Object.defineProperty(a,'metadataSummary',{get:()=>({status:'unexpected',fields:[{scope:'global',index:null,field:'<img src=x onerror=alert(1)>',key:'aa',classification:'unexpected',change:'added',reason:'<script>window.bad=true</script>'}]})})")
  h.file_details();h.page.get_by_text('Inspect unexpected changes',exact=True).click()
  assert h.page.locator('.metadata-fields img,.metadata-fields script').count()==0
  assert h.page.evaluate('window.bad===undefined');assert snapshot(h)==before;clean(h)
 test('SA-B06 hostile display strings stay text nodes and cannot change current state',hostile_text)
 for mode in ['present','throwing-getter']:
  def agent(mode=mode):
   body="window.agentReads=0;window.agentCalls=0;Object.defineProperty(document,'modelContext',{configurable:true,get(){agentReads++;"+ ("throw new Error('unexpected agent access');" if mode=='throwing-getter' else "return {registerTool(){agentCalls++}};")+"}});"
   fixture=HTML.replace('<head>','<head><script>'+body+'</script>',1)
   h=Harness(browser,html=fixture,width=390);assert h.page.evaluate('agentReads===0 && agentCalls===0');assert h.call('return !!a.seed.value');clean(h)
  test('SA-B07 no automatic browser-agent access even when API is '+mode,agent)
 def delayed_box():
  h=Harness(browser,width=390);h.page.locator('#wallet-loaded').click();h.page.locator('.sign-layout>.qr-column .qr-frame').wait_for(state='visible')
  h.page.evaluate("()=>{const e=document.querySelector('.sign-layout>.qr-column .qr-frame');e.style.setProperty('display','none','important');window.fixtureReady=true;setTimeout(()=>e.style.removeProperty('display'),200)}")
  h.page.wait_for_function('fixtureReady');old=h.page.locator('.sign-layout>.qr-column .qr-frame').evaluate('(e)=>e.getBoundingClientRect().width');assert old==0
  # The actual corrected helper is loaded, not a copied replacement.
  namespace=dict(globals());txt=(Path(__file__).parent/'polish-browser.py').read_text();helper=txt[txt.index('def box(h,s):'):txt.index('def same_edges')];exec(helper,namespace)
  box=namespace['box'](h,'.sign-layout>.qr-column .qr-frame');assert box['width']>100;clean(h)
 test('SA-B08 reactive-ready zero box reproduced, corrected geometry helper waits for actual visibility',delayed_box)
 def never_visible():
  h=Harness(browser,width=390);h.page.set_default_timeout(200)
  namespace=dict(globals());txt=(Path(__file__).parent/'polish-browser.py').read_text();exec(txt[txt.index('def box(h,s):'):txt.index('def same_edges')],namespace)
  caught=None
  try:namespace['box'](h,'.sign-layout>.qr-column .qr-frame')
  except PlaywrightTimeout as e:caught=str(e)
  assert caught and 'visible' in caught;clean(h)
 test('SA-B09 never-visible geometry is a bounded failure, not accepted as zero size',never_visible)
 def intact():
  h=Harness(browser,width=390,media=True);b=response(h,'normal');h.accept(b.hex());before=snapshot(h)
  h.workspace('advanced');h.workspace('session');h.workspace('test');h.open_evidence()
  assert snapshot(h)==before;assert h.page.evaluate('mediaCalls')==0
  h.page.locator('#workspace-test').click();h.page.locator('.stepper button').first.click();h.page.locator('#try-example').click()
  h.page.locator('#attack-example').wait_for(state='visible');assert snapshot(h)==before
  assert 'CHECK COMPLETE' in h.page.locator('#attack-example').inner_text();h.page.keyboard.press('Escape');clean(h)
 test('SA-B10 navigation and recorded example preserve current evidence with no camera acquisition',intact)
 def unknown():
  h=Harness(browser,width=390);b=response(h,'review');h.accept(b.hex());assert h.call('return a.sessionSummary.matched')==0
  h.workspace('session');h.page.evaluate("document.querySelector('.session-outcomes').style.fontSize='26px'");fit(h);clean(h)
 test('SA-B11 enlarged outcome labels reflow without hiding review count',unknown)
 def normal():
  h=Harness(browser,width=1440);b=response(h,'normal');h.accept(b.hex());assert h.call('return a.sessionSummary.matched===1 && a.sessionSummary.review===0');h.file_details()
  assert h.call('return a.metadataSummary.fieldOrderChanged')==0
  assert h.page.locator('.metadata-display-limit').is_visible() is False;clean(h)
 test('SA-B12 ordinary result has no added warning or truncation notice',normal)
 def preserved():
  h=Harness(browser,width=390);b=response(h,'review');h.accept(b.hex());original=h.call('return JSON.stringify(a.exportEvidence())');before=snapshot(h)
  h.workspace('session')
  with h.page.expect_download() as info:h.page.locator('#save-history').click()
  text=Path(info.value.path()).read_text();assert 'distinct-transaction-worst-observed-v2' in text
  assert original==h.call('return JSON.stringify(a.exportEvidence())');assert before==snapshot(h);clean(h)
 test('SA-B13 current result is immutable after session export with changed counting semantics',preserved)
 def ui():
  h=Harness(browser,width=390);h.page.emulate_media(forced_colors='active',reduced_motion='reduce');b=response(h,'many-fields');h.accept(b.hex());h.file_details();h.page.get_by_text('Inspect unexpected changes',exact=True).click();fit(h)
  assert h.page.locator('.metadata-fields>p').count()==32;assert h.call('return a.report().metadata.unexpected')==4000;clean(h)
 test('SA-B14 high-contrast result retains warning and capped full-count explanation',ui)
 browser.close()
r={'suite':'Source audit exact-DOM metadata summary privacy and synchronization','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':{'physicalSigner':False,'realOpticalScan':False,'origin':'offline Chromium exact HTML; labelled agent/timing fixtures'},'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results};OUT.write_text(json.dumps(r,indent=2));print('TOTAL',r['passed'],r['failed'],'DEFINED',test_index);sys.exit(bool(r['failed']))
