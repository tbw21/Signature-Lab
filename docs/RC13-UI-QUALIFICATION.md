# v0.20.12-rc13 qualification evidence and limitations

Status: **DEVELOPMENT UI PREVIEW. PUBLIC RELEASE BLOCKED.** This is not a firmware safety assurance.

- Architecture and allowed source changes were frozen before scoped implementation. Only the two presentation files, release identity, source lock, expected-output sidecar, current docs, and a dedicated focused browser test were changed/added.
- Targeted browser: 6/6 Chromium `document.set_content` contexts, 390/768/1440px, light/dark. Each case checked the short start heading/explainer and wallet safety, absence of purpose card, icon/drawer, Help/FAQ/return, no horizontal overflow, no page exceptions or HTTP(S) requests, hidden ordinary-scenario notice, and displayed boundary-scenario notice.
- Static: CSS parsed by `tinycss2`, Python compiled, HTML structural checks, source build lock and expected HTML output validation.
- Tests are synthetic and cannot attest that a physical signing device generated a particular signature. No hardware acceptance was run.
- Browser-native `file://` loading was BLOCKED BY TEST-ENVIRONMENT ADMINISTRATOR and is NOT counted as a pass. The offline document-context smoke test is not a substitute for native `file://` or production HTTPS origin.
- No full canonical 139-job campaign, physical signer/SeedQR camera cycle, production origin, external security/publisher verification, rollback hardware trial, real disk/power fault injection, or public release approval was performed for these bytes.
- Harness failures during development: one icon computed-size expectation (22px vs asserted 23px), a test scope error (attempt to set read-only `scenarioId`), a reference to a non-global Alpine variable, a Playwright arg-call mistake, then stale copy expectations after a copy refinement. Corrected in the test harness. None was a verified application defect. Preserve this disclosure rather than rewriting the history as a first-run pass.
