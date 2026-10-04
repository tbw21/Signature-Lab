> Historical v0.14 record. For the consolidated candidate, apply
> CONSOLIDATION-ARCHITECTURE.md and CONSOLIDATION-FIX-MATRIX.md.

# Clarification before qualification
2026-09-15. Q2 normal-origin startup must not depend on a test-only randomUUID shim. Session identifiers now use RFC4122 UUIDv4 layout filled solely by browser getRandomValues, already required by seed generation. No insecure random fallback. Missing/failed secure randomness is terminal. This is a session identifier, not a new entropy source or device attestation. Regression: missing randomUUID works; missing/failed getRandomValues cannot create a wallet.
