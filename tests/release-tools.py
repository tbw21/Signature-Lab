#!/usr/bin/env python3
"""Local tool contracts using throwaway keys and locally fabricated vendor tarballs.
Passing these simulations DOES NOT authenticate the TBW release or upstream pako.
"""
from pathlib import Path
import tempfile,subprocess,json,tarfile,io,os,sys
root=Path(__file__).resolve().parents[1];results=[]
def check(v,msg='assertion failed'):
    if not v:raise AssertionError(msg)
def test(name,fn):
    try:fn();results.append({'name':name,'status':'passed'})
    except Exception as e:results.append({'name':name,'status':'failed','error':repr(e)})
with tempfile.TemporaryDirectory(prefix='tbw-auth-fixture-') as tmp:
    d=Path(tmp);home=d/'gnupg';home.mkdir(mode=0o700);env={**os.environ,'GNUPGHOME':str(home),'PYTHONDONTWRITEBYTECODE':'1'}
    def gpg(*args):return subprocess.run(['gpg','--batch',*args],env=env,capture_output=True,text=True,timeout=30)
    r=gpg('--pinentry-mode','loopback','--passphrase','','--quick-generate-key','TBW qualification fixture NOT publisher','ed25519','sign','0');check(r.returncode==0,r.stderr)
    fp=next(line.split(':')[9] for line in gpg('--with-colons','--list-keys').stdout.splitlines() if line.startswith('fpr:'))
    manifest=d/'SHA256SUMS';manifest.write_text('0'*64+'  fixture.html\n');sig=d/'manifest.asc'
    def auth(operation,fingerprint=fp,signature=sig):return subprocess.run([sys.executable,str(root/'tools/release_auth.py'),operation,str(manifest),'--fingerprint',fingerprint,'--signature',str(signature)],env=env,capture_output=True,text=True,timeout=30)
    test('operator signing tool signs with explicitly supplied throwaway test key',lambda:check(auth('sign').returncode==0))
    test('operator verification accepts the separately supplied test fingerprint',lambda:check(auth('verify').returncode==0))
    test('wrong trusted fingerprint is rejected despite a mathematically valid signature',lambda:check(auth('verify','F'*40).returncode!=0))
    test('existing detached signature cannot be overwritten',lambda:check(auth('sign').returncode!=0))
    def tamper():
        original=manifest.read_bytes();manifest.write_bytes(original+b'altered');check(auth('verify').returncode!=0);manifest.write_bytes(original)
    test('altered checksum manifest fails signature verification',tamper)
    test('missing signature is rejected',lambda:check(auth('verify',signature=d/'absent.asc').returncode!=0))
    test('short ambiguous signing-key IDs are rejected',lambda:check(auth('sign',fingerprint='ABCDEF12',signature=d/'other.asc').returncode!=0))
    local=(root/'vendor/pako-1.0.11.min.js').read_bytes()
    def vendor(mode):
        p=d/(mode+'.tgz')
        with tarfile.open(p,'w:gz') as z:
            i=tarfile.TarInfo('package/dist/pako.min.js');data=local if mode not in ('altered',) else local+b'X';i.size=len(data)
            if mode=='symlink':i.type=tarfile.SYMTYPE;i.linkname='/tmp/outside';i.size=0;z.addfile(i)
            else:
                z.addfile(i,io.BytesIO(data))
                if mode=='duplicate':z.addfile(i,io.BytesIO(data))
        r=subprocess.run([sys.executable,str(root/'tools/verify_vendor.py'),str(p)],capture_output=True,text=True,timeout=30)
        check((r.returncode==0)==(mode=='matching'),r.stderr)
    for mode in ['matching','altered','duplicate','symlink']:test('vendor comparator '+mode+' fabricated archive (not provenance proof)',lambda x=mode:vendor(x))
    gpgconf=subprocess.run(['gpgconf','--kill','gpg-agent'],env=env,capture_output=True,timeout=10)
r={'suite':'Release-authentication/vendor tool simulations','publisherAuthenticated':False,'upstreamBytesIndependentlyObtained':False,'passed':sum(x['status']=='passed' for x in results),'failed':sum(x['status']=='failed' for x in results),'results':results};Path(sys.argv[1]).write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2));sys.exit(1 if r['failed'] else 0)
