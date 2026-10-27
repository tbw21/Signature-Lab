"""RC29 static-test bridge: exact current source pins; never a runtime code path.

Historical scripts are preserved byte-for-byte under fixtures/legacy-contracts-rc28.
The current contract binds an actual candidate to the authoritative source lock,
independently supplies current visible UI checks, and rejects publisher/status uplift.
"""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
def sha(raw): return hashlib.sha256(raw).hexdigest()
def require(value,reason):
    if not value: raise AssertionError(reason)
def pin_input(path):
    lock=json.loads((ROOT/'source-lock.json').read_text())
    require(path in lock,'Unlisted assembly input: '+path)
    require(sha((ROOT/path).read_bytes())==lock[path],'Current input pin mismatch: '+path)
def release_identity():
    release=json.loads((ROOT/'release.json').read_text())
    expected=json.loads((ROOT/'EXPECTED-OUTPUT.json').read_text())
    require(release['version']==expected['version'],'Current release mismatch')
    require(release['version'].startswith('0.20.12-rc'),'Unexpected release family')
    require(release['status']==expected['status']=='development-ui-preview-unqualified','Release grade overstated')
    require(release.get('publisherAuthenticated') is False and expected.get('publisherAuthenticated') is False,'Publisher incorrectly claimed authenticated')
    for f in ['build.py','src/page.html','src/style.css']:
        pin_input(f)
def archive_original_tests():
    d=ROOT/'fixtures/legacy-contracts-rc28'
    require(sha((d/'SHA256SUMS.json').read_bytes())=='59a90ef2b1f84248b83243c2b002db0fdd221f3c1c39b6d38a1652859da4e571','Historical manifest pin changed')
    hashes=json.loads((d/'SHA256SUMS.json').read_text())
    require(len(hashes)==8,'Historical archive size changed')
    for f,h in hashes.items():
        require(sha((d/f).read_bytes())==h,'Historical test overwritten: '+f)
def shared_wallet(soup):
    fingerprint=soup.select('#wallet-fingerprint-value')
    confirm=soup.select('#wallet-loaded')
    qr=soup.select('#seed-qr-display')
    actions=soup.select('.seed-qr-actions > button')
    words=soup.select('.seed-grid')
    require(all(len(v)==1 for v in [fingerprint,confirm,qr,actions,words]),'Duplicate or missing wallet surface')
    require(confirm[0].get('@click')=='confirmWalletLoaded()','Unapproved wallet confirmation path')
    require('wallet-compare-hint' in confirm[0].get('aria-describedby',''),'Fingerprint guidance missing from confirmation')
    require(actions[0].get('@click')=='seedQrExpanded = !seedQrExpanded','SeedQR action changed')
    require(actions[0].get('aria-controls')=='seed-qr-display','SeedQR target changed')
    require(not qr[0].select('button'),'QR quiet-zone violated')
    require(len(soup.select('[x-ref="seedQrCanvas"]'))==1,'SeedQR canvas changed')
def wallet_safety(soup):
    warning=soup.select_one('#wallet-safety')
    guidance=soup.select_one('#wallet-compare-hint')
    no_pass=soup.select_one('.premium-passphrase')
    require(warning is not None and 'Only use this disposable wallet' in warning.get_text(),'Disposable wallet safety removed')
    require(guidance is not None and 'Continue only if they match' in guidance.get_text(),'Fingerprint comparison missing')
    require(no_pass is not None and no_pass.get_text(strip=True)=='No passphrase','Passphrase warning missing')
    require('uses no passphrase' in soup.select_one('#wallet-technical-note').get_text(),'Technical passphrase caveat missing')
