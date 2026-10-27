# RC19 architecture freeze — UI-only scoped remediation

Baseline: RC17 (unmodified). RC18 standalone-only CSS patch is retired as a release source; it does not replace RC17.

Acceptance: four disclosure rows must communicate action at rest and after expansion, respond to pointer and keyboard, have a visible focus state, keep native semantics, and remain legible in dark and light. Session Go to test CTA must have a high-contrast foreground. Edge-case warning must remain conditional.

Ownership: one Alpine application coordinator and existing native `<details>/<summary>` controls; CSS affects presentation only. Existing wallet, Bitcoin signing, PSBT/QR, camera, verifier, and session journal remain authoritative. No new storage, routing, retry or privileged modules.

State: existing Alpine state; `open` attribute on native details for expanded controls. No added persisted state.

Recovery: reload retains existing RC17 behavior; no migration. Rollback: use unchanged RC17 archive. Upgrade: replace standalone HTML after scoped acceptance. No installation or hardware action.

Retired from release authority: incomplete RC18 standalone-only patch. Not a separate active controller.

Files changed from RC17 within the trusted source inputs: `src/style.css`, `src/page.html`, `release.json`, `source-lock.json`; other changes are test/doc/release metadata.
