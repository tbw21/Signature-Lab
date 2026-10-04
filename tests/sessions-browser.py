#!/usr/bin/env python3
"""Exact shipped HTML: guided physical-session simulations and independent fingerprints.
All signed responses below are synthetic fixtures. No physical device is claimed.
"""
from pathlib import Path
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0],globals())
import hmac,unicodedata
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
VECTORS=json.loads((Path(__file__).parents[1]/'fixtures/fingerprint-vectors.json').read_text())
def fingerprint(words):
    seed=hashlib.pbkdf2_hmac('sha512',unicodedata.normalize('NFKD',words).encode(),b'mnemonic',2048,64)
    master=hmac.new(b'Bitcoin seed',seed,hashlib.sha512).digest()
    public=ec.derive_private_key(int.from_bytes(master[:32],'big'),ec.SECP256K1()).public_key().public_bytes(serialization.Encoding.X962,serialization.PublicFormat.CompressedPoint)
    return hashlib.new('ripemd160',hashlib.sha256(public).digest()).digest()[:4].hex().upper()
def close(h):
    assert not h.errors,h.errors
    assert not h.requests,h.requests
    h.close()
def planned(browser,count=2,width=1280):
    h=Harness(browser,width=width,height=1000)
    h.open_tools();h.page.locator('#guided-setup summary').click();h.page.locator('#session-count').fill(str(count));h.page.locator('#start-guided-session').click()
    assert h.call('return a.guidedStatus.phase')=='receiving',h.call('return a.notice')
    h.page.locator('#wallet-loaded').click()
    return h

def add_marker(psbt):
    pos=5
    while True:
        n,pos=readcompact(psbt,pos)
        if not n:break
        pos+=n;n,pos=readcompact(psbt,pos);pos+=n
    key=b'\xfc\x01x\x00';value=b'public-simulation-marker'
    return psbt[:pos-1]+compact(len(key))+key+compact(len(value))+value+b'\x00'+psbt[pos:]

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    for vector in VECTORS:
        def vector_check(v=vector):
            h=Harness(browser);h.config();h.call('a.seed.value=arg;a.wordCount=String(arg.split(" ").length);a.recompute();a.goToStep(1)',v['mnemonic'])
            h.page.wait_for_function('('+APP+').seedQrVisible')
            expected=fingerprint(v['mnemonic']);assert expected==v['fingerprint']
            assert h.page.locator('#wallet-fingerprint-value').inner_text()==expected
            # Decode the actual rendered pixels independently with ZBar.
            png=h.page.locator('[x-ref="seedQrCanvas"]').screenshot();decoded=read_qr(Image.open(io.BytesIO(png)))
            assert len(decoded)==1
            data=decoded[0].data.decode();assert len(data)==4*len(v['mnemonic'].split())
            words=(Path(__file__).parents[1]/'src/07-wordlist.js').read_text().split('`')[1].split('\n')
            reconstructed=' '.join(words[int(data[i:i+4])] for i in range(0,len(data),4))
            assert reconstructed==v['mnemonic'];assert fingerprint(reconstructed)==expected
            close(h)
        test('C1 actual SeedQR pixels and independent BIP32 fingerprint: '+vector['name'],vector_check)
    def stable_fp():
        h=Harness(browser);original=h.call('return [a.seed.value,a.walletFingerprint]');h.call('a.randomizeTransaction("small");a.recompute()');assert h.call('return [a.seed.value,a.walletFingerprint]')==original
        h.call('a.selectSeedLength(24)');h.page.wait_for_function('('+APP+').seedQrVisible');assert h.call('return a.walletFingerprint')==fingerprint(h.call('return a.seed.value'));assert len(h.call('return a.seed.value').split())==24
        h.call('a.seed.value="invalid";a.recompute()');assert h.call('return a.walletFingerprint')==''
        close(h)
    test('C1 wallet changes update fingerprint; transactions retain it; invalid words hide it',stable_fp)
    def destroy_fp():
        h=Harness(browser);h.call('a.destroy()');assert h.call('return a.walletFingerprint')=='';assert not h.call('return a.seedQrVisible');h.close()
    test('C1 destroyed wallet has no stale displayed fingerprint',destroy_fp)
    for count in [20,50,100]:
        def preset(n=count):
            h=Harness(browser);h.open_tools();h.page.locator('#guided-setup summary').click();h.page.get_by_role('group',name='Session length presets').get_by_role('button',name=str(n),exact=True).click()
            h.page.locator('#start-guided-session').click();assert h.call('return a.exportSessionReport().plan.cases.length')==n;assert h.call('return a.guidedStatus.completed')==0;assert not h.call('return a.scan.active');close(h)
        test(f'C2 {count}-case preset plans without producing device results',preset)
    def invalid_count():
        h=Harness(browser);before=h.call('return [a.psbtBase64,a.stateSignature,a.walletSession]');h.call('a.sessionCount="201";a.startGuidedSession()');assert h.call('return [a.psbtBase64,a.stateSignature,a.walletSession]')==before;assert not h.call('return a.hasGuidedSession');close(h)
    test('C2 invalid plan count leaves the manual test unchanged',invalid_count)
    def full_session():
        h=planned(browser,3);plan=h.call('return a.exportSessionReport().plan');seed=h.call('return a.seed.value');fp=h.call('return a.walletFingerprint')
        for number in range(1,4):
            assert h.call('return a.guidedStatus.current')==number;assert not h.call('return a.scan.active')
            tx=h.call('return a.variants[0].txHex');p=h.call('return a.psbtBase64')
            # Exercise both PSBT and raw, using test references only.
            h.accept(sign_psbt(p,tx).hex() if number%2 else tx)
            assert h.call('return a.resultState')=='match';assert h.call('return a.guidedStatus.completed')==number
            assert h.call('return a.report().physicalSession.caseNumber')==number
            assert h.call('return a.walletFingerprint')==fp
            assert h.call('return a.exportEvidence().report.result')=='match'
            if number<3:h.page.locator('#next-transaction').click()
        report=h.call('return a.exportSessionReport()');assert report['status']['phase']=='complete';assert report['status']['notCompleted']==0
        assert report['plan']==plan;assert seed not in json.dumps(report);assert report['deviceOrigin']=='not-attested'
        h.session_controls();h.page.locator('.guided-end summary').click();h.page.locator('#end-guided-session').click();assert h.call('return a.guidedStatus.phase')=='ended'
        close(h)
    test('C3 three-case physical workflow simulation uses explicit Next and one verifier',full_session)
    def duplicate_next():
        h=planned(browser);before=h.call('return [a.psbtBase64,a.guidedStatus.planId]');h.call('a.advanceGuidedSession();a.startGuidedSession()');assert h.call('return [a.psbtBase64,a.guidedStatus.planId]')==before
        tx=h.call('return a.variants[0].txHex');h.accept(tx);h.call('a.verify();a.acceptArtifact(arg)',tx);assert h.call('return a.guidedStatus.completed')==1
        h.call('a.advanceGuidedSession()');before=h.call('return [a.psbtBase64,a.testNumber]');h.call('a.advanceGuidedSession()');assert h.call('return [a.psbtBase64,a.testNumber]')==before;close(h)
    test('C7 repeated Start/Next/response cannot skip or double count a case',duplicate_next)
    def old_response():
        h=planned(browser);tx=h.call('return a.variants[0].txHex');h.accept(tx);h.call('a.advanceGuidedSession()');h.accept(tx)
        assert h.call('return a.guidedStatus.phase')=='halted';assert h.call('return a.resultState')=='incomplete'
        assert h.page.locator('#next-transaction').is_disabled();assert h.page.get_by_role('button',name='Correct imported data').count()==0
        assert 'end this session before another attempt' in h.page.locator('.result .result-limit:visible').inner_text().lower()
        result=h.call('return a.report()');h.call('a.acceptArtifact(a.variants[0].txHex);a.advanceGuidedSession()');assert h.call('return a.report()')==result
        assert h.call('return a.guidedStatus.completed')==1;assert h.call('return a.guidedStatus.incomplete')==1
        h.call('a.endGuidedSession()');saved=h.call('return a.exportSessionReport()');h.accept(h.call('return a.variants[0].txHex'));assert h.call('return a.resultState')=='match';assert h.call('return a.exportSessionReport()')==saved;close(h)
    test('C4 earlier-case return halts, preserves evidence, and requires explicit End',old_response)
    def metadata():
        h=planned(browser);tx=h.call('return a.variants[0].txHex');p=h.call('return a.psbtBase64');h.accept(add_marker(sign_psbt(p,tx)).hex())
        assert h.call('return a.resultState')=='match';assert h.call('return a.guidedStatus.phase')=='halted';assert h.call('return a.guidedStatus.metadataWarnings')==1
        assert h.page.locator('.metadata-assessment').get_attribute('data-metadata-status')=='unexpected';assert h.page.locator('#next-transaction').is_disabled();close(h)
    test('C4 valid signatures with unexpected metadata stop planned advancement',metadata)
    def controls():
        h=planned(browser);old=h.call('return a.stateSignature');h.call('a.randomizeAll();a.selectSeedLength(24);a.setSigningPolicy("plain");a.generateRandomInputs();a.generateRandomOutputs()');assert h.call('return a.stateSignature')==old
        # The step's x-show update is scheduled for a render frame. A synchronous role
        # count can observe the prior hidden step immediately after wallet acknowledgement.
        # Wait for the original control; never retry signing or mutate application state.
        from playwright.sync_api import expect
        next_control=h.page.locator('.transaction-toolbar').get_by_role('button',name='Next planned transaction',exact=True)
        expect(next_control).to_have_count(1,timeout=6000)
        expect(next_control).to_be_visible(timeout=6000)
        expect(next_control).to_be_disabled(timeout=6000)
        assert h.call('return a.stateSignature')==old
        h.open_settings();assert h.page.locator('#locktime').is_disabled();assert h.page.locator('#psbt-version').is_disabled();close(h)
    test('C7 device wallet, policy and editing controls cannot replace an active plan',controls)
    def tamper():
        h=planned(browser);h.call('a.testNumber=77;a.recompute()');assert h.call('return a.guidedStatus.phase')=='halted';assert not h.call('return a.psbtQrAvailable');close(h)
    test('C7 out-of-band current-case number tampering halts the session',tamper)
    def late_file():
        h=planned(browser);tx=h.call('return a.variants[0].txHex');h.page.evaluate('window.releaseFile=null');h.call('a.loadFile({size:100,arrayBuffer:()=>new Promise(r=>window.releaseFile=r)})')
        h.call('a.endGuidedSession()');saved=h.call('return a.exportSessionReport()');h.page.evaluate('(raw)=>releaseFile(new Uint8Array(raw).buffer)',list(bytes.fromhex(tx)));h.page.wait_for_timeout(40)
        assert h.call('return a.exportSessionReport()')==saved;assert h.call('return a.resultState')=='unverified';close(h)
    test('C7 late file completion after explicit End cannot alter the session',late_file)
    def camera_failure():
        h=planned(browser);h.page.evaluate("Object.defineProperty(navigator,'mediaDevices',{configurable:true,value:{getUserMedia:async()=>{throw new DOMException('No','NotAllowedError')}}})")
        h.call('a.startScan()');h.page.wait_for_function('('+APP+').guidedStatus.phase==="halted"');assert not h.call('return a.scan.active');assert h.call('return a.guidedStatus.captureFailures')==1
        h.call('a.startScan()');assert h.call('return a.guidedStatus.captureFailures')==1;close(h)
    test('C4 camera permission failure halts once without automatic reacquisition',camera_failure)
    def restore():
        h=planned(browser);before=h.call('return [a.guidedStatus.planId,a.guidedStatus.current,a.psbtBase64]');h.page.evaluate('dispatchEvent(new PageTransitionEvent("pagehide",{persisted:true}));dispatchEvent(new PageTransitionEvent("pageshow",{persisted:true}))');h.page.wait_for_timeout(50)
        assert h.call('return [a.guidedStatus.planId,a.guidedStatus.current,a.psbtBase64]')==before;assert not h.call('return a.scan.active');close(h)
    test('C7 cached-page restoration preserves the plan without advancing or opening a camera',restore)
    def report_download():
        h=planned(browser);h.accept(h.call('return a.variants[0].txHex'))
        h.session_controls()
        with h.page.expect_download() as d:h.page.get_by_role('button',name='Save session report',exact=True).click()
        value=json.loads(Path(d.value.path()).read_text());assert value==h.call('return a.exportSessionReport()')
        plan=dict(value['plan']);digest=plan.pop('sha256');assert hashlib.sha256(json.dumps(plan,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()==digest
        assert h.call('return a.seed.value') not in json.dumps(value)
        close(h)
    test('C6 downloaded summary and independent plan SHA-256 agree with the immutable session',report_download)
    def download_failure():
        h=planned(browser);before=h.call('return a.exportSessionReport()');h.page.evaluate("window.oldCreate=document.createElement.bind(document);document.createElement=(t)=>{if(t==='a')throw Error('injected download');return oldCreate(t)}")
        h.call('a.downloadSessionReport()');assert h.call('return a.exportSessionReport()')==before;assert 'unavailable' in h.call('return a.notice');close(h)
    test('C6 failed report download never resets or alters the session',download_failure)
    for width in [320,360,768,1440]:
        def layout(w=width):
            h=planned(browser,2,w);h.accept('not a valid response');h.page.evaluate('scrollTo(0,0)');h.page.wait_for_timeout(50)
            assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            h.page.screenshot(path=str(SHOTS/f'session-halted-{w}.png'),full_page=True)
            assert h.page.locator('.guided-stop-reason').is_visible();close(h)
        test(f'C8 stopped-session labels and controls fit {width}px',layout)
    def fingerprint_layout():
        h=Harness(browser,width=360,height=1000);h.page.screenshot(path=str(SHOTS/'fingerprint-consolidated-360.png'),full_page=True)
        assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');qr=h.page.locator('#seed-qr-display').bounding_box();fp=h.page.locator('.wallet-fingerprint').bounding_box();assert fp['y']>=qr['y']+qr['height'];close(h)
    test('C1/C8 fingerprint remains outside the QR quiet zone on a narrow screen',fingerprint_layout)
    def ended_reset():
        h=planned(browser);h.call('a.sessionEndReason="Device refused boundary case";a.endGuidedSession()');before=h.call('return a.walletSession');assert h.call('return a.exportSessionReport().status.notCompleted')==2;h.call('a.randomizeAll()');h.page.wait_for_timeout(30);assert h.call('return a.walletSession')!=before;assert not h.call('return a.hasGuidedSession');assert h.call('return a.sessionChecks.length')==0;close(h)
    test('C7 explicit new wallet after End resets the journal without stored migration',ended_reset)
    browser.close()
output={'suite':'Consolidation exact-HTML browser / fingerprint simulations','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results}
OUT.write_text(json.dumps(output,indent=2));print(json.dumps({k:output[k] for k in ['suite','passed','failed']}));sys.exit(1 if output['failed'] else 0)
