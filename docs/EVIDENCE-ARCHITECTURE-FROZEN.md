# Evidence and independent verification — architecture freeze
Date: 2026-10-02. Baseline: exact v0.19.0-rc1 HTML/source hashes in the qualification record.
Candidate identity reserved: 0.20.0-rc1. No changes to frozen v0.19.0 artifacts.

## Requirements and acceptance
1. Optional full-response retention in the open tab, controlled from Session, off by default.
   Store the existing public evidence, never the private prepared object or reactive app. One
   authoritative journal owns summary entries and their optional evidence attachments. No separate ledger.
2. Up to 16 MiB of UTF-8 evidence JSON and 256 retained response payloads, within the existing
   2,000-entry journal ceiling. These are serialized-data limits, not an exact JavaScript heap limit.
   At a capacity/serialization fault, latch retention failure for this wallet lifetime, preserve prior
   payloads, continue core verification, and show an explicit incomplete-evidence notice. No eviction,
   implicit retry, silent truncation, automatic download or persistence. Earlier missed evidence is not recovered.
3. Session-evidence JSON export binds each retained public result to its journal index and content
   hash; every checked entry has retained/missing status and reason. Completeness concerns recorded
   checks only, not requested/unrun cases, physical origin, malware safety or every optical frame.
   Disabling retention preserves retained payloads. New wallet/reload intentionally discards them only
   under the existing used-wallet confirmation. Single-result exports retain their existing behavior.
4. With retention enabled, record one allowlisted diagnostic event for each terminal camera attempt,
   separately from signature counts, in the same journal. No raw QR frame text, stack traces or untrusted
   exception text in diagnostic-only exports. Camera ownership and explicit-start/terminal-failure rules unchanged.
5. One optional diagnostic package action, with explicit unchecked inclusion of current full response.
   Build identity, public outcome/status and allowlisted counts/codes; no automatic browser fingerprinting,
   network, seed or private key export. Returned bytes may themselves contain hidden data: warn before sharing.
6. Extend the existing public-only Python replay tool with independent psbt-envelope-v3 reconstruction
   and comparison of classifications, counts, positions, hashes and version conversion from raw PSBTs.
   Unknown metadata/evidence/count policies fail explicitly. Bundle replay validates hashes, index
   binding, missing entries and per-response results; incomplete checks cannot be declared replayed.
   No claim of secret-key nonce derivation, reference authenticity, device origin or an independent organization.
7. Replace availability-only origins probing with actual critical workflows when engines are available.
   Missing tools and administrator-blocked origins remain unavailable, never passes. Actual Safari,
   native permissions/optics and phones remain external gates. No security-policy bypass or download at runtime.
8. Deliberate-defect qualification: known transaction-binding, signature-validity, metadata, summary,
   retention and export deviations on labelled temporary copies must cause named checks to fail. Report
   detected/escaped/invalid mutants separately. Original candidate remains immutable.
9. Preserve main visual layout and all current warning semantics. Add only existing-style Session/technical
   controls. No runtime dependency or signing-family expansion. Retained tests rerun, new bounded tests
   include absence/fault/capacity/tampering/reloads/concurrent capture and real JSON download checks.

## Boundaries and privileges
Trusted core unchanged: Bitcoin/reference computations, generator, supported methods, metadata policy,
QR codecs, camera controller, startup reference gate, immutable per-result evidence generator. Journal
and application coordinator gain optional evidence operations only. Existing script/CSP/browser permissions
unchanged. Public replay remains an offline review utility, not a second browser verifier/controller.
One build/source tree, one active candidate identity. UI calls these authoritative operations; no UI ledger.
Each new operation exposes inspect/plan/apply/verify/status/rollback via journal methods or read-only
replay/qualification commands as applicable. Rollback disables retention but never deletes existing evidence.

## Lifecycle and failure
Synchronous bounded retention and explicit export. Unsupported/corrupt evidence fails locally. Capture
telemetry records only terminal attempts; unavailable diagnostics do not mutate signature findings.
No automatic resume, retry or external side effect. Tab close/new wallet cannot undo a device signature.
No OS installer, bootloader, Bitcoin/Fulcrum services or persistent-data migration; recovery-boot N/A.
Fresh extraction/rebuild, reload/back-forward/upgrade/rollback/idempotence are qualification cases.

## Retired / not silently completed
Availability-only Firefox/WebKit coverage claims are retired; legacy raw reports retain original meaning.
Summary-only session download remains, explicitly named; full evidence is a separate deliberate export.
Framework/CSP and inherited-dependency replacement are a separate qualification unit: upstream acquisition
failed DNS in this environment before this freeze. This candidate will include a source inventory and
migration constraints, but cannot authenticate unknown inherited bytes by relabelling them. Publisher
signing, actual device tests, outside review, Foundation original-case triage and comprehension studies
remain externally owned. No detector reliability percentage is claimed.

## Freeze policy
Complete development qualification before freezing HTML/source. After freeze any blocker disqualifies
those bytes; corrections require a new identity and complete restart. No test-count carryover from baseline.
