#!/usr/bin/env python3
"""Current candidate: non-scrolling navigation, unfinished intake and physical-workflow boundaries.
Actual DOM/QR pixels with synthetic streams and responses; never a hardware claim.
"""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())
def pos(h,s):return h.page.locator(s).evaluate('(e)=>{let r=e.getBoundingClientRect();return {x:r.x,y:r.y,top:r.top+scrollY,right:r.right,bottom:r.bottom,w:r.width,h:r.height}}')
def state(h):return h.call('return JSON.stringify([a.seed,a.walletSession,a.stateSignature,a.psbtBase64,a.signingPolicy,a.variants,a.preparedRevision,a.sessionHistory,a.guidedStatus,a.resultState,a.completedAt,a.artifactText])')
def stable(h):h.page.wait_for_timeout(75)
def camera_count(h):return h.page.evaluate('window.mediaCalls||0')
def spy(h):h.page.evaluate('''() => { window.scrollRequests=[]; const prev=Element.prototype.scrollIntoView;
 Element.prototype.scrollIntoView=function(...args){scrollRequests.push(this.id||this.tagName);return prev.apply(this,args)}; }''')
def notscroll(h):assert h.page.evaluate('scrollRequests.length')==0,h.page.evaluate('scrollRequests')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 environment={'browser':browser.version,'origin':'offline exact candidate setContent','camera':'synthetic canvas stream','physicalSigner':False,'realOpticalScan':False}
 for w in [320,360,390,438,768,1024,1440]:
  def nav(w=w):
   h=Harness(browser,width=w,height=1000,media=True);h.page.locator('#wallet-loaded').click();stable(h);h.page.evaluate('window.scrollTo(0,0)');spy(h)
   before=state(h);anchor=pos(h,'.workspace-heading')['top'];pane=None
   for idx in [2,0,1,2]:
    h.page.locator('.stepper>button').nth(idx).click();stable(h)
    assert h.call('return a.step')==idx+1;assert abs(pos(h,'.workspace-heading')['top']-anchor)<1
    top=pos(h,'.panel:visible')['top']
    if pane is None:pane=top
    else:assert abs(top-pane)<1,(pane,top)
    assert state(h)==before;notscroll(h);assert camera_count(h)==0;layout(h)
    if idx==2:assert h.page.locator('.intake').is_visible()
   h.call('a.goToStep(1)');stable(h)
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'delivery-wallet-{w}.png'),full_page=True)
   close(h)
  test(f'Delivery left navigation fixed alignment no scroll/camera/state change at {w}px',nav)
 for w in [320,390,768,1440]:
  def wallet(w=w):
   h=Harness(browser,width=w,height=1100)
   for words in [12,24]:
    if words==24:h.page.get_by_role('button',name='24 words',exact=True).click();stable(h)
    q=pos(h,'#word-count');hint=pos(h,'#word-count-help');assert hint['y']>=q['bottom'] and abs(hint['x']-q['x'])<1,(q,hint)
    assert h.page.locator('.seed-scan').evaluate('(e)=>getComputedStyle(e).backgroundColor')=='rgba(0, 0, 0, 0)'
    assert h.page.locator('.seed-scan').evaluate('(e)=>getComputedStyle(e).borderTopColor')=='rgba(0, 0, 0, 0)'
    pixel=h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(e)=>e.toDataURL()')
    assert len(read_qr(Image.open(io.BytesIO(base64.b64decode(pixel.split(',')[1]))))[0].data)==4*words
    s=state(h);h.page.get_by_role('button',name='Enlarge QR',exact=True).click();stable(h);layout(h)
    assert h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(e)=>e.toDataURL()')==pixel;assert state(h)==s
    qr=pos(h,'#seed-qr-display');card=pos(h,'#wallet-load-card');assert abs(qr['x']-card['x'])<1 and abs(qr['right']-card['right'])<1
    if w==1440 and words==12:h.page.screenshot(path=str(SHOTS/'delivery-enlarged-1440.png'),full_page=True)
    h.page.get_by_role('button',name='Reduce QR',exact=True).click();stable(h)
   close(h)
  test(f'Delivery helper placement borderless QR and preserved 12/24 QR pixels at {w}px',wallet)
 for w in [320,390,1440]:
  def big(w=w):
   h=Harness(browser,width=w,height=1100);h.page.get_by_role('button',name='24 words',exact=True).click();stable(h);h.page.evaluate(ENLARGE);layout(h)
   for s in ['#word-count','#word-count-help','#wallet-loaded','#try-example']:
    assert h.page.locator(s).evaluate('(e)=>e.scrollWidth<=e.clientWidth+2'),s
   h.page.get_by_role('button',name='Enlarge QR',exact=True).click();stable(h);layout(h)
   h.workspace('advanced');layout(h);h.workspace('session');layout(h);h.workspace('test');layout(h);close(h)
  test(f'Delivery enlarged text never clips wallet controls or helper at {w}px',big)
 def spacing():
  h=Harness(browser,width=320,height=1100);h.page.add_style_tag(content=TEXT_SPACE);layout(h)
  for s in ['#word-count-help','#try-example','#wallet-loaded']:assert h.page.locator(s).evaluate('(e)=>e.scrollWidth<=e.clientWidth+2'),s
  close(h)
 test('Delivery custom text spacing keeps helper and action names readable',spacing)
 def ack():
  h=Harness(browser,width=390,height=844);h.page.get_by_role('button',name='24 words',exact=True).click();stable(h);h.page.locator('#wallet-loaded').click();stable(h)
  assert h.call('return a.acknowledged && a.step===2');p=pos(h,'#sign-title');assert 0<=p['y']<300,p
  assert h.page.locator('#sign-title').evaluate('(e)=>e===document.activeElement');assert h.call('return a.sessionSummary.checked')==0
  h.page.screenshot(path=str(SHOTS/'delivery-confirm-390.png'));close(h)
 test('Delivery primary confirmation reveals transaction review after long mobile wallet',ack)
 def paused():
  h=Harness(browser,width=390,media=True);h.config();h.page.locator('.stepper>button').nth(2).click();stable(h)
  assert h.page.locator('.intake').is_visible();assert not h.page.locator('#scan-section').is_visible();assert camera_count(h)==0
  assert h.page.locator('#verify-title').inner_text()=='Import the signed response.';close(h)
 test('Delivery Results exposes import controls but no camera starts automatically',paused)
 def live():
  h=Harness(browser,width=390,media=True);h.config();h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="scanning"');assert camera_count(h)==1
  before=h.call('return JSON.stringify(a.scan)');h.page.locator('.stepper>button').nth(2).click();stable(h)
  assert h.call('return a.scan.active && a.scan.phase==="scanning"');assert camera_count(h)==1
  assert h.page.evaluate('testStreams[0].getTracks()[0].readyState')=='live';h.call('a.stopScan()');close(h)
 test('Delivery clicking active Results preserves the same synthetic camera stream',live)
 def leave():
  h=Harness(browser,width=390,media=True);h.config();h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="scanning"')
  h.page.locator('.stepper>button').nth(1).click();stable(h);assert h.page.evaluate('testStreams[0].getTracks()[0].readyState')=='ended'
  h.page.locator('.stepper>button').nth(2).click();stable(h);assert camera_count(h)==1 and not h.call('return a.scan.active');assert h.page.locator('.intake').is_visible();close(h)
 test('Delivery leaving capture stops tracks and returning never reacquires automatically',leave)
 def incomplete():
  h=Harness(browser,width=390);h.config();h.accept('not-a-signed-response');r=h.call('return a.report()');before=state(h)
  h.call('a.pasteOpen=true');h.page.locator('.stepper>button').nth(0).click();stable(h);h.page.locator('.stepper>button').nth(2).click();stable(h)
  assert h.page.locator('.intake').is_visible();assert h.page.locator('.result').is_visible();assert h.call('return a.report()')==r;assert state(h)==before;assert h.call('return a.pasteOpen');close(h)
 test('Delivery reentry shows incomplete finding and intact editable intake together',incomplete)
 def halted():
  h=planned(browser,width=390);h.page.locator('#wallet-loaded').click();h.accept('bad response');r=h.call('return a.exportSessionReport()')
  h.page.locator('.stepper>button').nth(0).click();stable(h);h.page.locator('.stepper>button').nth(2).click();stable(h)
  assert h.call('return a.guidedStatus.phase')=='halted';assert h.page.locator('.intake').is_visible()
  assert h.page.locator('.intake fieldset').evaluate('(e)=>e.disabled && e.matches(":disabled")');assert h.page.locator('.intake button').first.is_disabled();assert h.page.locator('.guided-stop-reason').is_visible();assert h.call('return a.exportSessionReport()')==r;close(h)
 test('Delivery guided halt is not erased or unlocked by reopening Results',halted)
 def complete():
  h=Harness(browser,width=390);d=h.config();h.accept(d['tx']);before=state(h);e=h.call('return a.exportEvidence()')
  for idx in [0,1,2]:h.page.locator('.stepper>button').nth(idx).click();stable(h)
  assert not h.page.locator('.intake').is_visible();assert h.page.locator('.result').is_visible();assert h.call('return a.exportEvidence()')==e;assert state(h)==before
  with h.page.expect_download() as event:h.page.get_by_role('button',name='Save result',exact=True).click()
  assert json.loads(Path(event.value.path()).read_text())==e;close(h)
 test('Delivery completed result remains immutable read-only and exports exact evidence',complete)
 def review():
  h=Harness(browser,width=390);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());assert h.call('return a.resultDisplayState')=='review';before=state(h)
  h.page.locator('.stepper>button').nth(0).click();stable(h);h.page.locator('.stepper>button').nth(2).click();stable(h)
  assert h.page.locator('.file-review-action').is_visible();assert 'File changes need review' in h.page.locator('.result-message').inner_text();assert state(h)==before
  assert not h.page.locator('.intake').is_visible();h.page.screenshot(path=str(SHOTS/'delivery-review-390.png'),full_page=True);close(h)
 test('Delivery unexpected metadata stays prominent through all step navigation',review)
 def example():
  h=Harness(browser,width=390);before=state(h);h.page.get_by_role('button',name='Dark Skippy example',exact=True).first.click();stable(h)
  assert h.page.locator('#attack-example').evaluate('(e)=>e.open');assert 'Signatures differ' in h.page.locator('.demo-result').inner_text()
  assert h.call('return a.demonstration.analysis.evidence.signaturesVerified')==2;assert state(h)==before
  h.page.keyboard.press('Escape');stable(h);assert state(h)==before;assert h.call('return a.sessionSummary.checked')==0;close(h)
 test('Delivery renamed demo opens and verifies in one click without overwriting a wallet',example)
 def stale():
  h=Harness(browser,width=390);h.config();h.call('a.goToStep(1);a.goToStep(3);a.goToStep(2)');stable(h)
  assert h.call('return a.step')==2;assert h.page.locator('#sign-title').evaluate('(e)=>e===document.activeElement');close(h)
 test('Delivery rapid step changes focus only the final visible view',stale)
 def invalid():
  h=Harness(browser,width=390);h.call("a.invalidate();a.seed={value:'invalid wallet',error:null};a.recompute()");stable(h)
  h.page.locator('#wallet-loaded').click();stable(h);assert not h.call('return a.acknowledged');assert h.call('return a.step')==1
  assert not h.page.locator('#seed-qr-display').is_visible();assert h.page.locator('#wallet-fingerprint-value').inner_text()=='Unavailable';close(h)
 test('Delivery unavailable wallet cannot be acknowledged from the visible primary button',invalid)
 def help():
  h=Harness(browser,width=390);h.config();h.workspace('session');before=state(h);h.page.get_by_role('link',name='Help',exact=True).click();stable(h)
  assert h.page.locator('#help').is_visible();h.page.locator('.help-navigation a').click();stable(h)
  assert h.call('return a.workspaceView')=='session';assert state(h)==before;close(h)
 test('Delivery global Help retains the originating workspace and current test',help)
 def keyboard():
  h=Harness(browser,width=390);h.config();h.page.evaluate('window.scrollTo(0,0)');spy(h);h.page.keyboard.press('Tab')
  for idx in [2,0,1]:
   e=h.page.locator('.stepper>button').nth(idx);e.focus();h.page.keyboard.press('Enter');stable(h);assert h.call('return a.step')==idx+1;notscroll(h)
  close(h)
 test('Delivery keyboard step activation reaches correct view without forced scroll',keyboard)
 def scans():
  h=Harness(browser,width=390,media=True);h.config();h.page.locator('.stepper>button').nth(2).click();stable(h)
  h.page.locator('.intake').get_by_role('button',name='Scan signed QR',exact=True).click();h.page.wait_for_function('('+APP+').scan.phase==="scanning"');stable(h)
  assert camera_count(h)==1;assert h.page.locator('#scan-section').is_visible();p=pos(h,'#scan-section');assert p['y']>=-2 and p['bottom']<=h.page.viewport_size['height'],p
  h.call('a.stopScan()');close(h)
 test('Delivery explicit Scan action still reveals capture and requests one stream',scans)
 browser.close()
r={'suite':'Delivery navigation and wording browser acceptance','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results}
OUT.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
