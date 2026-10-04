/* src/22-bootstrap.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
sa.data(`app`, () => { let e; try {
    e = Fv();
}
catch (e) {
    throw Lv(), e;
} let t = e.init; return e.init = function () { try {
    t.call(this), document.documentElement.dataset.appReady = `true`;
}
catch (e) {
    throw Lv(), e;
} this.$nextTick(() => { try {
    let e = ua(document);
    window.addEventListener(`pagehide`, t => { t.persisted || e(); });
}
catch { } try {
    let e = Iv(document, { onOpen: () => { this.cancelSectionFocus(), this.stopScan(); }, onReturn: () => this.focusCurrentSection() });
    window.addEventListener(`pagehide`, t => { t.persisted || e(); });
}
catch { } }); /* Browser-agent registration retired: no unsolicited status-sharing surface. */ }, e; }), sa.start();
