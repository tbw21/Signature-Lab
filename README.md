# The Bitcoin Way — Signature Lab v0.20.9-dev

**DEVELOPMENT PREVIEW — NOT A RELEASE CANDIDATE, NOT APPROVED FOR PUBLIC DEPLOYMENT.**

Signature Lab is a self-contained offline HTML application for preparing disposable Bitcoin test wallets, examining returned ECDSA signatures, and comparing them with supported deterministic reference results. A match **does not prove signer firmware is safe**. Do not use a real seed, overwrite a real signer wallet or fund the disposable wallet.

## Start here

1. Read **[WHATS-NEW.md](WHATS-NEW.md)** for the **single cumulative changelog** from the original v0.20.3-rc1 through v0.20.9-dev.
2. Read **[docs/V0209-ARCHITECTURE-FROZEN.md](docs/V0209-ARCHITECTURE-FROZEN.md)** for authorized source boundaries and acceptance criteria.
3. Read the accompanying **QUALIFICATION-REPORT.md** in the handoff before any testing or deployment.

The recent versions focused on visual polish; they do not change the existing cryptographic verifier or promise complete memory wiping.

## Reproducible offline build

```bash
python3 build.py /absolute/path/NEW-BUILD.html
python3 tools/verify_output.py /absolute/path/NEW-BUILD.html
```

`build.py` refuses to overwrite existing files, verifies `source-lock.json`, and requires no network or previous HTML build. `EXPECTED-OUTPUT.json` pins the exact expected built bytes. The manifest and checksum demonstrate release consistency **not publisher authenticity**.

The deterministic source archive is created by:

```bash
python3 archive.py /absolute/path/to/this/source /absolute/path/NEW-SOURCE.zip
```

## Runtime architecture and release gates

One application coordinator, one verifier, one session journal, one source lock and one authoritative offline HTML artifact. No new browser network endpoint, analytics, signer adapter, persistent secret storage, background retry engine or alternate verifier was added.

Public release is still blocked pending a complete clean software qualification campaign, native-browser and physical signing/optical acceptance, authenticated publisher signing, verified upstream dependency provenance and independent security review. Earlier v0.20.3-rc1 through v0.20.7-dev artifacts stay frozen and unmodified. The active public release pointer has not been changed.
