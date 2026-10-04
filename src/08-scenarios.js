/* src/08-scenarios.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
function nm(e) { let t = new Uint8Array(e); return crypto.getRandomValues(t), t; }
function $(e, t) { if (!Number.isSafeInteger(e) || !Number.isSafeInteger(t) || t < e)
    throw Error(`Invalid randInt range [${e}, ${t}]`); let n = BigInt(t) - BigInt(e) + 1n, r = n.toString(2).length, i = Math.max(1, Math.ceil(r / 8)), a = (1n << BigInt(i * 8)) / n * n, o = new Uint8Array(i), s, c = 0; do {
    if (++c > 128)
        throw Error(`Random sampler did not converge; start a new test explicitly`);
    crypto.getRandomValues(o), s = 0n;
    for (let e of o)
        s = s << 8n | BigInt(e);
} while (s >= a); return Number(BigInt(e) + s % n); }
function rm(e) { return Rl(tm, e === 12 ? 128 : 256); }
function im() { return $(9e5, 2e6); }
function am() { return K.encode(nm(32)); }
function om() { return bp(nm(20)); }
function sm() { return { utxoId: `${am()}:${$(0, 100)}`, amount: String($(2e3, 1e9)), pathSuffix: `0h/${$(0, 1)}/${$(0, 500)}`, sequence: `0xfffffffd` }; }
function cm() { return Array.from({ length: $(2, 10) }, () => sm()); }
function lm(e) { if (e < BigInt(1342))
    throw Error(`Need at least ${um} sats of inputs to generate random outputs`); if (e > BigInt(2 ** 53 - 1))
    throw Error(`Total input amount is too large for the random-output generator`); let t = Number(e), n = $(600, t - 742), r = t - n, i = r - $(141, Math.min(r - 600, 5e3)), a = { amount: String(n), dest: om() }, o = { amount: String(i), dest: mp(0, 1, $(0, 500)) }; return $(0, 1) === 0 ? [a, o] : [o, a]; }
var um = 1342;
var dm = [{ id: `small`, label: `Small payment` }, { id: `medium`, label: `Medium payment` }, { id: `large`, label: `Large payment` }, { id: `consolidation`, label: `Wallet consolidation` }, { id: `batch`, label: `Multiple recipients` }, { id: `boundary`, label: `Boundary case` }];
var fm = { small: [1e3, 1e5], medium: [100001, 1e7], large: [10000001, 1e9] };
var pm = [600, 1e3, 99999, 1e5, 100001, 9999999, 1e7, 10000001, 99999999, 1e8, 100000001, 1e9];
var mm = [0, 499999999, 5e8, 4294967295];
var hm = e => e[$(0, e.length - 1)];
function gm(e) { let t = dm.map(({ id: t }) => e.filter(e => e.scenario === t).length), n = Math.min(...t); return hm(dm.filter((e, r) => t[r] === n)).id; }
function _m(e) { for (let t = e.length - 1; t > 0; t--) {
    let n = $(0, t);
    [e[t], e[n]] = [e[n], e[t]];
} return e; }
function vm(e, t) { let n = $(e, t), r = hm([1, 100, 1e3]); return Math.max(e, Math.floor(n / r) * r); }
function ym(e, t) { if (!Number.isSafeInteger(e) || t < 1 || e < t * 600)
    throw Error(`Invalid scenario budget`); let n = []; for (let r = t; r > 1; r--) {
    let t = $(600, e - (r - 1) * 600);
    n.push(t), e -= t;
} return _m([...n, e]); }
function bm(e) { if (!dm.some(t => t.id === e))
    throw Error(`Unknown transaction scenario`); let t = e === `boundary`, n = e === `consolidation`, r = t ? hm([1, 20]) : 0, i = fm[e], a = n ? 0 : t ? hm([1, 20]) : e === `batch` ? $(2, 8) : 1, o = n ? 0 : t ? Math.max(hm(pm), a * 600, r * 600) : e === `batch` ? vm(1e4, 1e8) : vm(i[0], i[1]), s = n ? $(1e5, 1e8) : t || $(0, 1) === 0 ? 0 : $(600, Math.max(600, o * 2)), c = a + +(s > 0), l = n ? $(8, 20) : t ? r : Math.min($(1, e === `batch` ? 6 : 4), Math.floor((o + s) / 600)), u = t ? hm([1, 50, 100]) : $(1, e === `small` || n ? 5 : e === `medium` ? 15 : 25), d = (11 + 69 * l + 31 * c) * u, f = o + s + d, p = n ? [] : ym(o, a).map(e => ({ amount: String(e), dest: om() })); s > 0 && p.push({ amount: String(s), dest: mp(0, 1, $(0, 500)) }); let m = t ? hm(mm) : 0, h = hm(t ? [`0xfffffffd`, `0xfffffffe`, `0xffffffff`] : [`0xfffffffd`, `0xffffffff`]), g = new Set; return { scenario: e, inputs: _m(ym(f, l).map(e => { let n = `${am()}:${$(0, t ? 100 : 5)}`; if (g.has(n))
        throw Error(`Random generator repeated an input. Generate a fresh transaction explicitly.`); return g.add(n), { utxoId: n, amount: String(e), pathSuffix: `0h/${$(0, 1)}/${$(0, 500)}`, sequence: h }; })), outputs: _m(p), lockTime: m, feeSats: d }; }
var xm = { small: [`coffee`, `groceries`, `dinner`, `gift`, `reimbursement`, `donation`, `subscription`], medium: [`invoice`, `rent`, `freelance`, `reimbursement`, `equipment`, `services`, `payment`], large: [`invoice`, `property-deposit`, `equipment`, `payment`], consolidation: [`wallet-consolidation`, `savings-transfer`, `cold-storage`], batch: [`supplier-payments`, `contractor-payments`, `reimbursements`, `monthly-payments`], boundary: [`payment`, `invoice`, `transfer`], custom: [`payment`, `invoice`, `transfer`] };
function Sm(e, t = new Date) { let n = xm[e] ?? xm.custom, r = n[$(0, n.length - 1)], i = $(1e3, 9999); return `${r}-${$(0, 1) === 1 ? t.toISOString().slice(0, 10) + `-` : ``}${i}.psbt`; }
function Cm(e) { let t = e.inputs.reduce((e, t) => e + t.amountSats, 0n), n = 0n, r = 0n, i = 0, a = 0, o = 0; for (let t of e.outputs)
    t.dest.kind === `address` ? (n += t.amountSats, i++) : (r += t.amountSats, t.dest.change === 0 ? o++ : a++); let s = n + r, c = t - s; if (c < 0n)
    throw Error(`Outputs exceed inputs.`); return { inputSats: t, paymentSats: n, returnSats: r, outputSats: s, feeSats: c, walletDeltaSats: -(n + c), inputCount: e.inputs.length, outputCount: e.outputs.length, recipientOutputs: i, changeOutputs: a, selfTransferOutputs: o, lockTime: e.lockTime, psbtVersion: e.psbtVersion }; }
function wm(e) { return e.trim().toLowerCase().split(/\s+/).map(e => { let t = tm.indexOf(e); if (t < 0)
    throw Error(`Unknown BIP-39 word: ${e}`); return String(t).padStart(4, `0`); }).join(``); }
