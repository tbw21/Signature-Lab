/* Incoming transport boundary. One session and one terminal failure latch for every QR family.
 * UR framing follows BCR-2020-005. The inherited fountain decoder is preceded by bounded
 * structural admission; redundant equations are checked against the reconstructed message.
 */
var T_ = /^p(\d+)of(\d+)\s+([\s\S]+)$/i;
function tbwInspectUr(frame) {
    const match = /^ur:(crypto-psbt|bytes|psbt)\/(?:(\d+)-(\d+)\/)?([a-z]+)$/i.exec(frame);
    if (!match) tbwFail('UR_FORMAT', 'Unsupported or malformed BC-UR frame. Start a new scan.');
    const type = match[1].toLowerCase(), multipart = match[2] !== undefined;
    const bw = __().default;
    let encoded;
    try { encoded = K.decode(bw.decode(match[4].toLowerCase(), bw.STYLES.MINIMAL)); }
    catch { tbwFail('UR_FRAME_CHECKSUM', 'BC-UR frame encoding or checksum failed. Start a new scan.'); }
    if (!multipart) {
        if (encoded.length > TBW_LIMITS.bytes + 5) tbwFail('UR_SIZE', 'BC-UR payload exceeds the size limit.');
        C_(encoded); // Admit only the supported, complete untagged CBOR byte string.
        return { type, multipart, cbor: encoded, identity: type + ':single:' + K.encode(ns(encoded)) };
    }
    const seqNum = Number(match[2]), seqLen = Number(match[3]);
    if (!Number.isSafeInteger(seqNum) || seqNum < 1 || seqNum > 0xffffffff ||
        !Number.isSafeInteger(seqLen) || seqLen < 1 || seqLen > TBW_LIMITS.urParts)
        tbwFail('UR_SEQUENCE', 'Invalid or oversized BC-UR sequence.');
    // Decode only [uint, uint, uint, uint, bstr]. No recursive general-CBOR parser here.
    let offset = 0;
    const number = (major) => {
        if (offset >= encoded.length) tbwFail('UR_CBOR', 'Truncated BC-UR header.');
        const head = encoded[offset++], ai = head & 31;
        if (head >> 5 !== major || ai > 26) tbwFail('UR_CBOR', 'Unsupported BC-UR header type or integer size.');
        if (ai < 24) return ai;
        const length = {24:1,25:2,26:4}[ai];
        if (offset + length > encoded.length) tbwFail('UR_CBOR', 'Truncated BC-UR integer.');
        let value = 0; for (let i = 0; i < length; i++) value = value * 256 + encoded[offset++];
        if (value < ({24:24,25:256,26:65536}[ai])) tbwFail('UR_CBOR', 'Non-canonical BC-UR integer.');
        return value;
    };
    if (number(4) !== 5) tbwFail('UR_CBOR', 'BC-UR fountain header must contain exactly five fields.');
    const innerNum = number(0), innerLen = number(0), messageLength = number(0), checksum = number(0);
    const fragmentLength = number(2);
    if (innerNum !== seqNum || innerLen !== seqLen) tbwFail('UR_SEQUENCE', 'BC-UR path and fragment sequence disagree.');
    if (messageLength < 1 || messageLength > TBW_LIMITS.bytes + 5 || fragmentLength < 1 ||
        offset + fragmentLength !== encoded.length ||
        (seqLen - 1) * fragmentLength >= messageLength || seqLen * fragmentLength < messageLength)
        tbwFail('UR_SIZE', 'Invalid BC-UR declared size, fragment size or padding geometry.');
    return { type, multipart, seqNum, seqLen, messageLength, checksum, fragmentLength,
        fragment: encoded.slice(offset), cbor: encoded,
        identity: `${type}:multipart:${seqLen}:${messageLength}:${checksum}:${fragmentLength}` };
}
var E_ = class {
    frames = 0; receivedCharacters = 0; family = null;
    urDecoder = null; specterParts = null; specterTotal = 0; bbqr = null;
    error = null; errorCode = null; result = null;
    urIdentity = null; urParts = new Map(); urMessage = null; urWork = 0;
    get active() { return this.family !== null; }
    inspect() { return this.status(); }
    status() {
        const progress = this.error ? 0 : this.result ? 1 : this.family === 'ur'
            ? Math.min(.99, this.urDecoder?.estimatedPercentComplete() ?? 0)
            : this.family === 'specter' ? this.specterParts.filter(p => p !== undefined).length / this.specterTotal
            : this.bbqr ? tbwBBQrCodec().status(this.bbqr).progress : 0;
        return Object.freeze({ done: !!this.result, failed: !!this.error, error: this.error,
            code: this.errorCode, progress, frames: this.frames, family: this.family,
            format: this.family === 'ur' ? 'BC-UR animated QR' : this.family === 'specter'
                ? 'Specter animated QR (pMofN)' : this.family === 'bbqr' ? 'BBQr' : 'static QR' });
    }
    plan(frame) {
        if (typeof frame !== 'string' || frame.length > TBW_LIMITS.frame)
            tbwFail('QR_FRAME_SIZE', 'QR payload exceeds the size limit.');
        const text = frame.trim();
        if (!text) return { family: null, text };
        if (/^b\$/i.test(text)) return { family: 'bbqr', text };
        if (/^ur:/i.test(text)) return { family: 'ur', text, ur: tbwInspectUr(text) };
        const specter = T_.exec(text);
        return specter ? { family: 'specter', text, specter } : { family: 'static', text };
    }
    feed(frame) { return this.apply(frame); }
    apply(frame) {
        if (this.error) tbwFail('QR_SESSION_FAILED', 'QR session failed. Start a new scan explicitly.');
        try {
            if (typeof frame !== 'string' || ++this.frames > TBW_LIMITS.frames ||
                (this.receivedCharacters += frame.length) > TBW_LIMITS.characters)
                tbwFail('QR_SESSION_LIMIT', 'QR session limit reached. Start scanning again explicitly.');
            const part = this.plan(frame);
            if (!part.family) return this.status();
            if (this.family && this.family !== part.family) tbwFail('QR_MIXED', 'Mixed QR sequence formats. Start a new scan.');
            this.family = part.family;
            if (part.family === 'bbqr') this.feedBBQr(part.text);
            else if (part.family === 'ur') this.feedUr(part.text, part.ur);
            else if (part.family === 'specter') this.feedSpecter(part.specter);
            else {
                if (this.result && this.result.text !== part.text) tbwFail('QR_CONFLICT', 'Conflicting static QR responses.');
                this.result = { kind: 'text', text: part.text };
            }
            return this.status();
        } catch (error) {
            this.error = error instanceof Error ? error.message : String(error);
            this.errorCode = error.code ?? 'QR_DECODE_FAILED'; this.result = null;
            this.urParts.clear(); this.urMessage = null; this.urDecoder = null;
            this.specterParts = null; this.bbqr = null;
            throw error;
        }
    }
    feedBBQr(frame) {
        const codec = tbwBBQrCodec(); this.bbqr ||= codec.createSession();
        const state = codec.apply(this.bbqr, frame);
        if (state.done) {
            const decoded = codec.verify(this.bbqr), artifact = Fp(decoded.bytes);
            if ((decoded.fileType === 'P' ? 'psbt' : 'tx') !== artifact.kind)
                tbwFail('BBQR_TYPE', 'BBQr file type does not match its contents.');
            this.result = { kind: 'bytes', bytes: artifact.bytes };
        }
    }
    checkUrEquation(part, message) {
        if (!part.multipart) return;
        // Bound worst-case selection/XOR work, including legitimate but very large redundancy.
        const charge = part.seqNum <= part.seqLen ? part.fragmentLength
            : part.seqLen * part.seqLen + part.seqLen * part.fragmentLength;
        if ((this.urWork += charge) > TBW_LIMITS.work)
            tbwFail('UR_WORK_LIMIT', 'BC-UR verification work limit reached. Use a file or a new shorter sequence.');
        const expected = new Uint8Array(part.fragmentLength);
        for (const index of h_().chooseFragments(part.seqNum, part.seqLen, part.checksum)) {
            const start = index * part.fragmentLength;
            for (let i = 0; i < expected.length; i++) expected[i] ^= message[start + i] ?? 0;
        }
        if (K.encode(expected) !== K.encode(part.fragment))
            tbwFail('UR_EQUATION', 'Conflicting BC-UR fragment data. Start a new scan.');
    }
    feedUr(frame, part) {
        if (this.urIdentity && this.urIdentity !== part.identity)
            tbwFail('UR_IDENTITY', 'Conflicting BC-UR transfer identity. Scan one response at a time.');
        this.urIdentity = part.identity;
        if (!part.multipart) {
            this.urMessage = part.cbor;
            this.result = { kind: 'bytes', bytes: C_(part.cbor) };
            return;
        }
        const old = this.urParts.get(part.seqNum);
        if (old) {
            if (K.encode(old.cbor) !== K.encode(part.cbor))
                tbwFail('UR_DUPLICATE', 'Conflicting BC-UR duplicate fragment. Start a new scan.');
            return;
        }
        if (this.urMessage) {
            this.checkUrEquation(part, this.urMessage);
            this.urParts.set(part.seqNum, part); return;
        }
        // Charge decoder work before its allocations/mixing. Equation validation is charged separately.
        const admission = part.seqNum <= part.seqLen ? part.fragmentLength
            : part.seqLen * part.seqLen + part.seqLen * part.fragmentLength;
        if ((this.urWork += admission) > TBW_LIMITS.work)
            tbwFail('UR_WORK_LIMIT', 'BC-UR decoding work limit reached. Use a file or a new shorter sequence.');
        this.urParts.set(part.seqNum, part);
        this.urDecoder ||= new x_.URDecoder();
        this.urDecoder.receivePart(frame.toLowerCase());
        if (this.urDecoder.isError() || this.urDecoder.fountainDecoder.isFailure())
            tbwFail('UR_MESSAGE_CHECKSUM', 'BC-UR response checksum failed. Start a new scan explicitly.');
        if (this.urDecoder.isComplete()) {
            if (!this.urDecoder.isSuccess()) tbwFail('UR_DECODE', 'Failed to reconstruct the BC-UR response.');
            const result = this.urDecoder.resultUR(), message = new Uint8Array(result.cbor);
            if (result.type !== part.type || message.length !== part.messageLength)
                tbwFail('UR_LENGTH', 'BC-UR reconstructed size or type differs from its header.');
            const bytes = C_(message);
            for (const value of this.urParts.values()) this.checkUrEquation(value, message);
            this.urMessage = message;
            this.result = { kind: 'bytes', bytes };
        }
    }
    feedSpecter(match) {
        const index = Number(match[1]), total = Number(match[2]), payload = match[3].trim();
        if (!Number.isSafeInteger(index) || !Number.isSafeInteger(total) || total < 1 || total > 1024 || index < 1 || index > total)
            tbwFail('SPECTER_SEQUENCE', 'Invalid or oversized pMofN sequence.');
        if (!/^[A-Za-z0-9+/=]+$/.test(payload)) tbwFail('SPECTER_PAYLOAD', 'Malformed Specter fragment.');
        if (this.specterParts && this.specterTotal !== total) tbwFail('SPECTER_TOTAL', 'Conflicting pMofN sequence length.');
        if (!this.specterParts) { this.specterParts = Array(total); this.specterTotal = total; }
        if (this.specterParts[index - 1] !== undefined && this.specterParts[index - 1] !== payload)
            tbwFail('SPECTER_DUPLICATE', 'Conflicting QR fragment.');
        this.specterParts[index - 1] = payload;
        if (this.specterParts.filter(x => x !== undefined).length === total)
            this.result = { kind: 'text', text: this.specterParts.join('') };
    }
    verify() {
        if (this.error) tbwFail('QR_SESSION_FAILED', this.error);
        if (!this.result) tbwFail('QR_INCOMPLETE', 'Incomplete QR sequence. Supply every part.');
        return this.result.kind === 'bytes' ? { kind: 'bytes', bytes: this.result.bytes.slice() }
            : { kind: 'text', text: this.result.text };
    }
    rollback() {
        this.frames = this.receivedCharacters = this.urWork = 0;
        this.family = this.urDecoder = this.specterParts = this.bbqr = this.result = null;
        this.error = this.errorCode = this.urIdentity = this.urMessage = null;
        this.specterTotal = 0; this.urParts.clear(); return this.status();
    }
};
