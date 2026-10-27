# RC11 UI qualification and frozen design boundary

- Baseline: v0.20.12-rc10; presentation-only changes to the HTML template, CSS, release identity, and source lock.
- Trusted core remains the same: source files for wallet generation, session journal, crypto, PSBT, QR encoding, camera and verifier are unchanged.
- One theme preference source (`themeMode` and `setThemePreference`) powers the new header control; removing its duplicate from Settings does not create a second controller.
- Light Mode fixes unify Session, Advanced, Help, and result panels, including footer links and low-contrast labels.
- Browser qualification: six setup/Session/Advanced cases passed at 390/768/1440px in both themes, and six more Help/Results cases passed at the same widths.
- Focused Light Mode contrast scanner sampled text from setup, Session, and Advanced; 0 under-4.5:1 findings for Session and Advanced at 390/1440 after correction. One CSS color(srgb) parse limitation remained for the selected 12-word button, but the actual visual styling is dark text on a pale surface.
- Browser verification used isolated offline Chromium document contexts. Actual file://, HTTPS hosting and hardware tests are not established. Legacy RC10 static results included 16 failures; full canonical run is not complete here. No claiming release-readiness.
- No em dashes were introduced in the revised labels.
- Rollback: abandon RC11 and use the preserved RC10 or signed RC3 as appropriate. No state migration, no privileges, no automatic retries.
