"""Fail-closed RC36 CSS pin; preserve exact pre-optimization RC35 provenance."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
RC36_SHA="f6ad6246153ffbf8eeffbca408a578e1dd2c4a3714446de375ca4d4c522d5f37"
RC35_SHA="2add29b1edd73854307e3aba021be193bf2463d5225610c7b2305f26ecf4a9bb"
from rc35_historical_pin import MARKER,BASE_SHA,DELTA_SHA
def approved_rc35_css(raw=None):
    if raw is None: raw=(ROOT/'src/style.css').read_bytes()
    if isinstance(raw,str):raw=raw.encode()
    if hashlib.sha256(raw).hexdigest()!=RC36_SHA:raise AssertionError('Unreviewed RC36 stylesheet bytes')
    witness=(ROOT/'fixtures/rc36-historical/rc35-audit-style.css').read_bytes()
    if hashlib.sha256(witness).hexdigest()!=RC35_SHA:raise AssertionError('RC35 historical CSS witness tampered')
    from rc35_historical_pin import approved_rc35_css as historical
    return historical(witness)
def pinned_historical_css():
    approved_rc35_css()
    from rc35_historical_pin import pinned_historical_css as historical
    return historical.__wrapped__() if hasattr(historical,'__wrapped__') else _historical_projection()
def _historical_projection():
    raw=approved_rc35_css()
    assert raw.count(MARKER)==1
    base,tail=raw.split(MARKER,1)
    sha=lambda b:hashlib.sha256(b).hexdigest()
    assert sha(base)==BASE_SHA and sha(MARKER+tail)==DELTA_SHA
    from audit_projection import project
    return project('src/style.css',base.decode())
