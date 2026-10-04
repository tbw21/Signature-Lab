/* src/06-session-download.js: reconstructed from the reviewed v0.14.0-dev distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
var Zp = TBW_BUILD.version;
function Qp(e, t, n) { let r = typeof e == `string` ? e : new Uint8Array(e).buffer, i = URL.createObjectURL(new Blob([r], { type: n })), a = document.createElement(`a`); a.href = i, a.download = t, document.body.appendChild(a); try {
    a.click();
}
finally {
    a.remove(), setTimeout(() => URL.revokeObjectURL(i), 2e3);
} }
// One outcome rule for journal projections, guided status and saved summaries.
// A missing/unknown file assessment is not silently promoted to a clean reference match.
const TBW_SESSION_COUNT_POLICY = 'distinct-transaction-worst-observed-v2';
function tbwCheckOutcome(check) {
    if (check.result === 'mismatch') return 'differed';
    if (check.result === 'match' && ['expected', 'unchanged', 'not-applicable'].includes(check.metadataStatus)) return 'matched';
    return 'review';
}
function $p(checks, next) {
    const previous = checks.find(check => check.transactionId === next.transactionId);
    if (!previous) return [...checks, {...next}];
    const rank = {matched: 0, review: 1, differed: 2};
    return rank[tbwCheckOutcome(next)] > rank[tbwCheckOutcome(previous)]
        ? checks.map(check => check === previous ? {...next} : check) : [...checks];
}
function em(checks) {
    const counts = {checked: checks.length, matched: 0, review: 0, differed: 0, suggested: 20,
        countPolicy: TBW_SESSION_COUNT_POLICY};
    for (const check of checks) counts[tbwCheckOutcome(check)]++;
    return counts;
}

// Short public export names are a convenience, not protection from test recognition.
function tbwSaveJson(value, category) {
    if (!['record','detail','journal','notes'].includes(category)) throw new TypeError('Unknown export category');
    const text = JSON.stringify(value, null, 2);
    if (typeof text !== 'string') throw new TypeError('JSON export requires a value');
    const suffix = K.encode(ns(new TextEncoder().encode(text))).slice(0,12);
    const filename = category + '-' + suffix + '.json';
    Qp(text, filename, 'application/json');
    return filename;
}
