# Signature Lab RC16 — frozen scoped architecture and acceptance

## Scope and acceptance
The exact request is to build the signed-transaction page and empty results page, retaining all functionality. The signing page must be labeled "QR format" (not "Sign with your device"), display the same two BC-UR/BBQr modes, preserve the frame caption, Save PSBT, Copy PSBT, output disclosure, transaction disclosure, fresh-transaction control, and signed-response camera/file/paste flow. At desktop width, QR format and Save/Copy rows must share horizontal edges and the transaction/QR cards end on the same baseline. Step 3 must position "Your result" by the numbered heading, with a compact no-result card and a working return button. Dark/light at 390, 768 and 1440px must not overflow. Test failures are blockers for public release.

## Module boundaries and authoritative state
`src/page.html` owns semantic layout, `src/style.css` owns display geometry, `release.json` owns release version and signing status. The single `src/20-application.js` Alpine controller remains the sole owner of wallet/session, transaction, QR selection, importing, signature verification and step navigation. `build.py` is the one locked assembly operation. No duplicate controller, data ledger, retry engine, privileged service or network source has been introduced. 29 application/vendor units in sources.json are preserved byte-identically from RC15.

## Privilege, lifecycle and recovery
The application remains a local/offline, nonbroadcasting, disposable-wallet test tool. No server installation, escalation, background service, reboot, persistent secret state, wallet adoption, firmware change or node boot flow is introduced. A reload begins another test wallet; the existing user appearance preference may persist. Browser/operator rollback is opening the immutable RC15 HTML or handoff. No auto retries following signature or intake failure. Historical qualification scripts remain present as unresolved compatibility gates; nothing is retired merely to make a test pass.

## Acceptance and freeze
Syntax, locks, isolated faults, desktop/mobile layout, feature-preservation checks and deterministic output must pass before archive freeze. Hardware signer, original browser-file origin and full legacy 139-job qualification require separate acceptance and are not represented by this UI scope. Freeze SHA-256 of a single final candidate archive; never patch it after acceptance begins. Any blocker to full public release leaves the candidate development-preview only.
