# RC25 qualification — development UI preview; public release blocked

- **Scoped browser tests:** 8/8 passed; widths 320, 390, 768, 1440 in dark and light; actual inlined HTML rendered in Chromium via `set_content` (not native `file://`). Button enlargement, popup positioning with scrollbar tolerance, square/button width match, QR canvas unchanged, Escape, Reduce, outside-click, no JavaScript errors, and no network requests.
- **Static:** 29/29 application JavaScript units byte-identical to RC24 and syntax-valid; CSS stylesheet parses; source lock verifies.
- **Fault checks:** 2/2 passed: modified locked source rejected; existing build output not overwritten.
- **Not run / not claimed:** full historical 139-job campaign, physical signer, actual SeedQR scan by a physical device, signed PSBT result scenarios, native `file://` execution, full power-loss / network / disk / reboot / lifecycle qualification, publisher signature authentication.
- **Grade:** DEVELOPMENT UI PREVIEW / PUBLIC RELEASE BLOCKED. These targeted passes do not establish production readiness.
