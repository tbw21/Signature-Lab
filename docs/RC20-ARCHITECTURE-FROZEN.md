# RC20 architecture freeze — light-contrast and containment repair

Baseline: frozen RC19 handoff. The RC19 archive is unchanged; RC20 is a new candidate.

## Acceptance criteria
- In light mode, both specified FAQ links, session status text, and landing step numerals have a measured contrast ratio >= 4.5:1 against their actual rendered surface.
- The result Evidence/Diagnostics and Session Evidence download buttons must remain fully inside their respective cards at 390, 768 and 1440 px in dark and light.
- Dark theme visual intent, orange primary CTA and borders, native disclosures, and all feature handlers remain intact.
- No new controller, storage, retry, privilege or network access.

## Ownership and state
- Trusted core: original RC19 single application coordinator, 29 unmodified JavaScript modules, wallet/Bitcoin verifier, camera, QR codecs and session journal.
- Presentation: `src/style.css` is the only modified UI implementation source. Light text ink is `#824600`; fill/border orange remains `#EB8404`.
- Authoritative state: the existing Alpine state and native `<details>` elements. No separate state owner.
- Optional evidence exports remain under their original handlers; the CSS only contains the button action row.

## Lifecycle and rollback
- Reboot/resume/recovery: not a boot-installed service; page reload retains existing RC19 behavior and clears the disposable tab session as documented.
- Rollback: reopen untouched RC19. Upgrade: replace the standalone HTML, with no data migration or new persistent authority.
- Retired alternatives: no RC18 standalone override is a release source; no duplicate theme controller added.

## Qualification boundaries
Static compilation, unit-identity comparison, targeted CSS/DOM browser scenarios, deterministic rebuilding, source-lock faults and archive integrity are eligible scoped checks. Real `file://` Chromium navigation is blocked by environment administrator policy. Full canonical 139-job campaign, complete device hardware testing and publisher authentication are unperformed. This cannot be called public-release qualified.
