#!/usr/bin/env python3
"""Visible-navigation retirement smoke; use original browser Harness, no new coordinator.
Usage: python tests/rc30-retired-nav-smoke.py APP.html RECEIPT.json SHOTS
"""
from pathlib import Path
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0],globals())
with sync_playwright() as pw:
 browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
 for width in (320,390,1440):
  def check(width=width):
   h=Harness(browser,width=width)
   assert h.page.locator('nav.workspace-nav,#workspace-test,#workspace-advanced,#workspace-session,.workspace-alert').count()==0
   drawer=h.page.locator('#tbw-settings > summary');assert drawer.is_visible()
   box=drawer.bounding_box();assert box and box['width']>=44 and box['height']>=44,(width,box)
   drawer.focus();assert drawer.evaluate('(e)=>document.activeElement===e')
   h.workspace('test')
   original=h.call('return JSON.stringify([a.walletSession,a.stateSignature,a.sessionHistory,a.sessionSummary,a.signingPolicy])')
   for view in ('advanced','session','test'):
    h.workspace(view)
    assert h.call('return a.workspaceView')==view
    assert h.call('return JSON.stringify([a.walletSession,a.stateSignature,a.sessionHistory,a.sessionSummary,a.signingPolicy])')==original
    assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
   assert not h.errors,h.errors
   assert not h.requests,h.requests
   h.close()
  test(f'RC30 visible navigation, focus and state invariants at {width}px',check)
 browser.close()
r={'suite':'RC30 scoped retired navigation','complete':True,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),
   'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results,
   'hardwareAcceptance':False,'publisherAuthenticated':False}
OUT.write_text(json.dumps(r,indent=2)+'\n')
print('TOTAL',r['passed'],r['failed']);sys.exit(bool(r['failed']))
