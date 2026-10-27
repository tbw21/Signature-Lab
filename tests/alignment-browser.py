#!/usr/bin/env python3
"""Real Chromium geometry / interactions on exact HTML; no real signer or optical acceptance."""
from pathlib import Path
exec((Path(__file__).parent/'ux-browser.py').read_text().split('\nwith sync_playwright() as pw:')[0],globals())

def state(h):
    return h.call('return JSON.stringify([a.seed,a.walletSession,a.walletFingerprint,a.stateSignature,a.psbtBase64,a.signingPolicy,a.preparedRevision,a.sessionChecks,a.completedAt])')

def box(h,selector):
    h.page.locator(selector).wait_for(state="visible")
    return h.page.locator(selector).evaluate('(e)=>{const r=e.getBoundingClientRect();return {left:r.left,right:r.right,top:r.top,bottom:r.bottom,width:r.width,height:r.height}}')

def trailing(h,selector,container):
    child,parent=box(h,selector),box(h,container)
    assert abs(child['right']-parent['right'])<2,(selector,child,parent)

def seed_geometry(h):
    # RC32 approved two-column wallet: words, SeedQR, and a separate fingerprint card.
    # Preserve full-word visibility and the SeedQR quiet zone in both enlargement states.
    words=box(h,'.seed-grid');word_card=box(h,'.premium-words-card')
    assert words['left']>=word_card['left']-1 and words['right']<=word_card['right']+1
    assert h.page.locator('.seed-grid li:visible').count()==int(h.call('return a.wordCount'))
    assert h.page.locator('.premium-words-card h3').is_visible()
    assert h.page.locator('#wallet-fingerprint-value').is_visible()
    note=h.page.locator('#wallet-compare-hint')
    assert 'Compare this fingerprint' in note.inner_text()
    assert note.locator('xpath=ancestor::section[@id="wallet-load-card"]').count()==1
    action=box(h,'.seed-qr-actions>button');qr=box(h,'#seed-qr-display')
    assert h.page.locator('.seed-qr-actions>button').count()==1
    assert h.page.locator('[x-ref="seedQrCanvas"]').count()==1
    assert action['top']>=qr['bottom']-1,(action,qr)
    assert qr['width']>180,qr
    assert not h.page.locator('.seed-qr-actions>button').evaluate('(e)=>!!e.closest(".qr-frame")')
    assert h.page.locator('#wallet-loaded').is_visible()
    layout(h)

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    environment={'browser':browser.version,'origin':'exact HTML via offline setContent','physicalSigner':False,'realOpticalScan':False,'scope':'alignment, unchanged state and source regressions'}
    for width in [320,360,390,438,768,1024,1440]:
        def nav(w=width):
            h=Harness(browser,width=w,height=950);before=state(h)
            for view in ['test','advanced','session','test']:
                h.workspace(view)
                assert h.page.locator('nav.workspace-nav,#workspace-test,#workspace-advanced,#workspace-session').count()==0
                settings=box(h,'#tbw-settings > summary')
                assert settings['width']>=44 and settings['height']>=44,settings
                if view!='test':
                    back=h.page.locator('#'+view+'-view').get_by_role('button',name='Back to test').first
                    back.wait_for(state='visible')
                    assert back.is_visible() and back.bounding_box()['height']>=44
                layout(h);assert state(h)==before
            close(h)
        test(f'Alignment workspace and Back actions remain at right edge in every view at {width}px',nav)
    for width in [320,390,768,1440]:
        for words in [12,24]:
            def seed(w=width,n=words):
                h=Harness(browser,width=w,height=1100);h.workspace('test')
                if n==24:h.page.get_by_role('button',name='24 words',exact=True).click()
                h.page.wait_for_function('('+APP+').seedQrVisible && !!('+APP+').walletFingerprint')
                before=state(h);image=h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(c)=>c.toDataURL()')
                text=read_qr(Image.open(io.BytesIO(base64.b64decode(image.split(',')[1]))))[0].data
                assert len(text)==4*n,(n,text)
                seed_geometry(h)
                if w in [390,1440] and n==12:h.page.screenshot(path=str(SHOTS/f'alignment-wallet-{w}.png'),full_page=True)
                h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(40)
                seed_geometry(h);assert state(h)==before
                enlarged=h.page.locator('[x-ref="seedQrCanvas"]').evaluate('(c)=>c.toDataURL()')
                assert image==enlarged,'Rendering pixels must not change when only the CSS size changes'
                if w in [390,1440] and n==12:h.page.screenshot(path=str(SHOTS/f'alignment-enlarged-{w}.png'),full_page=True)
                h.page.get_by_role('button',name='Reduce QR',exact=True).click();h.page.wait_for_timeout(40)
                seed_geometry(h);assert state(h)==before;close(h)
            test(f'Alignment {words} words, instructions, QR pixels and enlarged/reduced state at {width}px',seed)
    for width in [320,768,1440]:
        def text(w=width):
            h=Harness(browser,width=w,height=1000);h.workspace('test');h.page.evaluate(ENLARGE)
            for n in [12,24]:
                if n==24:h.page.get_by_role('button',name='24 words',exact=True).click()
                for expanded in [False,True]:
                    h.call('a.seedQrExpanded=arg',expanded);h.page.wait_for_timeout(50);seed_geometry(h)
                h.call('a.seedQrExpanded=false')
            for view in ['advanced','session','test']:
                h.workspace(view);layout(h);assert box(h,'#tbw-settings > summary')['height']>=44
            close(h)
        test(f'Alignment reflows at doubled text size, 12/24 words and both QR sizes at {width}px',text)
    def spacing():
        h=Harness(browser,width=390,height=1000);h.workspace('test');h.page.add_style_tag(content=TEXT_SPACE)
        seed_geometry(h);h.page.get_by_role('button',name='Enlarge QR',exact=True).click();h.page.wait_for_timeout(40);seed_geometry(h);close(h)
    test('Alignment increased text spacing preserves instructions and trailing control',spacing)
    for width in [390,1440]:
        def actions(w=width):
            h=Harness(browser,width=w,height=1000);h.workspace('test');h.page.locator('#wallet-loaded').click()
            for group in ['.psbt-actions']:
                assert h.page.locator(group).evaluate('(e)=>getComputedStyle(e).justifyContent')=='flex-end'
                children=h.page.locator(group+' > :is(button,label)')
                children.last.wait_for(state='visible');right=children.last.evaluate('(e)=>e.getBoundingClientRect().right')
                assert abs(right-box(h,group)['right'])<2,(group,right,box(h,group))
            h.config();h.accept(h.call('return a.variants[0].txHex'));before=state(h)
            trailing(h,'.result-actions>button[aria-describedby="save-result-help"]','.result-actions')
            h.open_evidence()
            for name in ['Save evidence','Save summary only']:
                button=h.page.get_by_role('button',name=name,exact=True)
                parent=button.locator('..');b=button.bounding_box();p=parent.bounding_box()
                assert abs(b['x']+b['width']-p['x']-p['width'])<2,(name,b,p)
            assert before==state(h);layout(h);close(h)
        test(f'Alignment transaction/import/export action rows end at the right edge at {width}px',actions)
    def keyboard():
        h=Harness(browser,width=390);h.workspace('test');before=state(h)
        button=h.page.get_by_role('button',name='Enlarge QR',exact=True);button.focus()
        h.page.keyboard.press('Shift+Tab');h.page.keyboard.press('Tab')
        assert h.page.evaluate('document.activeElement===document.querySelector("[x-ref=seedQrToggle]")')
        assert button.evaluate('(e)=>getComputedStyle(e).outlineStyle')!='none'
        h.page.keyboard.press('Enter');h.page.wait_for_timeout(40)
        assert h.page.get_by_role('button',name='Reduce QR',exact=True).get_attribute('aria-expanded')=='true'
        h.page.keyboard.press('Space');h.page.wait_for_timeout(40);assert before==state(h)
        assert h.page.locator('[x-ref="seedQrCanvas"]').count()==1
        close(h)
    test('Alignment Enlarge/Reduce keyboard operation preserves data and unique canvas binding',keyboard)
    browser.close()
OUT.write_text(json.dumps({'suite':'Alignment layout and interaction regressions','artifact':FILE.name,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,'complete':True,'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results},indent=2))
print(json.dumps({'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results)}))
sys.exit(bool(sum(x['status']=='failed' for x in results)))
