# Development record: v0.15.2-rc1

## Baseline and diagnosis
The supplied UX source archive rebuilt dev-2.html exactly. Prior release files were not
changed. The current v0.12.2 attachment was not used as the implementation baseline.
The original failing QR response and original metadata-bearing response were unavailable.
A synthetic, correctly signed, uniformly reduced PSBT reproduced a metadata warning; a
corrupt Bytewords observation reproduced immediate scan termination. The standard
Bytewords vector passed and 300 exploratory valid transport round trips did not reproduce
a deterministic valid-data decoder failure. These are experiments, not hardware acceptance.

## Recorded harness corrections (not candidate acceptance)
1. An identity-mutation fixture used signed JavaScript XOR for a CRC with its high bit set.
   It hit the header bounds before the intended identity check. Unsigned coercion corrected
   the fixture; the identity check then passed.
2. A Playwright injection returned an assigned function, which Playwright invoked instead
   of merely installing the fault. Wrapping installation and returning true corrected it.
3. The new reduced-PSBT browser helper initially assumed the fixed two-input fixture.
   Guided planning creates a new transaction with its own counts. The helper now reads
   the PSBT's actual input count. No runtime exception was relaxed for these corrections.
All original failing test reports are retained in separate development evidence.

## Incomplete execution records
A combined static/core/independent command exceeded its 120-second external window during
core range 21-40. A second combined core-stage command exceeded its 240-second window in
range 41-54. A combined browser command completed range 21-40 but exceeded 120 seconds
inside range 41-62. These partial executions are not acceptance passes. Complete disjoint
ranges were rerun in bounded commands. Qualification gained an explicit one-job option;
its receipts distinguish job completion from full-stage completion and never replace
previous output. There are no automatic retries.

## Scope choices and caveats
Checksum-invalid camera observations may be excluded only before admission and within
the frozen limits. Failed complete transfers, conflicting valid data and internal decoder
faults remain terminal. The new UI does not label metadata universally harmless. The
current review notice is repeated near signature counts so those counts cannot conceal
an unresolved file finding. No source/dependency update, new signer, firmware simulation,
real-wallet procedure or expanded cryptographic scope was introduced.

## Outside-source access
Public Bytewords/BIP174 specifications were consulted. SeedSigner development signing code
shows a trimming step, but exact 0.8.7 trimming-source retrieval and container network
requests were unavailable. No exact-version behavior is claimed from that development
source. Independent fixtures implement generic stated framing and reduced-file rules.

## Completed development disposition
532 named checks passed in the selected completed runs. Four origin/browser checks were
unavailable, not passed. The selected runs and hashes are listed in the accompanying
summary. Duplicated reruns, partial executions, fixture generation and ad-hoc job-driver
checks are not added to that total. The added long-amber-header checks passed at 320 and
1440 px with the taller tracker, supplementing the existing focus/reflow tests.
The final acceptance run must start from a fresh, frozen archive and keep all earlier
acceptance artifacts unchanged. Source templates and runtime modules are now stable.
