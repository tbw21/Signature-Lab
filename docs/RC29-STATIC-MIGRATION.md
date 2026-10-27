# RC29 historical static-contract migration — DEVELOPMENT ONLY

## Immutable baselines and ownership

- Frozen input is the 0.20.12-rc28 original source and standalone HTML, never edited in place.
- The RC29 working tree is a test-only migration atop that input: eight historical static scripts, a pure test helper, a separately preserved original-script directory, this note, and a corrected current README.
- One authoritative application/Bitcoin/QR/signing runtime is retained. No alternative output generator, navigation engine, retry engine, state ledger, or separate release pointer.
- `release.json` is authoritative for release status; `source-lock.json` for exact assembler inputs; `EXPECTED-OUTPUT.json` for output identity; historical projections remain independently testable.
- No privilege, boot, installation, persistence, recovery, or rollback behavior is introduced to the application.

## Security and semantic rules

- Legacy assertions targeting the 0.20.11-rc3 version are migrated to the exact current version/status identity and unsigned caveat, never treated as publisher-signed.
- Historic assembler reverse-projection checks no longer misuse the old build.py digest. The current build.py must match its exact lock; the historical original script and historical projection records are retained.
- Retired `.seed-instructions`, `.tracker-session`, one-card/QR nesting, old Settings version badge, and retired copy labels are migrated to the current DOM while preserving separate control paths, user acknowledgment, fingerprint comparison, visible no-passphrase/seed warnings, release status, result warnings, QR canvas/quiet zone, offline CSP, and saved evidence.
- No original historical assertion is deleted from historical evidence. A contract migration is not proof of visual equivalence or of a physical wallet signing result.

## Qualification status

All changes are PREQUALIFICATION only. Do not freeze an RC29 candidate or start the canonical 139-job acceptance until all static families, browser regressions, independent negative mutation checks, source/manifests, reproducibility, and clean extraction are complete. Failures and unavailable hardware/publisher paths remain explicit blockers. RC28 remains a terminated/failed diagnostic candidate.
