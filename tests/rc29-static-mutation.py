#!/usr/bin/env python3
"""Development-only negative controls for the RC29 static-contract migration.
Executed against standalone RC28 HTML, never against candidate source in place.
"""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,shutil
ROOT=Path(__file__).resolve().parents[1]
HTML=Path(sys.argv[1]);OUT=Path(sys.argv[2]);H=HTML.read_text();rows=[]

def attempt(name,old,new,family,assertion):
    assert old in H and old!=new, 'Invalid mutation fixture '+name
    with tempfile.TemporaryDirectory(prefix='tbw-static-negative-') as d:
        path=Path(d)/'mutated.html';path.write_text(H.replace(old,new,1))
        receipt=Path(d)/'receipt.json'
        run=subprocess.run([sys.executable,str(ROOT/'tests'/(family+'-static.py')),str(path),str(receipt)],cwd=ROOT,capture_output=True,text=True,timeout=60)
        result=json.loads(receipt.read_text()) if receipt.exists() else {}
        matches=[r for r in result.get('results',[]) if r['name'].startswith(assertion)]
        passed=(run.returncode != 0 and len(matches)==1 and matches[0]['status']=='failed')
        rows.append({'probe':name,'family':family,'assertion':assertion,'passed':passed,'testReturnCode':run.returncode,'reportedFailed':result.get('failed')})

attempt('block-network-policies',"connect-src 'none'","connect-src 'self'",'delivery','D-S08')
attempt('remove-fingerprint-acknowledgment','@click="confirmWalletLoaded()"','@click="autoContinue()"','wallet-card','WC-S05')
attempt('remove-fingerprint-comparison','Continue only if they match.','You can continue without comparing.','wallet-card','WC-S07')
attempt('remove-no-passphrase-label','class="premium-passphrase">No passphrase','class="premium-passphrase">Passphrase optional','wallet-card','WC-S07')
attempt('change-seedqr-toggle','@click="seedQrExpanded = !seedQrExpanded"','@click="seedQrExpanded = true"','polish','P-S09')
attempt('erase-release-caveat','not an approved public release','an approved public release','polish','P-S07')
attempt('remove-purpose-warning','A match is not proof of firmware safety.','A match guarantees firmware safety.','copy','C-S01')

# Isolated source-lock mutation probes. Do not touch the source tree.
with tempfile.TemporaryDirectory(prefix='tbw-static-input-negative-') as d:
    tmp=Path(d)
    for n in ['source-lock.json','release.json','EXPECTED-OUTPUT.json','build.py','src/page.html','src/style.css']:
        q=tmp/n;q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/n,q)
    sys.path.insert(0,str(ROOT/'tests'));import rc29_static_contract as bridge
    original=bridge.ROOT
    try:
        bridge.ROOT=tmp
        bridge.release_identity()
        (tmp/'build.py').write_bytes((tmp/'build.py').read_bytes()+b'\n# unauthorized change\n')
        try:bridge.release_identity();ok=False
        except AssertionError:ok=True
        rows.append({'probe':'build-assembler-tampering','family':'current-pin','assertion':'build.py SHA-256','passed':ok})
        shutil.copy2(ROOT/'build.py',tmp/'build.py')
        release=json.loads((tmp/'release.json').read_text());release['status']='signed-release';(tmp/'release.json').write_text(json.dumps(release))
        try:bridge.release_identity();ok=False
        except AssertionError:ok=True
        rows.append({'probe':'unauthorized-status-uplift','family':'current-pin','assertion':'publisher/status','passed':ok})
    finally:bridge.ROOT=original

# Mutation of an archived historical assertion must not go undetected.
with tempfile.TemporaryDirectory(prefix='tbw-historic-negative-') as d:
    tmp=Path(d);dst=tmp/'fixtures/legacy-contracts-rc28';shutil.copytree(ROOT/'fixtures/legacy-contracts-rc28',dst)
    original=bridge.ROOT
    try:
        bridge.ROOT=tmp
        bridge.archive_original_tests()
        t=dst/'audit-static.py';t.write_bytes(t.read_bytes()+b'\n# tampered\n')
        try:bridge.archive_original_tests();ok=False
        except AssertionError:ok=True
        rows.append({'probe':'historical-test-tampering','family':'historical-archive','assertion':'SHA256 manifest','passed':ok})
    finally:bridge.ROOT=original

receipt={'schema':'tbw-rc29-static-negative-v1','scope':'development mutation testing only, no real candidate changes','htmlSha256':hashlib.sha256(HTML.read_bytes()).hexdigest(),'total':len(rows),'passed':sum(r['passed'] for r in rows),'failed':sum(not r['passed'] for r in rows),'probes':rows}
OUT.write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'total':receipt['total'],'passed':receipt['passed'],'failed':receipt['failed']}))
raise SystemExit(bool(receipt['failed']))
