# RC10 UI qualification scope

The original RC9 archive is preserved. New candidate v0.20.12-rc10 changes only the UI template/CSS and release identity inputs.

The original SeedQR canvas, seed generator, cryptographic signing, parsing, scanner, session journal, and exports are unchanged.

Focused checks: 12/12 QR dimension/unchanged-canvas/unchanged-wallet/escape/height-alignment tests; 6/6 multi-page workflow tests (Help, Settings, Session, Advanced, fingerprint gate, malformed import); 62/62 BBQr codec checks. Chromium run uses isolated document content, not native file/HTTPS origins.

The old static test suite reported 27 passes and 16 fails. Some failures stem from historical source projection pinning to v0.20.11-rc3 and previous UI contracts. They are NOT counted as green. Complete canonical qualification is not available on this candidate.

A first broad test used the wrong Help state assertion, then timed out when Help remained visible during Settings navigation; the latter was reproduced as a real UI issue and fixed prior to candidate freeze.
