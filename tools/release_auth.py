#!/usr/bin/env python3
"""Operator-owned release signing and verification. Never creates a publisher key.
Run outside the browser. Use a separately authenticated 40- or 64-hex fingerprint.
A public key bundled beside a download is NOT independent identity verification.
"""
from pathlib import Path
import argparse,re,subprocess,sys

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('operation',choices=['sign','verify']);p.add_argument('checksums',type=Path);p.add_argument('--fingerprint',required=True);p.add_argument('--signature',type=Path,required=True);a=p.parse_args()
    fingerprint=a.fingerprint.replace(' ','').upper()
    if not re.fullmatch(r'(?:[0-9A-F]{40}|[0-9A-F]{64})',fingerprint):raise ValueError('Supply the full independently authenticated fingerprint')
    if not a.checksums.is_file():raise ValueError('Checksum manifest missing')
    if a.operation=='sign':
        if a.signature.exists():raise ValueError('Refusing to overwrite signature')
        subprocess.run(['gpg','--batch','--local-user',fingerprint,'--armor','--detach-sign','--output',str(a.signature),'--',str(a.checksums)],check=True,timeout=120)
        print('Detached signature created using the operator-selected key. Publisher identity is not established by this script.')
    else:
        result=subprocess.run(['gpg','--batch','--status-fd','1','--verify',str(a.signature),str(a.checksums)],capture_output=True,text=True,timeout=30)
        if result.returncode:raise ValueError('Signature verification failed: '+result.stderr)
        valid=[line.split() for line in result.stdout.splitlines() if line.startswith('[GNUPG:] VALIDSIG ')]
        if not any(fingerprint in (row[2],row[-1]) for row in valid):raise ValueError('Signature does not match the independently trusted fingerprint')
        print('Signature valid for the supplied trusted fingerprint. Verify all manifest file hashes separately before opening.')
if __name__=='__main__':
    try:main()
    except Exception as exc:print('RELEASE AUTHENTICATION FAILED: '+str(exc),file=sys.stderr);sys.exit(1)
