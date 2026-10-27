# RC24 architecture and acceptance freeze

## Requirements / acceptance
Fix the Advanced page's uneven nested card headings/body insets; align Guided, Transaction settings and Device notes cards. Ensure expanded output/transaction technical text remains inside its review card at narrow and desktop widths. Correct light-theme output/input editor row fill vs text contrast. Preserve every optional control and all business logic.

## Architecture, trust boundary, state and ownership
The RC23 Alpine controller remains the single owner of workspace, wallet, transaction and session state. Only CSS in `src/style.css` plus `release.json` metadata changed. No application/vendor JavaScript modified; no new controllers, state stores, persistence, network calls or privileges. The trusted signer/verifier/wallet/PSBT/QR/camera/data systems are untouched. Optional Advanced and UI presentation remain outside the trusted core and cannot block core signing.

## Recovery, upgrade and rollback
Existing RC23 browser reload semantics remain (fresh disposable wallet); no new resume, retry, cleanup or recovery logic. No migration. Frozen RC23 remains the fallback release; RC24 never overwrites RC23 files. This is a new file build and not an update to an active production release pointer.

## Explicitly retired behavior
Removed no functional feature. Replaced conflicting dark-theme presentation of light-mode Input/Output rows. Older style rules remain upstream in the same stylesheet; the final scoped RC24 rules define these components for the selected theme.

## Contracts
No new inspect/plan/apply/status/rollback controller exists for these UI rules. Build accepts a locked source and a fresh output filename, rejects tampering and refuses overwrites; verify hashes, source extraction and inspect rendered DOM; rollback means reopening RC23.

## Public release blockers
The development preview cannot be called end-to-end validated until the historical campaign, file-origin, real signed-result, physical device, accessibility and associated failure/recovery testing are separately completed. The visual tests are not a hardware/software-security audit.
