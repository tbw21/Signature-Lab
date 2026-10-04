# Physical/OS acceptance addendum — v0.18.0-rc1

Use the full retained hardware checklists plus these items, on exact frozen hashes.
This file records planned acceptance, not physical passes.

1. Record signer/firmware authenticity evidence, browser/OS, opening mode and release hashes.
2. Confirm font rendering and enlarged text on actual macOS, Windows, Linux, iOS and Android
   combinations intended for support. system-ui intentionally selects a platform-native face,
   not one universally installed font. No font-download permission is needed.
3. Switch Test/Advanced/Session at the common navigation without unexpected page motion or
   lost controls. Test both wallet lengths, individual/guided/result/review states.
4. On Step1, open Dark Skippy example once. Confirm result appears without Help steps, firmware
   installation or device actions; Close/Escape returns to unchanged test and counts. Repeat
   with a completed result and a halted session. Check browser-native modal focus behavior.
5. Confirm short safety text is understood, no real seed/no funding; same-length wallet reset
   in Advanced explains that session state is cleared. Save evidence before replacing wallets.
6. Test actual SeedQR optical scanning and enlarged QR with both wallet lengths. Font/CSS
   pixel tests do not replace camera tests. Sign and preserve full result evidence, never real funds.
7. Retest permission denial, interrupted scans, locks/background/return and evidence downloads.
8. A hardware blocker requires a new uniquely identified candidate and renewed acceptance.

No camera keepalive, no real-wallet migration, no firmware safety certificate. Publisher signing,
dependency provenance and independent source review/rebuild remain separate requirements.
