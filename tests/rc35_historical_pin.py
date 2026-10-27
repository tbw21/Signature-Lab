"""Exact, additive CSS presentation correction; never substitutes for runtime checks."""
from pathlib import Path
import hashlib
ROOT=Path(__file__).resolve().parents[1]
MARKER=b'\n/* Signature Lab RC35:'
BASE_SHA='9c4ef0365efdcce75c0411f3aacaba410a882b62f921ad4082b5c6a10fcd2218'
DELTA_SHA='37d333fece22fe22f96e10fcdb20403981c40abfee4c3e3e6cc1073a69f2bb23'
AUDIT_MARKER=b'\n/* Narrow-header correction:'
AUDIT_DELTA_SHA='a76e39d6af2ad63495738d0d6a31d803acc6b34bf65c48b5da2250375de578e6'
def approved_rc35_css(raw=None):
    if raw is None:raw=(ROOT/'src/style.css').read_bytes()
    if isinstance(raw,str):raw=raw.encode()
    if raw.count(AUDIT_MARKER)!=1:raise AssertionError('Missing/duplicate audit CSS correction')
    old,delta=raw.split(AUDIT_MARKER,1)
    if hashlib.sha256(AUDIT_MARKER+delta).hexdigest()!=AUDIT_DELTA_SHA:
        raise AssertionError('Unreviewed audit CSS suffix')
    return old
def pinned_historical_css():
    raw=approved_rc35_css()
    if raw.count(MARKER)!=1:raise AssertionError('Missing/duplicate approved narrow CSS correction')
    base,delta=raw.split(MARKER,1);delta=MARKER+delta
    sha=lambda b:hashlib.sha256(b).hexdigest()
    if sha(base)!=BASE_SHA or sha(delta)!=DELTA_SHA:raise AssertionError('CSS outside exact reviewed override changed')
    from audit_projection import project
    return project('src/style.css',base.decode())
