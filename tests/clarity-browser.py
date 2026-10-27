#!/usr/bin/env python3
"""Clarity real-DOM geometry, font, dialog and immutable-state simulations; not physical OS/hardware."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())
def stable_state(h):return h.call('return JSON.stringify([a.stateSignature,a.walletSession,a.psbtBase64,a.variants,a.preparedRevision,a.sessionHistory,a.guidedStatus,a.resultState,a.completedAt,a.signingPolicy])')
def geom(h):
 # Header and main workspace have stable origins across views; the stepper is
 # intentionally visible only inside Test and must not be used as global nav.
 return h.page.evaluate('''()=>{const rect=e=>{const r=e.getBoundingClientRect();return [r.left,r.top,r.width,r.height]};return {nav:rect(document.querySelector('.header-inner')),panel:rect(document.querySelector('main.page-container')),scroll:scrollY,width:document.documentElement.clientWidth};}''')
def fonts(h):
 # Current approved design uses a system-ui reading face and a deliberately
 # contrasting serif wordmark; reject illegible or unexpected font fallbacks.
 result=h.page.evaluate("""()=>{const css=e=>getComputedStyle(document.querySelector(e));return {body:css('body').fontFamily,brand:css('.brand-name').fontFamily,brandSize:parseFloat(css('.brand-name').fontSize),textSize:parseFloat(css('body').fontSize)}}""")
 assert result['body'] and result['textSize']>=14,result
 assert ('Georgia' in result['brand'] or 'Times' in result['brand']) and result['brandSize']>=16,result


def dialog(h):
 h.page.get_by_role('link',name='Help',exact=True).click();h.page.locator('#try-example').click();h.page.wait_for_timeout(50)
 assert h.page.locator('#attack-example').evaluate('(e)=>e.open && e.matches(":modal")')
 assert h.call('return !!a.demonstration.analysis?.ok && !a.demonstration.analysis?.matched')
 assert 'does not run malicious firmware' in h.page.locator('#attack-example').inner_text().lower()

with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 environment={'browser':browser.version,'mode':'exact HTML setContent, native Linux system font','physicalSigner':False,'realCamera':False,'nativeMacWindows':False}
 for width in [320,360,390,438,768,1024,1440]:
  def geometry(w=width):
   h=Harness(browser,width=w,height=950);h.workspace('test');before=stable_state(h)
   for acknowledged in [False,True]:
    if acknowledged:h.call('a.acknowledged=true');h.page.wait_for_timeout(40)
    h.page.evaluate('window.scrollTo(0,0)');initial=geom(h)
    for view in ['advanced','session','test','session','advanced','test']:
     h.workspace(view);h.page.wait_for_timeout(60);now=geom(h);assert h.call('return a.workspaceView')==view
     # Progress steps intentionally disappear outside Test. Preserve the left edge,
     # viewport fit, and semantic state, not obsolete fixed vertical coordinates.
     for key in ['nav','panel']:
      assert abs(now[key][0]-initial[key][0])<1,(w,key,initial,now)
      assert now[key][2]>0 and now[key][2]<=w+1,(w,key,now)
     assert now['panel'][1]>=now['nav'][1]+now['nav'][3]-1,(w,now)
     assert abs(now['scroll']-initial['scroll'])<1,(w,initial,now)
     assert now['width']==initial['width'];assert stable_state(h)==before;layout(h);fonts(h)
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'clarity-wallet-{w}.png'),full_page=True)
   close(h)
  test(f'Clarity stable navigation/panel origin and one native family across views at {width}px',geometry)
 for width in [320,390,1440]:
  def scroll(w=width):
   h=Harness(browser,width=w,height=900);h.workspace('test');h.page.evaluate('scrollTo(0,60)');start=geom(h);before=stable_state(h)
   h.page.evaluate("""()=>{window.unrequestedScrolls=[];const into=Element.prototype.scrollIntoView,to=window.scrollTo;
    Element.prototype.scrollIntoView=function(...x){unrequestedScrolls.push('into');return into.apply(this,x)};
    window.scrollTo=function(...x){unrequestedScrolls.push('to');return to.apply(this,x)};}""")
   for v in ['advanced','session','test']:
    previous=geom(h);h.workspace(v);h.page.wait_for_timeout(50);g=geom(h);assert h.call('return a.workspaceView')==v
    maximum=h.page.evaluate('Math.max(0,document.documentElement.scrollHeight-innerHeight)')
    # A content-following footer may make a short view unscrollable. Preserve every
    # still-representable offset; accept only the browser's mandatory height clamp.
    assert abs(g['scroll']-min(previous['scroll'],maximum))<1,(w,previous,g,maximum)
    # View-specific stepper height changes the nav's document offset by design;
    # no programmatic scroll-to-top is allowed, and actual scroll remains bounded.
    assert g['nav'][1]+g['scroll']>=0 and g['nav'][1]+g['scroll']<=g['panel'][1]+g['scroll'],(w,start,g)
    assert not h.page.evaluate('unrequestedScrolls'),h.page.evaluate('unrequestedScrolls')
    assert stable_state(h)==before
   close(h)
  test(f'Clarity visible navigation preserves possible scroll and document alignment at {width}px',scroll)
 for width in [320,390,768,1440]:
  for words in [12,24]:
   def sizes(w=width,n=words):
    h=Harness(browser,width=w,height=1000);h.workspace('test')
    if n==24:h.page.get_by_role('button',name='24 words',exact=True).click()
    h.page.wait_for_function('('+APP+').seedQrVisible && !!('+APP+').walletFingerprint')
    s=stable_state(h);im=h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(c)=>c.toDataURL()')
    raw=read_qr(Image.open(io.BytesIO(base64.b64decode(im.split(',')[1]))))[0].data
    assert len(raw)==n*4;fonts(h);layout(h)
    assert h.page.locator('#wallet-safety').is_visible() and 'Never overwrite an existing wallet' in h.page.locator('#wallet-safety').inner_text()
    assert not h.page.locator('[onclick]').count()
    assert h.page.locator('#new-test-wallet').is_visible()
    h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(50)
    assert stable_state(h)==s;assert h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(c)=>c.toDataURL()')==im
    h.page.evaluate(ENLARGE);layout(h);fonts(h)
    close(h)
   test(f'Clarity {words} words retain QR pixels and readable enlarged native text at {width}px',sizes)
 for width in [320,390,1440]:
  def example(w=width):
   h=Harness(browser,width=w,height=1000);h.workspace('test');before=stable_state(h);dialog(h);y=h.page.evaluate('scrollY');layout(h);fonts(h)
   assert stable_state(h)==before;assert h.call('return a.sessionSummary.checked')==0
   for _ in range(8):
    h.page.keyboard.press('Tab');assert h.page.evaluate('document.activeElement===document.body || !!document.activeElement.closest("#attack-example")')
   h.page.evaluate('document.getElementById("wallet-loaded").focus()')
   assert h.page.evaluate('document.activeElement.id!=="wallet-loaded"')
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'clarity-example-{w}.png'),full_page=False)
   h.page.keyboard.press('Escape');h.page.wait_for_timeout(30);assert not h.page.locator('#attack-example').is_visible()
   assert h.page.evaluate('document.activeElement.id')=='try-example';assert stable_state(h)==before;assert h.page.evaluate('scrollY')==y
   h.page.locator('.help-navigation a').click();h.page.locator('#wallet-loaded').click();h.page.wait_for_timeout(60)
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'clarity-transaction-{w}.png'),full_page=True)
   close(h)
  test(f'Clarity one-click example and native modal background isolation/Escape preserve active test at {width}px',example)
 def example_large():
  h=Harness(browser,width=320,height=850);h.workspace('test');h.page.evaluate(ENLARGE);h.page.add_style_tag(content=TEXT_SPACE);dialog(h);layout(h);fonts(h)
  h.page.keyboard.press('Escape');assert not h.page.locator('#attack-example').is_visible();close(h)
 test('Clarity enlarged/spaced modal content stays reachable and escapable at 320px',example_large)
 def help_example():
  h=Harness(browser,width=390);h.workspace('test');h.page.get_by_role('link',name='Help',exact=True).click();link=h.page.locator('.help-contents a[href="#known-example"]');assert link.count()==1;link.locator('xpath=ancestor::details[1]').locator('summary').click();link.click()
  before=stable_state(h);h.page.get_by_role('link',name='Help',exact=True).click();h.page.locator('#try-example').click();assert h.page.locator('#attack-example').is_visible();assert stable_state(h)==before
  h.page.get_by_role('button',name='Close Dark Skippy example').click();assert h.page.locator('#known-example').is_visible();close(h)
 test('Clarity Help and Step1 use the same one-click dialog and verifier',help_example)
 def completed():
  h=Harness(browser,width=390);h.workspace('test');d=h.config();h.accept(d['tx']);before=stable_state(h);report=h.call('return a.report()');h.call('a.openExample()');assert h.page.locator('#attack-example').is_visible();h.page.keyboard.press('Escape');assert stable_state(h)==before;assert h.call('return a.report()')==report;close(h)
 test('Clarity opening optional demo cannot replace a completed immutable result',completed)
 def failure():
  h=Harness(browser,width=390);h.workspace('test');h.call("a.runDemonstration=()=>{a.demonstration.error='Injected example failure';a.demonstration.analysis=null}")
  before=stable_state(h);h.page.get_by_role('link',name='Help',exact=True).click();h.page.locator('#try-example').click();h.page.wait_for_function('document.getElementById("attack-example").innerText.includes("Injected example failure")');assert 'Injected example failure' in h.page.locator('#attack-example').inner_text();assert not h.page.locator('.example-checks').count();assert stable_state(h)==before;h.page.keyboard.press('Escape');close(h)
 test('Clarity example failure has no green result and leaves the device test intact',failure)
 def no_dialog():
  h=Harness(browser);h.workspace('test');h.page.evaluate('document.getElementById("attack-example").remove()');h.call('delete a.$refs.exampleDialog');before=stable_state(h);h.page.get_by_role('link',name='Help',exact=True).click();h.page.locator('#try-example').click();assert 'unavailable' in h.call('return a.notice');assert stable_state(h)==before;d=h.config();h.accept(d['tx']);assert h.call('return a.resultState')=='match';close(h)
 test('Clarity absent optional dialog does not block ordinary verification',no_dialog)
 def camera():
  h=Harness(browser,media=True);h.config();h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="scanning"');count=h.page.evaluate('mediaCalls');assert h.call('return a.openExample()')==False;assert h.call('return a.scan.active');assert h.page.evaluate('mediaCalls')==count;h.call('a.stopScan()');close(h)
 test('Clarity example cannot hide live camera capture or trigger another permission request',camera)
 def reset():
  h=Harness(browser,width=390);h.workspace('test');before=h.call('return a.seed.value');h.page.locator('#new-test-wallet').click();h.page.wait_for_timeout(70);assert h.call('return a.seed.value')!=before;assert h.call('return a.wordCount')=='12';assert h.call('return a.workspaceView')=='test';assert not h.call('return a.acknowledged');close(h)
 test('Clarity visible wallet replacement retains same-length regeneration',reset)
 def outcomes():
  h=Harness(browser,width=390);h.workspace('test');d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());present_result(h);assert h.page.locator('.file-review-action').is_visible();before=stable_state(h)
  for v in ['advanced','session','test']:h.workspace(v);assert stable_state(h)==before;fonts(h)
  present_result(h)
  assert h.page.locator('.file-review-action').is_visible();close(h)
 test('Clarity simplification does not hide unexpected file findings or change their evidence',outcomes)
 def forced():
  h=Harness(browser,width=390);h.workspace('test');h.page.emulate_media(forced_colors='active',reduced_motion='reduce');dialog(h);layout(h);h.page.keyboard.press('Escape')
  for view in ['advanced','session','test']:h.workspace(view);layout(h)
  close(h)
 test('Clarity controls and demo remain accessible in forced colors and reduced motion',forced)
 browser.close()
r={'suite':'Clarity native-font/navigation/demo browser qualification','complete':True,'total_defined':test_index,'test_range':':'.join(TEST_RANGE),'environment':environment,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results};OUT.write_text(json.dumps(r,indent=2));print(json.dumps({k:r[k] for k in ['suite','total_defined','passed','failed']}));sys.exit(bool(r['failed']))
