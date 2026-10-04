# Scoped review — no outside audit or firmware certification

Inspected exact v0.18.4 handoff, coordinator, journal, reset/navigation/demo, result/history
export boundaries, page bindings and relevant CSS. Verified source hash/manifest and baseline
rebuild. Recorded two physical-window-sized Chromium demo observations; no real hardware.

Critical distinction: hiding ended status is presentation only. TbwSessionJournal.rollback
still records end; halted reason/history and current immutable result are not cleared. Its
report remains exportable in Session. Existing locked/receive/advance decisions are unchanged.

New wallet confirmation wraps, rather than reimplements, randomizeAll. Intent is private,
not stored/exported, compared to wallet/transaction/epoch/result/session/import revisions and
consumed before applying. Native modal's safe initial action is Keep this wallet. Cancel,
missing support, stale close, late input and page lifecycle tested. The two visible word-length
controls use that same request boundary. Direct internal low-level reset contracts remain;
this is user-error protection, not a defence against injected JavaScript or a hostile browser.

Export finding: freezing an Alpine proxy-backed array made JSON serialization fail. The
existing public-history projection is detached before freeze. This keeps its JSON schema and
field selection intact and does not freeze UI backing objects. Current-result evidence remains
owned by the unchanged evidence module. A successful browser download event is not a guarantee
that a user retains or later authenticates the file. The UI tells the user to save first and
never claims saving happened automatically.

The demo executes Up/runDemonstration over the published signed transaction, not firmware or
a signer. Cached success is a recorded example result; it is not added to session counts. Its
source/witness/reference evidence is inspectable without substituting its seed into the test.
Complete demo invisibility reported by the user was not reproduced. Current native modal
behavior was checked against WHATWG HTML dialog semantics, but real Safari/Firefox/phone
acceptance remains external: https://html.spec.whatwg.org/multipage/interactive-elements.html#the-dialog-element

No new dependency, outgoing request, persistence, camera acquisition/retry or manufacturer
exception. Publisher signing, inherited dependency authentication, independent review/rebuild,
actual optical/hardware and user comprehension remain unclosed. A matching result cannot prove
future firmware behavior or rule out all hidden-information channels. The startup gate is not
publisher authentication. Existing Foundation orange findings are not diagnosed by this work.
