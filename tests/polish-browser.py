#!/usr/bin/env python3
"""Exact-candidate header/QR geometry and preserved security-state simulations."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())

def box(h,s):
 h.page.locator(s).wait_for(state="visible")
 return h.page.locator(s).evaluate('(e)=>{let r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}}')
def same_edges(a,b):assert abs(a['x']-b['x'])<1 and abs(a['right']-b['right'])<1,(a,b)
def state(h):return h.call('return JSON.stringify([a.seed,a.walletSession,a.walletFingerprint,a.stateSignature,a.psbtBase64,a.signingPolicy,a.variants,a.preparedRevision,a.sessionHistory,a.guidedStatus,a.completedAt,a.acknowledged,a.scan.phase])')
def geometry(h):
 qr=box(h,'#seed-qr-display');card=box(h,'#wallet-load-card');rail=box(h,'.seed-scan');same_edges(qr,card)
 assert qr['width']>=200,(qr,rail)
 assert card['y']>=qr['bottom']+10 and card['bottom']<=rail['bottom']-12,(card,qr,rail)
 for s in ['.wallet-fingerprint','#wallet-compare-hint','.wallet-confirmation-actions']:
  if h.page.locator(s).is_visible():same_edges(box(h,s),qr)
 a=box(h,'.seed-qr-actions>button');assert a['height']>=44
 if h.page.locator('#wallet-loaded').is_visible():
  b=box(h,'#wallet-loaded');assert b['height']>=44
  assert abs(a['x']-qr['x'])<1 and abs(b['right']-qr['right'])<1,(a,b,qr)
  if abs(a['y']-b['y'])<1:
   assert a['right']<=b['x']-7 and abs(a['height']-b['height'])<1,(a,b)
  else:
   assert a['bottom']<=b['y']-7,(a,b)
   same_edges(a,qr);same_edges(b,qr)
 for s in ['.seed-qr-actions>button','#wallet-loaded','#wallet-fingerprint-value']:
  e=h.page.locator(s)
  if e.is_visible():assert e.evaluate('(e)=>e.scrollWidth<=e.clientWidth+2'),s
 layout(h)
def header(h):
 e=h.page.get_by_role('link',name='Help',exact=True);assert e.is_visible();assert e.get_attribute('title')=='Help'
 r=box(h,'.help-control');assert r['width']>=44 and r['height']>=44
 assert h.page.locator('.workspace-nav .help-control').count()==0
 b=box(h,'.brand');a=box(h,'.header-actions')
 assert a['x']>=b['right']-1 or a['y']>=b['bottom']+6,(a,b)
 inner=h.page.locator('.header-inner').evaluate('(e)=>{let r=e.getBoundingClientRect(),c=getComputedStyle(e);return {right:r.right-parseFloat(c.paddingRight)}}')
 assert abs(r['right']-inner['right'])<1,(r,inner)
 assert h.page.locator('.release-status a').is_visible()
 for selector in ['.release-status a','.release-version','.brand-name']:
  assert h.page.locator(selector).evaluate('(e)=>e.clientWidth===0 || e.scrollWidth<=e.clientWidth+1'),selector
 assert 'hardware acceptance pending' in h.page.locator('.release-status a').get_attribute('aria-label')
 layout(h)
def image(h):return h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(e)=>e.toDataURL()')

with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 environment={'browser':browser.version,'origin':'offline exact HTML via setContent','physicalSigner':False,'realOpticalScan':False,'nativeWindowsMac':False}
 for w in [320,360,390,438,768,1024,1440]:
  def ordinary(w=w):
   h=Harness(browser,width=w,height=1100);geometry(h);header(h)
   assert box(h,'.header-inner')['height']<=150, 'Readable header may wrap without shrinking targets'
   base_mark=27 if w<=760 else 34;base_text=19 if w<=350 else 20 if w<=760 else 23
   mark=box(h,'.brand-mark')['width'];text=h.page.locator('.brand-name').evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)')
   assert 1.10<=mark/base_mark<=1.15 and text>=22,(w,mark,text)  # Superseded undersized wordmark; keep enlarged wheel and readable text.
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'polish-wallet-{w}.png'),full_page=True)
   close(h)
  test(f'Polish header scale global Help and exact QR/action edges at {w}px',ordinary)
 for w in [320,390,768,1440]:
  for n in [12,24]:
   def enlarge(w=w,n=n):
    h=Harness(browser,width=w,height=1100)
    if n==24:h.page.get_by_role('button',name='24 words',exact=True).click()
    h.page.wait_for_function('('+APP+').seedQrVisible && !!('+APP+').walletFingerprint')
    before=state(h);pixels=image(h);assert len(read_qr(Image.open(io.BytesIO(base64.b64decode(pixels.split(',')[1]))))[0].data)==4*n
    old=box(h,'#seed-qr-display')['width'];geometry(h)
    h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(50)
    geometry(h);assert image(h)==pixels and state(h)==before;assert box(h,'#seed-qr-display')['width']>=old
    if w==1440 and n==12:h.page.screenshot(path=str(SHOTS/'polish-enlarged-1440.png'),full_page=True)
    h.page.get_by_role('button',name='Reduce QR',exact=True).click();h.page.wait_for_timeout(50);geometry(h)
    assert state(h)==before and image(h)==pixels;close(h)
   test(f'Polish {n} words QR pixels geometry and authoritative state preserved on enlarge at {w}px',enlarge)
 for w in [320,390,768,1440]:
  def enlarged_text(w=w):
   h=Harness(browser,width=w,height=1100);h.page.get_by_role('button',name='24 words',exact=True).click();h.page.wait_for_timeout(60);h.page.evaluate(ENLARGE)
   for enlarged in [False,True]:h.call('a.seedQrExpanded=arg',enlarged);h.page.wait_for_timeout(50);geometry(h);header(h)
   for view in ['advanced','session','test']:h.workspace(view);header(h);layout(h)
   close(h)
  test(f'Polish header and all workspaces reflow with doubled text and 24 words at {w}px',enlarged_text)
 def spacing():
  h=Harness(browser,width=320);h.page.add_style_tag(content=TEXT_SPACE);header(h);geometry(h)
  h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(50);geometry(h);close(h)
 test('Polish increased text spacing keeps fingerprint and all action labels unclipped',spacing)
 for view in ['test','advanced','session']:
  def help_return(view=view):
   h=Harness(browser,width=390);h.workspace(view);before=state(h)
   help=h.page.get_by_role('link',name='Help',exact=True);h.page.keyboard.press('Tab');help.focus();assert help.evaluate('(e)=>getComputedStyle(e).outlineStyle')!='none'
   h.page.keyboard.press('Enter');h.page.wait_for_timeout(50)
   assert h.page.locator('#help').is_visible();assert help.get_attribute('aria-current')=='page';assert state(h)==before
   h.page.locator('.help-navigation a').click();h.page.wait_for_timeout(60)
   assert h.call('return a.workspaceView')==view and state(h)==before
   assert help.get_attribute('aria-current') is None;header(h);close(h)
  test(f'Polish accessible question-mark Help roundtrip preserves {view} workspace and test',help_return)
 def status_link():
  h=Harness(browser,width=390);before=state(h);h.page.locator('.release-status a').click();h.page.wait_for_timeout(50)
  assert h.page.locator('#release-status-help').evaluate('(e)=>e.open');assert state(h)==before
  assert h.page.locator('#release-status-help summary').evaluate('(e)=>e===document.activeElement');layout(h);close(h)
 test('Polish quieter version still opens the complete release-status limitations',status_link)
 def keyboard():
  h=Harness(browser,width=390);before=state(h);h.page.get_by_role('button',name='Enlarge QR',exact=True).focus()
  h.page.keyboard.press('Enter');h.page.wait_for_timeout(40);assert state(h)==before
  h.page.keyboard.press('Tab');assert h.page.locator('#wallet-loaded').evaluate('(e)=>e===document.activeElement')
  h.page.keyboard.press('Enter');assert h.call('return a.acknowledged && a.step===2');assert h.call('return a.sessionSummary.checked')==0;close(h)
 test('Polish enlargement and acknowledgement remain separate keyboard operations',keyboard)
 def accessibility_modes():
  h=Harness(browser,width=390);h.page.emulate_media(forced_colors='active',reduced_motion='reduce');geometry(h);header(h)
  h.page.locator('.help-control').focus();assert h.page.locator('.help-control').evaluate('(e)=>getComputedStyle(e).outlineStyle')!='none';close(h)
 test('Polish high-contrast and reduced-motion modes retain visible Help focus and controls',accessibility_modes)
 def unavailable():
  h=Harness(browser,width=390);h.call("a.invalidate();a.seed={value:'invalid test words',error:'fixture'};a.recompute()")
  assert not h.page.locator('#seed-qr-display').is_visible();assert h.page.locator('#wallet-fingerprint-value').inner_text()=='Unavailable'
  assert h.call('return a.sessionSummary.checked')==0;layout(h);close(h)
 test('Polish unavailable wallet has no stale QR or fingerprint in the shared rail',unavailable)
 def completed():
  h=Harness(browser,width=390);h.config();h.accept(h.call('return a.variants[0].txHex'));before=state(h)
  h.call('a.goToStep(1)');h.page.wait_for_timeout(60);assert not h.page.locator('#wallet-loaded').is_visible();geometry(h)
  h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(50);geometry(h);assert state(h)==before;close(h)
 test('Polish completed wallet remains read only and enlargement cannot change the result',completed)
 for w in [390,1440]:
  def qr_actions(w=w):
   h=Harness(browser,width=w);h.page.locator('#wallet-loaded').click()
   for mode in ['ur','bbqr']:
    h.call('a.setPsbtQrMode(arg)',mode);h.page.wait_for_function('('+APP+').psbtQrAvailable')
    q=box(h,'.sign-layout>.qr-column .qr-frame');a=box(h,'.psbt-actions');same_edges(q,a)
    same_edges(q,box(h,'.sign-layout>.qr-column .qr-format-control'))
    b1=box(h,'.psbt-actions>.button:first-child');b2=box(h,'.psbt-actions>.button:last-child')
    assert abs(b1['x']-q['x'])<1 and abs(b2['right']-q['right'])<1
    assert abs(b1['y']-b2['y'])<1 and b1['height']>=44 and b2['height']==44;layout(h)
   if w==1440:h.page.screenshot(path=str(SHOTS/'polish-transaction-1440.png'),full_page=True)
   close(h)
  test(f'Polish BC-UR and BBQr save/copy controls align to the transaction QR at {w}px',qr_actions)
 def example():
  h=Harness(browser,width=390);before=state(h);h.page.locator('#try-example').click();h.page.wait_for_timeout(50)
  assert h.page.locator('#attack-example').evaluate('(e)=>e.open && e.matches(":modal")');assert state(h)==before
  assert h.call('return a.demonstration.analysis.ok && !a.demonstration.analysis.matched')
  h.page.keyboard.press('Escape');assert state(h)==before;header(h);geometry(h);close(h)
 test('Polish existing one-click Dark Skippy demo cannot replace wallet or inflate test counts',example)
 def metadata_review():
  h=Harness(browser,width=390);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex())
  assert h.call('return a.resultDisplayState')=='review';assert h.page.locator('.file-review-action').is_visible()
  assert not h.page.locator('#result-tools').evaluate('(e)=>e.open');layout(h);header(h);close(h)
 test('Polish unrelated returned-file review finding remains visible and amber',metadata_review)
 def stable_views():
  h=Harness(browser,width=390,height=1100);h.page.evaluate('scrollTo(0,30)');before=state(h);r=box(h,'.workspace-heading');y=h.page.evaluate('scrollY')
  for v in ['advanced','session','test']:
   h.workspace(v);same_edges(r,box(h,'.workspace-heading'));assert abs(box(h,'.workspace-heading')['y']-r['y'])<1
   assert abs(h.page.evaluate('scrollY')-y)<1;assert state(h)==before
  close(h)
 test('Polish workspace strip remains stationary during scrolled navigation',stable_views)
 browser.close()
r={'suite':'Header and QR polish browser checks','complete':True,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results}
OUT.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':r['passed'],'failed':r['failed']}));sys.exit(bool(r['failed']))
