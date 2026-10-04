# Disposition of the supplied reference audit
Baseline reviewed: v0.16.4-rc1. Correction candidate: v0.17.0-rc1.
Basis: supplied six-page signature-lab-reference-audit.pdf, exact baseline HTML/source,
independent calculations and primary-source checks described in REFERENCE-SOURCES.md.
The audit itself states no hardware was tested. This review does not convert source
observations or synthetic tests into hardware acceptance.

## A1. BIP 461 and renaming the reference (PDF pages 1–2)
**Partly verified; naming recommendation not adopted as written.** The official BIPs index
lists Deterministic ECDSA Signatures as Draft; PR 2224 was merged 16 September 2026. The
repository explicitly separates publication from consensus/adoption. The PR maintainer
requires vectors and a reference implementation to advance to Complete. The author had
already described writing a test implementation in August, so “nobody has contributed”
must not become a first-mover claim. Contributing reviewed vectors could be useful, but
is not publisher authentication, an independent security audit or a substitute for hardware.

The bundled grind-core rule is directly inspectable: first no auxiliary bytes, then a
little-endian 32-bit counter in a zero-padded 32-byte buffer; strict r < 2^255; low-s. The
Bitcoin Core source path available in this review uses the same ordinary grinding approach.
All supplied vectors and additional digest/order boundaries reproduce. However, full
current BIP text at a pinned revision could not be retrieved reliably: GitHub file/diff
views failed and raw/API retrieval was unavailable. Therefore no exact full-BIP conformance
claim or policy-ID rename is issued. Help acknowledges the Draft and links its review;
grind-core, grind-embit and plain remain stable IDs. No default is changed.

**Rejected inference:** naming one option “standard” cannot narrow the covert channel if
the same multiple distinct outputs are accepted. Fixed-policy selection already exists;
labeling is not a verification change. Distinct accepted choices can carry information.

## A2. Firmware-reference table (PDF page 2)
**Not qualified as a device matrix.** The PDF gives default-branch paths, not pinned full
build chains, signed installed firmware or actual returned evidence. Some referenced
file/backend views were unavailable in this review. It also expressly did not inspect
the Passport C binding; a wrapper without a visible loop does not establish the backend's
nonce behavior. “Foundation Passport” cannot be silently generalized to Foundation Prime.

- Coldcard/Jade strict-low-r mapping: plausible source-level claims, not verified exact
  device/firmware/backend qualification here. No automatic profile was added.
- SeedSigner/Krux/Specter embit mapping: the Lab's actual DER-length variant is proven by
  counterexample vectors; a complete firmware mapping and the claimed 200-attempt cap
  require the pinned dependency/backend chain. The Lab retains its bounded 100,000-counter
  fail-closed implementation, not an assertion of every embit exhaustion behavior.
- Trezor plain/default/legacy-backend claims: no exact-version/backend matrix completed.
  Very rare digest/order boundaries are now independently tested in the Lab itself. That
  does not certify either backend. No broad warning that older Trezors are defective.
- Passport/Prime, Ledger and Keystone: source/response gaps remain; no device exemption,
  auto-selected policy or malware verdict is derived from them.
- Jade “only USB” anti-exfil claim: transport and firmware-dependent; not established
  here for all current transports/devices. Current product claims need exact source and
  supported-host workflow documentation, not a generic anti-exfil protocol description.

The relative cost of false positives versus false negatives is not a universal fact.
Both matter. An unsupported method or unexplained field transformation must retain its
actual finding, not be silently passed or called malware.

## A3. Variant divergence, sample rates and a two-input floor (PDF page 3)
**Mechanism verified; reported sample probabilities not imported as guarantees.** Supplied
vectors 13–16 have high-r but short-s signatures of DER length <=70; embit stops while
strict-low-r continues. Vectors 9–12 distinguish plain from both grinding methods. The
first eight coincide. All 48 answers match independently and the current baseline.

The PDF's 20,000-input corpus, sampling procedure and executable were not provided. Its
1-in-241, 3.7%, 49.9% and 2^-k statements cannot become measured reliability or attribution
rates for this Lab. Even the binomial calculation requires distribution/independence
assumptions. No minimum-two-input change: one-input and boundary coverage remains useful.

**Rejected universal claim:** an attacker-manipulated nonce need not always miss every
accepted reference. Choosing between accepted outputs or behaving honestly during a
spot test remains possible. Variant identification is not malware-detection probability.
Help now explains the distinct stopping rules and keeps these limits visible in methodology.

## A4. Taproot/BIP340 auxiliary randomness (PDF page 3)
**Feasible future capability, not a current ECDSA defect.** Fixed known auxiliary input plus
key/message yields reproducible BIP340 signing. Unknown fresh auxiliary input prevents
reconstructing that exact expected signature from the key/message alone, but does not
prevent mathematical signature validity checks. A mismatch cannot establish which nonce
or auxiliary policy produced it. Do not label a differing response “device randomizes aux”
without additional evidence; do not disable protective randomness to obtain a match.

BIP340 recommends unpredictable auxiliary randomness when available. “BIP86 is default
in most wallets” is unsupported by a measured wallet-distribution source here. Full
BIP86 derivation/tweaks, BIP341 sighashes, BIP371 maps, supported spend restrictions,
negative vectors and actual device qualification are separate work. This release keeps
Taproot unsupported rather than bolting it onto the ECDSA installation-critical path.

## A5. Known-answer startup check (PDF pages 3–6)
**Implemented, with narrower trust claims.** All 16 supplied rows were extracted without
OCR and normalized only for line-wrapped hex. Python HMAC/OpenSSL independently reproduced
48 DER answers and verified each signature before adoption. The independent suite also
checks 12 key/message boundary combinations (36 signatures), plus absent auxiliary bytes
versus an all-zero 32-byte auxiliary argument. OpenSSL's deterministic-signing implementation
is used as an additional plain-RFC6979 crosscheck.

The new mandatory gate runs all48 through the existing Op function, checks validity and
wrong-message rejection, and only then permits Fv to construct the disposable wallet.
Failure latches terminally with no camera, test result or in-page reset. Success is cached
once per page lifetime and reported quietly inside technical Help. Known answers and
public keys are never substituted for the user's device response or counted as test progress.

This catches exercised computation/regression faults. It cannot authenticate a download,
detect every corruption, guarantee entropy quality, monitor all subsequent operations or
stop a malicious page/browser that changes both the checker and its assertions. The
cooperative elapsed-time check is not a hard preemptive timeout for a stuck JS engine.
No success badge claims firmware safety. Publisher signature verification stays external.

## A6. Air-gapped signing and anti-exfil framing (PDF page 6)
**Do not adopt the proposed exclusivity claim.** Disposable test keys avoid importing
funded wallet keys only if never funded/reused. They do not make signature spot checks
protect later real-wallet signing. A malicious signer can recognize or pass a test.

The documented anti-exfil protocol uses a sequence of commitments and responses. As a
protocol-design inference, those bytes are not inherently restricted to USB; optical QR
exchange is possible when both applications implement the required rounds. That is not
a claim that a named product currently supports it. “Air-gapped QR has no other defense”
and “anti-exfil cannot reach QR” are therefore too strong. Help now distinguishes Lab
spot checks from anti-exfil rather than advertising them as equivalent or exclusive.

## Preserved scope and remaining evidence
Signing math and all method selection rules, parsing, metadata policy, QR and camera
controllers, exported evidence and session accounting are unchanged. Only application
startup gating/error presentation and technical Help are modified, with one additional
mandatory source module and documented test additions. No device profile is certified,
no old orange Foundation case is declared harmless, and no previously missing raw response
is reconstructed from a summary. Exact hardware/browser acceptance, complete dependency
provenance, publisher signing and outside organizational review remain external gates.
