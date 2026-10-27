# RC23 architecture freeze — 21 October 2026

## Goal and acceptance criteria
Replace the inconsistent header status/button pair with one authoritative passive status display and a separate, explicit navigation action. Standardize light-mode informational text/link accents to blue. Preserve all existing signing, transfer, result, wallet and session functionality; preserve dark mode and orange numbered steps/primary actions. At widths 390, 768, 1440 test the Test→Session→Test navigation, light/dark status appearance, Help/Advanced/expanded signing palette, no horizontal overflow, no JS errors.

## Trusted core and module boundaries
The existing Alpine application coordinator and state model remain authoritative for `workspaceView`, `acknowledged`, `sessionSummary`, `recordedReviewCount`, `recordedIncompleteCount`, `recordedOperationFailureCount`. No second state ledger or status controller is created. The single status is a presentational projection in `src/page.html`; the visual contract belongs to `src/style.css` only. All 29 application/vendor JavaScript source units remain byte-identical to RC22. Help, Advanced, device notes and diagnostics remain optional; none can mutate core generation, signing, network, security, or recovery paths.

## Privileges, ownership, and authoritative state
The application remains self-contained and local-first, with no new privileges, network requirements or account connections. Only the coordinator owns session state. Navigation invokes the existing `openWorkspace('session')` action; on the Session page the navigation button is hidden, leaving the same passive status. No external side effects or persistence model changes.

## Reboot/resume, rollback, recovery and upgrade
Browser reload still starts a fresh disposable wallet, according to existing RC22 semantics. No resume/rollback/retry engine is added. Recovery is to reopen RC22 (unchanged and separately frozen) if RC23 is rejected. RC23 does not alter any on-disk or persisted data schema; it does not promise to erase browser or OS memory. New package/version is isolated, never overwrites the RC22 archive.

## Retired UI elements
The old context-dependent clickable `tracker-status` and duplicate context-dependent text content are retired from page markup. The new single `tracker-status-readonly` is informational everywhere and separate `tracker-session-link` provides navigation. Legacy presentation selectors may remain inert for source compatibility; they do not own runtime state or event handlers.

## Qualification rules
Build only from an explicit source lock, reject modified inputs, freeze after tests and record archive SHA-256, then verify clean extraction and deterministic repacking. This is a development preview until full historical tests, native file-origin, signed-result and physical-device acceptance are completed. This qualification does not authorize a production/public release.
