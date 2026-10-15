"""Test-only guarded historical source provenance. No current-app behavior claims."""
from pathlib import Path
import json,hashlib,base64,zlib
ROOT=Path(__file__).resolve().parents[1]
FIX=json.loads((ROOT/'fixtures/historical-source-bridge-v0204.json').read_text())['files']
def sha(b):return hashlib.sha256(b).hexdigest()
def project(name,text):
    r=FIX.get(name)
    if r is None:return text
    src=text.encode()
    if sha(src)!=r['currentSha256']:
        raise AssertionError('Unauthorized current source input in historical provenance projection: '+name)
    prev=zlib.decompress(base64.b64decode(r['priorB64Zlib']))
    if len(prev)!=r['priorBytes'] or sha(prev)!=r['priorSha256']:
        raise AssertionError('Corrupt archived historical source fixture: '+name)
    return prev.decode()
