"""Test-only guarded historical source provenance. No current-app behavior claims."""
from pathlib import Path
import json,hashlib,base64,zlib
ROOT=Path(__file__).resolve().parents[1]
FIX=json.loads((ROOT/'fixtures/historical-source-bridge-v0204.json').read_text())['files']
def sha(b):return hashlib.sha256(b).hexdigest()
# Authorized RC3 release-label-only delta. The historical fixture remains immutable.
# Reverse *exact* approved substitutions before checking the historical dev page hash.
RC3_PAGE_REVERSE=(
    ('v@@VERSION@@ release candidate: hardware acceptance pending; not approved for public deployment',
     'v@@VERSION@@ development preview: hardware acceptance pending; not approved for public deployment'),
    ('title="Release candidate for disposable-wallet testing. Not approved for public deployment; hardware acceptance pending."',
     'title="Development preview. Not approved for public deployment; hardware acceptance pending."'),
    ('<span class="release-label">RC3</span>', '<span class="release-label">Preview</span>'),
    ('is a release candidate for disposable-wallet testing, not an approved public release.',
     'is a development preview, not an approved release.'),
)
def project(name,text):
    r=FIX.get(name)
    if r is None:return text
    src=text.encode()
    if sha(src)!=r['currentSha256']:
        if name=='src/page.html' and json.loads((ROOT/'release.json').read_text())['version']=='0.20.11-rc3':
            restored=text
            for new,old in RC3_PAGE_REVERSE:
                if restored.count(new)!=1:
                    raise AssertionError('Missing or duplicated RC3 release-label change: '+new)
                restored=restored.replace(new,old,1)
            if sha(restored.encode())!=r['currentSha256']:
                raise AssertionError('Unauthorized RC3 page change outside release identity')
        else:
            raise AssertionError('Unauthorized current source input in historical provenance projection: '+name)
    prev=zlib.decompress(base64.b64decode(r['priorB64Zlib']))
    if len(prev)!=r['priorBytes'] or sha(prev)!=r['priorSha256']:
        raise AssertionError('Corrupt archived historical source fixture: '+name)
    return prev.decode()
