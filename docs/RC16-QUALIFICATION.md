# RC16 software qualification — scoped, not public-release approved

## Positive evidence
- `rc16_layout_browser.py`: 6/6 combinations at 390/768/1440px in dark/light; wallet to signing, QR format selection in both directions, original PSBT/response controls, desktop same-height cards, QR control/action row alignment, pending-result heading/card and functional return; no runtime exceptions or HTTP(S) requests observed.
- Browser startup attempt at 1440 light **timed out at the initial 25-second wait**; the manually executed bounded 60-second startup test on unchanged application bytes subsequently passed. This is recorded as an initial timeout, not erased.
- 73 Python source/test files passed AST parsing, 30 JavaScript files passed Node syntax, CSS parsed with zero errors, and all 29 application/vendor implementation units listed in `sources.json` are byte-identical to RC15.
- 5/5 isolated fault checks passed: clean build, refusal to overwrite, source-lock tamper detection, false signed-release rejection, and concurrent creation safety.
- Source/outer manifests, deterministic packaging and clean extraction must be verified after candidate freeze separately.

## Known failures and unavailable work
- Historical static suite: 26 passed, **17 failed** on hard-coded older source/version and layout projection contracts. Preserved, not patched or bypassed. The entire legacy canonical 139-job acceptance was not run and is not qualified.
- A bounded BBQr regression command was interrupted before a result receipt and cannot count as passed. RC15's 178 passed core checks are prior-baseline evidence, not a fresh RC16 pass. Unmodified implementation source does not transform those into a newly executed pass.
- Physical signer/camera tests, native file-origin restrictions, signature/publisher authentication, real hardware fault injection, power-loss and full lifecycle acceptance were not performed.

**Grade: scoped development UI preview. Public release blocked.**
