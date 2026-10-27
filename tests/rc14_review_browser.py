#!/usr/bin/env python3
"""Targeted review contract: actual Chromium DOM, 6 viewport/theme combinations.
No device attestation or coverage substitution for frozen canonical 139-job suite.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
HTML=Path(sys.argv[1]).read_text()
results=[]
def check(cond,msg):
    if not cond:raise AssertionError(msg)
with sync_playwright() as p:
    browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    for width in (390,768,1440):
      for theme in ('light','dark'):
        page=browser.new_page(viewport={'width':width,'height':900},color_scheme=theme)
        errors=[];requests=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http://','https://')) else None)
        page.set_content(HTML,wait_until='domcontentloaded')
        page.wait_for_selector('html[data-app-ready="true"]',timeout=25000)
        page.evaluate('(theme)=>document.querySelector(".shell")._x_dataStack[0].setThemePreference(theme)',theme)
        check(page.evaluate('document.documentElement.dataset.theme')==theme,'wrong theme')
        check(page.locator('#tbw-landing-title').inner_text()=='Test your signing device','landing text')
        check(page.locator('#tbw-landing-title').count()==1,'duplicate landing heading')
        check(page.locator('.tbw-side-card.tbw-next-card').count()==0,'third step list still exists')
        check(page.locator('.tbw-guidance-panel .tbw-help-card').count()==1,'missing guided help')
        check(page.locator('.tbw-settings-visible-label').is_visible(),'Settings has no visible label')
        check(page.locator('.tbw-settings .tbw-drawer-about').text_content().find('unsigned development preview')==-1,'stale status')
        check(page.locator('.tbw-settings .tbw-drawer-about').text_content().find('Publisher authentication has not been verified')!=-1,'build status notice')
        check(page.locator('footer a[href="https://www.thebitcoinway.com/"]').count()==1,'official site link absent')
        check(page.locator('footer').inner_text().find('MIT license')!=-1,'license spelling')
        check(page.locator('#wallet-loaded').count()==1,'fingerprint action lost')
        check(page.locator('#new-test-wallet').count()==1,'wallet reset lost')
        check(page.locator('.tbw-wallet-panel .wallet-safety-card').count()==1,'wallet safety notice lost')
        check(page.locator('#supported-scope').inner_text().count('Never')==0,'duplicated wallet warning')
        check(page.locator('.tbw-wallet-panel .seed-instructions').inner_text().count('disposable')==0,'duplicate word warning')
        check(page.locator('.scenario-note').is_hidden(),'unprompted edge case warning')
        check(page.evaluate('document.body.scrollWidth<=innerWidth+1'),f'horizontal overflow landing {width}/{theme}')
        check(page.locator('.brand-name').evaluate('e=>Math.abs(e.getBoundingClientRect().height-parseFloat(getComputedStyle(e).lineHeight))<=2'),f'wordmark wrapped {width}/{theme}')
        page.locator('.tbw-settings summary').click()
        check(page.locator('.tbw-settings').get_attribute('open') is not None,'settings did not open')
        check('Session history' in page.locator('.tbw-drawer-workspace').inner_text(),'session not discoverable')
        check('Advanced testing' in page.locator('.tbw-drawer-workspace').inner_text(),'advanced not discoverable')
        page.locator('.tbw-close-settings').click()
        page.locator('#start-safe-test').click()
        check(page.locator('#prepare-title').is_visible(),'wallet setup absent')
        check(not page.locator('.tbw-side-card.tbw-next-card').count(),'repeated sidebar')
        check(page.locator('#wallet-loaded').is_visible(),'fingerprint action hidden')
        if width==1440:
            dims=page.locator('#wallet-loaded').evaluate('e=>{const r=e.getBoundingClientRect(),s=getComputedStyle(e);return {height:r.height,line:parseFloat(s.lineHeight),padding:parseFloat(s.paddingTop)+parseFloat(s.paddingBottom),nowrap:s.whiteSpace}}')
            check(dims['nowrap']=='nowrap' and dims['height']<54,f'fingerprint action wrapped {dims}')
        check(page.evaluate('document.body.scrollWidth<=innerWidth+1'),f'horizontal overflow setup {width}/{theme}')
        page.locator('.topbar a.help-control').click()
        check(page.locator('#help').is_visible(),'Help navigation failed')
        check('Settings, then Session history' in page.locator('#help').inner_text(),'stale Help copy')
        page.locator('#disposable-wallet>summary').click()
        check(page.locator('#disposable-wallet .details-body').is_visible(),'FAQ inaccessible')
        help_ratio=page.locator('#disposable-wallet').evaluate('e=>e.querySelector(".details-body").getBoundingClientRect().width/e.getBoundingClientRect().width')
        check(help_ratio>.93,f'FAQ wastes width: {help_ratio}')
        check(page.evaluate('document.body.scrollWidth<=innerWidth+1'),'Help overflow')
        page.locator('#help .help-navigation a').click()
        page.evaluate('''()=>{const a=document.querySelector('.shell')._x_dataStack[0];a.landingDismissed=true;a.workspaceView='test';a.step=2;a.generatedScenario='boundary'}''')
        page.wait_for_function('document.querySelector(".scenario-note").getClientRects().length>0')
        page.evaluate('''()=>{document.querySelector('.shell')._x_dataStack[0].generatedScenario='normal'}''')
        page.wait_for_function('document.querySelector(".scenario-note").getClientRects().length===0')
        check(page.locator('#sign-title').inner_text()=='Review and sign the test transaction','duplicate second step heading')
        # Inspect rendered CSS using a visual fixture mounted inside the real test workspace.
        checks=page.evaluate('''() => {
            const target=document.querySelector('#test-view');
            const div=document.createElement('div');div.setAttribute('data-testid','review-style-fixture');
            div.innerHTML=`<div class="result" data-result-state="match"><div class="result-header"><div class="result-message"><h3>Signatures matched</h3><p>This match applies to this transaction only.</p></div></div><div class="result-tools"><summary><span class="disclosure-copy"><strong>Evidence &amp; technical details</strong></span></summary></div></div><div class="transaction-summary"><div class="scenario-line"><strong>Small payment</strong></div></div>`;
            target.appendChild(div);
            function rgba(x){let m=x.match(/([0-9.]+)/g);return m?m.slice(0,3).map(Number):[0,0,0]}
            function luminance(v){let v2=v.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4});return .2126*v2[0]+.7152*v2[1]+.0722*v2[2]}
            function cr(a,b){const la=luminance(rgba(a)),lb=luminance(rgba(b));return (Math.max(la,lb)+.05)/(Math.min(la,lb)+.05)}
            function check(selector,bg){let e=div.querySelector(selector),style=getComputedStyle(e),parent=div.querySelector(bg),surf=getComputedStyle(parent);return {ratio:cr(style.color,surf.backgroundColor),fg:style.color,bg:surf.backgroundColor}}
            let out={heading:check('.result-message h3','.result'),explanation:check('.result-message p','.result'),evidence:check('.result-tools strong','.result-tools'),scenario:check('.scenario-line strong','.transaction-summary'),green:getComputedStyle(div.querySelector('.result')).backgroundColor};
            div.remove();return out;
        }''')
        if theme=='light':
            for name in ('heading','explanation','evidence','scenario'):
                check(checks[name]['ratio']>=4.5,f'low contrast {width}/{name}: {checks[name]}')
            check('233, 245, 237' in checks['green'],f'match card not green: {checks["green"]}')
        if theme=='light':
            why=page.locator('#test-view .report-section a[href="#repeat-tests"]').evaluate('''e=>{let c=getComputedStyle(e).color;return c}''')
            check(why=='rgb(113, 72, 23)',f'Why repeat link is too pale: {why}')
            limitation=page.locator('#test-view .result-limit strong').evaluate('e=>getComputedStyle(e).color')
            check(limitation=='rgb(17, 24, 32)',f'match limitation faint: {limitation}')
        check(not errors,f'Browser errors: {errors}')
        check(not requests,f'Unexpected external requests: {requests}')
        results.append({'width':width,'theme':theme,'contrasts':checks,'help_width_ratio':round(help_ratio,3),'errors':errors,'network_requests':requests,'status':'passed'})
        page.close()
    browser.close()
print(json.dumps({'status':'passed','cases':len(results),'results':results},indent=2))
