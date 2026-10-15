# v0.20.11 development architecture and acceptance contract

## Requirements and acceptance
- Repair every actionable finding in the 13 October v0.20.9 audit without weakening security or accessibility checks.
- Preserve the exact trusted cryptographic, signing, PSBT, QR, camera, startup, coordinator, and journal module bytes. The only runtime changes allowed for v0.20.11 are CSS reflow, workspace-button target height, and high-contrast selection, plus development version metadata.
- Preserve a single standalone offline HTML deliverable, an authoritative `build.py`, `source-lock.json`, `EXPECTED-OUTPUT.json`, and `qualify.py` runner. No duplicate verifier/controller/state ledger or runtime network dependency.
- Fix historical static provenance contracts separately from current browser/behavior contracts. Historical source reconstruction cannot count as current app behavior acceptance.
- Preserve negative tamper tests, current wallet warnings, no-camera-on-open rule, QR pixels, state immutability, and accessible Help/focus/keyboard navigation.

## Trusted core and optional boundaries
- Trusted core: unmodified cryptography and 29 build-time runtime units other than CSS. Retain one authoritative signer/PSBT verification path, journal, session coordinator, and user-visible result model.
- Presentation: `src/style.css` and pre-existing HTML in the current version. No optional module may change signed artifact checks or mutate the trusted result.
- Qualification: `qualify.py` is the only canonical stage/job plan, with version-aware current acceptance and guarded historical provenance tests.

## Authority, privilege and state
- Session journal, coordinator and current UI state remain authoritative. No persistent business state added. Release files and SHA-256 identifies immutable artifacts; qualification emits separate immutable evidence files.
- Publisher controls signing keys and distribution. Operator must approve deployment. Automated testing has no authority to certify hardware, sign a publisher release or move the public release pointer.

## Failure/recovery/upgrade behavior
- Invalid/unsupported responses or captured metadata remain review/terminal findings in the session. Recompute is guarded by the existing retire latch and capture stops during Finish testing. Browser/OS memory wipe is never claimed.
- Build output and source archives refuse overwrite. A failed, interrupted or timed-out qualification run is disqualified; a modified test harness or runtime requires a freshly packaged candidate and fresh full run.
- Recovery, upgrade and rollback of the website/release pointer remain externally gated; never mutate the previous signed release.

## Explicitly retired test expectations
- Source equality to v0.20.3 or exact historical release-copy instead of preserved provenance plus current semantics.
- Exact desktop/mobile coordinates for previously redesigned Test-only progress chrome, old intro color, long Results title and right-edge mobile controls.
- Exponential "200%" text inflation from reading already-mutated ancestor computed styles. A genuine doubled-text test snapshots sizes before changing styles.

## Acceptance gates
1. Static syntax, source locks, independent crypto/vendor preservation and negative tamper tests.
2. Unit, contract, integration, camera faults, QR, and PSBT/evidence replay.
3. Current browser, historical accessibility, forced-colors, keyboard, enlarged text, dialogs, session and failure/recovery tests.
4. File-system fault injection, clean extraction, deterministic rebuild, idempotent second run, no-replace behavior.
5. One uninterrupted complete `qualify.py --stage all` on exact frozen bytes and source archive, then external native-browser and hardware acceptance.
6. Independently authenticated publisher signature, upstream vendor provenance and third-party security review before full public-production claim.
