/* src/04-bitcoin.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
var op = 2147483648;
var sp = Uint8Array.of(112, 115, 98, 116, 255);
var cp = Uint8Array.of(4, 178, 71, 70);
var lp = Va(ns);
function up(e) { return Al.fromMasterSeed(Gl(dp(e))); }
function dp(e) { return e.trim().toLowerCase().split(/\s+/).join(` `); }
function fp(e, t, n, r) { return e.deriveChild(2147483732).deriveChild(2147483648).deriveChild(t + op).deriveChild(n).deriveChild(r); }
function pp(e, t, n) { return [2147483732, 2147483648, e + op, t, n]; }
function mp(e, t, n) { return `m/84h/0h/${e}h/${t}/${n}`; }
function hp(e, t = 0) { return e.deriveChild(2147483732).deriveChild(2147483648).deriveChild(t + op); }
function gp(e, t = 0) { let n = lp.decode(hp(e, t).publicExtendedKey), r = new Uint8Array(n); return r.set(cp, 0), lp.encode(r); }
function _p(e, t = 0, n = 5) { let r = []; for (let i = 0; i < n; i++)
    r.push(vp(fp(e, t, 0, i).publicKey)); return r; }
function vp(e) { return Af(e, _d).address; }
function yp(e) { let t = Lf(_d).decode(e); if (!t)
    throw Error(`Invalid address`); return Df.encode(t); }
function bp(e) { return Lf(_d).encode({ type: `wpkh`, hash: new Uint8Array(e) }); }
function xp(e) { return e.reduce((e, t) => e + t.amountSats, 0n); }
function Sp(e) { let t = ap.fromRaw(K.decode(e), { allowUnknownOutputs: !0, allowUnknownInputs: !0, disableScriptCheck: !0 }); return Math.ceil(t.weight / 4); }
function Cp(e) { return ap.fromRaw(K.decode(e), { allowUnknownOutputs: !0, allowUnknownInputs: !0, disableScriptCheck: !0 }).id; }
function wp(e, t) { let n = t ?? up(e.mnemonic), r = n.fingerprint, i = new ap({ version: 2, lockTime: e.lockTime, PSBTVersion: e.psbtVersion }); for (let t of e.inputs) {
    let e = fp(n, t.account, t.change, t.addressIndex).publicKey, a = Af(e, _d);
    i.addInput({ txid: K.decode(t.txid.toLowerCase()), index: t.vout, sequence: t.sequence, witnessUtxo: { script: a.script, amount: t.amountSats }, bip32Derivation: [[e, { fingerprint: r, path: pp(t.account, t.change, t.addressIndex) }]] });
} for (let t of e.outputs)
    if (t.dest.kind === `address`)
        i.addOutput({ script: yp(t.dest.address), amount: t.amountSats });
    else {
        let e = fp(n, t.dest.account, t.dest.change, t.dest.addressIndex).publicKey, a = Af(e, _d);
        i.addOutput({ script: a.script, amount: t.amountSats, bip32Derivation: [[e, { fingerprint: r, path: pp(t.dest.account, t.dest.change, t.dest.addressIndex) }]] });
    } return i; }
function Tp(e, t) { return wp(e, t).toPSBT(e.psbtVersion); }
var Ep = 1n << 255n;
function Dp(e) { return e.toBytes(`der`).length; }
function Op(e, t, n) { let r = n => qc.Signature.fromBytes(qc.sign(e, t, { prehash: !1, lowS: !0, ...n ? { extraEntropy: n } : {} })), i = r(); if (n !== `plain`) {
    let e = e => n === `grind-embit` ? Dp(e) <= 70 : e.r < Ep, t = new Uint8Array(32), a = 1;
    for (; !e(i);)
        if (t[0] = a & 255, t[1] = a >>> 8 & 255, t[2] = a >>> 16 & 255, t[3] = a >>> 24 & 255, i = r(t), a++, a > 1e5)
            throw Error(`low-R grinding did not converge`);
} return i.toBytes(`der`); }
function kp(e, t, n, r) { let i = n.inputs[t], a = fp(r, i.account, i.change, i.addressIndex), o = Df.encode({ type: `pkh`, hash: id(a.publicKey) }); return e.preimageWitnessV0(t, o, Gf.ALL, i.amountSats); }
var Ap = { "grind-embit": { label: `RFC 6979 + low-R grinding: embit`, wallets: `SeedSigner, Specter DIY, Krux` }, "grind-core": { label: `RFC 6979 + low-R grinding: Bitcoin Core / bitcoinjs lowR`, wallets: `Bitcoin Core, bitcoinjs-lib with lowR` }, plain: { label: `RFC 6979 plain`, wallets: `trezor-crypto family and others` } };
function jp(e, t) { e.ids.push(t); let n = new Set(e.ids), r = [], i = []; n.has(`grind-embit`) && n.has(`grind-core`) ? (r.push(`RFC 6979 + low-R grinding: Bitcoin Core, embit (SeedSigner, Specter DIY, Krux), bitcoinjs lowR`), i.push(`Bitcoin Core, embit (SeedSigner, Specter DIY, Krux), bitcoinjs-lib with lowR`)) : n.has(`grind-embit`) ? (r.push(Ap[`grind-embit`].label), i.push(Ap[`grind-embit`].wallets)) : n.has(`grind-core`) && (r.push(Ap[`grind-core`].label), i.push(Ap[`grind-core`].wallets)), n.has(`plain`) && (r.push(Ap.plain.label), i.push(Ap.plain.wallets)), e.label = r.join(` / `), e.wallets = i.join(`; `); }
function Mp(e, t, n) { let r = wp(e, t); for (let i = 0; i < e.inputs.length; i++) {
    let a = e.inputs[i], o = fp(t, a.account, a.change, a.addressIndex), s = Op(kp(r, i, e, t), o.privateKey, n);
    r.updateInput(i, { partialSig: [[o.publicKey, td(s, Uint8Array.of(Gf.ALL))]] }, !0);
} return r.finalize(), K.encode(r.extract()); }
function Np(e, t) { let n = t ?? up(e.mnemonic), r = [`grind-embit`, `grind-core`, `plain`], i = []; for (let t of r) {
    let r = Mp(e, n, t), a = i.find(e => e.txHex === r);
    a ? jp(a, t) : i.push({ ids: [t], label: Ap[t].label, wallets: Ap[t].wallets, txHex: r });
} return i; }
function Pp(e, t) { if (e.length < t.length)
    return !1; for (let n = 0; n < t.length; n++)
    if (e[n] !== t[n])
        return !1; return !0; }
function Fp(e) { if (e.length > 524288)
    throw Error(`Artifact exceeds the 512 KiB limit`); if (Pp(e, sp))
    return { kind: `psbt`, bytes: e }; try {
    return ap.fromRaw(e, { allowUnknownOutputs: !0, allowUnknownInputs: !0, disableScriptCheck: !0 }), { kind: `tx`, bytes: e };
}
catch {
    throw Error(`Data is neither a PSBT (missing psbt magic bytes) nor a valid raw transaction`);
} }
function Ip(e) { if (e.length > 1048576)
    throw Error(`Artifact text exceeds the 1 MiB limit`); let t = e.replace(/\s+/g, ``); if (!t)
    throw Error(`No data`); if (/^[0-9a-fA-F]+$/.test(t) && t.length % 2 == 0)
    return Fp(K.decode(t.toLowerCase())); let n; try {
    n = Ra.decode(t);
}
catch {
    throw Error(`Data is neither hex nor base64`);
} return Fp(n); }
function Lp(e) { if (Pp(e, sp))
    return K.encode(e); try {
    let t = new TextDecoder(`utf-8`, { fatal: !0 }).decode(e);
    if (/^[\t\n\r\x20-\x7e]*$/.test(t))
        return t.trim();
}
catch { } return K.encode(e); }
function Rp(e, t, n) { let r = ap.fromRaw(K.decode(t), { allowUnknownOutputs: !0, allowUnknownInputs: !0, disableScriptCheck: !0 }), i = wp(e, n); if (K.encode(r.unsignedTx) !== K.encode(i.unsignedTx))
    throw Error(`This signed transaction belongs to a different test. Import the transaction currently shown on this page.`); for (let t = 0; t < e.inputs.length; t++) {
    let a = r.getInput(t), o = `Input ${t + 1}`;
    if (a.finalScriptSig?.length)
        throw Error(`${o}: native SegWit requires an empty scriptSig.`);
    let s = a.finalScriptWitness;
    if (!s || s.length !== 2)
        throw Error(`${o}: expected exactly one signature and one public key. The signed data is missing or unsupported.`);
    let c = e.inputs[t], l = fp(n, c.account, c.change, c.addressIndex);
    if (K.encode(s[1]) !== K.encode(l.publicKey))
        throw Error(`${o}: the signing key does not match this test wallet.`);
    let u = s[0];
    if (u.length < 9 || u[u.length - 1] !== Gf.ALL)
        throw Error(`${o}: a complete SIGHASH_ALL ECDSA signature is required.`);
    let d = u.slice(0, -1), f = !1;
    try {
        f = qc.verify(d, kp(i, t, e, n), l.publicKey, { prehash: !1, lowS: !0, format: `der` });
    }
    catch { }
    if (!f)
        throw Error(`${o}: signature verification failed. The signature may be corrupt, use an unsupported form, or have been made for different test data.`);
} return r; }
function zp(spec, artifact, references, root, preparedPsbtHex) {
    try {
        if (artifact.bytes.length > TBW_LIMITS.bytes) throw new Error('Artifact exceeds the 512 KiB limit');
        if (!references.length) throw new Error('No reference signatures are available. The comparison could not run.');
        const master = root ?? up(spec.mnemonic);
        // Account for the complete PSBT framing before the semantic decoder can discard anything.
        const metadata = tbwAssessMetadata(spec, artifact, master, preparedPsbtHex);
        const txHex = artifact.kind === 'tx' ? K.encode(artifact.bytes) : Bp(spec, artifact.bytes, master);
        const transaction = Rp(spec, txHex, master);
        const matched = references.find(reference => reference.txHex === txHex);
        return {ok:true, txHex, matched, metadata, evidence:{transactionId:transaction.id,
            signaturesVerified:spec.inputs.length, artifactSha256:K.encode(ns(artifact.bytes)),
            artifactKind:artifact.kind, comparison:'exact-signed-transaction'}};
    } catch (error) { return {ok:false, error:error instanceof Error ? error.message : String(error), code:error.code ?? 'VERIFICATION_FAILED'}; }
}
function Bp(e, t, n) { let r; try {
    r = ap.fromPSBT(t, { allowUnknownOutputs: !0, allowUnknownInputs: !0, allowLegacyWitnessUtxo: !0, disableScriptCheck: !0, allowUnknown: !0 });
}
catch (e) {
    throw Error(`Cannot parse returned PSBT: ${e instanceof Error ? e.message : e}`);
} if (r.inputsLength !== e.inputs.length)
    throw Error(`Returned PSBT has ${r.inputsLength} inputs but the transaction above has ${e.inputs.length}`); let i = wp(e, n); if (K.encode(r.unsignedTx) !== K.encode(i.unsignedTx))
    throw Error(`Returned PSBT transaction differs from the current test (inputs, outputs, version or locktime)`); for (let t = 0; t < e.inputs.length; t++) {
    let n = r.getInput(t), a = i.getInput(t), o = `Input ${t + 1}`, s = a.bip32Derivation[0][0];
    if (n.finalScriptSig?.length)
        throw Error(`${o}: unexpected scriptSig for native SegWit.`);
    if (n.redeemScript?.length || n.witnessScript?.length || Object.keys(n).some(e => e.startsWith(`tap`)))
        throw Error(`${o}: returned PSBT contains unsupported signing fields.`);
    if (n.partialSig && (n.partialSig.length !== 1 || K.encode(n.partialSig[0][0]) !== K.encode(s)))
        throw Error(`${o}: returned PSBT contains extra signatures or a different signing key.`);
    if (n.partialSig?.length && n.finalScriptWitness?.length && K.encode(n.partialSig[0][1]) !== K.encode(n.finalScriptWitness[0]))
        throw Error(`${o}: partial and finalized signatures disagree.`);
    if (n.bip32Derivation && (n.bip32Derivation.length !== 1 || K.encode(n.bip32Derivation[0][0]) !== K.encode(s) || n.bip32Derivation[0][1].fingerprint !== a.bip32Derivation[0][1].fingerprint || JSON.stringify(n.bip32Derivation[0][1].path) !== JSON.stringify(a.bip32Derivation[0][1].path)))
        throw Error(`${o}: returned key derivation differs from this test wallet.`);
    if (n.nonWitnessUtxo) {
        let r = n.nonWitnessUtxo.outputs[e.inputs[t].vout];
        if (!r || r.amount !== a.witnessUtxo.amount || K.encode(r.script) !== K.encode(a.witnessUtxo.script))
            throw Error(`${o}: previous transaction data changes the input amount or script.`);
    }
    if (n.sighashType !== void 0 && n.sighashType !== Gf.ALL)
        throw Error(`Unsupported sighash for input ${t}`);
    if (n.witnessUtxo && (n.witnessUtxo.amount !== a.witnessUtxo.amount || K.encode(n.witnessUtxo.script) !== K.encode(a.witnessUtxo.script)))
        throw Error(`Returned PSBT input ${t} changes the amount or script`);
    if (n.txid && K.encode(n.txid) !== e.inputs[t].txid.toLowerCase())
        throw Error(`Returned PSBT input ${t} spends a different UTXO than the transaction above`);
    if (n.finalScriptWitness?.length)
        i.updateInput(t, { finalScriptWitness: n.finalScriptWitness }, !0);
    else if (n.partialSig?.length)
        i.updateInput(t, { partialSig: n.partialSig }, !0), i.finalizeIdx(t);
    else
        throw Error(`Returned PSBT has no signature for input ${t}`);
} return K.encode(i.extract()); }
var Vp = `0200000000010285e2b9007ee5a8e2219e6a67473dd60ecb386798c3ed31f25caac7dfa04cf9950000000000fdffffff86afd0dc919bb44676fee9ee90e3b8b1d8f87161260b4bfee4a774fc5dfba54b0100000000fdffffff019fdc00000000000016001463f4022d7c4e81c82a19e5ce3c91e9c30be4a38b02473044022045d33bfd52700d4103136801bfb968556b747def60794340f9787b2203efa76502203bcf20909ca2f75ff5908626c4ede44b14eff6b2c08f557f5be65f7b225b4f2301210366041ee7dd06f5325c78ab2ee2e015bbfabc312a17e28bfa1a9958945e7aa2d3024730440220033aa02ea64257fa0e29857f0e097a3f9ebbc2f2f024e13affe919251c53aa4202205e32165660396f8368e9624980a7efc385cd25bd8feb4371e8643f0fe096d915012103f9b2d924331348de24170061f96a839566e80a58d553a450d96a0f3877f03cf480030d00`;
function Hp() { return { mnemonic: `flag effort pulp expire foster kite scan taste replace note hundred rural`, lockTime: 852864, psbtVersion: 2, inputs: [{ txid: `95f94ca0dfc7aa5cf231edc3986738cb0ed63d47676a9e21e2a8e57e00b9e285`, vout: 0, amountSats: 38151n, account: 0, change: 0, addressIndex: 17, sequence: 4294967293 }, { txid: `4ba5fb5dfc74a7e4fe4b0b266171f8d8b1b8e390eee9fe7646b49b91dcd0af86`, vout: 1, amountSats: 20000n, account: 0, change: 0, addressIndex: 15, sequence: 4294967293 }], outputs: [{ amountSats: 56479n, dest: { kind: `change`, account: 0, change: 0, addressIndex: 18 } }] }; }
function Up() { let e = Hp(), t = up(e.mnemonic); return zp(e, { kind: `tx`, bytes: K.decode(Vp) }, Np(e, t), t); }
