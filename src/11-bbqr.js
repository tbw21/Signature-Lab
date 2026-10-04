/* src/11-bbqr.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
function createTBWBBQrCodec(loadCompression) {
    'use strict';
    const LIMITS = Object.freeze({ bytes: 524288, parts: 1295, frameCharacters: 4296,
        frames: 4096, sessionCharacters: 4194304 });
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ234567';
    const fail = message => { throw new Error(`BBQr: ${message}`); };
    const checkBytes = bytes => {
        if (!(bytes instanceof Uint8Array) || !bytes.length || bytes.length > LIMITS.bytes)
            fail('expected 1 to 512 KiB of binary data');
    };
    function encode32(bytes) {
        let output = '', bits = 0, value = 0;
        for (const byte of bytes) {
            value = (value << 8) | byte;
            bits += 8;
            while (bits >= 5) {
                bits -= 5;
                output += alphabet[(value >>> bits) & 31];
            }
            value &= (1 << bits) - 1;
        }
        if (bits)
            output += alphabet[(value << (5 - bits)) & 31];
        return output;
    }
    function decode32(text) {
        if (!/^[A-Z2-7]+$/.test(text) || ![0, 2, 4, 5, 7].includes(text.length % 8))
            fail('invalid unpadded Base32 payload');
        const output = new Uint8Array(Math.floor(text.length * 5 / 8));
        let bits = 0, value = 0, offset = 0;
        for (const char of text) {
            value = (value << 5) | alphabet.indexOf(char);
            bits += 5;
            if (bits >= 8) {
                bits -= 8;
                output[offset++] = (value >>> bits) & 255;
            }
            value &= (1 << bits) - 1;
        }
        if (value !== 0)
            fail('non-zero Base32 padding bits');
        return output;
    }
    function inspect(frame) {
        if (typeof frame !== 'string')
            fail('frame must be text');
        if (frame.length > LIMITS.frameCharacters)
            fail('frame exceeds 4296 characters');
        const match = /^B\$([H2Z])([PT])([0-9A-Z]{2})([0-9A-Z]{2})(.+)$/.exec(frame);
        if (!match)
            fail('invalid header or payload; only uppercase H/2/Z and PSBT (P)/transaction (T) are accepted');
        const [, encoding, fileType, countText, indexText, payload] = match;
        const total = parseInt(countText, 36), index = parseInt(indexText, 36);
        if (total < 1 || total > LIMITS.parts || index >= total)
            fail('invalid part count or index');
        let bytes;
        if (encoding === 'H') {
            if (!/^(?:[0-9A-F]{2})+$/.test(payload))
                fail('invalid uppercase Hex payload');
            bytes = Uint8Array.from(payload.match(/../g), pair => parseInt(pair, 16));
        }
        else {
            if (index !== total - 1 && payload.length % 8)
                fail('non-final Base32 part is not byte-aligned');
            bytes = decode32(payload);
        }
        return Object.freeze({ encoding, fileType, total, index, payload, bytes });
    }
    function inflateBounded(packed) {
        checkBytes(packed);
        const library = loadCompression();
        if (typeof library?.Inflate !== 'function')
            fail('compression module unavailable; restart explicitly or import the signed file');
        const inflator = new library.Inflate({ raw: true, windowBits: 10, chunkSize: 4096 });
        const chunks = [];
        let length = 0;
        inflator.onData = chunk => {
            length += chunk.length;
            if (length > LIMITS.bytes)
                fail('decompressed payload exceeds the 512 KiB limit');
            chunks.push(new Uint8Array(chunk));
        };
        // Do not force finish: pako 1.x otherwise treats some truncated streams as ended.
        // Only a real Z_STREAM_END sets ended on this non-finishing push.
        inflator.push(packed, false);
        if (inflator.err || !inflator.ended)
            fail('invalid or truncated raw DEFLATE stream');
        if (inflator.strm.avail_in !== 0)
            fail('trailing data after raw DEFLATE stream');
        if (!length)
            fail('empty decompressed payload');
        const output = new Uint8Array(length);
        let offset = 0;
        for (const chunk of chunks) {
            output.set(chunk, offset);
            offset += chunk.length;
        }
        return output;
    }
    function plan(bytes, fileType = 'P', payloadCharacters = 160) {
        checkBytes(bytes);
        if (!['P', 'T'].includes(fileType))
            fail('only PSBT (P) and transaction (T) exports are allowed');
        if (!Number.isInteger(payloadCharacters) || payloadCharacters < 8 || payloadCharacters > 4288)
            fail('invalid frame payload budget');
        const library = loadCompression();
        if (typeof library?.deflateRaw !== 'function')
            fail('compression module unavailable');
        const compressed = library.deflateRaw(bytes, { level: 9, windowBits: 10 });
        const encoding = compressed.length < bytes.length ? 'Z' : '2';
        const packed = encoding === 'Z' ? compressed : bytes;
        const encoded = encode32(packed), budget = Math.floor(payloadCharacters / 8) * 8;
        const count = Math.ceil(encoded.length / budget);
        if (count > LIMITS.parts)
            fail('too many parts; use a larger frame budget or a file');
        // Balance parts on 5-byte boundaries. Last part may be shorter, never longer.
        const partLength = Math.ceil(encoded.length / count / 8) * 8;
        const total = Math.ceil(encoded.length / partLength);
        const base36 = n => n.toString(36).toUpperCase().padStart(2, '0');
        const frames = [];
        for (let index = 0; index < total; index++) {
            frames.push(`B$${encoding}${fileType}${base36(total)}${base36(index)}` +
                encoded.slice(index * partLength, (index + 1) * partLength));
        }
        return Object.freeze({ encoding, fileType, byteLength: bytes.length,
            packedByteLength: packed.length, frames: Object.freeze(frames) });
    }
    class Session {
        #parts = new Map();
        #header = null;
        #normalLength = null;
        #lastLength = null;
        #size = 0;
        #frames = 0;
        #characters = 0;
        #result = null;
        #error = null;
        apply(frame) {
            if (this.#error)
                fail('session failed; start a new scan explicitly');
            try {
                if (typeof frame !== 'string' || ++this.#frames > LIMITS.frames ||
                    (this.#characters += frame.length) > LIMITS.sessionCharacters)
                    fail('session limit reached; start a new scan explicitly');
                const part = inspect(frame);
                const header = frame.slice(0, 6);
                if (this.#header !== null && this.#header !== header)
                    fail('conflicting encoding, file type or part count; scan one response at a time');
                const previous = this.#parts.get(part.index);
                if (previous) {
                    if (previous.payload !== part.payload)
                        fail('conflicting duplicate part');
                    return this.status();
                }
                const size = this.#size + part.bytes.length;
                const normalLength = part.index < part.total - 1 ? part.bytes.length : this.#normalLength;
                const lastLength = part.index === part.total - 1 ? part.bytes.length : this.#lastLength;
                if (this.#normalLength !== null && part.index < part.total - 1 &&
                    part.bytes.length !== this.#normalLength)
                    fail('unequal non-final part lengths');
                if (normalLength !== null && lastLength !== null && lastLength > normalLength)
                    fail('final part is longer than the other parts');
                if (size > LIMITS.bytes || (normalLength !== null &&
                    normalLength * (part.total - 1) + (lastLength ?? 1) > LIMITS.bytes))
                    fail('assembled payload exceeds the 512 KiB limit');
                this.#header = header;
                this.#normalLength = normalLength;
                this.#lastLength = lastLength;
                this.#size = size;
                this.#parts.set(part.index, part);
                if (this.#parts.size === part.total) {
                    const packed = new Uint8Array(size);
                    let offset = 0;
                    for (let index = 0; index < part.total; index++) {
                        const bytes = this.#parts.get(index).bytes;
                        packed.set(bytes, offset);
                        offset += bytes.length;
                    }
                    const bytes = part.encoding === 'Z' ? inflateBounded(packed) : packed;
                    checkBytes(bytes);
                    this.#result = { bytes, fileType: part.fileType };
                }
                return this.status();
            }
            catch (error) {
                this.#error = error instanceof Error ? error.message : String(error);
                this.#result = null;
                this.#parts.clear();
                throw error;
            }
        }
        verify() {
            if (this.#error)
                fail('session failed; start a new scan explicitly');
            if (!this.#result)
                fail('incomplete sequence; supply every part');
            return { fileType: this.#result.fileType, bytes: this.#result.bytes.slice() };
        }
        status() {
            const total = this.#header ? parseInt(this.#header.slice(4, 6), 36) : 0;
            return Object.freeze({ done: !!this.#result, failed: !!this.#error, error: this.#error,
                received: this.#parts.size, total, progress: total ? this.#parts.size / total : 0,
                encoding: this.#header?.[2] ?? null, fileType: this.#header?.[3] ?? null,
                format: 'BBQr' });
        }
        rollback() {
            this.#parts.clear();
            this.#header = this.#normalLength = this.#lastLength = null;
            this.#size = this.#frames = this.#characters = 0;
            this.#result = this.#error = null;
            return this.status();
        }
    }
    return Object.freeze({ limits: LIMITS, inspect, plan, createSession: () => new Session(),
        apply: (session, frame) => session.apply(frame), verify: session => session.verify(),
        status: session => session.status(), rollback: session => session.rollback() });
}
let tbwBBQrInstance = null;
function tbwBBQrCodec() {
    if (!tbwBBQrInstance)
        tbwBBQrInstance = createTBWBBQrCodec(tbwBBQrCompression);
    return tbwBBQrInstance;
}
