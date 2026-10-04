# Header and QR alignment: architecture frozen

Scope: v0.18.2-rc1, based only on the supplied v0.18.1-rc1 HTML and source archive.
Baseline hashes: HTML fffa9b9c4357918fb3d79c3b041a411feb274c018260f7c036fdf3a86ee38448;
ZIP 39354907c4e325be9597af977d7e1a1412f49435d99b21528d5b8e3e13d50647.
This is a presentation-only stabilization pass. No new runtime feature or dependency.

## Requirements and acceptance
1. Rebalance existing wheel/wordmark: wheel approximately 10-15 percent larger, wordmark
   approximately 5-8 percent smaller at corresponding desktop/mobile breakpoints. Native
   system-ui family and existing embedded logo bytes remain unchanged.
2. Version stays a quiet, legible global utility on the right. Retain accessible release
   status/limitations link. Help becomes one question-mark control in that header, not a
   fourth workspace tab. Accessible name Help, title, visible keyboard focus, 44px target.
3. QR and its existing fingerprint/reminder/action group share exact inner left/right
   alignment in one calm right-hand wallet column. Keep one fingerprint, one QR canvas,
   one acknowledgement and one enlargement control. The surrounding wallet card is a
   single visual group. At narrow available widths actions stack; do not shrink labels
   to force a horizontal row. Enlarge/Reduce never acknowledges a wallet.
4. Both 12/24 words, normal/enlarged QR, 320/360/390/438/768/1024/1440px and enlarged/space-
   adjusted text must reflow without clipped text, overlapping actions or changed QR pixels.
5. Related transaction QR download/copy controls use the same alignment and clear action
   hierarchy. Preserve all-output review, warnings, reports and historical findings.
6. Test/Advanced/Session positions and authoritative state must remain stable on switching;
   Help and its return behavior continue via the single existing navigation implementation.
7. Dark Skippy remains the existing isolated one-click recorded example. No live-wallet
   replacement, seed copying, counter changes or second demonstration mode.
8. Complete retained software suite plus new layout/preservation tests; compare every ordered
   runtime JS byte with baseline. No pass count inferred from prior runs. New golden layout
   assertions may retire superseded full-width-card geometry only with explicit replacement.

## Architecture and module boundaries
Only src/page.html and src/style.css may change application presentation. build.py remains
one authoritative source assembler. Existing Fv, prepared test, immutable result, journal,
reference self-check, QR session, camera owner and navigation code remain authoritative.
All 29 ordered runtime JavaScript files must remain byte-identical to v0.18.1. Build source
locks/release metadata, tests and documentation may change for this candidate.

## Trusted core / optional modules
No trusted-core calculation is edited. Help and the isolated example remain optional UI
surfaces, not alternate verification logic. Their absence must not bypass startup checks or
mutate wallet/test state. No new controllers, ledgers, caches, retries or renderer libraries.

## Privilege, ownership and state
Retain browser-only privileges, current CSP, no networking/font download, no storage or
background camera retention. The operator owns exported evidence; no upload or publication
is performed. UI position is not an additional state source. The new release identity is
unique. The previous candidate stays immutable and is not relabelled or overwritten.

## Interruption / resume / rollback / recovery / upgrade
Retain terminal scan/failure behavior and explicit restart. Reload creates a new tab lifetime;
no persistent secret-state resume exists. Save current evidence before changing versions.
Rollback means open a retained prior file in a fresh context, not undo a device signature.
No OS installation, bootloader, Bitcoin/Fulcrum services, storage adoption or recovery-boot
exists in this standalone HTML app; those operations are not applicable. Test applicable
fresh-context adoption/upgrade/rollback, page restoration and idempotence using retained tests.

## Retired presentation
Large wordmark/small-wheel imbalance; word Help link; detached full-width wallet confirmation
footer whose action edges do not follow the QR. No underlying information/action is retired.
Existing full-width-card geometry assertions are replaced with shared QR/card inner-edge
assertions; actual runtime tests still use exact current HTML, never historical projections.

## Qualification and limitations
Development corrections occur only before freeze. At acceptance freeze HTML, source ZIP and
manifest hashes; extract fresh, execute all jobs without retries. Any candidate blocker means
new identity and restarted qualification. Record unavailable tools separately, never as passes.
Physical signer/optical/native OS and real permission acceptance, dependency authenticity,
publisher signing, outside review and the unresolved Foundation findings remain open gates.
We make no claim that these presentation changes increase malware detection probability.

## References for layout checks (not conformance certification)
W3C WCAG 2.2 Understanding: Target Size Enhanced (44 CSS px), Reflow (320 CSS px), Label in
Name. Used as engineering criteria only; not a full WCAG assessment or native OS scaling test.
https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html
https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
https://www.w3.org/WAI/WCAG22/Understanding/label-in-name.html
