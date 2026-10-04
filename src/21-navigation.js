/* src/21-navigation.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
function Iv(e, t = {}) { let n = e.defaultView, r = e.getElementById(`help`), i = e.getElementById(`test-view`), a = ``, o = t => { let n = e.getElementById(t); return n?.tagName === `DETAILS` && n.closest(`.guide`) ? n : null; }, s = e => { try {
    e?.();
}
catch { } }, c = (c, l = !0) => { let u = o(c), d = c === `help` || !!u; if (a = n?.location.hash ?? ``, r && i) {
    e.documentElement.dataset.helpView = String(d);
    for (let t of e.querySelectorAll(`[data-help-home]`))
        d ? t.setAttribute(`aria-current`, `page`) : t.removeAttribute(`aria-current`);
    d && s(t.onOpen);
} if (u) {
    for (let t of e.querySelectorAll(`.guide .faq-highlight`))
        t.classList.remove(`faq-highlight`);
    u.setAttribute(`open`, ``), u.classList.add(`faq-highlight`), l && s(() => { u.querySelector(`summary`)?.focus({ preventScroll: !0 }), u.scrollIntoView?.({ block: `start`, behavior: `auto` }); });
}
else
    l && d ? s(() => { e.getElementById(`help-title`)?.focus({ preventScroll: !0 }), r?.scrollIntoView?.({ block: `start`, behavior: `auto` }); }) : l && r && i && (t.onReturn ? s(t.onReturn) : s(() => { i.focus({ preventScroll: !0 }), i.scrollIntoView?.({ block: `start`, behavior: `auto` }); })); }, l = () => { n && n.location.hash !== a && c(n.location.hash.slice(1)); }, u = e => { if (e.button !== 0 || e.ctrlKey || e.metaKey || e.shiftKey || e.altKey)
    return; let t = (e.target?.closest?.(`a[data-faq-link],a[data-help-link]`))?.getAttribute(`href`); if (!t?.startsWith(`#`))
    return; let a = t.slice(1); if (!(!o(a) && !(r && i && (a === `help` || a === `test-view`)))) {
    if (n && n.location.hash !== t)
        try {
            n.history.pushState(n.history.state, ``, t);
        }
        catch {
            try {
                n.location.hash = t;
            }
            catch {
                return;
            }
        }
    e.preventDefault(), c(a);
} }; return e.addEventListener(`click`, u), n?.addEventListener(`hashchange`, l), n?.addEventListener(`popstate`, l), c(n?.location.hash.slice(1) ?? ``, !!n?.location.hash), () => { e.removeEventListener(`click`, u), n?.removeEventListener(`hashchange`, l), n?.removeEventListener(`popstate`, l), delete e.documentElement.dataset.helpView; for (let t of e.querySelectorAll(`[data-help-home]`))
    t.removeAttribute(`aria-current`); }; }
function Lv() { document.documentElement.dataset.appReady = `false`;
    if (typeof tbwReferenceSelfTest === 'undefined' || tbwReferenceSelfTest.status().phase === 'failed') {
        const title = document.getElementById('startup-title'), message = document.getElementById('startup-message');
        if (title) title.textContent = 'Reference self-check failed';
        if (message) message.textContent = 'No test wallet was created. Do not use this copy. Close the page and verify a fresh release before trying again. A self-check is not publisher authentication.';
        return;
    }
 let e = document.getElementById(`startup-title`), t = document.getElementById(`startup-message`); e && (e.textContent = `Unable to start the test`), t && (t.textContent = `The test could not initialize. Reopen this file in a current browser with secure random generation available. No test has run.`); }
