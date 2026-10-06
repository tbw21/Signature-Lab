#!/usr/bin/env python3
"""Exact-candidate combined-card geometry/state/keyboard checks; synthetic, not hardware."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())

def core(h):return h.call('return JSON.stringify([a.seed,a.walletSession,a.walletFingerprint,a.stateSignature,a.psbtBase64,a.signingPolicy,a.variants,a.preparedRevision,a.sessionHistory,a.guidedStatus,a.completedAt,a.acknowledged,a.scan.phase])')
def rect(h,s):
 h.page.locator(s).wait_for(state="visible")
 return h.page.locator(s).evaluate('(e)=>{let r=e.getBoundingClientRect();return {x:r.x,y:r.y,right:r.right,bottom:r.bottom,width:r.width,height:r.height}}')
def geometry(h):
 card=rect(h,'#wallet-load-card');qr=rect(h,'#seed-qr-display');words=rect(h,'.seed-grid')
 assert card['y']>=qr['bottom']+10,(card,qr) # P03: shared QR rail, no full-width footer
 assert abs(card['x']-qr['x'])<1,(card,qr)
 assert abs(card['right']-qr['right'])<1,(card,qr)
 for selector in ['.wallet-fingerprint','#wallet-compare-hint','.seed-qr-actions>button','#wallet-loaded']:
  e=h.page.locator(selector)
  if not e.is_visible():continue
  b=rect(h,selector);assert b['x']>=card['x'] and b['right']<=card['right'],(selector,b,card)
  assert b['y']>=card['y'] and b['bottom']<=card['bottom'],(selector,b,card)
  if e.evaluate('(e)=>e.tagName')=='BUTTON':assert b['height']>=44,(selector,b)
 b1=rect(h,'.seed-qr-actions>button')
 if h.page.locator('#wallet-loaded').is_visible():
  b2=rect(h,'#wallet-loaded');assert b1['right']<=b2['x']-5 or b1['bottom']<=b2['y']-5,(b1,b2)
 assert h.page.locator('#wallet-fingerprint-value').count()==1
 assert h.page.locator('[x-ref="seedQrCanvas"]').count()==1
 assert h.page.locator('.wallet-confirmation .wallet-fingerprint').evaluate('(e)=>getComputedStyle(e).borderTopWidth')=='0px'
 layout(h)

def pixels(h):return h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(c)=>c.toDataURL()')
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 environment={'browser':browser.version,'origin':'offline exact candidate setContent','physicalSigner':False,'realOpticalScan':False,'scope':'combined card and nearby controls'}
 for width in [320,360,390,438,768,1024,1440]:
  def card(w=width):
   h=Harness(browser,width=w,height=1000);geometry(h)
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'card-wallet-{w}.png'),full_page=True)
   close(h)
  test(f'Wallet card groups fingerprint, reminder and two usable actions at {width}px',card)
 for width in [320,390,768,1440]:
  for words in [12,24]:
   def preserve(w=width,n=words):
    h=Harness(browser,width=w,height=1050)
    if n==24:h.page.get_by_role('button',name='24 words',exact=True).click()
    h.page.wait_for_function('('+APP+').seedQrVisible && !!('+APP+').walletFingerprint')
    before=core(h);image=pixels(h);decoded=read_qr(Image.open(io.BytesIO(base64.b64decode(image.split(',')[1]))))[0].data
    assert len(decoded)==n*4
    geometry(h)
    h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(60);geometry(h)
    assert core(h)==before;assert image==pixels(h)
    if w==1440 and n==12:h.page.screenshot(path=str(SHOTS/'card-enlarged-1440.png'),full_page=True)
    h.page.get_by_role('button',name='Reduce QR',exact=True).click();h.page.wait_for_timeout(50)
    assert core(h)==before;assert image==pixels(h);geometry(h);close(h)
   test(f'Wallet card {words} words QR pixels and state preserved through enlargement at {width}px',preserve)
 for width in [320,390,768,1440]:
  def enlarged(w=width):
   h=Harness(browser,width=w,height=1000);h.page.get_by_role('button',name='24 words',exact=True).click();h.page.wait_for_timeout(80);h.page.evaluate(ENLARGE)
   for exp in [False,True]:h.call('a.seedQrExpanded=arg',exp);h.page.wait_for_timeout(40);geometry(h)
   for view in ['advanced','session','test']:h.workspace(view);layout(h)
   close(h)
  test(f'Wallet card and related workspaces reflow with 24 words and doubled text at {width}px',enlarged)
 def spacing():
  h=Harness(browser,width=320);h.page.add_style_tag(content=TEXT_SPACE);geometry(h)
  h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(50);geometry(h);close(h)
 test('Wallet card accepts increased word, letter and line spacing without clipping',spacing)
 def keyboard():
  h=Harness(browser,width=390);before=core(h);b=h.page.get_by_role('button',name='Enlarge QR',exact=True);b.focus()
  assert b.evaluate('(e)=>getComputedStyle(e).outlineStyle')!='none'
  h.page.keyboard.press('Enter');h.page.wait_for_timeout(40);assert core(h)==before
  h.page.keyboard.press('Space');h.page.wait_for_timeout(40);assert core(h)==before
  h.page.keyboard.press('Tab');assert h.page.locator('#wallet-loaded').evaluate('(e)=>e===document.activeElement')
  h.page.keyboard.press('Enter');assert h.call('return a.step')==2;assert h.call('return a.acknowledged')
  assert h.call('return a.sessionSummary.checked')==0;close(h)
 test('Wallet card keyboard order enlarges separately before explicit wallet acknowledgement',keyboard)
 def unavailable():
  h=Harness(browser,width=390);h.call("a.invalidate();a.seed={value:'invalid seed fixture',error:'fixture'};a.recompute()")
  assert h.page.locator('#wallet-fingerprint-value').inner_text()=='Unavailable';assert not h.page.locator('#seed-qr-display').is_visible()
  assert h.call('return a.sessionSummary.checked')==0;layout(h);close(h)
 test('Wallet card invalid seed never displays the previous fingerprint or QR',unavailable)
 def completed():
  h=Harness(browser,width=390);h.config();h.accept(h.call('return a.variants[0].txHex'));before=core(h)
  h.call('a.goToStep(1)');h.page.wait_for_timeout(50)
  assert not h.page.locator('#wallet-loaded').is_visible();assert h.page.locator('#wallet-fingerprint-value').is_visible()
  h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(40);geometry(h);assert core(h)==before;close(h)
 test('Wallet card completed test stays read-only without duplicate acknowledgement',completed)
 def highcontrast():
  h=Harness(browser,width=390);h.page.emulate_media(forced_colors='active',reduced_motion='reduce');geometry(h)
  h.page.locator('.seed-qr-actions>button').focus();assert h.page.locator('.seed-qr-actions>button').evaluate('(e)=>getComputedStyle(e).outlineStyle')!='none';close(h)
 test('Wallet card forced colors and reduced motion keep controls and focus visible',highcontrast)
 def layers():
  h=Harness(browser,width=390);before=core(h)
  for view in ['advanced','session','test']:
   h.workspace(view);assert core(h)==before;layout(h)
  h.page.locator('#try-example').click();h.page.wait_for_timeout(60)
  assert h.page.locator('#attack-example').evaluate('(e)=>e.open');assert not h.page.locator('#wallet-loaded').evaluate('(e)=>e===document.activeElement')
  h.page.keyboard.press('Escape');h.page.wait_for_timeout(40);assert core(h)==before;geometry(h);close(h)
 test('Wallet card survives all workspaces and optional example without modifying the test',layers)
 def balanced_actions():
  for w in [438,500]:
   h=Harness(browser,width=w,height=1000)
   a=rect(h,'.seed-qr-actions>button');b=rect(h,'#wallet-loaded')
   assert a['height']>=44 and b['height']>=44
   # Larger approved type may stack whole actions; preserve equal edges/heights without shrinking.
   if abs(a['y']-b['y'])<1:assert abs(a['height']-b['height'])<1,(w,a,b)
   else:assert a['bottom']<=b['y'] and abs(a['x']-b['x'])<1 and abs(a['width']-b['width'])<1,(w,a,b)
   for selector in ['.seed-qr-actions>button','#wallet-loaded']:
    assert h.page.locator(selector).evaluate('(e)=>parseFloat(getComputedStyle(e).fontSize)>=16 && e.scrollWidth<=e.clientWidth+1')
   geometry(h);close(h)
 test('Wallet card intermediate-width action row has level buttons without unnecessary label wrapping',balanced_actions)
 browser.close()
r={'suite':'Wallet confirmation browser checks','complete':True,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results};OUT.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'passed':r['passed'],'failed':r['failed']}));sys.exit(bool(r['failed']))
