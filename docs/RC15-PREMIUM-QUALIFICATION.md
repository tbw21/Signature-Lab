# RC15 premium UI development qualification

## Source / implementation
- Changed executable inputs: `src/page.html`, `src/style.css`, `release.json`, and `source-lock.json`; `build.py` remained unchanged.
- Test addition: `tests/rc15_premium_browser.py`. Historical tests retained.
- All 30 underlying source and vendor JavaScript files remain byte-for-byte identical to RC14.
- No product/device illustrations are embedded in the landing screen. The one proprietary The Bitcoin Way brand header icon remains unchanged.

## Scope-passed checks
- Chromium standalone-document responsive interaction: 6/6 cases at 390, 768, 1440 px in dark and light. Landing, safety warning, responsive layout, 12/24-word generation, original SeedQR canvas, eight-character fingerprint, explicit operator confirmation, BC-UR/BBQr selection, PSBT export/copy presence, signed response intake, Help/Settings/Advanced/Session access. No observed JS error, HTTP(S) request or horizontal overflow; SeedQR and Enlarge button widths equal within tolerance.
- The independent layout probe also passed 6/6 browser combinations.
- Node BBQr contracts: 62/62. Audit/reliability/evidence: 54/54. Session journal: 38/38. Reference known-answer self-test contract: 24/24. No failures within these suites.
- Static and synthetic fault checks: 10/10; CSS parse, all source JS syntax, assembled JS syntax, CSP, single-inline-module, source lock, tamper rejection, false publisher status rejection, missing-input rejection, output overwrite refusal.

## Failures / blocked or not-run
- Historical `tests/static.cjs` returns nonzero. Its historic projection pins v0.20.11-rc3 and previous page/style layouts; it rejects changed current presentation. This is a **qualification blocker**, not a passed test or an authorization to retire that suite.
- Full canonical 139-job campaign and the legacy browser/copy suite migration were not performed to completion. Historical coverage cannot be inferred from the scoped tests above.
- Chromium direct `file://` or `http://127.0.0.1` navigation is restricted with `ERR_BLOCKED_BY_ADMINISTRATOR` in this environment; the scoped browser suite uses a document context. This cannot establish actual native-origin behavior.
- Real physical-device signing/camera, powered hardware, actual disk/read-only/power-loss simulation, independently reproduced publisher signing, upgrade/reboot/recovery and third-party audits were not run. Install/boot/upgrade are not applicable to this static HTML, but are not claimed as checked.

## Grade
`SCOPED IMPLEMENTATION PASS — DEVELOPMENT UI PREVIEW — PUBLIC RELEASE BLOCKED`. No public release or firmware safety certification is implied. Scope checks are not a substitute for the historical 139-job test repair or hardware/origin qualification.
