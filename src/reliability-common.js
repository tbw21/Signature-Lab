/* Shared failure and immutable-public-data contracts. No DOM or persistence. */
class TBWFailure extends Error {
    constructor(code, message) { super(message); this.name = 'TBWFailure'; this.code = code; }
}
function tbwFail(code, message) { throw new TBWFailure(code, message); }
function tbwFreeze(value) {
    if (value && typeof value === 'object' && !Object.isFrozen(value)) {
        if (ArrayBuffer.isView(value)) throw new TypeError('Immutable snapshots require strings, not mutable byte arrays');
        for (const item of Object.values(value)) tbwFreeze(item);
        Object.freeze(value);
    }
    return value;
}
const TBW_LIMITS = Object.freeze({ bytes: 524288, text: 1048576, frame: 16384,
    frames: 4096, characters: 4194304, urParts: 1024, work: 33554432,
    psbtFields: 4096, psbtMaps: 41 });

function tbwUUID() {
    if (typeof globalThis.crypto?.getRandomValues !== 'function')
        tbwFail('RANDOM_UNAVAILABLE', 'Secure browser randomness is unavailable. Use a supported browser; no test was created.');
    const bytes = globalThis.crypto.getRandomValues(new Uint8Array(16));
    bytes[6] = (bytes[6] & 15) | 64; bytes[8] = (bytes[8] & 63) | 128;
    const text = Array.from(bytes, byte => byte.toString(16).padStart(2, '0')).join('');
    return [text.slice(0,8), text.slice(8,12), text.slice(12,16), text.slice(16,20), text.slice(20)].join('-');
}
