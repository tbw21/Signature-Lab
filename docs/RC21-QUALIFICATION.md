# RC21 Qualification and limitations

Grade: **development UI preview — public release blocked**.

## Verified before candidate freeze

- Static: 29/29 JS modules pass Node syntax and are byte-identical with RC20; Python build/archive parse; CSS parses with no errors.
- Chromium actual standalone app in `page.set_content` (document context): 6 responsive theme/width combinations and 14 states each, **84 state checks / 6,578 rendered text samples**, **0 detected contrast failures**, **0 horizontal overflow states**, **0 offscreen control states**, **0 JS errors**, **0 observed HTTP(S) requests**. States: landing, 12/24-word wallet, sign closed/open, BBQr, response method, session collapsed/expanded, Settings open, Advanced collapsed/expanded, Help collapsed/expanded.
- Keyboard/pointer and auxiliary checks: 4 combinations (light/dark × 390/1440): output and technical disclosure activation, space-key state change, BC-UR/BBQr controls, empty-result navigation, diagnostic card containment, session export and finish actions. Complete tests pass.
- Fault tests: tampered source rejected by source lock; overwrite refused; unauthenticated signed-release label rejected.
- Independent clean extraction/reproducibility: see frozen handoff verification receipt.

## Fixed after the previous broad-but-incomplete RC20 fixture checks

- Light mode `#summary-txid` inherited pale-on-light text; scenario output cards contained dark backgrounds with dark text. Now the transaction cards and addresses use consistent themed foreground/surface colors.
- Guide previously inherited pale peach links; `Back to contents`, external references and scenario table headers unreadable. Now legible in light mode.
- Active Help link and open Settings label reintroduced bright orange even after general text fixes; scoped active-state corrections now pass the scan.
- Diagnostics nested action remains inside its Evidence card; no button wrap/overhang at tested sizes.

## Explicit limitations

- Chromium direct `file://` and local HTTP navigation blocked by `net::ERR_BLOCKED_BY_ADMINISTRATOR`; this is a test-environment limitation, not a pass.
- Computed text contrast scanner models composited ancestor background colors; it does not replace a complete external WCAG audit of gradients, animations and assistive technology.
- Valid signature/mismatch/review/incomplete report states after physical device signing, physical camera, mobile browsers, hardware and publisher authentication **not tested**. This report does not certify the verifier or a hardware signer.
- Full historical 139-job campaign not run/ported. Earlier version-locked static failures remain unresolved release qualification blockers.
- Earlier in this effort, selectors and an audit command were accidentally pointed at a previous intermediate HTML; those harness errors were corrected and rerun. The first auxiliary script also used an incorrect QR button selector and sampled a result view before its render settled; corrected independent rerun passed. No application fixes were attributed to harness mistakes.
- No real power loss/reboot/read-only disk/full-disk/network outage/installer/adoption/recovery hardware simulation was performed. These lie outside presentation-only validation.

No source code changes after candidate freeze. Failures and skipped checks are deliberately not represented as passes.
