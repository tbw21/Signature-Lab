/* vendor/03-bitcoin-primitives.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
function da(e) { return e instanceof Uint8Array || ArrayBuffer.isView(e) && e.constructor.name === `Uint8Array` && `BYTES_PER_ELEMENT` in e && e.BYTES_PER_ELEMENT === 1; }
function fa(e) { if (!da(e))
    throw TypeError(`Uint8Array expected`); }
function pa(e, t) { return Array.isArray(t) ? t.length === 0 ? !0 : e ? t.every(e => typeof e == `string`) : t.every(e => Number.isSafeInteger(e)) : !1; }
function ma(e) { if (typeof e != `function`)
    throw TypeError(`function expected`); return !0; }
function ha(e, t) { if (typeof t != `string`)
    throw TypeError(`${e}: string expected`); return !0; }
function ga(e) { if (typeof e != `number`)
    throw TypeError(`number expected, got ${typeof e}`); if (!Number.isSafeInteger(e))
    throw RangeError(`invalid integer: ${e}`); }
function _a(e) { if (!Array.isArray(e))
    throw TypeError(`array expected`); }
function va(e, t) { if (!pa(!0, t))
    throw TypeError(`${e}: array of strings expected`); }
function ya(e, t) { if (!pa(!1, t))
    throw TypeError(`${e}: array of numbers expected`); }
function ba(...e) { let t = e => e, n = (e, t) => n => e(t(n)); return { encode: e.map(e => e.encode).reduceRight(n, t), decode: e.map(e => e.decode).reduce(n, t) }; }
function xa(e) { let t = typeof e == `string` ? e.split(``) : e, n = t.length; va(`alphabet`, t); let r = new Map(t.map((e, t) => [e, t])); return { encode: r => (_a(r), r.map(r => { if (!Number.isSafeInteger(r) || r < 0 || r >= n)
        throw Error(`alphabet.encode: digit index outside alphabet "${r}". Allowed: ${e}`); return t[r]; })), decode: t => (_a(t), t.map(t => { ha(`alphabet.decode`, t); let n = r.get(t); if (n === void 0)
        throw Error(`Unknown letter: "${t}". Allowed: ${e}`); return n; })) }; }
function Sa(e = ``) { return ha(`join`, e), { encode: t => (va(`join.decode`, t), t.join(e)), decode: t => (ha(`join.decode`, t), t.split(e)) }; }
function Ca(e, t = `=`) { return ga(e), ha(`padding`, t), { encode(n) { for (va(`padding.encode`, n); n.length * e % 8;)
        n.push(t); return n; }, decode(n) { va(`padding.decode`, n); let r = n.length; if (r * e % 8)
        throw Error(`padding: invalid, string should have whole number of bytes`); for (; r > 0 && n[r - 1] === t; r--)
        if ((r - 1) * e % 8 == 0)
            throw Error(`padding: invalid, string has too much padding`); return n.slice(0, r); } }; }
function wa(e) { return ma(e), { encode: e => e, decode: t => e(t) }; }
function Ta(e, t, n) { if (t < 2)
    throw RangeError(`convertRadix: invalid from=${t}, base cannot be less than 2`); if (n < 2)
    throw RangeError(`convertRadix: invalid to=${n}, base cannot be less than 2`); if (_a(e), !e.length)
    return []; let r = 0, i = [], a = Array.from(e, e => { if (ga(e), e < 0 || e >= t)
    throw Error(`invalid integer: ${e}`); return e; }), o = a.length; for (;;) {
    let e = 0, s = !0;
    for (let i = r; i < o; i++) {
        let o = a[i], c = t * e, l = c + o;
        if (!Number.isSafeInteger(l) || c / t !== e || l - o !== c)
            throw Error(`convertRadix: carry overflow`);
        let u = l / n;
        e = l % n;
        let d = Math.floor(u);
        if (a[i] = d, !Number.isSafeInteger(d) || d * n + e !== l)
            throw Error(`convertRadix: carry overflow`);
        if (s)
            d ? s = !1 : r = i;
        else
            continue;
    }
    if (i.push(e), s)
        break;
} for (let t = 0; t < e.length - 1 && e[t] === 0; t++)
    i.push(0); return i.reverse(); }
var Ea = (e, t) => t === 0 ? e : Ea(t, e % t);
var Da = (e, t) => e + (t - Ea(e, t));
var Oa = (() => { let e = []; for (let t = 0; t < 40; t++)
    e.push(2 ** t); return e; })();
function ka(e, t, n, r) { if (_a(e), t <= 0 || t > 32)
    throw RangeError(`convertRadix2: wrong from=${t}`); if (n <= 0 || n > 32)
    throw RangeError(`convertRadix2: wrong to=${n}`); if (Da(t, n) > 32)
    throw Error(`convertRadix2: carry overflow from=${t} to=${n} carryBits=${Da(t, n)}`); let i = 0, a = 0, o = Oa[t], s = Oa[n] - 1, c = []; for (let r of e) {
    if (ga(r), r >= o)
        throw Error(`convertRadix2: invalid data word=${r} from=${t}`);
    if (i = i << t | r, a + t > 32)
        throw Error(`convertRadix2: carry overflow pos=${a} from=${t}`);
    for (a += t; a >= n; a -= n)
        c.push((i >> a - n & s) >>> 0);
    let e = Oa[a];
    if (e === void 0)
        throw Error(`invalid carry`);
    i &= e - 1;
} if (i = i << n - a & s, !r && a >= t)
    throw Error(`Excess padding`); if (!r && i > 0)
    throw Error(`Non-zero padding: ${i}`); return r && a > 0 && c.push(i >>> 0), c; }
function Aa(e) { return ga(e), { encode: t => { if (!da(t))
        throw TypeError(`radix.encode input should be Uint8Array`); return Ta(Array.from(t), 256, e); }, decode: t => (ya(`radix.decode`, t), Uint8Array.from(Ta(t, e, 256))) }; }
function ja(e, t = !1) { if (ga(e), e <= 0 || e > 32)
    throw RangeError(`radix2: bits should be in (0..32]`); if (Da(8, e) > 32 || Da(e, 8) > 32)
    throw RangeError(`radix2: carry overflow`); return { encode: n => { if (!da(n))
        throw TypeError(`radix2.encode input should be Uint8Array`); return ka(Array.from(n), 8, e, !t); }, decode: n => (ya(`radix2.decode`, n), Uint8Array.from(ka(n, e, 8, t))) }; }
function Ma(e) { return ma(e), function (...t) { try {
    return e.apply(null, t);
}
catch { } }; }
function Na(e, t) { if (ga(e), e <= 0)
    throw RangeError(`checksum length must be positive: ${e}`); ma(t); let n = t; return { encode(t) { if (!da(t))
        throw TypeError(`checksum.encode: input should be Uint8Array`); let r = n(t).slice(0, e), i = new Uint8Array(t.length + e); return i.set(t), i.set(r, t.length), i; }, decode(t) { if (!da(t))
        throw TypeError(`checksum.decode: input should be Uint8Array`); let r = t.slice(0, -e), i = t.slice(-e), a = n(r).slice(0, e); for (let t = 0; t < e; t++)
        if (a[t] !== i[t])
            throw Error(`Invalid checksum`); return r; } }; }
var Pa = Object.freeze({ alphabet: xa, chain: ba, checksum: Na, convertRadix: Ta, convertRadix2: ka, radix: Aa, radix2: ja, join: Sa, padding: Ca });
ba(ja(4), xa(`0123456789ABCDEF`), Sa(``)), ba(ja(5), xa(`ABCDEFGHIJKLMNOPQRSTUVWXYZ234567`), Ca(5), Sa(``)), ba(ja(5), xa(`ABCDEFGHIJKLMNOPQRSTUVWXYZ234567`), Sa(``)), ba(ja(5), xa(`0123456789ABCDEFGHIJKLMNOPQRSTUV`), Ca(5), Sa(``)), ba(ja(5), xa(`0123456789ABCDEFGHIJKLMNOPQRSTUV`), Sa(``)), ba(ja(5), xa(`0123456789ABCDEFGHJKMNPQRSTVWXYZ`), Sa(``), wa(e => e.toUpperCase().replace(/O/g, `0`).replace(/[IL]/g, `1`)));
var Fa = typeof Uint8Array.from([]).toBase64 == `function` && typeof Uint8Array.fromBase64 == `function`;
var Ia = /[\t\n\f\r ]/;
var La = (e, t) => { ha(`base64`, e); let n = t ? `base64url` : `base64`; if (e.length > 0 && Ia.test(e))
    throw Error(`invalid base64`); return Uint8Array.fromBase64(e, { alphabet: n, lastChunkHandling: `strict` }); };
var Ra = Object.freeze(Fa ? { encode(e) { return fa(e), e.toBase64(); }, decode(e) { return La(e, !1); } } : ba(ja(6), xa(`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`), Ca(6), Sa(``)));
ba(ja(6), xa(`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/`), Sa(``)), Fa || ba(ja(6), xa(`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_`), Ca(6), Sa(``)), ba(ja(6), xa(`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_`), Sa(``));
var za = Object.freeze((e => ba(Aa(58), xa(e), Sa(``)))(`123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz`));
var Ba = e => { ma(e); let t = e; return ba(Na(4, e => t(t(e))), za); };
var Va = Ba;
var Ha = ba(xa(`qpzry9x8gf2tvdw0s3jn54khce6mua7l`), Sa(``));
var Ua = [996825010, 642813549, 513874426, 1027748829, 705979059];
function Wa(e) { let t = e >> 25, n = (e & 33554431) << 5; for (let e = 0; e < Ua.length; e++)
    (t >> e & 1) == 1 && (n ^= Ua[e]); return n; }
function Ga(e, t, n = 1) { let r = e.length, i = 1; for (let t = 0; t < r; t++) {
    let n = e.charCodeAt(t);
    if (n < 33 || n > 126)
        throw Error(`Invalid prefix (${e})`);
    i = Wa(i) ^ n >> 5;
} i = Wa(i); for (let t = 0; t < r; t++)
    i = Wa(i) ^ e.charCodeAt(t) & 31; for (let e of t)
    i = Wa(i) ^ e; for (let e = 0; e < 6; e++)
    i = Wa(i); return i ^= n, Ha.encode(ka([i % Oa[30]], 30, 5, !1)); }
function Ka(e) { let t = e === `bech32` ? 1 : 734539939, n = ja(5), r = n.decode, i = n.encode, a = Ma(r); function o(e, n, r = 90) { ha(`bech32.encode prefix`, e), da(n) && (n = Array.from(n)), ya(`bech32.encode`, n); let i = e.length; if (i === 0)
    throw TypeError(`Invalid prefix length ${i}`); let a = i + 7 + n.length; if (r !== !1 && a > r)
    throw TypeError(`Length ${a} exceeds limit ${r}`); let o = e.toLowerCase(), s = Ga(o, n, t); return `${o}1${Ha.encode(n)}${s}`; } function s(e, n = 90) { ha(`bech32.decode input`, e); let r = e.length; if (r < 8 || n !== !1 && r > n)
    throw TypeError(`invalid string length: ${r} (${e}). Expected (8..${n})`); let i = e.toLowerCase(); if (e !== i && e !== e.toUpperCase())
    throw Error(`String must be lowercase or uppercase`); let a = i.lastIndexOf(`1`); if (a === 0 || a === -1)
    throw Error(`Letter "1" must be present between prefix and data only`); let o = i.slice(0, a), s = i.slice(a + 1); if (s.length < 6)
    throw Error(`Data must be at least 6 characters long`); let c = Ha.decode(s).slice(0, -6), l = Ga(o, c, t); if (!s.endsWith(l))
    throw Error(`Invalid checksum in ${e}: expected "${l}"`); return { prefix: o, words: c }; } let c = Ma(s); function l(e) { let { prefix: t, words: n } = s(e, !1); return { prefix: t, words: n, bytes: r(n) }; } function u(e, t) { return o(e, i(t)); } return { encode: o, decode: s, encodeFromBytes: u, decodeToBytes: l, decodeUnsafe: c, fromWords: r, fromWordsUnsafe: a, toWords: i }; }
var qa = Object.freeze(Ka(`bech32`));
var Ja = Object.freeze(Ka(`bech32m`));
var Ya = typeof ``.isWellFormed == `function` ? e => e.isWellFormed() : e => { try {
    return encodeURI(e) !== null;
}
catch {
    return !1;
} };
var Xa = Object.freeze({ encode(e) { fa(e); let t = ``; for (let n = 0; n < e.length;) {
        let r = e[n++];
        if (r < 128) {
            t += String.fromCharCode(r);
            continue;
        }
        if (r < 194 || n >= e.length)
            throw TypeError(`invalid utf8 at byte ${n - 1}`);
        let i = e[n++];
        if ((i & 192) != 128)
            throw TypeError(`invalid utf8 at byte ${n - 1}`);
        let a = (r & 31) << 6 | i & 63;
        if (r >= 224) {
            if (n >= e.length)
                throw TypeError(`invalid utf8 at byte ${n - 1}`);
            let t = e[n++];
            if ((t & 192) != 128 || r === 224 && i < 160 || r === 237 && i >= 160)
                throw TypeError(`invalid utf8 at byte ${n - 1}`);
            if (a = (r & 15) << 12 | (i & 63) << 6 | t & 63, r >= 240) {
                if (n >= e.length)
                    throw TypeError(`invalid utf8 at byte ${n - 1}`);
                let o = e[n++];
                if (r > 244 || (o & 192) != 128 || r === 240 && i < 144 || r === 244 && i >= 144)
                    throw TypeError(`invalid utf8 at byte ${n - 1}`);
                a = (r & 7) << 18 | (i & 63) << 12 | (t & 63) << 6 | o & 63;
            }
        }
        a < 65536 ? t += String.fromCharCode(a) : (a -= 65536, t += String.fromCharCode((a >> 10) + 55296, (a & 1023) + 56320));
    } return t; }, decode(e) { if (ha(`utf8`, e), !Ya(e))
        throw TypeError(`utf8 expected well-formed string`); let t = new Uint8Array(e.length * 3), n = 0; for (let r = 0; r < e.length; r++) {
        let i = e.charCodeAt(r);
        if (i < 128) {
            t[n++] = i;
            continue;
        }
        if (i >= 55296 && i <= 57343) {
            let t = e.charCodeAt(++r);
            i = 65536 + (i - 55296 << 10) + t - 56320;
        }
        i >= 65536 ? (t[n++] = i >> 18 | 240, t[n++] = i >> 12 & 63 | 128) : i >= 2048 ? t[n++] = i >> 12 | 224 : t[n++] = i >> 6 | 192, i >= 2048 && (t[n++] = i >> 6 & 63 | 128), t[n++] = i & 63 | 128;
    } return t.subarray(0, n); } });
var Za = (() => { let e, t, n = { encode(e) { return fa(e), (t ||= new TextDecoder(`utf-8`, { ignoreBOM: !0, fatal: !0 })).decode(e); }, decode(t) { if (ha(`utf8`, t), !Ya(t))
        throw TypeError(`utf8 expected well-formed string`); return (e ||= new TextEncoder).encode(t); } }; return Object.freeze({ encode: typeof TextDecoder == `function` ? n.encode : Xa.encode, decode: typeof TextEncoder == `function` ? n.decode : Xa.decode }); })();
var Qa = typeof Uint8Array.from([]).toHex == `function` && typeof Uint8Array.fromHex == `function`;
var K = Object.freeze(Qa ? { encode(e) { return fa(e), e.toHex(); }, decode(e) { return ha(`hex`, e), Uint8Array.fromHex(e); } } : ba(ja(4), xa(`0123456789abcdef`), Sa(``), wa(e => { if (typeof e != `string` || e.length % 2 != 0)
    throw TypeError(`hex.decode: expected string, got ${typeof e} with length ${e.length}`); return e.toLowerCase(); })));
function $a(e) { return e instanceof Uint8Array || ArrayBuffer.isView(e) && e.constructor.name === `Uint8Array` && `BYTES_PER_ELEMENT` in e && e.BYTES_PER_ELEMENT === 1; }
function eo(e, t = ``) { if (typeof e != `number`) {
    let n = t && `"${t}" `;
    throw TypeError(`${n}expected number, got ${typeof e}`);
} if (!Number.isSafeInteger(e) || e < 0) {
    let n = t && `"${t}" `;
    throw RangeError(`${n}expected integer >= 0, got ${e}`);
} }
function to(e, t, n = ``) { let r = $a(e), i = e?.length, a = t !== void 0; if (!r || a && i !== t) {
    let o = n && `"${n}" `, s = a ? ` of length ${t}` : ``, c = r ? `length=${i}` : `type=${typeof e}`, l = o + `expected Uint8Array` + s + `, got ` + c;
    throw r ? RangeError(l) : TypeError(l);
} return e; }
function no(e) { if (typeof e != `function` || typeof e.create != `function`)
    throw TypeError(`Hash must wrapped by utils.createHasher`); if (eo(e.outputLen), eo(e.blockLen), e.outputLen < 1)
    throw Error(`"outputLen" must be >= 1`); if (e.blockLen < 1)
    throw Error(`"blockLen" must be >= 1`); }
function ro(e, t = !0) { if (e.destroyed)
    throw Error(`Hash instance has been destroyed`); if (t && e.finished)
    throw Error(`Hash#digest() has already been called`); }
function io(e, t) { to(e, void 0, `digestInto() output`); let n = t.outputLen; if (e.length < n)
    throw RangeError(`"digestInto() output" expected to be of length >=` + n); }
function ao(...e) { for (let t = 0; t < e.length; t++)
    e[t].fill(0); }
function oo(e) { return new DataView(e.buffer, e.byteOffset, e.byteLength); }
function so(e, t) { return e << 32 - t | e >>> t; }
function co(e, t) { return e << t | e >>> 32 - t >>> 0; }
var lo = typeof Uint8Array.from([]).toHex == `function` && typeof Uint8Array.fromHex == `function`;
var uo = Array.from({ length: 256 }, (e, t) => t.toString(16).padStart(2, `0`));
function fo(e) { if (to(e), lo)
    return e.toHex(); let t = ``; for (let n = 0; n < e.length; n++)
    t += uo[e[n]]; return t; }
var po = { _0: 48, _9: 57, A: 65, F: 70, a: 97, f: 102 };
function mo(e) { if (e >= po._0 && e <= po._9)
    return e - po._0; if (e >= po.A && e <= po.F)
    return e - (po.A - 10); if (e >= po.a && e <= po.f)
    return e - (po.a - 10); }
function ho(e) { if (typeof e != `string`)
    throw TypeError(`hex string expected, got ` + typeof e); if (lo)
    try {
        return Uint8Array.fromHex(e);
    }
    catch (e) {
        throw e instanceof SyntaxError ? RangeError(e.message) : e;
    } let t = e.length, n = t / 2; if (t % 2)
    throw RangeError(`hex string expected, got unpadded hex of length ` + t); let r = new Uint8Array(n); for (let t = 0, i = 0; t < n; t++, i += 2) {
    let n = mo(e.charCodeAt(i)), a = mo(e.charCodeAt(i + 1));
    if (n === void 0 || a === void 0) {
        let t = e[i] + e[i + 1];
        throw RangeError(`hex string expected, got non-hex character "` + t + `" at index ` + i);
    }
    r[t] = n * 16 + a;
} return r; }
function go(e) { if (typeof e != `string`)
    throw TypeError(`string expected`); return new Uint8Array(new TextEncoder().encode(e)); }
function _o(e, t = ``) { return typeof e == `string` ? go(e) : to(e, void 0, t); }
function vo(...e) { let t = 0; for (let n = 0; n < e.length; n++) {
    let r = e[n];
    to(r), t += r.length;
} let n = new Uint8Array(t); for (let t = 0, r = 0; t < e.length; t++) {
    let i = e[t];
    n.set(i, r), r += i.length;
} return n; }
function yo(e, t) { if (t !== void 0 && {}.toString.call(t) !== `[object Object]`)
    throw TypeError(`options must be object or undefined`); return Object.assign(e, t); }
function bo(e, t = {}) { let n = (t, n) => e(n).update(t).digest(), r = e(void 0); return n.outputLen = r.outputLen, n.blockLen = r.blockLen, n.canXOF = r.canXOF, n.create = t => e(t), Object.assign(n, t), Object.freeze(n); }
function xo(e = 32) { eo(e, `bytesLength`); let t = typeof globalThis == `object` ? globalThis.crypto : null; if (typeof t?.getRandomValues != `function`)
    throw Error(`crypto.getRandomValues must be defined`); if (e > 65536)
    throw RangeError(`"bytesLength" expected <= 65536, got ${e}`); return t.getRandomValues(new Uint8Array(e)); }
var So = e => ({ oid: Uint8Array.from([6, 9, 96, 134, 72, 1, 101, 3, 4, 2, e]) });
function Co(e, t, n) { return e & t ^ ~e & n; }
function wo(e, t, n) { return e & t ^ e & n ^ t & n; }
var To = class {
    blockLen;
    outputLen;
    canXOF = !1;
    padOffset;
    isLE;
    buffer;
    view;
    finished = !1;
    length = 0;
    pos = 0;
    destroyed = !1;
    constructor(e, t, n, r) { this.blockLen = e, this.outputLen = t, this.padOffset = n, this.isLE = r, this.buffer = new Uint8Array(e), this.view = oo(this.buffer); }
    update(e) { ro(this), to(e); let { view: t, buffer: n, blockLen: r } = this, i = e.length; for (let a = 0; a < i;) {
        let o = Math.min(r - this.pos, i - a);
        if (o === r) {
            let t = oo(e);
            for (; r <= i - a; a += r)
                this.process(t, a);
            continue;
        }
        n.set(e.subarray(a, a + o), this.pos), this.pos += o, a += o, this.pos === r && (this.process(t, 0), this.pos = 0);
    } return this.length += e.length, this.roundClean(), this; }
    digestInto(e) { ro(this), io(e, this), this.finished = !0; let { buffer: t, view: n, blockLen: r, isLE: i } = this, { pos: a } = this; t[a++] = 128, ao(this.buffer.subarray(a)), this.padOffset > r - a && (this.process(n, 0), a = 0); for (let e = a; e < r; e++)
        t[e] = 0; n.setBigUint64(r - 8, BigInt(this.length * 8), i), this.process(n, 0); let o = oo(e), s = this.outputLen; if (s % 4)
        throw Error(`_sha2: outputLen must be aligned to 32bit`); let c = s / 4, l = this.get(); if (c > l.length)
        throw Error(`_sha2: outputLen bigger than state`); for (let e = 0; e < c; e++)
        o.setUint32(4 * e, l[e], i); }
    digest() { let { buffer: e, outputLen: t } = this; this.digestInto(e); let n = e.slice(0, t); return this.destroy(), n; }
    _cloneInto(e) { e ||= new this.constructor, e.set(...this.get()); let { blockLen: t, buffer: n, length: r, finished: i, destroyed: a, pos: o } = this; return e.destroyed = a, e.finished = i, e.length = r, e.pos = o, r % t && e.buffer.set(n), e; }
    clone() { return this._cloneInto(); }
};
var Eo = Uint32Array.from([1779033703, 3144134277, 1013904242, 2773480762, 1359893119, 2600822924, 528734635, 1541459225]);
var Do = Uint32Array.from([1779033703, 4089235720, 3144134277, 2227873595, 1013904242, 4271175723, 2773480762, 1595750129, 1359893119, 2917565137, 2600822924, 725511199, 528734635, 4215389547, 1541459225, 327033209]);
var Oo = BigInt(2 ** 32 - 1);
var ko = BigInt(32);
function Ao(e, t = !1) { return t ? { h: Number(e & Oo), l: Number(e >> ko & Oo) } : { h: Number(e >> ko & Oo) | 0, l: Number(e & Oo) | 0 }; }
function jo(e, t = !1) { let n = e.length, r = new Uint32Array(n), i = new Uint32Array(n); for (let a = 0; a < n; a++) {
    let { h: n, l: o } = Ao(e[a], t);
    [r[a], i[a]] = [n, o];
} return [r, i]; }
var Mo = (e, t, n) => e >>> n;
var No = (e, t, n) => e << 32 - n | t >>> n;
var Po = (e, t, n) => e >>> n | t << 32 - n;
var Fo = (e, t, n) => e << 32 - n | t >>> n;
var Io = (e, t, n) => e << 64 - n | t >>> n - 32;
var Lo = (e, t, n) => e >>> n - 32 | t << 64 - n;
function Ro(e, t, n, r) { let i = (t >>> 0) + (r >>> 0); return { h: e + n + (i / 2 ** 32 | 0) | 0, l: i | 0 }; }
var zo = (e, t, n) => (e >>> 0) + (t >>> 0) + (n >>> 0);
var Bo = (e, t, n, r) => t + n + r + (e / 2 ** 32 | 0) | 0;
var Vo = (e, t, n, r) => (e >>> 0) + (t >>> 0) + (n >>> 0) + (r >>> 0);
var Ho = (e, t, n, r, i) => t + n + r + i + (e / 2 ** 32 | 0) | 0;
var Uo = (e, t, n, r, i) => (e >>> 0) + (t >>> 0) + (n >>> 0) + (r >>> 0) + (i >>> 0);
var Wo = (e, t, n, r, i, a) => t + n + r + i + a + (e / 2 ** 32 | 0) | 0;
var Go = Uint32Array.from([1116352408, 1899447441, 3049323471, 3921009573, 961987163, 1508970993, 2453635748, 2870763221, 3624381080, 310598401, 607225278, 1426881987, 1925078388, 2162078206, 2614888103, 3248222580, 3835390401, 4022224774, 264347078, 604807628, 770255983, 1249150122, 1555081692, 1996064986, 2554220882, 2821834349, 2952996808, 3210313671, 3336571891, 3584528711, 113926993, 338241895, 666307205, 773529912, 1294757372, 1396182291, 1695183700, 1986661051, 2177026350, 2456956037, 2730485921, 2820302411, 3259730800, 3345764771, 3516065817, 3600352804, 4094571909, 275423344, 430227734, 506948616, 659060556, 883997877, 958139571, 1322822218, 1537002063, 1747873779, 1955562222, 2024104815, 2227730452, 2361852424, 2428436474, 2756734187, 3204031479, 3329325298]);
var Ko = new Uint32Array(64);
var qo = class extends To {
    constructor(e) { super(64, e, 8, !1); }
    get() { let { A: e, B: t, C: n, D: r, E: i, F: a, G: o, H: s } = this; return [e, t, n, r, i, a, o, s]; }
    set(e, t, n, r, i, a, o, s) { this.A = e | 0, this.B = t | 0, this.C = n | 0, this.D = r | 0, this.E = i | 0, this.F = a | 0, this.G = o | 0, this.H = s | 0; }
    process(e, t) { for (let n = 0; n < 16; n++, t += 4)
        Ko[n] = e.getUint32(t, !1); for (let e = 16; e < 64; e++) {
        let t = Ko[e - 15], n = Ko[e - 2], r = so(t, 7) ^ so(t, 18) ^ t >>> 3, i = so(n, 17) ^ so(n, 19) ^ n >>> 10;
        Ko[e] = i + Ko[e - 7] + r + Ko[e - 16] | 0;
    } let { A: n, B: r, C: i, D: a, E: o, F: s, G: c, H: l } = this; for (let e = 0; e < 64; e++) {
        let t = so(o, 6) ^ so(o, 11) ^ so(o, 25), u = l + t + Co(o, s, c) + Go[e] + Ko[e] | 0, d = (so(n, 2) ^ so(n, 13) ^ so(n, 22)) + wo(n, r, i) | 0;
        l = c, c = s, s = o, o = a + u | 0, a = i, i = r, r = n, n = u + d | 0;
    } n = n + this.A | 0, r = r + this.B | 0, i = i + this.C | 0, a = a + this.D | 0, o = o + this.E | 0, s = s + this.F | 0, c = c + this.G | 0, l = l + this.H | 0, this.set(n, r, i, a, o, s, c, l); }
    roundClean() { ao(Ko); }
    destroy() { this.destroyed = !0, this.set(0, 0, 0, 0, 0, 0, 0, 0), ao(this.buffer); }
};
var Jo = class extends qo {
    A = Eo[0] | 0;
    B = Eo[1] | 0;
    C = Eo[2] | 0;
    D = Eo[3] | 0;
    E = Eo[4] | 0;
    F = Eo[5] | 0;
    G = Eo[6] | 0;
    H = Eo[7] | 0;
    constructor() { super(32); }
};
var Yo = jo(`0x428a2f98d728ae22.0x7137449123ef65cd.0xb5c0fbcfec4d3b2f.0xe9b5dba58189dbbc.0x3956c25bf348b538.0x59f111f1b605d019.0x923f82a4af194f9b.0xab1c5ed5da6d8118.0xd807aa98a3030242.0x12835b0145706fbe.0x243185be4ee4b28c.0x550c7dc3d5ffb4e2.0x72be5d74f27b896f.0x80deb1fe3b1696b1.0x9bdc06a725c71235.0xc19bf174cf692694.0xe49b69c19ef14ad2.0xefbe4786384f25e3.0x0fc19dc68b8cd5b5.0x240ca1cc77ac9c65.0x2de92c6f592b0275.0x4a7484aa6ea6e483.0x5cb0a9dcbd41fbd4.0x76f988da831153b5.0x983e5152ee66dfab.0xa831c66d2db43210.0xb00327c898fb213f.0xbf597fc7beef0ee4.0xc6e00bf33da88fc2.0xd5a79147930aa725.0x06ca6351e003826f.0x142929670a0e6e70.0x27b70a8546d22ffc.0x2e1b21385c26c926.0x4d2c6dfc5ac42aed.0x53380d139d95b3df.0x650a73548baf63de.0x766a0abb3c77b2a8.0x81c2c92e47edaee6.0x92722c851482353b.0xa2bfe8a14cf10364.0xa81a664bbc423001.0xc24b8b70d0f89791.0xc76c51a30654be30.0xd192e819d6ef5218.0xd69906245565a910.0xf40e35855771202a.0x106aa07032bbd1b8.0x19a4c116b8d2d0c8.0x1e376c085141ab53.0x2748774cdf8eeb99.0x34b0bcb5e19b48a8.0x391c0cb3c5c95a63.0x4ed8aa4ae3418acb.0x5b9cca4f7763e373.0x682e6ff3d6b2b8a3.0x748f82ee5defb2fc.0x78a5636f43172f60.0x84c87814a1f0ab72.0x8cc702081a6439ec.0x90befffa23631e28.0xa4506cebde82bde9.0xbef9a3f7b2c67915.0xc67178f2e372532b.0xca273eceea26619c.0xd186b8c721c0c207.0xeada7dd6cde0eb1e.0xf57d4f7fee6ed178.0x06f067aa72176fba.0x0a637dc5a2c898a6.0x113f9804bef90dae.0x1b710b35131c471b.0x28db77f523047d84.0x32caab7b40c72493.0x3c9ebe0a15c9bebc.0x431d67c49c100d4c.0x4cc5d4becb3e42b6.0x597f299cfc657e2a.0x5fcb6fab3ad6faec.0x6c44198c4a475817`.split(`.`).map(e => BigInt(e)));
var Xo = Yo[0];
var Zo = Yo[1];
var Qo = new Uint32Array(80);
var $o = new Uint32Array(80);
var es = class extends To {
    constructor(e) { super(128, e, 16, !1); }
    get() { let { Ah: e, Al: t, Bh: n, Bl: r, Ch: i, Cl: a, Dh: o, Dl: s, Eh: c, El: l, Fh: u, Fl: d, Gh: f, Gl: p, Hh: m, Hl: h } = this; return [e, t, n, r, i, a, o, s, c, l, u, d, f, p, m, h]; }
    set(e, t, n, r, i, a, o, s, c, l, u, d, f, p, m, h) { this.Ah = e | 0, this.Al = t | 0, this.Bh = n | 0, this.Bl = r | 0, this.Ch = i | 0, this.Cl = a | 0, this.Dh = o | 0, this.Dl = s | 0, this.Eh = c | 0, this.El = l | 0, this.Fh = u | 0, this.Fl = d | 0, this.Gh = f | 0, this.Gl = p | 0, this.Hh = m | 0, this.Hl = h | 0; }
    process(e, t) { for (let n = 0; n < 16; n++, t += 4)
        Qo[n] = e.getUint32(t), $o[n] = e.getUint32(t += 4); for (let e = 16; e < 80; e++) {
        let t = Qo[e - 15] | 0, n = $o[e - 15] | 0, r = Po(t, n, 1) ^ Po(t, n, 8) ^ Mo(t, n, 7), i = Fo(t, n, 1) ^ Fo(t, n, 8) ^ No(t, n, 7), a = Qo[e - 2] | 0, o = $o[e - 2] | 0, s = Po(a, o, 19) ^ Io(a, o, 61) ^ Mo(a, o, 6), c = Vo(i, Fo(a, o, 19) ^ Lo(a, o, 61) ^ No(a, o, 6), $o[e - 7], $o[e - 16]), l = Ho(c, r, s, Qo[e - 7], Qo[e - 16]);
        Qo[e] = l | 0, $o[e] = c | 0;
    } let { Ah: n, Al: r, Bh: i, Bl: a, Ch: o, Cl: s, Dh: c, Dl: l, Eh: u, El: d, Fh: f, Fl: p, Gh: m, Gl: h, Hh: g, Hl: _ } = this; for (let e = 0; e < 80; e++) {
        let t = Po(u, d, 14) ^ Po(u, d, 18) ^ Io(u, d, 41), v = Fo(u, d, 14) ^ Fo(u, d, 18) ^ Lo(u, d, 41), y = u & f ^ ~u & m, b = d & p ^ ~d & h, x = Uo(_, v, b, Zo[e], $o[e]), S = Wo(x, g, t, y, Xo[e], Qo[e]), C = x | 0, w = Po(n, r, 28) ^ Io(n, r, 34) ^ Io(n, r, 39), T = Fo(n, r, 28) ^ Lo(n, r, 34) ^ Lo(n, r, 39), E = n & i ^ n & o ^ i & o, D = r & a ^ r & s ^ a & s;
        g = m | 0, _ = h | 0, m = f | 0, h = p | 0, f = u | 0, p = d | 0, { h: u, l: d } = Ro(c | 0, l | 0, S | 0, C | 0), c = o | 0, l = s | 0, o = i | 0, s = a | 0, i = n | 0, a = r | 0;
        let O = zo(C, T, D);
        n = Bo(O, S, w, E), r = O | 0;
    } ({ h: n, l: r } = Ro(this.Ah | 0, this.Al | 0, n | 0, r | 0)), { h: i, l: a } = Ro(this.Bh | 0, this.Bl | 0, i | 0, a | 0), { h: o, l: s } = Ro(this.Ch | 0, this.Cl | 0, o | 0, s | 0), { h: c, l } = Ro(this.Dh | 0, this.Dl | 0, c | 0, l | 0), { h: u, l: d } = Ro(this.Eh | 0, this.El | 0, u | 0, d | 0), { h: f, l: p } = Ro(this.Fh | 0, this.Fl | 0, f | 0, p | 0), { h: m, l: h } = Ro(this.Gh | 0, this.Gl | 0, m | 0, h | 0), { h: g, l: _ } = Ro(this.Hh | 0, this.Hl | 0, g | 0, _ | 0), this.set(n, r, i, a, o, s, c, l, u, d, f, p, m, h, g, _); }
    roundClean() { ao(Qo, $o); }
    destroy() { this.destroyed = !0, ao(this.buffer), this.set(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0); }
};
var ts = class extends es {
    Ah = Do[0] | 0;
    Al = Do[1] | 0;
    Bh = Do[2] | 0;
    Bl = Do[3] | 0;
    Ch = Do[4] | 0;
    Cl = Do[5] | 0;
    Dh = Do[6] | 0;
    Dl = Do[7] | 0;
    Eh = Do[8] | 0;
    El = Do[9] | 0;
    Fh = Do[10] | 0;
    Fl = Do[11] | 0;
    Gh = Do[12] | 0;
    Gl = Do[13] | 0;
    Hh = Do[14] | 0;
    Hl = Do[15] | 0;
    constructor() { super(64); }
};
var ns = bo(() => new Jo, So(1));
var rs = bo(() => new ts, So(3));
var q = (e, t, n) => to(e, t, n);
var is = eo;
var as = fo;
var os = (...e) => vo(...e);
var ss = e => ho(e);
var cs = $a;
var ls = e => xo(e);
var us = BigInt(0);
var ds = BigInt(1);
function fs(e, t = ``) { if (typeof e != `boolean`) {
    let n = t && `"${t}" `;
    throw TypeError(n + `expected boolean, got type=` + typeof e);
} return e; }
function ps(e) { if (typeof e == `bigint`) {
    if (!Cs(e))
        throw RangeError(`positive bigint expected, got ` + e);
}
else
    is(e); return e; }
function ms(e, t = ``) { if (typeof e != `number`) {
    let n = t && `"${t}" `;
    throw TypeError(n + `expected number, got type=` + typeof e);
} if (!Number.isSafeInteger(e)) {
    let n = t && `"${t}" `;
    throw RangeError(n + `expected safe integer, got ` + e);
} }
function hs(e) { let t = ps(e).toString(16); return t.length & 1 ? `0` + t : t; }
function gs(e) { if (typeof e != `string`)
    throw TypeError(`hex string expected, got ` + typeof e); return e === `` ? us : BigInt(`0x` + e); }
function _s(e) { return gs(fo(e)); }
function vs(e) { return gs(fo(xs(to(e)).reverse())); }
function ys(e, t) { if (eo(t), t === 0)
    throw RangeError(`zero length`); e = ps(e); let n = e.toString(16); if (n.length > t * 2)
    throw RangeError(`number too large`); return ho(n.padStart(t * 2, `0`)); }
function bs(e, t) { return ys(e, t).reverse(); }
function xs(e) { return Uint8Array.from(q(e)); }
function Ss(e) { if (typeof e != `string`)
    throw TypeError(`ascii string expected, got ` + typeof e); return Uint8Array.from(e, (t, n) => { let r = t.charCodeAt(0); if (t.length !== 1 || r > 127)
    throw RangeError(`string contains non-ASCII character "${e[n]}" with code ${r} at position ${n}`); return r; }); }
var Cs = e => typeof e == `bigint` && us <= e;
function ws(e, t, n) { return Cs(e) && Cs(t) && Cs(n) && t <= e && e < n; }
function Ts(e, t, n, r) { if (!ws(t, n, r))
    throw RangeError(`expected valid ` + e + `: ` + n + ` <= n < ` + r + `, got ` + t); }
function Es(e) { if (e < us)
    throw Error(`expected non-negative bigint, got ` + e); let t; for (t = 0; e > us; e >>= ds, t += 1)
    ; return t; }
var Ds = e => (ds << BigInt(e)) - ds;
function Os(e, t, n) { if (eo(e, `hashLen`), eo(t, `qByteLen`), typeof n != `function`)
    throw TypeError(`hmacFn must be a function`); let r = e => new Uint8Array(e), i = Uint8Array.of(), a = Uint8Array.of(0), o = Uint8Array.of(1), s = r(e), c = r(e), l = 0, u = () => { s.fill(1), c.fill(0), l = 0; }, d = (...e) => n(c, os(s, ...e)), f = (e = i) => { c = d(a, e), s = d(), e.length !== 0 && (c = d(o, e), s = d()); }, p = () => { if (l++ >= 1e3)
    throw Error(`drbg: tried max amount of iterations`); let e = 0, n = []; for (; e < t;) {
    s = d();
    let t = s.slice();
    n.push(t), e += s.length;
} return os(...n); }; return (e, t) => { u(), f(e); let n; for (; (n = t(p())) === void 0;)
    f(); return u(), n; }; }
function ks(e, t = {}, n = {}) { if (Object.prototype.toString.call(e) !== `[object Object]`)
    throw TypeError(`expected valid options object`); function r(t, n, r) { if (!r && n !== `function` && !Object.hasOwn(e, t))
    throw TypeError(`param "${t}" is invalid: expected own property`); let i = e[t]; if (r && i === void 0)
    return; let a = typeof i; if (a !== n || i === null)
    throw TypeError(`param "${t}" is invalid: expected ${n}, got ${a}`); } let i = (e, t) => Object.entries(e).forEach(([e, n]) => r(e, n, t)); i(t, !1), i(n, !0); }
var As = BigInt(0);
var js = BigInt(1);
var Ms = BigInt(2);
var Ns = BigInt(3);
var Ps = BigInt(4);
var Fs = BigInt(5);
var Is = BigInt(7);
var Ls = BigInt(8);
var Rs = BigInt(9);
var zs = BigInt(16);
function Bs(e, t) { if (t <= As)
    throw Error(`mod: expected positive modulus, got ` + t); let n = e % t; return n >= As ? n : t + n; }
function Vs(e, t, n) { if (t < As)
    throw Error(`pow2: expected non-negative exponent, got ` + t); let r = e; for (; t-- > As;)
    r *= r, r %= n; return r; }
function Hs(e, t) { if (e === As)
    throw Error(`invert: expected non-zero number`); if (t <= As)
    throw Error(`invert: expected positive modulus, got ` + t); let n = Bs(e, t), r = t, i = As, a = js, o = js, s = As; for (; n !== As;) {
    let e = r / n, t = r - n * e, c = i - o * e, l = a - s * e;
    r = n, n = t, i = o, a = s, o = c, s = l;
} if (r !== js)
    throw Error(`invert: does not exist`); return Bs(i, t); }
function Us(e, t, n) { let r = e; if (!r.eql(r.sqr(t), n))
    throw Error(`Cannot find square root`); }
function Ws(e, t) { let n = e, r = (n.ORDER + js) / Ps, i = n.pow(t, r); return Us(n, i, t), i; }
function Gs(e, t) { let n = e, r = (n.ORDER - Fs) / Ls, i = n.mul(t, Ms), a = n.pow(i, r), o = n.mul(t, a), s = n.mul(n.mul(o, Ms), a), c = n.mul(o, n.sub(s, n.ONE)); return Us(n, c, t), c; }
function Ks(e) { let t = rc(e), n = qs(e), r = n(t, t.neg(t.ONE)), i = n(t, r), a = n(t, t.neg(r)), o = (e + Is) / zs; return ((e, t) => { let n = e, s = n.pow(t, o), c = n.mul(s, r), l = n.mul(s, i), u = n.mul(s, a), d = n.eql(n.sqr(c), t), f = n.eql(n.sqr(l), t); s = n.cmov(s, c, d), c = n.cmov(u, l, f); let p = n.eql(n.sqr(c), t), m = n.cmov(s, c, p); return Us(n, m, t), m; }); }
function qs(e) { if (e < Ns)
    throw Error(`sqrt is not defined for small field`); let t = e - js, n = 0; for (; t % Ms === As;)
    t /= Ms, n++; let r = Ms, i = rc(e); for (; $s(i, r) === 1;)
    if (r++ > 1e3)
        throw Error(`Cannot find square root: probably non-prime P`); if (n === 1)
    return Ws; let a = i.pow(r, t), o = (t + js) / Ms; return function (e, r) { let i = e; if (i.is0(r))
    return r; if ($s(i, r) !== 1)
    throw Error(`Cannot find square root`); let s = n, c = i.mul(i.ONE, a), l = i.pow(r, t), u = i.pow(r, o); for (; !i.eql(l, i.ONE);) {
    if (i.is0(l))
        return i.ZERO;
    let e = 1, t = i.sqr(l);
    for (; !i.eql(t, i.ONE);)
        if (e++, t = i.sqr(t), e === s)
            throw Error(`Cannot find square root`);
    let n = js << BigInt(s - e - 1), r = i.pow(c, n);
    s = e, c = i.sqr(r), l = i.mul(l, c), u = i.mul(u, r);
} return u; }; }
function Js(e) { return e % Ps === Ns ? Ws : e % Ls === Fs ? Gs : e % zs === Rs ? Ks(e) : qs(e); }
var Ys = [`create`, `isValid`, `is0`, `neg`, `inv`, `sqrt`, `sqr`, `eql`, `add`, `sub`, `mul`, `pow`, `div`, `addN`, `subN`, `mulN`, `sqrN`];
function Xs(e) { if (ks(e, Ys.reduce((e, t) => (e[t] = `function`, e), { ORDER: `bigint`, BYTES: `number`, BITS: `number` })), ms(e.BYTES, `BYTES`), ms(e.BITS, `BITS`), e.BYTES < 1 || e.BITS < 1)
    throw Error(`invalid field: expected BYTES/BITS > 0`); if (e.ORDER <= js)
    throw Error(`invalid field: expected ORDER > 1, got ` + e.ORDER); return e; }
function Zs(e, t, n) { let r = e; if (n < As)
    throw Error(`invalid exponent, negatives unsupported`); if (n === As)
    return r.ONE; if (n === js)
    return t; let i = r.ONE, a = t; for (; n > As;)
    n & js && (i = r.mul(i, a)), a = r.sqr(a), n >>= js; return i; }
function Qs(e, t, n = !1) { let r = e, i = Array(t.length).fill(n ? r.ZERO : void 0), a = t.reduce((e, t, n) => r.is0(t) ? e : (i[n] = e, r.mul(e, t)), r.ONE), o = r.inv(a); return t.reduceRight((e, t, n) => r.is0(t) ? e : (i[n] = r.mul(e, i[n]), r.mul(e, t)), o), i; }
function $s(e, t) { let n = e, r = (n.ORDER - js) / Ms, i = n.pow(t, r), a = n.eql(i, n.ONE), o = n.eql(i, n.ZERO), s = n.eql(i, n.neg(n.ONE)); if (!a && !o && !s)
    throw Error(`invalid Legendre symbol result`); return a ? 1 : o ? 0 : -1; }
function ec(e, t) { if (t !== void 0 && is(t), e <= As)
    throw Error(`invalid n length: expected positive n, got ` + e); if (t !== void 0 && t < 1)
    throw Error(`invalid n length: expected positive bit length, got ` + t); let n = Es(e); if (t !== void 0 && t < n)
    throw Error(`invalid n length: expected bit length (${n}) >= n.length (${t})`); let r = t === void 0 ? n : t; return { nBitLength: r, nByteLength: Math.ceil(r / 8) }; }
var tc = new WeakMap;
var nc = class {
    ORDER;
    BITS;
    BYTES;
    isLE;
    ZERO = As;
    ONE = js;
    _lengths;
    _mod;
    constructor(e, t = {}) { if (e <= js)
        throw Error(`invalid field: expected ORDER > 1, got ` + e); let n; this.isLE = !1, typeof t == `object` && t && (typeof t.BITS == `number` && (n = t.BITS), typeof t.sqrt == `function` && Object.defineProperty(this, "sqrt", { value: t.sqrt, enumerable: !0 }), typeof t.isLE == `boolean` && (this.isLE = t.isLE), t.allowedLengths && (this._lengths = Object.freeze(t.allowedLengths.slice())), typeof t.modFromBytes == `boolean` && (this._mod = t.modFromBytes)); let { nBitLength: r, nByteLength: i } = ec(e, n); if (i > 2048)
        throw Error(`invalid field: expected ORDER of <= 2048 bytes`); this.ORDER = e, this.BITS = r, this.BYTES = i, Object.freeze(this); }
    create(e) { return Bs(e, this.ORDER); }
    isValid(e) { if (typeof e != `bigint`)
        throw TypeError(`invalid field element: expected bigint, got ` + typeof e); return As <= e && e < this.ORDER; }
    is0(e) { return e === As; }
    isValidNot0(e) { return !this.is0(e) && this.isValid(e); }
    isOdd(e) { return (e & js) === js; }
    neg(e) { return Bs(-e, this.ORDER); }
    eql(e, t) { return e === t; }
    sqr(e) { return Bs(e * e, this.ORDER); }
    add(e, t) { return Bs(e + t, this.ORDER); }
    sub(e, t) { return Bs(e - t, this.ORDER); }
    mul(e, t) { return Bs(e * t, this.ORDER); }
    pow(e, t) { return Zs(this, e, t); }
    div(e, t) { return Bs(e * Hs(t, this.ORDER), this.ORDER); }
    sqrN(e) { return e * e; }
    addN(e, t) { return e + t; }
    subN(e, t) { return e - t; }
    mulN(e, t) { return e * t; }
    inv(e) { return Hs(e, this.ORDER); }
    sqrt(e) { let t = tc.get(this); return t || tc.set(this, t = Js(this.ORDER)), t(this, e); }
    toBytes(e) { return this.isLE ? bs(e, this.BYTES) : ys(e, this.BYTES); }
    fromBytes(e, t = !1) { q(e); let { _lengths: n, BYTES: r, isLE: i, ORDER: a, _mod: o } = this; if (n) {
        if (e.length < 1 || !n.includes(e.length) || e.length > r)
            throw Error(`Field.fromBytes: expected ` + n + ` bytes, got ` + e.length);
        let t = new Uint8Array(r);
        t.set(e, i ? 0 : t.length - e.length), e = t;
    } if (e.length !== r)
        throw Error(`Field.fromBytes: expected ` + r + ` bytes, got ` + e.length); let s = i ? vs(e) : _s(e); if (o && (s = Bs(s, a)), !t && !this.isValid(s))
        throw Error(`invalid field element: outside of range 0..ORDER`); return s; }
    invertBatch(e) { return Qs(this, e); }
    cmov(e, t, n) { return fs(n, `condition`), n ? t : e; }
};
Object.freeze(nc.prototype);
function rc(e, t = {}) { return new nc(e, t); }
function ic(e) { if (typeof e != `bigint`)
    throw Error(`field order must be bigint`); if (e <= js)
    throw Error(`field order must be greater than 1`); let t = Es(e - js); return Math.ceil(t / 8); }
function ac(e) { let t = ic(e); return t + Math.ceil(t / 2); }
function oc(e, t, n = !1) { q(e); let r = e.length, i = ic(t), a = Math.max(ac(t), 16); if (r < a || r > 1024)
    throw Error(`expected ` + a + `-1024 bytes of input, got ` + r); let o = Bs(n ? vs(e) : _s(e), t - js) + js; return n ? bs(o, i) : ys(o, i); }
var sc = BigInt(0);
var cc = BigInt(1);
function lc(e, t) { let n = t.negate(); return e ? n : t; }
function uc(e, t) { let n = Qs(e.Fp, t.map(e => e.Z)); return t.map((t, r) => e.fromAffine(t.toAffine(n[r]))); }
function dc(e, t) { if (!Number.isSafeInteger(e) || e <= 0 || e > t)
    throw Error(`invalid window size, expected [1..` + t + `], got W=` + e); }
function fc(e, t) { dc(e, t); let n = Math.ceil(t / e) + 1, r = 2 ** (e - 1), i = 2 ** e; return { windows: n, windowSize: r, mask: Ds(e), maxNumber: i, shiftBy: BigInt(e) }; }
function pc(e, t, n) { let { windowSize: r, mask: i, maxNumber: a, shiftBy: o } = n, s = Number(e & i), c = e >> o; s > r && (s -= a, c += cc); let l = t * r, u = l + Math.abs(s) - 1, d = s === 0, f = s < 0, p = t % 2 != 0; return { nextN: c, offset: u, isZero: d, isNeg: f, isNegF: p, offsetF: l }; }
var mc = new WeakMap;
var hc = new WeakMap;
function gc(e) { return hc.get(e) || 1; }
function _c(e) { if (e !== sc)
    throw Error(`invalid wNAF`); }
var vc = class {
    BASE;
    ZERO;
    Fn;
    bits;
    constructor(e, t) { this.BASE = e.BASE, this.ZERO = e.ZERO, this.Fn = e.Fn, this.bits = t; }
    _unsafeLadder(e, t, n = this.ZERO) { let r = e; for (; t > sc;)
        t & cc && (n = n.add(r)), r = r.double(), t >>= cc; return n; }
    precomputeWindow(e, t) { let { windows: n, windowSize: r } = fc(t, this.bits), i = [], a = e, o = a; for (let e = 0; e < n; e++) {
        o = a, i.push(o);
        for (let e = 1; e < r; e++)
            o = o.add(a), i.push(o);
        a = o.double();
    } return i; }
    wNAF(e, t, n) { if (!this.Fn.isValid(n))
        throw Error(`invalid scalar`); let r = this.ZERO, i = this.BASE, a = fc(e, this.bits); for (let e = 0; e < a.windows; e++) {
        let { nextN: o, offset: s, isZero: c, isNeg: l, isNegF: u, offsetF: d } = pc(n, e, a);
        n = o, c ? i = i.add(lc(u, t[d])) : r = r.add(lc(l, t[s]));
    } return _c(n), { p: r, f: i }; }
    wNAFUnsafe(e, t, n, r = this.ZERO) { let i = fc(e, this.bits); for (let e = 0; e < i.windows && n !== sc; e++) {
        let { nextN: a, offset: o, isZero: s, isNeg: c } = pc(n, e, i);
        if (n = a, !s) {
            let e = t[o];
            r = r.add(c ? e.negate() : e);
        }
    } return _c(n), r; }
    getPrecomputes(e, t, n) { let r = mc.get(t); return r || (r = this.precomputeWindow(t, e), e !== 1 && (typeof n == `function` && (r = n(r)), mc.set(t, r))), r; }
    cached(e, t, n) { let r = gc(e); return this.wNAF(r, this.getPrecomputes(r, e, n), t); }
    unsafe(e, t, n, r) { let i = gc(e); return i === 1 ? this._unsafeLadder(e, t, r) : this.wNAFUnsafe(i, this.getPrecomputes(i, e, n), t, r); }
    createCache(e, t) { dc(t, this.bits), hc.set(e, t), mc.delete(e); }
    hasCache(e) { return gc(e) !== 1; }
};
function yc(e, t, n, r) { let i = t, a = e.ZERO, o = e.ZERO; for (; n > sc || r > sc;)
    n & cc && (a = a.add(i)), r & cc && (o = o.add(i)), i = i.double(), n >>= cc, r >>= cc; return { p1: a, p2: o }; }
function bc(e, t, n) { if (t) {
    if (t.ORDER !== e)
        throw Error(`Field.ORDER must match order: Fp == p, Fn == n`);
    return Xs(t), t;
} return rc(e, { isLE: n }); }
function xc(e, t, n = {}, r) { if (r === void 0 && (r = e === `edwards`), !t || typeof t != `object`)
    throw Error(`expected valid ${e} CURVE object`); for (let e of [`p`, `n`, `h`]) {
    let n = t[e];
    if (!(typeof n == `bigint` && n > sc))
        throw Error(`CURVE.${e} must be positive bigint`);
} let i = bc(t.p, n.Fp, r), a = bc(t.n, n.Fn, r), o = [`Gx`, `Gy`, `a`, e === `weierstrass` ? `b` : `d`]; for (let e of o)
    if (!i.isValid(t[e]))
        throw Error(`CURVE.${e} must be valid field element of CURVE.Fp`); return t = Object.freeze(Object.assign({}, t)), { CURVE: t, Fp: i, Fn: a }; }
function Sc(e, t) { return function (n) { let r = e(n); return { secretKey: r, publicKey: t(r) }; }; }
var Cc = class {
    oHash;
    iHash;
    blockLen;
    outputLen;
    canXOF = !1;
    finished = !1;
    destroyed = !1;
    constructor(e, t) { if (no(e), to(t, void 0, `key`), this.iHash = e.create(), typeof this.iHash.update != `function`)
        throw Error(`Expected instance of class which extends utils.Hash`); this.blockLen = this.iHash.blockLen, this.outputLen = this.iHash.outputLen; let n = this.blockLen, r = new Uint8Array(n); r.set(t.length > n ? e.create().update(t).digest() : t); for (let e = 0; e < r.length; e++)
        r[e] ^= 54; this.iHash.update(r), this.oHash = e.create(); for (let e = 0; e < r.length; e++)
        r[e] ^= 106; this.oHash.update(r), ao(r); }
    update(e) { return ro(this), this.iHash.update(e), this; }
    digestInto(e) { ro(this), io(e, this), this.finished = !0; let t = e.subarray(0, this.outputLen); this.iHash.digestInto(t), this.oHash.update(t), this.oHash.digestInto(t), this.destroy(); }
    digest() { let e = new Uint8Array(this.oHash.outputLen); return this.digestInto(e), e; }
    _cloneInto(e) { e ||= Object.create(Object.getPrototypeOf(this), {}); let { oHash: t, iHash: n, finished: r, destroyed: i, blockLen: a, outputLen: o } = this; return e = e, e.finished = r, e.destroyed = i, e.blockLen = a, e.outputLen = o, e.oHash = t._cloneInto(e.oHash), e.iHash = n._cloneInto(e.iHash), e; }
    clone() { return this._cloneInto(); }
    destroy() { this.destroyed = !0, this.oHash.destroy(), this.iHash.destroy(); }
};
var wc = (() => { let e = ((e, t, n) => new Cc(e, t).update(n).digest()); return e.create = (e, t) => new Cc(e, t), e; })();
var Tc = (e, t) => (e + (e >= 0 ? t : -t) / Mc) / t;
function Ec(e, t, n) { Ts(`scalar`, e, Ac, n); let [[r, i], [a, o]] = t, s = Tc(o * e, n), c = Tc(-i * e, n), l = e - s * r - c * a, u = -s * i - c * o, d = l < Ac, f = u < Ac; d && (l = -l), f && (u = -u); let p = Ds(Math.ceil(Es(n) / 2)) + jc; if (l < Ac || l >= p || u < Ac || u >= p)
    throw Error(`splitScalar (endomorphism): failed for k`); return { k1neg: d, k1: l, k2neg: f, k2: u }; }
function Dc(e) { if (![`compact`, `recovered`, `der`].includes(e))
    throw Error(`Signature format must be "compact", "recovered", or "der"`); return e; }
function Oc(e, t) { ks(e); let n = {}; for (let r of Object.keys(t))
    n[r] = e[r] === void 0 ? t[r] : e[r]; return fs(n.lowS, `lowS`), fs(n.prehash, `prehash`), n.format !== void 0 && Dc(n.format), n; }
var kc = { Err: class extends Error {
        constructor(e = ``) { super(e); }
    }, _tlv: { encode: (e, t) => { let { Err: n } = kc; if (ms(e, `tag`), e < 0 || e > 255)
            throw new n(`tlv.encode: wrong tag`); if (typeof t != `string`)
            throw TypeError(`"data" expected string, got type=` + typeof t); if (t.length & 1)
            throw new n(`tlv.encode: unpadded data`); let r = t.length / 2, i = hs(r); if (i.length / 2 & 128)
            throw new n(`tlv.encode: long form length too big`); let a = r > 127 ? hs(i.length / 2 | 128) : ``; return hs(e) + a + i + t; }, decode(e, t) { let { Err: n } = kc; t = q(t, void 0, `DER data`); let r = 0; if (e < 0 || e > 255)
            throw new n(`tlv.encode: wrong tag`); if (t.length < 2 || t[r++] !== e)
            throw new n(`tlv.decode: wrong tlv`); let i = t[r++], a = !!(i & 128), o = 0; if (!a)
            o = i;
        else {
            let e = i & 127;
            if (!e)
                throw new n(`tlv.decode(long): indefinite length not supported`);
            if (e > 4)
                throw new n(`tlv.decode(long): byte length is too big`);
            let a = t.subarray(r, r + e);
            if (a.length !== e)
                throw new n(`tlv.decode: length bytes not complete`);
            if (a[0] === 0)
                throw new n(`tlv.decode(long): zero leftmost byte`);
            for (let e of a)
                o = o << 8 | e;
            if (r += e, o < 128)
                throw new n(`tlv.decode(long): not minimal encoding`);
        } let s = t.subarray(r, r + o); if (s.length !== o)
            throw new n(`tlv.decode: wrong value length`); return { v: s, l: t.subarray(r + o) }; } }, _int: { encode(e) { let { Err: t } = kc; if (ps(e), e < Ac)
            throw new t(`integer: negative integers are not allowed`); let n = hs(e); if (Number.parseInt(n[0], 16) & 8 && (n = `00` + n), n.length & 1)
            throw new t(`unexpected DER parsing assertion: unpadded hex`); return n; }, decode(e) { let { Err: t } = kc; if (e.length < 1)
            throw new t(`invalid signature integer: empty`); if (e[0] & 128)
            throw new t(`invalid signature integer: negative`); if (e.length > 1 && e[0] === 0 && !(e[1] & 128))
            throw new t(`invalid signature integer: unnecessary leading zero`); return _s(e); } }, toSig(e) { let { Err: t, _int: n, _tlv: r } = kc, i = q(e, void 0, `signature`), { v: a, l: o } = r.decode(48, i); if (o.length)
        throw new t(`invalid signature: left bytes after parsing`); let { v: s, l: c } = r.decode(2, a), { v: l, l: u } = r.decode(2, c); if (u.length)
        throw new t(`invalid signature: left bytes after parsing`); return { r: n.decode(s), s: n.decode(l) }; }, hexFromSig(e) { let { _tlv: t, _int: n } = kc, r = t.encode(2, n.encode(e.r)) + t.encode(2, n.encode(e.s)); return t.encode(48, r); } };
Object.freeze(kc._tlv), Object.freeze(kc._int), Object.freeze(kc);
var Ac = BigInt(0);
var jc = BigInt(1);
var Mc = BigInt(2);
var Nc = BigInt(3);
var Pc = BigInt(4);
function Fc(e, t = {}) { let n = xc(`weierstrass`, e, t), r = n.Fp, i = n.Fn, a = n.CURVE, { h: o, n: s } = a; ks(t, {}, { allowInfinityPoint: `boolean`, clearCofactor: `function`, isTorsionFree: `function`, fromBytes: `function`, toBytes: `function`, endo: `object` }); let { endo: c, allowInfinityPoint: l } = t; if (c && (!r.is0(a.a) || typeof c.beta != `bigint` || !Array.isArray(c.basises)))
    throw Error(`invalid endo: expected "beta": bigint and "basises": array`); let u = Lc(r, i); function d() { if (!r.isOdd)
    throw Error(`compression is not supported: Field does not have .isOdd()`); } function f(e, t, n) { if (l && t.is0())
    return Uint8Array.of(0); let { x: i, y: a } = t.toAffine(), o = r.toBytes(i); return fs(n, `isCompressed`), n ? (d(), os(Ic(!r.isOdd(a)), o)) : os(Uint8Array.of(4), o, r.toBytes(a)); } function p(e) { q(e, void 0, `Point`); let { publicKey: t, publicKeyUncompressed: n } = u, i = e.length, a = e[0], o = e.subarray(1); if (l && i === 1 && a === 0)
    return { x: r.ZERO, y: r.ZERO }; if (i === t && (a === 2 || a === 3)) {
    let e = r.fromBytes(o);
    if (!r.isValid(e))
        throw Error(`bad point: is not on curve, wrong x`);
    let t = g(e), n;
    try {
        n = r.sqrt(t);
    }
    catch (e) {
        let t = e instanceof Error ? `: ` + e.message : ``;
        throw Error(`bad point: is not on curve, sqrt error` + t);
    }
    d();
    let i = r.isOdd(n);
    return (a & 1) == 1 !== i && (n = r.neg(n)), { x: e, y: n };
} if (i === n && a === 4) {
    let e = r.BYTES, t = r.fromBytes(o.subarray(0, e)), n = r.fromBytes(o.subarray(e, e * 2));
    if (!_(t, n))
        throw Error(`bad point: is not on curve`);
    return { x: t, y: n };
} throw Error(`bad point: got length ${i}, expected compressed=${t} or uncompressed=${n}`); } let m = t.toBytes === void 0 ? f : t.toBytes, h = t.fromBytes === void 0 ? p : t.fromBytes; function g(e) { let t = r.sqr(e), n = r.mul(t, e); return r.add(r.add(n, r.mul(e, a.a)), a.b); } function _(e, t) { let n = r.sqr(t), i = g(e); return r.eql(n, i); } if (!_(a.Gx, a.Gy))
    throw Error(`bad curve params: generator point`); let v = r.mul(r.pow(a.a, Nc), Pc), y = r.mul(r.sqr(a.b), BigInt(27)); if (r.is0(r.add(v, y)))
    throw Error(`bad curve params: a or b`); function b(e, t, n = !1) { if (!r.isValid(t) || n && r.is0(t))
    throw Error(`bad point coordinate ${e}`); return t; } function x(e) { if (!(e instanceof w))
    throw Error(`Weierstrass Point expected`); } function S(e) { if (!c || !c.basises)
    throw Error(`no endo`); return Ec(e, c.basises, i.ORDER); } function C(e, t, n, i, a) { return n = new w(r.mul(n.X, e), n.Y, n.Z), t = lc(i, t), n = lc(a, n), t.add(n); } class w {
    static BASE = new w(a.Gx, a.Gy, r.ONE);
    static ZERO = new w(r.ZERO, r.ONE, r.ZERO);
    static Fp = r;
    static Fn = i;
    X;
    Y;
    Z;
    constructor(e, t, n) { this.X = b(`x`, e), this.Y = b(`y`, t, !0), this.Z = b(`z`, n), Object.freeze(this); }
    static CURVE() { return a; }
    static fromAffine(e) { let { x: t, y: n } = e || {}; if (!e || !r.isValid(t) || !r.isValid(n))
        throw Error(`invalid affine point`); if (e instanceof w)
        throw Error(`projective point not allowed`); return r.is0(t) && r.is0(n) ? w.ZERO : new w(t, n, r.ONE); }
    static fromBytes(e) { let t = w.fromAffine(h(q(e, void 0, `point`))); return t.assertValidity(), t; }
    static fromHex(e) { return w.fromBytes(ss(e)); }
    get x() { return this.toAffine().x; }
    get y() { return this.toAffine().y; }
    precompute(e = 8, t = !0) { return E.createCache(this, e), t || this.multiply(Nc), this; }
    assertValidity() { let e = this; if (e.is0()) {
        if (t.allowInfinityPoint && r.is0(e.X) && r.eql(e.Y, r.ONE) && r.is0(e.Z))
            return;
        throw Error(`bad point: ZERO`);
    } let { x: n, y: i } = e.toAffine(); if (!r.isValid(n) || !r.isValid(i))
        throw Error(`bad point: x or y not field elements`); if (!_(n, i))
        throw Error(`bad point: equation left != right`); if (!e.isTorsionFree())
        throw Error(`bad point: not in prime-order subgroup`); }
    hasEvenY() { let { y: e } = this.toAffine(); if (!r.isOdd)
        throw Error(`Field doesn't support isOdd`); return !r.isOdd(e); }
    equals(e) { x(e); let { X: t, Y: n, Z: i } = this, { X: a, Y: o, Z: s } = e, c = r.eql(r.mul(t, s), r.mul(a, i)), l = r.eql(r.mul(n, s), r.mul(o, i)); return c && l; }
    negate() { return new w(this.X, r.neg(this.Y), this.Z); }
    double() { let { a: e, b: t } = a, n = r.mul(t, Nc), { X: i, Y: o, Z: s } = this, c = r.ZERO, l = r.ZERO, u = r.ZERO, d = r.mul(i, i), f = r.mul(o, o), p = r.mul(s, s), m = r.mul(i, o); return m = r.add(m, m), u = r.mul(i, s), u = r.add(u, u), c = r.mul(e, u), l = r.mul(n, p), l = r.add(c, l), c = r.sub(f, l), l = r.add(f, l), l = r.mul(c, l), c = r.mul(m, c), u = r.mul(n, u), p = r.mul(e, p), m = r.sub(d, p), m = r.mul(e, m), m = r.add(m, u), u = r.add(d, d), d = r.add(u, d), d = r.add(d, p), d = r.mul(d, m), l = r.add(l, d), p = r.mul(o, s), p = r.add(p, p), d = r.mul(p, m), c = r.sub(c, d), u = r.mul(p, f), u = r.add(u, u), u = r.add(u, u), new w(c, l, u); }
    add(e) { x(e); let { X: t, Y: n, Z: i } = this, { X: o, Y: s, Z: c } = e, l = r.ZERO, u = r.ZERO, d = r.ZERO, f = a.a, p = r.mul(a.b, Nc), m = r.mul(t, o), h = r.mul(n, s), g = r.mul(i, c), _ = r.add(t, n), v = r.add(o, s); _ = r.mul(_, v), v = r.add(m, h), _ = r.sub(_, v), v = r.add(t, i); let y = r.add(o, c); return v = r.mul(v, y), y = r.add(m, g), v = r.sub(v, y), y = r.add(n, i), l = r.add(s, c), y = r.mul(y, l), l = r.add(h, g), y = r.sub(y, l), d = r.mul(f, v), l = r.mul(p, g), d = r.add(l, d), l = r.sub(h, d), d = r.add(h, d), u = r.mul(l, d), h = r.add(m, m), h = r.add(h, m), g = r.mul(f, g), v = r.mul(p, v), h = r.add(h, g), g = r.sub(m, g), g = r.mul(f, g), v = r.add(v, g), m = r.mul(h, v), u = r.add(u, m), m = r.mul(y, v), l = r.mul(_, l), l = r.sub(l, m), m = r.mul(_, h), d = r.mul(y, d), d = r.add(d, m), new w(l, u, d); }
    subtract(e) { return x(e), this.add(e.negate()); }
    is0() { return this.equals(w.ZERO); }
    multiply(e) { let { endo: n } = t; if (!i.isValidNot0(e))
        throw RangeError(`invalid scalar: out of range`); let r, a, o = e => E.cached(this, e, e => uc(w, e)); if (n) {
        let { k1neg: t, k1: i, k2neg: s, k2: c } = S(e), { p: l, f: u } = o(i), { p: d, f } = o(c);
        a = u.add(f), r = C(n.beta, l, d, t, s);
    }
    else {
        let { p: t, f: n } = o(e);
        r = t, a = n;
    } return uc(w, [r, a])[0]; }
    multiplyUnsafe(e) { let { endo: n } = t, r = this, a = e; if (!i.isValid(a))
        throw RangeError(`invalid scalar: out of range`); if (a === Ac || r.is0())
        return w.ZERO; if (a === jc)
        return r; if (E.hasCache(this))
        return this.multiply(a); if (n) {
        let { k1neg: e, k1: t, k2neg: i, k2: o } = S(a), { p1: s, p2: c } = yc(w, r, t, o);
        return C(n.beta, s, c, e, i);
    } return E.unsafe(r, a); }
    toAffine(e) { let t = this, n = e, { X: i, Y: a, Z: o } = t; if (r.eql(o, r.ONE))
        return { x: i, y: a }; let s = t.is0(); n ??= s ? r.ONE : r.inv(o); let c = r.mul(i, n), l = r.mul(a, n), u = r.mul(o, n); if (s)
        return { x: r.ZERO, y: r.ZERO }; if (!r.eql(u, r.ONE))
        throw Error(`invZ was invalid`); return { x: c, y: l }; }
    isTorsionFree() { let { isTorsionFree: e } = t; return o === jc ? !0 : e ? e(w, this) : E.unsafe(this, s).is0(); }
    clearCofactor() { let { clearCofactor: e } = t; return o === jc ? this : e ? e(w, this) : this.multiplyUnsafe(o); }
    isSmallOrder() { return o === jc ? this.is0() : this.clearCofactor().is0(); }
    toBytes(e = !0) { return fs(e, `isCompressed`), this.assertValidity(), m(w, this, e); }
    toHex(e = !0) { return as(this.toBytes(e)); }
    toString() { return `<Point ${this.is0() ? `ZERO` : this.toHex()}>`; }
} let T = i.BITS, E = new vc(w, t.endo ? Math.ceil(T / 2) : T); return T >= 8 && w.BASE.precompute(8), Object.freeze(w.prototype), Object.freeze(w), w; }
function Ic(e) { return Uint8Array.of(e ? 2 : 3); }
function Lc(e, t) { return { secretKey: t.BYTES, publicKey: 1 + e.BYTES, publicKeyUncompressed: 1 + 2 * e.BYTES, publicKeyHasPrefix: !0, signature: 2 * t.BYTES }; }
function Rc(e, t = {}) { let { Fn: n } = e, r = t.randomBytes === void 0 ? ls : t.randomBytes, i = Object.assign(Lc(e.Fp, n), { seed: Math.max(ac(n.ORDER), 16) }); function a(e) { try {
    let t = n.fromBytes(e);
    return n.isValidNot0(t);
}
catch {
    return !1;
} } function o(t, n) { let { publicKey: r, publicKeyUncompressed: a } = i; try {
    let i = t.length;
    return n === !0 && i !== r || n === !1 && i !== a ? !1 : !!e.fromBytes(t);
}
catch {
    return !1;
} } function s(e) { return e = e === void 0 ? r(i.seed) : e, oc(q(e, i.seed, `seed`), n.ORDER); } function c(t, r = !0) { return e.BASE.multiply(n.fromBytes(t)).toBytes(r); } function l(e) { let { secretKey: t, publicKey: r, publicKeyUncompressed: a } = i, o = n._lengths; if (!cs(e))
    return; let s = q(e, void 0, `key`).length, c = s === r || s === a, l = s === t || !!o?.includes(s); if (!(c && l))
    return c; } function u(t, r, i = !0) { if (l(t) === !0)
    throw Error(`first arg must be private key`); if (l(r) === !1)
    throw Error(`second arg must be public key`); let a = n.fromBytes(t); return e.fromBytes(r).multiply(a).toBytes(i); } let d = { isValidSecretKey: a, isValidPublicKey: o, randomSecretKey: s }, f = Sc(s, c); return Object.freeze(d), Object.freeze(i), Object.freeze({ getPublicKey: c, getSharedSecret: u, keygen: f, Point: e, utils: d, lengths: i }); }
function zc(e, t, n = {}) { let r = t; no(r), ks(n, {}, { hmac: `function`, lowS: `boolean`, randomBytes: `function`, bits2int: `function`, bits2int_modN: `function` }), n = Object.assign({}, n); let i = n.randomBytes === void 0 ? ls : n.randomBytes, a = n.hmac === void 0 ? (e, t) => wc(r, e, t) : n.hmac, { Fp: o, Fn: s } = e, { ORDER: c, BITS: l } = s, { keygen: u, getPublicKey: d, getSharedSecret: f, utils: p, lengths: m } = Rc(e, n), h = { prehash: !0, lowS: typeof n.lowS != `boolean` || n.lowS, format: `compact`, extraEntropy: !1 }, g = c * Mc + jc < o.ORDER; function _(e) { return e > c >> jc; } function v(e, t) { if (!s.isValidNot0(t))
    throw Error(`invalid signature ${e}: out of range 1..Point.Fn.ORDER`); return t; } function y() { if (g)
    throw Error(`"recovered" sig type is not supported for cofactor >2 curves`); } function b(e, t) { Dc(t); let n = m.signature; return q(e, t === `compact` ? n : t === `recovered` ? n + 1 : void 0); } class x {
    r;
    s;
    recovery;
    constructor(e, t, n) { if (this.r = v(`r`, e), this.s = v(`s`, t), n != null) {
        if (y(), ![0, 1, 2, 3].includes(n))
            throw Error(`invalid recovery id`);
        this.recovery = n;
    } Object.freeze(this); }
    static fromBytes(e, t = h.format) { b(e, t); let n; if (t === `der`) {
        let { r: t, s: n } = kc.toSig(q(e));
        return new x(t, n);
    } t === `recovered` && (n = e[0], t = `compact`, e = e.subarray(1)); let r = m.signature / 2, i = e.subarray(0, r), a = e.subarray(r, r * 2); return new x(s.fromBytes(i), s.fromBytes(a), n); }
    static fromHex(e, t) { return this.fromBytes(ss(e), t); }
    assertRecovery() { let { recovery: e } = this; if (e == null)
        throw Error(`invalid recovery id: must be present`); return e; }
    addRecoveryBit(e) { return new x(this.r, this.s, e); }
    recoverPublicKey(t) { let { r: n, s: r } = this, i = this.assertRecovery(), a = i === 2 || i === 3 ? n + c : n; if (!o.isValid(a))
        throw Error(`invalid recovery id: sig.r+curve.n != R.x`); let l = o.toBytes(a), u = e.fromBytes(os(Ic(!(i & 1)), l)), d = s.inv(a), f = C(q(t, void 0, `msgHash`)), p = s.create(-f * d), m = s.create(r * d), h = e.BASE.multiplyUnsafe(p).add(u.multiplyUnsafe(m)); if (h.is0())
        throw Error(`invalid recovery: point at infinify`); return h.assertValidity(), h; }
    hasHighS() { return _(this.s); }
    toBytes(e = h.format) { if (Dc(e), e === `der`)
        return ss(kc.hexFromSig(this)); let { r: t, s: n } = this, r = s.toBytes(t), i = s.toBytes(n); return e === `recovered` ? (y(), os(Uint8Array.of(this.assertRecovery()), r, i)) : os(r, i); }
    toHex(e) { return as(this.toBytes(e)); }
} Object.freeze(x.prototype), Object.freeze(x); let S = n.bits2int === void 0 ? function (e) { if (e.length > 8192)
    throw Error(`input is too large`); let t = _s(e), n = e.length * 8 - l; return n > 0 ? t >> BigInt(n) : t; } : n.bits2int, C = n.bits2int_modN === void 0 ? function (e) { return s.create(S(e)); } : n.bits2int_modN, w = Ds(l); function T(e) { return Ts(`num < 2^` + l, e, Ac, w), s.toBytes(e); } function E(e, t) { return q(e, void 0, `message`), t ? q(r(e), void 0, `prehashed message`) : e; } function D(t, n, r) { let { lowS: a, prehash: o, extraEntropy: c } = Oc(r, h); t = E(t, o); let l = C(t), u = s.fromBytes(n); if (!s.isValidNot0(u))
    throw Error(`invalid private key`); let d = [T(u), T(l)]; if (c != null && c !== !1) {
    let e = c === !0 ? i(m.secretKey) : c;
    d.push(q(e, void 0, `extraEntropy`));
} let f = os(...d), p = l; function v(t) { let n = S(t); if (!s.isValidNot0(n))
    return; let r = s.inv(n), i = e.BASE.multiply(n).toAffine(), o = s.create(i.x); if (o === Ac)
    return; let c = s.create(r * s.create(p + o * u)); if (c === Ac)
    return; let l = (i.x === o ? 0 : 2) | Number(i.y & jc), d = c; return a && _(c) && (d = s.neg(c), l ^= 1), new x(o, d, g ? void 0 : l); } return { seed: f, k2sig: v }; } function O(e, t, n = {}) { let { seed: i, k2sig: o } = D(e, t, n); return Os(r.outputLen, s.BYTES, a)(i, o).toBytes(n.format); } function k(t, n, r, i = {}) { let { lowS: a, prehash: o, format: c } = Oc(i, h); if (r = q(r, void 0, `publicKey`), n = E(n, o), !cs(t)) {
    let e = t instanceof x ? `, use sig.toBytes()` : ``;
    throw Error(`verify expects Uint8Array signature` + e);
} b(t, c); try {
    let i = x.fromBytes(t, c), o = e.fromBytes(r);
    if (a && i.hasHighS())
        return !1;
    let { r: l, s: u } = i, d = C(n), f = s.inv(u), p = s.create(d * f), m = s.create(l * f), h = e.BASE.multiplyUnsafe(p).add(o.multiplyUnsafe(m));
    return !h.is0() && s.create(h.x) === l;
}
catch {
    return !1;
} } function A(e, t, n = {}) { let { prehash: r } = Oc(n, h); return t = E(t, r), x.fromBytes(e, `recovered`).recoverPublicKey(t).toBytes(); } return Object.freeze({ keygen: u, getPublicKey: d, getSharedSecret: f, utils: p, lengths: m, Point: e, sign: O, verify: k, recoverPublicKey: A, Signature: x, hash: r }); }
var Bc = { p: BigInt(`0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f`), n: BigInt(`0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141`), h: BigInt(1), a: BigInt(0), b: BigInt(7), Gx: BigInt(`0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798`), Gy: BigInt(`0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8`) };
var Vc = { beta: BigInt(`0x7ae96a2b657c07106e64479eac3434e99cf0497512f58995c1396c28719501ee`), basises: [[BigInt(`0x3086d221a7d46bcde86c90e49284eb15`), -BigInt(`0xe4437ed6010e88286f547fa90abfe4c3`)], [BigInt(`0x114ca50f7a8e2f3f657c1108d9d44cfd8`), BigInt(`0x3086d221a7d46bcde86c90e49284eb15`)]] };
var Hc = BigInt(0);
var Uc = BigInt(2);
function Wc(e) { let t = Bc.p, n = BigInt(3), r = BigInt(6), i = BigInt(11), a = BigInt(22), o = BigInt(23), s = BigInt(44), c = BigInt(88), l = e * e * e % t, u = l * l * e % t, d = Vs(Vs(Vs(u, n, t) * u % t, n, t) * u % t, Uc, t) * l % t, f = Vs(d, i, t) * d % t, p = Vs(f, a, t) * f % t, m = Vs(p, s, t) * p % t, h = Vs(Vs(Vs(Vs(Vs(Vs(m, c, t) * m % t, s, t) * p % t, n, t) * u % t, o, t) * f % t, r, t) * l % t, Uc, t); if (!Gc.eql(Gc.sqr(h), e))
    throw Error(`Cannot find square root`); return h; }
var Gc = rc(Bc.p, { sqrt: Wc });
var Kc = Fc(Bc, { Fp: Gc, endo: Vc });
var qc = zc(Kc, ns);
var Jc = {};
function Yc(e, ...t) { let n = Jc[e]; if (n === void 0) {
    let t = ns(Ss(e));
    n = os(t, t), Jc[e] = n;
} return ns(os(n, ...t)); }
var Xc = e => e.toBytes(!0).slice(1);
var Zc = e => e % Uc === Hc;
function Qc(e) { let { Fn: t, BASE: n } = Kc, r = t.fromBytes(e), i = n.multiply(r); return { scalar: Zc(i.y) ? r : t.neg(r), bytes: Xc(i) }; }
function $c(e) { let t = Gc; if (!t.isValidNot0(e))
    throw Error(`invalid x: Fail if x ≥ p`); let n = t.create(e * e), r = t.create(n * e + BigInt(7)), i = t.sqrt(r); Zc(i) || (i = t.neg(i)); let a = Kc.fromAffine({ x: e, y: i }); return a.assertValidity(), a; }
var el = _s;
function tl(...e) { return Kc.Fn.create(el(Yc(`BIP0340/challenge`, ...e))); }
function nl(e) { return Qc(e).bytes; }
function rl(e, t, n = xo(32)) { let { Fn: r, BASE: i } = Kc, a = q(e, void 0, `message`), { bytes: o, scalar: s } = Qc(t), c = q(n, 32, `auxRand`), l = Yc(`BIP0340/nonce`, r.toBytes(s ^ el(Yc(`BIP0340/aux`, c))), o, a), u = r.create(el(l)); if (u === 0n)
    throw Error(`sign failed: k is zero`); let d = i.multiply(u), f = Zc(d.y) ? u : r.neg(u), p = Xc(d), m = tl(p, o, a), h = new Uint8Array(64); if (h.set(p, 0), h.set(r.toBytes(r.create(f + m * s)), 32), !il(h, a, o))
    throw Error(`sign: Invalid signature produced`); return h; }
function il(e, t, n) { let { Fp: r, Fn: i, BASE: a } = Kc, o = q(e, 64, `signature`), s = q(t, void 0, `message`), c = q(n, 32, `publicKey`); try {
    let e = $c(el(c)), t = el(o.subarray(0, 32));
    if (!r.isValidNot0(t))
        return !1;
    let n = el(o.subarray(32, 64));
    if (!i.isValidNot0(n))
        return !1;
    let l = tl(i.toBytes(t), Xc(e), s), u = a.multiplyUnsafe(n).add(e.multiplyUnsafe(i.neg(l))), { x: d, y: f } = u.toAffine();
    return !(u.is0() || !Zc(f) || d !== t);
}
catch {
    return !1;
} }
var al = (() => { let e = e => (e = e === void 0 ? xo(48) : e, oc(e, Bc.n)); return Object.freeze({ keygen: Sc(e, nl), getPublicKey: nl, sign: rl, verify: il, Point: Kc, utils: Object.freeze({ randomSecretKey: e, taggedHash: Yc, lift_x: $c, pointToBytes: Xc }), lengths: Object.freeze({ secretKey: 32, publicKey: 32, publicKeyHasPrefix: !1, signature: 64, seed: 48 }) }); })();
var ol = Uint8Array.from([7, 4, 13, 1, 10, 6, 15, 3, 12, 0, 9, 5, 2, 14, 11, 8]);
var sl = Uint8Array.from(Array(16).fill(0).map((e, t) => t));
var cl = sl.map(e => (9 * e + 5) % 16);
var ll = (() => { let e = [[sl], [cl]]; for (let t = 0; t < 4; t++)
    for (let n of e)
        n.push(n[t].map(e => ol[e])); return e; })();
var ul = ll[0];
var dl = ll[1];
var fl = [[11, 14, 15, 12, 5, 8, 7, 9, 11, 13, 14, 15, 6, 7, 9, 8], [12, 13, 11, 15, 6, 9, 9, 7, 12, 15, 11, 13, 7, 8, 7, 7], [13, 15, 14, 11, 7, 7, 6, 8, 13, 14, 13, 12, 5, 5, 6, 9], [14, 11, 12, 14, 8, 6, 5, 5, 15, 12, 15, 14, 9, 9, 8, 6], [15, 12, 13, 13, 9, 5, 8, 6, 14, 11, 12, 11, 8, 6, 5, 5]].map(e => Uint8Array.from(e));
var pl = ul.map((e, t) => e.map(e => fl[t][e]));
var ml = dl.map((e, t) => e.map(e => fl[t][e]));
var hl = Uint32Array.from([0, 1518500249, 1859775393, 2400959708, 2840853838]);
var gl = Uint32Array.from([1352829926, 1548603684, 1836072691, 2053994217, 0]);
function _l(e, t, n, r) { return e === 0 ? t ^ n ^ r : e === 1 ? t & n | ~t & r : e === 2 ? (t | ~n) ^ r : e === 3 ? t & r | n & ~r : t ^ (n | ~r); }
var vl = new Uint32Array(16);
var yl = class extends To {
    h0 = 1732584193;
    h1 = -271733879;
    h2 = -1732584194;
    h3 = 271733878;
    h4 = -1009589776;
    constructor() { super(64, 20, 8, !0); }
    get() { let { h0: e, h1: t, h2: n, h3: r, h4: i } = this; return [e, t, n, r, i]; }
    set(e, t, n, r, i) { this.h0 = e | 0, this.h1 = t | 0, this.h2 = n | 0, this.h3 = r | 0, this.h4 = i | 0; }
    process(e, t) { for (let n = 0; n < 16; n++, t += 4)
        vl[n] = e.getUint32(t, !0); let n = this.h0 | 0, r = n, i = this.h1 | 0, a = i, o = this.h2 | 0, s = o, c = this.h3 | 0, l = c, u = this.h4 | 0, d = u; for (let e = 0; e < 5; e++) {
        let t = 4 - e, f = hl[e], p = gl[e], m = ul[e], h = dl[e], g = pl[e], _ = ml[e];
        for (let t = 0; t < 16; t++) {
            let r = co(n + _l(e, i, o, c) + vl[m[t]] + f, g[t]) + u | 0;
            n = u, u = c, c = co(o, 10) | 0, o = i, i = r;
        }
        for (let e = 0; e < 16; e++) {
            let n = co(r + _l(t, a, s, l) + vl[h[e]] + p, _[e]) + d | 0;
            r = d, d = l, l = co(s, 10) | 0, s = a, a = n;
        }
    } this.set(this.h1 + o + l | 0, this.h2 + c + d | 0, this.h3 + u + r | 0, this.h4 + n + a | 0, this.h0 + i + s | 0); }
    roundClean() { ao(vl); }
    destroy() { this.destroyed = !0, ao(this.buffer), this.set(0, 0, 0, 0, 0); }
};
var bl = bo(() => new yl);
var xl = qc.Point;
var Sl = xl.Fn;
var Cl = Ba(ns);
var wl = Uint8Array.from(`Bitcoin seed`.split(``), e => e.charCodeAt(0));
var Tl = { private: 76066276, public: 76067358 };
var El = 2147483648;
var Dl = e => bl(ns(e));
var Ol = e => oo(e).getUint32(0, !1);
var kl = e => { if (typeof e != `number`)
    throw TypeError(`invalid number, should be from 0 to 2**32-1, got ` + e); if (!Number.isSafeInteger(e) || e < 0 || e > 2 ** 32 - 1)
    throw RangeError(`invalid number, should be from 0 to 2**32-1, got ` + e); let t = new Uint8Array(4); return oo(t).setUint32(0, e, !1), t; };
var Al = class e {
    get fingerprint() { if (!this.pubHash)
        throw Error(`No publicKey set!`); return Ol(this.pubHash); }
    get identifier() { return this.pubHash; }
    get pubKeyHash() { return this.pubHash; }
    get privateKey() { return this._privateKey || null; }
    get publicKey() { return this._publicKey || null; }
    get privateExtendedKey() { let e = this._privateKey; if (!e)
        throw Error(`No private key`); return Cl.encode(this.serialize(this.versions.private, vo(Uint8Array.of(0), e))); }
    get publicExtendedKey() { if (!this._publicKey)
        throw Error(`No public key`); return Cl.encode(this.serialize(this.versions.public, this._publicKey)); }
    static fromMasterSeed(t, n = Tl) { if (to(t), 8 * t.length < 128 || 8 * t.length > 512)
        throw RangeError(`HDKey: seed length must be between 128 and 512 bits; 256 bits is advised, got ` + t.length); let r = wc(rs, wl, t), i = r.slice(0, 32), a = r.slice(32); return new e({ versions: n, chainCode: a, privateKey: i }); }
    static fromExtendedKey(t, n = Tl) { let r = Cl.decode(t), i = oo(r), a = i.getUint32(0, !1), o = { versions: n, depth: r[4], parentFingerprint: i.getUint32(5, !1), index: i.getUint32(9, !1), chainCode: r.slice(13, 45) }, s = r.slice(45), c = s[0] === 0; if (a !== n[c ? `private` : `public`])
        throw Error(`Version mismatch`); return c ? new e({ ...o, privateKey: s.slice(1) }) : new e({ ...o, publicKey: s }); }
    static fromJSON(t) { return e.fromExtendedKey(t.xpriv); }
    versions;
    depth = 0;
    index = 0;
    chainCode = null;
    parentFingerprint = 0;
    _privateKey;
    _publicKey;
    pubHash;
    constructor(e) { if (!e || typeof e != `object`)
        throw Error(`HDKey.constructor must not be called directly`); if (this.versions = e.versions || Tl, this.depth = e.depth || 0, this.chainCode = e.chainCode ? Uint8Array.from(e.chainCode) : null, this.index = e.index || 0, this.parentFingerprint = e.parentFingerprint || 0, !this.depth && (this.parentFingerprint || this.index))
        throw Error(`HDKey: zero depth with non-zero index/parent fingerprint`); if (this.depth > 255)
        throw Error(`HDKey: depth exceeds the serializable value 255`); if (e.publicKey && e.privateKey)
        throw Error(`HDKey: publicKey and privateKey at same time.`); if (e.privateKey) {
        if (!qc.utils.isValidSecretKey(e.privateKey))
            throw Error(`Invalid private key`);
        this._privateKey = Uint8Array.from(e.privateKey), this._publicKey = qc.getPublicKey(this._privateKey, !0);
    }
    else if (e.publicKey)
        this._publicKey = xl.fromBytes(e.publicKey).toBytes(!0);
    else
        throw Error(`HDKey: no public or private key provided`); this.pubHash = Dl(this._publicKey); }
    derive(e) { if (!/^[mM]'?/.test(e))
        throw Error(`Path must start with "m" or "M"`); if (/^[mM]'?$/.test(e))
        return this; let t = e.replace(/^[mM]'?\//, ``).split(`/`), n = this; for (let e of t) {
        let t = /^(\d+)('?)$/.exec(e), r = t && t[1];
        if (!t || t.length !== 3 || typeof r != `string`)
            throw Error(`invalid child index: ` + e);
        let i = +r;
        if (!Number.isSafeInteger(i) || i >= 2147483648)
            throw Error(`Invalid index`);
        t[2] === `'` && (i += El), n = n.deriveChild(i);
    } return n; }
    deriveChild(t, n) { if (!this._publicKey || !this.chainCode)
        throw Error(`No publicKey or chainCode set`); let r = kl(t); if (t >= 2147483648) {
        let e = this._privateKey;
        if (!e)
            throw Error(`Could not derive hardened child key`);
        r = vo(Uint8Array.of(0), e, r);
    }
    else
        r = vo(this._publicKey, r); let i = n || wc(rs, this.chainCode, r); to(i, 64); let a = i.slice(0, 32), o = i.slice(32), s = { versions: this.versions, chainCode: o, depth: this.depth + 1, parentFingerprint: this.fingerprint, index: t }; if (s.depth > 255)
        throw Error(`HDKey: depth exceeds the serializable value 255`); try {
        let t = Sl.fromBytes(a);
        if (this._privateKey) {
            let e = Sl.create(Sl.fromBytes(this._privateKey) + t);
            if (!Sl.isValidNot0(e))
                throw Error(`The tweak was out of range or the resulted private key is invalid`);
            s.privateKey = Sl.toBytes(e);
        }
        else {
            let e = xl.fromBytes(this._publicKey), n = t === 0n ? e : e.add(xl.BASE.multiply(t));
            if (n.equals(xl.ZERO))
                throw Error(`The tweak was equal to negative P, which made the result key invalid`);
            s.publicKey = n.toBytes(!0);
        }
        return new e(s);
    }
    catch {
        return this.deriveChild(t + 1);
    } }
    sign(e) { if (!this._privateKey)
        throw Error(`No privateKey set!`); return to(e, 32), qc.sign(e, this._privateKey, { prehash: !1 }); }
    verify(e, t) { if (to(e, 32), to(t, 64), !this._publicKey)
        throw Error(`No publicKey set!`); return qc.verify(t, e, this._publicKey, { prehash: !1 }); }
    wipePrivateData() { return this._privateKey &&= (this._privateKey.fill(0), void 0), this; }
    toJSON() { return { xpriv: this.privateExtendedKey, xpub: this.publicExtendedKey }; }
    serialize(e, t) { if (!this.chainCode)
        throw Error(`No chainCode set`); return to(t, 33), vo(kl(e), new Uint8Array([this.depth]), kl(this.parentFingerprint), kl(this.index), this.chainCode, t); }
};
function jl(e, t, n, r) { no(e); let { c: i, dkLen: a, asyncTick: o } = yo({ dkLen: 32, asyncTick: 10 }, r); if (eo(i, `c`), eo(a, `dkLen`), eo(o, `asyncTick`), i < 1)
    throw Error(`iterations (c) must be >= 1`); if (a < 1)
    throw Error(`"dkLen" must be >= 1`); if (a > (2 ** 32 - 1) * e.outputLen)
    throw Error(`derived key too long`); let s = _o(t, `password`), c = _o(n, `salt`), l = new Uint8Array(a), u = wc.create(e, s); return { c: i, dkLen: a, asyncTick: o, DK: l, PRF: u, PRFSalt: u._cloneInto().update(c) }; }
function Ml(e, t, n, r, i) { return e.destroy(), t.destroy(), r && r.destroy(), ao(i), n; }
function Nl(e, t, n, r) { let { c: i, dkLen: a, DK: o, PRF: s, PRFSalt: c } = jl(e, t, n, r), l, u = new Uint8Array(4), d = oo(u), f = new Uint8Array(s.outputLen); for (let e = 1, t = 0; t < a; e++, t += s.outputLen) {
    let n = o.subarray(t, t + s.outputLen);
    d.setInt32(0, e, !1), (l = c._cloneInto(l)).update(u).digestInto(f), n.set(f.subarray(0, n.length));
    for (let e = 1; e < i; e++) {
        s._cloneInto(l).update(f).digestInto(f);
        for (let e = 0; e < n.length; e++)
            n[e] ^= f[e];
    }
} return Ml(s, c, o, l, f); }
var Pl = e => e[0] === `あいこくしん`;
function Fl(e) { if (typeof e != `string`)
    throw TypeError(`invalid mnemonic type: ` + typeof e); return e.normalize(`NFKD`); }
function Il(e) { let t = Fl(e), n = t.split(` `); if (![12, 15, 18, 21, 24].includes(n.length))
    throw Error(`Invalid mnemonic`); return { nfkd: t, words: n }; }
function Ll(e) { if (to(e), ![16, 20, 24, 28, 32].includes(e.length))
    throw RangeError(`invalid entropy length`); }
function Rl(e, t = 128) { if (eo(t), t % 32 != 0 || t > 256)
    throw RangeError(`Invalid entropy`); return Hl(xo(t / 8), e); }
var zl = e => { let t = 8 - e.length / 4; return new Uint8Array([ns(e)[0] >> t << t]); };
function Bl(e) { if (!Array.isArray(e) || e.length !== 2048 || typeof e[0] != `string`)
    throw TypeError(`Wordlist: expected array of 2048 strings`); return e.forEach(e => { if (typeof e != `string`)
    throw TypeError(`wordlist: non-string element: ` + e); }), Pa.chain(Pa.checksum(1, zl), Pa.radix2(11, !0), Pa.alphabet(e)); }
function Vl(e, t) { let { words: n } = Il(e), r = Bl(t).decode(n); return Ll(r), r; }
function Hl(e, t) { return Ll(e), Bl(t).encode(e).join(Pl(t) ? `　` : ` `); }
function Ul(e, t) { try {
    Vl(e, t);
}
catch {
    return !1;
} return !0; }
var Wl = e => Fl(`mnemonic` + e);
function Gl(e, t = ``) { return Nl(rs, Il(e).nfkd, Wl(t), { c: 2048, dkLen: 64 }); }
var Kl = Uint8Array.of();
var ql = Uint8Array.of(0);
var Jl = new Set([`__proto__`, `constructor`, `prototype`]);
var Yl = (e, t) => { if (typeof e != `string`)
    throw Error(`${t} should be string, got ${typeof e}`); if (e.includes(`..`))
    throw TypeError(`${t} ${e} cannot contain path parent ..`); if (e.includes(`/`))
    throw TypeError(`${t} ${e} cannot contain path separator /`); if (Jl.has(e))
    throw Error(`${t} ${e} is reserved`); };
function Xl(e, t) { if (e.length !== t.length)
    return !1; for (let n = 0; n < e.length; n++)
    if (e[n] !== t[n])
        return !1; return !0; }
function Zl(e) { if (e.length === 1) {
    let t = e[0];
    return (e, n = 0) => { let r = e.indexOf(t, n); return r === -1 ? void 0 : r; };
} let t = new Uint32Array(e.length); for (let n = 1, r = 0; n < e.length; n++) {
    for (; r && e[n] !== e[r];)
        r = t[r - 1];
    e[n] === e[r] && (t[n] = ++r);
} return (n, r = 0) => { for (let i = r, a = 0; i < n.length; i++) {
    for (; a && n[i] !== e[a];)
        a = t[a - 1];
    if (n[i] === e[a] && ++a === e.length)
        return i - e.length + 1;
} }; }
var Ql = (e, t, n = 0) => Zl(e)(t, n);
function $l(e, t) { let n = eu(e), r = eu(t); return n || r ? n && r && Xl(e, t) : e === t; }
function eu(e) { return e instanceof Uint8Array || ArrayBuffer.isView(e) && e.constructor.name === `Uint8Array` && `BYTES_PER_ELEMENT` in e && e.BYTES_PER_ELEMENT === 1; }
function tu(...e) { let t = 0; for (let n = 0; n < e.length; n++) {
    let r = e[n];
    if (!eu(r))
        throw Error(`Uint8Array expected`);
    t += r.length;
} let n = new Uint8Array(t); for (let t = 0, r = 0; t < e.length; t++) {
    let i = e[t];
    n.set(i, r), r += i.length;
} return n; }
var nu = e => new DataView(e.buffer, e.byteOffset, e.byteLength);
var ru = BigInt(0);
var iu = BigInt(1);
var au = BigInt(2);
var ou = BigInt(8);
var su = BigInt(10);
var cu = BigInt(255);
function lu(e) { return Object.prototype.toString.call(e) === `[object Object]`; }
function J(e) { return Number.isSafeInteger(e); }
var uu = (e, t) => Object.prototype.hasOwnProperty.call(e, t);
var du = Object.freeze({ equalBytes: Xl, isBytes: eu, isCoder: Cu, checkBounds: vu, concatBytes: tu, createView: nu, isPlainObject: lu });
var fu = e => { if (e !== null && typeof e != `string` && !Cu(e) && !eu(e) && !J(e))
    throw TypeError(`lengthCoder: expected null | number | Uint8Array | CoderType, got ${e} (${typeof e})`); if (typeof e == `number` && e < 0)
    throw Error(`lengthCoder: wrong length=${e}`); if (eu(e) && !e.length)
    throw Error(`lengthCoder: empty terminator`); return { encodeStream(t, n) { if (e === null)
        return; if (Cu(e))
        return e.encodeStream(t, n); let r; if (typeof e == `number` ? r = e : typeof e == `string` && (r = mu.resolve(t.stack, e)), typeof r == `bigint` && (r = Number(r)), r === void 0 || r !== n)
        throw t.err(`Wrong length: ${r} len=${e} exp=${n} (${typeof n})`); }, decodeStream(t) { let n; if (Cu(e) ? n = Number(e.decodeStream(t)) : typeof e == `number` ? n = e : typeof e == `string` && (n = mu.resolve(t.stack, e)), typeof n == `bigint` && (n = Number(n)), !J(n) || n < 0)
        throw t.err(`Wrong length: ${n}`); return n; } }; };
var pu = Object.freeze({ BITS: 32, FULL_MASK: -1 >>> 0, len: e => { if (!J(e) || e < 0)
        throw Error(`wrong len=${e}`); return Math.ceil(e / 32); }, create: e => new Uint32Array(pu.len(e)), clean: e => e.fill(0), debug: e => Array.from(e).map(e => (e >>> 0).toString(2).padStart(32, `0`)), checkLen: (e, t) => { if (pu.len(t) !== e.length)
        throw Error(`wrong length=${e.length}. Expected: ${pu.len(t)}`); }, chunkLen: (e, t, n) => { if (!J(e) || e < 0)
        throw Error(`wrong bsLen=${e}`); if (!J(t) || t < 0)
        throw Error(`wrong pos=${t}`); if (!J(n) || n < 0)
        throw Error(`wrong len=${n}`); if (t > e - n)
        throw Error(`wrong range=${t}/${n} of ${e}`); }, set: (e, t, n, r = !0) => !J(t) || t < 0 || t >= e.length || !r && (e[t] & n) !== 0 ? !1 : (e[t] |= n, !0), pos: (e, t) => ({ chunk: Math.floor((e + t) / 32), mask: 1 << 32 - (e + t) % 32 - 1 }), indices: (e, t, n = !1) => { pu.checkLen(e, t); let { FULL_MASK: r, BITS: i } = pu, a = i - t % i, o = a ? r >>> a << a : r, s = []; for (let t = 0; t < e.length; t++) {
        let r = e[t];
        if (n && (r = ~r), t === e.length - 1 && (r &= o), r !== 0)
            for (let e = 0; e < i; e++) {
                let n = 1 << i - e - 1;
                r & n && s.push(t * i + e);
            }
    } return s; }, range: e => { let t = [], n; for (let r of e)
        n === void 0 || r !== n.pos + n.length ? t.push(n = { pos: r, length: 1 }) : n.length += 1; return t; }, rangeDebug: (e, t, n = !1) => `[${pu.range(pu.indices(e, t, n)).map(e => `(${e.pos}/${e.length})`).join(`, `)}]`, setRange: (e, t, n, r, i = !0) => { if (pu.chunkLen(t, n, r), r === 0)
        return !0; let { FULL_MASK: a, BITS: o } = pu, s = n % o ? Math.floor(n / o) : void 0, c = n + r, l = c % o ? Math.floor(c / o) : void 0, u = (t, n) => t >= 0 && t < e.length && (e[t] & n) === 0; if (!i)
        if (s !== void 0 && s === l) {
            if (!u(s, a >>> o - r << o - r - n))
                return !1;
        }
        else {
            if (s !== void 0 && !u(s, a >>> n % o))
                return !1;
            let e = s === void 0 ? n / o : s + 1, t = l === void 0 ? c / o : l;
            for (let n = e; n < t; n++)
                if (!u(n, a))
                    return !1;
            if (l !== void 0 && s !== l && !u(l, a << o - c % o))
                return !1;
        } if (s !== void 0 && s === l)
        return pu.set(e, s, a >>> o - r << o - r - n, i); if (s !== void 0 && !pu.set(e, s, a >>> n % o, i))
        return !1; let d = s === void 0 ? n / o : s + 1, f = l === void 0 ? c / o : l; for (let t = d; t < f; t++)
        if (!pu.set(e, t, a, i))
            return !1; return !(l !== void 0 && s !== l && !pu.set(e, l, a << o - c % o, i)); } });
var mu = Object.freeze({ pushObj: (e, t, n) => { let r = { obj: t }; e.push(r), n((e, t) => { r.field = e, t(), r.field = void 0; }), e.pop(); }, path: e => { let t = []; for (let n of e)
        n.field !== void 0 && t.push(n.field === `` ? `""` : n.field); return t.join(`/`); }, err: (e, t, n) => { let r = `${e}(${mu.path(t)}): ${typeof n == `string` ? n : n.message}`, i = n instanceof TypeError ? TypeError(r) : n instanceof RangeError ? RangeError(r) : Error(r); if (n instanceof Error && n.stack) {
        let e = `${n.name}: ${n.message}`, t = `${i.name}: ${i.message}`;
        i.stack = n.stack.startsWith(e) ? `${t}${n.stack.slice(e.length)}` : n.stack;
    } return i; }, resolve: (e, t) => { let n = t.split(`/`), r = e.map(e => e.obj), i = 0; for (; i < n.length && n[i] === `..`; i++)
        r.pop(); let a = r.pop(); for (; i < n.length; i++) {
        if (!a || a[n[i]] === void 0)
            return;
        a = a[n[i]];
    } return a; } });
var hu = class e {
    pos = 0;
    data;
    opts;
    stack;
    parent;
    parentOffset;
    bitBuf = 0;
    bitPos = 0;
    bs;
    view;
    constructor(e, t = {}, n = [], r = void 0, i = 0) { this.data = e, this.opts = t, this.stack = n, this.parent = r, this.parentOffset = i, this.view = nu(e); }
    _enablePointers() { if (this.parent)
        return this.parent._enablePointers(); this.bs || (this.bs = pu.create(this.data.length), pu.setRange(this.bs, this.data.length, 0, this.pos, this.opts.allowMultipleReads)); }
    markBytesBS(e, t) { return this.parent ? this.parent.markBytesBS(this.parentOffset + e, t) : !t || !this.bs || pu.setRange(this.bs, this.data.length, e, t, !1); }
    markBytes(e) { let t = this.pos, n = this.markBytesBS(t, e); if (!this.opts.allowMultipleReads && !n)
        throw this.err(`multiple read pos=${t} len=${e}`); return this.pos += e, n; }
    pushObj(e, t) { return mu.pushObj(this.stack, e, t); }
    readView(e, t) { if (!J(e) || e < 0)
        throw this.err(`readView: wrong length=${e}`); if (this.pos + e > this.data.length)
        throw this.err(`readView: Unexpected end of buffer`); let n = t(this.view, this.pos); return this.markBytes(e), n; }
    absBytes(e) { if (!J(e) || e < 0 || e > this.data.length)
        throw Error(`Unexpected end of buffer`); return this.data.subarray(e); }
    finish() { if (!this.opts.allowUnreadBytes) {
        if (this.bitPos)
            throw this.err(`${this.bitPos} bits left after unpack: ${K.encode(this.data.subarray(this.pos))}`);
        if (this.bs && !this.parent) {
            let e = pu.indices(this.bs, this.data.length, !0);
            if (e.length) {
                let t = pu.range(e).map(({ pos: e, length: t }) => `(${e}/${t})[${K.encode(this.data.subarray(e, e + t))}]`).join(`, `);
                throw this.err(`unread byte ranges: ${t} (total=${this.data.length})`);
            }
            return;
        }
        if (!this.isEnd())
            throw this.err(`${this.leftBytes} bytes ${this.bitPos} bits left after unpack: ${K.encode(this.data.subarray(this.pos))}`);
    } }
    err(e) { return mu.err(`Reader`, this.stack, e); }
    offsetReader(t) { if (!J(t) || t < 0 || t > this.data.length)
        throw this.err(`offsetReader: Unexpected end of buffer`); return new e(this.absBytes(t), this.opts, this.stack, this, t); }
    bytes(e, t = !1) { if (this.bitPos)
        throw this.err(`readBytes: bitPos not empty`); if (!J(e) || e < 0)
        throw this.err(`readBytes: wrong length=${e}`); if (this.pos + e > this.data.length)
        throw this.err(`readBytes: Unexpected end of buffer`); let n = this.data.subarray(this.pos, this.pos + e); return t || this.markBytes(e), n; }
    byte(e = !1) { if (this.bitPos)
        throw this.err(`readByte: bitPos not empty`); if (this.pos + 1 > this.data.length)
        throw this.err(`readByte: Unexpected end of buffer`); let t = this.data[this.pos]; return e || this.markBytes(1), t; }
    get leftBytes() { return this.data.length - this.pos; }
    get totalBytes() { return this.data.length; }
    isEnd() { return this.pos >= this.data.length && !this.bitPos; }
    progress() { return this.pos * 8 - this.bitPos; }
    bits(e) { if (!J(e) || e < 0)
        throw this.err(`BitReader: wrong length=${e}`); if (e > 32)
        throw this.err(`BitReader: cannot read more than 32 bits in single call`); let t = 0; for (; e;) {
        this.bitPos ||= (this.bitBuf = this.byte(), 8);
        let n = Math.min(e, this.bitPos);
        this.bitPos -= n, t = t << n | this.bitBuf >> this.bitPos & 2 ** n - 1, this.bitBuf &= 2 ** this.bitPos - 1, e -= n;
    } return t >>> 0; }
    find(e, t = this.pos) { if (!eu(e))
        throw this.err(`find: needle is not bytes! ${e}`); if (this.bitPos)
        throw this.err(`find: bitPos not empty`); if (!e.length)
        throw this.err(`find: needle is empty`); if (!J(t) || t < 0)
        throw this.err(`find: wrong pos=${t}`); return Ql(e, this.data, t); }
};
var gu = class {
    pos = 0;
    stack;
    buffers = [];
    cleanBuffers = [];
    ptrs = [];
    bitBuf = 0;
    bitPos = 0;
    viewBuf = new Uint8Array(8);
    view;
    finished = !1;
    constructor(e = []) { this.stack = e, this.view = nu(this.viewBuf); }
    pushObj(e, t) { return mu.pushObj(this.stack, e, t); }
    writeView(e, t) { if (this.finished)
        throw this.err(`buffer: finished`); if (!J(e) || e < 0 || e > 8)
        throw Error(`wrong writeView length=${e}`); t(this.view); let n = this.viewBuf.slice(0, e); this.bytes(n), this.cleanBuffers.push(n), this.viewBuf.fill(0); }
    err(e) { return mu.err(`Writer`, this.stack, e); }
    bytes(e) { if (this.finished)
        throw this.err(`buffer: finished`); if (this.bitPos)
        throw this.err(`writeBytes: ends with non-empty bit buffer`); this.buffers.push(e), this.pos += e.length; }
    byte(e) { if (this.finished)
        throw this.err(`buffer: finished`); if (this.bitPos)
        throw this.err(`writeByte: ends with non-empty bit buffer`); if (!J(e) || e < 0 || e > 255)
        throw this.err(`writeByte: wrong value=${e}`); let t = new Uint8Array([e]); this.buffers.push(t), this.cleanBuffers.push(t), this.pos++; }
    finish(e = !0) { if (this.finished)
        throw this.err(`buffer: finished`); if (this.bitPos)
        throw this.err(`buffer: ends with non-empty bit buffer`); let t = this.buffers.concat(this.ptrs.map(e => e.buffer)), n = t.map(e => e.length).reduce((e, t) => e + t, 0), r = new Uint8Array(n); for (let e = 0, n = 0; e < t.length; e++) {
        let i = t[e];
        r.set(i, n), n += i.length;
    } for (let e = this.pos, t = 0; t < this.ptrs.length; t++) {
        let n = this.ptrs[t];
        r.set(n.ptr.encode(e), n.pos), e += n.buffer.length;
    } if (e) {
        for (let e of this.cleanBuffers)
            e.fill(0);
        this.buffers = [], this.cleanBuffers = [];
        for (let e of this.ptrs)
            e.buffer.fill(0);
        this.ptrs = [], this.finished = !0, this.bitBuf = 0;
    } return r; }
    bits(e, t) { if (this.finished)
        throw this.err(`buffer: finished`); if (!J(t) || t < 0)
        throw this.err(`writeBits: wrong length=${t}`); if (t > 32)
        throw this.err(`writeBits: cannot write more than 32 bits in single call`); if (!J(e) || e < 0)
        throw this.err(`writeBits: wrong value=${e}`); if (e >= 2 ** t)
        throw this.err(`writeBits: value (${e}) >= 2**bits (${t})`); for (; t;) {
        let n = Math.min(t, 8 - this.bitPos);
        if (this.bitBuf = this.bitBuf << n | e >> t - n, this.bitPos += n, t -= n, e &= 2 ** t - 1, this.bitPos === 8) {
            this.bitPos = 0;
            let e = new Uint8Array([this.bitBuf]);
            this.buffers.push(e), this.cleanBuffers.push(e), this.pos++;
        }
    } }
};
var _u = e => Uint8Array.from(e).reverse();
function vu(e, t, n) { if (n) {
    if (t <= ru)
        throw Error(`checkBounds: signed bits must be positive, got ${t}`);
    let n = au ** (t - iu);
    if (e < -n || e >= n)
        throw Error(`value out of signed bounds. Expected ${-n} <= ${e} < ${n}`);
}
else {
    let n = au ** t;
    if (ru > e || e >= n)
        throw Error(`value out of unsigned bounds. Expected 0 <= ${e} < ${n}`);
} }
function yu(e) { let t = e; return { encodeStream: t.encodeStream, decodeStream: t.decodeStream, size: t.size, encode: e => { let n = new gu; return t.encodeStream(n, e), n.finish(); }, decode: (e, n = {}) => { let r = new hu(e, n), i = t.decodeStream(r); return r.finish(), i; } }; }
function bu(e, t) { if (!Cu(e))
    throw TypeError(`validate: invalid inner value ${e}`); if (typeof t != `function`)
    throw TypeError(`validate: fn should be function`); return yu({ size: e.size, encodeStream: (n, r) => { let i; try {
        i = t(r);
    }
    catch (e) {
        throw n.err(e);
    } e.encodeStream(n, i); }, decodeStream: n => { let r = e.decodeStream(n); try {
        return t(r);
    }
    catch (e) {
        throw n.err(e);
    } } }); }
var xu = e => { let t = e; if (!lu(t))
    throw TypeError(`wrap: invalid inner value ${t}`); if (typeof t.encodeStream != `function`)
    throw TypeError(`wrap: encodeStream should be function`); if (typeof t.decodeStream != `function`)
    throw TypeError(`wrap: decodeStream should be function`); if (t.size !== void 0 && (!J(t.size) || t.size < 0))
    throw TypeError(`wrap: invalid size ${t.size}`); if (t.validate !== void 0 && typeof t.validate != `function`)
    throw TypeError(`wrap: validate should be function`); let n = yu(t); return t.validate === void 0 ? n : bu(n, t.validate); };
var Su = e => lu(e) && typeof e.decode == `function` && typeof e.encode == `function`;
function Cu(e) { return lu(e) && Su(e) && typeof e.encodeStream == `function` && typeof e.decodeStream == `function` && (e.size === void 0 || J(e.size) && e.size >= 0); }
function wu() { return { encode: e => { if (!Array.isArray(e))
        throw Error(`array expected`); let t = {}, n = new Set; for (let r of e) {
        if (!Array.isArray(r) || r.length !== 2)
            throw Error(`array of two elements expected`);
        let e = r[0], i = r[1];
        if (Yl(e, `dict: key`), n.has(e))
            throw Error(`key(${e}) appears twice in struct`);
        n.add(e), t[e] = i;
    } return t; }, decode: e => { if (!lu(e))
        throw Error(`expected plain object, got ${e}`); for (let t in e)
        Yl(t, `dict: key`); return Object.entries(e); } }; }
var Tu = Object.freeze({ encode: e => { if (typeof e != `bigint`)
        throw Error(`expected bigint, got ${typeof e}`); if (e > BigInt(2 ** 53 - 1))
        throw Error(`element bigger than MAX_SAFE_INTEGER=${e}`); if (e < BigInt(-(2 ** 53 - 1)))
        throw Error(`element smaller than MIN_SAFE_INTEGER=${e}`); return Number(e); }, decode: e => { if (!J(e))
        throw Error(`element is not a safe integer`); return BigInt(e); } });
function Eu(e) { if (!lu(e))
    throw Error(`plain object expected`); return { encode: t => { if (!J(t) || !(t in e))
        throw Error(`wrong value ${t}`); return e[t]; }, decode: t => { if (typeof t != `string`)
        throw Error(`wrong value ${typeof t}`); let n = e[t]; if (!uu(e, t) || !J(n))
        throw Error(`wrong value ${t}`); return n; } }; }
function Du(e, t = !1) { if (!J(e) || e < 0)
    throw Error(`decimal/precision: wrong value ${e}`); if (typeof t != `boolean`)
    throw Error(`decimal/round: expected boolean, got ${typeof t}`); let n = su ** BigInt(e); return { encode: t => { if (typeof t != `bigint`)
        throw Error(`expected bigint, got ${typeof t}`); let n = (t < ru ? -t : t).toString(10), r = n.length - e; r < 0 && (n = n.padStart(n.length - r, `0`), r = 0); let i = n.length - 1; for (; i >= r && n[i] === `0`; i--)
        ; let a = n.slice(0, r), o = n.slice(r, i + 1); return a ||= `0`, t < ru && (a = `-` + a), o ? `${a}.${o}` : a; }, decode: r => { if (typeof r != `string`)
        throw Error(`expected string, got ${typeof r}`); let i = !1; if (r.startsWith(`-`) && (i = !0, r = r.slice(1)), !/^(0|[1-9]\d*)(\.\d+)?$/.test(r))
        throw Error(`wrong string value=${r}`); let a = r.indexOf(`.`); a = a === -1 ? r.length : a; let o = r.slice(0, a), s = r.slice(a + 1).replace(/0+$/, ``), c = BigInt(o) * n; if (!t && s.length > e)
        throw Error(`fractional part cannot be represented with this precision (num=${r}, prec=${e})`); let l = Math.min(s.length, e), u = c + BigInt(s.slice(0, l)) * su ** BigInt(e - l); if (i && u === ru)
        throw Error(`negative zero is not allowed`); return i ? -u : u; } }; }
function Ou(e) { if (!Array.isArray(e))
    throw Error(`expected array, got ${typeof e}`); for (let t of e)
    if (!Su(t))
        throw Error(`wrong base coder ${t}`); return { encode: t => { for (let n of e) {
        let e;
        try {
            e = n.encode(t);
        }
        catch {
            continue;
        }
        if (e !== void 0)
            return e;
    } throw Error(`match/encode: cannot find match in ${t}`); }, decode: t => { for (let n of e) {
        let e;
        try {
            e = n.decode(t);
        }
        catch {
            continue;
        }
        if (e !== void 0)
            return e;
    } throw Error(`match/decode: cannot find match in ${t}`); } }; }
var ku = e => { if (!Su(e))
    throw Error(`BaseCoder expected`); return { encode: t => e.decode(t), decode: t => e.encode(t) }; };
var Au = Object.freeze({ dict: wu, numberBigint: Tu, tsEnum: Eu, decimal: Du, match: Ou, reverse: ku });
var ju = (e, t = !1, n = !1, r = !0) => { if (!J(e) || e <= 0)
    throw Error(`bigint/size: wrong value ${e}`); if (typeof t != `boolean`)
    throw Error(`bigint/le: expected boolean, got ${typeof t}`); if (typeof n != `boolean`)
    throw Error(`bigint/signed: expected boolean, got ${typeof n}`); if (typeof r != `boolean`)
    throw Error(`bigint/sized: expected boolean, got ${typeof r}`); let i = BigInt(e), a = au ** (ou * i - iu); return xu({ size: r ? e : void 0, encodeStream: (i, o) => { let s = o === ru; n && o < 0 && (o |= a); let c = []; for (let t = 0; t < e; t++)
        c.push(Number(o & cu)), o >>= ou; let l = new Uint8Array(c).reverse(); if (!r) {
        let e = 0;
        if (n) {
            for (; e < l.length - 1; e++) {
                let t = l[e + 1];
                if (!(l[e] === 0 && !(t & 128)) && !(l[e] === 255 && t & 128))
                    break;
            }
            l = s ? l.subarray(l.length) : l.subarray(e);
        }
        else {
            for (; e < l.length && l[e] === 0; e++)
                ;
            l = l.subarray(e);
        }
    } i.bytes(t ? l.reverse() : l); }, decodeStream: i => { let o = i.bytes(r ? e : Math.min(e, i.leftBytes)), s = t ? o : _u(o), c = ru; for (let e = 0; e < s.length; e++)
        c |= BigInt(s[e]) << ou * BigInt(e); let l = r || !o.length ? a : au ** (ou * BigInt(o.length) - iu); return n && c & l && (c = (c ^ l) - l), c; }, validate: e => { if (typeof e != `bigint`)
        throw Error(`bigint: invalid value: ${e}`); return vu(e, ou * i, !!n), e; } }); };
var Mu = Object.freeze(ju(32, !1));
var Nu = Object.freeze(ju(8, !0));
var Pu = Object.freeze(ju(8, !0, !0));
var Fu = (e, t) => xu({ size: e, encodeStream: (n, r) => n.writeView(e, e => t.write(e, r)), decodeStream: n => n.readView(e, t.read), validate: e => { if (typeof e != `number`)
        throw TypeError(`viewCoder: expected number, got ${typeof e}`); return t.validate && t.validate(e), e; } });
var Iu = (e, t, n) => { let r = e * 8, i = 2 ** (r - 1), a = e => { if (!J(e))
    throw TypeError(`sintView: value is not safe integer: ${e}`); if (e < -i || e >= i)
    throw RangeError(`sintView: value out of bounds. Expected ${-i} <= ${e} < ${i}`); }, o = 2 ** r; return Fu(e, { write: n.write, read: n.read, validate: t ? a : e => { if (!J(e))
        throw TypeError(`uintView: value is not safe integer: ${e}`); if (0 > e || e >= o)
        throw RangeError(`uintView: value out of bounds. Expected 0 <= ${e} < ${o}`); } }); };
var Y = Object.freeze(Iu(4, !1, { read: (e, t) => e.getUint32(t, !0), write: (e, t) => e.setUint32(0, t, !0) }));
var Lu = Object.freeze(Iu(4, !1, { read: (e, t) => e.getUint32(t, !1), write: (e, t) => e.setUint32(0, t, !1) }));
var Ru = Object.freeze(Iu(4, !0, { read: (e, t) => e.getInt32(t, !0), write: (e, t) => e.setInt32(0, t, !0) }));
var zu = Object.freeze(Iu(2, !1, { read: (e, t) => e.getUint16(t, !0), write: (e, t) => e.setUint16(0, t, !0) }));
var Bu = Object.freeze(Iu(1, !1, { read: (e, t) => e.getUint8(t), write: (e, t) => e.setUint8(0, t) }));
var Vu = (e, t = !1) => { if (typeof t != `boolean`)
    throw TypeError(`bytes/le: expected boolean, got ${typeof t}`); let n = fu(e), r = eu(e), i = r ? Uint8Array.from(e) : void 0, a = i && i.length ? Zl(i) : void 0; return xu({ size: typeof e == `number` ? e : void 0, encodeStream: (e, a) => { r || n.encodeStream(e, a.length), e.bytes(t ? _u(a) : a), i && e.bytes(i); }, decodeStream: r => { let a; if (i) {
        let e = r.find(i);
        if (e === void 0)
            throw r.err(`bytes: cannot find terminator`);
        a = r.bytes(e - r.pos), r.bytes(i.length);
    }
    else
        a = r.bytes(e === null ? r.leftBytes : n.decodeStream(r)); return t ? _u(a) : a; }, validate: e => { if (!eu(e))
        throw TypeError(`bytes: invalid value ${e}`); if (a) {
        let n = t ? _u(e) : e;
        if (a(n) !== void 0)
            throw Error(`bytes: value contains terminator`);
    } return e; } }); };
function Hu(e, t) { if (!Cu(t))
    throw Error(`prefix: invalid inner value ${t}`); return Wu(Vu(e), ku(t)); }
var Uu = (e, t = !1) => bu(Wu(Vu(e, t), Za), e => { if (typeof e != `string`)
    throw Error(`expected string, got ${typeof e}`); return e; });
function Wu(e, t) { if (!Cu(e))
    throw TypeError(`apply: invalid inner value ${e}`); if (!Su(t))
    throw TypeError(`apply: invalid base value ${t}`); return xu({ size: e.size, encodeStream: (n, r) => { let i; try {
        i = t.decode(r);
    }
    catch (e) {
        throw n.err(`` + e);
    } return e.encodeStream(n, i); }, decodeStream: n => { let r = e.decodeStream(n); try {
        return t.encode(r);
    }
    catch (e) {
        throw n.err(`` + e);
    } } }); }
var Gu = (e, t = !1) => { if (!eu(e))
    throw TypeError(`flag/flagValue: expected Uint8Array, got ${typeof e}`); if (e.length === 0)
    throw Error(`flag/flagValue: empty marker`); if (typeof t != `boolean`)
    throw TypeError(`flag/xor: expected boolean, got ${typeof t}`); return xu({ size: void 0, encodeStream: (n, r) => { !!r !== t && n.bytes(e); }, decodeStream: n => { let r = n.leftBytes >= e.length; return r && (r = Xl(n.bytes(e.length, !0), e), r && n.bytes(e.length)), r !== t; }, validate: e => { if (e !== void 0 && typeof e != `boolean`)
        throw Error(`flag: expected boolean value or undefined, got ${typeof e}`); return e; } }); };
function Ku(e, t, n) { if (typeof e != `string` && !Cu(e))
    throw TypeError(`flagged: wrong path=${e}`); if (!Cu(t))
    throw TypeError(`flagged: invalid inner value ${t}`); let r = n !== void 0; return xu({ encodeStream: (i, a) => { if (typeof e == `string`)
        mu.resolve(i.stack, e) ? t.encodeStream(i, a) : r && t.encodeStream(i, n);
    else {
        let o = a !== void 0;
        e.encodeStream(i, o), o ? t.encodeStream(i, a) : r && t.encodeStream(i, n);
    } }, decodeStream: n => { let i = !1; if (i = typeof e == `string` ? !!mu.resolve(n.stack, e) : e.decodeStream(n), i)
        return t.decodeStream(n); r && t.decodeStream(n); } }); }
function qu(e, t, n = !0) { if (!Cu(e))
    throw TypeError(`magic: invalid inner value ${e}`); if (typeof n != `boolean`)
    throw TypeError(`magic: expected boolean, got ${typeof n}`); return xu({ size: e.size, encodeStream: (n, r) => e.encodeStream(n, t), decodeStream: r => { let i = e.decodeStream(r), a = typeof i == `object` && !!i && !eu(i), o = typeof t == `object` && !!t && !eu(t); if (n && (!a || !o) && !$l(i, t))
        throw r.err(`magic: invalid value: ${i} !== ${t}`); }, validate: e => { if (e !== void 0)
        throw Error(`magic: wrong value=${typeof e}`); return e; } }); }
function Ju(e) { let t = 0; for (let n of e) {
    if (n.size === void 0)
        return;
    if (!J(n.size))
        throw Error(`sizeof: wrong element size=${t}`);
    t += n.size;
} return t; }
function Yu(e) { if (!lu(e))
    throw TypeError(`struct: expected plain object, got ${e}`); let t = []; for (let n in e) {
    if (Yl(n, `struct: field`), !Cu(e[n]))
        throw TypeError(`struct: field ${n} is not CoderType`);
    t.push(e[n]);
} return xu({ size: Ju(t), encodeStream: (t, n) => { t.pushObj(n, r => { for (let i in e)
        r(i, () => e[i].encodeStream(t, n[i])); }); }, decodeStream: t => { let n = {}; return t.pushObj(n, r => { for (let i in e)
        r(i, () => n[i] = e[i].decodeStream(t)); }), n; }, validate: e => { if (typeof e != `object` || !e)
        throw Error(`struct: invalid value ${e}`); return e; } }); }
function Xu(e, t) { if (!Cu(t))
    throw TypeError(`array: invalid inner value ${t}`); let n = fu(typeof e == `string` ? `../${e}` : e); if (e === null && t.size === 0)
    throw Error(`array: null length cannot use zero-size inner`); return xu({ size: typeof e == `number` && t.size !== void 0 ? e * t.size : void 0, encodeStream: (r, i) => { let a = r; a.pushObj(i, o => { eu(e) || n.encodeStream(r, i.length); for (let n = 0; n < i.length; n++)
        o(`${n}`, () => { let o = i[n], s = r.pos; if (t.encodeStream(r, o), eu(e)) {
            if (e.length > a.pos - s)
                return;
            let t = a.finish(!1).subarray(s, a.pos);
            if (Xl(t.subarray(0, e.length), e))
                throw a.err(`array: inner element encoding same as separator. elm=${o} data=${t}`);
        } }); }), eu(e) && r.bytes(e); }, decodeStream: r => { let i = [], a = r; return a.pushObj(i, o => { if (e === null)
        for (let e = 0; !r.isEnd() && (o(`${e}`, () => { let e = a.progress(); if (i.push(t.decodeStream(r)), a.progress() === e)
            throw r.err(`array: inner decoder did not consume input`); }), !(t.size && r.leftBytes < t.size)); e++)
            ;
    else if (eu(e))
        for (let n = 0;; n++) {
            if (Xl(r.bytes(e.length, !0), e)) {
                r.bytes(e.length);
                break;
            }
            o(`${n}`, () => { let e = a.progress(); if (i.push(t.decodeStream(r)), a.progress() === e)
                throw r.err(`array: inner decoder did not consume input`); });
        }
    else {
        let e;
        o(`arrayLen`, () => e = n.decodeStream(r));
        for (let n = 0; n < e; n++)
            o(`${n}`, () => i.push(t.decodeStream(r)));
    } }), i; }, validate: e => { if (!Array.isArray(e))
        throw Error(`array: invalid value ${e}`); return e; } }); }
var Zu = qc.Point;
var Qu = Zu.Fn;
var $u = Zu.Fn.ORDER;
var ed = e => e % 2n == 0n;
var X = du.isBytes;
var td = du.concatBytes;
var nd = du.equalBytes;
var rd = ns;
var id = e => bl(rd(e));
var ad = (...e) => rd(rd(td(...e)));
var od = e => al.getPublicKey(e);
var sd = (e, t) => qc.getPublicKey(e, t);
var cd = e => e.r < $u / 2n;
function ld(e, t, n = !1) { q(e, 32, `hash`); let r = qc.Signature.fromBytes(qc.sign(e, t, { prehash: !1 })); if (n && !cd(r)) {
    let n = new Uint8Array(32), i = 0;
    for (; !cd(r);)
        if (n.set(Y.encode(i++)), r = qc.Signature.fromBytes(qc.sign(e, t, { prehash: !1, extraEntropy: n })), i > 4294967295)
            throw Error(`lowR counter overflow: report the error`);
} return r.toBytes(`der`); }
var ud = (e, t, n) => al.sign(e, t, n);
var dd = (e, ...t) => al.utils.taggedHash(e, ...t);
var fd = Object.freeze({ ecdsa: 0, schnorr: 1 });
function pd(e, t) { let n = e.length; if (t === fd.ecdsa) {
    if (n === 32)
        throw RangeError(`Expected non-Schnorr key`);
    return Zu.fromBytes(e), e;
} if (t === fd.schnorr) {
    if (n !== 32)
        throw RangeError(`Expected 32-byte Schnorr key`);
    return al.utils.lift_x(_s(e)), e;
} throw TypeError(`Unknown key type`); }
function md(e, t) { let n = _s(al.utils.taggedHash(`TapTweak`, e, t)); if (n >= $u)
    throw Error(`tweak higher than curve order`); return n; }
function hd(e, t = Uint8Array.of()) { let n = al.utils; q(e, 32, `privKey`); let r = _s(e), i = Zu.BASE.multiply(r), a = ed(i.y) ? r : Qu.neg(r), o = md(n.pointToBytes(i), t); return ys(Qu.add(a, o), 32); }
function gd(e, t) { let n = al.utils; q(e, 32, `pubKey`); let r = md(e, t), i = n.lift_x(_s(e)).add(Zu.BASE.multiply(r)), a = +!ed(i.y); return [n.pointToBytes(i), a]; }
var _d = Object.freeze({ bech32: `bc`, pubKeyHash: 0, scriptHash: 5, wif: 128 });
function vd(e, t) { if (!X(e) || !X(t))
    throw TypeError(`cmp: wrong type a=${typeof e} b=${typeof t}`); let n = Math.min(e.length, t.length); for (let r = 0; r < n; r++)
    if (e[r] != t[r])
        return Math.sign(e[r] - t[r]); return Math.sign(e.length - t.length); }
function yd(e) { let t = Object.create(null); for (let n in e) {
    if (t[e[n]] !== void 0)
        throw Error(`duplicate key`);
    t[e[n]] = n;
} return t; }
var bd = Object.freeze({ OP_0: 0, PUSHDATA1: 76, PUSHDATA2: 77, PUSHDATA4: 78, "1NEGATE": 79, RESERVED: 80, OP_1: 81, OP_2: 82, OP_3: 83, OP_4: 84, OP_5: 85, OP_6: 86, OP_7: 87, OP_8: 88, OP_9: 89, OP_10: 90, OP_11: 91, OP_12: 92, OP_13: 93, OP_14: 94, OP_15: 95, OP_16: 96, NOP: 97, VER: 98, IF: 99, NOTIF: 100, VERIF: 101, VERNOTIF: 102, ELSE: 103, ENDIF: 104, VERIFY: 105, RETURN: 106, TOALTSTACK: 107, FROMALTSTACK: 108, "2DROP": 109, "2DUP": 110, "3DUP": 111, "2OVER": 112, "2ROT": 113, "2SWAP": 114, IFDUP: 115, DEPTH: 116, DROP: 117, DUP: 118, NIP: 119, OVER: 120, PICK: 121, ROLL: 122, ROT: 123, SWAP: 124, TUCK: 125, CAT: 126, SUBSTR: 127, LEFT: 128, RIGHT: 129, SIZE: 130, INVERT: 131, AND: 132, OR: 133, XOR: 134, EQUAL: 135, EQUALVERIFY: 136, RESERVED1: 137, RESERVED2: 138, "1ADD": 139, "1SUB": 140, "2MUL": 141, "2DIV": 142, NEGATE: 143, ABS: 144, NOT: 145, "0NOTEQUAL": 146, ADD: 147, SUB: 148, MUL: 149, DIV: 150, MOD: 151, LSHIFT: 152, RSHIFT: 153, BOOLAND: 154, BOOLOR: 155, NUMEQUAL: 156, NUMEQUALVERIFY: 157, NUMNOTEQUAL: 158, LESSTHAN: 159, GREATERTHAN: 160, LESSTHANOREQUAL: 161, GREATERTHANOREQUAL: 162, MIN: 163, MAX: 164, WITHIN: 165, RIPEMD160: 166, SHA1: 167, SHA256: 168, HASH160: 169, HASH256: 170, CODESEPARATOR: 171, CHECKSIG: 172, CHECKSIGVERIFY: 173, CHECKMULTISIG: 174, CHECKMULTISIGVERIFY: 175, NOP1: 176, CHECKLOCKTIMEVERIFY: 177, CHECKSEQUENCEVERIFY: 178, NOP4: 179, NOP5: 180, NOP6: 181, NOP7: 182, NOP8: 183, NOP9: 184, NOP10: 185, CHECKSIGADD: 186, INVALID: 255 });
var xd = Object.freeze(yd(bd));
function Sd(e = 6, t = !1) { return xu({ encodeStream: (e, t) => { if (t === 0n)
        return; let n = t < 0, r = BigInt(t), i = []; for (let e = n ? -r : r; e; e >>= 8n)
        i.push(Number(e & 255n)); i[i.length - 1] >= 128 ? i.push(n ? 128 : 0) : n && (i[i.length - 1] |= 128), e.bytes(new Uint8Array(i)); }, decodeStream: n => { let r = n.leftBytes; if (r > e)
        throw Error(`ScriptNum: number (${r}) bigger than limit=${e}`); if (r === 0)
        return 0n; if (t) {
        let e = n.bytes(r, !0);
        if (!(e[e.length - 1] & 127) && (r <= 1 || !(e[e.length - 2] & 128)))
            throw Error(`Non-minimally encoded ScriptNum`);
    } let i = 0, a = 0n; for (let e = 0; e < r; ++e)
        i = n.byte(), a |= BigInt(i) << 8n * BigInt(e); return i >= 128 && (a &= 2n ** BigInt(r * 8) - 1n >> 1n, a = -a), a; } }); }
function Cd(e, t = 4, n = !0) { if (typeof e == `number`)
    return e; if (X(e))
    try {
        let r = Sd(t, n).decode(e);
        return r > 2 ** 53 - 1 ? void 0 : Number(r);
    }
    catch {
        return;
    } }
var wd = (e, t) => { if (bd.OP_0 < e && e <= bd.PUSHDATA4) {
    if (e < bd.PUSHDATA1)
        return e;
    if (e === bd.PUSHDATA1)
        return t(1);
    if (e === bd.PUSHDATA2)
        return t(2);
    if (e === bd.PUSHDATA4)
        return t(4);
    throw Error(`Should be not possible`);
} };
var Td = Object.freeze(xu({ encodeStream: (e, t) => { for (let n of t) {
        if (typeof n == `string`) {
            if (bd[n] === void 0)
                throw Error(`Unknown opcode=${n}`);
            e.byte(bd[n]);
            continue;
        }
        if (typeof n == `number`) {
            if (n === 0) {
                e.byte(0);
                continue;
            }
            if (n === -1) {
                e.byte(bd[`1NEGATE`]);
                continue;
            }
            if (1 <= n && n <= 16) {
                e.byte(bd.OP_1 - 1 + n);
                continue;
            }
        }
        if (typeof n == `number` && (n = Sd().encode(BigInt(n))), !X(n))
            throw Error(`Wrong Script OP=${n} (${typeof n})`);
        let t = n.length;
        t < bd.PUSHDATA1 ? e.byte(t) : t <= 255 ? (e.byte(bd.PUSHDATA1), e.byte(t)) : t <= 65535 ? (e.byte(bd.PUSHDATA2), e.bytes(zu.encode(t))) : (e.byte(bd.PUSHDATA4), e.bytes(Y.encode(t))), e.bytes(n);
    } }, decodeStream: e => { let t = []; for (; !e.isEnd();) {
        let n = e.byte(), r = wd(n, t => t === 1 ? Bu.decodeStream(e) : t === 2 ? zu.decodeStream(e) : Y.decodeStream(e));
        if (r !== void 0)
            t.push(e.bytes(r));
        else if (n === 0)
            t.push(0);
        else if (bd.OP_1 <= n && n <= bd.OP_16)
            t.push(n - (bd.OP_1 - 1));
        else {
            let e = xd[n];
            if (e === void 0)
                throw Error(`Unknown opcode=${n.toString(16)}`);
            t.push(e);
        }
    } return t; } }));
var Ed = { 253: [253, 2, 253n, 65535n], 254: [254, 4, 65536n, 4294967295n], 255: [255, 8, 4294967296n, 18446744073709551615n] };
var Dd = Object.freeze(xu({ encodeStream: (e, t) => { if (typeof t == `number` && (t = BigInt(t)), 0n <= t && t <= 252n)
        return e.byte(Number(t)); for (let [n, r, i, a] of Object.values(Ed))
        if (!(i > t || t > a)) {
            e.byte(n);
            for (let n = 0; n < r; n++)
                e.byte(Number(t >> 8n * BigInt(n) & 255n));
            return;
        } throw e.err(`VarInt too big: ${t}`); }, decodeStream: e => { let t = e.byte(); if (t <= 252)
        return BigInt(t); let [n, r, i] = Ed[t], a = 0n; for (let t = 0; t < r; t++)
        a |= BigInt(e.byte()) << 8n * BigInt(t); if (a < i)
        throw e.err(`Wrong CompactSize(${8 * r})`); return a; } }));
var Od = Object.freeze(Wu(Dd, Au.numberBigint));
var kd = Object.freeze(Vu(Dd));
var Ad = kd;
var jd = Object.freeze(Xu(Od, kd));
var Md = jd;
var Nd = e => Xu(Dd, e);
var Pd = Object.freeze(Yu({ txid: Vu(32, !0), index: Y, finalScriptSig: kd, sequence: Y }));
var Fd = Object.freeze(Yu({ amount: Nu, script: kd }));
var Id = Yu({ version: Ru, segwitFlag: Gu(new Uint8Array([0, 1])), inputs: Nd(Pd), outputs: Nd(Fd), witnesses: Ku(`segwitFlag`, Xu(`inputs/length`, jd)), lockTime: Y });
function Ld(e) { if (e.segwitFlag && e.witnesses && e.witnesses.every(e => !e.length))
    throw Error(`Segwit flag with only empty witness fields`); return e; }
var Rd = Object.freeze(bu(Id, Ld));
var zd = Object.freeze(Yu({ version: Ru, inputs: Nd(Pd), outputs: Nd(Fd), lockTime: Y }));
var Bd = bu(Vu(null), e => pd(e, fd.ecdsa));
var Vd = bu(Vu(33), e => pd(e, fd.ecdsa));
var Hd = bu(Vu(32), e => pd(e, fd.schnorr));
var Ud = bu(Vu(null), e => { if (e.length !== 64 && e.length !== 65)
    throw Error(`Schnorr signature should be 64 or 65 bytes long`); return e; });
var Wd = Md;
var Gd = Yu({ fingerprint: Lu, path: Xu(null, Y) });
var Kd = Yu({ hashes: Xu(Od, Vu(32)), der: Gd });
var qd = bu(Yu({ version: Lu, depth: Bu, parentFingerprint: Lu, childNumber: Lu, chainCode: Vu(32), publicKey: Vd }), e => { if (e.depth === 0 && e.parentFingerprint !== 0)
    throw Error(`GlobalXPUB: depth=0 requires parentFingerprint=0`); if (e.depth === 0 && e.childNumber !== 0)
    throw Error(`GlobalXPUB: depth=0 requires childNumber=0`); return e; });
var Jd = Yu({ pubKey: Hd, leafHash: Vu(32) });
var Yd = Yu({ version: Bu, internalKey: Vu(32), merklePath: Xu(null, Vu(32)) });
var Xd = Object.freeze(bu(Yd, e => { if (e.merklePath.length > 128)
    throw Error(`TaprootControlBlock: merklePath should be of length 0..128 (inclusive)`); return e; }));
var Zd = bu(Xu(null, Yu({ depth: Bu, version: Bu, script: Ad })), e => { if (e.length < 1)
    throw Error(`tapTree: expected at least one tuple`); let t = Array(e[0].depth).fill(0), n = e[0].depth; for (let r = 1; r < e.length; r++) {
    let { depth: i } = e[r];
    i > n && (n = i);
    let a = t.length - 1;
    for (; a >= 0 && t[a] === 1;)
        a--;
    if (a < 0)
        throw Error(`tapTree: tuples must be in DFS order`);
    let o = t.slice(0, a);
    if (o.push(1), i < o.length)
        throw Error(`tapTree: tuples must be in DFS order`);
    for (; o.length < i;)
        o.push(0);
    t = o;
} let r = 0n; for (let t = 0; t < e.length; t++)
    r += 1n << BigInt(n - e[t].depth); if (r !== 1n << BigInt(n))
    throw Error(`tapTree: tuples must describe a complete binary tree`); return e; });
var Qd = Vu(null);
var $d = Vu(20);
var ef = Vu(32);
var Z = (e, t, n, r, i, a) => Object.freeze([e, t && typeof t == `object` ? Object.freeze(t) : t, n && typeof n == `object` ? Object.freeze(n) : n, Object.freeze([...r]), Object.freeze([...i]), a]);
var tf = Object.freeze({ unsignedTx: Z(0, !1, zd, [0], [0], !1), xpub: Z(1, qd, Gd, [], [0, 2], !1), txVersion: Z(2, !1, Y, [2], [2], !1), fallbackLocktime: Z(3, !1, Y, [], [2], !1), inputCount: Z(4, !1, Od, [2], [2], !1), outputCount: Z(5, !1, Od, [2], [2], !1), txModifiable: Z(6, !1, Bu, [], [2], !1), version: Z(251, !1, Y, [], [0, 2], !1), proprietary: Z(252, Qd, Qd, [], [0, 2], !1) });
var nf = Object.freeze({ nonWitnessUtxo: Z(0, !1, Rd, [], [0, 2], !1), witnessUtxo: Z(1, !1, Fd, [], [0, 2], !1), partialSig: Z(2, Bd, Qd, [], [0, 2], !1), sighashType: Z(3, !1, Y, [], [0, 2], !1), redeemScript: Z(4, !1, Qd, [], [0, 2], !1), witnessScript: Z(5, !1, Qd, [], [0, 2], !1), bip32Derivation: Z(6, Bd, Gd, [], [0, 2], !1), finalScriptSig: Z(7, !1, Qd, [], [0, 2], !1), finalScriptWitness: Z(8, !1, Wd, [], [0, 2], !1), porCommitment: Z(9, !1, Qd, [], [0, 2], !1), ripemd160: Z(10, $d, Qd, [], [0, 2], !1), sha256: Z(11, ef, Qd, [], [0, 2], !1), hash160: Z(12, $d, Qd, [], [0, 2], !1), hash256: Z(13, ef, Qd, [], [0, 2], !1), txid: Z(14, !1, Vu(32, !0), [2], [2], !0), index: Z(15, !1, Y, [2], [2], !0), sequence: Z(16, !1, Y, [], [2], !0), requiredTimeLocktime: Z(17, !1, Y, [], [2], !1), requiredHeightLocktime: Z(18, !1, Y, [], [2], !1), tapKeySig: Z(19, !1, Ud, [], [0, 2], !1), tapScriptSig: Z(20, Jd, Ud, [], [0, 2], !1), tapLeafScript: Z(21, Xd, Qd, [], [0, 2], !1), tapBip32Derivation: Z(22, Hd, Kd, [], [0, 2], !1), tapInternalKey: Z(23, !1, Hd, [], [0, 2], !1), tapMerkleRoot: Z(24, !1, ef, [], [0, 2], !1), proprietary: Z(252, Qd, Qd, [], [0, 2], !1) });
var rf = Object.freeze([`txid`, `sequence`, `index`, `witnessUtxo`, `nonWitnessUtxo`, `finalScriptSig`, `finalScriptWitness`, `unknown`]);
var af = Object.freeze([`partialSig`, `finalScriptSig`, `finalScriptWitness`, `tapKeySig`, `tapScriptSig`]);
var of = Object.freeze({ redeemScript: Z(0, !1, Qd, [], [0, 2], !1), witnessScript: Z(1, !1, Qd, [], [0, 2], !1), bip32Derivation: Z(2, Bd, Gd, [], [0, 2], !1), amount: Z(3, !1, Pu, [2], [2], !0), script: Z(4, !1, Qd, [2], [2], !0), tapInternalKey: Z(5, !1, Hd, [], [0, 2], !1), tapTree: Z(6, !1, Zd, [], [0, 2], !1), tapBip32Derivation: Z(7, Hd, Kd, [], [0, 2], !1), proprietary: Z(252, Qd, Qd, [], [0, 2], !1) });
var sf = Object.freeze([]);
var cf = Xu(ql, Yu({ key: Hu(Od, Yu({ type: Od, key: Vu(null) })), value: Vu(Od) }));
function lf(e) { let [t, n, r, i, a, o] = e; return { type: t, kc: n, vc: r, reqInc: i, allowInc: a, silentIgnore: o }; }
var uf = Yu({ type: Od, key: Vu(null) });
function df(e) { let t = {}; for (let n in e) {
    let [r, i, a] = e[n];
    t[r] = [n, i, a];
} return xu({ encodeStream: (t, n) => { let r = n, i = [], a = {}, o = (e, t) => { let n = t, r = K.encode(uf.encode(e)); if (a[r])
        throw Error(`PSBT: duplicate key=${r}`); a[r] = !0, i.push({ key: e, value: n }); }; for (let t in e) {
        let n = r[t];
        if (n === void 0)
            continue;
        let [i, a, s] = e[t];
        if (!a)
            o({ type: i, key: Kl }, s.encode(n));
        else {
            let e = n.map(([e, t]) => [a.encode(e), s.encode(t)]);
            e.sort((e, t) => vd(e[0], t[0]));
            for (let [t, n] of e)
                o({ key: t, type: i }, n);
        }
    } if (r.unknown) {
        r.unknown.sort((e, t) => vd(e[0].key, t[0].key));
        for (let [e, t] of r.unknown)
            o(e, t);
    } cf.encodeStream(t, i); }, decodeStream: e => { let n = cf.decodeStream(e), r = {}, i = {}, a = {}; for (let e of n) {
        let n = K.encode(uf.encode(e.key));
        if (a[n])
            throw Error(`PSBT: duplicate key=${n}`);
        a[n] = !0;
        let o = `unknown`, s = e.key.key, c = e.value;
        if (t[e.key.type]) {
            let [n, a, l] = t[e.key.type];
            if (o = n, !a && s.length)
                throw Error(`PSBT: Non-empty key for ${o} (key=${K.encode(s)} value=${K.encode(c)}`);
            if (s = a ? a.decode(s) : void 0, c = l.decode(c), !a) {
                if (r[o])
                    throw Error(`PSBT: Same keys: ${o} (key=${s} value=${c})`);
                r[o] = c, i[o] = !0;
                continue;
            }
        }
        else
            s = { type: e.key.type, key: e.key.key };
        if (i[o])
            throw Error(`PSBT: Key type with empty key and no key=${o} val=${c}`);
        r[o] || (r[o] = []), r[o].push([s, c]);
    } return r; } }); }
var ff = Object.freeze(bu(df(nf), e => { if (e.finalScriptWitness && !e.finalScriptWitness.length)
    throw Error(`validateInput: empty finalScriptWitness`); if (e.partialSig && !e.partialSig.length)
    throw Error(`Empty partialSig`); if (e.partialSig)
    for (let [t] of e.partialSig)
        pd(t, fd.ecdsa); if (e.bip32Derivation)
    for (let [t] of e.bip32Derivation)
        pd(t, fd.ecdsa); if (e.requiredTimeLocktime !== void 0 && e.requiredTimeLocktime < 5e8)
    throw Error(`validateInput: wrong timeLocktime=${e.requiredTimeLocktime}`); if (e.requiredHeightLocktime !== void 0 && (e.requiredHeightLocktime <= 0 || e.requiredHeightLocktime >= 5e8))
    throw Error(`validateInput: wrong heighLocktime=${e.requiredHeightLocktime}`); if (e.tapLeafScript)
    for (let [t, n] of e.tapLeafScript) {
        if ((t.version & 254) !== n[n.length - 1])
            throw Error(`validateInput: tapLeafScript version mimatch`);
        if (n[n.length - 1] & 1)
            throw Error(`validateInput: tapLeafScript version has parity bit!`);
    } return e; }));
var pf = Object.freeze(bu(df(of), e => { if (e.amount !== void 0 && e.amount < 0n)
    throw Error(`validateOutput: wrong amount=${e.amount}`); if (e.bip32Derivation)
    for (let [t] of e.bip32Derivation)
        pd(t, fd.ecdsa); return e; }));
var mf = bu(df(tf), e => { if ((e.version || 0) === 0) {
    if (!e.unsignedTx)
        throw Error(`PSBTv0: missing unsignedTx`);
    for (let t of e.unsignedTx.inputs)
        if (t.finalScriptSig && t.finalScriptSig.length)
            throw Error(`PSBTv0: input scriptSig found in unsignedTx`);
} for (let [t, n] of e.xpub || [])
    if (t.depth !== n.path.length)
        throw Error(`PSBT_GLOBAL_XPUB: xpub depth=${t.depth} must match derivation path length=${n.path.length}`); return e; });
var hf = Object.freeze(Yu({ magic: qu(Uu(new Uint8Array([255])), `psbt`), global: mf, inputs: Xu(`global/unsignedTx/inputs/length`, ff), outputs: Xu(null, pf) }));
var gf = Object.freeze(Yu({ magic: qu(Uu(new Uint8Array([255])), `psbt`), global: mf, inputs: Xu(`global/inputCount`, ff), outputs: Xu(`global/outputCount`, pf) }));
function _f(e, t, n) { let r = n; for (let n in r) {
    if (n === `unknown` || !t[n])
        continue;
    let { allowInc: r } = lf(t[n]);
    if (!r.includes(e))
        throw Error(`PSBTv${e}: field ${n} is not allowed`);
} for (let n in t) {
    let { reqInc: i } = lf(t[n]);
    if (i.includes(e) && r[n] === void 0)
        throw Error(`PSBTv${e}: missing required field ${n}`);
} }
function vf(e, t, n) { let r = n, i = {}; for (let n in r) {
    let a = n;
    if (a !== `unknown`) {
        if (!t[a])
            continue;
        let { allowInc: n, silentIgnore: r } = lf(t[a]);
        if (!n.includes(e)) {
            if (r)
                continue;
            throw Error(`Failed to serialize in PSBTv${e}: ${a} but versions allows inclusion=${n}`);
        }
    }
    i[a] = r[a];
} return i; }
function yf(e) { let t = e && e.global && e.global.version || 0; _f(t, tf, e.global); for (let n of e.inputs)
    _f(t, nf, n); for (let n of e.outputs)
    _f(t, of, n); let n = t ? e.global.inputCount : e.global.unsignedTx.inputs.length; if (e.inputs.length < n)
    throw Error(`Not enough inputs`); let r = e.inputs.slice(n); if (r.length > 1 || r.length && Object.keys(r[0]).length)
    throw Error(`Unexpected inputs left in tx=${r}`); let i = t ? e.global.outputCount : e.global.unsignedTx.outputs.length; if (e.outputs.length < i)
    throw Error(`Not outputs inputs`); let a = e.outputs.slice(i); if (a.length > 1 || a.length && Object.keys(a[0]).length)
    throw Error(`Unexpected outputs left in tx=${a}`); return e; }
function bf(e, t, n, r, i) { let a = t, o = n, s = r, c = { ...o, ...a }; for (let t in e) {
    let n = t, [r, i, l] = e[n], u = s && !s.includes(t);
    if (a[t] === void 0 && t in a) {
        if (u)
            throw Error(`Cannot remove signed field=${t}`);
        delete c[t];
    }
    else if (i) {
        let e = o && o[t] ? o[t] : [], r = a[n];
        if (r) {
            if (!Array.isArray(r))
                throw Error(`keyMap(${t}): KV pairs should be [k, v][]`);
            r = r.map(e => { if (e.length !== 2)
                throw Error(`keyMap(${t}): KV pairs should be [k, v][]`); return [typeof e[0] == `string` ? i.decode(K.decode(e[0])) : e[0], typeof e[1] == `string` ? l.decode(K.decode(e[1])) : e[1]]; });
            let a = {}, o = (e, t, r) => { if (a[e] === void 0) {
                a[e] = [t, r];
                return;
            } let i = K.encode(l.encode(a[e][1])), o = K.encode(l.encode(r)); if (i !== o)
                throw Error(`keyMap(${n}): same key=${e} oldVal=${i} newVal=${o}`); };
            for (let [t, n] of e)
                o(K.encode(i.encode(t)), t, n);
            for (let [e, t] of r) {
                let r = K.encode(i.encode(e));
                if (t === void 0) {
                    if (u)
                        throw Error(`Cannot remove signed field=${n}/${e}`);
                    delete a[r];
                }
                else
                    o(r, e, t);
            }
            c[n] = Object.values(a);
        }
    }
    else if (typeof c[t] == `string`)
        c[t] = l.decode(K.decode(c[t]));
    else if (u && t in a && o && o[t] !== void 0 && !nd(l.encode(a[t]), l.encode(o[t])))
        throw Error(`Cannot change signed field=${t}`);
} if (i && a.unknown) {
    let e = {};
    for (let [t, n] of o?.unknown || [])
        e[K.encode(uf.encode(t))] = [t, n];
    for (let [t, n] of a.unknown) {
        let r = K.encode(uf.encode(t));
        if (e[r] === void 0) {
            e[r] = [t, n];
            continue;
        }
        let i = K.encode(Qd.encode(e[r][1])), a = K.encode(Qd.encode(n));
        if (i !== a)
            throw Error(`keyMap(unknown): same key=${r} oldVal=${i} newVal=${a}`);
    }
    c.unknown = Object.values(e);
} for (let t in c)
    if (!e[t]) {
        if (i && t === `unknown`)
            continue;
        delete c[t];
    } return c; }
var xf = Object.freeze(bu(hf, yf));
var Sf = Object.freeze(bu(gf, yf));
var Cf = { encode(e) { if (!(e.length !== 2 || e[0] !== 1 || !X(e[1]) || K.encode(e[1]) !== `4e73`))
        return { type: `p2a`, script: Td.encode(e) }; }, decode: e => { if (e.type === `p2a`)
        return [1, K.decode(`4e73`)]; } };
function wf(e, t) { try {
    return pd(e, t), !0;
}
catch {
    return !1;
} }
var Tf = [Cf, { encode(e) { if (!(e.length !== 2 || !X(e[0]) || !wf(e[0], fd.ecdsa) || e[1] !== `CHECKSIG`))
            return { type: `pk`, pubkey: e[0] }; }, decode: e => { if (e.type === `pk`)
            return [e.pubkey, `CHECKSIG`]; } }, { encode(e) { if (!(e.length !== 5 || e[0] !== `DUP` || e[1] !== `HASH160` || !X(e[2])) && e[3] === `EQUALVERIFY` && e[4] === `CHECKSIG`)
            return { type: `pkh`, hash: e[2] }; }, decode: e => e.type === `pkh` ? [`DUP`, `HASH160`, e.hash, `EQUALVERIFY`, `CHECKSIG`] : void 0 }, { encode(e) { if (!(e.length !== 3 || e[0] !== `HASH160` || !X(e[1]) || e[2] !== `EQUAL`))
            return { type: `sh`, hash: e[1] }; }, decode: e => e.type === `sh` ? [`HASH160`, e.hash, `EQUAL`] : void 0 }, { encode(e) { if (!(e.length !== 2 || e[0] !== 0 || !X(e[1])) && e[1].length === 32)
            return { type: `wsh`, hash: e[1] }; }, decode: e => e.type === `wsh` ? [0, e.hash] : void 0 }, { encode(e) { if (!(e.length !== 2 || e[0] !== 0 || !X(e[1])) && e[1].length === 20)
            return { type: `wpkh`, hash: e[1] }; }, decode: e => e.type === `wpkh` ? [0, e.hash] : void 0 }, { encode(e) { let t = e.length - 1; if (e[t] !== `CHECKMULTISIG`)
            return; let n = e[0], r = e[t - 1]; if (typeof n != `number` || typeof r != `number`)
            return; let i = e.slice(1, -2); if (r === i.length) {
            for (let e of i)
                if (!X(e))
                    return;
            return { type: `ms`, m: n, pubkeys: i };
        } }, decode: e => e.type === `ms` ? [e.m, ...e.pubkeys, e.pubkeys.length, `CHECKMULTISIG`] : void 0 }, { encode(e) { if (!(e.length !== 2 || e[0] !== 1 || !X(e[1]) || e[1].length !== 32))
            return { type: `tr`, pubkey: e[1] }; }, decode: e => e.type === `tr` ? [1, e.pubkey] : void 0 }, { encode(e) { let t = e.length - 1; if (e[t] !== `CHECKSIG`)
            return; let n = []; for (let r = 0; r < t; r++) {
            let i = e[r];
            if (r & 1) {
                if (i !== `CHECKSIGVERIFY` || r === t - 1)
                    return;
                continue;
            }
            if (!X(i) || !wf(i, fd.schnorr))
                return;
            n.push(i);
        } if (n.length)
            return { type: `tr_ns`, pubkeys: n }; }, decode: e => { if (e.type !== `tr_ns`)
            return; let t = []; for (let n = 0; n < e.pubkeys.length - 1; n++)
            t.push(e.pubkeys[n], `CHECKSIGVERIFY`); return t.push(e.pubkeys[e.pubkeys.length - 1], `CHECKSIG`), t; } }, { encode(e) { let t = e.length - 1; if (e[t] !== `NUMEQUAL` || e[1] !== `CHECKSIG`)
            return; let n = [], r = Cd(e[t - 1]); if (typeof r == `number`) {
            for (let r = 0; r < t - 1; r++) {
                let t = e[r];
                if (r & 1) {
                    if (t !== (r === 1 ? `CHECKSIG` : `CHECKSIGADD`))
                        return;
                    continue;
                }
                if (!X(t))
                    return;
                n.push(t);
            }
            return { type: `tr_ms`, pubkeys: n, m: r };
        } }, decode: e => { if (e.type !== `tr_ms`)
            return; let t = [e.pubkeys[0], `CHECKSIG`]; for (let n = 1; n < e.pubkeys.length; n++)
            t.push(e.pubkeys[n], `CHECKSIGADD`); return t.push(e.m, `NUMEQUAL`), t; } }, { encode(e) { return { type: `unknown`, script: Td.encode(e) }; }, decode: e => e.type === `unknown` ? Td.decode(e.script) : void 0 }];
var Ef = Wu(Td, Au.match(Tf));
var Df = Object.freeze(bu(Ef, e => { if (e.type === `pk` && !wf(e.pubkey, fd.ecdsa))
    throw Error(`OutScript/pk: wrong key`); if ((e.type === `pkh` || e.type === `sh` || e.type === `wpkh`) && (!X(e.hash) || e.hash.length !== 20))
    throw Error(`OutScript/${e.type}: wrong hash`); if (e.type === `wsh` && (!X(e.hash) || e.hash.length !== 32))
    throw Error(`OutScript/wsh: wrong hash`); if (e.type === `tr` && (!X(e.pubkey) || !wf(e.pubkey, fd.schnorr)))
    throw Error(`OutScript/tr: wrong taproot public key`); if ((e.type === `ms` || e.type === `tr_ns` || e.type === `tr_ms`) && !Array.isArray(e.pubkeys))
    throw Error(`OutScript/multisig: wrong pubkeys array`); if (e.type === `ms`) {
    let t = e.pubkeys.length;
    for (let t of e.pubkeys)
        if (!wf(t, fd.ecdsa))
            throw Error(`OutScript/multisig: wrong pubkey`);
    if (eo(e.m, `m`), e.m <= 0 || t > 16 || e.m > t)
        throw Error(`OutScript/multisig: invalid params`);
} if (e.type === `tr_ns` || e.type === `tr_ms`) {
    for (let t of e.pubkeys)
        if (!wf(t, fd.schnorr))
            throw Error(`OutScript/${e.type}: wrong pubkey`);
} if (e.type === `tr_ms`) {
    let t = e.pubkeys.length;
    if (eo(e.m, `m`), e.m <= 0 || t > 999 || e.m > t)
        throw Error(`OutScript/tr_ms: invalid params`);
} return e; }));
function Of(e, t) { if (!nd(e.hash, rd(t)))
    throw Error(`checkScript: wsh wrong witnessScript hash`); let n = Df.decode(t); if (n.type === `tr` || n.type === `tr_ns` || n.type === `tr_ms`)
    throw Error(`checkScript: P2${n.type} cannot be wrapped in P2SH`); if (n.type === `wpkh` || n.type === `wsh` || n.type === `sh`)
    throw Error(`checkScript: P2${n.type} cannot be wrapped in P2WSH`); }
function kf(e, t, n) { let r = !1, i; if (e) {
    let a = Df.decode(e);
    if (a.type === `tr_ns` || a.type === `tr_ms` || a.type === `ms` || a.type == `pk`)
        throw Error(`checkScript: non-wrapped ${a.type}`);
    if (t) {
        if (a.type !== `sh`)
            throw Error(`checkScript: redeemScript without P2SH`);
        if (!nd(a.hash, id(t)))
            throw Error(`checkScript: sh wrong redeemScript hash`);
        if (i = Df.decode(t), i?.type === `tr` || i?.type === `tr_ns` || i?.type === `tr_ms`)
            throw Error(`checkScript: P2${i.type} cannot be wrapped in P2SH`);
        if (i?.type === `sh`)
            throw Error(`checkScript: P2SH cannot be wrapped in P2SH`);
    }
    a.type === `wsh` && (r = !0, n && Of(a, n));
} if (t && (i === void 0 && (i = Df.decode(t)), i?.type === `wsh` && (r = !0, n && Of(i, n))), n && !r)
    throw Error(`checkScript: witnessScript without P2WSH`); }
var Af = (e, t = _d) => { if (!wf(e, fd.ecdsa))
    throw Error(`P2WPKH: invalid publicKey`); if (e.length === 65)
    throw Error(`P2WPKH: uncompressed public key`); let n = id(e); return { type: `wpkh`, script: Df.encode({ type: `wpkh`, hash: n }), address: Lf(t).encode({ type: `wpkh`, hash: n }), hash: n }; };
var jf = e => { if (e === void 0)
    return 192; if (eo(e, `leafVersion`), e > 254 || e === 80 || e & 1)
    throw Error(`P2TR: invalid leafVersion=${e}`); return e; };
var Mf = (e, t = 192) => dd(`TapLeaf`, new Uint8Array([jf(t)]), Ad.encode(e));
var Nf = Ba(rd);
function Pf(e, t) { if (t.length < 2 || t.length > 40)
    throw Error(`Witness: invalid length`); if (e > 16)
    throw Error(`Witness: invalid version`); if (e === 0 && t.length !== 20 && t.length !== 32)
    throw Error(`Witness: invalid length for version`); }
function Ff(e, t, n = _d) { Pf(e, t); let r = e === 0 ? qa : Ja; return r.encode(n.bech32, [e].concat(r.toWords(t))); }
function If(e, t) { return Nf.encode(td(Uint8Array.from(t), e)); }
function Lf(e = _d) { return { encode(t) { let { type: n } = t; if (n === `wpkh` || n === `wsh`)
        return Ff(0, t.hash, e); if (n === `tr`)
        return Ff(1, t.pubkey, e); if (n === `pkh`)
        return If(t.hash, [e.pubKeyHash]); if (n === `sh`)
        return If(t.hash, [e.scriptHash]); throw Error(`Unknown address type=${n}`); }, decode(t) { if (t.length < 14 || t.length > 74)
        throw Error(`Invalid address length`); if (e.bech32 && t.toLowerCase().startsWith(`${e.bech32}1`)) {
        let n;
        try {
            if (n = qa.decode(t), n.words[0] !== 0)
                throw Error(`bech32: wrong version=${n.words[0]}`);
        }
        catch {
            if (n = Ja.decode(t), n.words[0] === 0)
                throw Error(`bech32m: wrong version=${n.words[0]}`);
        }
        if (n.prefix !== e.bech32)
            throw Error(`wrong bech32 prefix=${n.prefix}`);
        let [r, ...i] = n.words, a = qa.fromWords(i);
        if (Pf(r, a), r === 0 && a.length === 32)
            return { type: `wsh`, hash: a };
        if (r === 0 && a.length === 20)
            return { type: `wpkh`, hash: a };
        if (r === 1 && a.length === 32)
            return { type: `tr`, pubkey: a };
        throw Error(`Unknown witness program`);
    } let n = Nf.decode(t); if (n.length !== 21)
        throw Error(`Invalid base58 address`); if (n[0] === e.pubKeyHash)
        return { type: `pkh`, hash: n.slice(1) }; if (n[0] === e.scriptHash)
        return { type: `sh`, hash: n.slice(1) }; throw Error(`Invalid address prefix=${n[0]}`); } }; }
var Rf = new Uint8Array(32);
var zf = { amount: 18446744073709551615n, script: Kl };
var Bf = e => Math.ceil(e / 4);
var Vf = e => { let t = 0, n = []; for (let r = 0; r < e.length;) {
    let i = r, a = e[r++];
    if (a === bd.CODESEPARATOR) {
        t < i && n.push(e.subarray(t, i)), t = r;
        continue;
    }
    let o = wd(a, t => { if (r + t > e.length)
        throw Error(`Unexpected end of script`); let n = 0; for (let i = 0; i < t; i++)
        n |= e[r + i] << 8 * i; return r += t, n; });
    if (o !== void 0 && (r += o, r > e.length))
        throw Error(`Unexpected end of script`);
} return t === 0 ? e : (t < e.length && n.push(e.subarray(t)), n.length ? td(...n) : Kl); };
var Hf = 4294967295;
var Uf = (e, t) => e === void 0 ? t : e;
function Wf(e) { if (Array.isArray(e))
    return e.map(e => Wf(e)); if (X(e))
    return Uint8Array.from(e); if ([`number`, `bigint`, `boolean`, `string`, `undefined`].includes(typeof e) || e === null)
    return e; if (typeof e == `object`)
    return Object.fromEntries(Object.entries(e).map(([e, t]) => [e, Wf(t)])); throw Error(`cloneDeep: unknown type=${typeof e}`); }
var Q = Object.freeze({ DEFAULT: 0, ALL: 1, NONE: 2, SINGLE: 3, ANYONECANPAY: 128 });
var Gf = Object.freeze({ DEFAULT: Q.DEFAULT, ALL: Q.ALL, NONE: Q.NONE, SINGLE: Q.SINGLE, ALL_ANYONECANPAY: Q.ALL | Q.ANYONECANPAY, NONE_ANYONECANPAY: Q.NONE | Q.ANYONECANPAY, SINGLE_ANYONECANPAY: Q.SINGLE | Q.ANYONECANPAY });
var Kf = Object.freeze(yd(Gf));
function qf(e, t, n, r = Kl) { return nd(n, t) && (e = hd(e, r), t = od(e)), { privKey: e, pubKey: t }; }
function Jf(e) { if (e.script === void 0 || e.amount === void 0)
    throw Error(`Transaction/output: script and amount required`); return { script: e.script, amount: e.amount }; }
function Yf(e) { if (e.txid === void 0 || e.index === void 0)
    throw Error(`Transaction/input: txid and index required`); let t = { txid: e.txid, index: e.index, sequence: Uf(e.sequence, Hf), finalScriptSig: Uf(e.finalScriptSig, Kl) }; return Pd.encode(t), t; }
function Xf(e) { let t = e; for (let e in t) {
    let n = e;
    rf.includes(n) || delete t[n];
} }
var Zf = Yu({ txid: Vu(32, !0), index: Y });
function Qf(e) { if (typeof e != `number` || typeof Kf[e] != `string`)
    throw Error(`Invalid SigHash=${e}`); return e; }
function $f(e) { let t = e & 31; return { isAny: !!(e & Q.ANYONECANPAY), isNone: t === Q.NONE, isSingle: t === Q.SINGLE }; }
function ep(e) { if (e !== void 0 && {}.toString.call(e) !== `[object Object]`)
    throw Error(`Wrong object type for transaction options: ${e}`); let t = { ...e, version: Uf(e.version, 2), lockTime: Uf(e.lockTime, 0), PSBTVersion: Uf(e.PSBTVersion, 0) }; if (t.allowUnknowInput !== void 0 && (t.allowUnknownInputs = t.allowUnknowInput), t.allowUnknowOutput !== void 0 && (t.allowUnknownOutputs = t.allowUnknowOutput), typeof t.lockTime != `number`)
    throw Error(`Transaction lock time should be number`); if (Y.encode(t.lockTime), t.PSBTVersion !== 0 && t.PSBTVersion !== 2)
    throw Error(`Unknown PSBT version ${t.PSBTVersion}`); for (let e of [`allowUnknownVersion`, `allowUnknownOutputs`, `allowUnknownInputs`, `disableScriptCheck`, `bip174jsCompat`, `allowLegacyWitnessUtxo`, `lowR`]) {
    let n = t[e];
    if (n !== void 0 && typeof n != `boolean`)
        throw Error(`Transation options wrong type: ${e}=${n} (${typeof n})`);
} if (t.allowUnknownVersion ? typeof t.version == `number` : ![-1, 0, 1, 2, 3].includes(t.version))
    throw Error(`Unknown version: ${t.version}`); if (t.customScripts !== void 0) {
    let e = t.customScripts;
    if (!Array.isArray(e))
        throw Error(`wrong custom scripts type (expected array): customScripts=${e} (${typeof e})`);
    for (let t of e)
        if (typeof t.encode != `function` || typeof t.decode != `function` || t.finalizeTaproot !== void 0 && typeof t.finalizeTaproot != `function`)
            throw Error(`wrong script=${t} (${typeof t})`);
} return Object.freeze(t); }
function tp(e) { let t = e; if (t.nonWitnessUtxo && t.index !== void 0) {
    let e = t.nonWitnessUtxo.outputs.length - 1;
    if (t.index > e)
        throw Error(`validateInput: index(${t.index}) not in nonWitnessUtxo`);
    let n = t.nonWitnessUtxo.outputs[t.index];
    if (t.witnessUtxo && (!nd(t.witnessUtxo.script, n.script) || t.witnessUtxo.amount !== n.amount))
        throw Error(`validateInput: witnessUtxo different from nonWitnessUtxo`);
    if (t.txid) {
        if (t.nonWitnessUtxo.outputs.length - 1 < t.index)
            throw Error(`nonWitnessUtxo: incorect output index`);
        let e = ap.fromRaw(Rd.encode(t.nonWitnessUtxo), { allowUnknownOutputs: !0, disableScriptCheck: !0, allowUnknownInputs: !0 }), n = K.encode(t.txid);
        if (e.id !== n)
            throw Error(`nonWitnessUtxo: wrong txid, exp=${n} got=${e.id}`);
    }
} return t; }
function np(e) { let t = e; if (t.nonWitnessUtxo) {
    if (t.index === void 0)
        throw Error(`Unknown input index`);
    if (!Number.isSafeInteger(t.index) || t.index < 0 || t.index >= t.nonWitnessUtxo.outputs.length)
        throw Error(`Wrong input index=${t.index}`);
    return t.nonWitnessUtxo.outputs[t.index];
} if (t.witnessUtxo)
    return t.witnessUtxo; throw Error(`Cannot find previous output info`); }
function rp(e, t, n, r = !1, i = !1) { let a = e, o = t, s = n, { nonWitnessUtxo: c, txid: l } = a; typeof c == `string` && (c = K.decode(c)), X(c) && (c = Rd.decode(c)), !(`nonWitnessUtxo` in a) && c === void 0 && (c = o?.nonWitnessUtxo), typeof l == `string` && (l = K.decode(l)), l === void 0 && (l = o?.txid); let u = { ...o, ...a, nonWitnessUtxo: c, txid: l }; !(`nonWitnessUtxo` in a) && u.nonWitnessUtxo === void 0 && delete u.nonWitnessUtxo, u.sequence === void 0 && (u.sequence = Hf), u.tapMerkleRoot === null && delete u.tapMerkleRoot, u = bf(nf, u, o, s, i), ff.encode(u); let d; return u.nonWitnessUtxo && u.index !== void 0 ? d = u.nonWitnessUtxo.outputs[u.index] : u.witnessUtxo && (d = u.witnessUtxo), d && !r && kf(d && d.script, u.redeemScript, u.witnessScript), u; }
function ip(e, t = !1) { let n = e, r = `legacy`, i = Q.ALL, a = np(n), o = Df.decode(a.script), s = o.type, c = o, l = [o]; if (o.type === `tr`)
    return i = Q.DEFAULT, { txType: `taproot`, type: `tr`, last: o, lastScript: a.script, defaultSighash: i, sighash: n.sighashType || i }; {
    if ((o.type === `wpkh` || o.type === `wsh`) && (r = `segwit`), o.type === `sh`) {
        if (!n.redeemScript)
            throw Error(`inputType: sh without redeemScript`);
        let e = Df.decode(n.redeemScript);
        (e.type === `wpkh` || e.type === `wsh`) && (r = `segwit`), l.push(e), c = e, s += `-${e.type}`;
    }
    if (c.type === `wsh`) {
        if (!n.witnessScript)
            throw Error(`inputType: wsh without witnessScript`);
        let e = Df.decode(n.witnessScript);
        e.type === `wsh` && (r = `segwit`), l.push(e), c = e, s += `-${e.type}`;
    }
    let e = l[l.length - 1];
    if (e.type === `sh` || e.type === `wsh`)
        throw Error(`inputType: sh/wsh cannot be terminal type`);
    let a = Df.encode(e), u = { type: s, txType: r, last: e, lastScript: a, defaultSighash: i, sighash: n.sighashType || i };
    if (r === `legacy` && !t && !n.nonWitnessUtxo)
        throw Error(`Transaction/sign: legacy input without nonWitnessUtxo, can result in attack that forces paying higher fees. Pass allowLegacyWitnessUtxo=true, if you sure`);
    return u;
} }
var ap = class e {
    global = {};
    inputs = [];
    outputs = [];
    opts;
    constructor(e = {}) { let t = this.opts = ep(e); t.lockTime !== 0 && (this.global.fallbackLocktime = t.lockTime), this.global.txVersion = t.version; }
    static fromRaw(t, n = {}) { let r = Rd.decode(t), i = new e({ ...n, version: r.version, lockTime: r.lockTime }); for (let e of r.outputs)
        i.addOutput(e); if (i.outputs = r.outputs, i.inputs = r.inputs, r.witnesses)
        for (let e = 0; e < r.witnesses.length; e++)
            i.inputs[e].finalScriptWitness = r.witnesses[e]; return i; }
    static fromPSBT(t, n = {}) { let r; try {
        r = xf.decode(t);
    }
    catch (e) {
        try {
            r = Sf.decode(t);
        }
        catch {
            throw e;
        }
    } let i = r.global.version || 0; if (i !== 0 && i !== 2)
        throw Error(`Wrong PSBT version=${i}`); let a = r.global.unsignedTx, o = i === 0 ? a?.version : r.global.txVersion, s = i === 0 ? a?.lockTime : r.global.fallbackLocktime, c = new e({ ...n, version: o, lockTime: s, PSBTVersion: i }), l = i === 0 ? a?.inputs.length : r.global.inputCount; c.inputs = r.inputs.slice(0, l).map((e, t) => tp({ finalScriptSig: Kl, ...r.global.unsignedTx?.inputs[t], ...e })); let u = i === 0 ? a?.outputs.length : r.global.outputCount; return c.outputs = r.outputs.slice(0, u).map((e, t) => ({ ...e, ...r.global.unsignedTx?.outputs[t] })), c.global = { ...r.global, txVersion: o }, s !== 0 && (c.global.fallbackLocktime = s), c; }
    toPSBT(e = this.global.version || this.opts.PSBTVersion) { if (e !== 0 && e !== 2)
        throw Error(`Wrong PSBT version=${e}`); let t = this.inputs.map(t => vf(e, nf, tp(t))); for (let e of t)
        e.partialSig && !e.partialSig.length && delete e.partialSig, e.finalScriptSig && !e.finalScriptSig.length && delete e.finalScriptSig, e.finalScriptWitness && !e.finalScriptWitness.length && delete e.finalScriptWitness; let n = this.outputs.map(t => vf(e, of, t)), r = { ...this.global }; e === 0 ? (r.unsignedTx = zd.decode(zd.encode({ version: this.version, lockTime: this.lockTime, inputs: this.inputs.map(e => Yf(e)).map(e => ({ ...e, finalScriptSig: Kl })), outputs: this.outputs.map(e => Jf(e)) })), delete r.fallbackLocktime, delete r.txVersion, delete r.inputCount, delete r.outputCount, delete r.version) : (delete r.unsignedTx, r.version = e, r.txVersion = this.version, r.inputCount = this.inputs.length, r.outputCount = this.outputs.length, r.fallbackLocktime && r.fallbackLocktime === 0 && delete r.fallbackLocktime), this.opts.bip174jsCompat && (t.length || t.push({}), n.length || n.push({})); let i = { global: r, inputs: t, outputs: n }; return e === 0 ? xf.encode(i) : Sf.encode(i); }
    get lockTime() { let e = 0, t = 0, n = 0, r = 0; for (let i of this.inputs)
        i.requiredHeightLocktime && (e = Math.max(e, i.requiredHeightLocktime), t++), i.requiredTimeLocktime && (n = Math.max(n, i.requiredTimeLocktime), r++); return t && t >= r ? e : n === 0 ? this.global.fallbackLocktime || 0 : n; }
    get version() { if (this.global.txVersion === void 0)
        throw Error(`No global.txVersion`); return this.global.txVersion; }
    inputStatus(e) { this.checkInputIdx(e); let t = this.inputs[e]; return t.finalScriptSig && t.finalScriptSig.length || t.finalScriptWitness && t.finalScriptWitness.length ? `finalized` : t.tapKeySig || t.tapScriptSig && t.tapScriptSig.length || t.partialSig && t.partialSig.length ? `signed` : `unsigned`; }
    inputSighash(e) { this.checkInputIdx(e); let t = this.inputs[e].sighashType, n = t === void 0 ? Q.DEFAULT : t, r = n === Q.DEFAULT ? Q.ALL : n & 3; return { sigInputs: n & Q.ANYONECANPAY, sigOutputs: r }; }
    signStatus() { let e = !0, t = !0, n = [], r = []; for (let i = 0; i < this.inputs.length; i++) {
        if (this.inputStatus(i) === `unsigned`)
            continue;
        let { sigInputs: a, sigOutputs: o } = this.inputSighash(i);
        if (a === Q.ANYONECANPAY ? n.push(i) : e = !1, o === Q.ALL)
            t = !1;
        else if (o === Q.SINGLE)
            r.push(i);
        else if (o !== Q.NONE)
            throw Error(`Wrong signature hash output type: ${o}`);
    } return { addInput: e, addOutput: t, inputs: n, outputs: r }; }
    get isFinal() { for (let e = 0; e < this.inputs.length; e++)
        if (this.inputStatus(e) !== `finalized`)
            return !1; return !0; }
    get hasWitnesses() { let e = !1; for (let t of this.inputs)
        t.finalScriptWitness && t.finalScriptWitness.length && (e = !0); return e; }
    get weight() { if (!this.isFinal)
        throw Error(`Transaction is not finalized`); let e = 32, t = this.outputs.map(Jf); e += 4 * Od.encode(this.outputs.length).length; for (let n of t)
        e += 32 + 4 * Ad.encode(n.script).length; this.hasWitnesses && (e += 2), e += 4 * Od.encode(this.inputs.length).length; for (let t of this.inputs)
        e += 160 + 4 * Ad.encode(t.finalScriptSig || Kl).length, this.hasWitnesses && (e += Md.encode(t.finalScriptWitness || []).length); return e; }
    get vsize() { return Bf(this.weight); }
    toBytes(e = !1, t = !1) { return Rd.encode({ version: this.version, lockTime: this.lockTime, inputs: this.inputs.map(Yf).map(t => ({ ...t, finalScriptSig: e && t.finalScriptSig || Kl })), outputs: this.outputs.map(Jf), witnesses: this.inputs.map(e => e.finalScriptWitness || []), segwitFlag: t && this.hasWitnesses }); }
    get unsignedTx() { return this.toBytes(!1, !1); }
    get hex() { return K.encode(this.toBytes(!0, this.hasWitnesses)); }
    get hash() { return K.encode(ad(this.toBytes(!0))); }
    get id() { return K.encode(ad(this.toBytes(!0)).reverse()); }
    checkInputIdx(e) { if (!Number.isSafeInteger(e) || 0 > e || e >= this.inputs.length)
        throw Error(`Wrong input index=${e}`); }
    getInput(e) { return this.checkInputIdx(e), Wf(this.inputs[e]); }
    get inputsLength() { return this.inputs.length; }
    addInput(e, t = !1) { if (!t && !this.signStatus().addInput)
        throw Error(`Tx has signed inputs, cannot add new one`); return this.inputs.push(Wf(rp(e, void 0, void 0, this.opts.disableScriptCheck))), this.inputs.length - 1; }
    updateInput(e, t, n = !1) { this.checkInputIdx(e); let r; if (!n) {
        let t = this.signStatus();
        (!t.addInput || t.inputs.includes(e)) && (r = af);
    } this.inputs[e] = Wf(rp(t, this.inputs[e], r, this.opts.disableScriptCheck, this.opts.allowUnknown)); }
    checkOutputIdx(e) { if (!Number.isSafeInteger(e) || 0 > e || e >= this.outputs.length)
        throw Error(`Wrong output index=${e}`); }
    getOutput(e) { return this.checkOutputIdx(e), Wf(this.outputs[e]); }
    getOutputAddress(e, t = _d) { let n = this.getOutput(e); if (n.script)
        return Lf(t).encode(Df.decode(n.script)); }
    get outputsLength() { return this.outputs.length; }
    normalizeOutput(e, t, n) { let { amount: r, script: i } = e; if (r === void 0 && (r = t?.amount), typeof r != `bigint`)
        throw Error(`Wrong amount type, should be of type bigint in sats, but got ${r} of type ${typeof r}`); typeof i == `string` && (i = K.decode(i)), i === void 0 && (i = t?.script); let a = { ...t, ...e, amount: r, script: i }; if (a.amount === void 0 && delete a.amount, a = bf(of, a, t, n, this.opts.allowUnknown), pf.encode(a), a.script && !this.opts.allowUnknownOutputs && Df.decode(a.script).type === `unknown`)
        throw Error(`Transaction/output: unknown output script type, there is a chance that input is unspendable. Pass allowUnknownOutputs=true, if you sure`); return this.opts.disableScriptCheck || kf(a.script, a.redeemScript, a.witnessScript), a; }
    addOutput(e, t = !1) { if (!t && !this.signStatus().addOutput)
        throw Error(`Tx has signed outputs, cannot add new one`); return this.outputs.push(Wf(this.normalizeOutput(e))), this.outputs.length - 1; }
    updateOutput(e, t, n = !1) { this.checkOutputIdx(e); let r; if (!n) {
        let t = this.signStatus();
        (!t.addOutput || t.outputs.includes(e)) && (r = sf);
    } this.outputs[e] = Wf(this.normalizeOutput(t, this.outputs[e], r)); }
    addOutputAddress(e, t, n = _d) { return this.addOutput({ script: Df.encode(Lf(n).decode(e)), amount: t }); }
    get fee() { let e = 0n; for (let t of this.inputs) {
        let n = np(t);
        if (!n)
            throw Error(`Empty input amount`);
        e += n.amount;
    } let t = this.outputs.map(Jf); for (let n of t)
        e -= n.amount; return e; }
    preimageLegacy(e, t, n) { let { isAny: r, isNone: i, isSingle: a } = $f(n); if (e < 0 || !Number.isSafeInteger(e))
        throw Error(`Invalid input idx=${e}`); if (a && e >= this.outputs.length || e >= this.inputs.length)
        return Mu.encode(1n); t = Vf(t); let o = this.inputs.map(Yf).map((n, r) => ({ ...n, finalScriptSig: r === e ? t : Kl })); r ? o = [o[e]] : (i || a) && (o = o.map((t, n) => ({ ...t, sequence: n === e ? t.sequence : 0 }))); let s = this.outputs.map(Jf); return i ? s = [] : a && (s = s.slice(0, e).fill(zf).concat([s[e]])), ad(Rd.encode({ lockTime: this.lockTime, version: this.version, segwitFlag: !1, inputs: o, outputs: s }), Ru.encode(n)); }
    preimageWitnessV0(e, t, n, r) { if (e < 0 || !Number.isSafeInteger(e) || e >= this.inputs.length)
        throw Error(`Invalid input idx=${e}`); let { isAny: i, isNone: a, isSingle: o } = $f(n), s = Rf, c = Rf, l = Rf, u = this.inputs.map(Yf), d = this.outputs.map(Jf); i || (s = ad(...u.map(Zf.encode))), !i && !o && !a && (c = ad(...u.map(e => Y.encode(e.sequence)))), !o && !a ? l = ad(...d.map(Fd.encode)) : o && e < d.length && (l = ad(Fd.encode(d[e]))); let f = u[e]; return ad(Ru.encode(this.version), s, c, Vu(32, !0).encode(f.txid), Y.encode(f.index), Ad.encode(t), Nu.encode(r), Y.encode(f.sequence), l, Y.encode(this.lockTime), Y.encode(n)); }
    preimageWitnessV1(e, t, n, r, i = -1, a, o = 192, s) { if (!Array.isArray(r) || this.inputs.length !== r.length)
        throw Error(`Invalid amounts array=${r}`); if (!Array.isArray(t) || this.inputs.length !== t.length)
        throw Error(`Invalid prevOutScript array=${t}`); if (e < 0 || !Number.isSafeInteger(e) || e >= this.inputs.length)
        throw Error(`Invalid input idx=${e}`); let c = [Bu.encode(0), Bu.encode(n), Ru.encode(this.version), Y.encode(this.lockTime)], l = n === Q.DEFAULT ? Q.ALL : n & 3, u = n & Q.ANYONECANPAY, d = this.inputs.map(Yf), f = this.outputs.map(Jf); u !== Q.ANYONECANPAY && c.push(...[d.map(Zf.encode), r.map(Nu.encode), t.map(Ad.encode), d.map(e => Y.encode(e.sequence))].map(e => rd(td(...e)))), l === Q.ALL && c.push(rd(td(...f.map(Fd.encode)))); let p = !!s | (a ? 2 : 0); if (c.push(new Uint8Array([p])), u === Q.ANYONECANPAY) {
        let n = d[e];
        c.push(Zf.encode(n), Nu.encode(r[e]), Ad.encode(t[e]), Y.encode(n.sequence));
    }
    else
        c.push(Y.encode(e)); return p & 1 && c.push(rd(Ad.encode(s || Kl))), l === Q.SINGLE && c.push(e < f.length ? rd(Fd.encode(f[e])) : Rf), a && c.push(Mf(a, o), Bu.encode(0), Ru.encode(i)), dd(`TapSighash`, ...c); }
    signIdx(e, t, n, r) { this.checkInputIdx(t); let i = this.inputs[t], a = ip(i, this.opts.allowLegacyWitnessUtxo), o = e => { if (a.txType === `taproot`) {
        let t = od(e);
        if (i.tapInternalKey && nd(t, i.tapInternalKey))
            return !0;
        if (!i.tapLeafScript)
            return !1;
        for (let [e, n] of i.tapLeafScript)
            for (let e of Td.decode(n.subarray(0, -1)))
                if (X(e) && nd(e, t))
                    return !0;
        return !1;
    } let t = sd(e), n = id(t); for (let e of Td.decode(a.lastScript))
        if (X(e) && (nd(e, t) || nd(e, n)))
            return !0; return !1; }; if (!X(e)) {
        let s = e, c = (e, t, n) => { if (!t || !t.length)
            throw Error(`${e}: empty`); let r = t.filter(e => e.fingerprint == s.fingerprint).map(t => { let r = s; for (let e of t.path)
            r = r.deriveChild(e); if (!nd(n(r), t.pubKey))
            throw Error(`${e}: wrong pubKey`); if (!r.privateKey)
            throw Error(`${e}: no privateKey`); return r; }); if (!r.length)
            throw Error(`${e}: no items with fingerprint=${s.fingerprint}`); return r; }, l = a.txType === `taproot` ? c(`tapBip32Derivation`, i.tapBip32Derivation?.map(([e, { der: t }]) => ({ pubKey: e, fingerprint: t.fingerprint, path: t.path })), e => e.publicKey.slice(1)) : c(`bip32Derivation`, i.bip32Derivation?.map(([e, t]) => ({ pubKey: e, fingerprint: t.fingerprint, path: t.path })), e => e.publicKey), u = !1;
        for (let e of l)
            o(e.privateKey) && this.signIdx(e.privateKey, t, n, r) && (u = !0);
        if (u)
            return !0;
        throw a.txType === `taproot` ? Error(`No taproot scripts signed`) : Error(`Input script doesn't have pubKey: ${a.lastScript}`);
    } n ? n.forEach(Qf) : n = [a.defaultSighash]; let s = a.sighash; if (!n.includes(s))
        throw Error(`Input with not allowed sigHash=${s}. Allowed: ${n.join(`, `)}`); let { sigOutputs: c } = this.inputSighash(t); if (c === Q.SINGLE && t >= this.outputs.length)
        throw Error(`Input with sighash SINGLE, but there is no output with corresponding index=${t}`); let l = np(i); if (a.txType === `taproot`) {
        let n = this.inputs.map(np), a = n.map(e => e.script), o = n.map(e => e.amount), c = !1, l = od(e), u = i.tapMerkleRoot || Kl;
        if (i.tapInternalKey) {
            let { pubKey: n, privKey: d } = qf(e, l, i.tapInternalKey, u), [f, p] = gd(i.tapInternalKey, u);
            if (nd(f, n)) {
                let e = td(ud(this.preimageWitnessV1(t, a, s, o), d, r), s === Q.DEFAULT ? Kl : new Uint8Array([s]));
                this.updateInput(t, { tapKeySig: e }, !0), c = !0;
            }
        }
        if (i.tapLeafScript) {
            i.tapScriptSig = i.tapScriptSig || [];
            for (let [n, u] of i.tapLeafScript) {
                let n = u.subarray(0, -1), i = Td.decode(n), d = u[u.length - 1], f = Mf(n, d);
                if (i.findIndex(e => X(e) && nd(e, l)) === -1)
                    continue;
                let p = td(ud(this.preimageWitnessV1(t, a, s, o, void 0, n, d), e, r), s === Q.DEFAULT ? Kl : new Uint8Array([s]));
                this.updateInput(t, { tapScriptSig: [[{ pubKey: l, leafHash: f }, p]] }, !0), c = !0;
            }
        }
        if (!c)
            throw Error(`No taproot scripts signed`);
        return !0;
    } {
        let n = sd(e), r = !1, i = id(n);
        for (let e of Td.decode(a.lastScript))
            X(e) && (nd(e, n) || nd(e, i)) && (r = !0);
        if (!r)
            throw Error(`Input script doesn't have pubKey: ${a.lastScript}`);
        let o;
        if (a.txType === `legacy`)
            o = this.preimageLegacy(t, a.lastScript, s);
        else if (a.txType === `segwit`) {
            let e = a.lastScript;
            a.last.type === `wpkh` && (e = Df.encode({ type: `pkh`, hash: a.last.hash })), o = this.preimageWitnessV0(t, e, s, l.amount);
        }
        else
            throw Error(`Transaction/sign: unknown tx type: ${a.txType}`);
        let c = ld(o, e, this.opts.lowR);
        this.updateInput(t, { partialSig: [[n, td(c, new Uint8Array([s]))]] }, !0);
    } return !0; }
    sign(e, t, n) { let r = 0; for (let i = 0; i < this.inputs.length; i++)
        try {
            this.signIdx(e, i, t, n) && r++;
        }
        catch { } if (!r)
        throw Error(`No inputs signed`); return r; }
    finalizeIdx(e) { if (this.checkInputIdx(e), this.fee < 0n)
        throw Error(`Outputs spends more than inputs amount`); let t = this.inputs[e], n = ip(t, this.opts.allowLegacyWitnessUtxo); if (n.txType === `taproot`) {
        if (t.tapKeySig)
            t.finalScriptWitness = [t.tapKeySig];
        else if (t.tapLeafScript && t.tapScriptSig) {
            let e = t.tapLeafScript.sort((e, t) => Xd.encode(e[0]).length - Xd.encode(t[0]).length);
            for (let [n, r] of e) {
                let e = r.slice(0, -1), i = r[r.length - 1], a = Df.decode(e), o = Mf(e, i), s = t.tapScriptSig.filter(e => nd(e[0].leafHash, o)), c = [];
                if (a.type === `tr_ms`) {
                    let e = a.m, t = a.pubkeys, n = 0;
                    for (let r of t) {
                        let t = s.findIndex(e => nd(e[0].pubKey, r));
                        if (n === e || t === -1) {
                            c.push(Kl);
                            continue;
                        }
                        c.push(s[t][1]), n++;
                    }
                    if (n !== e)
                        continue;
                }
                else if (a.type === `tr_ns`) {
                    for (let e of a.pubkeys) {
                        let t = s.findIndex(t => nd(t[0].pubKey, e));
                        t !== -1 && c.push(s[t][1]);
                    }
                    if (c.length !== a.pubkeys.length)
                        continue;
                }
                else if (a.type === `unknown` && this.opts.allowUnknownInputs) {
                    let t = Td.decode(e);
                    if (c = s.map(([{ pubKey: e }, n]) => { let r = t.findIndex(t => X(t) && nd(t, e)); if (r === -1)
                        throw Error(`finalize/taproot: cannot find position of pubkey in script`); return { signature: n, pos: r }; }).sort((e, t) => e.pos - t.pos).map(e => e.signature), !c.length)
                        continue;
                }
                else {
                    let r = this.opts.customScripts;
                    if (r)
                        for (let i of r) {
                            if (!i.finalizeTaproot)
                                continue;
                            let r = Td.decode(e), a = i.encode(r);
                            if (a === void 0)
                                continue;
                            let o = i.finalizeTaproot(e, a, s);
                            if (o) {
                                t.finalScriptWitness = o.concat(Xd.encode(n)), delete t.finalScriptSig, Xf(t);
                                return;
                            }
                        }
                    throw Error(`Finalize: Unknown tapLeafScript`);
                }
                t.finalScriptWitness = c.reverse().concat([e, Xd.encode(n)]);
                break;
            }
            if (!t.finalScriptWitness)
                throw Error(`finalize/taproot: empty witness`);
        }
        else
            throw Error(`finalize/taproot: unknown input`);
        delete t.finalScriptSig, Xf(t);
        return;
    } if (!t.partialSig || !t.partialSig.length)
        throw Error(`Not enough partial sign`); let r = Kl, i = []; if (n.last.type === `ms`) {
        let e = n.last.m, i = n.last.pubkeys, a = [];
        for (let e of i) {
            let n = t.partialSig.find(t => nd(e, t[0]));
            n && a.push(n[1]);
        }
        if (a = a.slice(0, e), a.length !== e)
            throw Error(`Multisig: wrong signatures count, m=${e} n=${i.length} signatures=${a.length}`);
        r = Td.encode([0, ...a]);
    }
    else if (n.last.type === `pk`)
        r = Td.encode([t.partialSig[0][1]]);
    else if (n.last.type === `pkh`)
        r = Td.encode([t.partialSig[0][1], t.partialSig[0][0]]);
    else if (n.last.type === `wpkh`)
        r = Kl, i = [t.partialSig[0][1], t.partialSig[0][0]];
    else if (n.last.type === `unknown` && !this.opts.allowUnknownInputs)
        throw Error(`Unknown inputs not allowed`); let a, o; if (n.type.includes(`wsh-`) && (r.length && n.lastScript.length && (i = Td.decode(r).map(e => { if (e === 0)
        return Kl; if (X(e))
        return e; throw Error(`Wrong witness op=${e}`); })), i = i.concat(n.lastScript)), n.txType === `segwit` && (o = i), n.type.startsWith(`sh-wsh-`) ? a = Td.encode([Td.encode([0, rd(n.lastScript)])]) : n.type.startsWith(`sh-`) ? a = Td.encode([...Td.decode(r), n.lastScript]) : n.type.startsWith(`wsh-`) || n.txType !== `segwit` && (a = r), !a && !o)
        throw Error(`Unknown error finalizing input`); a && (t.finalScriptSig = a), o && (t.finalScriptWitness = o), Xf(t); }
    finalize() { for (let e = 0; e < this.inputs.length; e++)
        this.finalizeIdx(e); }
    extract() { if (!this.isFinal)
        throw Error(`Transaction has unfinalized inputs`); if (!this.outputs.length)
        throw Error(`Transaction has no outputs`); if (this.fee < 0n)
        throw Error(`Outputs spends more than inputs amount`); return this.toBytes(!0, !0); }
    combine(e) { let t = Math.max(this.opts.PSBTVersion || 0, e.opts.PSBTVersion || 0); for (let t of [`version`, `lockTime`])
        if (this.opts[t] !== e.opts[t])
            throw Error(`Transaction/combine: different ${t} this=${this.opts[t]} other=${e.opts[t]}`); for (let t of [`inputs`, `outputs`])
        if (this[t].length !== e[t].length)
            throw Error(`Transaction/combine: different ${t} length this=${this[t].length} other=${e[t].length}`); if (!nd(this.unsignedTx, e.unsignedTx))
        throw Error(`Transaction/combine: different unsigned tx`); this.global = bf(tf, this.global, e.global, void 0, this.opts.allowUnknown), t && (this.global.version = t); for (let t = 0; t < this.inputs.length; t++)
        this.updateInput(t, e.inputs[t], !0); for (let t = 0; t < this.outputs.length; t++)
        this.updateOutput(t, e.outputs[t], !0); return this; }
    clone() { return e.fromPSBT(this.toPSBT(), this.opts); }
};
