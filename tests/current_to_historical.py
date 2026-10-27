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
# Independently reviewed RC26 presentation hashes. This list is fixed in test code,
# not loaded from mutable source-lock.json or candidate metadata.
REVIEWED_RC26={
 'src/page.html':'5fb24284faa8822dfc53f40dd49107ce503698f4ceb5fbdb885afe8f2e5ef24b',
 'src/style.css':'221e33ad63e0f214c53b44d831d6bec490273bac4fe88e2b89ed5f6492206ce3',
 'src/20-application.js':'4ded7810831f8f841fdde9c9c3f3e94c808eb25605de995c53297c6ab8fcb26d',
}
# RC28 presentation/a11y contract migration, independently pinned to reviewed bytes.
# These pins do NOT authenticate publication, and historical fixtures remain immutable.
REVIEWED_RC28={'src/page.html': 'cc24ed0d0de48de6ba9d0e2d73888201a56acd6b4385b63e418fa04c55988425', 'src/style.css': '9a2c9a385a9082c5915e7ea2b5d252b3ee11775f4d47fcf875c2f06301f9111f', 'src/20-application.js': '4ded7810831f8f841fdde9c9c3f3e94c808eb25605de995c53297c6ab8fcb26d'}

# Exact RC30 scoped-removal identities, reviewed against the archived RC28 witnesses.
# Deliberately independent of mutable source-lock.json. Never accepts arbitrary edits.
REVIEWED_RC30={
 'src/page.html':'bc4323fe9ca8f9fc7fe69c885b4c9c912de4d34f207dabbe4f5affb43d1a67f4',
 'src/style.css':'cbcf6fef2e10877c16d3e7929d0e5ee95079083a4b5b7d9dec4f76923a2e3bfb',
 'src/20-application.js':'c3e4558e8b1d5afa1251691013abdfd1534a646dcd31ac2443c59dbe339fbe58',
}
RC30_WITNESSES={
 'src/page.html':'page-rc28.html',
 'src/style.css':'style-rc28.css',
 'src/20-application.js':'20-application-rc28.js',
}
def verify_rc30_witness(name):
    frozen=ROOT/'fixtures/rc30-historical'/RC30_WITNESSES[name]
    if sha(frozen.read_bytes())!=REVIEWED_RC28[name]:
        raise AssertionError('RC28 historical witness changed: '+name)
    if name=='src/20-application.js':
        p=json.loads((ROOT/'fixtures/rc30-historical/rc30-focus-provenance.json').read_text())
        if p['baselineSha256']!=REVIEWED_RC28[name] or p['currentSha256']!=REVIEWED_RC30[name]:
            raise AssertionError('RC30 application focus provenance changed')

def project(name,text):
    r=FIX.get(name)
    if r is None:return text
    src=text.encode()
    approved=json.loads((ROOT/'fixtures/current-ui-provenance.json').read_text())['files']
    if name in approved:
        if approved[name]['rc26Sha256']!=REVIEWED_RC26[name]:raise AssertionError('Historical RC26 pin changed: '+name)
        if sha(src)==REVIEWED_RC30.get(name):
            verify_rc30_witness(name)
        elif sha(src) not in {approved[name]['rc26Sha256'], REVIEWED_RC28.get(name)}:
            raise AssertionError('Unauthorized current source input in reviewed UI provenance: '+name)
        if approved[name]['archivedPriorSha256']!=r['priorSha256']:
            raise AssertionError('Archived historical pin changed: '+name)
    elif sha(src)!=r['currentSha256']:
        raise AssertionError('Unauthorized unreviewed historical projection: '+name)
    prev=zlib.decompress(base64.b64decode(r['priorB64Zlib']))
    if len(prev)!=r['priorBytes'] or sha(prev)!=r['priorSha256']:
        raise AssertionError('Corrupt archived historical source fixture: '+name)
    return prev.decode()
