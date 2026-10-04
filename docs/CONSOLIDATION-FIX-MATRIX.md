# Consolidation: requirements, changes and evidence

The frozen design is `CONSOLIDATION-ARCHITECTURE.md`. This matrix describes implemented
software, not hardware compatibility or completion of external trust gates.

| Requirement | Implementation | Regression evidence |
|---|---|---|
| C1: consolidate fingerprint and v0.14 | Cached-root, guarded eight-hex fingerprint; SeedQR readiness request identity; seed-page and persistent session displays | Independent BIP32/OpenSSL vectors, leading zero, actual QR pixel decoding, invalid/destroyed/changed wallet, legacy verifier/camera/QR suites |
| C2: optional fixed plan | Bounded 1-200 case planner, 20/50/100 shortcuts, existing generator, six balanced types, immutable public plan/hash | Every count boundary, 20/50/100/200 shapes, uniqueness, safe rejection on generator failure, no signing/camera activation |
| C3: physical approval and explicit transitions | No simulator, no firmware upload, no automatic Next/Start/retry | Browser actions and repeated Start/Next tests, camera inactivity checks; actual approvals remain a physical gate |
| C4: current-case binding and halt | Binding includes full root public key, wallet-session ID, PSBT version, policy, case hash and number; failures stop progression | Other-case imports, changed state, signature-policy difference, incomplete data, metadata warning, capture errors, late file and explicit End |
| C5: one historical owner | One private journal; old unique tally is a read-only cached projection; current result remains immutable | Sticky differences, duplicate intake, bounded history, optional planner absence, no writable sessionChecks path |
| C6: useful public report | Fixed public plan plus per-case summaries, counts, reasons and build identity; no local secrets | Independent plan-hash check, schema/public allowlist, snapshots, download error; session report explicitly not a whole-run raw replay archive |
| C7: lifecycle and manual retention | Locked planning, explicit advance/end, manual mode before/after, reset/new wallet, no automatic restoration actions | Cancelled/late files/camera, Back/Forward restore, post-End history, refusal reason, no silent plan reuse |
| C8: coherent accessible layout | Existing segmented controls, native labeled buttons/number field, collapsible plan, main fingerprint, sticky status | Chromium 320/360/768/1440 widths and QR quiet-zone checks; actual optics/usability remain unmeasured |

The baseline v0.14 audit corrections, separate metadata status, immutable current reports,
public per-result evidence, prepared cache, fixed-method choice and source-assembly build
are retained. Their earlier traceability matrix remains in `FIX-MATRIX.md` as baseline
history; the full applicable regression suite is rerun on the new candidate.

## Explicitly not delivered as completed facts

- Actual physical signer, real optical scan or measured time-saving results.
- Independently certified signer/firmware profiles. The existing explicit method choice
  remains available, without device-name inference.
- Repeat-signing diagnostics, QR density/speed tuning or new script/signature families.
- Firmware upload or consumer simulation mode.
- Trusted publisher signing, authenticated complete upstream dependency provenance,
  external organizational source review or independent release reproduction.

These are recorded external gates/deferred work, not silently treated as software passes.
