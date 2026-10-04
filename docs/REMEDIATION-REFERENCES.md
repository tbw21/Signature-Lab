# Primary protocol references and scope

- Blockchain Commons BCR-2020-012, Bytewords dictionary, CRC32 network byte order and published vector:
  https://github.com/BlockchainCommons/Research/blob/master/papers/bcr-2020-012-bytewords.md
- BIP174 PSBT format, signing/finalization fields and unknown/proprietary fields:
  https://github.com/bitcoin/bips/blob/master/bip-0174.mediawiki
- SeedSigner development signing view (not the exact user firmware):
  https://github.com/SeedSigner/seedsigner/blob/dev/src/seedsigner/views/psbt_views.py

The Bytewords test oracle was independently written with Python zlib and explicit CBOR.
It is not the official upstream conformance suite or an organizational security audit.
The reduced-PSBT rule is explicitly defined and tested in this project. Inspection of
development-source trimming calls is not substituted for the actual user response or
complete review of SeedSigner 0.8.7. Exact-version source retrieval was unavailable.
The 8-consecutive/24-total capture rejection limits are bounded engineering choices, not
optically calibrated thresholds or a claimed statistical guarantee against seed leakage.
