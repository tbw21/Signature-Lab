# RC21 Architecture and acceptance freeze

Baseline: frozen RC20 handoff. Goal: eliminate illegible text or escaped action controls across real application routes, light/dark and responsive widths. No new functionality.

**Trusted and authoritative core:** Existing `src/20-application.js`, verifier, wallet generator, QR codec, camera, importer, session journal and their dependencies are unchanged. The Alpine controller remains the single controller and state authority. No parallel UI ledger, retry engine or controller is introduced.

**Presentation-only boundary:** Only `src/style.css` changes user-visible rendering. Light theme has dark orange text on light surfaces but preserves filled orange CTA styling; transaction outputs and TXID use theme ink and surface tokens; Guide controls and contents table use legible contrast. Source identity/manifest/release metadata and documentation are updated only for this candidate.

**Ownership and privilege:** Browser-local disposable test wallet; no new persistent storage, network, filesystem write, permissions or browser API. Source build remains no-overwrite and locked. Downloads and user-controlled import remain existing authority.

**Reboot/resume/rollback/recovery/upgrade:** Page reload discards temporary wallet according to existing application contract; no new migration/adoption changes. RC20 remains untouched as previous frozen rollback artifact. New RC21 standalone bytes are immutable after candidate freeze. No software/service installation performed.

**Explicitly retired:** None. All original optional session, Help, camera, evidence, QR, diagnostic and transaction operations retained.

**Acceptance contract:** Browser-document measurements across 390, 768, 1440 in both themes: no text contrast below 4.5:1 for regular text and 3:1 for sufficiently large/bold text in audited visible states; no document horizontal overflow or offscreen controls; native disclosure activation and keyboard semantics unchanged; diagnostics export contained; no page error or external network requests. Note measured effective background is a computed ancestral-color approximation. Native `file://` acceptance and hardware remain distinct blockers.
