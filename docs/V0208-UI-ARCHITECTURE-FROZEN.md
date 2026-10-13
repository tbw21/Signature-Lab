# v0.20.8-dev — frozen UI stabilization contract

Status: DEVELOPMENT. No approved public release. Scope frozen before implementation.

## Required result and acceptance criteria

* No changes to cryptography, signing-reference behavior, PSBT data interpretation, QR transport, camera capture, coordinator, session journal, seed generation, storage, safety outcomes, or network policy.
* One authoritative source tree, source lock and build; one resulting standalone HTML. The existing v0.20.7-dev and v0.20.3-rc1 artifacts remain unchanged.
* Fix the reproducible 390px Advanced/Session mobile heading dead-space issue (~460px filler) without clipping text or controls.
* Keep the Test progress stepper only in Test; do not confuse Advanced/Session navigation with disabled Test phases.
* Apply coherent typography, spacing, semantic button hierarchy, disclosure surfaces, neutral metadata, and restrained matched-state presentation across Test wallet, Transaction, Results, Advanced, Session, Help and dialogs.
* Preserve the disposable-wallet warnings and explicit match-limit language, preserve accessibility labels and controls.
* At widths 320, 360, 390, 768, 1024 and 1440 and in tested states, no horizontal document overflow or clipped primary actions, target buttons >=40px generally and >=44px for important touch actions; no unexpected 200+ px mobile empty heading region.
* Dialogs fit small screens without inaccessible confirmation/cancellation, and keyboard navigation/focus remains usable.
* Invalid imported response and matching-signature flows retain their existing state semantics. Explicit evidence handling and wallet retirement remain unchanged.
* Correct any confirmed malformed nonsemantic HTML in editable UI with a focused regression, but do not change runtime business behavior.
* Cumulative What's New from the initial v0.20.3-rc1 baseline through v0.20.8-dev.

## Boundaries

Trusted unchanged modules: all `src/*.js`, vendor files, `build.py`, `sources.json`, source-lock generator, and existing test algorithms. Allowed build inputs: `release.json`, `src/page.html`, `src/style.css` only. The source lock and expected output hashes are generated for this development version, not amended in a frozen candidate.

Optional UI presentation: CSS and semantic HTML. CSS must not implement business-state transitions or introduce unbounded retry/polling, telemetry, or extra controllers.

Privilege/ownership: browser-only, locally executed, no new origin, endpoint, upload, clipboard reads, privilege escalation or file persistence. Existing user-initiated export remains authoritative.

Authoritative state: existing coordinator and session journal. No duplicate ledgers, verification decisions, controller or retry engine.

Reboot/resume/rollback: single-document lifecycle unchanged; no cross-reload secret persistence, no automatic retry. Reverting to the v0.20.7-dev bytes is the rollback option. No active production release pointer changed.

Retired components: none; decorative duplication in non-Test navigation may be hidden, not new business logic. UI-only old style overrides may remain for backwards compatibility in the development candidate, but no new duplicate state logic.

## Qualification gates

1. Source inventory and exact allowed delta.
2. Build integrity, JS parsing, DOM structure and privacy attribute checks.
3. Browser visual/geometry matrix, interaction/focus/modals, expected success and error flows, no network requests.
4. Previously existing bounded unit/contract and fault-injection tests where practical, report historical version-bound failures separately.
5. Clean source and handoff archive extraction, byte-identical rebuild, deterministic packaging, idempotence, tamper rejection.
6. Hardware, native browser, publisher-signature, dependency provenance and independent security review are separate unfulfilled release gates and must be reported as such.

No candidate archive will be called an RC or approved for hardware acceptance until this qualification completes without a blocker. Any new runtime modification thereafter gets a new development identity.
