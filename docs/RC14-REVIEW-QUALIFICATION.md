# RC14 development preview: qualified scope and open gates

## Positive evidence
- Offline single-HTML build with locked sources, no unresolved tokens, Python compile and CSS parser checks.
- New `tests/rc14_review_browser.py`: 6/6 Chromium document contexts (390, 768, 1440px in light/dark), including landing/setup/help, drawers, warning scoping, contrast and positive state semantics, no page exceptions, no attempted HTTP(S) requests, no overflow, visible header label, privacy and external website link.
- Legacy `tests/rc13_ui_contract.py`: 6/6 exercised against the changed copy (scoped DOM-context, not a release-wide pass).
- Additional targeted prequalification: BBQR jobs 1-15, 16-40, 41-62 passed (62 checks). Regression 1-20 and 21-40 passed (40 checks). Camera unit job passed. Session 1-29 and 30-33 passed (33 checks).
- Application coordinator, signer crypto/reference, camera, vendor JS and session source units are byte-identical to RC13. `build.py` changes only to expose validated release status in the assembled standalone HTML.

## Failures and incompletes (do not reinterpret as passes)
- `current-release-contract` failed 5/10 checks because it is hardcoded to the v0.20.11-rc3 expected digest, status and older trusted-source hashes, and an older literal safety sentence.
- `static` historical-projection job failed with a hardcoded v0.20.11 identity/provenance boundary and layout changes.
- Selected broader regression invocation timed out before all jobs completed. Incomplete jobs are NOT passed: regression 41-54, sessions 34-38, browser integration completion and other queued jobs.
- Full canonical 139-job campaign NOT completed, including porting of 83 historic UI/copy/browser jobs reported by independent reviewer. This is a public-release blocker. The legacy checks remain present rather than being deleted or disabled.
- Chromium `file://` navigation returned `net::ERR_BLOCKED_BY_ADMINISTRATOR`. Native offline-file and deployed HTTPS-origin tests are not passed. No real signer QR/camera run, power-loss/disk fault run, independent signer attestations, publisher signature verification or hardware acceptance occurred.

Status: **development UI preview, public release blocked**. All source/final-archive cryptographic identity and extraction checks must be verified separately at packaging time. Passing scoped presentation tests is not proof of firmware security.
