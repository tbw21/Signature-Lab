# External gates: not closed by code or synthetic tests

1. **Publisher authentication:** no independently trusted TBW release key/fingerprint
   was supplied. Tools for operator-owned signing and verification are provided and
   tested using throwaway keys only. This artifact is not publisher-authenticated.
2. **Upstream dependency provenance and review:** inherited library implementations
   remain reconstructed from the supplied bundle. pako 1.0.11 is pinned exactly, but
   independent comparison against authenticated upstream bytes is still outstanding.
   Container downloads failed, and registry/CDN metadata access was blocked. No claim
   of maliciousness or age-based vulnerability is made. A completed vulnerability and
   licensing review of exact upstream dependencies is still required.
3. **Independent source review/reproduction and publication:** a direct readable-source
   build is now provided. Original TypeScript/lockfile recovery, publication in an
   authorized repository, and reproduction/review by another organization were not
   performed. Current same-environment rebuilds do not replace these steps.
4. **Actual startup and interoperability:** file:// and loopback HTTP navigation were
   blocked by Chromium administrator policy in this environment. No policy bypass was
   attempted. Firefox/WebKit executables are unavailable. Actual Safari, Android/iOS,
   permission prompts, camera optics and physical signer/firmware qualification are
   outstanding. Physical signer tests: zero. Real optical scan tests: zero.
5. **Physical faults:** power loss, device disconnect, OS rollback failures, genuinely
   full disks and read-only mounted filesystems require separate testing. A real
   permission-denied directory check and API/process-boundary injections are labelled
   separately. Browser-only software does not install bootloaders, node services,
   Bitcoin/Fulcrum data or persistent wallet storage; those cases are not applicable.

The retained Alpine inline/eval CSP permissions are a disclosed defense-in-depth
review item, not a reproduced injection finding. Removing them blindly would break
this inherited application; no complete CSP-compatible UI rewrite is claimed.

These gates must remain visible in release communications. A hardware failure rejects
the candidate; fixes belong in a new frozen release, not a live patch to this archive.
