/* A finite submission is accepted only after the entire submission has been consumed.
 * Live camera capture uses E_ directly and may stop on its first complete artifact.
 */
function Pv(text) {
    if (typeof text !== 'string' || text.length > TBW_LIMITS.text)
        tbwFail('IMPORT_SIZE', 'Artifact exceeds the 1 MiB text limit.');
    const trimmed = text.trim();
    if (!/^(?:ur:|b\$|p\d+of\d+\s)/i.test(trimmed)) {
        const artifact = Ip(trimmed);
        return { ...artifact, transport: { family: 'text', frames: 1, completeSubmission: true } };
    }
    const session = new E_();
    const parts = /^p\d+of\d+\s/i.test(trimmed) ? trimmed.split(/\r?\n/) : trimmed.split(/\s+/);
    for (const part of parts) if (part.trim()) session.feed(part);
    const decoded = session.verify();
    const artifact = decoded.kind === 'bytes' ? Fp(decoded.bytes) : Ip(decoded.text);
    return { ...artifact, transport: { ...session.status(), completeSubmission: true } };
}
