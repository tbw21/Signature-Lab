# Navigation and handoff — architecture frozen
Recorded 2026-09-19T07:40:22.401806+00:00, before implementation. Candidate: 0.18.4-rc1.

## Recovery and requirements
The last recoverable full source and HTML are v0.18.2-rc1. Their SHA-256 values are
28f2c90a3fc9331ed7d5db420f2e8d56aecb052d089aaefed62f0946a3c16a9e (HTML) and
3f915f9d1bbdf7ecb18789e0be5e165b11cf38e99086d8b11b0f61609a660242 (source ZIP).
All 188 source manifest entries were checked on extraction.
Prior navigation-work checkpoints mention v0.18.3-rc1 and rc2; only screenshots,
not their executable/source/test archives, were recovered in this continuation.
Those checkpoints do not supply verifiable bytes or acceptance results. Do not reuse
those version names, invent their hashes, or carry forward their reported tests.
This is a fresh reconstruction of the approved changes, not recovery of that archive.

## Acceptance criteria
N1. Keep native font, two-level compact brand, right-side version and global Help.
N2. Remove only the wallet QR group's extra border/background; preserve white QR
quiet area, one canvas/fingerprint, and shared QR/action edges. No shrinking/cropping.
N3. Put 'Changing length creates a new test wallet.' immediately beneath the 12/24
selector, semantically linked. Keep no-passphrase and disposable-wallet instructions.
N4. Use 'Wallet confirmed', 'Run Dark Skippy demo', 'Import the signed response.'
and 'Scan, import or paste the signed response from your signer.' Preserve import formats.
N5. Left step navigation uses non-scrolling focus like workspace navigation. A primary
wallet acknowledgement may intentionally reveal the transaction review after a long
mobile wallet page. No timer/scroll retry controller. Browser height clamping is not
an application-initiated jump. Stale focus must not override a later action.
N6. Results entry opens unfinished intake without changing results/evidence/paste
content or errors; completed results stay read-only; guided holds stay locked.
N7. Navigation never starts/reacquires camera. Selecting current Results while scanning
must not stop its live stream. Leaving capture stops it without clearing failed state.
N8. The optional one-click recorded demo stays isolated; no seed loading, no forged
hardware result, no journal reset or counts added. The changed label describes existing work.
N9. Run all applicable retained cases and new source, contract/fault and browser checks.
Update only assertions directly superseded by approved copy/geometry/navigation.
Document exact reversals for historical preservation tests; runtime tests use real candidate.
N10. Deliver a single handoff ZIP with one canonical versioned HTML, exact source ZIP,
qualification/results, checksum manifest, evidence and operator instructions. No publication,
publisher signing, personal keys, installation or Library mutation is authorized here.

## Architecture and boundaries
Fv remains the sole application coordinator; one prepared test, immutable result, existing
session journal, camera lifecycle and reference-self-check are authoritative. Navigation
uses the existing focus generation and workspace request/epoch guards. No new controller,
verifier, ledger, signing method, firmware profile, font, runtime dependency, network access,
secret persistence, camera keepalive, retry engine, or metadata exception.
Trusted core: transaction construction, verification, reference methods/gate and imports.
Optional: Help/demo/presentation, which cannot mutate core semantics or create device evidence.
Allowed runtime change: narrowly declared navigation/focus dispatch in src/20-application.js.
The other runtime sources must remain byte-identical to the baseline.

## Privilege/ownership and authoritative state
Application retains exact offline CSP and existing browser permissions. No elevation or
new external access. Operator initiates camera and downloads; publisher keys stay with TBW.
Working tree is editable only before freeze. Existing release artifacts remain untouched.
The only active candidate for this handoff is 0.18.4-rc1; no automatic latest pointer inside app.

## Interruption, recovery, upgrades and rollback
Scan/verification failures preserve terminal state and require explicit operator recovery.
Changing view cannot reset a failed result or silently retry signing/capture. Reload starts
fresh and drops secrets/session as before. Save evidence before closing. New version uses
a fresh disposable wallet; no secret-data adoption/migration. Returning to an older HTML does
not undo a physical device operation. Test page restoration and clean lifetime behavior.
No OS installation, bootloader, Bitcoin/Fulcrum, service ownership or recovery boot applies.

## Retired behavior
Decorative inner wallet square, detached word-length warning, awkward button/result labels,
forced scrolling by left navigation, hidden unfinished intake on re-entry, and current-step
navigation canceling live capture. Do not retire metadata checks or isolate warnings out of sight.

## Qualification and disqualification
Complete development preflight before freeze. Freeze HTML+source ZIP with hashes and fresh
extraction before acceptance. A blocker disqualifies that candidate: no patches during a run.
A new candidate/restart is required for source changes. Bounded test jobs, no auto retries.
Record passed/failed/unavailable/timeout/skipped independently. Physical signers/optical camera,
macOS/Windows/iOS native fonts, authenticated publisher/dependencies, external review and
Foundation findings remain explicit external gates. No claim of 100% detection or all-browser
acceptance. Any historical pass totals are historical only.
