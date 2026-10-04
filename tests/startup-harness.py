#!/usr/bin/env python3
"""Bounded harness setup regression. Synthetic faults, no physical origin/performance claim.
Exact candidate and setup budgets are exercised; labelled fault copies are not release bytes.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout
import hashlib,json,sys,time,traceback
ROOT=Path(__file__).resolve().parents[1]
FILE=Path(sys.argv[1]);OUT=Path(sys.argv[2]);SHOTS=Path(sys.argv[3])
HTML=FILE.read_text();APP="document.querySelector('[x-data]')._x_dataStack[0]"
source=(ROOT/'tests/browser.py').read_text().split('with sync_playwright() as pw:')[0]
assert 'self.page.set_content(html, timeout=15000)' in source
assert 'self.page.set_default_timeout(6000)' in source
assert "timeout=10000)" in source
new={'__file__':str(ROOT/'tests/browser.py')};exec(compile(source,str(ROOT/'tests/browser.py'),'exec'),new)
oldsource=source.replace('self.page.set_content(html, timeout=15000)','self.page.set_content(html)',1)
old={'__file__':str(ROOT/'tests/browser.py')};exec(compile(oldsource,str(ROOT/'tests/browser.py'),'exec'),old)
results=[];observations=[]
def record(name,fn):
    start=time.monotonic()
    try: fn();result={'name':name,'status':'passed'}
    except Exception as e: result={'name':name,'status':'failed','error':str(e),'traceback':traceback.format_exc()}
    result['seconds']=round(time.monotonic()-start,3);results.append(result)
    OUT.write_text(json.dumps(report(False),indent=2)+'\n')
def report(complete):
    return {'suite':'Bounded document setup regression','complete':complete,'test_range':'1:3','total_defined':3,
      'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),
      'scope':'Offline Chromium; deliberately delayed/unready fixtures. Not the established cause of the isolated rc1 timeout; not physical or deployment acceptance.',
      'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),
      'results':results,'observations':observations}
def cleanup(browser):
    for c in list(browser.contexts): c.close()
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    def exact():
        try:
            h=new['Harness'](browser,width=1440,height=950)
            assert h.call('return !!a.seed.value && a.seedQrVisible && !a.acknowledged')
            assert not h.errors and not h.requests,(h.errors,h.requests)
            assert h.page.locator('#new-test-wallet').is_visible()
            assert h.page.evaluate("document.documentElement.dataset.appReady")=='true'
            observations.append({'mode':'exact-candidate','ready':True,'pageErrors':h.errors,'networkRequests':h.requests})
        finally:cleanup(browser)
    record('H-B01 exact candidate loads with fixed setup and unchanged interaction/readiness budgets',exact)
    def delayed():
        # A finite prelude before the app simulates document setup outside its own reference gate.
        # It does not alter the gate or turn an unready application into a pass.
        prelude='<script>/* DELIBERATELY DELAYED TEST FIXTURE */ const fixtureUntil=performance.now()+6500; while(performance.now()<fixtureUntil) {}</script>'
        assert HTML.count('<head>')==1
        fixture=HTML.replace('<head>','<head>'+prelude,1)
        try:
            caught=None;start=time.monotonic()
            try:old['Harness'](browser,html=fixture,width=1440)
            except PlaywrightTimeout as e:caught=str(e)
            observations.append({'mode':'old-budget-delayed-fixture','elapsedSeconds':round(time.monotonic()-start,3),'expectedTimeout':caught})
            assert caught and '6000ms' in caught and 'set_content' in caught,caught
        finally:cleanup(browser)
        try:
            start=time.monotonic();h=new['Harness'](browser,html=fixture,width=1440)
            elapsed=time.monotonic()-start
            assert elapsed>=6 and elapsed<18,elapsed
            assert h.call('return !!a.seed.value && a.seedQrVisible') and not h.errors
            observations.append({'mode':'explicit-budget-delayed-fixture','elapsedSeconds':round(elapsed,3),'ready':True,'retries':0})
        finally:cleanup(browser)
    record('H-B02 old deadline rejects delayed fixture while bounded setup permits its genuine readiness',delayed)
    def unready():
        try:
            caught=None;start=time.monotonic()
            try:new['Harness'](browser,html='<!doctype html><html><head></head><body>UNREADY TEST FIXTURE</body></html>')
            except PlaywrightTimeout as e:caught=str(e)
            elapsed=time.monotonic()-start
            assert caught and 'wait_for_function' in caught and '10000ms' in caught,caught
            assert elapsed>=9 and elapsed<15,elapsed
            observations.append({'mode':'never-ready-fixture','elapsedSeconds':round(elapsed,3),'expectedTimeout':caught,'retries':0})
        finally:cleanup(browser)
    record('H-B03 unready page remains a terminal app-readiness timeout with no retry',unready)
    browser.close()
r=report(True);OUT.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(1 if r['failed'] else 0)
