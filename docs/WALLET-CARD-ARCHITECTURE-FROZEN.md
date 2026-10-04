# Wallet confirmation card — architecture and acceptance frozen

Scope frozen before implementation on 18 September 2026. New candidate: 0.18.1-rc1.
Baseline: conversation-supplied clarity-work/dev-4.html and dev-4-source.zip, not v0.12.
The baseline archive's 174 manifest entries and CRCs passed; rebuilding reproduced the exact
supplied development HTML (b0489bd6d5ebbdf56d9377cc3892ea2bc9fda4120058d4e8b2dca10a6e241ba1).
That development snapshot had not completed full release acceptance. This run must include its
entire retained qualification suite and investigate/adapt only genuinely superseded UI assertions.

## Requirements and acceptance criteria
W01 Keep existing words and QR in the one wallet panel. One compact confirmation card within that
panel groups the existing live wallet fingerprint, comparison reminder and both existing actions.
No duplication of words, canvas, fingerprint value, state, or wallet-loaded button.
W02 Enlarge/Reduce QR is secondary; Test wallet loaded is a separate primary action. Both stay in
one trailing-edge action row that wraps naturally. No single button performs both operations.
W03 Remove the former isolated bordered fingerprint box, separate enlargement row and full-width
acknowledgement footer. One border and consistent spacing replace those three fragments.
W04 Preserve all existing runtime JavaScript byte-for-byte. No signing, generation, reference gate,
QR, camera, metadata, evidence, journal, failure/retry, workspace or optional example logic changes.
The same fingerprint binding/leading-zero/unavailable handling and acknowledgement guard apply.
Do not hide true warnings or change policy. Presentation review includes Test/Advanced/Session/Help.
W05 Inspect related action alignment, spacing and responsive behavior. Correct only reproduced,
closely related layout issues, with a reason and regression test. No unrelated features or libraries.
W06 Layout tests: 320/360/390/438/768/1024/1440px; 12/24 words; enlarged/reduced QR; doubled text;
increased spacing; keyboard; forced colors; native modal; no overlaps/overflow or cropped warnings.
Check the seed QR decodes before/after CSS enlargement with identical pixels and unchanged wallet,
transaction, policy and journal. Verify card identity/actions remain local, accessible and unique.
W07 Complete retained static/syntax, unit/contract, cross-module, fault, browser/simulation,
independent oracle, packaging/reproducibility tests. All new named checks use actual candidate bytes.
Historical source projections test only explicitly allowed changes, not runtime execution.

## Architecture, trust boundary, ownership and privileges
Only the page template and stylesheet are eligible runtime presentation changes. Existing Fv,
reference gate, prepared test, immutable result and TbwSessionJournal stay authoritative.
The same local browser sandbox/CSP applies; no new permissions, fonts, network, persistence,
controllers, retry engines or data sources. Optional Help/demo cannot mutate the critical path.
No new component or new state contract is introduced. Existing inspect/plan/apply/verify/status/
rollback contracts and terminal failure behavior stay unchanged. Existing explicit user actions
call the existing implementation; CSS enlargement is not wallet acknowledgement.

## Recovery, upgrade and retirement
Seed and session stay in memory only. Save evidence before reloading or changing versions. Reload
begins a new page lifetime; no crash-resume or secret migration is added. Rollback opens the old
unchanged HTML in a new context and cannot undo a physical signature. No OS installer, bootloader,
Bitcoin/Fulcrum services or disk migration exists; those hardware boot cases are not applicable.
Retire the detached wallet footer and nested fingerprint border, not their information or controls.

## Release process and open gates
Record every changed file. Development can change unfrozen inputs with a logged reason and test.
Before acceptance freeze HTML and source archive hashes, then clean-extract and run all tests.
Any acceptance blocker disqualifies those bytes; changes require a new candidate and fresh run.
No automatic retries. Record failures, exclusions and unavailable modes separately. Repeat builds
and archive recreation must be exact. Tests that require real media/hardware are not simulated passes.
Physical signer/optical/native Mac/Windows/mobile acceptance, publisher signing, inherited dependency
authentication, outside review and original Foundation findings remain open. No firmware certificate
or quantified detection reliability is claimed. Broad trust review is not part of this layout fix.
