#!/usr/bin/env python3
"""Exact-HTML regression for bounded capture and accurately scoped file findings.
Generated signatures and synthetic canvas cameras only, never physical signer acceptance.
"""
from pathlib import Path
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0],globals())
from bytewords_oracle import frames as urframes, corrupt_frame

def maps(raw):
    assert raw[:5]==b'psbt\xff';pos=5;out=[]
    while pos<len(raw):
        m=[]
        while True:
            n,pos=readcompact(raw,pos)
            if not n:break
            key=raw[pos:pos+n];pos+=n;n,pos=readcompact(raw,pos);value=raw[pos:pos+n];pos+=n
            m.append((key,value))
        out.append(m)
    return out

def assemble(ms):
    return b'psbt\xff'+b''.join(b''.join(compact(len(k))+k+compact(len(v))+v for k,v in m)+b'\0' for m in ms)

def reduced(raw):
    ms=maps(raw);g=dict(ms[0]);ninputs=readcompact(g[b'\x04'],0)[0] if b'\x04' in g else readcompact(g[b'\x00'],4)[0]
    for i in range(1,len(ms)):
        allowed=[2,14,15,16] if i<=ninputs else [3,4]
        ms[i]=[(k,v) for k,v in ms[i] if k[0] in allowed]
    return assemble(ms)

def marker(raw):
    ms=maps(raw);ms[0].append((b'\xfc\x01x\x00',b'investigation-fixture'));return assemble(ms)

def stop_if_errors(h):
    assert not h.errors,h.errors;assert not h.requests,h.requests;h.close()

def observe(h,text):
    h.call('a.onScanHit({text:arg,binary:new Uint8Array(0)}); return true;',text)

def start(h):
    h.call('a.startScan();return true;');h.page.wait_for_function(APP+'.scan.phase==="scanning"')

def draw(h,uri):
    h.page.evaluate('''async uri=>{const im=new Image();im.src=uri;await im.decode();const c=testSource.getContext('2d');c.fillStyle='white';c.fillRect(0,0,700,700);c.imageSmoothingEnabled=false;c.drawImage(im,20,20,660,660);}''',uri)

def blank(h):
    h.page.evaluate("testSource.getContext('2d').fillStyle='white';testSource.getContext('2d').fillRect(0,0,700,700)")

def fit(h):
    assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+2')
    assert h.page.evaluate('''() => {const els=[...document.querySelectorAll('.result h3,.metadata-assessment p,.metadata-assessment summary,.scan-frame-note,.scan-diagnostics-actions')];return els.filter(e=>e.checkVisibility({checkVisibilityCSS:true})).every(e=>{const r=e.getBoundingClientRect();return r.left>=-2&&r.right<=innerWidth+2&&e.scrollWidth<=e.clientWidth+2})}''')

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    def retryable_observation():
        h=Harness(browser,media=True);d=h.config();f=urframes(bytes.fromhex(d['tx']));start(h);observe(h,corrupt_frame(f[0]));assert h.call('return a.scan.active');assert h.call('return a.scan.diagnostics.rejectedFrames')==1
        h.page.locator('.scan-frame-note').wait_for(state='visible');assert not h.call('return a.isTestComplete');assert not h.call('return a.scan.error');assert 'not used' in h.page.locator('.scan-frame-note').inner_text();stop_if_errors(h)
    test('one rejected observation remains visible as acquisition progress, not a firmware failure',retryable_observation)
    def success_after_reject():
        h=Harness(browser,media=True);d=h.config();f=urframes(bytes.fromhex(d['tx']));start(h);observe(h,corrupt_frame(f[0]));
        for frame in reversed(f):observe(h,frame)
        h.page.wait_for_function(APP+'.isTestComplete');assert h.call('return a.resultState')=='match';assert h.call('return a.report().transport.rejectedFrames')==1;assert h.call('return a.exportEvidence().submission.transport.rejectedFrames')==1;assert h.call('return a.completedScanNote');assert h.page.evaluate('testStreams.every(s=>s.getTracks().every(t=>t.readyState==="ended"))');stop_if_errors(h)
    test('valid response after rejected observation records count and releases capture',success_after_reject)
    def limit():
        h=Harness(browser,media=True);d=h.config();f=urframes(bytes.fromhex(d['tx']));start(h)
        for i in range(8):observe(h,corrupt_frame(f[0]))
        assert h.call('return a.scan.code')=='UR_CAPTURE_LIMIT';assert h.call('return a.scan.phase')=='failed';assert not h.call('return a.scan.active');assert not h.call('return a.isTestComplete');assert h.call('return a.sessionSummary.checked')==0
        h.page.locator('[x-show="scan.error"]').wait_for(state='visible');assert h.call('return a.scan.diagnostics.rejectedFrames')==8
        stop_if_errors(h)
    test('eighth rejected camera observation visibly stops with no result or progress credit',limit)
    def diagnostics_download():
        h=Harness(browser,media=True);d=h.config();f=urframes(bytes.fromhex(d['tx']));start(h);bad=corrupt_frame(f[0]);observe(h,bad)
        with h.page.expect_download() as info:h.page.get_by_role('button',name='Save scan diagnostics',exact=True).click()
        data=json.loads(Path(info.value.path()).read_text());assert data['schema']=='tbw-scan-diagnostics-v1';assert data['build']['version']==h.call('return a.releaseVersion');assert data['transport']['rejectedFrames']==1
        assert d['seed'] not in json.dumps(data);assert bad not in json.dumps(data);assert not data['signatureTestCompleted'];stop_if_errors(h)
    test('diagnostics download contains build/count/hash without raw QR or seed',diagnostics_download)
    def diagnostics_failure():
        h=Harness(browser,media=True);d=h.config();f=urframes(bytes.fromhex(d['tx']));start(h);observe(h,corrupt_frame(f[0]));before=h.call('return JSON.stringify(a.scan.diagnostics)');h.page.evaluate('() => {URL.createObjectURL=()=>{throw Error("injected unavailable download")};return true}');h.call('a.downloadScanDiagnostics()');assert 'unavailable' in h.call('return a.notice');assert h.call('return JSON.stringify(a.scan.diagnostics)')==before;assert h.call('return a.scan.active');stop_if_errors(h)
    test('diagnostic-export failure cannot mutate scan or manufacture a result',diagnostics_failure)
    def explicit_restart():
        h=Harness(browser,media=True);d=h.config();f=urframes(bytes.fromhex(d['tx']));start(h)
        for i in range(8):observe(h,corrupt_frame(f[0]))
        for frame in f:observe(h,frame)
        assert not h.call('return a.isTestComplete');assert h.page.evaluate('mediaCalls')==1
        start(h)
        for frame in f:observe(h,frame)
        assert h.call('return a.resultState')=='match';assert h.call('return a.report().transport.rejectedFrames')==0;assert h.page.evaluate('mediaCalls')==2;stop_if_errors(h)
    test('individual scan only recovers after explicit restart, preserving same unsigned transaction',explicit_restart)
    def bad_paste():
        h=Harness(browser);d=h.config();f=urframes(bytes.fromhex(d['tx']));r=h.accept('\n'.join([corrupt_frame(f[0]),*f]));assert r['state']=='incomplete';assert r['checked']==0;assert h.call('return a.resultDisplayState')=='incomplete';stop_if_errors(h)
    test('pasted damaged sequence is strictly incomplete even when all valid frames follow',bad_paste)
    def bad_file():
        h=Harness(browser);d=h.config();f=urframes(bytes.fromhex(d['tx']));payload='\n'.join([*f,corrupt_frame(f[0])]).encode();h.page.locator('input[type=file]').first.set_input_files({'name':'signed-qr.txt','mimeType':'text/plain','buffer':payload});h.page.wait_for_function(APP+'.resultState==="incomplete"');assert h.call('return a.sessionSummary.checked')==0;stop_if_errors(h)
    test('file import never ignores corrupt trailing data',bad_file)
    def actual_pixels():
        h=Harness(browser,media=True);d=h.config();f=urframes(bytes.fromhex(d['tx']),fragment_size=130);start(h);bad=corrupt_frame(f[0]);uri=png_uri(bad)
        # Independently recover QR pixel text before feeding synthetic canvas capture.
        im=Image.open(io.BytesIO(base64.b64decode(uri.split(',')[1])));assert read_qr(im)[0].data.decode()==bad
        draw(h,uri);h.page.wait_for_function(APP+'.scan.diagnostics?.rejectedFrames>=1',timeout=10000);blank(h);assert h.call('return a.scan.active')
        for frame in f:
            draw(h,png_uri(frame));h.page.wait_for_timeout(360)
        h.page.wait_for_function(APP+'.isTestComplete',timeout=10000);assert h.call('return a.resultState')=='match';assert h.call('return a.report().transport.rejectedFrames')>=1
        h.page.screenshot(path=str(SHOTS/'camera-recovered-1440.png'),full_page=True);stop_if_errors(h)
    test('independent Bytewords and QR pixels pass through synthetic camera after a damaged frame',actual_pixels)
    def reduced_metadata():
        h=Harness(browser);d=h.config();p=reduced(sign_psbt(d['psbt'],d['tx']));assert h.accept(p.hex())['state']=='match';h.file_details();assert h.page.locator('.metadata-summary').inner_text()=='Reduced signing response';assert h.call('return a.metadataSummary.supportingFieldsRemoved')==5;assert h.call('return a.resultDisplayState')=='match';assert not h.page.locator('.metadata-assessment summary').is_visible();assert h.call('return a.report().overallStatus')=='match';stop_if_errors(h)
    test('fully reduced signature-only response is explained neutrally, not a metadata alarm',reduced_metadata)
    def ordinary_metadata():
        h=Harness(browser);d=h.config();h.accept(sign_psbt(d['psbt'],d['tx']).hex());h.file_details();assert h.page.locator('.metadata-summary').inner_text()=='Only expected signing changes';assert h.page.locator('.result').get_attribute('data-result-state')=='match';stop_if_errors(h)
    test('ordinary signer fields do not produce file warning',ordinary_metadata)
    def primary_amber():
        h=Harness(browser);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());assert h.call('return a.resultState')=='match';assert h.call('return a.resultDisplayState')=='review';box=h.page.locator('.result');assert box.get_attribute('data-result-state')=='review';assert box.locator('h3').inner_text()=='Signatures matched. File changes need review.';assert h.call('return a.report().overallStatus')=='review';assert h.page.locator('.file-review-action').is_visible();assert not h.page.locator('#result-tools').evaluate('(e)=>e.open');assert h.page.locator('.file-review-action').is_visible();h.file_details();assert h.page.locator('.metadata-assessment').is_visible();stop_if_errors(h)
    test('unexplained fields override overall green appearance without changing valid signature finding',primary_amber)
    def change_detail():
        h=Harness(browser);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());h.page.get_by_role('button',name='Inspect file changes',exact=True).click();h.page.wait_for_function('document.activeElement===document.querySelector("#returned-file-details>summary")');details=h.page.locator('.metadata-assessment summary');details.focus();h.page.keyboard.press('Enter');assert 'Application-specific field' in h.page.locator('.metadata-assessment').inner_text();assert 'Technical key:' in h.page.locator('.metadata-assessment').inner_text();stop_if_errors(h)
    test('unexpected file details expose plain-English field, reason and technical key by keyboard',change_detail)
    def report_amber():
        h=Harness(browser);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex())
        with h.page.expect_download() as info:h.summary_download().click()
        r=json.loads(Path(info.value.path()).read_text());assert r['overallStatus']=='review';assert r['result']=='match';assert r['metadata']['status']=='unexpected';assert r==h.call('return a.report()');stop_if_errors(h)
    test('downloaded report preserves the same overall review classification as the UI',report_amber)
    def guided_expected():
        h=Harness(browser);h.config();h.call('a.sessionCount="3";a.startGuidedSession()');assert h.call('return a.guidedLocked');d=h.call('return {psbt:a.psbtBase64,tx:a.variants[0].txHex}');h.accept(reduced(sign_psbt(d['psbt'],d['tx'])).hex());assert h.call('return a.guidedStatus.phase')=='ready';assert h.call('return a.report().metadata.reducedResponse');stop_if_errors(h)
    test('documented reduced response allows guided continuation after actual verifier success',guided_expected)
    def guided_warning():
        h=Harness(browser);h.config();h.call('a.sessionCount="3";a.startGuidedSession()');d=h.call('return {psbt:a.psbtBase64,tx:a.variants[0].txHex}');h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());assert h.call('return a.guidedStatus.phase')=='halted';old=h.call('return a.testNumber');h.call('a.advanceGuidedSession()');assert h.call('return a.testNumber')==old;stop_if_errors(h)
    test('genuinely unexplained returned fields still halt guided advancement',guided_warning)
    def guided_noise():
        h=Harness(browser,media=True);h.config();h.call('a.sessionCount="3";a.startGuidedSession()');d=h.call('return {tx:a.variants[0].txHex}');f=urframes(bytes.fromhex(d['tx']));start(h);observe(h,corrupt_frame(f[0]));assert h.call('return a.guidedStatus.phase')=='receiving'
        for i in range(7):observe(h,corrupt_frame(f[0]))
        assert h.call('return a.guidedStatus.phase')=='halted';assert h.call('return a.guidedLocked');assert h.call('return a.scan.code')=='UR_CAPTURE_LIMIT';stop_if_errors(h)
    test('bounded acquisition is not a session failure until the terminal limit is reached',guided_noise)
    for width in [320,360,438,1440]:
        for outcome in ['reduced','review']:
            def layout(w=width,which=outcome):
                h=Harness(browser,width=w,height=1000);d=h.config();p=sign_psbt(d['psbt'],d['tx']);p=reduced(p) if which=='reduced' else marker(p);h.accept(p.hex());h.page.locator('.result h3').scroll_into_view_if_needed();fit(h)
                if which=='review':h.file_details();h.page.locator('.metadata-assessment summary').click();fit(h)
                h.page.screenshot(path=str(SHOTS/f'{which}-{w}.png'),full_page=True);stop_if_errors(h)
            test(f'{outcome} result including scope and file details fits {width}px',layout)
    def enlarged():
        h=Harness(browser,width=360,height=1000);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());h.page.add_style_tag(content='.result,.result h3,.result p,.metadata-assessment summary{font-size:200%!important}');fit(h);stop_if_errors(h)
    test('overall review wording reflows under enlarged result text',enlarged)
    for width in [320,1440]:
        def focused_review(w=width):
            h=Harness(browser,width=w,height=1000);d=h.config();h.accept(marker(sign_psbt(d['psbt'],d['tx'])).hex());h.page.wait_for_timeout(180);h.call('a.focusCurrentSection()');h.page.wait_for_timeout(100)
            title=h.page.locator('[x-ref="resultTitle"]').bounding_box();tracker=h.page.locator('.session-tracker').bounding_box();heading=h.page.locator('.result h3').bounding_box()
            assert title and tracker and heading;assert title['y']>=0
            if h.page.locator('.session-tracker').evaluate('(e)=>getComputedStyle(e).position')=='sticky':
                assert title['y']>=tracker['y']+tracker['height']-1,(title,tracker)
                assert heading['y']>=tracker['y']+tracker['height']-1,(heading,tracker)
            assert heading['y']+heading['height']<=1000,heading;fit(h)
            h.page.screenshot(path=str(SHOTS/f'review-focused-{w}.png'));h.page.evaluate('window.scrollTo(0,0)');h.page.wait_for_timeout(50)
            if w==1440:h.page.screenshot(path=str(SHOTS/'review-unscrolled-1440.png'),full_page=True)
            stop_if_errors(h)
        test(f'overall review headline stays visible below the taller sticky finding tracker at {width}px',focused_review)
    browser.close()
out={'suite':'QR and file-scope remediation browser integration','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'artifact':FILE.name,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results}
OUT.write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['suite','passed','failed']}));sys.exit(1 if out['failed'] else 0)
