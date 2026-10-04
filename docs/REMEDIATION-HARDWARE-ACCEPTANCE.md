# v0.15.2-rc1: SS/CCQ physical acceptance

Software and physical acceptance are distinct. Record the exact HTML and archive SHA-256,
OS/browser/version/origin, device model/hardware/firmware and how firmware authenticity
was checked. Publisher authentication is still pending; never infer it from unsigned hashes.
Use only a fresh disposable test wallet and a supported temporary-wallet/spare-device flow.
Never weaken device checks, overwrite a funded wallet, fund test addresses or broadcast.

## Start with the two reported issues
1. Open the exact frozen candidate, load a disposable wallet on SS 0.8.7, compare the
   fingerprint and sign one ordinary native-SegWit test. Save the original returned PSBT
   and per-result evidence before changing the test. Record file-format assessment and
   every listed field change. A different metadata finding is not silently ignored.
2. Scan that same signed response in ordinary lighting and usable brightness. Record
   capture time, rejected-observation count and exact outcome. If it stops, save scan
   diagnostics and keep the same response. A video of the signed response (not seed QR)
   can support offline reproduction. The new behavior has not yet been optically qualified.
3. Test the corresponding physical workflow separately on the COLDCARD Q firmware actually
   in use. Record supported outgoing/return QR formats, not presumed compatibility.
4. Run 3-6 individual/guided transactions first, then the agreed longer session. A count
   is an operational test target, never a firmware safety threshold. A signature match with
   unexplained returned fields is not a clean overall finding and must stop guided progress.

## Required behavior
- Expected complete signature-only reduction is neutral and retains removal records in
  evidence. Unknown/altered/selectively removed fields stay visible and amber on a match.
- One invalid camera observation is counted, excluded and does not erase valid progress.
  Stop at 8 consecutive/24 total known frame rejections or the existing deadline. No
  complete-message checksum, signature, identity or resource validation is bypassed.
- Stop/restart is explicit. Late responses must not alter another test. No camera restarts
  on its own. Finite imports containing corrupt content must remain rejected.
- Review the exact transaction, wallet and absolute fee on the physical signer.
- Keep diagnostic failures separate from signature findings. A successful fresh scan
  does not erase the fact that an earlier scan failed.

Use the retained docs/HARDWARE-ACCEPTANCE.md for interruption, file/report export, refusal,
permission, screen lock, backgrounding, browser, layout, user-comprehension and rollback
coverage. Save per-result evidence before advancing; session summaries are not complete
archives of original responses. A blocker disqualifies the candidate; change a new candidate
and restart qualification. No physical pass is claimed in this document.
