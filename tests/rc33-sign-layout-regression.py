#!/usr/bin/env python3
"""RC33 targeted CSS safety regression, synthetic browser only, never a release certificate."""
from pathlib import Path
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0], globals())
RULE='#test-view .sign-layout[style*="display: none"]{display:none!important}'
assert HTML.count(RULE)==1,'RC33 safety rule missing/duplicated'

def signing_state(h):
    return h.page.locator('.sign-layout').evaluate('(e)=>({visible:e.checkVisibility(),style:e.getAttribute("style"),computed:getComputedStyle(e).display})')

def invalid(h):
    h.workspace('test');h.page.locator('#wallet-loaded').click();h.open_settings()
    h.page.locator('#locktime').fill('invalid-locktime')
    h.page.locator('#advanced-tools>summary').click();h.workspace('test')
    h.page.wait_for_function('!!('+APP+').buildProblem')
    assert not h.call('return a.transactionReady')
    assert h.call('return a.buildProblem')
    return signing_state(h)

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    def safe_failure():
        h=Harness(browser);state=invalid(h)
        assert state['visible'] is False and state['computed']=='none',state
        assert h.page.locator('[x-text="buildProblem"]:visible').count()>0
        assert not h.errors and not h.requests,(h.errors,h.requests)
        h.close()
    test('RC33 invalid locktime hides entire stale signing layout with visible error',safe_failure)
    def valid_flow():
        h=Harness(browser);h.workspace('test');h.page.locator('#wallet-loaded').click()
        assert h.call('return a.transactionReady')
        assert signing_state(h)['visible'] is True,signing_state(h)
        assert not h.errors and not h.requests,(h.errors,h.requests)
        h.close()
    test('RC33 valid PSBT retains visible signing layout',valid_flow)
    def mutation_detected():
        tampered=HTML.replace(RULE,' ' * len(RULE))
        assert tampered!=HTML
        h=Harness(browser,html=tampered)
        state=invalid(h)
        assert state['visible'] is True,state
        h.close()
    test('RC33 negative mutation reproduces unsafe stale-layout visibility',mutation_detected)
    browser.close()
receipt={'suite':'RC33 sign-layout visibility and negative mutation','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'artifact':FILE.name,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(i['status']=='passed' for i in results),'failed':sum(i['status']=='failed' for i in results),'results':results,'acceptance':False}
OUT.write_text(json.dumps(receipt,indent=2));print(json.dumps({k:receipt[k] for k in ('passed','failed','complete')}));sys.exit(bool(receipt['failed']))
