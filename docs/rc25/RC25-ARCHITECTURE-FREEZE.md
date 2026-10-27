# Signature Lab v0.20.12-rc25 — scoped architecture freeze

## Requirement and acceptance
Repair the existing "Enlarge QR" button on the disposable test-wallet SeedQR. The existing button must open a centered, genuinely enlarged QR at supported viewport sizes; the QR and "Reduce QR" button widths must match; Reduce, Escape and clicking outside must collapse it; QR payload/rendered canvas must remain unchanged. This is a presentation-only repair; nothing may broadcast, sign, import or alter test-wallet state because of this button.

## Architecture and authority
Single existing Alpine app controller in `src/20-application.js` owns `seedQrExpanded` and the SeedQR canvas. Single `src/page.html` button retains its Alpine handler, `aria-expanded`, `aria-controls`, and `click.outside`/Escape behavior. `src/style.css` owns presentation. Source lock and `build.py` own source-to-standalone HTML. No secondary modal controller, signing path, QR encoder, wallet generator, session ledger, or state store is introduced.

## Trust boundaries and lifecycle
No new permissions, network calls, file storage, or authority. The displayed QR is disposable test-wallet material and stays in the existing tab memory. The enlarged view is transient UI state; clicking Reduce/Escape/outside collapses it. An interruption or reload retains existing RC24 reload behavior. Rollback is the archived unchanged RC24 handoff. This preview does not change installation, recovery, upgrade, or authoritative runtime application state.

## Retired conflict
Removed the newer `position:relative!important` for `.premium-test-step .seed-scan.seed-expanded`. Existing collapsed-only width rules are explicitly scoped with `:not(.seed-expanded)`. The original fixed modal rule is the sole enlargement geometry authority. Its action width is now intentionally the same as the QR width.

## Scope and limitations
Changed: `src/style.css`, `release.json`, `source-lock.json`; added RC25-specific UI test and qualification documentation. Zero changes to existing application JavaScript, source HTML, vendor code or Bitcoin operations. Device scans, full historical suite, native file-origin integration, and real hardware acceptance are separate from the scoped UI qualification.
