# Signature Lab v0.20.4-dev: scoped privacy and usability change contract

STATUS: ARCHITECTURE FROZEN; developmental work only; v0.20.3-rc1 preserved byte-for-byte.

## Requirements / acceptance
* Preserve the existing single offline HTML and compatible cryptographic results; no runtime network dependencies.
* Preserve one application coordinator, one signed-response verifier, one immutable result snapshot, one session journal.
* Mark fields containing potentially sensitive transaction, device, or response information with cooperative browser text-service opt-outs, including cloned Alpine template fields. This does not defend against malicious browser extensions.
* Prevent translation of seed words and essential cryptographic identifiers using `translate=no` where those values are displayed; descriptive copy stays translatable. Detection of browser translation remains deliberately out of scope (no reliable cross-engine contract established).
* Initial wallet/test transaction uses a small payment case, while existing randomized later transactions and guided coverage remain unchanged.
* Warn users never to overwrite an existing real wallet, disclose supported BIP84 P2WPKH ECDSA only scope before proceeding.
* Present evidence-retention opt-in before scanning/importing the first signed response, sharing the current journal-owned state with Session; default off, bounded and in-memory.
* Add a separately confirmed Finish testing action for ending use of the disposable wallet (distinct from the journal's End session). It must stop capture and scheduled work, invalidate application-held secrets and references, reset retained evidence and navigate away from the test page. Never claim reliable zeroization of JS strings, browser caches, OS memory, swap, or extensions. Explicitly warn to save exports first.
* No wallet.dat, real wallet import, user entropy mode, WASM rewrites, new signing protocols, duplicate export/state ledgers, remote services, analytics or storage.

## Modules / trust boundaries
* Trusted core unchanged: source `src/04-bitcoin.js`, reference cryptography, signer-verification, metadata policy, result-snapshot, session journal and application coordinator (`src/20-application.js`).
* Presentation changes: `src/page.html` and `src/style.css`; minimal coordinator changes for starter case and Finish testing. No secondary controller.
* Browser attributes are advisory and optional; they may be ignored by an extension, OS, translation or browser feature. No parser/verification behavior may rely on them.
* Single HTML distributed as the authoritative application bytes; source-lock and build output verify identical bytes. No inline injection or visitor tracking from a CMS.

## Ownership / privileged operations
* Operator directly chooses a wallet, signs on an external signer, opts into evidence, exports reports and confirms end of testing. Site never acquires secrets from an existing wallet or device keys; browser only receives signed public responses.
* Downloads are explicit; file access is browser-provided; camera activation remains explicit.
* Publisher signing cannot be simulated by developer scripts; operator-controlled authenticated signing and independent key establishment are public-release prerequisites.

## State / rollback / reboot / recovery / upgrade
* Sole authoritative in-tab state: one application coordinator plus one journal and immutable result; no persistence, automatic resume or retry after reload or device reboot.
* Finish testing retires in-tab state. Browser/OS memory outside JS reach is not guaranteed deleted. A subsequent test starts by explicitly opening the app anew.
* Existing report and evidence export contracts unchanged; unsaved volatile results may be lost on Finish and new wallet; the confirmation must state this.
* Rollback is distribution-level: restore unchanged v0.20.3-rc1 bytes; do not hot patch a running user session.
* Upgrade requires fresh session, never imports active seed or merges previous volatile state.
* Retired: additional memory controller, WAsm rewrites, new signer adapters, auto-save, telemetry, automatic retesting, self-attesting safety badges.

## Qualification gates
Syntax/static; unit and contract; cross-module integration; hostile input / fault injection; clean install file/HTTP(S) simulation; populated-data adoption simulation; upgrade and rollback; recovery boot/reopen; idempotent second run; reproducible clean extraction. Test power interruption, script interruption, read-only filesystem, full disk, concurrent openings, CSP/network failure, signer failure, failed exports, stale caches, optional controls absent, translation advisory ignored and fake extensions. Unsupported native browsers and hardware are explicit unavailable gates. Candidate becomes frozen only after build plus accepted tests; a blocker requires a new version and full requalification.
