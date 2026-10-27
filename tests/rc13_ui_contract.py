#!/usr/bin/env python3
"""Scoped RC13 presentation smoke tests in a Chromium document context.
No signer, live origin, file-origin or end-to-end wallet security conclusion.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
HTML=Path(sys.argv[1]).read_text() if len(sys.argv)>1 else None
if not HTML: raise SystemExit('Usage: python tests/rc13_ui_contract.py /absolute/path/app.html')
results=[]
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    for width in (390,768,1440):
        for theme in ('light','dark'):
            page=b.new_page(viewport={'width':width,'height':900},device_scale_factor=1)
            errs=[];requests=[]
            page.on('pageerror',lambda e:errs.append(str(e)))
            page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http://','https://')) else None)
            page.set_content(HTML,wait_until='domcontentloaded')
            page.wait_for_selector('html[data-app-ready="true"]',timeout=23000)
            if page.evaluate('document.documentElement.dataset.theme')!=theme:
                page.locator('.tbw-header-theme').click()
                page.wait_for_function('(t)=>document.documentElement.dataset.theme===t',arg=theme)
            assert page.locator('#tbw-landing-title').inner_text()=='Test your signing device'
            assert page.locator('#start-safe-test').inner_text().startswith('Start test')
            assert page.locator('.tbw-purpose-note').count()==0
            assert 'A match does not prove firmware is safe.' in page.locator('.tbw-landing-lede').inner_text()
            assert 'Use a disposable test wallet only' in page.locator('.tbw-safety').inner_text()
            assert not page.locator('.scenario-note').is_visible(),f'Boundary warning shown in default test: {width}/{theme}'
            assert page.locator('.tbw-settings-icon').count()==1
            assert 21<=float(page.locator('.tbw-settings-icon').evaluate('(e)=>getComputedStyle(e).width').replace('px',''))<=24
            assert page.locator('.tbw-settings summary').get_attribute('aria-label')=='Open settings'
            assert page.locator('.tbw-settings summary').bounding_box()['width']>=40
            assert page.locator('body').evaluate('(e)=>e.scrollWidth <= window.innerWidth+1'),f'Horizontal overflow {width}'
            # Check real settings drawer remains reachable and closes.
            page.locator('.tbw-settings summary').click()
            assert page.locator('.tbw-settings').get_attribute('open') is not None
            page.locator('.tbw-close-settings').click()
            assert page.locator('.tbw-settings').get_attribute('open') is None
            # Help link, FAQ and return route.
            page.locator('.topbar [href="#help"]').click()
            page.locator('#disposable-wallet > summary').click()
            assert page.locator('#disposable-wallet').get_attribute('open') is not None
            dims=page.locator('#disposable-wallet').evaluate('''e=>{
              const a=e.getBoundingClientRect(),b=e.querySelector('.details-body').getBoundingClientRect();
              return {container:a.width,answer:b.width,bodyMax:getComputedStyle(e.querySelector('.details-body')).maxWidth}
            }''')
            assert dims['answer']/dims['container']>.93,f'Help wastes width: {dims}'
            assert page.locator('#disposable-wallet .details-body').is_visible()
            assert page.locator('#help').evaluate('(e)=>e.getBoundingClientRect().width')<=1081
            assert page.locator('body').evaluate('(e)=>e.scrollWidth <= window.innerWidth+1')
            page.locator('#help .help-navigation a').click()
            assert page.locator('#tbw-landing-title').is_visible()
            # UI contract: explicit boundary scenario only, and hidden after going back.
            page.evaluate('''()=>{const d=document.querySelector('.shell')._x_dataStack[0];d.landingDismissed=true;d.workspaceView='test';d.step=2;d.generatedScenario='boundary'}''')
            page.wait_for_function('document.querySelector(".scenario-note").getClientRects().length > 0')
            assert page.locator('.scenario-note').is_visible()
            page.evaluate('''()=>{document.querySelector('.shell')._x_dataStack[0].generatedScenario='normal'}''')
            page.wait_for_function('document.querySelector(".scenario-note").getClientRects().length === 0')
            assert not page.locator('.scenario-note').is_visible()
            assert not errs,errs
            assert not requests,requests
            results.append({'width':width,'theme':theme,'help_dimensions':dims,'app_errors':len(errs),'network_requests':len(requests),'passed':True})
            if width==1440:
                # Save only one screen per theme, optional qualitative review.
                page.locator('.topbar a.brand').click()
                page.screenshot(path=f'/mnt/data/signlab-rc13-{theme}.png')
            page.close()
    b.close()
print(json.dumps({'status':'passed','browser_document_context_cases':len(results),'results':results},indent=2))
