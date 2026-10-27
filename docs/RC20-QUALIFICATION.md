# RC20 scoped qualification evidence

**Grade: development UI preview — public release blocked.**

## Focused acceptance
- Browser fixture: 6/6 combinations at 390/768/1440 CSS px in dark/light. Two named links and both session status labels and landing numeral are measured in light theme. Text contrast spans **6.85:1–7.43:1** across tested foreground/background combinations.
- Both result Evidence action row and Session Evidence nested diagnostic button are inside card bounds at all six fixture combinations.
- 29/29 application JavaScript sources match RC19 exactly and pass Node syntax checks.
- CSS parses; source-lock tampering and overwrite refusal work; independent rebuild matches output bytes.
- See `RC20-BROWSER-RECEIPT.json` and `RC20-STATIC-FAULT-RECEIPT.json`.

## Limitations and failed/incomplete attempts
- First contrast fixture failed because the harness attempted to parse `color(srgb ...)` from a *dark-mode blended background*, not an app failure. Harness corrected to compute contrast only for the requested light-mode text; dark-mode cards still undergo geometry checks. No change to app was made for this failure.
- Native file-origin test **blocked**: Chromium `net::ERR_BLOCKED_BY_ADMINISTRATOR` on the standalone local HTML.
- Focused CSS browser fixtures do not execute the wallet signing, QR import, result-verifier or save-export lifecycle. No complete end-to-end browser test run.
- Historical 139-job campaign, hardware acceptance and publisher authentication **not run**.

Source scope: `src/style.css`, `release.json`, `source-lock.json`, expected-output record, regression test and documentation/manifest. No core JS changed. No hardware effects. There is no automatic retry or other new state.
