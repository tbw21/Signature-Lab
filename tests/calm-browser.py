#!/usr/bin/env python3
"""Calm workspace acceptance: actual DOM/QR pixels; synthetic signer/camera only."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())

def nav(h,view):
    h.page.locator('#workspace-'+view).click();h.page.wait_for_timeout(50)

def same(h):
    return h.call('return JSON.stringify([a.stateSignature,a.psbtBase64,a.variants,a.walletSession,a.preparedRevision,a.sessionChecks,a.resultState,a.isTestComplete,a.signingPolicy])')

def navigation(h):
    bs=h.page.locator('.workspace-nav>button');assert bs.count()==3
    boxes=bs.evaluate_all('(es)=>es.map(e=>{const r=e.getBoundingClientRect();return {w:r.width,h:r.height}})')
    assert max(x['w'] for x in boxes)-min(x['w'] for x in boxes)<2,boxes
    assert all(x['h']>=44 for x in boxes),boxes
    assert h.page.locator('.workspace-nav>button[aria-pressed="true"]').count()==1
    assert all(bs.nth(i).is_visible() for i in range(3))

def tx20(h):
    h.config()
    h.call('''a.invalidate();a.outputs=Array.from({length:20},(_,i)=>({id:30000+i,amount:{value:String(600+i),error:null},dest:{value:'m/84h/0h/0h/'+(i%2)+'/'+(50+i),error:null}}));a.recompute();a.goToStep(2)''')
    h.page.wait_for_timeout(40)
    assert h.call('return a.outputReview.outputs.length')==20

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    environment={'browser':browser.version,'origin':'offline exact-HTML harness','physicalSigner':False,'realOpticalScan':False}
    for width in [320,360,390,438,768,1024,1440]:
        def views(w=width):
            h=Harness(browser,width=w,height=950);before=same(h);navigation(h);layout(h)
            for view in ['advanced','session','test']:
                nav(h,view);assert same(h)==before;navigation(h);layout(h)
                if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'calm-{view}-{w}.png'),full_page=True)
            h.page.locator('#wallet-loaded').click();layout(h)
            if w in [390,1440]:h.page.screenshot(path=str(SHOTS/f'calm-transaction-{w}.png'),full_page=True)
            close(h)
        test(f'Calm equally sized workspace controls and all views at {width}px',views)
    def keyboard_nav():
        h=Harness(browser,width=390);before=same(h)
        for view,key in [('advanced','Enter'),('session','Space'),('test','Enter')]:
            control=h.page.locator('#workspace-'+view);control.focus();assert control.evaluate('(e)=>getComputedStyle(e).outlineStyle')!='none'
            h.page.keyboard.press(key);h.page.wait_for_timeout(70);assert h.call('return a.workspaceView')==view;assert same(h)==before
        close(h)
    test('Calm native keyboard workspace activation preserves authoritative state',keyboard_nav)
    for width in [320,438,1440]:
        def enlarged_nav(w=width):
            h=Harness(browser,width=w,height=1000);h.config();h.call('a.goToStep(1)');h.page.evaluate(ENLARGE)
            for view in ['advanced','session','test']:
                nav(h,view);layout(h);navigation(h)
            close(h)
        test(f'Calm 200-percent text navigation and workspace reflow at {width}px',enlarged_nav)
    def spacing_nav():
        h=Harness(browser,width=390);h.page.add_style_tag(content=TEXT_SPACE)
        for view in ['advanced','session','test']:nav(h,view);layout(h);navigation(h)
        close(h)
    test('Calm increased text spacing preserves all workspace controls',spacing_nav)
    def force_colors():
        h=Harness(browser,width=390);h.page.emulate_media(forced_colors='active');navigation(h)
        assert h.page.locator('#workspace-test').evaluate('(e)=>parseFloat(getComputedStyle(e).borderTopWidth)')>=2
        nav(h,'advanced');layout(h);close(h)
    test('Calm forced colors retain explicit selected-state border',force_colors)
    def outputs():
        h=Harness(browser,width=390);tx20(h);before=same(h)
        assert not h.page.locator('#advanced-view').is_visible();h.page.locator('#output-review>summary').click()
        assert h.page.locator('.review-output:visible').count()==20
        rows=h.call('return a.outputReview.outputs')
        for i,row in enumerate(rows):
            element=h.page.locator('.review-output').nth(i);assert element.locator('.output-address').inner_text()==row['address']
            assert h.call('return a.formatReviewAmount(arg)',row['amountSats'])==element.locator('.output-value').inner_text()
        assert same(h)==before;layout(h);h.page.screenshot(path=str(SHOTS/'calm-20-outputs-390.png'),full_page=True);close(h)
    test('Calm 20 full output amounts and addresses visible without opening the editor',outputs)
    def output_units():
        h=Harness(browser,width=390);tx20(h);h.page.locator('#output-review>summary').click();before=same(h)
        h.page.get_by_role('button',name='Sats',exact=True).click();assert '600 sats' in h.page.locator('.output-value').first.inner_text();assert same(h)==before;close(h)
    test('Calm output amount unit switch changes display only',output_units)
    def stale_output():
        h=Harness(browser);tx20(h);h.page.locator('#output-review>summary').click();h.open_settings();h.page.locator('#locktime').fill('bad')
        nav(h,'test');h.page.wait_for_function('!!('+APP+').buildProblem')
        assert not h.page.locator('.sign-layout').is_visible();assert h.page.locator('[x-text="buildProblem"]:visible').count();close(h)
    test('Calm invalid edited state hides the old QR and output addresses',stale_output)
    def helper_failure():
        h=Harness(browser);h.config();h.call("Object.defineProperty(a,'outputReview',{get(){return {ok:false,outputs:[],problem:'Output details are unavailable. Do not sign until the full destination list can be reviewed.'}}});a.preparedRevision++")
        h.page.wait_for_timeout(50);assert not h.page.locator('.sign-layout').is_visible();assert h.page.locator('[x-text="outputReview.problem"]').is_visible();close(h)
    test('Calm failed read-only projection has a visible stop-review explanation',helper_failure)
    def clean_result():
        h=Harness(browser,width=390);d=h.config();h.accept(d['tx']);assert h.call('return a.resultState')=='match'
        assert not h.page.locator('.metadata-assessment').is_visible();assert h.page.locator('.result-limit:visible').count()==1
        assert h.page.get_by_role('button',name='Save result',exact=True).is_visible();h.file_details();assert h.page.locator('.metadata-assessment').is_visible();layout(h);close(h)
    test('Calm normal result is compact while original technical details remain accessible',clean_result)
    def amber():
        h=Harness(browser,width=390);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex())
        assert h.call('return a.resultDisplayState')=='review';assert h.page.locator('.file-review-action').is_visible()
        assert h.page.locator('.result').get_attribute('data-result-state')=='review';h.page.get_by_role('button',name='Inspect file changes',exact=True).click()
        assert h.page.locator('.metadata-assessment').is_visible();assert h.page.locator('#returned-file-details').evaluate('(e)=>e.open');layout(h)
        h.page.screenshot(path=str(SHOTS/'calm-review-390.png'),full_page=True);close(h)
    test('Calm unresolved file changes stay amber and open directly from the main result',amber)
    def earlier_issue():
        h=Harness(browser,width=390);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());h.page.locator('#next-transaction').click()
        h.accept(h.call('return a.variants[0].txHex'));assert h.call('return a.resultDisplayState')=='match';assert h.page.locator('.workspace-alert').is_visible()
        nav(h,'session');assert h.page.locator('.history-item[data-finding="review"]').count()==1
        nav(h,'advanced');assert h.page.locator('.workspace-alert').is_visible();close(h)
    test('Calm a later match cannot conceal the session previous unresolved file finding',earlier_issue)
    def download_result():
        h=Harness(browser);d=h.config();h.accept(d['tx']);expected=h.call('return a.exportEvidence()')
        with h.page.expect_download() as event:h.page.get_by_role('button',name='Save result',exact=True).click()
        download=event.value;raw=Path(download.path()).read_bytes();got=json.loads(raw)
        assert got==expected;assert re.fullmatch(r'detail-[0-9a-f]{12}\.json',download.suggested_filename)
        assert download.suggested_filename=='detail-'+hashlib.sha256(raw).hexdigest()[:12]+'.json';assert d['seed'] not in raw.decode();close(h)
    test('Calm primary Save result downloads exact evidence with short content-derived filename',download_result)
    def summary_result():
        h=Harness(browser);d=h.config();h.accept(d['tx']);expected=h.call('return a.report()')
        with h.page.expect_download() as event:h.summary_download().click()
        download=event.value;got=json.loads(Path(download.path()).read_text());assert got==expected;assert download.suggested_filename.startswith('record-');close(h)
    test('Calm summary-only export remains an explicit secondary choice',summary_result)
    def incomplete():
        h=Harness(browser,width=320);h.config();h.accept('bad');assert h.call('return a.resultState')=='incomplete';assert h.page.locator('.result h3').inner_text()=='Could not complete the check'
        with h.page.expect_download() as event:h.page.get_by_role('button',name='Save result',exact=True).click()
        data=json.loads(Path(event.value.path()).read_text());assert data['schema']=='tbw-signature-result-v2' and data['result']=='incomplete';close(h)
    test('Calm incomplete unparseable results stay visible and export summary not success',incomplete)
    def inert_notes():
        h=Harness(browser);h.open_tools();h.page.locator('#device-notes>summary').click();text='<img src=x onerror="window.attack=true">'
        h.page.locator('#firmware').fill(text);nav(h,'test');h.page.locator('#wallet-loaded').click();h.accept(h.call('return a.variants[0].txHex'))
        assert h.call('return a.report().firmware')==text;nav(h,'session');assert h.page.evaluate('window.attack===true') is False;close(h)
    test('Calm operator labels cannot inject markup or change device attestation',inert_notes)
    def capture_nav():
        h=Harness(browser,media=True,width=390);h.config();h.call('a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="scanning"')
        before=h.page.evaluate('window.mediaCalls')
        for view in ['test','advanced','session']:assert h.page.locator('#workspace-'+view).is_disabled()
        h.call('a.openWorkspace("advanced")');assert h.call('return a.workspaceView')=='test';assert h.page.evaluate('window.mediaCalls')==before
        h.call('a.stopScan()');nav(h,'advanced');assert h.page.evaluate('window.mediaCalls')==before;close(h)
    test('Calm workspace navigation never reacquires camera or hides live capture',capture_nav)
    def halted_advanced():
        h=planned(browser);h.page.locator('#wallet-loaded').click();h.accept('bad');assert h.call('return a.guidedStatus.phase')=='halted';nav(h,'advanced')
        assert h.page.locator('.guided-status').is_visible();assert h.page.locator('.guided-stop-reason').is_visible();assert h.page.locator('#start-guided-session').is_disabled() or not h.page.locator('#start-guided-session').is_visible();close(h)
    test('Calm guided failure remains visible even in the advanced workspace',halted_advanced)
    def late_focus():
        h=Harness(browser);h.call('a.openWorkspace("advanced");a.openWorkspace("session");a.openWorkspace("test")');h.page.wait_for_timeout(200)
        assert h.call('return a.workspaceView')=='test';assert h.page.evaluate('!document.activeElement.closest("#advanced-view,#session-view")');close(h)
    test('Calm fast repeated navigation cannot leave keyboard focus in a hidden view',late_focus)
    def controls_single():
        h=Harness(browser,width=390);h.page.locator('#wallet-loaded').click();assert h.page.locator('.return-actions [aria-label="Paste signed transaction"]').inner_text().strip()=='Paste'
        qr=h.page.locator('#qr-format button').first.evaluate('(e)=>{const s=getComputedStyle(e);return [s.fontSize,s.padding,s.minHeight]}')
        h.call('a.goToStep(1)');seed=h.page.locator('#word-count button').first.evaluate('(e)=>{const s=getComputedStyle(e);return [s.fontSize,s.padding,s.minHeight]}');assert seed==qr,(seed,qr);close(h)
    test('Calm paste label appears once and QR/seed segmented controls share sizing',controls_single)
    def large_history():
        h=Harness(browser,width=320);h.config();h.call("Object.defineProperty(a,'sessionSummary',{get(){return {checked:2000,matched:1999,differed:1,suggested:20}}})")
        h.page.wait_for_timeout(40);navigation(h);layout(h);close(h)
    test('Calm long session counts do not squeeze or overflow mobile navigation',large_history)
    def outputs_text():
        h=Harness(browser,width=320,height=950);tx20(h);h.page.locator('#output-review>summary').click();h.page.evaluate(ENLARGE);layout(h)
        assert h.page.locator('.output-address:visible').count()==20;close(h)
    test('Calm all 20 full addresses reflow at 320px with doubled text',outputs_text)
    def failed_download():
        h=Harness(browser);d=h.config();h.accept(d['tx']);before=same(h);h.page.evaluate('() => {URL.createObjectURL=()=>{throw Error("injected unavailable download") }}')
        h.page.get_by_role('button',name='Save result',exact=True).click();assert 'unavailable' in h.page.locator('.notice:visible').first.inner_text();assert same(h)==before;close(h)
    test('Calm failed evidence download is visible and leaves verified state unchanged',failed_download)
    def help_return():
        h=Harness(browser,width=390);nav(h,'advanced');before=same(h);h.page.get_by_role('link',name='Help',exact=True).click();h.page.get_by_role('link',name='Back to test',exact=True).click()
        assert same(h)==before;assert h.call('return a.workspaceView')=='advanced';assert h.page.locator('#advanced-title').is_visible();close(h)
    test('Calm Help return preserves the active workspace and its exact test',help_return)
    browser.close()
out={'suite':'Calm mobile/output/evidence browser integration','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results}
OUT.write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['suite','total_defined','passed','failed']},indent=2));sys.exit(1 if out['failed'] else 0)
