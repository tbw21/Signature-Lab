# What would justify trusting this project for its limited purpose?

Trust the evidence for a particular check, not an implied guarantee about firmware.
A signature spot checker is not an anti-exfil protocol, firmware scanner or identity
attestation. Matching today cannot rule out a conditional future attack. The browser
knows the disposable secret and can itself produce references: importing those is not
proof that a physical device was operated. Keep real seeds/funds out of this tool.

## Release identity: a concrete issue in earlier deliveries
Two earlier attachments shared the version/file name v0.15.0-rc1 but had different
contents, functionality and acceptance records:
- 417-case record: HTML 9808d4b398c0389d56cb25a823526f1217bea123abcc24e368a35c96385ffc04,
  source ZIP 746c146f00d44daf77d1f68f0aaac89cb3f7b64471aa9b1b9b8d0c0ee424b73b.
- Latest 391-case record, matching the reported 1-200 UI:
  HTML 3d5dc1835bc4841132f099e771f05ce5eac113c126d7a0abb783626d594c3811,
  ZIP 9c752b1f456053f755713d923bda8eee3f6b97a0dd995c6626f94fec6908dc3f.
This is a release-management defect, not evidence of malicious code. A filename/version
alone cannot select between these packages. v0.15.1 has a fresh identity and pins the
latter baseline by hash. No old artifact is overwritten. Do not combine their test counts
or claim that every feature of both branches exists in this candidate.
Require an append-only release register, unique versions, authentic signed manifests,
immutable artifacts and a single advertised active release before broad distribution.

## Conditions for broader reliance
1. Publish readable source, documented trust boundaries/threat model, dependency inventory
   and authenticated build inputs. Reconstructed/minified inherited code is still a review
   and provenance limitation, even if local source assembly reproduces exactly.
2. Authenticate publication using the actual publisher's established signing key and an
   independently trusted fingerprint channel. A hash or key displayed by the same page
   does not authenticate that page. This candidate is unsigned; no publisher key was invented.
3. Obtain independent organizational review focused on verifier/PSBT parsing, malicious
   imports, return metadata, stale/concurrent state, report binding and release provenance.
   Tests authored during this workflow are not an outside audit. Fix findings with new
   immutable candidates and regression tests; publish scope and unresolved findings.
4. Rebuild the exact release independently and compare bytes. Reproducibility establishes
   source-to-artifact correspondence, not that the source is safe. A signature proves a
   publisher authorized bytes, not that those bytes lack defects.
5. Qualify actual hardware/firmware/browser/OS combinations, including ordinary file/HTTPS
   startup, optical scanning, permission changes and interruptions. Keep real device-produced
   fixtures with documented provenance. Public reference fixtures do not prove compatibility.
6. Observe beginners and experienced users on match, mismatch, incomplete, metadata warning,
   refusal and stalled-camera tasks. Require correct interpretation and recovery without
   real seeds or weakened signer protections. An attractive green result can mislead even
   when small print is accurate. No comprehension study has been performed here.
7. Publish a security-reporting channel, supported-version policy and clear response to a
   compromised release/signing key. Never silently replace old candidate bytes to repair it.

## Design consequences in this candidate
Advanced hides controls, never findings. Selecting or hiding tools cannot alter verification.
The active nondefault settings remain visible. The default path does not ask for real wallet
secrets. A fingerprint is a short comparison aid, not proof of unique identity or firmware.
Counts measure supplied checks and do not create a safety percentage. An incomplete/capture
failure is not a malware accusation; a mathematically valid mismatch still needs investigation.
No telemetry, runtime networking, automatic persistence or firmware-simulation shortcut added.
No claim that self-testing the website proves the website itself trustworthy.

## Sources consulted for this design (outside material, not test results)
- W3C WCAG 2.2 Understanding Reflow: https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
- W3C Resize Text: https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
- Dark Skippy authors on conditional behavior and spot-check limits:
  https://darkskippy.com/mitigations.html
- Reproducible Builds definition: https://reproducible-builds.org/
These support design principles. Actual defect/fix claims rely on local recorded tests.
