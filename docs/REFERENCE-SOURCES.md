# Primary sources and retrieval limits
Reviewed 17 September 2026. Source facts, direct code observations and deductions are
separated in REFERENCE-AUDIT-DISPOSITION.md. External references are documentation links,
not runtime downloads. No external dependency is fetched when the page starts.

1. Supplied signature-lab-reference-audit.pdf, 6 pages. Vectors pages4–6 transcribed by
   programmatic text extraction; all inputs/answers verified independently. No hardware
   evidence or the 20,000-signature experiment's corpus/code was supplied.
2. BIP repository index: https://github.com/bitcoin/bips . Draft listing for BIP461 and
   repository publication criteria were retrieved. Publication is not community adoption.
3. BIP461 PR2224: https://github.com/bitcoin/bips/pull/2224 . Merged16September2026; visible
   final proposal short commit b24f038, merge55083d3. September16 review requests vectors/
   implementation before Complete. August4 author comment describes an already-written
   implementation. Full final .md and diff retrieval did not yield complete pinned text;
   no full specification-conformance claim is based on an old/cached partial diff.
4. Bitcoin Core source: https://github.com/bitcoin/bitcoin/blob/master/src/key.cpp . The
   ordinary CKey::Sign low-r loop and SigHasLowR were readable; unpinned default-branch
   observation, not proof of a device's installed firmware. No Core executable is used
   as the production verifier. RFC6979 independent calculation is provided separately.
5. RFC6979: https://www.rfc-editor.org/rfc/rfc6979 . HMAC nonce construction and bits2octets
   reduction inform the independent Python oracle. It is not a pasted firmware signer.
6. BIP340 specification text: https://bips.dev/340/ . Default signing includes auxiliary
   data; fresh randomness recommended; other signing algorithms can produce valid outputs.
   This reference informs the deferred Taproot scope, not a new implementation.
7. Blockstream protocol explanation:
   https://blog.blockstream.com/anti-exfil-stopping-key-exfiltration/ . Multi-round host/
   signer commitment protocol and selective-abort caution. The possibility of transporting
   its required messages over QR is a protocol inference, not a product support claim.
8. BitBox developer explanation:
   https://blog.bitbox.swiss/en/anti-klepto-explained-protection-against-leaking-private-keys/
   . Historical anti-klepto design; not evidence of exclusive current product support.
9. Dark Skippy authors: https://darkskippy.com/mitigations.html . Conditional signing and
   spot-check limitations. The supplied PDF cannot override these limits by renaming methods.

Several requested GitHub backend/blob/raw views failed or returned incomplete file content:
libngu k1.c, embit ec.py, Jade sign_psbt/libwally sign.c, Trezor backend chain and Passport
C binding. The readable repository landing pages are not evidence of those function bodies.
Container DNS/raw/API retrieval was unavailable. No identity/firmware behavior is guessed
from a project name. Full exact-build source chains and authentic installed artifacts remain
necessary before publishing a qualified device-method matrix. No source submission, author
endorsement, external audit or hardware acceptance was performed in this workflow.
