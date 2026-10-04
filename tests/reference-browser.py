#!/usr/bin/env python3
"""Exact HTML startup safety and calm presentation; no physical signer/optical evidence."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())
def technical(h):
 h.page.get_by_role('link',name='Help',exact=True).click()
 link=h.page.locator('.help-contents a[href="#technical-help"]');g=link.locator('xpath=ancestor::details[1]')
 if not g.evaluate('(e)=>e.open'):g.locator(':scope > summary').click()
 link.click();h.page.wait_for_timeout(40)
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 environment={'browser':browser.version,'origin':'offline setContent; no UUID shim for candidate','hardware':False,'optical':False,'scope':'startup known-answer check, not release/browser authentication'}
 for width in [320,390,768,1440]:
  def ordinary(w=width):
   h=Harness(browser,width=w,height=1050);assert h.call('return a.referenceSelfCheck.phase')=='passed'
   assert h.call('return a.referenceSelfCheck.checked')==48
   assert h.call('return a.sessionChecks.length')==0
   assert not h.page.locator('#reference-self-check-note').is_visible();layout(h)
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'reference-wallet-{w}.png'),full_page=True)
   before=snapshot(h);technical(h)
   assert '48 of 48 known answers passed' in h.page.locator('#reference-self-check-note').inner_text()
   assert 'BIP 461 (Draft)' in h.page.locator('#technical-help').inner_text();layout(h)
   if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'reference-help-{w}.png'),full_page=True)
   h.page.get_by_role('link',name='Back to test',exact=True).click();assert snapshot(h)==before;close(h)
  test(f'R-B startup succeeds quietly and technical Help preserves state at {width}px',ordinary)
 def one_lifetime():
  h=Harness(browser,width=390);a=h.call('return a.referenceSelfCheck');data=h.config();h.accept(data['tx']);assert h.call('return a.resultState')=='match'
  report=h.call('return a.report()');h.workspace('advanced');h.workspace('session');h.workspace('test')
  assert h.call('return a.report()')==report;assert h.call('return a.referenceSelfCheck')==a
  h.call('a.randomizeTransaction()');assert h.call('return a.referenceSelfCheck')==a;assert h.call('return a.sessionSummary.checked')==1;close(h)
 test('R-B05 repeated workspaces and transactions retain one passed startup status, not extra test counts',one_lifetime)
 def reduced():
  h=Harness(browser,width=390);d=h.config();h.accept(sign_psbt(d['psbt'],d['tx']).hex());assert h.call('return a.resultDisplayState')=='match'
  assert not h.page.locator('#reference-self-check-note').is_visible();assert not h.page.locator('#returned-file-details').is_visible();layout(h);close(h)
 test('R-B06 routine results do not gain new self-test badges or metadata clutter',reduced)
 def review():
  h=Harness(browser,width=390);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());assert h.call('return a.resultDisplayState')=='review'
  assert h.page.locator('.file-review-action').is_visible();report=h.call('return a.report()');technical(h)
  h.page.get_by_role('link',name='Back to test',exact=True).click();assert h.call('return a.report()')==report;layout(h);close(h)
 test('R-B07 successful startup check never downgrades unexpected metadata review',review)
 for width in [320,1440]:
  def large(w=width):
   h=Harness(browser,width=w,height=1100);technical(h);h.page.evaluate(ENLARGE);layout(h);close(h)
  test(f'R-B technical audit explanations reflow with doubled text at {width}px',large)
 def fail_page(kind):
  context=browser.new_context(viewport={'width':390,'height':900},offline=True);page=context.new_page();requests=[];page.on('request',lambda r:requests.append(r.url))
  page.evaluate('() => {window.rngCalls=0;const rng=crypto.getRandomValues.bind(crypto);crypto.getRandomValues=(...args)=>{rngCalls++;return rng(...args)};}')
  if kind=='missing':broken=HTML.replace('const tbwReferenceSelfTest =', 'const deliberatelyRemovedGate =', 1)
  elif kind=='answer':
   # Corrupt only a fixed expected DER byte. Exercise exact current page, not a clean substitute.
   start=HTML.index('const TBW_REFERENCE_VECTORS');i=HTML.index('"plain_der":"',start)+len('"plain_der":"')
   broken=HTML[:i]+('31' if HTML[i:i+2]!='31' else '30')+HTML[i+2:]
  elif kind=='signer':broken=HTML.replace('    tbwReferenceSelfTest.apply();','    Op = () => { throw Error("injected signer fault"); };\n    tbwReferenceSelfTest.apply();',1)
  else:raise ValueError(kind)
  assert broken!=HTML;page.set_content(broken);page.wait_for_timeout(1000)
  assert page.evaluate('document.documentElement.dataset.appReady')=='false'
  assert not page.locator('.shell').is_visible();assert page.locator('#startup-status').is_visible()
  assert page.evaluate('window.rngCalls')==0
  assert page.locator('#startup-title').inner_text()=='Reference self-check failed';assert 'No test wallet was created' in page.locator('#startup-message').inner_text()
  assert not requests
  if kind=='answer':page.screenshot(path=str(SHOTS/'reference-startup-failed-390.png'),full_page=True)
  context.close()
 for kind in ['answer','signer','missing']:
  test('R-B startup '+kind+' fault hides wallet/import controls before random key generation',lambda k=kind:fail_page(k))
 def no_optional():
  h=Harness(browser);h.page.evaluate('document.querySelector("#help").remove();document.querySelector("#try-example").remove();document.querySelector("#attack-example").remove()')
  data=h.config();h.accept(data['tx']);assert h.call('return a.resultState')=='match';assert h.call('return a.referenceSelfCheck.phase')=='passed';close(h)
 test('R-B13 Help/demo absence neither blocks nor substitutes for mandatory startup self-check',no_optional)
 def contrast_keyboard():
  h=Harness(browser,width=390);technical(h)
  h.page.emulate_media(forced_colors='active');layout(h)
  h.page.get_by_role('link',name='BIP 461 proposal and review',exact=True).focus();assert h.page.evaluate('document.activeElement.textContent')=='BIP 461 proposal and review';close(h)
 test('R-B14 reference source link is keyboard accessible and high-contrast Help remains readable',contrast_keyboard)
 browser.close()
result={'suite':'Reference audit startup and UX browser simulations','complete':True,'testRange':TEST_RANGE,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results}
OUT.write_text(json.dumps(result,indent=2));print(json.dumps({'passed':result['passed'],'failed':result['failed']},indent=2));sys.exit(bool(result['failed']))
