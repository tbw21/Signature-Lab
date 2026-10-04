# Signature Lab

Offline signature spot checker for disposable BIP84 P2WPKH single-signature wallets. It compares the signatures returned by a hardware signer with deterministic reference signatures computed locally, to help detect firmware that leaks seed information through its signatures, such as a [Dark Skippy](https://darkskippy.com/) attack.

> **Never enter real wallet words, fund generated addresses or broadcast the test transactions.** Use only the fresh disposable words the page generates. A matching response is not firmware certification or proof that a physical device performed the operation.

## Download and verify

Get the HTML from the [latest release](https://github.com/tbw21/Signature-Lab/releases/latest). It is a single self-contained file that runs offline in a browser.

The HTML is signed by The Bitcoin Way release key:

```
The Bitcoin Way <info@thebitcoinway.com>
4A90 B73E 93B8 74E5 C9AF  4283 1EE7 B858 B999 BC2B
```

Download `tbw-release-key.asc`, the HTML and its `.sig` from the release, then:

```sh
gpg --import tbw-release-key.asc
gpg --verify TBW-Signature-Lab-<version>.html.sig TBW-Signature-Lab-<version>.html
```

Confirm the fingerprint from a source other than this repository before trusting the key.

## How a test works

1. Open the HTML in your browser. The built-in reference self-check must pass before the test wallet appears.
2. Load the displayed disposable words on your signer with no extra passphrase. Compare the fingerprint, then choose **Wallet confirmed**.
3. Review all destinations, amounts and fees on the signer itself, then sign.
4. Scan, import or paste the signed response. All three paths use the same verifier.
5. Repeat with new randomized transactions using the same seed. 20 is a suggested routine, not a safety threshold.

A device may refuse the invented transactions. Stop there; do not weaken device protections, overwrite a real wallet or fund the disposable wallet to make a test work.

## What is checked

- **Signatures**: each response is checked against reference results for plain RFC 6979, Bitcoin Core low-R grinding and embit DER-length grinding. A fixed policy can be selected before import to require one method.
- **Transaction binding**: the transaction is rebuilt from local data; returned signatures are verified against it and must match a reference byte for byte.
- **PSBT metadata**: every returned key/value field is inventoried and compared with the prepared PSBT, including field positions. A signature match with unexplained file changes is shown as needing review.

Taproot/Schnorr, multisig, non-BIP84 scripts, BIP39 passphrases, randomized nonces and anti-exfil protocols are outside the supported test flow.

## Saving evidence

- **Save result**: the current result with its original returned data and public test details.
- **Save session evidence**: earlier responses retained in the open tab. Enable **Session > Session evidence & diagnostics > Keep result evidence in this tab** before importing the first response; earlier responses cannot be recovered. Retention is limited to 16 MiB of serialized evidence and 256 responses, with no eviction.
- **Save session record**: summaries and history, not every original response.

Exports never deliberately include the locally held seed or private keys, but returned data can contain hidden information. Review before sharing. Nothing is saved or uploaded automatically.

## Independent replay

From the source root, a reviewer can recheck a saved result or session file offline:

```sh
python3 tools/replay_evidence.py saved-result-or-session.json --output replay.json
```

It checks transaction binding, signatures, consistency with saved public references, and independently reconstructs the PSBT metadata assessment. It cannot authenticate a reference, derive secret-key nonces from seed-free data, attest hardware origin or certify firmware.

## Build from source

Python 3.10+; all runtime inputs are bundled and no network access is needed. The output path must not already exist.

```sh
python3 build.py /absolute/path/rebuild.html
python3 tools/verify_output.py /absolute/path/rebuild.html
```

`verify_output.py` confirms the rebuild matches the release HTML recorded in `EXPECTED-OUTPUT.json`.

## Qualification

Use a dedicated environment without real wallet secrets. Install the exact versions in [qualification-requirements.txt](https://github.com/tbw21/Signature-Lab/blob/main/qualification-requirements.txt); the suite also needs Node, system Chromium, OpenSSL and libzbar.

```sh
python3 -m pip install -r qualification-requirements.txt
python3 qualify.py HTML SOURCE_ARCHIVE RESULTS --stage environment
python3 qualify.py HTML SOURCE_ARCHIVE FRESH_RESULTS --stage all
```

A missing or mismatched prerequisite reports an unavailable environment, not a test failure. Results must be written outside the source tree.

## Limitations

A match confirms a supported reference result for one transaction. It cannot rule out every way of hiding information. A malicious signer can behave honestly during a test and leak later, or trigger only for particular amounts, wallets or transactions. Choosing between several accepted reference methods could itself carry information. This tool does not audit firmware, seed generation, supply chains or the browser running it. See [what would justify trusting this project](https://github.com/tbw21/Signature-Lab/blob/main/docs/TRUST-REQUIREMENTS.md).

Physical device and native browser acceptance, vendor dependency provenance and independent organizational review remain open. Testers can use the [hardware acceptance checklist](https://github.com/tbw21/Signature-Lab/blob/main/docs/HARDWARE-ACCEPTANCE.md) and the [evidence retention addendum](https://github.com/tbw21/Signature-Lab/blob/main/docs/EVIDENCE-HARDWARE-ACCEPTANCE.md).

## Credits

The detection method and the three reference signing algorithms come from [exfil-tester](https://github.com/oren-z0/exfil-tester/tree/27baa3afc5d4ff8e19b7e77cf1ffe7c2a4b9d912) by oren-z0.

## License

[MIT](https://github.com/tbw21/Signature-Lab/blob/main/LICENSE.txt)
