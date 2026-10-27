#!/usr/bin/env python3
"""Isolated RC16 source-lock/build failure cases; never alter the release source tree."""
from pathlib import Path
import tempfile,shutil,subprocess,sys,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(sys.argv[1]);OUT.parent.mkdir(parents=True,exist_ok=True)
def h(data):return hashlib.sha256(data).hexdigest()
def run(args,cwd):return subprocess.run(args,cwd=cwd,capture_output=True,text=True,timeout=20)
def fixture():
 t=tempfile.TemporaryDirectory();p=Path(t.name)
 locked=json.loads((ROOT/'source-lock.json').read_text())
 for rel in [*locked,'source-lock.json']:
  (p/rel).parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(ROOT/rel,p/rel)
 return t,p
outcome=[]
# All writes happen inside isolated temporary fixtures.
with tempfile.TemporaryDirectory() as tmp:
 base=Path(tmp)
 # Legitimate first build and explicit refusal to replace it.
 t,p=fixture()
 with t:
  target=base/'fresh.html'
  r=run([sys.executable,'build.py',str(target)],p)
  assert r.returncode==0 and target.exists(),r.stderr
  outcome.append('clean isolated source builds')
  r=run([sys.executable,'build.py',str(target)],p)
  assert r.returncode!=0 and 'Refusing to overwrite existing output' in r.stderr
  outcome.append('idempotent second output refused')
 # A source change without an updated lock must be terminal.
 t,p=fixture()
 with t:
  (p/'src/style.css').write_bytes((p/'src/style.css').read_bytes()+b'\n/* mutated fixture */')
  r=run([sys.executable,'build.py',str(base/'tampered.html')],p)
  assert r.returncode!=0 and 'Source lock mismatch' in r.stderr
  assert not (base/'tampered.html').exists()
  outcome.append('tampered CSS rejected by source lock')
 # A fixture with an updated lock still cannot lie about release authentication.
 t,p=fixture()
 with t:
  meta=json.loads((p/'release.json').read_text());meta.update(status='signed-release',publisherAuthenticated=False)
  (p/'release.json').write_text(json.dumps(meta))
  locked=json.loads((p/'source-lock.json').read_text());locked['release.json']=h((p/'release.json').read_bytes())
  (p/'source-lock.json').write_text(json.dumps(locked))
  r=run([sys.executable,'build.py',str(base/'false-signed.html')],p)
  assert r.returncode!=0 and 'Signed release needs explicit authentication evidence' in r.stderr
  outcome.append('unauthenticated signed release rejected')
 # Two writers contend on the same fresh path: one wins, one is rejected.
 t,p=fixture()
 with t:
  target=base/'concurrent.html'
  cmd=[sys.executable,'build.py',str(target)]
  a=subprocess.Popen(cmd,cwd=p,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  b=subprocess.Popen(cmd,cwd=p,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
  ao,ae=a.communicate(timeout=20);bo,be=b.communicate(timeout=20)
  assert sorted((a.returncode,b.returncode))==[0,1],(a.returncode,b.returncode,ae,be)
  assert target.is_file()
  outcome.append('concurrent writers allow one immutable output')
OUT.write_text(json.dumps({'status':'passed','tests':len(outcome),'checks':outcome,'scope':'isolated synthetic fixtures, no application source mutation'},indent=2)+'\n')
print(OUT.read_text())
