#!/usr/bin/env python3
"""Compare an independently obtained pako 1.0.11 npm tarball with pinned vendor bytes.
This does not fetch files, execute package scripts, extract archives, or prove who
published the supplied tarball. Authenticate its origin/integrity separately.
"""
from pathlib import Path
import argparse,hashlib,json,tarfile,sys

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('tarball',type=Path);a=p.parse_args()
    if a.tarball.stat().st_size>10*1024*1024:raise ValueError('Oversized archive')
    with tarfile.open(a.tarball,'r:*') as archive:
        matches=[m for m in archive.getmembers() if m.name=='package/dist/pako.min.js']
        if len(matches)!=1 or not matches[0].isfile() or matches[0].size>1024*1024:raise ValueError('Invalid/duplicate pako vendor member')
        data=archive.extractfile(matches[0]).read(1024*1024+1)
    local=(Path(__file__).resolve().parents[1]/'vendor/pako-1.0.11.min.js').read_bytes()
    if data!=local:raise ValueError('Upstream member and pinned vendor bytes differ')
    print(json.dumps({'matchingBytes':True,'sha256':hashlib.sha256(local).hexdigest(),'publisherIdentityEstablished':False}))
if __name__=='__main__':
    try:main()
    except Exception as exc:print('VENDOR COMPARISON FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
