"""Test-only, fail-closed RC34 CSS reversal to immutable RC28 witness.

Never imported by the application or build. All version steps must reconstruct
exactly; independent fixed hashes prevent mutable provenance records granting
arbitrary CSS edits. The actual stylesheet is not changed.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
SHA_RC28 = '9a2c9a385a9082c5915e7ea2b5d252b3ee11775f4d47fcf875c2f06301f9111f'
SHA_RC30 = 'cbcf6fef2e10877c16d3e7929d0e5ee95079083a4b5b7d9dec4f76923a2e3bfb'
SHA_RC32 = '442b6837a3ea39d467b804f801bfc8b23bdde5a6fc6758950a63159a16793f04'
SHA_RC33 = 'ef4ef4ed54cc0352da1b771e9a143ede22e11fea7b68b18927da65130d520d4c'
SHA_RC34 = '9c4ef0365efdcce75c0411f3aacaba410a882b62f921ad4082b5c6a10fcd2218'
SHA_HTML_RC34 = 'e77a04c6998ba5b19c86623ff1dd81aa712308e3e553ff894b3893409395bc23'


def digest(b):
    return hashlib.sha256(b).hexdigest()


def require(test, reason):
    if not test:
        raise AssertionError(reason)


def reviewed_rc28_css(current):
    """Validate current exact RC34 provenance; return independently pinned RC28 witness."""
    # Exact RC35 presentation-only suffix: preserve and independently pin every
    # historical RC34 byte before running all original provenance assertions.
    from rc35_style_pin import approved_rc35_css
    # RC36 requires a SHA-pinned current stylesheet and independently pinned RC35 witness.
    from rc35_style_pin import RC36_SHA
    if digest(current.encode())==RC36_SHA:
        current=approved_rc35_css(current).decode()
    elif "\n/* Narrow-header correction:" in current:
        from rc35_historical_pin import approved_rc35_css as old_approved
        current=old_approved(current).decode()
    suffix_marker='\n/* Signature Lab RC35:'
    if suffix_marker in current:
        from rc35_style_pin import BASE_SHA,DELTA_SHA
        prior_current,tail=current.split(suffix_marker,1)
        tail=suffix_marker+tail
        require(digest(prior_current.encode()) == BASE_SHA and
                digest(tail.encode()) == DELTA_SHA, 'Unreviewed RC35 stylesheet delta')
        current=prior_current
    require(digest(current.encode()) == SHA_RC34, 'Unreviewed RC34 stylesheet bytes')
    prior = (ROOT / 'fixtures/rc30-historical/style-rc28.css').read_bytes()
    require(digest(prior) == SHA_RC28, 'RC28 historical stylesheet tampered')
    rc30 = (ROOT / 'fixtures/rc32-historical/style-rc30.css').read_bytes()
    require(digest(rc30) == SHA_RC30, 'RC30 stylesheet witness tampered')
    r32 = json.loads((ROOT / 'fixtures/rc32-historical/rc32-css-provenance.json').read_text())
    require(r32['schema'] == 'tbw-reviewed-rc32-css-delta-v1' and
            r32['rc30Sha256'] == SHA_RC30 and r32['rc32Sha256'] == SHA_RC32 and
            len(r32['replacements']) == 2, 'Invalid RC32 provenance')
    derived = rc30
    for p in r32['replacements']:
        old, new = p['before'].encode(), p['after'].encode()
        require(old != new and derived.count(old) == 1, 'Ambiguous RC32 CSS reversal')
        derived = derived.replace(old, new)
    require(digest(derived) == SHA_RC32 and
            derived == (ROOT / 'fixtures/rc33-historical/rc32-style.css').read_bytes(),
            'RC32 CSS witness mismatch')
    r33 = json.loads((ROOT / 'fixtures/rc33-historical/rc33-css-provenance.json').read_text())
    require(r33['schema'] == 'rc33-reviewed-delta-v1' and
            r33['cssBaselineSha256'] == SHA_RC32 and r33['cssCurrentSha256'] == SHA_RC33,
            'Invalid RC33 provenance')
    anchor = (b"#test-view .sign-layout{display:grid!important;grid-template-columns:"
              b"minmax(0,1.55fr) minmax(320px,.93fr)!important;grid-template-areas:"
              b"'summary qr'!important;column-gap:16px!important;margin-top:17px!important;"
              b"align-items:start!important}")
    note = (b'\n/* RC33: Alpine x-show must win over the approved premium grid layout.\n'
            b'   When transactionReady/outputReview fails, never display stale signing information. */\n')
    rule = r33['cssSafetyRule'].encode()
    require(derived.count(anchor) == 1 and rule not in derived, 'RC33 safety rule placement changed')
    rc33 = derived.replace(anchor, anchor + note + rule)
    require(digest(rc33) == SHA_RC33, 'RC33 security CSS reconstruction failed')
    r34 = json.loads((ROOT / 'fixtures/rc36-historical/rc34-css-provenance.json').read_text())
    append = r34['exactAppend'].encode()
    require(r34['schema'] == 'tbw-reviewed-rc34-segmented-controls-v1' and
            r34['baselineSha256'] == SHA_RC33 and r34['currentSha256'] == SHA_RC34 and
            r34['approvedHtmlSha256'] == SHA_HTML_RC34 and
            digest(append) == r34['appendSha256'] and append not in rc33,
            'Invalid RC34 scoped CSS provenance')
    require(rc33 + append == current.encode(), 'Current CSS differs from reviewed RC34 derivation')
    return prior.decode()
