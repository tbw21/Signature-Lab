#!/usr/bin/env python3
"""Validate build status projection and fail-closed source integrity in an isolated copy."""
import sys, shutil, tempfile, json, subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT));import build
assert build.locked()==build.manifest()
assert build.help_contents((ROOT/'src/page.html').read_text()).count('help-topic')>=5
with tempfile.TemporaryDirectory(prefix='tbw-rc14-status-') as tmp:
    target=Path(tmp)/'source';shutil.copytree(ROOT,target,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    def rebuild(release):
        (target/'release.json').write_text(json.dumps(release))
        script=f'''import json,build;from pathlib import Path;Path('source-lock.json').write_text(json.dumps(build.manifest()));html,_=build.assemble();print('preview' if b'Development UI preview.' in html else 'candidate' if b'Release candidate undergoing qualification.' in html else 'signed' if b'Publisher authentication recorded' in html else 'unknown')'''
        return subprocess.run([sys.executable,'-c',script],cwd=target,capture_output=True,text=True)
    release=json.loads((ROOT/'release.json').read_text())
    p=rebuild(release);assert p.returncode==0 and p.stdout.strip()=='preview',(p.stdout,p.stderr)
    release['status']='release-candidate-unqualified';p=rebuild(release);assert p.returncode==0 and p.stdout.strip()=='candidate',(p.stdout,p.stderr)
    release['status']='signed-release';p=rebuild(release);assert p.returncode!=0 and 'Signed release needs explicit authentication evidence' in p.stderr,(p.stdout,p.stderr)
    release['status']='unrecognized';p=rebuild(release);assert p.returncode!=0 and 'Invalid release status' in p.stderr,(p.stdout,p.stderr)
    release['status']='development-ui-preview-unqualified';p=rebuild(release);assert p.returncode==0 and p.stdout.strip()=='preview',(p.stdout,p.stderr)
    # Mutation of locked source without an explicit new source lock is always refused.
    with (target/'src/page.html').open('a') as f:f.write('<!-- altered -->')
    p=subprocess.run([sys.executable,'-c','import build; build.assemble()'],cwd=target,capture_output=True,text=True)
    assert p.returncode!=0 and 'Source lock mismatch' in p.stderr,(p.stdout,p.stderr)
print(json.dumps({'status':'passed','checks':7,'scope':'isolated build status, unknown/rejected signed release and source lock tampering'}))
