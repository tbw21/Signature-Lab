/* src/18-form.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
var av = 4294967295;
var ov = 2147483647;
function sv(e) { let t = dp(e), n = t ? t.split(` `).length : 0; return n !== 12 && n !== 24 ? null : Ul(t, tm) ? t : null; }
function cv(e) { let t = /^([0-9a-fA-F]{64}):(\d+)$/.exec(e.trim()); if (!t)
    return null; let n = Number(t[2]); return !Number.isSafeInteger(n) || n > av ? null : { txid: t[1].toLowerCase(), vout: n }; }
function lv(e) { let t = e.trim(); if (!/^\d+$/.test(t))
    return null; let n = BigInt(t); return n < 1n || n > 2100000000000000n ? null : n; }
function uv(e) { let t = /^(\d+)[h']\/([01])\/(\d+)$/.exec(e.trim()); if (!t)
    return null; let n = Number(t[1]), r = Number(t[2]), i = Number(t[3]); return n > ov || i > ov ? null : { account: n, change: r, addressIndex: i }; }
function dv(e) { let t = e.trim(), n; if (/^0x[0-9a-fA-F]{1,8}$/.test(t))
    n = Number.parseInt(t.slice(2), 16);
else if (/^\d+$/.test(t))
    n = Number(t);
else
    return null; return !Number.isSafeInteger(n) || n > av ? null : n; }
function fv(e) { let t = e.trim(); if (!/^\d+$/.test(t))
    return null; let n = Number(t); return !Number.isSafeInteger(n) || n > av ? null : n; }
function pv(e) { let t = e.trim(); if (/^m\//i.test(t)) {
    let e = /^m\/84[h']\/0[h']\/(\d+)[h']\/([01])\/(\d+)$/.exec(t);
    if (!e)
        return null;
    let n = Number(e[1]), r = Number(e[2]), i = Number(e[3]);
    return n > ov || i > ov ? null : { kind: `change`, account: n, change: r, addressIndex: i };
} try {
    return yp(t), { kind: `address`, address: t };
}
catch {
    return null;
} }
function mv(e) { if (!e.trim())
    return `Enter a seed phrase`; let t = dp(e).split(` `); if (t.length !== 12 && t.length !== 24)
    return `Seed phrase must have 12 or 24 words (got ${t.length})`; let n = t.find(e => !tm.includes(e)); return n ? `"${n}" is not a BIP-39 word` : sv(e) ? null : `Invalid seed phrase (checksum mismatch)`; }
function hv(e) { return e.trim() ? fv(e) === null ? `nLockTime must be an integer between 0 and 4294967295` : null : `Enter an nLockTime (0 disables it)`; }
function gv(e, t = []) { if (!e.trim())
    return `Enter a UTXO id`; let n = cv(e); if (!n)
    return `Expected format: <64 hex chars>:<vout>`; let r = `${n.txid}:${n.vout}`; return t.includes(r) ? `Duplicate UTXO: already spent by another input` : null; }
function _v(e) { return e.trim() ? lv(e) === null ? `Amount must be a whole number of sats (at least 1)` : null : `Enter an amount in sats`; }
function vv(e) { return e.trim() ? uv(e) ? null : `Expected format: <account>h/<change>/<address_index> with change 0 or 1 (e.g. 0h/0/5)` : `Enter a derivation path suffix`; }
function yv(e) { return e.trim() ? dv(e) === null ? `nSequence must be an integer or 0x-hex up to 0xffffffff` : null : `Enter an nSequence`; }
function bv(e) { let t = e.trim(); return t ? pv(t) ? null : /^m\//i.test(t) ? `Unsupported derivation path: only BIP84 paths m/84h/0h/<account>h/<0|1>/<address_index> are supported` : `Invalid Bitcoin address` : `Enter an address or BIP84 derivation path`; }
function xv(e, t, n) { let r = _v(e); if (r)
    return r; if (t === null || n === null)
    return null; let i = n + lv(e); return i > t ? `Total outputs (${i} sats) exceed total inputs (${t} sats)` : null; }
var Sv = e => ({ value: e, error: null });
var Cv = 1;
var wv = 100000000n;
function Tv(e) { return e.toLocaleString(`en-US`); }
function Ev(e) { let t = e < 0n, n = t ? -e : e, r = n / wv, i = n % wv; return `${t ? `-` : ``}${r}.${i.toString().padStart(8, `0`)}`; }
function Dv(e, t) { return t === `sats` ? `${Tv(e)} sats` : `${Ev(e)} BTC`; }
function Ov() { let e = sm(); return { id: Cv++, utxoId: Sv(e.utxoId), amount: Sv(e.amount), pathSuffix: Sv(e.pathSuffix), sequence: Sv(e.sequence) }; }
function kv() { return cm().map(e => ({ id: Cv++, utxoId: Sv(e.utxoId), amount: Sv(e.amount), pathSuffix: Sv(e.pathSuffix), sequence: Sv(e.sequence) })); }
function Av(e) { return lm(e).map(e => ({ id: Cv++, amount: Sv(e.amount), dest: Sv(e.dest) })); }
function jv(e = [], t) { let n = bm(t ?? gm(e)); return { scenario: n.scenario, lockTime: Sv(String(n.lockTime)), inputs: n.inputs.map(e => ({ id: Cv++, utxoId: Sv(e.utxoId), amount: Sv(e.amount), pathSuffix: Sv(e.pathSuffix), sequence: Sv(e.sequence) })), outputs: n.outputs.map(e => ({ id: Cv++, amount: Sv(e.amount), dest: Sv(e.dest) })) }; }
function Mv(e, t, n) { return JSON.stringify([e.value, t.map(e => [e.utxoId.value, e.amount.value, e.pathSuffix.value, e.sequence.value]), n.map(e => [e.amount.value, e.dest.value])]); }
function Nv(e) { if (!e)
    return !0; try {
    let t = e.getContext(`2d`);
    return t ? (t.clearRect(0, 0, e.width, e.height), !0) : !1;
}
catch {
    return !1;
} }
