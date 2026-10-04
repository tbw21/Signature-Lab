#!/usr/bin/env python3
"""Additional exact-HTML UI and camera-lifecycle simulations. No UUID shim on candidate."""
from pathlib import Path
# Reuse the one test harness, without executing its separate legacy case list.
exec((Path(__file__).parent/'browser.py').read_text().split('with sync_playwright() as pw:')[0],globals())
import subprocess
fixtures=json.loads(subprocess.check_output(['node','-e',"const fs=require('fs');const {load}=require('./tests/load.cjs');const{A}=load(process.argv[1]);const frames=A.w_(A.K.decode(A.Np(A.Hp())[0].txHex),90),BW=A.__().default,p=A.g_().FountainEncoderPart.fromCBOR(BW.decode(frames[0].split('/')[2],BW.STYLES.MINIMAL));p._fragment[3]^=1;console.log(JSON.stringify({frames,bad:[A.x_.UREncoder.encodePart('crypto-psbt',p),...frames.slice(1)]}))",str(FILE)],cwd=Path(__file__).resolve().parents[1],text=True))
def add_global(psbt,key=b'\xfc\x01x\x00',value=b'audit-marker'):
    pos=5
    while True:
        n,pos=readcompact(psbt,pos)
        if not n:break
        pos+=n;n,pos=readcompact(psbt,pos);pos+=n
    return psbt[:pos-1]+compact(len(key))+key+compact(len(value))+value+b'\0'+psbt[pos:]
def clean_close(h):
    assert not h.errors,h.errors
    h.close()
with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    def startup_no_uuid():
        h=Harness(browser);assert h.call('return a.transactionReady');assert not h.requests;clean_close(h)
    test('Q2 exact HTML starts without candidate UUID shim',startup_no_uuid)
    def metadata_expected():
        h=Harness(browser);d=h.config();p=sign_psbt(d['psbt'],d['tx']);assert h.accept(p.hex())['state']=='match'
        h.file_details();assert h.page.locator('.metadata-assessment').is_visible();assert h.page.locator('.metadata-summary').inner_text()=='Only expected signing changes'
        assert h.call('return a.metadataSummary.unexpected')==0;clean_close(h)
    test('D1 completed expected PSBT shows separate metadata assessment',metadata_expected)
    def metadata_warning():
        h=Harness(browser);d=h.config();p=add_global(sign_psbt(d['psbt'],d['tx']));assert h.accept(p.hex())['state']=='match'
        assert h.page.locator('.file-review-action').is_visible();h.file_details();box=h.page.locator('.metadata-assessment');assert box.is_visible() and box.get_attribute('data-metadata-status')=='unexpected'
        box.locator('summary').click();assert 'Application-specific field' in box.inner_text();assert 'added' in box.inner_text();assert h.call('return a.report().metadata.unexpected')==1;clean_close(h)
    test('D1 unknown marker stays a signature match but has visible amber metadata warning',metadata_warning)
    def raw_assessment():
        h=Harness(browser);d=h.config();h.accept(d['tx']);h.file_details();assert h.page.locator('.metadata-summary').inner_text()=='No PSBT metadata';clean_close(h)
    test('D1 raw transaction explicitly has no PSBT metadata assessment',raw_assessment)
    def evidence_download():
        h=Harness(browser);d=h.config();p=add_global(sign_psbt(d['psbt'],d['tx']));h.page.locator('input[type=file]').first.set_input_files({'name':'signed.psbt','mimeType':'application/octet-stream','buffer':p});h.page.wait_for_timeout(50)
        h.open_evidence()
        with h.page.expect_download() as event:h.page.get_by_role('button',name='Save evidence',exact=True).click()
        data=json.loads(Path(event.value.path()).read_text());assert data['returnedArtifact']['hex']==p.hex();assert data['submission']['originalFileHex']==p.hex();assert d['seed'] not in json.dumps(data);assert data['report']==h.call('return a.report()');assert data['report']['build']['sourceSha256'];clean_close(h)
    test('D2 explicit evidence download contains exact original file and frozen seed-excluding snapshot',evidence_download)
    def failed_download():
        h=Harness(browser);d=h.config();h.accept(d['tx']);before=h.call('return JSON.stringify(a.report())');h.page.evaluate('() => { URL.createObjectURL=()=>{throw Error("injected full disk boundary")}; return true; }');h.open_evidence();h.page.get_by_role('button',name='Save evidence',exact=True).click();assert 'unavailable' in h.call('return a.notice');assert h.call('return JSON.stringify(a.report())')==before;clean_close(h)
    test('D2 evidence download failure does not mutate verification result',failed_download)
    def strict_policy():
        h=Harness(browser);h.config();h.open_settings();h.page.locator('#signing-policy').select_option('plain');assert h.call('return a.signingPolicy')=='plain';tx=h.call('return a.variants.find(v=>v.ids.includes("plain")).txHex');assert h.accept(tx)['state']=='match';assert h.call('return a.report().signingPolicy.id')=='plain';assert h.page.locator('#signing-policy').is_disabled();clean_close(h)
    test('D4 fixed policy is explicit, recorded and locked after verification',strict_policy)
    def strict_other():
        h=Harness(browser);h.config();h.call('a.setSigningPolicy("plain")');other=h.call('return a.variants.find(v=>!v.ids.includes("plain"))?.txHex');assert other,'fixture requires distinct policies';assert h.accept(other)['state']=='mismatch';assert 'selected reference policy' in h.page.locator('.result-message').inner_text();clean_close(h)
    test('D4 another valid reference method differs under the fixed selected policy',strict_other)
    def profile_locked():
        h=Harness(browser);h.config();h.accept('bad');h.call('a.setSigningPolicy("plain")');assert h.call('return a.signingPolicy')=='compatible';h.call('a.randomizeTransaction();a.setSigningPolicy("plain")');assert h.call('return a.signingPolicy')=='plain';clean_close(h)
    test('D4 incomplete attempt cannot silently change policy; explicit new transaction unlocks it',profile_locked)
    def ur_failed_scan():
        h=Harness(browser,media=True);h.config();h.call('a.startScan()');h.page.wait_for_function(APP+'.scan.phase==="scanning"');
        h.call('for(const text of arg)a.onScanHit({text,binary:new Uint8Array()})',fixtures['bad']);assert h.call('return a.scan.phase')=='failed';assert 'checksum' in h.call('return a.scan.error');assert h.call('return a.scan.progress')==0;assert h.call('return a.resultState')=='unverified';assert h.page.evaluate('testStreams.every(s=>s.getTracks().every(t=>t.readyState==="ended"))');clean_close(h)
    test('R1 failed UR checksum visibly stops the exact app camera session',ur_failed_scan)
    for name,tail in [('unrelated tail','garbage'),('mixed family','p1of1 AA==')]:
        def finite(value=tail):
            h=Harness(browser);h.config();r=h.accept('\n'.join(fixtures['frames'])+'\n'+value);assert r['state']=='incomplete' and r['checked']==0;clean_close(h)
        test('R2 exact app rejects complete UR plus '+name,finite)
    for kind in ['ended','inactive','error']:
        def lost(event=kind):
            h=Harness(browser,media=True);h.config();h.call('a.startScan()');h.page.wait_for_function(APP+'.scan.phase==="scanning"');
            target={'ended':'testStreams[0].getVideoTracks()[0]','inactive':'testStreams[0]','error':"document.querySelector('video')"}[event]
            h.page.evaluate(f'{target}.dispatchEvent(new Event("{event}"))');assert h.call('return a.scan.phase')=='failed';assert not h.call('return a.scan.active');assert h.call('return a.scan.error');h.page.locator('[x-show="scan.error"]').wait_for(state='visible');clean_close(h)
        test('R4 exact app handles '+kind+' with a visible terminal error',lost)
    def pending_permission():
        h=Harness(browser);h.config();h.page.clock.install();h.page.evaluate("Object.defineProperty(navigator,'mediaDevices',{configurable:true,value:{getUserMedia:()=>new Promise(r=>window.grantCamera=r)}})")
        h.call('a.startScan();return true');assert h.call('return a.scan.phase')=='awaiting-permission';h.page.clock.fast_forward(30001);assert h.call('return a.scan.phase')=='failed';assert h.call('return a.scan.code')=='CAMERA_START_TIMEOUT';clean_close(h)
    test('R3 exact app expires unanswered permission with controlled clock and no UUID shim',pending_permission)
    def late_permission():
        h=Harness(browser);h.config();h.page.clock.install();h.page.evaluate("Object.defineProperty(navigator,'mediaDevices',{configurable:true,value:{getUserMedia:()=>new Promise(r=>window.grantCamera=r)}})")
        h.call('a.startScan();return true');h.page.clock.fast_forward(30001);h.page.evaluate("const c=document.createElement('canvas');window.lateStream=c.captureStream();grantCamera(lateStream)");h.page.wait_for_timeout(10);assert h.page.evaluate('lateStream.getTracks().every(t=>t.readyState==="ended")');assert h.call('return a.scan.phase')=='failed';clean_close(h)
    test('R3 late granted actual canvas MediaStream is stopped after app startup expiry',late_permission)
    def cache():
        h=Harness(browser);h.config();before=h.call('return a.preparedRevision');times=h.call('const times=[];for(let i=0;i<20;i++){const t=performance.now();a.recompute();times.push(performance.now()-t)}return times');assert h.call('return a.preparedRevision')==before;OUT.with_name(OUT.stem+'-cache.json').write_text(json.dumps({'timingsMs':times,'medianMs':sorted(times)[10],'scope':'same prepared 2-input test, Chromium harness; not phone benchmark'}));clean_close(h)
    test('D3 repeated exact app recomputation retains the prepared revision',cache)
    def immutable_report():
        h=Harness(browser);d=h.config();h.accept(d['tx']);r=h.call('return a.report()');h.call('a.firmware="changed outside UI";a.device="changed"');assert h.call('return a.report()')==r;clean_close(h)
    test('D2 post-completion operator-field mutation cannot rewrite the report snapshot',immutable_report)
    for width in [360,768,1440]:
        def result_layout(w=width):
            h=Harness(browser,width=w,height=950);d=h.config();h.accept(add_global(sign_psbt(d['psbt'],d['tx'])).hex());h.file_details();h.page.locator('.metadata-assessment summary').click();assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1');h.open_evidence();assert h.page.get_by_role('button',name='Save evidence',exact=True).is_visible();h.page.screenshot(path=str(SHOTS/f'reliability-result-{w}.png'),full_page=True);clean_close(h)
        test(f'D1/D2 result evidence controls and metadata details fit {width}px',result_layout)
    def rollback_rc2():
        h=Harness(browser);d=h.config();h.accept(d['tx']);session=h.call('return a.walletSession');clean_close(h)
        previous=(Path(__file__).resolve().parents[1]/'baseline/TBW-Signature-Lab-v0.13.0-rc2.html').read_text()
        old=Harness(browser,html=previous);assert old.call('return a.transactionReady');assert old.call('return a.walletSession')!=session;clean_close(old)
        fresh=Harness(browser);assert fresh.call('return a.transactionReady && a.sessionChecks.length===0');clean_close(fresh)
    test('Q2 rollback to untouched rc2 and return to fresh candidate have one active context and no stored migration',rollback_rc2)
    browser.close()
out={'suite':'Reliability exact-HTML browser integration','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'artifact':FILE.name,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results}
OUT.write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['suite','passed','failed']}));sys.exit(1 if out['failed'] else 0)
