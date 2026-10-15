# The Bitcoin Way — Signature Lab v0.20.11-dev

**Development preview only. Not a release candidate or approved public release.**

Signature Lab is a self-contained offline HTML application for preparing disposable Bitcoin test wallets, checking returned ECDSA signatures, and reviewing supported PSBT/transaction metadata. A matching result is not a firmware-safety certificate. Never import real seed words, overwrite an existing wallet, or fund this disposable wallet.

## Getting started

- **WHATS-NEW.md:** one cumulative, change-only record since v0.20.3-rc1.
- **docs/CURRENT-QUALIFICATION-REPAIR-ARCHITECTURE.md:** precise qualification-harness scope and acceptance criteria.
- **docs/ACCEPTANCE-PLAN.md:** test categories and frozen release-candidate rules.
- **docs/OPEN-GATES.md:** remaining external trust and hardware acceptance.
- **docs/FEEDBACK-ARCHITECTURE-FROZEN.md:** historical source and evidence lineage (not current qualification).

Never choose an older release as an automatic rollback or downgrade. Retired historical source projections support provenance only; they cannot qualify current UI or behavior. The v0.20.3-rc1 and later released development archives are separate artifacts with their own hashes. Tests against one version cannot be carried over silently to another.

## Reproducible build

From an extracted source archive, using preinstalled dependencies:

```bash
python3 build.py /absolute/path/to/NEW-BUILD.html
python3 tools/verify_output.py /absolute/path/to/NEW-BUILD.html
```

The builder checks `source-lock.json`, never overwrites existing output and requires no network. `EXPECTED-OUTPUT.json` records the expected exact HTML hash and size. Source lock and reproducible output establish consistency, not publisher authenticity.

The one authorized source archiver is:

```bash
python3 archive.py /absolute/path/to/this/source /absolute/path/to/NEW-SOURCE.zip
```

## Architecture and qualification

One authoritative application coordinator, signature-verification path, journal and offline HTML artifact. Cryptography, signer/PSBT code, QR and camera modules, and trusted vendor code remain at their recorded baseline hashes. No automatic upload, analytics or external fonts.

Current hardware/optical camera acceptance, genuine mobile browser and offline file/HTTPS origins, authenticated publisher identity, upstream dependency authenticity and independent security review are not fully qualified by synthetic software tests. A final release requires one clean, uninterrupted canonical campaign against frozen bytes followed by physical acceptance and explicit operator approval.

The historical hardware checklists are checklists, not records of completed device testing. Development diagnostics and failure records must be retained separately.
