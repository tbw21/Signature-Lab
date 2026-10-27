# RC12 presentation and Results comparison

## Scope
Frozen as documented in the separately supplied ARCHITECTURE-FROZEN.md. Compared with RC11: `src/page.html`, `src/style.css`, `release.json` and `source-lock.json` are the only changed original source entries. Navigation, verifier, wallet, QR, camera, and session state modules are unchanged.

## Tests
- 6/6 offline Chromium document-context combinations: Light/Dark by 390, 768, 1440px. Checked logo from wallet setup, Help, Advanced and Session, wallet/session identity preservation, no network requests, readability of welcome supporting text, and absence of horizontal overflow or JavaScript errors.
- 2/2 synthetic valid signed-PSBT completed-Results scenarios, one per theme. Checks the completed result, evidence cards, report section, result controls, and disappearance of the empty state.
- The first two UI runs failed on incorrect test assertions (an exact phrase mismatch and an ambiguous Help locator), not application defects. Original receipts are kept in the handoff evidence. The corrected third run passed.
- Both result scenarios used an offline document-context Chromium harness, not live hardware, `file://`, HTTPS, or browser-origin acceptance.

## Original RC3 Results disposition
Verified in the source and rendered on a completed synthetic result: transaction data evidence, signature counts, reference comparison, repeat-test and Save result actions, evidence/diagnostic sections remain. Signed response intake lives in the combined sign-and-return workspace, not the completed Result card. No application result or security checker was retired.

## Limitations
The newly supplied reference screenshot in the conversation could not be accessed by the runtime at review time, so a specific unnamed visual element in that image was not verified. This must not be represented as accepted. Complete canonical, production browser origin, physical device acceptance, and public release approvals are outstanding. Zero application security module changes does not guarantee zero regressions.
