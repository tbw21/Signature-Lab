# WHAT'S NEW — TBW Signature Lab (cumulative)

**Covers all work from the point I started here: v0.20.4-dev through v0.20.9-dev.**

**Development preview only. Not a release candidate. Not approved for public deployment.**

This is the single cumulative changelog for the development line created during this engagement. It starts from the frozen **v0.20.3-rc1** baseline and records everything added or changed in the later development builds.

---

## v0.20.9-dev — Session and Advanced clarity refinement

**Reason:** User review identified an overly dense Session dashboard and nested, box-heavy Advanced settings, despite prior responsive fixes.

- **Session:** elevated the number of checked transactions, de-emphasized outcome counters, and retained the explicit statement that 20 is a routine rather than a safety threshold.
- Moved the longer explanation of matched/review/incomplete accounting behind a native **How to read this record** disclosure, without dropping the warning that counts are not a safety score.
- Aligned **Save session record** with the evidence tools, replaced the empty-state sentence with a clear path back to Test, and grouped the Finish action with its data-loss warning.
- **Advanced:** removed unnecessary nested card borders and the repeated **Optional** badge, retaining all guided-session, transaction editor, PSBT and device-note controls and their original event handlers.
- Preserved all existing data bindings, output semantics, navigation, evidence capture, Session journal logic and cryptography.
- Recorded the user's report of **30 physical SeedSigner v0.8.7 runs on the earlier supplied build** as separately reported evidence only. Exact outcomes, original binary identity and transport/scenario coverage have not been independently documented; this is not 30 independently witnessed passes or hardware qualification of v0.20.9.

**Qualification:** scoped desktop/mobile controlled Chromium layout and navigation, static trusted-source checks, bounded QR, camera, session and privacy regressions; individual results in qualification report. Native-origin browser and actual hardware acceptance on the exact v0.20.9 bytes remain open.

## v0.20.8-dev — whole-product polish and mobile layout repair

The first genuinely **whole-product** presentation pass, not limited to the Test wallet header.

**Presentation and usability:**
- Fixed a concrete mobile bug: Advanced and Session headings reserved approximately 460px of empty height on narrow screens, pushing their controls out of sight.
- The Test-only three-step progress indicator now disappears when viewing Advanced or Session, reducing duplicate navigation and disabled-step clutter.
- Made headings and spacing consistent across Test wallet, transaction preparation, Results, Advanced, Session, Help, and modal dialogs.
- Tightened the transaction intake panel, QR/import control spacing and alignment of action rows.
- Refined Results hierarchy and restrained the matching-result treatment without changing its meaning; the warning that a match does not rule out seed leakage remains visible.
- Standardized advanced disclosures, editable transaction rows, session-evidence controls, history panels and guided-state spacing.
- Improved mobile and desktop dialog layout, focus visibility, secondary/action button hierarchy and the footer.
- Presented **Finish and clear this tab** as a distinct, subdued destructive confirmation rather than a bright primary call-to-action.
- Simplified the Results and transaction headings (presentation copy only).
- Repaired a malformed self-closing syntax fragment in the optional firmware-version input without changing its value bindings or cooperative privacy attributes.

**Verification completed:** bounded offline Chromium UI matrix at 320/360/390/768/1024/1440px, interactions on Test/Advanced/Session, dialogs, real-vs-disposable wallet warnings, synthetic success/incomplete flows and controlled archive checks. See `QUALIFICATION-REPORT.md` for exact counts, interrupted tests and limitations; no real signer tested.

**Source boundary:** only `src/page.html`, `src/style.css` and `release.json` changed among build inputs relative to v0.20.7-dev. Verifier, cryptography, camera, QR, state coordinator and session journal source units remain byte-identical. A version-aware presentation regression test was updated for the current accurate wallet-scope wording, retaining its semantic safety intent.

## v0.20.7-dev — shared UI polish extended into Advanced and Session

This version completes the next stage of the premium-interface pass.

### What changed
- Extended the refined visual hierarchy beyond the opening Test workspace into:
  - **Advanced**
  - **Session**
  - shared notices / callouts used across the page.
- Reworked the **Advanced tools** section so it now has a cleaner heading structure, calmer spacing, and more deliberate card presentation.
- Reworked the **Session record** section so it now matches the same product language as Test, with improved heading hierarchy, cleaner overview cards, and more polished history/evidence presentation.
- Refined the shared callout treatment used for:
  - the disposable-wallet warning,
  - nondefault-settings notices,
  - and related in-page alert/status blocks.
- Softened boxed warning styles into a subtler, more premium left-accent treatment.
- Tightened spacing, borders, and container hierarchy across details panels, overview cards, and session/history blocks.
- Improved consistency between desktop and mobile layouts for Test, Advanced, and Session.

### Controlled verification completed for this pass
- Exact output verified against `EXPECTED-OUTPUT.json`.
- Controlled Chromium UI smoke check passed for **desktop and mobile** across:
  - Test,
  - Advanced,
  - Session.
- Checks passed:
  - application ready,
  - target section visible after navigation,
  - no horizontal overflow,
  - no runtime errors,
  - no network requests.

---

## v0.20.6-dev — visual refinement and hierarchy cleanup

This version focused on the **feel** of the interface rather than new trust or cryptographic behavior.

### What changed
- Simplified the visual hierarchy at the top of the Test workspace so the page feels calmer and more premium.
- Reduced the sense of clutter by separating **primary**, **secondary**, and **contextual** information more clearly.
- Reworked the Test wallet header so it now presents:
  - the main title,
  - the supported scope,
  - the safety warning,
  - and the Dark Skippy example
  with less competition for attention.
- Restyled the warning block so it remains clear without feeling noisy or heavy.
- Tightened spacing and alignment across the opening panel, especially the header region and seed controls row.
- Softened the chrome on the progress stepper and workspace navigation so they support the task without dominating it.
- Improved mobile reflow so the opening screen feels more intentional rather than compressed.

---

## v0.20.5-dev — release-status truthfulness correction

This version corrected a trust problem in the interface and help copy.

### What changed
- Replaced misleading **release-candidate** wording with accurate **development preview** wording.
- Updated the visible release label, help copy, and accessibility text so the build no longer overstates its status.
- Clarified that public deployment is **not approved**, hardware acceptance remains pending, and the build is not a completed release.

### Why it mattered
A tool like this must be trustworthy not only in behavior, but also in how honestly it describes its own state. Overstating release status weakens trust.

---

## v0.20.4-dev — privacy, safety and usability improvements

This was the first development version created during this work.

### What changed
1. **Safer first-run flow**
   - Starts with a straightforward, smaller transaction path instead of opening with a more complex case.

2. **Stronger safety guardrails**
   - Clear warning not to enter a real seed.
   - Clear warning not to overwrite an existing real wallet on the signer.
   - Clear warning not to send bitcoin to the disposable wallet.
   - Scope disclosed as BIP84 native SegWit single-signature ECDSA testing only.

3. **Earlier evidence-retention choice**
   - Added an optional, bounded evidence-retention choice before the first signed-response intake.
   - Remains off by default.

4. **Cooperative browser privacy controls**
   - Added opt-outs for text-assistance features such as spellcheck, autocomplete and related helpers on editable fields.
   - Extended those protections to dynamically created fields.

5. **Translation protection**
   - Added `translate="no"` where appropriate for seed words and technical identifiers.

6. **Explicit Finish testing flow**
   - Added a distinct lifecycle action for finishing testing, separate from ending a guided session.
   - Stops capture and retires app-owned session/test state while honestly avoiding impossible claims about guaranteed browser/OS memory erasure.

---

## What has not changed across this development line

- No claim that a matching result proves firmware is safe.
- No independent signer-firmware certification.
- No new cryptographic engine, alternate verification engine, hidden network service, or background upload path.
- No publication to production website or GitHub release channel as an approved public release.
- No claim of completed hardware acceptance, real mobile browser acceptance, publisher-authenticated release signing, dependency-authenticity closure, or independent external security review.

---

## Current state of the development line

- **Status:** development preview only.
- **Public release status:** blocked.
- **Trust posture:** improved.
- **Visual quality:** opening screen refined in v0.20.6-dev, Advanced/Session included in v0.20.7-dev, and whole-product/mobile layout repaired in v0.20.8-dev.
- **Qualification posture:** still incomplete for public release.

This cumulative changelog is descriptive. It is **not** a security certificate, release approval, or hardware-acceptance record.
