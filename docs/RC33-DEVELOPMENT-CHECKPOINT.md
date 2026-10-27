# Signature Lab RC33 — development qualification checkpoint

22 October 2026. **GRADE: DEVELOPMENT / NO-GO. NO RELEASE CANDIDATE FROZEN.**

## Frozen architecture and scope

- RC32 baseline remains immutable (outer SHA-256 `123137d4f937b3f54cfc015d68664a801a2456ab9649b1595e07b1cf14087568`).
- Authoritative runtime remains one application coordinator, one session journal, unchanged original Bitcoin/signature/QR/camera modules; all 29 build-time JS/vendor units are byte-identical to RC32.
- RC33 application changes: exactly one safety-scoped stylesheet rule correcting priority between a premium grid `display:grid!important` and Alpine `x-show` `display:none`. `release.json`, source lock and expected-output identity are updated to **0.20.12-rc33**, publisher unauthenticated.
- Test changes: migrated visible navigation in UX/Calm browser tests; retained checks for signing warnings, camera, export, file review, bad locktime, 20 outputs and session-history review. Historical RC32 test/CSS bytes and an exact CSS-provenance record are preserved in `fixtures/rc33-historical/`.
- No storage, boot, network services, retries, backends, Bitcoin, signer, QR codec or session-state algorithms changed. No historical case was deleted from the canonical 139-job inventory.

## Critical fix

RC32 incorrectly displayed `.sign-layout` even when `transactionReady == false` and Alpine added `style="display: none;"`. A high-specificity `#test-view .sign-layout{display:grid!important}` overrode that style. RC33's exact rule `#test-view .sign-layout[style*="display: none"]{display:none!important}` restores required hiding. Browser tests verify invalid transaction: error visible, stale QR/summary hidden; valid transaction: signing layout visible. Deliberate deletion of this rule reproduces the unsafe condition.

## Verified development preflight

- Exact RC33 source lock and standalone HTML expected-output sidecar: PASS. HTML SHA-256 `d8b6fbf7c8d675d90a064fff19ea4853c490ea057f1ad7a288c4ac097c783f80`, 1,403,037 bytes.
- Current release contract **10/10** and current assurance **16/16**, including source/provenance mutation rejection: PASS.
- Targeted RC33 signing-layout safety/positive/negative mutation **3/3**: PASS.
- UX browser suite **48/48 individual cases** with completed receipts in bounded development groups: PASS.
- Calm browser suite **31/32** cases passed, **case 28 failed** on font/padding/minimum-height equality for the QR-format and recovery-word segmented controls. Do not waive or count as passed.
- Alignment browser **7/22** passed; remaining 15 not tested in RC33 preflight.
- Feedback browser **7/29** passed; remaining 22 not tested in RC33 preflight. The first 1–7 batch was interrupted after six passes, and case 7 was executed separately with a complete passing receipt. Both records are retained.
- Native file:// and loopback HTTP were unavailable in the earlier environment; neither is qualified here. Real camera optics/signers, publisher authentication, hardware, full 139-job suite, clean-install/adoption/upgrade/recovery acceptance: NOT RUN.

## Release policy

This ZIP is a **development snapshot**. It must never be relabeled as 139/139 qualified or publisher-authenticated. The current Calm styling failure is a real outstanding contract; correct or formally review it in a **new development revision** with a regression test. Then finish the other preflight families. Only after preflight is green: freeze a new immutable acceptance candidate, record its SHA-256, run all 139 canonical jobs via the durable external controller from Job 1; a blocker disqualifies that candidate. Publisher verification and physical hardware gates remain separate.

## Checkpoint ledger

- Architecture frozen for RC33 scope: YES.
- Implementation complete for the targeted safety repair: YES.
- Static and source security validation: PASS for recorded subsets.
- Targeted fault injection: 3/3 PASS.
- Browser simulation: UX 48/48; Calm 31/32 with 1 FAIL; Alignment 7/22; Feedback 7/29.
- Candidate bytes frozen: NO acceptance candidate. Development ZIP frozen only after reproducible archive verification.
- Hardware acceptance ready: NO. Hardware acceptance completed: NO.
