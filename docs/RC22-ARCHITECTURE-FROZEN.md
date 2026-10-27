# RC22 architecture and acceptance boundaries — frozen before acceptance

Baseline: immutable v0.20.12-rc21. Scope: UI presentation and conditional status semantics only.

- Trusted core: existing wallet generation, PSBT assembly, signing/reference verifier, QR encoder/decoder, camera lifecycle and importers, metadata, evidence and session journal. No edits.
- Optional capabilities: guided sessions, advanced editing, diagnostics, QR mode choice, educational examples. None blocks the core test path.
- State: the existing single Alpine app controller and in-tab session journal. No new persistence, ledger, retry logic or extra controller.
- Privileges: browser-local operation, no added network, storage or OS privileges; no persistent authentication or publisher claim.
- Lifecycle: reload/discard remains as in RC21, no installation, service management, boot behavior or ownership modification.
- Rollback: use untouched RC21 standalone HTML and handoff; no in-place replacement.
- Retired: no functional components retired. A redundant session link is replaced by a static status only while Sessions is already active.
- Component contracts: existing inspect/plan/apply/verify/status/rollback behavior not extended; source build verifies a locked manifest and refuses overwrites.

Acceptance: zero syntax errors, zero modified trusted JavaScript files, no overflow/contrast findings in surveyed light/dark UI states, correct selector alignment, no inert control on Sessions, preserved import/QR paths. Release status remains development-ui-preview-unqualified until full historical, real-origin, signed-response and hardware qualification passes.
