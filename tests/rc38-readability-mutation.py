#!/usr/bin/env python3
"""Isolated negative tests for RC38 historical CSS and release-trust contracts.

All mutations occur in a private temp copy; no original source or HTML changes.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile

SRC=Path(__file__).resolve().parents[1]
HTML=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2]).resolve()
SHA=lambda x:hashlib.sha256(x).hexdigest()


def append_css(data): return data+b'\n/* unauthorized rules */\n'
def change_rc28(data): return data+b'\n/* altered archived witness */\n'
def change_rc32_review(data):
    r=json.loads(data);r['replacements'][0]['after']+=' /* forged */';return (json.dumps(r)+'\n').encode()
def change_rc33_review(data):
    r=json.loads(data);r['cssSafetyRule']+=' /* forged */';return (json.dumps(r)+'\n').encode()
def change_rc34_review(data):
    r=json.loads(data);r['exactAppend']+=' /* forged */';return (json.dumps(r)+'\n').encode()
def forge_version(data):
    r=json.loads(data);r['version']='0.20.12-rc99';return (json.dumps(r)+'\n').encode()
def publisher_fraud(data):
    r=json.loads(data);r['publisherAuthenticated']=True;return (json.dumps(r)+'\n').encode()
def hide_hardware_caveat(data):
    a=b'Physical signing-device and optical-scanning acceptance remain pending'
    assert data.count(a)==1
    return data.replace(a,b'Hardware acceptance complete')

CASES=[
 ('unreviewed-css','src/style.css',append_css,'R04'),
 ('tampered-rc28-witness','fixtures/rc30-historical/style-rc28.css',change_rc28,'R04'),
 ('forged-rc32-delta','fixtures/rc32-historical/rc32-css-provenance.json',change_rc32_review,'R04'),
 ('forged-rc33-safety','fixtures/rc33-historical/rc33-css-provenance.json',change_rc33_review,'R04'),
 ('forged-rc34-addition','fixtures/rc36-historical/rc34-css-provenance.json',change_rc34_review,'R04'),
 ('coordinated-version-fraud','release.json',forge_version,'R15'),
 ('publisher-claim-fraud','release.json',publisher_fraud,'R15'),
 ('missing-hardware-warning','src/page.html',hide_hardware_caveat,'R15')
]

def main():
    assert HTML.is_file()
    with tempfile.TemporaryDirectory(prefix='rc38-mutation-') as tmp:
        root=Path(tmp)/'source'
        shutil.copytree(SRC,root,symlinks=False)
        rows=[]
        for name,path,mutator,expected in CASES:
            p=root/path;before=p.read_bytes();after=mutator(before)
            assert after!=before
            try:
                p.write_bytes(after)
                receipt=Path(tmp)/(name+'.json')
                completed=subprocess.run([sys.executable,str(root/'tests/readability-static.py'),str(HTML),str(receipt)],capture_output=True,text=True,timeout=35,env={'PYTHONDONTWRITEBYTECODE':'1'})
                assert receipt.is_file(),name+': no receipt'
                result=json.loads(receipt.read_text())
                failed=[r['name'] for r in result['results'] if r['status']=='failed']
                ok=completed.returncode!=0 and any(x.startswith(expected+' ') for x in failed)
                rows.append({'case':name,'rejected':ok,'requiredFailedAssertion':expected,'actualFailures':failed,'mutationSha256':SHA(after)})
            finally:
                p.write_bytes(before)
        final={'schema':'rc38-readability-negative-v1','baseHtmlSha256':SHA(HTML.read_bytes()),'passed':sum(r['rejected'] for r in rows),'failed':sum(not r['rejected'] for r in rows),'tests':rows}
        OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(final,indent=2)+'\n')
        print(json.dumps({'passed':final['passed'],'failed':final['failed']}))
        return int(final['failed']!=0)

if __name__=='__main__':raise SystemExit(main())
