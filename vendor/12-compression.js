/* Lazy compression boundary. Vendor bytes are inserted verbatim by build.py. */
let tbwBBQrCompressionInstance = null;
function tbwBBQrCompression() {
    if (tbwBBQrCompressionInstance) return tbwBBQrCompressionInstance;
    const module = { exports: {} }, exports = module.exports;
    /*@@PAKO_NOTICES@@*/
    /*@@PAKO_BYTES@@*/
    const library = module.exports;
    if (typeof library.deflateRaw !== 'function' || typeof library.Inflate !== 'function')
        throw new Error('BBQr compression dependency unavailable. Use BC-UR or a signed file.');
    tbwBBQrCompressionInstance = library;
    return library;
}
