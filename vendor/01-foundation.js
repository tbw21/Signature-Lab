/* vendor/01-foundation.js: reconstructed from the reviewed v0.13.0-rc2 distribution.
 * Application symbols retained for traceability; this is not recovered original TypeScript.
 */
var e = Object.create;
var t = Object.defineProperty;
var n = Object.getOwnPropertyDescriptor;
var r = Object.getOwnPropertyNames;
var i = Object.getPrototypeOf;
var a = Object.prototype.hasOwnProperty;
var o = (e, t, n) => () => { if (n)
    throw n[0]; try {
    return e && (t = e(e = 0)), t;
}
catch (e) {
    throw n = [e], e;
} };
var s = (e, t) => () => (t || (e((t = { exports: {} }).exports, t), e = null), t.exports);
var c = (e, n) => { let r = {}; for (var i in e)
    t(r, i, { get: e[i], enumerable: !0 }); return n || t(r, Symbol.toStringTag, { value: `Module` }), r; };
var l = (e, i, o, s) => { if (i && typeof i == `object` || typeof i == `function`)
    for (var c = r(i), l = 0, u = c.length, d; l < u; l++)
        d = c[l], !a.call(e, d) && d !== o && t(e, d, { get: (e => i[e]).bind(null, d), enumerable: !(s = n(i, d)) || s.enumerable }); return e; };
var u = (n, r, o) => (o = n == null ? {} : e(i(n)), l(r || !n || !n.__esModule || !a.call(n, `default`) ? t(o, `default`, { value: n, enumerable: !0 }) : o, n));
var d = e => a.call(e, `module.exports`) ? e[`module.exports`] : l(t({}, `__esModule`, { value: !0 }), e);
(function () { let e = document.createElement(`link`).relList; if (e && e.supports && e.supports(`modulepreload`))
    return; for (let e of document.querySelectorAll(`link[rel="modulepreload"]`))
    n(e); new MutationObserver(e => { for (let t of e)
    if (t.type === `childList`)
        for (let e of t.addedNodes)
            e.tagName === `LINK` && e.rel === `modulepreload` && n(e); }).observe(document, { childList: !0, subtree: !0 }); function t(e) { let t = {}; return e.integrity && (t.integrity = e.integrity), e.referrerPolicy && (t.referrerPolicy = e.referrerPolicy), t.credentials = e.crossOrigin === `use-credentials` ? `include` : e.crossOrigin === `anonymous` ? `omit` : `same-origin`, t; } function n(e) { if (e.ep)
    return; e.ep = !0; let n = t(e); fetch(e.href, n); } })();
var f = !1;
var p = !1;
var m = [];
var h = -1;
var g = !1;
function _(e) { b(e); }
function v() { g = !0; }
function y() { g = !1, S(); }
function b(e) { m.includes(e) || m.push(e), S(); }
function x(e) { let t = m.indexOf(e); t !== -1 && t > h && m.splice(t, 1); }
function S() { if (!p && !f) {
    if (g)
        return;
    f = !0, queueMicrotask(C);
} }
function C() { f = !1, p = !0; for (let e = 0; e < m.length; e++)
    m[e](), h = e; m.length = 0, h = -1, p = !1; }
var w;
var T;
var E;
var D;
var O = !0;
function k(e) { O = !1, e(), O = !0; }
function A(e) { w = e.reactive, E = e.release, T = t => e.effect(t, { scheduler: e => { O ? _(e) : e(); } }), D = e.raw; }
function j(e) { T = e; }
function M(e) { let t = () => { }; return [n => { let r = T(n); return e._x_effects || (e._x_effects = new Set, e._x_runEffects = () => { e._x_effects.forEach(e => e()); }), e._x_effects.add(r), t = () => { r !== void 0 && (e._x_effects.delete(r), E(r)); }, r; }, () => { t(); }]; }
function N(e, t) { let n = !0, r, i, a = T(() => { let a = e(), o = JSON.stringify(a); if (!n && (typeof a == `object` || a !== r)) {
    let e = typeof r == `object` ? JSON.parse(i) : r;
    queueMicrotask(() => { t(a, e); });
} r = a, i = o, n = !1; }); return () => E(a); }
async function ee(e) { v(); try {
    await e(), await Promise.resolve();
}
finally {
    y();
} }
var P = [];
var F = [];
var I = [];
function L(e) { I.push(e); }
function R(e, t) { typeof t == `function` ? (e._x_cleanups ||= [], e._x_cleanups.push(t)) : (t = e, F.push(t)); }
function z(e) { P.push(e); }
function B(e, t, n) { e._x_attributeCleanups ||= {}, e._x_attributeCleanups[t] || (e._x_attributeCleanups[t] = []), e._x_attributeCleanups[t].push(n); }
function V(e, t) { e._x_attributeCleanups && Object.entries(e._x_attributeCleanups).forEach(([n, r]) => { (t === void 0 || t.includes(n)) && (r.forEach(e => e()), delete e._x_attributeCleanups[n]); }); }
function te(e) { for (e._x_effects?.forEach(x); e._x_cleanups?.length;)
    e._x_cleanups.pop()(); }
var ne = new MutationObserver(ue);
var re = !1;
function ie() { ne.observe(document, { subtree: !0, childList: !0, attributes: !0, attributeOldValue: !0 }), re = !0; }
function ae() { H(), ne.disconnect(), re = !1; }
var oe = [];
function H() { let e = ne.takeRecords(); oe.push(() => e.length > 0 && ue(e)); let t = oe.length; queueMicrotask(() => { if (oe.length === t)
    for (; oe.length > 0;)
        oe.shift()(); }); }
function U(e) { if (!re)
    return e(); ae(); let t = e(); return ie(), t; }
var se = !1;
var W = [];
function ce() { se = !0; }
function le() { se = !1, ue(W), W = []; }
function ue(e) { if (se) {
    W = W.concat(e);
    return;
} let t = [], n = new Set, r = new Map, i = new Map; for (let a = 0; a < e.length; a++)
    if (!e[a].target._x_ignoreMutationObserver && (e[a].type === `childList` && (e[a].removedNodes.forEach(e => { e.nodeType === 1 && e._x_marker && n.add(e); }), e[a].addedNodes.forEach(e => { if (e.nodeType === 1) {
        if (n.has(e)) {
            n.delete(e);
            return;
        }
        e._x_marker || t.push(e);
    } })), e[a].type === `attributes`)) {
        let t = e[a].target, n = e[a].attributeName, o = e[a].oldValue, s = () => { r.has(t) || r.set(t, []), r.get(t).push({ name: n, value: t.getAttribute(n) }); }, c = () => { i.has(t) || i.set(t, []), i.get(t).push(n); };
        t.hasAttribute(n) && o === null ? s() : t.hasAttribute(n) ? (c(), s()) : c();
    } i.forEach((e, t) => { V(t, e); }), r.forEach((e, t) => { P.forEach(n => n(t, e)); }); for (let e of n)
    t.some(t => t.contains(e)) || F.forEach(t => t(e)); for (let e of t)
    e.isConnected && I.forEach(t => t(e)); t = null, n = null, r = null, i = null; }
function de(e) { return me(pe(e)); }
function fe(e, t, n) { return e._x_dataStack = [t, ...pe(n || e)], () => { e._x_dataStack = e._x_dataStack.filter(e => e !== t); }; }
function pe(e) { return e._x_dataStack ? e._x_dataStack : typeof ShadowRoot == `function` && e instanceof ShadowRoot ? pe(e.host) : e.parentNode ? pe(e.parentNode) : []; }
function me(e) { return new Proxy({ objects: e }, ge); }
function he(e, t) { return e === null || e === Object.prototype ? null : Object.prototype.hasOwnProperty.call(e, t) ? e : he(Object.getPrototypeOf(e), t); }
var ge = { ownKeys({ objects: e }) { return Array.from(new Set(e.flatMap(e => Object.keys(e)))); }, has({ objects: e }, t) { return t != Symbol.unscopables && e.some(e => Object.prototype.hasOwnProperty.call(e, t) || Reflect.has(e, t)); }, get({ objects: e }, t, n) { return t == `toJSON` ? _e : Reflect.get(e.find(e => Reflect.has(e, t)) || {}, t, n); }, set({ objects: e }, t, n, r) { let i; for (let n of e)
        if (i = he(n, t), i)
            break; i ||= e[e.length - 1]; let a = Object.getOwnPropertyDescriptor(i, t); return a?.set && a?.get ? a.set.call(r, n) || !0 : Reflect.set(i, t, n); } };
function _e() { return Reflect.ownKeys(this).reduce((e, t) => (e[t] = Reflect.get(this, t), e), {}); }
function ve(e) { let t = e => typeof e == `object` && !Array.isArray(e) && e !== null, n = (r, i = ``) => { Object.entries(Object.getOwnPropertyDescriptors(r)).forEach(([a, { value: o, enumerable: s }]) => { if (s === !1 || o === void 0 || typeof o == `object` && o && o.__v_skip)
    return; let c = i === `` ? a : `${i}.${a}`; typeof o == `object` && o && o._x_interceptor ? r[a] = o.initialize(e, c, a) : t(o) && o !== r && !(o instanceof Element) && n(o, c); }); }; return n(e); }
function ye(e, t = () => { }) { let n = { initialValue: void 0, _x_interceptor: !0, initialize(t, n, r) { return e(this.initialValue, () => be(t, n), e => xe(t, n, e), n, r); } }; return t(n), e => { if (typeof e == `object` && e && e._x_interceptor) {
    let t = n.initialize.bind(n);
    n.initialize = (r, i, a) => { let o = e.initialize(r, i, a); return n.initialValue = o, t(r, i, a); };
}
else
    n.initialValue = e; return n; }; }
function be(e, t) { return t.split(`.`).reduce((e, t) => e[t], e); }
function xe(e, t, n) { if (typeof t == `string` && (t = t.split(`.`)), t.length === 1)
    e[t[0]] = n;
else if (t.length === 0)
    throw error;
else if (e[t[0]])
    return xe(e[t[0]], t.slice(1), n);
else
    return e[t[0]] = {}, xe(e[t[0]], t.slice(1), n); }
var Se = {};
function Ce(e, t) { Se[e] = t; }
function we(e, t) { let n = Te(t); return Object.entries(Se).forEach(([r, i]) => { Object.defineProperty(e, `$${r}`, { get() { return i(t, n); }, enumerable: !1 }); }), e; }
function Te(e) { let [t, n] = at(e), r = { interceptor: ye, ...t }; return R(e, n), r; }
function Ee(e, t, n, ...r) { try {
    return n(...r);
}
catch (n) {
    De(n, e, t);
} }
function De(...e) { return Oe(...e); }
var Oe = Ae;
function ke(e) { Oe = e; }
function Ae(e, t, n = void 0) {
    e = Object.assign(e ?? { message: `No error message given.` }, { el: t, expression: n }), console.warn(`Alpine Expression Error: ${e.message}

${n ? `Expression: "` + n + `"

` : ``}`, t), setTimeout(() => { throw e; }, 0);
}
var je = !0;
function Me(e) { let t = je; je = !1; let n = e(); return je = t, n; }
function Ne(e, t, n = {}) { let r; return Pe(e, t)(e => r = e, n), r; }
function Pe(...e) { return Fe(...e); }
var Fe = () => { };
function Ie(e) { Fe = e; }
var Le;
function Re(e) { Le = e; }
function ze(e, t) { let n = {}; we(n, e); let r = [n, ...pe(e)], i = typeof t == `function` ? Be(r, t) : Ue(r, t, e); return Ee.bind(null, e, t, i); }
function Be(e, t) { return (n = () => { }, { scope: r = {}, params: i = [], context: a } = {}) => { if (!je) {
    We(n, t, me([r, ...e]), i);
    return;
} We(n, t.apply(me([r, ...e]), i)); }; }
var Ve = {};
function He(e, t) { if (Ve[e])
    return Ve[e]; let n = Object.getPrototypeOf(async function () { }).constructor, r = /^[\n\s]*if.*\(.*\)/.test(e.trim()) || /^(let|const)\s/.test(e.trim()) ? `(async()=>{ ${e} })()` : e, i = (() => { try {
    let t = new n([`__self`, `scope`], `with (scope) { __self.result = ${r} }; __self.finished = true; return __self.result;`);
    return Object.defineProperty(t, "name", { value: `[Alpine] ${e}` }), t;
}
catch (n) {
    return De(n, t, e), Promise.resolve();
} })(); return Ve[e] = i, i; }
function Ue(e, t, n) { let r = He(t, n); return (i = () => { }, { scope: a = {}, params: o = [], context: s } = {}) => { r.result = void 0, r.finished = !1; let c = me([a, ...e]); if (typeof r == `function`) {
    let e = r.call(s, r, c).catch(e => De(e, n, t));
    r.finished ? (We(i, r.result, c, o, n), r.result = void 0) : e.then(e => { We(i, e, c, o, n); }).catch(e => De(e, n, t)).finally(() => r.result = void 0);
} }; }
function We(e, t, n, r, i) { if (je && typeof t == `function`) {
    let a = t.apply(n, r);
    a instanceof Promise ? a.then(t => We(e, t, n, r)).catch(e => De(e, i, t)) : e(a);
}
else
    typeof t == `object` && t instanceof Promise ? t.then(t => e(t)) : e(t); }
function Ge(...e) { return Le(...e); }
function Ke(e, t, n = {}) { let r = {}; we(r, e); let i = [r, ...pe(e)], a = me([n.scope ?? {}, ...i]), o = n.params ?? []; if (t.includes(`await`)) {
    let e = Object.getPrototypeOf(async function () { }).constructor;
    return new e([`scope`], `with (scope) { let __result = ${/^[\n\s]*if.*\(.*\)/.test(t.trim()) || /^(let|const)\s/.test(t.trim()) ? `(async()=>{ ${t} })()` : t}; return __result }`).call(n.context, a);
} {
    let e = /^[\n\s]*if.*\(.*\)/.test(t.trim()) || /^(let|const)\s/.test(t.trim()) ? `(()=>{ ${t} })()` : t, r = Function([`scope`], `with (scope) { let __result = ${e}; return __result }`).call(n.context, a);
    return typeof r == `function` && je ? r.apply(a, o) : r;
} }
var qe = `x-`;
function Je(e = ``) { return qe + e; }
function Ye(e) { qe = e; }
var Xe = {};
function Ze(e, t) { return Xe[e] = t, { before(t) { if (!Xe[t]) {
        console.warn(String.raw `Cannot find directive \`${t}\`. \`${e}\` will use the default order of execution`);
        return;
    } let n = gt.indexOf(t); gt.splice(n >= 0 ? n : gt.indexOf(`DEFAULT`), 0, e); } }; }
function Qe(e) { return Object.keys(Xe).includes(e); }
function $e(e, t, n) { if (t = Array.from(t), e._x_virtualDirectives) {
    let n = Object.entries(e._x_virtualDirectives).map(([e, t]) => ({ name: e, value: t })), r = et(n);
    n = n.map(e => r.find(t => t.name === e.name) ? { name: `x-bind:${e.name}`, value: `"${e.value}"` } : e), t = t.concat(n);
} let r = {}; return t.map(lt((e, t) => r[e] = t)).filter(ft).map(mt(r, n)).sort(_t).map(t => ot(e, t)); }
function et(e) { return Array.from(e).map(lt()).filter(e => !ft(e)); }
var tt = !1;
var nt = new Map;
var rt = Symbol();
function it(e) { tt = !0; let t = Symbol(); rt = t, nt.set(t, []); let n = () => { for (; nt.get(t).length;)
    nt.get(t).shift()(); nt.delete(t); }; e(n), tt = !1, n(); }
function at(e) { let t = [], n = e => t.push(e), [r, i] = M(e); return t.push(i), [{ Alpine: Qn, effect: r, cleanup: n, evaluateLater: Pe.bind(Pe, e), evaluate: Ne.bind(Ne, e) }, () => t.forEach(e => e())]; }
function ot(e, t) { let n = Xe[t.type] || (() => { }), [r, i] = at(e); B(e, t.original, i); let a = () => { e._x_ignore || e._x_ignoreSelf || (n.inline && n.inline(e, t, r), n = n.bind(n, e, t, r), tt ? nt.get(rt).push(n) : n()); }; return a.runCleanups = i, a; }
var st = (e, t) => ({ name: n, value: r }) => (n.startsWith(e) && (n = n.replace(e, t)), { name: n, value: r });
var ct = e => e;
function lt(e = () => { }) { return ({ name: t, value: n }) => { let { name: r, value: i } = ut.reduce((e, t) => t(e), { name: t, value: n }); return r !== t && e(r, t), { name: r, value: i }; }; }
var ut = [];
function dt(e) { ut.push(e); }
function ft({ name: e }) { return pt().test(e); }
var pt = () => RegExp(`^${qe}([^:^.]+)\\b`);
function mt(e, t) { return ({ name: n, value: r }) => { n === r && (r = ``); let i = n.match(pt()), a = n.match(/:([a-zA-Z0-9\-_:]+)/), o = n.match(/\.[^.\]]+(?=[^\]]*$)/g) || [], s = t || e[n] || n; return { type: i ? i[1] : null, value: a ? a[1] : null, modifiers: o.map(e => e.replace(`.`, ``)), expression: r, original: s }; }; }
var ht = `DEFAULT`;
var gt = [`ignore`, `ref`, `id`, `data`, `anchor`, `bind`, `init`, `for`, `model`, `modelable`, `transition`, `show`, `if`, ht, `teleport`];
function _t(e, t) { let n = gt.indexOf(e.type) === -1 ? ht : e.type, r = gt.indexOf(t.type) === -1 ? ht : t.type; return gt.indexOf(n) - gt.indexOf(r); }
function vt(e, t, n = {}, r = {}) { return e.dispatchEvent(new CustomEvent(t, { detail: n, bubbles: !0, composed: !0, cancelable: !0, ...r })); }
function yt(e, t) { if (typeof ShadowRoot == `function` && e instanceof ShadowRoot) {
    Array.from(e.children).forEach(e => yt(e, t));
    return;
} let n = !1; if (t(e, () => n = !0), n)
    return; let r = e.firstElementChild; for (; r;)
    yt(r, t, !1), r = r.nextElementSibling; }
function bt(e, ...t) { console.warn(`Alpine Warning: ${e}`, ...t); }
var xt = !1;
function St() { xt && bt(`Alpine has already been initialized on this page. Calling Alpine.start() more than once can cause problems.`), xt = !0, document.body || bt("Unable to initialize. Trying to load Alpine before `<body>` is available. Did you forget to add `defer` in Alpine's `<script>` tag?"), vt(document, `alpine:init`), vt(document, `alpine:initializing`), ie(), L(e => Ft(e, yt)), R(e => It(e)), z((e, t) => { $e(e, t).forEach(e => e()); }), Array.from(document.querySelectorAll(Et().join(`,`))).filter(e => !kt(e.parentElement, !0)).forEach(e => { Ft(e); }), vt(document, `alpine:initialized`), setTimeout(() => { Lt(); }); }
var Ct = [];
var wt = [];
function Tt() { return Ct.map(e => e()); }
function Et() { return Ct.concat(wt).map(e => e()); }
function Dt(e) { Ct.push(e); }
function Ot(e) { wt.push(e); }
function kt(e, t = !1) { return At(e, e => { if ((t ? Et() : Tt()).some(t => e.matches(t)))
    return !0; }); }
function At(e, t) { if (e) {
    if (t(e))
        return e;
    if (e._x_teleportBack)
        return At(e._x_teleportBack, t);
    if (e.parentNode instanceof ShadowRoot)
        return At(e.parentNode.host, t);
    if (e.parentElement)
        return At(e.parentElement, t);
} }
function jt(e) { return Tt().some(t => e.matches(t)); }
var Mt = [];
function Nt(e) { Mt.push(e); }
var Pt = 1;
function Ft(e, t = yt, n = () => { }) { At(e, e => e._x_ignore) || it(() => { t(e, (e, t) => { e._x_marker || (n(e, t), Mt.forEach(n => n(e, t)), $e(e, e.attributes).forEach(e => e()), e._x_ignore || (e._x_marker = Pt++), e._x_ignore && t()); }); }); }
function It(e, t = yt) { t(e, e => { te(e), V(e), delete e._x_marker; }); }
function Lt() { [[`ui`, `dialog`, [`[x-dialog], [x-popover]`]], [`anchor`, `anchor`, [`[x-anchor]`]], [`sort`, `sort`, [`[x-sort]`]]].forEach(([e, t, n]) => { Qe(t) || n.some(t => { if (document.querySelector(t))
    return bt(`found "${t}", but missing ${e} plugin`), !0; }); }); }
var Rt = [];
var zt = !1;
function Bt(e = () => { }) { return queueMicrotask(() => { zt || setTimeout(() => { Vt(); }); }), new Promise(t => { Rt.push(() => { e(), t(); }); }); }
function Vt() { for (zt = !1; Rt.length;)
    Rt.shift()(); }
function Ht() { zt = !0; }
function Ut(e, t) { return Array.isArray(t) ? Gt(e, t.join(` `)) : typeof t == `object` && t ? Kt(e, t) : typeof t == `function` ? Ut(e, t()) : Gt(e, t); }
function Wt(e) { return e.split(/\s/).filter(Boolean); }
function Gt(e, t) { return t = t === !0 ? t = `` : t || ``, (t => (e.classList.add(...t), () => { e.classList.remove(...t); }))((t => Wt(t).filter(t => !e.classList.contains(t)).filter(Boolean))(t)); }
function Kt(e, t) { let n = Object.entries(t).flatMap(([e, t]) => t ? Wt(e) : !1).filter(Boolean), r = Object.entries(t).flatMap(([e, t]) => !t && Wt(e)).filter(Boolean), i = [], a = []; return r.forEach(t => { e.classList.contains(t) && (e.classList.remove(t), a.push(t)); }), n.forEach(t => { e.classList.contains(t) || (e.classList.add(t), i.push(t)); }), () => { a.forEach(t => e.classList.add(t)), i.forEach(t => e.classList.remove(t)); }; }
function qt(e, t) { return typeof t == `object` && t ? Jt(e, t) : Yt(e, t); }
function Jt(e, t) { let n = {}; return Object.entries(t).forEach(([t, r]) => { n[t] = e.style[t], t.startsWith(`--`) || (t = Xt(t)), e.style.setProperty(t, r); }), setTimeout(() => { e.style.length === 0 && e.removeAttribute(`style`); }), () => { qt(e, n); }; }
function Yt(e, t) { let n = e.getAttribute(`style`, t); return e.setAttribute(`style`, t), () => { e.setAttribute(`style`, n || ``); }; }
function Xt(e) { return e.replace(/([a-z])([A-Z])/g, `$1-$2`).toLowerCase(); }
function Zt(e, t = () => { }) { let n = !1; return function () { n ? t.apply(this, arguments) : (n = !0, e.apply(this, arguments)); }; }
Ze(`transition`, (e, { value: t, modifiers: n, expression: r }, { evaluate: i }) => { typeof r == `function` && (r = i(r)), r !== !1 && (!r || typeof r == `boolean` ? $t(e, n, t) : Qt(e, r, t)); });
function Qt(e, t, n) { en(e, Ut, ``), { enter: t => { e._x_transition.enter.during = t; }, "enter-start": t => { e._x_transition.enter.start = t; }, "enter-end": t => { e._x_transition.enter.end = t; }, leave: t => { e._x_transition.leave.during = t; }, "leave-start": t => { e._x_transition.leave.start = t; }, "leave-end": t => { e._x_transition.leave.end = t; } }[n](t); }
function $t(e, t, n) { en(e, qt); let r = !t.includes(`in`) && !t.includes(`out`) && !n, i = r || t.includes(`in`) || [`enter`].includes(n), a = r || t.includes(`out`) || [`leave`].includes(n); t.includes(`in`) && !r && (t = t.filter((e, n) => n < t.indexOf(`out`))), t.includes(`out`) && !r && (t = t.filter((e, n) => n > t.indexOf(`out`))); let o = !t.includes(`opacity`) && !t.includes(`scale`), s = o || t.includes(`opacity`), c = o || t.includes(`scale`), l = +!s, u = c ? an(t, `scale`, 95) / 100 : 1, d = an(t, `delay`, 0) / 1e3, f = an(t, `origin`, `center`), p = `opacity, transform`, m = an(t, `duration`, 150) / 1e3, h = an(t, `duration`, 75) / 1e3, g = `cubic-bezier(0.4, 0.0, 0.2, 1)`; i && (e._x_transition.enter.during = { transformOrigin: f, transitionDelay: `${d}s`, transitionProperty: p, transitionDuration: `${m}s`, transitionTimingFunction: g }, e._x_transition.enter.start = { opacity: l, transform: `scale(${u})` }, e._x_transition.enter.end = { opacity: 1, transform: `scale(1)` }), a && (e._x_transition.leave.during = { transformOrigin: f, transitionDelay: `${d}s`, transitionProperty: p, transitionDuration: `${h}s`, transitionTimingFunction: g }, e._x_transition.leave.start = { opacity: 1, transform: `scale(1)` }, e._x_transition.leave.end = { opacity: l, transform: `scale(${u})` }); }
function en(e, t, n = {}) { e._x_transition ||= { enter: { during: n, start: n, end: n }, leave: { during: n, start: n, end: n }, in(n = () => { }, r = () => { }) { nn(e, t, { during: this.enter.during, start: this.enter.start, end: this.enter.end }, n, r); }, out(n = () => { }, r = () => { }) { nn(e, t, { during: this.leave.during, start: this.leave.start, end: this.leave.end }, n, r); } }; }
window.Element.prototype._x_toggleAndCascadeWithTransitions = function (e, t, n, r) { let i = document.visibilityState === `visible` ? requestAnimationFrame : setTimeout, a = () => i(n); if (t) {
    e._x_transition && (e._x_transition.enter || e._x_transition.leave) ? e._x_transition.enter && (Object.entries(e._x_transition.enter.during).length || Object.entries(e._x_transition.enter.start).length || Object.entries(e._x_transition.enter.end).length) ? e._x_transition.in(n) : a() : e._x_transition ? e._x_transition.in(n) : a();
    return;
} e._x_hidePromise = e._x_transition ? new Promise((t, n) => { e._x_transition.out(() => { }, () => t(r)), e._x_transitioning && e._x_transitioning.beforeCancel(() => n({ isFromCancelledTransition: !0 })); }) : Promise.resolve(r), queueMicrotask(() => { let t = tn(e); t ? (t._x_hideChildren ||= [], t._x_hideChildren.push(e)) : i(() => { let t = e => { let n = Promise.all([e._x_hidePromise, ...(e._x_hideChildren || []).map(t)]).then(([e]) => e?.()); return delete e._x_hidePromise, delete e._x_hideChildren, n; }; t(e).catch(e => { if (!e.isFromCancelledTransition)
    throw e; }); }); }); };
function tn(e) { let t = e.parentNode; if (t)
    return t._x_hidePromise ? t : tn(t); }
function nn(e, t, { during: n, start: r, end: i } = {}, a = () => { }, o = () => { }) { if (e._x_transitioning && e._x_transitioning.cancel(), Object.keys(n).length === 0 && Object.keys(r).length === 0 && Object.keys(i).length === 0) {
    a(), o();
    return;
} let s, c, l; rn(e, { start() { s = t(e, r); }, during() { c = t(e, n); }, before: a, end() { s(), l = t(e, i); }, after: o, cleanup() { c(), l(); } }); }
function rn(e, t) { let n, r, i, a = Zt(() => { U(() => { n = !0, r || t.before(), i || (t.end(), Vt()), t.after(), e.isConnected && t.cleanup(), delete e._x_transitioning; }); }); e._x_transitioning = { beforeCancels: [], beforeCancel(e) { this.beforeCancels.push(e); }, cancel: Zt(function () { for (; this.beforeCancels.length;)
        this.beforeCancels.shift()(); a(); }), finish: a }, U(() => { t.start(), t.during(); }), Ht(), requestAnimationFrame(() => { if (n)
    return; let a = Number(getComputedStyle(e).transitionDuration.replace(/,.*/, ``).replace(`s`, ``)) * 1e3, o = Number(getComputedStyle(e).transitionDelay.replace(/,.*/, ``).replace(`s`, ``)) * 1e3; a === 0 && (a = Number(getComputedStyle(e).animationDuration.replace(`s`, ``)) * 1e3), U(() => { t.before(); }), r = !0, requestAnimationFrame(() => { n || (U(() => { t.end(); }), Vt(), setTimeout(e._x_transitioning.finish, a + o), i = !0); }); }); }
function an(e, t, n) { if (e.indexOf(t) === -1)
    return n; let r = e[e.indexOf(t) + 1]; if (!r || t === `scale` && isNaN(r))
    return n; if (t === `duration` || t === `delay`) {
    let e = r.match(/([0-9]+)ms/);
    if (e)
        return e[1];
} return t === `origin` && [`top`, `right`, `left`, `center`, `bottom`].includes(e[e.indexOf(t) + 2]) ? [r, e[e.indexOf(t) + 2]].join(` `) : r; }
var on = !1;
function sn(e, t = () => { }) { return (...n) => on ? t(...n) : e(...n); }
function cn(e) { return (...t) => on && e(...t); }
var ln = [];
function un(e) { ln.push(e); }
function dn(e, t) { ln.forEach(n => n(e, t)), on = !0, hn(() => { Ft(t, (e, t) => { t(e, () => { }); }); }), on = !1; }
var fn = !1;
function pn(e, t) { t._x_dataStack ||= e._x_dataStack, on = !0, fn = !0, hn(() => { mn(t); }), on = !1, fn = !1; }
function mn(e) { let t = !1; Ft(e, (e, n) => { yt(e, (e, r) => { if (t && jt(e))
    return r(); t = !0, n(e, r); }); }); }
function hn(e) { let t = T; j((e, n) => { let r = t(e); return E(r), () => { }; }), e(), j(t); }
function gn(e, t, n, r = []) { switch (e._x_bindings ||= w({}), e._x_bindings[t] = n, t = r.includes(`camel`) ? Tn(t) : t, t) {
    case `value`:
        _n(e, n);
        break;
    case `style`:
        yn(e, n);
        break;
    case `class`:
        vn(e, n);
        break;
    case `selected`:
    case `checked`:
        bn(e, t, n);
        break;
    default: xn(e, t, n);
} }
function _n(e, t) { if (Fn(e))
    e.attributes.value === void 0 && (e.value = t);
else if (Pn(e))
    Number.isInteger(t) ? e.value = t : !Array.isArray(t) && typeof t != `boolean` && ![null, void 0].includes(t) ? e.value = String(t) : e.checked = Array.isArray(t) ? t.some(t => En(t, e.value)) : !!t;
else if (e.tagName === `SELECT`)
    wn(e, t);
else {
    if (e.value === t)
        return;
    e.value = t === void 0 ? `` : t;
} }
function vn(e, t) { e._x_undoAddedClasses && e._x_undoAddedClasses(), e._x_undoAddedClasses = Ut(e, t); }
function yn(e, t) { e._x_undoAddedStyles && e._x_undoAddedStyles(), e._x_undoAddedStyles = qt(e, t); }
function bn(e, t, n) { xn(e, t, n), Cn(e, t, n); }
function xn(e, t, n) { [null, void 0, !1].includes(n) && An(t) ? e.removeAttribute(t) : (kn(t) && (n = t), Sn(e, t, n)); }
function Sn(e, t, n) { e.getAttribute(t) != n && e.setAttribute(t, n); }
function Cn(e, t, n) { e[t] !== n && (e[t] = n); }
function wn(e, t) { let n = [].concat(t).map(e => e + ``); Array.from(e.options).forEach(e => { e.selected = n.includes(e.value); }); }
function Tn(e) { return e.toLowerCase().replace(/-(\w)/g, (e, t) => t.toUpperCase()); }
function En(e, t) { return e == t; }
function Dn(e) { return [1, `1`, `true`, `on`, `yes`, !0].includes(e) ? !0 : [0, `0`, `false`, `off`, `no`, !1].includes(e) ? !1 : e ? !!e : null; }
var On = new Set(`allowfullscreen.async.autofocus.autoplay.checked.controls.default.defer.disabled.formnovalidate.inert.ismap.itemscope.loop.multiple.muted.nomodule.novalidate.open.playsinline.readonly.required.reversed.selected.shadowrootclonable.shadowrootdelegatesfocus.shadowrootserializable`.split(`.`));
function kn(e) { return On.has(e); }
function An(e) { return ![`aria-pressed`, `aria-checked`, `aria-expanded`, `aria-selected`].includes(e); }
function jn(e, t, n) { return e._x_bindings && e._x_bindings[t] !== void 0 ? e._x_bindings[t] : Nn(e, t, n); }
function Mn(e, t, n, r = !0) { if (e._x_bindings && e._x_bindings[t] !== void 0)
    return e._x_bindings[t]; if (e._x_inlineBindings && e._x_inlineBindings[t] !== void 0) {
    let n = e._x_inlineBindings[t];
    return n.extract = r, Me(() => Ne(e, n.expression));
} return Nn(e, t, n); }
function Nn(e, t, n) { let r = e.getAttribute(t); return r === null ? typeof n == `function` ? n() : n : r === `` ? !0 : kn(t) ? !![t, `true`].includes(r) : r; }
function Pn(e) { return e.type === `checkbox` || e.localName === `ui-checkbox` || e.localName === `ui-switch`; }
function Fn(e) { return e.type === `radio` || e.localName === `ui-radio`; }
function In(e, t) { let n; return function () { let r = this, i = arguments; clearTimeout(n), n = setTimeout(function () { n = null, e.apply(r, i); }, t); }; }
function Ln(e, t) { let n; return function () { let r = this, i = arguments; n || (e.apply(r, i), n = !0, setTimeout(() => n = !1, t)); }; }
function Rn({ get: e, set: t }, { get: n, set: r }) { let i = !0, a, o = T(() => { let o = e(), s = n(); if (i)
    r(zn(o)), i = !1;
else {
    let e = JSON.stringify(o), n = JSON.stringify(s);
    e === a ? e !== n && t(zn(s)) : r(zn(o));
} a = JSON.stringify(e()), JSON.stringify(n()); }); return () => { E(o); }; }
function zn(e) { return typeof e == `object` ? JSON.parse(JSON.stringify(e)) : e; }
function Bn(e) { (Array.isArray(e) ? e : [e]).forEach(e => e(Qn)); }
var Vn = {};
var Hn = !1;
function Un(e, t) { if (Hn ||= (Vn = w(Vn), !0), t === void 0)
    return Vn[e]; Vn[e] = t, ve(Vn[e]), typeof t == `object` && t && t.hasOwnProperty(`init`) && typeof t.init == `function` && Vn[e].init(); }
function Wn() { return Vn; }
var Gn = {};
function Kn(e, t) { let n = typeof t == `function` ? t : () => t; return e instanceof Element ? Jn(e, n()) : (Gn[e] = n, () => { }); }
function qn(e) { return Object.entries(Gn).forEach(([t, n]) => { Object.defineProperty(e, t, { get() { return (...e) => n(...e); } }); }), e; }
function Jn(e, t, n) { let r = []; for (; r.length;)
    r.pop()(); let i = Object.entries(t).map(([e, t]) => ({ name: e, value: t })), a = et(i); return i = i.map(e => a.find(t => t.name === e.name) ? { name: `x-bind:${e.name}`, value: `"${e.value}"` } : e), $e(e, i, n).map(e => { r.push(e.runCleanups), e(); }), () => { for (; r.length;)
    r.pop()(); }; }
var Yn = {};
function Xn(e, t) { Yn[e] = t; }
function Zn(e, t) { return Object.entries(Yn).forEach(([n, r]) => { Object.defineProperty(e, n, { get() { return (...e) => r.bind(t)(...e); }, enumerable: !1 }); }), e; }
var Qn = { get reactive() { return w; }, get release() { return E; }, get effect() { return T; }, get raw() { return D; }, get transaction() { return ee; }, version: `3.15.12`, flushAndStopDeferringMutations: le, dontAutoEvaluateFunctions: Me, disableEffectScheduling: k, startObservingMutations: ie, stopObservingMutations: ae, setReactivityEngine: A, onAttributeRemoved: B, onAttributesAdded: z, closestDataStack: pe, skipDuringClone: sn, onlyDuringClone: cn, addRootSelector: Dt, addInitSelector: Ot, setErrorHandler: ke, interceptClone: un, addScopeToNode: fe, deferMutations: ce, mapAttributes: dt, evaluateLater: Pe, interceptInit: Nt, initInterceptors: ve, injectMagics: we, setEvaluator: Ie, setRawEvaluator: Re, mergeProxies: me, extractProp: Mn, findClosest: At, onElRemoved: R, closestRoot: kt, destroyTree: It, interceptor: ye, transition: nn, setStyles: qt, mutateDom: U, directive: Ze, entangle: Rn, throttle: Ln, debounce: In, evaluate: Ne, evaluateRaw: Ge, initTree: Ft, nextTick: Bt, prefixed: Je, prefix: Ye, plugin: Bn, magic: Ce, store: Un, start: St, clone: pn, cloneNode: dn, bound: jn, $data: de, watch: N, walk: yt, data: Xn, bind: Kn };
function $n(e, t) { let n = Object.create(null), r = e.split(`,`); for (let e = 0; e < r.length; e++)
    n[r[e]] = !0; return t ? e => !!n[e.toLowerCase()] : e => !!n[e]; }
var er = Object.freeze({});
Object.freeze([]);
var tr = Object.prototype.hasOwnProperty;
var nr = (e, t) => tr.call(e, t);
var rr = Array.isArray;
var ir = e => lr(e) === `[object Map]`;
var ar = e => typeof e == `string`;
var or = e => typeof e == `symbol`;
var sr = e => typeof e == `object` && !!e;
var cr = Object.prototype.toString;
var lr = e => cr.call(e);
var ur = e => lr(e).slice(8, -1);
var dr = e => ar(e) && e !== `NaN` && e[0] !== `-` && `` + parseInt(e, 10) === e;
var fr = (e => { let t = Object.create(null); return n => t[n] || (t[n] = e(n)); })(e => e.charAt(0).toUpperCase() + e.slice(1));
var pr = (e, t) => e !== t && (e === e || t === t);
var mr = new WeakMap;
var hr = [];
var gr;
var _r = Symbol(`iterate`);
var vr = Symbol(`Map key iterate`);
function yr(e) { return e && e._isEffect === !0; }
function br(e, t = er) { yr(e) && (e = e.raw); let n = Cr(e, t); return t.lazy || n(), n; }
function xr(e) { e.active &&= (wr(e), e.options.onStop && e.options.onStop(), !1); }
var Sr = 0;
function Cr(e, t) { let n = function () { if (!n.active)
    return e(); if (!hr.includes(n)) {
    wr(n);
    try {
        return Or(), hr.push(n), gr = n, e();
    }
    finally {
        hr.pop(), kr(), gr = hr[hr.length - 1];
    }
} }; return n.id = Sr++, n.allowRecurse = !!t.allowRecurse, n._isEffect = !0, n.active = !0, n.raw = e, n.deps = [], n.options = t, n; }
function wr(e) { let { deps: t } = e; if (t.length) {
    for (let n = 0; n < t.length; n++)
        t[n].delete(e);
    t.length = 0;
} }
var Tr = !0;
var Er = [];
function Dr() { Er.push(Tr), Tr = !1; }
function Or() { Er.push(Tr), Tr = !0; }
function kr() { let e = Er.pop(); Tr = e === void 0 || e; }
function Ar(e, t, n) { if (!Tr || gr === void 0)
    return; let r = mr.get(e); r || mr.set(e, r = new Map); let i = r.get(n); i || r.set(n, i = new Set), i.has(gr) || (i.add(gr), gr.deps.push(i), gr.options.onTrack && gr.options.onTrack({ effect: gr, target: e, type: t, key: n })); }
function jr(e, t, n, r, i, a) { let o = mr.get(e); if (!o)
    return; let s = new Set, c = e => { e && e.forEach(e => { (e !== gr || e.allowRecurse) && s.add(e); }); }; if (t === `clear`)
    o.forEach(c);
else if (n === `length` && rr(e))
    o.forEach((e, t) => { (t === `length` || t >= r) && c(e); });
else
    switch (n !== void 0 && c(o.get(n)), t) {
        case `add`:
            rr(e) ? dr(n) && c(o.get(`length`)) : (c(o.get(_r)), ir(e) && c(o.get(vr)));
            break;
        case `delete`:
            rr(e) || (c(o.get(_r)), ir(e) && c(o.get(vr)));
            break;
        case `set`: ir(e) && c(o.get(_r));
    } s.forEach(o => { o.options.onTrigger && o.options.onTrigger({ effect: o, target: e, key: n, type: t, newValue: r, oldValue: i, oldTarget: a }), o.options.scheduler ? o.options.scheduler(o) : o(); }); }
var Mr = $n(`__proto__,__v_isRef,__isVue`);
var Nr = new Set(Object.getOwnPropertyNames(Symbol).map(e => Symbol[e]).filter(or));
var Pr = Rr();
var Fr = Rr(!0);
var Ir = Lr();
function Lr() { let e = {}; return [`includes`, `indexOf`, `lastIndexOf`].forEach(t => { e[t] = function (...e) { let n = G(this); for (let e = 0, t = this.length; e < t; e++)
    Ar(n, `get`, e + ``); let r = n[t](...e); return r === -1 || r === !1 ? n[t](...e.map(G)) : r; }; }), [`push`, `pop`, `shift`, `unshift`, `splice`].forEach(t => { e[t] = function (...e) { Dr(); let n = G(this)[t].apply(this, e); return kr(), n; }; }), e; }
function Rr(e = !1, t = !1) { return function (n, r, i) { if (r === `__v_isReactive`)
    return !e; if (r === `__v_isReadonly`)
    return e; if (r === `__v_raw` && i === (e ? t ? vi : _i : t ? gi : hi).get(n))
    return n; let a = rr(n); if (!e && a && nr(Ir, r))
    return Reflect.get(Ir, r, i); let o = Reflect.get(n, r, i); return (or(r) ? Nr.has(r) : Mr(r)) || (e || Ar(n, `get`, r), t) ? o : wi(o) ? !a || !dr(r) ? o.value : o : sr(o) ? e ? Si(o) : xi(o) : o; }; }
var zr = Br();
function Br(e = !1) { return function (t, n, r, i) { let a = t[n]; if (!e && (r = G(r), a = G(a), !rr(t) && wi(a) && !wi(r)))
    return a.value = r, !0; let o = rr(t) && dr(n) ? Number(n) < t.length : nr(t, n), s = Reflect.set(t, n, r, i); return t === G(i) && (o ? pr(r, a) && jr(t, `set`, n, r, a) : jr(t, `add`, n, r)), s; }; }
function Vr(e, t) { let n = nr(e, t), r = e[t], i = Reflect.deleteProperty(e, t); return i && n && jr(e, `delete`, t, void 0, r), i; }
function Hr(e, t) { let n = Reflect.has(e, t); return (!or(t) || !Nr.has(t)) && Ar(e, `has`, t), n; }
function Ur(e) { return Ar(e, `iterate`, rr(e) ? `length` : _r), Reflect.ownKeys(e); }
var Wr = { get: Pr, set: zr, deleteProperty: Vr, has: Hr, ownKeys: Ur };
var Gr = { get: Fr, set(e, t) { return console.warn(`Set operation on key "${String(t)}" failed: target is readonly.`, e), !0; }, deleteProperty(e, t) { return console.warn(`Delete operation on key "${String(t)}" failed: target is readonly.`, e), !0; } };
var Kr = e => sr(e) ? xi(e) : e;
var qr = e => sr(e) ? Si(e) : e;
var Jr = e => e;
var Yr = e => Reflect.getPrototypeOf(e);
function Xr(e, t, n = !1, r = !1) { e = e.__v_raw; let i = G(e), a = G(t); t !== a && !n && Ar(i, `get`, t), !n && Ar(i, `get`, a); let { has: o } = Yr(i), s = r ? Jr : n ? qr : Kr; if (o.call(i, t))
    return s(e.get(t)); if (o.call(i, a))
    return s(e.get(a)); e !== i && e.get(t); }
function Zr(e, t = !1) { let n = this.__v_raw, r = G(n), i = G(e); return e !== i && !t && Ar(r, `has`, e), !t && Ar(r, `has`, i), e === i ? n.has(e) : n.has(e) || n.has(i); }
function Qr(e, t = !1) { return e = e.__v_raw, !t && Ar(G(e), `iterate`, _r), Reflect.get(e, `size`, e); }
function $r(e) { e = G(e); let t = G(this); return Yr(t).has.call(t, e) || (t.add(e), jr(t, `add`, e, e)), this; }
function ei(e, t) { t = G(t); let n = G(this), { has: r, get: i } = Yr(n), a = r.call(n, e); a ? mi(n, r, e) : (e = G(e), a = r.call(n, e)); let o = i.call(n, e); return n.set(e, t), a ? pr(t, o) && jr(n, `set`, e, t, o) : jr(n, `add`, e, t), this; }
function ti(e) { let t = G(this), { has: n, get: r } = Yr(t), i = n.call(t, e); i ? mi(t, n, e) : (e = G(e), i = n.call(t, e)); let a = r ? r.call(t, e) : void 0, o = t.delete(e); return i && jr(t, `delete`, e, void 0, a), o; }
function ni() { let e = G(this), t = e.size !== 0, n = ir(e) ? new Map(e) : new Set(e), r = e.clear(); return t && jr(e, `clear`, void 0, void 0, n), r; }
function ri(e, t) { return function (n, r) { let i = this, a = i.__v_raw, o = G(a), s = t ? Jr : e ? qr : Kr; return !e && Ar(o, `iterate`, _r), a.forEach((e, t) => n.call(r, s(e), s(t), i)); }; }
function ii(e, t, n) { return function (...r) { let i = this.__v_raw, a = G(i), o = ir(a), s = e === `entries` || e === Symbol.iterator && o, c = e === `keys` && o, l = i[e](...r), u = n ? Jr : t ? qr : Kr; return !t && Ar(a, `iterate`, c ? vr : _r), { next() { let { value: e, done: t } = l.next(); return t ? { value: e, done: t } : { value: s ? [u(e[0]), u(e[1])] : u(e), done: t }; }, [Symbol.iterator]() { return this; } }; }; }
function ai(e) { return function (...t) { {
    let n = t[0] ? `on key "${t[0]}" ` : ``;
    console.warn(`${fr(e)} operation ${n}failed: target is readonly.`, G(this));
} return e !== `delete` && this; }; }
function oi() { let e = { get(e) { return Xr(this, e); }, get size() { return Qr(this); }, has: Zr, add: $r, set: ei, delete: ti, clear: ni, forEach: ri(!1, !1) }, t = { get(e) { return Xr(this, e, !1, !0); }, get size() { return Qr(this); }, has: Zr, add: $r, set: ei, delete: ti, clear: ni, forEach: ri(!1, !0) }, n = { get(e) { return Xr(this, e, !0); }, get size() { return Qr(this, !0); }, has(e) { return Zr.call(this, e, !0); }, add: ai(`add`), set: ai(`set`), delete: ai(`delete`), clear: ai(`clear`), forEach: ri(!0, !1) }, r = { get(e) { return Xr(this, e, !0, !0); }, get size() { return Qr(this, !0); }, has(e) { return Zr.call(this, e, !0); }, add: ai(`add`), set: ai(`set`), delete: ai(`delete`), clear: ai(`clear`), forEach: ri(!0, !0) }; return [`keys`, `values`, `entries`, Symbol.iterator].forEach(i => { e[i] = ii(i, !1, !1), n[i] = ii(i, !0, !1), t[i] = ii(i, !1, !0), r[i] = ii(i, !0, !0); }), [e, n, t, r]; }
var [si, ci, li, ui] = oi();
function di(e, t) { let n = t ? e ? ui : li : e ? ci : si; return (t, r, i) => r === `__v_isReactive` ? !e : r === `__v_isReadonly` ? e : r === `__v_raw` ? t : Reflect.get(nr(n, r) && r in t ? n : t, r, i); }
var fi = { get: di(!1, !1) };
var pi = { get: di(!0, !1) };
function mi(e, t, n) { let r = G(n); if (r !== n && t.call(e, r)) {
    let t = ur(e);
    console.warn(`Reactive ${t} contains both the raw and reactive versions of the same object${t === `Map` ? ` as keys` : ``}, which can lead to inconsistencies. Avoid differentiating between the raw and reactive versions of an object and only use the reactive version if possible.`);
} }
var hi = new WeakMap;
var gi = new WeakMap;
var _i = new WeakMap;
var vi = new WeakMap;
function yi(e) { switch (e) {
    case `Object`:
    case `Array`: return 1;
    case `Map`:
    case `Set`:
    case `WeakMap`:
    case `WeakSet`: return 2;
    default: return 0;
} }
function bi(e) { return e.__v_skip || !Object.isExtensible(e) ? 0 : yi(ur(e)); }
function xi(e) { return e && e.__v_isReadonly ? e : Ci(e, !1, Wr, fi, hi); }
function Si(e) { return Ci(e, !0, Gr, pi, _i); }
function Ci(e, t, n, r, i) { if (!sr(e))
    return console.warn(`value cannot be made reactive: ${String(e)}`), e; if (e.__v_raw && !(t && e.__v_isReactive))
    return e; let a = i.get(e); if (a)
    return a; let o = bi(e); if (o === 0)
    return e; let s = new Proxy(e, o === 2 ? r : n); return i.set(e, s), s; }
function G(e) { return e && G(e.__v_raw) || e; }
function wi(e) { return !!(e && e.__v_isRef === !0); }
Ce(`nextTick`, () => Bt), Ce(`dispatch`, e => vt.bind(vt, e)), Ce(`watch`, (e, { evaluateLater: t, cleanup: n }) => (e, r) => { let i = t(e); n(N(() => { let e; return i(t => e = t), e; }, r)); }), Ce(`store`, Wn), Ce(`data`, e => de(e)), Ce(`root`, e => kt(e)), Ce(`refs`, e => (e._x_refs_proxy ||= me(Ti(e)), e._x_refs_proxy));
function Ti(e) { let t = []; return At(e, e => { e._x_refs && t.push(e._x_refs); }), t; }
var Ei = {};
function Di(e) { return Ei[e] || (Ei[e] = 0), ++Ei[e]; }
function Oi(e, t) { return At(e, e => { if (e._x_ids && e._x_ids[t])
    return !0; }); }
function ki(e, t) { e._x_ids ||= {}, e._x_ids[t] || (e._x_ids[t] = Di(t)); }
Ce(`id`, (e, { cleanup: t }) => (n, r = null) => Ai(e, `${n}${r ? `-${r}` : ``}`, t, () => { let t = Oi(e, n), i = t ? t._x_ids[n] : Di(n); return r ? `${n}-${i}-${r}` : `${n}-${i}`; })), un((e, t) => { e._x_id && (t._x_id = e._x_id); });
function Ai(e, t, n, r) { if (e._x_id ||= {}, e._x_id[t])
    return e._x_id[t]; let i = r(); return e._x_id[t] = i, n(() => { delete e._x_id[t]; }), i; }
Ce(`el`, e => e), ji(`Focus`, `focus`, `focus`), ji(`Persist`, `persist`, `persist`);
function ji(e, t, n) { Ce(t, r => bt(`You can't use [$${t}] without first installing the "${e}" plugin here: https://alpinejs.dev/plugins/${n}`, r)); }
Ze(`modelable`, (e, { expression: t }, { effect: n, evaluateLater: r, cleanup: i }) => { let a = r(t), o = () => { let e; return a(t => e = t), e; }, s = r(`${t} = __placeholder`), c = e => s(() => { }, { scope: { __placeholder: e } }); c(o()), queueMicrotask(() => { if (!e._x_model)
    return; e._x_removeModelListeners.default(); let t = e._x_model.get, n = e._x_model.setWithModifiers; i(Rn({ get() { return t(); }, set(e) { n(e); } }, { get() { return o(); }, set(e) { c(e); } })); }); }), Ze(`teleport`, (e, { modifiers: t, expression: n }, { cleanup: r }) => { e.tagName.toLowerCase() !== `template` && bt(`x-teleport can only be used on a <template> tag`, e); let i = Ni(n), a = e.content.cloneNode(!0).firstElementChild; e._x_teleport = a, a._x_teleportBack = e, e.setAttribute(`data-teleport-template`, !0), a.setAttribute(`data-teleport-target`, !0), e._x_forwardEvents && e._x_forwardEvents.forEach(t => { a.addEventListener(t, t => { t.stopPropagation(), e.dispatchEvent(new t.constructor(t.type, t)); }); }), fe(a, {}, e); let o = (e, t, n) => { n.includes(`prepend`) ? t.parentNode.insertBefore(e, t) : n.includes(`append`) ? t.parentNode.insertBefore(e, t.nextSibling) : t.appendChild(e); }; U(() => { sn(() => { o(a, i, t), Ft(a); })(); }), e._x_teleportPutBack = () => { let r = Ni(n); U(() => { o(e._x_teleport, r, t); }); }, r(() => U(() => { a.remove(), It(a); })); });
var Mi = document.createElement(`div`);
function Ni(e) { let t = sn(() => document.querySelector(e), () => Mi)(); return t || bt(`Cannot find x-teleport element for selector: "${e}"`), t; }
var Pi = () => { };
Pi.inline = (e, { modifiers: t }, { cleanup: n }) => { t.includes(`self`) ? e._x_ignoreSelf = !0 : e._x_ignore = !0, n(() => { t.includes(`self`) ? delete e._x_ignoreSelf : delete e._x_ignore; }); }, Ze(`ignore`, Pi), Ze(`effect`, sn((e, { expression: t }, { effect: n }) => { n(Pe(e, t)); }));
function Fi(e, t, n, r) { let i = e, a = e => r(e), o = {}, s = (e, t) => n => t(e, n); return n.includes(`dot`) && (t = Li(t)), n.includes(`camel`) && (t = Ri(t)), n.includes(`capture`) && (o.capture = !0), n.includes(`window`) && (i = window), n.includes(`document`) && (i = document), n.includes(`passive`) && (o.passive = n[n.indexOf(`passive`) + 1] !== `false`), a = Ii(n, a), n.includes(`prevent`) && (a = s(a, (e, t) => { t.preventDefault(), e(t); })), n.includes(`stop`) && (a = s(a, (e, t) => { t.stopPropagation(), e(t); })), n.includes(`once`) && (a = s(a, (e, n) => { e(n), i.removeEventListener(t, a, o); })), (n.includes(`away`) || n.includes(`outside`)) && (i = document, a = s(a, (t, n) => { e.contains(n.target) || n.target.isConnected !== !1 && (e.offsetWidth < 1 && e.offsetHeight < 1 || e._x_isShown !== !1 && t(n)); })), n.includes(`self`) && (a = s(a, (t, n) => { n.target === e && t(n); })), t === `submit` && (a = s(a, (e, t) => { t.target._x_pendingModelUpdates && t.target._x_pendingModelUpdates.forEach(e => e()), e(t); })), (Vi(t) || Hi(t)) && (a = s(a, (e, t) => { Ui(t, n) || e(t); })), i.addEventListener(t, a, o), () => { i.removeEventListener(t, a, o); }; }
function Ii(e, t) { if (e.includes(`debounce`)) {
    let n = e[e.indexOf(`debounce`) + 1] || `invalid-wait`, r = zi(n.split(`ms`)[0]) ? Number(n.split(`ms`)[0]) : 250;
    t = In(t, r);
} if (e.includes(`throttle`)) {
    let n = e[e.indexOf(`throttle`) + 1] || `invalid-wait`, r = zi(n.split(`ms`)[0]) ? Number(n.split(`ms`)[0]) : 250;
    t = Ln(t, r);
} return t; }
function Li(e) { return e.replace(/-/g, `.`); }
function Ri(e) { return e.toLowerCase().replace(/-(\w)/g, (e, t) => t.toUpperCase()); }
function zi(e) { return !Array.isArray(e) && !isNaN(e); }
function Bi(e) { return [` `, `_`].includes(e) ? e : e.replace(/([a-z])([A-Z])/g, `$1-$2`).replace(/[_\s]/, `-`).toLowerCase(); }
function Vi(e) { return [`keydown`, `keyup`].includes(e); }
function Hi(e) { return [`contextmenu`, `click`, `mouse`].some(t => e.includes(t)); }
function Ui(e, t) { let n = t.filter(e => ![`window`, `document`, `prevent`, `stop`, `once`, `capture`, `self`, `away`, `outside`, `passive`, `preserve-scroll`, `blur`, `change`, `lazy`].includes(e)); if (n.includes(`debounce`)) {
    let e = n.indexOf(`debounce`);
    n.splice(e, zi((n[e + 1] || `invalid-wait`).split(`ms`)[0]) ? 2 : 1);
} if (n.includes(`throttle`)) {
    let e = n.indexOf(`throttle`);
    n.splice(e, zi((n[e + 1] || `invalid-wait`).split(`ms`)[0]) ? 2 : 1);
} if (n.length === 0 || n.length === 1 && Wi(e.key).includes(n[0]))
    return !1; let r = [`ctrl`, `shift`, `alt`, `meta`, `cmd`, `super`].filter(e => n.includes(e)); return n = n.filter(e => !r.includes(e)), !(r.length > 0 && r.filter(t => ((t === `cmd` || t === `super`) && (t = `meta`), e[`${t}Key`])).length === r.length && (Hi(e.type) || Wi(e.key).includes(n[0]))); }
function Wi(e) { if (!e)
    return []; e = Bi(e); let t = { ctrl: `control`, slash: `/`, space: ` `, spacebar: ` `, cmd: `meta`, esc: `escape`, up: `arrow-up`, down: `arrow-down`, left: `arrow-left`, right: `arrow-right`, period: `.`, comma: `,`, equal: `=`, minus: `-`, underscore: `_` }; return t[e] = e, Object.keys(t).map(n => { if (t[n] === e)
    return n; }).filter(e => e); }
Ze(`model`, (e, { modifiers: t, expression: n }, { effect: r, cleanup: i }) => { let a = e; t.includes(`parent`) && (a = At(e, t => t !== e)); let o = Pe(a, n), s; s = typeof n == `string` ? Pe(a, `${n} = __placeholder`) : typeof n == `function` && typeof n() == `string` ? Pe(a, `${n()} = __placeholder`) : () => { }; let c = () => { let e; return o(t => e = t), Yi(e) ? e.get() : e; }, l = e => { let t; o(e => t = e), Yi(t) ? t.set(e) : s(() => { }, { scope: { __placeholder: e } }); }; typeof n == `string` && e.type === `radio` && U(() => { e.hasAttribute(`name`) || e.setAttribute(`name`, n); }); let u = t.includes(`change`) || t.includes(`lazy`), d = t.includes(`blur`), f = t.includes(`enter`), p = u || d || f, m; if (on)
    m = () => { };
else if (p) {
    let n = [], r = n => l(Gi(e, t, n, c()));
    if (u && n.push(Fi(e, `change`, t, r)), d && (n.push(Fi(e, `blur`, t, r)), e.form)) {
        let t = e.form, n = () => r({ target: e });
        t._x_pendingModelUpdates ||= [], t._x_pendingModelUpdates.push(n), i(() => { t._x_pendingModelUpdates && t._x_pendingModelUpdates.splice(t._x_pendingModelUpdates.indexOf(n), 1); });
    }
    f && n.push(Fi(e, `keydown`, t, e => { e.key === `Enter` && r(e); })), m = () => n.forEach(e => e());
}
else
    m = Fi(e, e.tagName.toLowerCase() === `select` || [`checkbox`, `radio`].includes(e.type) ? `change` : `input`, t, n => { l(Gi(e, t, n, c())); }); if (t.includes(`fill`) && ([void 0, null, ``].includes(c()) || Pn(e) && Array.isArray(c()) || e.tagName.toLowerCase() === `select` && e.multiple) && l(Gi(e, t, { target: e }, c())), e._x_removeModelListeners ||= {}, e._x_removeModelListeners.default = m, i(() => e._x_removeModelListeners.default()), e.form) {
    let n = Fi(e.form, `reset`, [], n => { Bt(() => e._x_model && e._x_model.set(Gi(e, t, { target: e }, c()))); });
    i(() => n());
} e._x_model = { get() { return c(); }, set(e) { l(e); }, setWithModifiers: Ii(t, l) }, e._x_forceModelUpdate = t => { t === void 0 && typeof n == `string` && n.match(/\./) && (t = ``), U(() => { Pn(e) ? e.checked = Array.isArray(t) ? t.some(t => t == e.value) : !!t : Fn(e) ? e.checked = typeof t == `boolean` ? Dn(e.value) === t : e.value == t : gn(e, `value`, t); }); }, r(() => { let n = c(); t.includes(`unintrusive`) && document.activeElement.isSameNode(e) || e._x_forceModelUpdate(n); }); });
function Gi(e, t, n, r) { return U(() => { if (n instanceof CustomEvent && n.detail !== void 0)
    return n.detail !== null && n.detail !== void 0 ? n.detail : n.target.value; if (Pn(e))
    if (Array.isArray(r)) {
        let e = null;
        return e = t.includes(`number`) ? Ki(n.target.value) : t.includes(`boolean`) ? Dn(n.target.value) : n.target.value, n.target.checked ? r.includes(e) ? r : r.concat([e]) : r.filter(t => !qi(t, e));
    }
    else
        return n.target.checked; if (e.tagName.toLowerCase() === `select` && e.multiple)
    return t.includes(`number`) ? Array.from(n.target.selectedOptions).map(e => Ki(e.value || e.text)) : t.includes(`boolean`) ? Array.from(n.target.selectedOptions).map(e => Dn(e.value || e.text)) : Array.from(n.target.selectedOptions).map(e => e.value || e.text); {
    let i;
    return i = Fn(e) ? n.target.checked ? n.target.value : r : n.target.value, t.includes(`number`) ? Ki(i) : t.includes(`boolean`) ? Dn(i) : t.includes(`trim`) ? i.trim() : i;
} }); }
function Ki(e) { let t = e ? parseFloat(e) : null; return Ji(t) ? t : e; }
function qi(e, t) { return e == t; }
function Ji(e) { return !Array.isArray(e) && !isNaN(e); }
function Yi(e) { return typeof e == `object` && !!e && typeof e.get == `function` && typeof e.set == `function`; }
Ze(`cloak`, e => queueMicrotask(() => U(() => e.removeAttribute(Je(`cloak`))))), Ot(() => `[${Je(`init`)}]`), Ze(`init`, sn((e, { expression: t }, { evaluate: n }) => typeof t == `string` ? !!t.trim() && n(t, {}, !1) : n(t, {}, !1))), Ze(`text`, (e, { expression: t }, { effect: n, evaluateLater: r }) => { let i = r(t); n(() => { i(t => { U(() => { e.textContent = t; }); }); }); }), Ze(`html`, (e, { expression: t }, { effect: n, evaluateLater: r }) => { let i = r(t); n(() => { i(t => { U(() => { e.innerHTML = t ?? ``, e._x_ignoreSelf = !0, Ft(e), delete e._x_ignoreSelf; }); }); }); }), dt(st(`:`, ct(Je(`bind:`))));
var Xi = (e, { value: t, modifiers: n, expression: r, original: i }, { effect: a, cleanup: o }) => { if (!t) {
    let t = {};
    qn(t), Pe(e, r)(t => { Jn(e, t, i); }, { scope: t });
    return;
} if (t === `key`)
    return Zi(e, r); if (e._x_inlineBindings && e._x_inlineBindings[t] && e._x_inlineBindings[t].extract)
    return; let s = Pe(e, r); a(() => s(i => { i === void 0 && typeof r == `string` && r.match(/\./) && (i = ``), U(() => gn(e, t, i, n)); })), o(() => { e._x_undoAddedClasses && e._x_undoAddedClasses(), e._x_undoAddedStyles && e._x_undoAddedStyles(); }); };
Xi.inline = (e, { value: t, modifiers: n, expression: r }) => { t && (e._x_inlineBindings ||= {}, e._x_inlineBindings[t] = { expression: r, extract: !1 }); }, Ze(`bind`, Xi);
function Zi(e, t) { e._x_keyExpression = t; }
Dt(() => `[${Je(`data`)}]`), Ze(`data`, (e, { expression: t }, { cleanup: n }) => { if (Qi(e))
    return; t = t === `` ? `{}` : t; let r = {}; we(r, e); let i = {}; Zn(i, r); let a = Ne(e, t, { scope: i }); (a === void 0 || a === !0) && (a = {}), we(a, e); let o = w(a); ve(o); let s = fe(e, o); o.init && Ne(e, o.init), n(() => { o.destroy && Ne(e, o.destroy), s(); }); }), un((e, t) => { e._x_dataStack && (t._x_dataStack = e._x_dataStack, t.setAttribute(`data-has-alpine-state`, !0)); });
function Qi(e) { return on ? fn ? !0 : e.hasAttribute(`data-has-alpine-state`) : !1; }
Ze(`show`, (e, { modifiers: t, expression: n }, { effect: r }) => { let i = Pe(e, n); e._x_doHide ||= () => { U(() => { e.style.setProperty(`display`, `none`, t.includes(`important`) ? `important` : void 0); }); }, e._x_doShow ||= () => { U(() => { e.style.length === 1 && e.style.display === `none` ? e.removeAttribute(`style`) : e.style.removeProperty(`display`); }); }; let a = () => { e._x_doHide(), e._x_isShown = !1; }, o = () => { e._x_doShow(), e._x_isShown = !0; }, s = () => setTimeout(o), c = Zt(e => e ? o() : a(), t => { typeof e._x_toggleAndCascadeWithTransitions == `function` ? e._x_toggleAndCascadeWithTransitions(e, t, o, a) : t ? s() : a(); }), l, u = !0; r(() => i(e => { !u && e === l || (t.includes(`immediate`) && (e ? s() : a()), c(e), l = e, u = !1); })); }), Ze(`for`, (e, { expression: t }, { effect: n, cleanup: r }) => { let i = ta(t), a = Pe(e, i.items), o = Pe(e, e._x_keyExpression || `index`); e._x_lookup = new Map, n(() => ea(e, i, a, o)), r(() => { e._x_lookup.forEach(e => U(() => { It(e), e.remove(); })), delete e._x_lookup; }); });
function $i(e) { return t => { Object.entries(t).forEach(([t, n]) => { e[t] = n; }); }; }
function ea(e, t, n, r) { n(n => { ra(n) && (n = Array.from({ length: n }, (e, t) => t + 1)), n ??= [], n instanceof Set && (n = Array.from(n)), n instanceof Map && (n = Array.from(n)); let i = e._x_lookup, a = new Map; e._x_lookup = a; let o = ia(n), s = Object.entries(n).map(([s, c]) => { o || (s = parseInt(s)); let l = na(t, c, s, n), u; return r(t => { typeof t == `object` && bt(`x-for key cannot be an object, it must be a string or an integer`, e), i.has(t) && (a.set(t, i.get(t)), i.delete(t)), u = t; }, { scope: { index: s, ...l } }), [u, l]; }); U(() => { i.forEach(e => { It(e), e.remove(); }); let t = new Set, n = e; s.forEach(([r, i]) => { if (a.has(r)) {
    let e = a.get(r);
    e._x_refreshXForScope(i), n.nextElementSibling !== e && (n.nextElementSibling && e.replaceWith(n.nextElementSibling), n.after(e)), n = e, e._x_currentIfEl && (e.nextElementSibling !== e._x_currentIfEl && n.after(e._x_currentIfEl), n = e._x_currentIfEl);
    return;
} e.content.children.length > 1 && bt(`x-for templates require a single root element, additional elements will be ignored.`, e); let o = document.importNode(e.content, !0).firstElementChild, s = w(i); fe(o, s, e), o._x_refreshXForScope = $i(s), a.set(r, o), t.add(o), n.after(o), n = o; }), sn(() => t.forEach(e => Ft(e)))(); }); }); }
function ta(e) { let t = /,([^,\}\]]*)(?:,([^,\}\]]*))?$/, n = /^\s*\(|\)\s*$/g, r = e.match(/([\s\S]*?)\s+(?:in|of)\s+([\s\S]*)/); if (!r)
    return; let i = {}; i.items = r[2].trim(); let a = r[1].replace(n, ``).trim(), o = a.match(t); return o ? (i.item = a.replace(t, ``).trim(), i.index = o[1].trim(), o[2] && (i.collection = o[2].trim())) : i.item = a, i; }
function na(e, t, n, r) { let i = {}; return /^\[.*\]$/.test(e.item) && Array.isArray(t) ? e.item.replace(`[`, ``).replace(`]`, ``).split(`,`).map(e => e.trim()).forEach((e, n) => { i[e] = t[n]; }) : /^\{.*\}$/.test(e.item) && !Array.isArray(t) && typeof t == `object` ? e.item.replace(`{`, ``).replace(`}`, ``).split(`,`).map(e => e.trim()).forEach(e => { i[e] = t[e]; }) : i[e.item] = t, e.index && (i[e.index] = n), e.collection && (i[e.collection] = r), i; }
function ra(e) { return typeof e != `object` && !isNaN(e); }
function ia(e) { return typeof e == `object` && !Array.isArray(e); }
function aa() { }
aa.inline = (e, { expression: t }, { cleanup: n }) => { let r = kt(e); r && (r._x_refs ||= {}, r._x_refs[t] = e, n(() => delete r._x_refs[t])); }, Ze(`ref`, aa), Ze(`if`, (e, { expression: t }, { effect: n, cleanup: r }) => { e.tagName.toLowerCase() !== `template` && bt(`x-if can only be used on a <template> tag`, e); let i = Pe(e, t), a = () => { if (e._x_currentIfEl)
    return e._x_currentIfEl; let t = e.content.cloneNode(!0).firstElementChild; return fe(t, {}, e), U(() => { e.after(t), sn(() => Ft(t))(); }), e._x_currentIfEl = t, e._x_undoIf = () => { U(() => { It(t), t.remove(); }), delete e._x_currentIfEl; }, t; }, o = () => { e._x_undoIf && (e._x_undoIf(), delete e._x_undoIf); }; n(() => i(e => { e ? a() : o(); })), r(() => e._x_undoIf && e._x_undoIf()); }), Ze(`id`, (e, { expression: t }, { evaluate: n }) => { n(t).forEach(t => ki(e, t)); }), un((e, t) => { e._x_ids && (t._x_ids = e._x_ids); }), dt(st(`@`, ct(Je(`on:`)))), Ze(`on`, sn((e, { value: t, modifiers: n, expression: r }, { cleanup: i }) => { let a = r ? Pe(e, r) : () => { }; e.tagName.toLowerCase() === `template` && (e._x_forwardEvents ||= [], e._x_forwardEvents.includes(t) || e._x_forwardEvents.push(t)); let o = Fi(e, t, n, e => { a(() => { }, { scope: { $event: e }, params: [e] }); }); i(() => o()); })), oa(`Collapse`, `collapse`, `collapse`), oa(`Intersect`, `intersect`, `intersect`), oa(`Focus`, `trap`, `focus`), oa(`Mask`, `mask`, `mask`);
function oa(e, t, n) { Ze(t, r => bt(`You can't use [x-${t}] without first installing the "${e}" plugin here: https://alpinejs.dev/plugins/${n}`, r)); }
Qn.setEvaluator(ze), Qn.setRawEvaluator(Ke), Qn.setReactivityEngine({ reactive: xi, effect: br, release: xr, raw: G });
var sa = Qn;
