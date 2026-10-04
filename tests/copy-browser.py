#!/usr/bin/env python3
"""Gold scope copy and removed wallet note in exact candidate DOM; no physical device claims."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())
INTRO='Compare test signatures with expected results to flag deviations such as the published Dark Skippy example; a match cannot rule out all attacks.'
def identity(h):return h.call('return JSON.stringify([a.stateSignature,a.psbtBase64,a.variants,a.walletSession,a.walletFingerprint,a.preparedRevision,a.sessionChecks,a.guidedStatus,a.resultState,a.completedAt,a.signingPolicy])')
def help_topic(h,id):
 h.page.get_by_role('link',name='Help',exact=True).click()
 link=h.page.locator('.help-contents a[href="#'+id+'"]');parent=link.locator('xpath=ancestor::details[1]')
 if not parent.evaluate('(e)=>e.open'):parent.locator(':scope > summary').click()
 link.click();h.page.wait_for_timeout(40)
def metrics(h):
 return h.page.locator('#test-purpose').evaluate('''e=>{const c=getComputedStyle(e),r=document.createRange();r.selectNodeContents(e);const ctx=document.createElement("canvas").getContext("2d");ctx.font=c.fontStyle+" "+c.fontWeight+" "+c.fontSize+" "+c.fontFamily;return {naturalWidth:ctx.measureText(e.textContent).width,text:e.textContent,font:parseFloat(c.fontSize),color:c.color,background:getComputedStyle(document.documentElement).backgroundColor,lines:new Set([...r.getClientRects()].map(r=>r.y)).size,width:e.clientWidth,scroll:e.scrollWidth,whiteSpace:c.whiteSpace,overflow:c.overflowX};}''')
def luminance(s):
 c=[int(n)/255 for n in re.findall(r'\d+',s)[:3]];c=[n/12.92 if n<=.04045 else ((n+.055)/1.055)**2.4 for n in c]
 return sum(a*b for a,b in zip(c,[.2126,.7152,.0722]))
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 environment={'browser':browser.version,'mode':'exact candidate HTML in offline Chromium harness','physical':False,'optical':False}
 for width in [320,360,390,438,768,1024,1440]:
  def responsive(w=width):
   h=Harness(browser,width=w,height=1050);m=metrics(h)
   assert m['text']==INTRO and m['color']=='rgb(229, 182, 125)';assert m['whiteSpace']=='normal'
   assert m['scroll']<=m['width']+1 and m['font']>=13
   contrast=(max(luminance(m['color']),luminance(m['background']))+.05)/(min(luminance(m['color']),luminance(m['background']))+.05)
   assert contrast>=4.5,contrast
   # Native system fonts differ in glyph widths. Preserve natural wrapping, not a fixed line count.
   if m['naturalWidth']<=m['width']:assert m['lines']==1,m
   else:assert m['lines']>1,m
   if w>=1024:assert m['font']==14,m
   if w<=438:assert m['lines']>1,m
   assert h.page.locator('.seed-scan .wallet-fingerprint-help').count()==0
   assert h.page.locator('#wallet-fingerprint-value').is_visible()
   assert not h.page.locator('#wallet-technical-note').is_visible()
   before=identity(h)
   for view in ['advanced','session','test']:
    h.workspace(view);assert metrics(h)['text']==INTRO;assert identity(h)==before;layout(h)
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'copy-wallet-{w}.png'),full_page=True)
   close(h)
  test(f'Copy layout: gold, readable contrast and natural reflow at {width}px',responsive)
 for width in [390,1440]:
  for words in [12,24]:
   def wallet(w=width,n=words):
    h=Harness(browser,width=w,height=1100);h.call('a.selectSeedLength(arg)',n)
    h.page.wait_for_function(f'document.querySelectorAll(".seed-grid li").length==={n}')
    h.page.wait_for_function('('+APP+').seedQrVisible && ('+APP+').walletFingerprint')
    before=identity(h);uri=h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(e)=>e.toDataURL()')
    fingerprint=h.page.locator('#wallet-fingerprint-value').inner_text();assert re.fullmatch('[0-9A-F]{8}',fingerprint)
    for action in ['Enlarge QR','Reduce QR']:
     h.page.get_by_role('button',name=action,exact=True).click();assert identity(h)==before
     assert h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(e)=>e.toDataURL()')==uri
     assert h.page.locator('#wallet-fingerprint-value').inner_text()==fingerprint;layout(h)
    assert h.page.locator('.seed-scan').inner_text().find('No passphrase')==-1
    close(h)
   test(f'Copy wallet note relocation preserves {words}-word QR and fingerprint at {width}px',wallet)
 for width in [320,1440]:
  def large(w=width):
   h=Harness(browser,width=w,height=1100);h.page.evaluate(ENLARGE);layout(h)
   assert metrics(h)['lines']>1
   help_topic(h,'technical-help');assert h.page.locator('#wallet-technical-note').is_visible();layout(h);close(h)
  test(f'Copy and relocated technical note reflow with doubled text at {width}px',large)
 def spacing():
  h=Harness(browser,width=390);h.page.add_style_tag(content=TEXT_SPACE);layout(h);m=metrics(h);assert m['scroll']<=m['width']+1;close(h)
 test('Copy and controls retain complete text with increased letter/word/line spacing',spacing)
 def details():
  h=Harness(browser,width=390);before=identity(h);help_topic(h,'technical-help')
  txt=h.page.locator('#wallet-technical-note').inner_text();assert 'BIP32 master-key fingerprint' in txt and 'uses no passphrase' in txt
  assert h.page.evaluate('document.activeElement.parentElement.id')=='technical-help'
  h.page.locator('#technical-help > .help-answer-nav a').click();h.page.locator('.help-contents a[href="#signature-check"]').locator('xpath=ancestor::details[1]').locator(':scope > summary').click()
  link=h.page.locator('.help-contents a[href="#signature-check"]');link.focus();h.page.keyboard.press('Enter')
  assert 'conditional Dark Skippy variant' in h.page.locator('#signature-scope-note').inner_text()
  h.page.get_by_role('link',name='Back to test',exact=True).click();assert identity(h)==before;close(h)
 test('Moved wallet details and attack scope are keyboard-reachable without changing the active test',details)
 def result():
  h=Harness(browser,width=390);d=h.config();h.accept(d['tx']);before=identity(h);report=h.call('return a.report()')
  limit=h.page.locator('.result-limit:visible');assert limit.count()==1
  assert 'this transaction only' in limit.inner_text() and 'does not rule out seed leakage' in limit.inner_text()
  h.page.screenshot(path=str(SHOTS/'copy-result-390.png'),full_page=True)
  help_topic(h,'signature-check');h.page.get_by_role('link',name='Back to test',exact=True).click()
  assert identity(h)==before and h.call('return a.report()')==report;close(h)
 test('Matching result keeps one precise scope limitation and unchanged immutable evidence',result)
 def example():
  h=Harness(browser);before=identity(h);h.page.locator('#try-example').click()
  assert h.page.locator('#attack-example').is_visible()
  assert h.call('return a.demonstration.analysis.evidence.signaturesVerified')==2
  assert not h.call('return !!a.demonstration.analysis.matched')
  assert identity(h)==before and h.call('return a.sessionSummary.checked')==0;close(h)
 test('Published Dark Skippy example still differs while the active hardware-test count stays unchanged',example)
 def forced():
  h=Harness(browser,width=390);h.page.emulate_media(forced_colors='active');assert metrics(h)['color']!='rgb(229, 182, 125)';layout(h);close(h)
 test('Scope introduction follows system high-contrast text color rather than forcing gold',forced)
 browser.close()
r={'suite':'Copy/scope browser integration','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results}
OUT.write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(bool(r['failed']))
