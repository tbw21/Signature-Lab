# Signature Lab v0.20.12-rc36 — DEVELOPMENT / NO-GO

**Current status:** unsigned development build. The complete 139-job frozen-candidate campaign, native browser-origin checks, optical/hardware signing and publisher verification have **not** been completed. Never use an actual wallet seed, real bitcoin or production signing device for unapproved experiments. A successful match does not certify firmware.

**Authoritative current state:** `release.json`, `source-lock.json` and `EXPECTED-OUTPUT.json`. The existing Bitcoin/signature/QR/camera/session runtime is unchanged from the independently reviewed RC30 cleanup except for the approved focus-reference change documented in its historical provenance. RC32 corrected two mobile control heights; RC33 corrected stale signing-layout visibility on invalid transactions; RC34 aligned 12/24-word and QR-format control sizing. These scoped presentation changes are independently pinned in `fixtures/rc32-historical/`, `fixtures/rc33-historical/` and `fixtures/rc36-historical/`. Rebuild with `python build.py NEW_OUTPUT.html` and verify with `python tools/verify_output.py NEW_OUTPUT.html`. A passing rebuild is consistency evidence, not publisher authentication.

**Current testing:** RC36 is the approved CSS-optimized presentation with a unique version and SHA-256 identity. The 29 application runtime modules, template, and vendor code remain unchanged. The full qualification suite is included only in the Full Source and Tests archive; focused static checks pass, but an uninterrupted 139-job RC36 acceptance receipt has not been obtained. Prior RC35 acceptance is historical and does not qualify these RC36 bytes. Publisher signing, physical optical/hardware validation and unavailable normal-origin browsers are separate requirements.

## Historical source history, not current qualification

The following archived notes document earlier development revisions. Their release names and test claims do **not** describe the current RC34 application or RC38 development-overlay acceptance.

### RC30 retired-navigation cleanup (historical)

The hidden old three-tab Test/Advanced/Session navigation and its CSS were removed. Current Settings drawer, visible Back to test controls and existing application coordinator remain authoritative. One focus fallback in `src/20-application.js` now targets the visible Settings summary. See `docs/RC30-RETIREMENT-ARCHITECTURE.md` and `RC30-QUALIFICATION-STATUS.md`.

**Historical records below are archival references, not current release claims.**

---

# Signature Lab v0.20.12-rc28 — BLOCKED development preflight

**Authoritative release state:** see `release.json`, `EXPECTED-OUTPUT.json`, `source-lock.json` and `QUALIFICATION-STATUS.md`. These RC28 files are a **development UI preview**, unsigned and not approved for public release, hardware acceptance or deployment. Original RC28 application and vendor modules are unchanged in the RC29 static-test migration. Do not treat isolated preflight passes as a qualified 139-job run.

**Current migration:** the test-only RC29 development work ports retired navigation, historic version-string and obsolete copy/layout assertions without relaxing the underlying offline/privacy, fingerprint, no-passphrase, recovery-word, signing-verification, evidence and terminal-failure safeguards. Historic unmodified tests are under `fixtures/legacy-contracts-rc28/`; their SHA-256 entries are in `SHA256SUMS.json`. This migration is not an RC29 release candidate, has no publisher signature, and does not change the trusted runtime. See `docs/RC29-STATIC-MIGRATION.md` for what changed and which tests actually ran.

**Architecture history:** `docs/FEEDBACK-ARCHITECTURE-FROZEN.md` and other frozen architecture records remain historical, not a replacement for the current source lock. Never choose an older release as an automatic rollback or downgrade; use only an explicitly approved, hash-verified candidate.

**Historical source history, not current qualification:** Prior release notes are preserved below for reference. Names and qualification claims in the sections below refer to their own historic candidates only.

---

# Signature Lab v0.20.12-rc26 — BLOCKED development preflight

This source is not a qualified release. See `RC26-PREFLIGHT-STOP.md` and `RC26-MIGRATION-NOTES.md`. Its original historical security fixtures are retained; original RC25 versions of modified tests are under `fixtures/legacy-contracts-rc25/`.

# TBW Signature Lab v0.20.12-rc24

**Development UI preview; not a public release.** Based on frozen RC23; presentation-only correction of Advanced card spacing, expanded technical transaction content, and light-mode Input/Output row contrast. No functional modules changed.

Build from locked source with `python build.py /new/output.html` (must not already exist). Run `python tests/rc24-layout-browser.py /new/output.html 320 390 768 1440` and `python tests/rc24-contrast-browser.py /new/output.html` with Playwright/Chromium installed. See `docs/RC24-ARCHITECTURE-FROZEN.md` and `docs/RC24-QUALIFICATION.md`.

Only use a disposable wallet and no real bitcoin. A signature match cannot certify firmware safety.
