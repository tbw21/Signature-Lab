/* src/02-layout.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
var ca = new WeakMap;
function la(e) { e && ca.get(e)?.refresh(); }
function ua(e) { ca.get(e)?.stop(); let t = e.getElementById(`test-view`), n = e.querySelector(`.session-tracker`), r = e.defaultView, i = () => { n?.removeAttribute(`data-sticky-ready`), t?.style.removeProperty(`--session-clearance`); }; if (!t || !n || !r)
    return i(), () => { }; let a, o = null, s = !1, c = () => { if (!s) {
    s = !0;
    try {
        a?.disconnect();
    }
    catch { }
    r.removeEventListener(`resize`, l), r.removeEventListener(`pageshow`, l), o?.removeEventListener(`resize`, l), o?.removeEventListener(`scroll`, l), ca.get(e)?.stop === c && ca.delete(e), i();
} }, l = () => { if (!s)
    try {
        let a = n.getBoundingClientRect().height, s = o?.height ?? r.innerHeight;
        if (a === 0 && e.documentElement.dataset.helpView === `true`)
            return;
        if (o && (o.scale !== 1 || o.offsetTop !== 0 || o.offsetLeft !== 0) || !Number.isFinite(a) || !Number.isFinite(s) || a <= 0 || s <= 0 || a > s * .35) {
            i();
            return;
        }
        t.style.setProperty(`--session-clearance`, `${Math.ceil(a) + 24}px`), n.setAttribute(`data-sticky-ready`, `true`);
    }
    catch {
        c();
    } }; try {
    if (typeof r.ResizeObserver != `function`)
        return c(), c;
    o = r.visualViewport, a = new r.ResizeObserver(l), a.observe(n), r.addEventListener(`resize`, l), r.addEventListener(`pageshow`, l), o?.addEventListener(`resize`, l), o?.addEventListener(`scroll`, l), ca.set(e, { refresh: l, stop: c }), l();
}
catch {
    c();
} return c; }
