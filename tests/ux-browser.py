#!/usr/bin/env python3
"""Progressive disclosure, safety visibility, reflow and integrity regressions.
Exact HTML in offline Chromium; synthetic signatures/camera, not hardware acceptance.
"""
from pathlib import Path
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0],globals())

# Rectangle checks supplement screenshots: do not hide or merely crop overflow.
LAYOUT="""() => {
 const vw=document.documentElement.clientWidth;
 const shown=e=>e.checkVisibility({checkVisibilityCSS:true,checkOpacity:true})&&!e.closest('.sr-only,.skip,svg');
 const nodes=[...document.querySelectorAll('body *')].filter(e=>shown(e)&&!['SCRIPT','STYLE','TEMPLATE'].includes(e.tagName));
 const overflow=nodes.map(e=>{const r=e.getBoundingClientRect();return {id:e.id,tag:e.tagName,cls:String(e.className),left:r.left,right:r.right,width:r.width,scroll:e.scrollWidth}}).filter(r=>r.width&& (r.left < -2 || r.right > vw+2));
 const clipped=[];const root=document.getElementById('advanced-tools');
 for(const e of root.querySelectorAll('p,label,summary,button,.field-label')) {
  if(!shown(e))continue;const r=e.getBoundingClientRect();
  if(e.scrollWidth>e.clientWidth+2)clipped.push({id:e.id,tag:e.tagName,text:e.textContent.slice(0,45),width:e.clientWidth,scroll:e.scrollWidth});
 }
 return {width:vw,scroll:document.documentElement.scrollWidth,overflow,clipped};
}"""
ENLARGE="""() => {const es=[...document.querySelectorAll('body *')].filter(e=>!['SCRIPT','STYLE'].includes(e.tagName));const sizes=es.map(e=>getComputedStyle(e).fontSize);es.forEach((e,i)=>e.style.fontSize=(parseFloat(sizes[i])*2)+'px')}"""
TEXT_SPACE="""*{line-height:1.5!important;letter-spacing:.12em!important;word-spacing:.16em!important}p{margin-bottom:2em!important}"""

def close(h):
    assert not h.errors,h.errors
    assert not h.requests,h.requests
    h.close()

def layout(h):
    r=h.page.evaluate(LAYOUT)
    assert r['scroll']<=r['width']+2,r
    assert not r['overflow'],r
    assert not r['clipped'],r
    return r

def snapshot(h):
    return h.call('return JSON.stringify([a.stateSignature,a.psbtBase64,a.variants,a.walletSession,a.walletFingerprint,a.preparedRevision,a.sessionChecks,a.guidedStatus,a.resultState,a.completedAt,a.scan.phase])')

def planned(browser,count=2,width=1280):
    h=Harness(browser,width=width,height=950)
    h.open_tools();h.page.locator('#guided-setup>summary').click()
    h.page.locator('#session-count').fill(str(count));h.page.locator('#start-guided-session').click()
    assert h.call('return a.guidedStatus.phase')=='receiving'
    h.workspace('test')
    return h

def marker(psbt):
    pos=5
    while True:
        n,pos=readcompact(psbt,pos)
        if not n:break
        pos+=n;n,pos=readcompact(psbt,pos);pos+=n
    key=b'\xfc\x01x\x00';value=b'non-secret-ux-fixture'
    return psbt[:pos-1]+compact(len(key))+key+compact(len(value))+value+b'\x00'+psbt[pos:]

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    environment={'browser':browser.version,'origin':'about:blank/document.setContent; exact candidate','network':'offline','camera':'synthetic only','enlargement':'computed font doubling or CSS zoom, not native browser zoom; no WCAG certification'}
    def initial():
        h=Harness(browser,width=360);assert not h.page.locator('#advanced-tools').evaluate('(e)=>e.open')
        for selector in ['#session-count','#signing-policy','#device','#locktime']:
            assert not h.page.locator(selector).is_visible(),selector
        assert h.page.locator('#workspace-advanced').is_visible()
        assert not h.page.locator('.session-tracker').is_visible()
        assert h.page.locator('#wallet-loaded').is_visible()
        assert 'Never enter a real seed' in h.page.locator('.warning:visible').inner_text();assert 'send bitcoin to this wallet' in h.page.locator('.warning:visible').inner_text()
        assert 'hardware acceptance pending' in h.page.locator('.release-status a').get_attribute('aria-label');layout(h);close(h)
    test('UX default: optional tools closed and essential warning/action/discovery visible',initial)
    def normal():
        h=Harness(browser,width=360);h.page.locator('#wallet-loaded').click()
        assert h.call('return a.step')==2
        assert not h.page.locator('#advanced-tools').evaluate('(e)=>e.open')
        assert h.page.locator('#qr-format').is_visible()
        tx=h.call('return a.variants[0].txHex')
        h.page.get_by_role('button',name='Paste signed transaction',exact=True).click()
        h.page.locator('#artifact').fill(tx)
        h.page.get_by_role('button',name='Verify signatures',exact=True).click()
        assert h.call('return a.resultState')=='match'
        assert h.page.get_by_role('button',name='Save result',exact=True).is_visible()
        assert not h.page.locator('#advanced-tools').evaluate('(e)=>e.open')
        assert not h.page.locator('#result-tools').evaluate('(e)=>e.open')
        assert 'does not rule out seed leakage' in h.page.locator('.result-limit:visible').inner_text();assert 'this transaction only' in h.page.locator('.result-limit:visible').inner_text();close(h)
    test('UX ordinary three-step test completes without opening advanced controls (synthetic response)',normal)
    def keyboard():
        h=Harness(browser);h.workspace('advanced');h.page.locator('#advanced-tools>summary').click();summary=h.page.locator('#advanced-tools>summary');h.page.keyboard.press('Tab');summary.focus()
        assert summary.evaluate('(e)=>getComputedStyle(e).outlineStyle')!='none'
        h.page.keyboard.press('Enter');assert h.page.locator('#advanced-tools').evaluate('(e)=>e.open')
        h.page.keyboard.press('Space');assert not h.page.locator('#advanced-tools').evaluate('(e)=>e.open')
        for _ in range(12):
            h.page.keyboard.press('Tab')
            assert h.page.evaluate("!['session-count','signing-policy','locktime','device','firmware'].includes(document.activeElement.id)")
        close(h)
    test('UX native disclosure Enter/Space and closed controls excluded from keyboard order',keyboard)
    def unchanged():
        h=Harness(browser);h.config();before=snapshot(h)
        for _ in range(4):
            h.open_settings();h.page.locator('#transaction-editor>summary').click();h.page.locator('#advanced-tools>summary').click()
        assert snapshot(h)==before;close(h)
    test('UX opening/closing all configuration changes no authoritative test/result state',unchanged)
    def custom():
        h=Harness(browser);h.page.locator('#wallet-loaded').click();h.open_settings()
        h.page.locator('#signing-policy').select_option('plain');h.page.locator('#psbt-version').select_option('2')
        h.page.wait_for_function('('+APP+').transactionReady');h.page.locator('#advanced-tools>summary').click()
        assert h.page.locator('.active-settings').is_visible()
        text=h.page.locator('.active-settings').inner_text();assert 'RFC 6979 plain' in text and 'PSBT v2' in text
        before=snapshot(h);h.page.get_by_role('button',name='Review settings',exact=True).click()
        assert h.page.locator('#signing-policy').is_visible();h.page.wait_for_function('document.activeElement.parentElement.id==="transaction-editor"')
        assert snapshot(h)==before;close(h)
    test('UX nondefault policy/PSBT stays visible after collapse; review reveals without changing it',custom)
    def edited():
        h=Harness(browser);h.page.locator('#wallet-loaded').click();h.open_settings();h.page.locator('#locktime').fill('1234')
        h.page.wait_for_function('('+APP+').transactionReady');h.page.locator('#advanced-tools>summary').click()
        assert 'Edited transaction' in h.page.locator('.active-settings').inner_text();close(h)
    test('UX edited transaction cannot silently disappear behind collapsed settings',edited)
    def locked():
        h=planned(browser);h.page.locator('#wallet-loaded').click();before=snapshot(h)
        h.open_settings();assert h.page.locator('#locktime').is_disabled();assert h.page.locator('#signing-policy').is_disabled()
        h.page.locator('#advanced-tools>summary').click();assert snapshot(h)==before;h.workspace('test')
        assert h.page.locator('.guided-status').is_visible();close(h)
    test('UX guided transaction/policy lock survives disclosures and controls are disabled',locked)
    def invalid():
        h=Harness(browser);h.config();h.accept('unusable response')
        assert h.call('return a.resultState')=='incomplete';assert h.page.locator('.result').is_visible()
        assert not h.page.locator('#advanced-tools').evaluate('(e)=>e.open');assert 'Could not complete' in h.page.locator('.result-message').inner_text();close(h)
    test('UX malformed import displays incomplete result with advanced tools closed',invalid)
    def differ():
        h=Harness(browser);h.config();attack=(Path(__file__).parents[1]/'fixtures/bitcoin-before.js').read_text().split('var Vp = ')[-1] if False else None
        # Official published fixture already used by the retained independent tests.
        tx=(Path(__file__).parents[1]/'fixtures/crypto-vectors.json')
        # Obtain known-attack hex from the pinned legacy bundled fixture, not a hidden runtime signer.
        m=re.search(r'var Vp\s*=\s*[`\"]([0-9a-f]+)[`\"]',BASE)
        assert m;h.accept(m[1]);assert h.call('return a.resultState')=='mismatch'
        assert h.page.locator('.result-message').is_visible();assert 'Signatures differ' in h.page.locator('.result-message').inner_text()
        assert not h.page.locator('#advanced-tools').evaluate('(e)=>e.open');close(h)
    test('UX published valid-but-different signatures remain visible without advanced access',differ)
    def metadata():
        h=Harness(browser,width=360);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex())
        assert h.call('return a.resultState')=='match';assert h.call('return a.metadataSummary.status')=='unexpected'
        assert h.page.locator('.file-review-action').is_visible();assert not h.page.locator('#result-tools').evaluate('(e)=>e.open')
        assert not h.page.locator('#advanced-tools').evaluate('(e)=>e.open');layout(h);close(h)
    test('UX matching signatures never conceal unexpected metadata in the default view',metadata)
    def report():
        h=Harness(browser);d=h.config();h.accept(d['tx']);before=h.call('return a.report()');h.open_evidence()
        assert h.page.get_by_role('button',name='Save evidence',exact=True).is_visible()
        h.page.locator('#result-tools>summary').click();assert h.call('return a.report()')==before
        assert h.page.get_by_role('button',name='Save result',exact=True).is_visible();close(h)
    test('UX evidence disclosure preserves the immutable result and ordinary report action',report)
    def evidence_download():
        h=Harness(browser);d=h.config();h.accept(d['tx']);expected=h.call('return a.exportEvidence()');h.open_evidence()
        with h.page.expect_download() as event:h.page.get_by_role('button',name='Save evidence',exact=True).click()
        got=json.loads(Path(event.value.path()).read_text());assert got==expected
        assert d['seed'] not in json.dumps(got);close(h)
    test('UX explicit advanced evidence export equals current snapshot and excludes local seed',evidence_download)
    def terminal():
        h=planned(browser);h.page.locator('#wallet-loaded').click();h.accept('bad data')
        assert h.call('return a.guidedStatus.phase')=='halted'
        assert not h.page.locator('#advanced-tools').is_visible()
        assert h.page.locator('.guided-status').is_visible();assert h.page.locator('.guided-stop-reason').is_visible()
        h.page.locator('.guided-end>summary').click();assert h.page.locator('#end-guided-session').is_visible()
        h.page.locator('#end-guided-session').click();assert h.call('return a.guidedStatus.phase')=='ended';close(h)
    test('UX halted state and explicit End are reachable outside collapsed advanced tools',terminal)
    def complete():
        h=planned(browser);h.page.locator('#wallet-loaded').click();seed=h.call('return a.seed.value')
        for i in range(2):
            h.accept(h.call('return a.variants[0].txHex'))
            if not i:h.page.locator('#next-transaction').click()
        assert h.call('return a.guidedStatus.phase')=='complete';assert h.call('return a.guidedStatus.completed')==2
        assert h.call('return a.seed.value')==seed;assert h.page.locator('.guided-status').is_visible();close(h)
    test('UX guided two-case session completes with advanced panel closed (synthetic signatures)',complete)
    def interruption():
        h=planned(browser);h.page.locator('#wallet-loaded').click();before=h.call('return a.guidedStatus')
        h.call('a.pause()');h.page.evaluate('window.dispatchEvent(new PageTransitionEvent("pageshow",{persisted:true}))')
        assert not h.call('return a.scan.active');assert h.call('return a.guidedStatus')==before;close(h)
    test('UX page restoration cannot auto-advance or reacquire capture',interruption)
    def capture():
        h=Harness(browser,media=True);h.page.locator('#wallet-loaded').click();h.call('a.startScan()')
        h.page.wait_for_function('('+APP+').scan.phase==="scanning"');before=h.page.evaluate('mediaCalls')
        for _ in range(3):
            assert h.page.locator('#workspace-advanced').is_disabled();h.page.locator('#workspace-advanced').evaluate('(e)=>e.click()')
            h.call('a.openWorkspace("advanced")');assert h.call('return a.workspaceView')=='test'
        assert h.page.evaluate('mediaCalls')==before
        assert h.page.get_by_role('button',name='Stop camera',exact=True).is_visible()
        h.page.get_by_role('button',name='Stop camera',exact=True).click();assert not h.call('return a.scan.active');close(h)
    test('UX disclosures neither restart camera nor hide Stop while scanning',capture)
    def denied():
        h=planned(browser);h.page.locator('#wallet-loaded').click()
        h.page.evaluate('Object.defineProperty(navigator,"mediaDevices",{configurable:true,value:{getUserMedia:()=>Promise.reject(new DOMException("denied","NotAllowedError"))}})')
        h.call('a.scan.supported=true; a.startScan()');h.page.wait_for_function('('+APP+').scan.phase==="failed"')
        assert h.page.locator('[x-text="scan.error"]').is_visible();assert h.page.locator('.guided-status').is_visible();close(h)
    test('UX denied camera remains an explicit terminal session finding in beginner view',denied)
    def help_identity():
        h=Harness(browser);h.page.locator('.release-status a').click();box=h.page.locator('#release-status-help')
        assert box.evaluate('(e)=>e.open');t=box.inner_text();assert 'unsigned' in t and 'not the SHA-256 of the final HTML' in t
        assert h.call('return a.releaseVersion') in t
        assert len(h.page.locator('.source-identity').inner_text())==64;close(h)
    test('UX release status links to exact version and correctly limited source identity',help_identity)
    def links():
        h=Harness(browser)
        broken=h.page.evaluate('''() => [...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(a.getAttribute('href').slice(1))).map(a=>a.getAttribute('href'))''')
        assert not broken,broken;close(h)
    test('UX every internal Help/disclosure link resolves to one actual target',links)
    def notes():
        h=Harness(browser);h.open_tools();h.page.locator('#device-notes>summary').click()
        payload='<img src=x onerror="window.injected=true">';h.page.locator('#firmware').fill(payload)
        h.page.locator('#advanced-tools>summary').click();h.workspace('test');h.page.locator('#wallet-loaded').click();h.accept(h.call('return a.variants[0].txHex'))
        assert h.call('return a.report().firmware')==payload;assert not h.page.evaluate('window.injected===true');close(h)
    test('UX operator notes remain inert text, not markup or a certified device identity',notes)
    def limits():
        h=Harness(browser);h.open_tools();h.page.locator('#guided-setup>summary').click()
        before=snapshot(h)
        for bad in ['0','201','1.5','-1','']:
            h.page.locator('#session-count').fill(bad);h.page.locator('#start-guided-session').click()
            assert not h.call('return a.hasGuidedSession');assert snapshot(h)==before
        assert h.page.locator('.notice:visible').count()>0;close(h)
    test('UX invalid session counts fail without replacing the current manual transaction',limits)
    def narrow_container():
        h=Harness(browser);h.open_tools();h.page.locator('#guided-setup>summary').click()
        h.page.locator('#advanced-tools').evaluate('(e)=>e.style.width="260px"')
        r=h.page.evaluate(LAYOUT);assert not r['clipped'],r
        widths=h.page.locator('#guided-setup .guided-plan-controls').evaluate('(e)=>[e.clientWidth,e.scrollWidth]');assert widths[1]<=widths[0]+2,widths;close(h)
    test('UX planner respects its container width as well as viewport media breakpoints',narrow_container)
    def stale():
        h=Harness(browser);h.page.locator('#wallet-loaded').click();h.open_settings();h.page.locator('#locktime').fill('not-valid')
        h.page.locator('#advanced-tools>summary').click();h.workspace('test');h.page.wait_for_function('!!('+APP+').buildProblem')
        assert not h.page.locator('.sign-layout').is_visible();assert h.page.locator('[x-text="buildProblem"]:visible').count()>0;close(h)
    test('UX invalid hidden settings never expose stale signing QR or hide the build failure',stale)
    def returned_result():
        h=Harness(browser);d=h.config();h.accept(d['tx']);before=h.call('return JSON.stringify(a.report())')
        h.page.get_by_role('button',name='Review settings',exact=True).click()
        assert h.page.locator('#locktime').is_disabled();h.page.locator('#advanced-tools>summary').click()
        assert h.call('return JSON.stringify(a.report())')==before;close(h)
    test('UX reviewing a completed test leaves inputs locked and result immutable',returned_result)

    # Each width runs both experiences in all three steps, rather than only a screenshot of a closed box.
    for width in [320,360,390,438,768,1024,1440]:
        def responsive(w=width):
            h=Harness(browser,width=w,height=1000);layout(h);h.open_settings();h.page.locator('#guided-setup>summary').click();h.page.locator('#device-notes>summary').click();layout(h)
            h.page.locator('#session-count').fill('20');assert h.page.locator('#start-guided-session').is_enabled()
            if w in [360,1440]:h.page.locator('#advanced-tools').screenshot(path=str(SHOTS/f'advanced-{w}.png'))
            h.page.locator('#advanced-tools>summary').click();h.workspace('test');h.page.locator('#wallet-loaded').click();layout(h)
            h.accept(h.call('return a.variants[0].txHex'));layout(h);h.open_evidence();layout(h)
            if w in [360,1440]:h.page.screenshot(path=str(SHOTS/f'result-{w}.png'),full_page=True)
            close(h)
        test(f'UX all-step beginner/advanced layout and original planner controls at {width}px',responsive)
    for width in [320,438,768,1440]:
        def enlarged(w=width):
            h=Harness(browser,width=w,height=1100);h.open_settings();h.page.locator('#guided-setup>summary').click();h.page.locator('#device-notes>summary').click()
            h.page.evaluate(ENLARGE);layout(h)
            h.page.locator('#session-count').fill('50');assert h.page.locator('#session-count').input_value()=='50'
            h.page.get_by_role('group',name='Session length presets').get_by_role('button',name='100',exact=True).click();assert h.page.locator('#session-count').input_value()=='100'
            h.page.locator('#advanced-tools').screenshot(path=str(SHOTS/f'large-text-{w}.png'));close(h)
        test(f'UX 200-percent computed-text enlargement keeps full controls operable at {width}px',enlarged)
    for width in [320,438,1440]:
        def spacing(w=width):
            h=Harness(browser,width=w);h.open_settings();h.page.locator('#guided-setup>summary').click();h.page.add_style_tag(content=TEXT_SPACE);layout(h);close(h)
        test(f'UX increased line/letter/word/paragraph spacing reflows at {width}px',spacing)
    for width in [320,360,768,1440]:
        def halted(w=width):
            h=planned(browser,width=w);h.page.locator('#wallet-loaded').click();h.accept('wrong incomplete response')
            h.page.locator('.guided-end>summary').click();h.page.locator('#session-end-reason').fill('Device refused this request; preserve the evidence before retrying.')
            layout(h);assert h.page.locator('#end-guided-session').is_visible()
            if w==360:h.page.screenshot(path=str(SHOTS/'halted-360.png'),full_page=True)
            close(h)
        test(f'UX halted guided session and End action remain readable at {width}px',halted)
    def forced_colors():
        h=Harness(browser,width=360);h.page.emulate_media(forced_colors='active');h.open_tools()
        h.page.keyboard.press('Tab');h.page.locator('#advanced-tools>summary').focus();assert h.page.locator('#advanced-tools>summary').evaluate('(e)=>getComputedStyle(e).outlineStyle')!='none'
        layout(h);close(h)
    test('UX forced-color mode retains visible disclosure focus and border cues',forced_colors)
    def zoom():
        h=Harness(browser,width=1280,height=1000);h.page.evaluate('document.body.style.zoom="2"');h.open_settings();h.page.locator('#guided-setup>summary').click();layout(h);close(h)
    test('UX CSS 200-percent page-zoom simulation reflows planner without cropping (not native zoom)',zoom)
    def seed24():
        h=Harness(browser,width=320);h.page.get_by_role('button',name='24 words',exact=True).click();h.page.wait_for_function('('+APP+').seedQrVisible');layout(h)
        qr=h.page.locator('#seed-qr-display').bounding_box();fp=h.page.locator('.wallet-fingerprint').bounding_box();assert fp['y']>=qr['y']+qr['height'];close(h)
    test('UX 24-word wallet and matching fingerprint remain outside the QR quiet zone at 320px',seed24)
    for width in [320,1440]:
        def focused_result(w=width):
            h=Harness(browser,width=w,height=900);h.page.locator('#wallet-loaded').click();h.accept(h.call('return a.variants[0].txHex'))
            h.page.wait_for_timeout(180)
            h.call('a.focusCurrentSection()');h.page.wait_for_timeout(100)
            title=h.page.locator('[x-ref="resultTitle"]').bounding_box();tracker=h.page.locator('.session-tracker').bounding_box()
            assert title and tracker
            assert title['y']>=0
            if h.page.locator('.session-tracker').evaluate('(e)=>getComputedStyle(e).position')=='sticky':
                assert title['y']>=tracker['y']+tracker['height']-1,(title,tracker)
            h.page.screenshot(path=str(SHOTS/f'focused-result-{w}.png'))
            h.page.evaluate('window.scrollTo(0,0)');h.page.wait_for_timeout(50)
            if w==1440:h.page.screenshot(path=str(SHOTS/'result-unscrolled-1440.png'),full_page=True)
            close(h)
        test(f'UX focused result heading is not obscured by the live session tracker at {width}px',focused_result)
    def license_link():
        h=Harness(browser);h.page.locator('footer a[href="#license-help"]').click();box=h.page.locator('#license-help')
        assert box.evaluate('(e)=>e.open');assert 'Permission is hereby granted' in box.inner_text();assert 'MIT License' in box.inner_text();close(h)
    test('UX single-file footer license works offline through the exact embedded MIT notice',license_link)
    browser.close()

out={'suite':'UX/disclosure/reflow/failure-visibility regression','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'artifact':FILE.name,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results}
OUT.write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['suite','total_defined','passed','failed']},indent=2));sys.exit(1 if out['failed'] else 0)
