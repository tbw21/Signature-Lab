#!/usr/bin/env python3
"""Chromium DOM/canvas/workflow simulations. No real camera or origin qualification.
Usage: python tests/browser.py artifact.html results.json screenshot_directory
Requires playwright, Pillow, qrcode, pyzbar/libzbar. System policy stays untouched.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright
from PIL import Image
from pyzbar.pyzbar import decode as read_qr
import qrcode
import base64
import io
import json
import re
import sys
import time
import os
import hashlib
from oracle import encode, decode

FILE=Path(sys.argv[1]); OUT=Path(sys.argv[2]); SHOTS=Path(sys.argv[3]);SHOTS.mkdir(parents=True,exist_ok=True)
HTML=FILE.read_text(); BASE=(Path(__file__).resolve().parent.parent/'baseline/TBW-Signature-Lab-v0.12.2.html').read_text()
APP="document.querySelector('[x-data]')._x_dataStack[0]"
UUID_SHIM="""Object.defineProperty(crypto,'randomUUID',{configurable:true,value:()=>{
 const b=crypto.getRandomValues(new Uint8Array(16));b[6]=(b[6]&15)|64;b[8]=(b[8]&63)|128;
 const h=Array.from(b,x=>x.toString(16).padStart(2,'0')).join('');
 return h.slice(0,8)+'-'+h.slice(8,12)+'-'+h.slice(12,16)+'-'+h.slice(16,20)+'-'+h.slice(20);
}})"""
CONFIG="""() => { const a=APP;
 if(a.isTestComplete)a.randomizeTransaction();a.invalidate();a.acknowledged=true;
 a.seed={value:'flag effort pulp expire foster kite scan taste replace note hundred rural',error:null};
 a.lockTime={value:'852864',error:null};a.psbtVersion='2';
 const field=value=>({value,error:null});
 a.inputs=[{id:50001,utxoId:field('95f94ca0dfc7aa5cf231edc3986738cb0ed63d47676a9e21e2a8e57e00b9e285:0'),amount:field('38151'),pathSuffix:field('0h/0/17'),sequence:field('4294967293')},
 {id:50002,utxoId:field('4ba5fb5dfc74a7e4fe4b0b266171f8d8b1b8e390eee9fe7646b49b91dcd0af86:1'),amount:field('20000'),pathSuffix:field('0h/0/15'),sequence:field('4294967293')}];
 a.outputs=[{id:50003,amount:field('56479'),dest:field('m/84h/0h/0h/0/18')}];
 a.testNumber=1;a.recompute();a.goToStep(2);
 return {ready:a.transactionReady,psbt:a.psbtBase64,tx:a.variants[0].txHex,state:a.stateSignature,seed:a.seed.value};
}""".replace('APP',APP)

def compact(n):
    if n<253:return bytes([n])
    for marker,size in [(253,2),(254,4),(255,8)]:
        if n<1<<(size*8):return bytes([marker])+n.to_bytes(size,'little')

def readcompact(raw,pos):
    first=raw[pos];pos+=1
    if first<253:return first,pos
    n={253:2,254:4,255:8}[first];return int.from_bytes(raw[pos:pos+n],'little'),pos+n

def witness_pairs(raw):
    assert raw[4:6]==b'\x00\x01';count,pos=readcompact(raw,6)
    for _ in range(count):
        pos+=36;n,pos=readcompact(raw,pos);pos+=n+4
    outs,pos=readcompact(raw,pos)
    for _ in range(outs):
        pos+=8;n,pos=readcompact(raw,pos);pos+=n
    pairs=[]
    for _ in range(count):
        n,pos=readcompact(raw,pos);assert n==2
        size,pos=readcompact(raw,pos);sig=raw[pos:pos+size];pos+=size
        size,pos=readcompact(raw,pos);pub=raw[pos:pos+size];pos+=size
        pairs.append((sig,pub))
    assert pos+4==len(raw)
    return pairs

def sign_psbt(psbt64, txhex):
    """Insert already-generated fixture signatures; this is not a signing implementation."""
    raw=base64.b64decode(psbt64); assert raw[:5]==b'psbt\xff'
    pairs=witness_pairs(bytes.fromhex(txhex));pos=5;maps=[]
    while pos<len(raw):
        start=pos
        while True:
            n,pos=readcompact(raw,pos)
            if n==0:break
            pos+=n;n,pos=readcompact(raw,pos);pos+=n
        maps.append(raw[start:pos])
    for index,(sig,pub) in enumerate(pairs):
        key=b'\x02'+pub
        maps[index+1]=maps[index+1][:-1]+compact(len(key))+key+compact(len(sig))+sig+b'\x00'
    return raw[:5]+b''.join(maps)


def png_uri(text):
    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=7,border=4)
    qr.add_data(text,optimize=0);qr.make(fit=True);im=qr.make_image().convert('RGB');o=io.BytesIO();im.save(o,format='PNG')
    return 'data:image/png;base64,'+base64.b64encode(o.getvalue()).decode()

class Harness:
    def __init__(self,browser,html=HTML,width=1280,height=1000,media=False):
        self.context=browser.new_context(viewport={'width':width,'height':height},offline=True)
        self.page=self.context.new_page();self.page.set_default_timeout(6000);self.errors=[];self.requests=[]
        self.page.on('pageerror',lambda e:self.errors.append(str(e)))
        self.page.on('request',lambda r:self.requests.append(r.url))
        if html != HTML: self.page.evaluate(UUID_SHIM)
        if media:
            self.page.evaluate("""() => {
              window.testSource=document.createElement('canvas');testSource.width=700;testSource.height=700;
              testSource.getContext('2d').fillStyle='white';testSource.getContext('2d').fillRect(0,0,700,700);
              window.mediaCalls=0;window.testStreams=[];
              Object.defineProperty(navigator,'mediaDevices',{configurable:true,value:{getUserMedia:async()=>{
                mediaCalls++;const stream=testSource.captureStream(15);testStreams.push(stream);
                window.testPulse??=setInterval(()=>{const c=testSource.getContext('2d');c.fillStyle='white';c.fillRect(0,0,1,1)},40);return stream;
              }}});
            }""")
        self.page.set_content(html, timeout=15000)  # Setup budget; action/app-ready budgets stay unchanged.
        self.page.wait_for_function("document.documentElement.dataset.appReady==='true'",timeout=10000)
        self.page.wait_for_timeout(30)
    def workspace(self,view):
        control=self.page.locator('#workspace-'+view)
        if control.count() and self.call('return a.workspaceView')!=view:
            control.click();self.page.wait_for_timeout(40)
    def open_tools(self):
        self.workspace('advanced')
        panel=self.page.locator('#advanced-tools')
        if panel.count() and not panel.evaluate('(e)=>e.open'):
            panel.locator(':scope > summary').click()
    def open_settings(self):
        self.open_tools()
        panel=self.page.locator('#transaction-editor')
        if panel.count():
            if not panel.evaluate('(e)=>e.open'):panel.locator(':scope > summary').click()
        else:self.page.get_by_role('button',name='Customize',exact=True).click()
    def open_evidence(self):
        self.workspace('test')
        panel=self.page.locator('#result-tools')
        if panel.count() and not panel.evaluate('(e)=>e.open'):panel.locator(':scope > summary').click()
    def file_details(self):
        self.workspace('test');self.open_evidence()
        panel=self.page.locator('#returned-file-details')
        if panel.count() and not panel.evaluate('(e)=>e.open'):panel.locator(':scope > summary').click()
    def session_controls(self):
        self.workspace('test')
        panel=self.page.locator('.guided-status')
        if panel.evaluate('(e)=>e.tagName==="DETAILS"&&!e.open'):panel.locator(':scope > summary').click()
    def summary_download(self):
        self.open_evidence()
        return self.page.get_by_role('button',name='Save summary only',exact=True)
    def call(self,expr,arg=None):
        return self.page.evaluate('(arg)=>{const a='+APP+';'+expr+'}',arg)
    def config(self):
        data=self.page.evaluate(CONFIG);assert data['ready'];self.page.wait_for_timeout(30);return data
    def accept(self,text):
        self.call('a.acceptArtifact(arg)',text);self.page.wait_for_timeout(25)
        return self.call('return {state:a.resultState,complete:a.isTestComplete,error:a.parseProblem||a.analysis?.error,checked:a.sessionChecks.length,evidence:a.analysis?.evidence}')
    def close(self):
        self.context.close()

results=[]
test_index=0
TEST_RANGE=os.environ.get("TEST_RANGE", "1:999").split(":")

def test(name,fn):
    global test_index
    test_index+=1
    if not int(TEST_RANGE[0]) <= test_index <= int(TEST_RANGE[1]): return
    started=time.monotonic()
    print('RUN',name,flush=True)
    try: fn();results.append({'name':name,'status':'passed','seconds':round(time.monotonic()-started,3)})
    except Exception as e:
        import traceback
        results.append({'name':name,'status':'failed','error':str(e),'traceback':traceback.format_exc()})
        print('FAILED',name,str(e),flush=True)
    OUT.write_text(json.dumps({'complete':False,'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results},indent=2))

def collect_qrs(h,mode='bbqr',seconds=15):
    frames={};widths=set();end=time.monotonic()+seconds;total=None
    while time.monotonic()<end:
        uri=h.page.locator('[x-ref="psbtQrCanvas"]').evaluate('(c)=>c.toDataURL()')
        img=Image.open(io.BytesIO(base64.b64decode(uri.split(',')[1])));widths.add(img.size)
        codes=read_qr(img)
        if codes:
            text=codes[0].data.decode()
            if mode=='bbqr' and text.startswith('B$'):
                total=int(text[4:6],36);frames[int(text[6:8],36)]=text
            elif mode=='ur' and text.upper().startswith('UR:'):
                match=re.search(r'/(\d+)-(\d+)/',text)
                if not match:return [text],widths
                total=int(match[2]);frames[int(match[1])-1]=text
            if total and len(frames)==total:return [frames[i] for i in range(total)],widths
        h.page.wait_for_timeout(65)
    raise AssertionError(f'QR collection incomplete: {len(frames)}/{total}')

with sync_playwright() as pw:
    browser=pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox'])
    environment={'browser':browser.version,'origin':'about:blank document.setContent','network':'offline context','UUID':'No shim for candidate; prior baseline rollback only has UUID shim','camera':'canvas MediaStream simulation, not physical hardware'}
    def startup():
        h=Harness(browser);assert h.call('return a.transactionReady&&a.psbtQrAvailable&&a.psbtQrMode==="ur"');assert not h.errors,h.errors;assert not h.requests,h.requests;h.close()
    test('offline exact-HTML startup, default BC-UR, no JS errors or network requests',startup)
    def isolation():
        h=Harness(browser);h.config();before=h.call('return [a.stateSignature,a.psbtBase64,JSON.stringify(a.variants),a.walletSession,JSON.stringify(a.sessionChecks),a.testNumber]')
        for mode in ['bbqr','ur','bbqr','ur','bbqr']:
            h.page.locator(f'#qr-format button[data-qr-mode="{mode}"]').click();assert h.call('return a.psbtQrAvailable')
        after=h.call('return [a.stateSignature,a.psbtBase64,JSON.stringify(a.variants),a.walletSession,JSON.stringify(a.sessionChecks),a.testNumber]');assert before==after
        assert not h.errors,h.errors;h.close()
    test('changing export transport preserves PSBT, seed/test state, references and ledger',isolation)
    def output():
        h=Harness(browser);fixture=h.config();h.page.locator('#qr-format button[data-qr-mode="bbqr"]').click();frames,widths=collect_qrs(h)
        assert decode(frames)['base64']==fixture['psbt'];assert len(widths)==1;assert all(f.startswith('B$ZP') for f in frames)
        assert h.call('return a.psbtQrCaption').endswith(f'{len(frames)} frames')
        h.page.screenshot(path=str(SHOTS/'desktop-bbqr.png'),full_page=True)
        h.close()
    test('actual rendered BBQr pixels decode with independent ZBar and Python; fixed QR dimensions',output)
    def import_mode(encoding,kind,version='2'):
        h=Harness(browser);data=h.config()
        if version=='0':h.call('a.psbtVersion="0";a.recompute()');data=h.call('return {psbt:a.psbtBase64,tx:a.variants[0].txHex}')
        raw=sign_psbt(data['psbt'],data['tx']) if kind=='P' else bytes.fromhex(data['tx'])
        frames=encode(raw,kind,encoding,40);frames=list(reversed(frames));frames.insert(1,frames[0])
        outcome=h.accept('\n\t'.join(frames));assert outcome['state']=='match',outcome;assert outcome['checked']==1;assert outcome['evidence']['artifactKind']==('psbt' if kind=='P' else 'tx');assert not h.errors,h.errors;h.close()
    for encoding in ['H','2','Z']:
        for kind in ['P','T']:test(f'BBQr {encoding}/{kind} signed response: automatic paste, shuffled and duplicate parts',lambda e=encoding,k=kind:import_mode(e,k))
    test('BBQr signed PSBT v0 preserves existing v0 support',lambda:import_mode('Z','P','0'))
    def legacy(mode):
        h=Harness(browser);data=h.config();raw=sign_psbt(data['psbt'],data['tx'])
        if mode=='hex':text=data['tx']
        elif mode=='base64':text=base64.b64encode(raw).decode()
        elif mode=='specter':
            text=base64.b64encode(raw).decode();chunks=[text[i:i+60] for i in range(0,len(text),60)];text='\n'.join(f'p{i+1}of{len(chunks)} {c}' for i,c in reversed(list(enumerate(chunks))))
        else:
            h.call('a.renderPsbtQr(new Uint8Array(arg))',list(raw));frames,_=collect_qrs(h,'ur');text='\n'.join(frames)
        out=h.accept(text);assert out['state']=='match',out;assert not h.errors,h.errors;h.close()
    for mode in ['hex','base64','specter','ur']:test(f'legacy {mode} successful signed import regression',lambda m=mode:legacy(m))
    def file_import(kind):
        h=Harness(browser);data=h.config();raw=sign_psbt(data['psbt'],data['tx'])
        payload='\n'.join(encode(raw,'P','Z')).encode() if kind=='bbqr text' else raw
        h.page.locator('input[type=file]').first.set_input_files({'name':'signed.txt' if kind=='bbqr text' else 'signed.psbt','mimeType':'text/plain' if kind=='bbqr text' else 'application/octet-stream','buffer':payload})
        h.page.wait_for_function(APP+'.isTestComplete');assert h.call('return a.resultState')=='match';assert not h.errors,h.errors;h.close()
    for kind in ['bbqr text','binary PSBT']:test(f'{kind} import through actual file-input change handler',lambda k=kind:file_import(k))
    def incomplete():
        h=Harness(browser);data=h.config();frames=encode(bytes.fromhex(data['tx']),'T','H',25)
        out=h.accept('\n'.join(frames[:-1]));assert out['state']=='incomplete' and not out['complete'] and out['checked']==0,out
        out=h.accept('\n'.join(frames));assert out['state']=='match';h.close()
    test('incomplete transfer never commits a result; explicit complete import succeeds',incomplete)
    def wrong_header():
        h=Harness(browser);data=h.config();frames=encode(bytes.fromhex(data['tx']),'P','2');out=h.accept('\n'.join(frames));assert out['state']=='incomplete' and 'file type' in out['error'],out;h.close()
    test('BBQr header type must match parsed PSBT/transaction bytes',wrong_header)
    def bad_signature():
        h=Harness(browser);data=h.config();raw=bytearray.fromhex(data['tx']);sig,_=witness_pairs(raw)[0];where=bytes(raw).index(sig);raw[where+10]^=1
        out=h.accept('\n'.join(encode(raw,'T','Z')));assert out['state']=='incomplete' and not out['complete'] and out['checked']==0,out;h.close()
    test('BBQr cannot bypass invalid ECDSA signature rejection',bad_signature)
    def wrong_test():
        h=Harness(browser);data=h.config();h.call('a.randomizeTransaction()');out=h.accept('\n'.join(encode(bytes.fromhex(data['tx']),'T','2')));assert out['state']=='incomplete' and 'different test' in out['error'],out;h.close()
    test('BBQr from an earlier transaction fails current-test binding',wrong_test)
    def unsigned():
        h=Harness(browser);data=h.config();out=h.accept('\n'.join(encode(base64.b64decode(data['psbt']),'P','Z')));assert out['state']=='incomplete' and not out['complete'],out;h.close()
    test('unsigned PSBT BBQr does not count as a signature check',unsigned)
    def trailing():
        h=Harness(browser);data=h.config();frames=encode(bytes.fromhex(data['tx']),'T','2');out=h.accept('\n'.join(frames+['B$2T0100AA']));assert out['state']=='incomplete' and not out['complete'],out;h.close()
    test('complete pasted sequence with conflicting trailing transfer is rejected',trailing)
    def demonstration():
        h=Harness(browser);h.config();published=re.search(r'var Vp=`([^`]+)`',BASE)[1]
        out=h.accept('\n'.join(encode(bytes.fromhex(published),'T','Z')));assert out['state']=='mismatch' and out['complete'] and out['evidence']['signaturesVerified']==2,out;h.close()
    test('supplied published non-reference signature fixture remains a valid mismatch through BBQr',demonstration)
    def completed():
        h=Harness(browser);data=h.config();out=h.accept('\n'.join(encode(bytes.fromhex(data['tx']),'T','Z')));assert out['state']=='match'
        before=h.call('return [a.completedAt,a.psbtQrMode,JSON.stringify(a.sessionChecks)]');h.call('a.setPsbtQrMode("bbqr");a.verify();a.acceptArtifact("bad")');after=h.call('return [a.completedAt,a.psbtQrMode,JSON.stringify(a.sessionChecks)]');assert before==after
        h.call('a.randomizeTransaction()');assert h.call('return a.testNumber===2&&a.sessionChecks.length===1&&!a.isTestComplete')
        before=h.call('return JSON.stringify(a.sessionChecks)');h.page.locator('#qr-format button[data-qr-mode="bbqr"]').click();assert h.call('return JSON.stringify(a.sessionChecks)')==before;h.close()
    test('completed test locks correctly; next-test BBQr preserves populated session ledger',completed)
    def restoration():
        h=Harness(browser);h.config();h.page.locator('#qr-format button[data-qr-mode="bbqr"]').click();before=h.call('return [a.psbtBase64,a.stateSignature,a.walletSession]')
        h.page.evaluate("window.dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true}))");assert not h.call('return a.psbtQrAvailable')
        h.page.evaluate("window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))");h.page.wait_for_timeout(50);assert h.call('return a.psbtQrAvailable&&a.psbtQrMode==="bbqr"');assert before==h.call('return [a.psbtBase64,a.stateSignature,a.walletSession]');h.close()
    test('cached-page pause/resume restores selected transport with unchanged transaction',restoration)
    def idempotence():
        h=Harness(browser);h.config();h.page.locator('#qr-format button[data-qr-mode="bbqr"]').click();before=h.call('return [a.psbtBase64,a.stateSignature,a.psbtQrCaption]')
        for _ in range(3):h.call('a.apply()')
        assert before==h.call('return [a.psbtBase64,a.stateSignature,a.psbtQrCaption]');assert not h.errors,h.errors;h.close()
    test('idempotent repeated apply retains the current export and test',idempotence)
    def unavailable():
        # Deliberately remove only optional-module source in memory, never from artifact bytes.
        altered=re.sub(r'/\* TBW_BBQR_CODEC_BEGIN \*/[\s\S]*?/\* TBW_BBQR_CODEC_END \*/','',HTML)
        h=Harness(browser,altered);data=h.config();assert h.call('return a.transactionReady&&a.psbtQrAvailable')
        h.page.locator('#qr-format button[data-qr-mode="bbqr"]').click();assert h.call('return a.transactionReady&&!a.psbtQrAvailable&&!!a.qrProblem')
        h.page.locator('#qr-format button[data-qr-mode="ur"]').click();assert h.call('return a.psbtQrAvailable')
        assert h.accept(data['tx'])['state']=='match';h.close()
    test('optional BBQr module absence fails only BBQr and leaves core/BC-UR/raw import usable',unavailable)
    def qr_error():
        h=Harness(browser);h.config()
        h.page.locator('[x-ref="psbtQrCanvas"]').evaluate('(c)=>{c.realGetContext=c.getContext;c.getContext=()=>{throw Error("injected canvas failure")}}')
        h.page.locator('#qr-format button[data-qr-mode="bbqr"]').click();assert h.call('return !a.psbtQrAvailable&&!!a.qrProblem&&a.transactionReady')
        h.page.locator('[x-ref="psbtQrCanvas"]').evaluate('(c)=>{c.getContext=c.realGetContext}')
        h.call('a.recompute()');assert not h.call('return a.psbtQrAvailable')
        h.page.locator('#qr-format button[data-qr-mode="ur"]').click();assert h.call('return a.psbtQrAvailable');h.close()
    test('canvas failure stays terminal until explicit transport change, core stays usable',qr_error)
    def read_error():
        h=Harness(browser);h.config();h.call('a.loadFile({size:10,arrayBuffer:async()=>{throw Error("injected read error")}})');h.page.wait_for_timeout(40)
        assert h.call('return a.resultState==="incomplete"&&!a.isTestComplete&&a.parseProblem.includes("could not be read")');h.close()
    test('file read failure does not retain or commit signed results',read_error)
    def huge_file():
        h=Harness(browser);h.config();h.call('a.loadFile({size:524289,arrayBuffer:async()=>{throw Error("must not read")}})');h.page.wait_for_timeout(30);assert h.call('return a.parseProblem.includes("512 KiB")&&!a.isTestComplete');h.close()
    test('file cap is enforced before reading data',huge_file)
    def delayed_file():
        h=Harness(browser);data=h.config();h.call('window.releaseFile=null;window.pendingFile=a.loadFile({size:100,arrayBuffer:()=>new Promise(resolve=>{window.releaseFile=resolve})});')
        h.call('a.randomizeTransaction()');h.page.evaluate('(raw)=>releaseFile(new Uint8Array(raw).buffer)',list(bytes.fromhex(data['tx'])));h.page.wait_for_timeout(80)
        assert h.call('return a.resultState==="unverified"&&!a.isTestComplete&&a.artifactText===""');h.close()
    test('late file read after new transaction is discarded',delayed_file)
    def no_clipboard_download():
        h=Harness(browser);h.config();before=h.call('return a.psbtBase64')
        h.page.evaluate("() => {URL.createObjectURL=()=>{throw Error('injected disk/download failure')}}")
        h.call('a.downloadPsbt()');assert h.call('return a.notice.includes("Download unavailable")&&a.transactionReady');assert h.call('return a.psbtBase64')==before;h.close()
    test('simulated download allocation failure leaves PSBT/core unchanged',no_clipboard_download)
    def scanner_direct(encoding):
        h=Harness(browser,media=True);data=h.config();frames=encode(bytes.fromhex(data['tx']),'T',encoding,40)
        h.call('return Promise.race([a.startScan(),new Promise((_,reject)=>setTimeout(()=>reject(Error("simulated camera start timed out")),3000))])');assert h.call('return a.scan.active')
        for frame in list(reversed(frames)):
            h.call('a.onScanHit({text:arg,binary:new Uint8Array()})',frame)
        assert h.call('return a.resultState==="match"&&!a.scan.active&&a.sessionChecks.length===1');assert h.page.evaluate('testStreams.every(s=>s.getTracks().every(t=>t.readyState==="ended"))');assert not h.errors,h.errors;h.close()
    for enc in ['H','2','Z']:test(f'live scanner intake state machine accepts {enc} BBQr and stops all simulated tracks',lambda e=enc:scanner_direct(e))
    def scanner_pixels():
        h=Harness(browser,media=True);data=h.config();frames=encode(bytes.fromhex(data['tx']),'T','Z',60)
        h.call('return Promise.race([a.startScan(),new Promise((_,reject)=>setTimeout(()=>reject(Error("simulated camera start timed out")),3000))])')
        for frame in frames:
            h.page.evaluate("""async (src)=>{const image=new Image();image.src=src;await image.decode();
              const ctx=testSource.getContext('2d');ctx.fillStyle='white';ctx.fillRect(0,0,700,700);
              ctx.imageSmoothingEnabled=false;ctx.drawImage(image,0,0,700,700)}""",png_uri(frame))
            h.page.wait_for_timeout(500)
        h.page.wait_for_function(APP+'.isTestComplete',timeout=5000);assert h.call('return a.resultState')=='match';h.close()
    test('actual scanner jsQR decodes independent QR pixels through canvas MediaStream',scanner_pixels)
    def mixed_scan(binary=False):
        h=Harness(browser,media=True);data=h.config();frames=encode(bytes.fromhex(data['tx']),'T','H',40)
        h.call('return Promise.race([a.startScan(),new Promise((_,reject)=>setTimeout(()=>reject(Error("simulated camera start timed out")),3000))])');h.call('a.onScanHit({text:arg,binary:new Uint8Array()})',frames[0]);assert h.call('return a.scan.progress>0&&a.scan.progress<1')
        if binary:h.call('a.onScanHit({text:"",binary:new Uint8Array(arg)})',list(base64.b64decode(data['psbt'])))
        else:h.call('a.onScanHit({text:"p1of2 AAA",binary:new Uint8Array()})')
        assert h.call('return !a.scan.active&&!!a.scan.error&&!a.isTestComplete&&a.sessionChecks.length===0');h.close()
    test('scanner rejects mixed BBQr/Specter sequences',mixed_scan)
    test('scanner rejects static binary PSBT while an animated sequence is active',lambda:mixed_scan(True))
    def interruption():
        h=Harness(browser,media=True);data=h.config();frames=encode(bytes.fromhex(data['tx']),'T','2',40)
        h.call('return Promise.race([a.startScan(),new Promise((_,reject)=>setTimeout(()=>reject(Error("simulated camera start timed out")),3000))])');h.call('a.onScanHit({text:arg,binary:new Uint8Array()})',frames[0]);h.call('a.stopScan();return Promise.race([a.startScan(),new Promise((_,reject)=>setTimeout(()=>reject(Error("simulated camera restart timed out")),3000))])')
        for frame in frames[1:]:h.call('a.onScanHit({text:arg,binary:new Uint8Array()})',frame)
        assert h.call('return !a.isTestComplete&&a.scan.progress<1');h.call('a.onScanHit({text:arg,binary:new Uint8Array()})',frames[0]);assert h.call('return a.resultState')=='match';h.close()
    test('scan interruption discards previous fragments; explicit restart needs every part',interruption)
    def concurrent():
        h=Harness(browser,media=True);h.config();h.page.evaluate("()=>{navigator.mediaDevices.getUserMedia=()=>{window.mediaCalls++;return new Promise(resolve=>{window.releaseMedia=resolve})}}")
        h.call('window.pendingStart=a.startScan();a.startScan()');assert h.page.evaluate('mediaCalls')==1
        h.call('a.randomizeTransaction()');h.page.evaluate('window.lateStream=testSource.captureStream(10);releaseMedia(lateStream)');h.page.wait_for_timeout(50)
        assert not h.call('return a.scan.active');assert h.page.evaluate('lateStream.getTracks().every(t=>t.readyState==="ended")');h.close()
    test('concurrent camera start is bounded; late permission result after test change is stopped',concurrent)
    def permission():
        h=Harness(browser,media=True);h.config();h.page.evaluate("()=>{navigator.mediaDevices.getUserMedia=async()=>{throw new DOMException('denied','NotAllowedError')}}");h.call('return Promise.race([a.startScan(),new Promise((_,reject)=>setTimeout(()=>reject(Error("simulated camera start timed out")),3000))])')
        assert h.call('return !a.scan.active&&a.scan.error.includes("denied")&&!a.isTestComplete');h.close()
    test('camera permission/dependency failure is terminal and visible',permission)
    def timeout_scan():
        h=Harness(browser,media=True);h.config();h.page.evaluate("()=>{window.realTimeout=setTimeout;window.setTimeout=(f,t,...args)=>realTimeout(f,t===120000?10:t,...args)}")
        h.call('return Promise.race([a.startScan(),new Promise((_,reject)=>setTimeout(()=>reject(Error("simulated camera start timed out")),3000))])');h.page.wait_for_timeout(100);assert h.call('return !a.scan.active&&a.scan.error.includes("two-minute")&&!a.isTestComplete');h.close()
    test('two-minute scanner limit callback stops capture (time accelerated in harness)',timeout_scan)
    def reset_recovery():
        h=Harness(browser);h.config();before=h.call('return a.walletSession');h.page.locator('#qr-format button[data-qr-mode="bbqr"]').click();h.close()
        fresh=Harness(browser);assert fresh.call('return a.walletSession')!=before;assert fresh.call('return a.testNumber===1&&a.sessionChecks.length===0&&a.psbtQrMode==="ur"');fresh.close()
        old=Harness(browser,BASE);assert old.call('return a.transactionReady&&a.sessionChecks.length===0');old.close()
    test('fresh-open upgrade, context-loss recovery and baseline rollback simulations',reset_recovery)
    for width,height in [(320,700),(360,800),(390,844),(768,1024),(1440,1000)]:
        def layout(w=width,hh=height):
            h=Harness(browser,width=w,height=hh);h.config();h.page.locator('#qr-format button[data-qr-mode="bbqr"]').click();h.page.wait_for_timeout(120)
            sizes=h.page.evaluate("""() => {const s=document.getElementById('qr-format').getBoundingClientRect();
              const caption=document.querySelector('.qr-column .qr-caption');return {width:innerWidth,scroll:document.documentElement.scrollWidth,
              left:s.left,right:s.right,captionScroll:caption.scrollWidth,captionWidth:caption.clientWidth};}""")
            assert sizes['scroll']<=sizes['width']+1,sizes;assert sizes['left']>=0 and sizes['right']<=w,sizes
            assert not h.errors,h.errors
            if w in (360,768):h.page.screenshot(path=str(SHOTS/f'bbqr-{w}px.png'),full_page=True)
            h.close()
        test(f'BBQr layout at {width}x{height}: selector in viewport, no horizontal overflow',layout)

    def selector_semantics():
        h=Harness(browser);h.config();g=h.page.locator('#qr-format');b=g.locator('button')
        assert g.get_attribute('role')=='group'
        assert g.get_attribute('aria-labelledby')=='qr-format-label'
        assert g.get_attribute('aria-describedby')=='qr-format-hint'
        assert b.count()==2 and b.all_text_contents()==['BC-UR','BBQr']
        assert all(x.get_attribute('type')=='button' for x in b.all())
        assert g.locator('button[aria-pressed="true"]').count()==1
        assert b.nth(0).get_attribute('aria-pressed')=='true'
        assert h.page.locator('select#qr-format').count()==0
        h.close()
    test('segmented selector: two named native buttons, labelled group, BC-UR default, no retired dropdown',selector_semantics)
    def keyboard_selector():
        h=Harness(browser);h.config();ur=h.page.locator('[data-qr-mode="ur"]');bbqr=h.page.locator('[data-qr-mode="bbqr"]')
        ur.focus();h.page.keyboard.press('Tab');assert bbqr.evaluate('(b)=>document.activeElement===b')
        h.page.keyboard.press('Enter');assert h.call('return a.psbtQrMode==="bbqr"&&a.psbtQrAvailable')
        assert bbqr.get_attribute('aria-pressed')=='true' and ur.get_attribute('aria-pressed')=='false'
        h.page.keyboard.press('Shift+Tab');assert ur.evaluate('(b)=>document.activeElement===b')
        h.page.keyboard.press('Space');assert h.call('return a.psbtQrMode==="ur"&&a.psbtQrAvailable')
        assert ur.get_attribute('aria-pressed')=='true' and bbqr.get_attribute('aria-pressed')=='false'
        assert not h.errors,h.errors;h.close()
    test('segmented selector supports Tab, Shift+Tab, Enter and Space with exclusive pressed state',keyboard_selector)
    def selector_style():
        h=Harness(browser);h.config()
        styles=h.page.evaluate("""() => {
          const keys=['backgroundColor','borderRadius','borderWidth','paddingTop','paddingRight','gap'];
          const bkeys=['color','backgroundColor','borderRadius','paddingTop','paddingRight','minHeight','fontSize'];
          const style=(e,ks)=>Object.fromEntries(ks.map(k=>[k,getComputedStyle(e)[k]]));
          const seed=document.getElementById('word-count'),qr=document.getElementById('qr-format');
          return {seed:style(seed,keys),qr:style(qr,keys),seedActive:style(seed.querySelector('[aria-pressed=true]'),bkeys),
            qrActive:style(qr.querySelector('[aria-pressed=true]'),bkeys),seedOther:style(seed.querySelector('[aria-pressed=false]'),bkeys),qrOther:style(qr.querySelector('[aria-pressed=false]'),bkeys)};
        }""")
        assert styles['seed']==styles['qr'],styles
        assert styles['seedActive']==styles['qrActive'],styles
        assert styles['seedOther']==styles['qrOther'],styles
        h.page.screenshot(path=str(SHOTS/'segmented-desktop.png'),full_page=True)
        h.page.locator('.qr-format-control').screenshot(path=str(SHOTS/'selector-bc-ur.png'))
        h.page.locator('[data-qr-mode="bbqr"]').click()
        h.page.locator('.qr-format-control').screenshot(path=str(SHOTS/'selector-bbqr.png'))
        h.close()
    test('segmented selector computed styling matches the existing 12/24-word control',selector_style)
    def selector_disabled():
        h=Harness(browser);h.config();h.call('a.inputs[0].amount.value="invalid";a.recompute()');h.page.wait_for_timeout(40)
        assert h.page.locator('#qr-format button:disabled').count()==2
        before=h.call('return a.psbtQrMode');h.page.locator('[data-qr-mode="bbqr"]').evaluate('(b)=>b.click()')
        assert h.call('return a.psbtQrMode')==before;h.close()
    test('invalid transaction disables both format buttons and native click cannot bypass it',selector_disabled)
    def selector_completion():
        h=Harness(browser);data=h.config();h.accept(data['tx'])
        assert h.page.locator('#qr-format').is_hidden()
        assert h.page.locator('#qr-format button:disabled').count()==2
        before=h.call('return [a.psbtQrMode,a.completedAt,JSON.stringify(a.sessionChecks)]')
        h.page.locator('[data-qr-mode="bbqr"]').evaluate('(b)=>b.click()')
        assert before==h.call('return [a.psbtQrMode,a.completedAt,JSON.stringify(a.sessionChecks)]');h.close()
    test('completed test hides/disables both buttons and cannot be altered by their clicks',selector_completion)
    def selector_repeat():
        h=Harness(browser);h.config();h.page.locator('[data-qr-mode="bbqr"]').click()
        before=h.call('return [a.psbtBase64,a.stateSignature,a.psbtQrCaption,a.walletSession,JSON.stringify(a.sessionChecks)]')
        for _ in range(5):h.page.locator('[data-qr-mode="bbqr"]').click()
        assert before==h.call('return [a.psbtBase64,a.stateSignature,a.psbtQrCaption,a.walletSession,JSON.stringify(a.sessionChecks)]')
        assert h.page.locator('#qr-format button[aria-pressed="true"]').count()==1
        assert not h.errors,h.errors;h.close()
    test('repeated selected-button clicks are idempotent without changing the PSBT or session',selector_repeat)
    def selector_restore():
        h=Harness(browser);h.config();h.page.locator('[data-qr-mode="bbqr"]').click()
        h.page.evaluate("window.dispatchEvent(new PageTransitionEvent('pagehide',{persisted:true}));window.dispatchEvent(new PageTransitionEvent('pageshow',{persisted:true}))")
        h.page.wait_for_timeout(60)
        assert h.page.locator('[data-qr-mode="bbqr"]').get_attribute('aria-pressed')=='true'
        assert h.page.locator('[data-qr-mode="ur"]').get_attribute('aria-pressed')=='false'
        assert h.call('return a.psbtQrAvailable&&!a.scan.active');h.close()
    test('cached-page restoration keeps the segmented selection and does not resume scanning',selector_restore)
    def selector_focus():
        h=Harness(browser);h.config();b=h.page.locator('[data-qr-mode="bbqr"]');b.focus();h.page.keyboard.press('Tab');h.page.keyboard.press('Shift+Tab')
        assert b.evaluate('(b)=>b.matches(":focus-visible")')
        focus=b.evaluate('(b)=>({outline:getComputedStyle(b).outlineStyle,width:getComputedStyle(b).outlineWidth})')
        assert focus['outline']!='none' and focus['width']!='0px',focus;h.close()
    test('keyboard format selection has a visible focus outline',selector_focus)
    for width in [320,360,390,768,1440]:
        def selector_layout(w=width):
            h=Harness(browser,width=w,height=900);h.config()
            for mode in ['ur','bbqr']:
                h.page.locator(f'[data-qr-mode="{mode}"]').click()
                rect=h.page.locator('#qr-format').bounding_box();assert rect and rect['x']>=0 and rect['x']+rect['width']<=w
                b=[x.bounding_box() for x in h.page.locator('#qr-format button').all()]
                assert abs(b[0]['y']-b[1]['y'])<1 and b[0]['x']+b[0]['width']<=b[1]['x']
                assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
            if w in (360,1440):h.page.screenshot(path=str(SHOTS/f'segmented-{w}px.png'),full_page=True)
            assert not h.errors,h.errors;h.close()
        test(f'segmented controls at {width}px stay side by side with no clipping or horizontal scroll',selector_layout)
    def selector_text_zoom():
        h=Harness(browser,width=360,height=900);h.config()
        h.page.add_style_tag(content='#qr-format button,#qr-format-label,#qr-format-hint{font-size:28px!important}')
        h.page.locator('[data-qr-mode="bbqr"]').click()
        assert h.page.evaluate('document.documentElement.scrollWidth<=innerWidth+1')
        b=h.page.locator('#qr-format').bounding_box();assert b and b['x']>=0 and b['x']+b['width']<=360
        h.page.screenshot(path=str(SHOTS/'segmented-large-text.png'),full_page=True);h.close()
    test('selector-only 200-percent text-size simulation remains operable at 360px (not browser zoom)',selector_text_zoom)

    browser.close()

out={'suite':'Chromium browser/workflow/lifecycle simulations','complete':True,'test_range':':'.join(TEST_RANGE),'total_defined':test_index,'artifact':FILE.name,'sha256':hashlib.sha256(FILE.read_bytes()).hexdigest(),'environment':environment,
     'passed':sum(r['status']=='passed' for r in results),'failed':sum(r['status']=='failed' for r in results),'results':results}
OUT.write_text(json.dumps(out,indent=2));print(json.dumps({k:out[k] for k in ['suite','passed','failed']},indent=2))
sys.exit(1 if out['failed'] else 0)
