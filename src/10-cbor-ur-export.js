/* src/10-cbor-ur-export.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
function S_(e) { let t = e.length, n; n = t < 24 ? [64 + t] : t < 256 ? [88, t] : t < 65536 ? [89, t >> 8, t & 255] : [90, t >>> 24 & 255, t >>> 16 & 255, t >>> 8 & 255, t & 255]; let r = new Uint8Array(n.length + t); return r.set(n, 0), r.set(e, n.length), r; }
function C_(e) { if (e.length === 0)
    throw Error(`Empty CBOR payload`); let t = e[0]; if (t >> 5 != 2)
    throw Error(`CBOR payload is not a byte string`); let n = t & 31, r = n < 24 ? 1 : n === 24 ? 2 : n === 25 ? 3 : n === 26 ? 5 : 1; if (e.length < r)
    throw Error(`Truncated CBOR length`); let i, a; if (n < 24)
    i = n, a = 1;
else if (n === 24)
    i = e[1], a = 2;
else if (n === 25)
    i = e[1] << 8 | e[2], a = 3;
else if (n === 26)
    i = e[1] * 16777216 + (e[2] << 16 | e[3] << 8 | e[4]), a = 5;
else
    throw Error(`Unsupported CBOR byte string length`); if (i > 524288)
    throw Error(`CBOR payload exceeds the size limit`); if (a + i !== e.length)
    throw Error(`Truncated CBOR byte string or trailing data`); return e.slice(a, a + i); }
function w_(e, t = 90) { let n = new x_.UR(Jp.Buffer.from(S_(e)), `crypto-psbt`), r = new x_.UREncoder(n, t), i = []; for (let e = 0; e < r.fragmentsLength; e++)
    i.push(r.nextPart()); return i; }
