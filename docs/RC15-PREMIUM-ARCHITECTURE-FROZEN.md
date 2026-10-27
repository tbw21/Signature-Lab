# RC15 premium application UI — frozen architecture and scope

## Requirements / acceptance
The user-approved wallet-setup screen is the presentation reference. Refine the welcome screen by eliminating device/product imagery and redundant instruction text. Explain the tool in plain language and keep the critical disposable-wallet and no-broadcast cautions. Preserve every existing signing/camera/verification/BBQr/BC-UR/PSBT/file/import, fingerprint, setup reset, Light/Dark, Session, Advanced, Help and Settings capability. Use the same dark navy/orange design language across actual pages and retain a usable Light Mode. The SeedQR and Enlarge control must match widths at 390, 768 and 1440px.

## Authoritative boundaries
`src/page.html` owns copy and DOM presentation; `src/style.css` owns appearance. The single existing `src/20-application.js` controller owns mutable operations, navigation and theme. `src/13-qr-session.js`, `src/15-qr-render.js`, `src/11-bbqr.js`, `src/17-camera.js`, `src/session-journal.js`, the source-level transaction/verifier code, and all `vendor/*.js` stay byte-identical to RC14. No duplicate wallet, request, retry, scan, verifier or journal controller is introduced. All existing Alpine event handlers remain the authoritative operations; the Step 1 markup reconnects to the same named handlers, QR canvas/ref, fingerprint state and confirmation. The moved QR canvas does not change its QR payload.

`release.json` is the single authoritative release-status and version declaration, incorporated by the source-locked `build.py`; `source-lock.json` pins all build inputs. `EXPECTED-OUTPUT.json` records the exact standalone HTML output identity. The handoff ZIP and embedded source ZIP are not upgrade tools.

## Trust / privileges / private state
Offline, no added network access or privileged system component. The existing CSP continues to forbid connection attempts. The generated disposable seed and session live only in tab memory; existing appearance preference handling may store light/dark. Never import an existing funded wallet. The fingerprint is a BIP32 comparison aid and can only be confirmed explicitly by the operator; it is not device attestation. Only supported expected signatures/transaction data are checked. No signing or button press is performed on the physical device.

## Lifecycle / retirement / recovery
No install, reboot, recovery-boot or data upgrade lifecycle applies to a single standalone HTML file. Reload creates another disposable wallet; a verified original result is not restored by the tool. Rollback is explicit: reopen the unchanged frozen RC14 HTML/ZIP after operator selection. No automatic retry of failed verification, camera or export paths. No feature/module was retired. The redundant landing graphics and nested setup instructions are presentation-only removals; the functional controls are retained.

## Acceptance gate
Scoped browser/static/core contracts and fault tests are prerequisites to packaging. The 139-job older qualification campaign contains literal historic v0.20.11-rc3 source/provenance/layout assertions and remains unported; do not delete, loosen or relabel those failures. Physical QR signers/cameras, publisher authentication and native file/HTTPS origin require separate acceptance. Until all qualifying gates pass, grade is `DEVELOPMENT UI PREVIEW — PUBLIC RELEASE BLOCKED`.
