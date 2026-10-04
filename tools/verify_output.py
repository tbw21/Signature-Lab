#!/usr/bin/env python3
"""Verify a rebuilt HTML against the frozen source package's public expected-output sidecar.
Uses only the standard library. Does not build, modify files, or authenticate the publisher.
"""
from pathlib import Path
import argparse, hashlib, json, re, sys
ROOT=Path(__file__).resolve().parents[1]
def verify(html,expected=ROOT/'EXPECTED-OUTPUT.json'):
    record=json.loads(Path(expected).read_text());data=Path(html).read_bytes()
    if record.get('schema')!='tbw-expected-output-v1':raise ValueError('Unsupported expected-output schema')
    if not re.fullmatch(r'[a-f0-9]{64}',record.get('sha256','')):raise ValueError('Invalid expected hash')
    if hashlib.sha256(data).hexdigest()!=record['sha256'] or len(data)!=record['bytes']:raise ValueError('Rebuilt HTML does not match the frozen expected output')
    marker=re.search(rb'const TBW_BUILD = Object.freeze\((\{[^\n]+\})\);',data)
    if not marker:raise ValueError('Build identity missing')
    build=json.loads(marker.group(1))
    if build.get('version')!=record['version'] or build.get('sourceSha256')!=record['sourceSha256']:raise ValueError('Embedded build identity mismatch')
    return {'verified':True,'sha256':record['sha256'],'bytes':len(data),'version':record['version'],
            'publisherAuthenticated':False,'scope':'Consistency with source-package sidecar, not authenticity.'}
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('html',type=Path)
    parser.add_argument('--expected',type=Path,default=ROOT/'EXPECTED-OUTPUT.json');args=parser.parse_args()
    try:print(json.dumps(verify(args.html,args.expected)));return 0
    except Exception as exc:print('OUTPUT VERIFICATION FAILED: '+str(exc),file=sys.stderr);return 1
if __name__=='__main__':raise SystemExit(main())
