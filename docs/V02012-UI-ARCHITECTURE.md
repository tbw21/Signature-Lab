# Signature Lab v0.20.12-rc1 UI qualification scope (frozen before implementation)

Baseline: signed v0.20.11-rc3 HTML and October 19 audit-fixed source. A new UI-only release candidate must not inherit the baseline's 139/139 test result.

Requirements and acceptance: same BIP84/P2WPKH ECDSA verifier, PSBT and QR codecs, self-check, immutable session journal, strict parsing/resource limits, recovery and explicit operations; no added network calls, dependencies, persistence of seed/evidence or separate verification logic. Clear disposable-wallet warning and wallet fingerprint confirmation. Keep selectable 12/24 words; do not force writing them down. Minimize clicks without changing the exact meaning of verification results. A single combined transaction/response workspace has two independently necessary actions, with a choice of supported transport for each. Accurate result statuses. One advanced area and one help projection. HTML must work standalone and remain website-hostable with strict CSP and no analytics inside app origin.

Visual system: official bundled wheel logo, orange #EB8404, thin monochrome iconography, warm off-white light mode plus deep-navy dark mode, user-selectable theme, no em dash in visible labels. Prefer system sans-serif fonts without external resource loads. Avoid decorative backgrounds, excessive iconography and stacked reassurances.

Architecture: Existing src/20-application.js remains the unique coordinator. No new verifier or storage owner. One session journal, one camera owner, one build pipeline. Entry screen is presentation state only. Test stage 1 is disposable-wallet setup; stage 2 contains unsigned PSBT and signed-response intake; stage 3 is read-only results. Device fingerprint check is mandatory before stage 2. Source asset and manifest are canonical; archive has one active RC identity.

Trust and safety: no user seed is read from a file or requested for past wallet; only locally generated disposable words. No clipboard auto-copy, storage of private material, or automatic background camera. No automatic retry of failed parsing/signature checks. Aborted or failing tests remain visible.

Resume, rollback, recovery: reload discards ephemeral seed/session. Operator can save evidence, not recreate historical session by reloading. Old signed v0.20.11-rc3 is preserved unchanged as rollback artifact; rollback is manual and not implicit. Any candidate test blocker rejects rc1 and requires a new rcN and whole qualification restart.

Explicitly retired: split camera intake page; duplicate step-3 import interface; former prominent developer navigation on beginner landing; mockups that claimed privacy risk absent without evidence; fictitious persistent saved-results browser database.

Qualification required: static, unit/contract, cross-module, fault injection, clean install/source build, existing test-data adoption (simulated), upgrade/rollback, recovery-boot equivalent browser reload, idempotent second run, archive reproduction, entire canonical 139-job suite, browser origins and physical-device tests recorded separately. No 'fully qualified' grade without all in-scope gates actually passing.


## RC2 visual remediation addendum

The prior RC1 is rejected and frozen. RC2 changes only src/page.html, src/style.css, release.json, release metadata, and the integrity manifest. The browser-rendered workspace header flex-basis caused the 720-pixel empty gap; it is now explicitly bounded. The Dark Skippy optional demonstration is reached from Help, not the beginner seed setup, and uses theme variables rather than a hard-coded dark dialog. The original recorded attack evidence is preserved. Response import is gated on a built/reviewable original transaction, with QR, file and paste alternatives and one evidence opt-in. No new application coordinator, ledger, verifier, dependency, storage, or restart model exists. Full RC2 qualification remains pending; RC1 results cannot be inherited.
