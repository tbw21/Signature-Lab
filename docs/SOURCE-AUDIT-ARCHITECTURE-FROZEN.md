# Source-audit remediation: requirements and architecture frozen

Scope fixed before implementation, 2026-09-30. Planned release: 0.19.0-rc1.
Baseline: exact 0.18.5-rc2 HTML cea26a18a7ec1cb1250b15193fe9c77f22ad7f328f34501f31c60e2fe2d6b44f;
source ZIP 704262839a8fcbe638d8c211e8f5a2a4364cba4a00d8dc6576390122fe2f2250.
Input audit: 2026-09-21-source-audit-0.18.5-rc2.md,
SHA256 d365f5a0470f03b80bdb31b14aad965236e48793dca22f52f08a566afd427908.

## Requirements / acceptance
A. A uniformly reduced, complete signature envelope may retain only the exact empty-key-data
SIGHASH_ALL field (type 3, 01000000), as the existing addition rule already allows. Both PSBT
versions and partial/final signatures must remain transaction/key/sighash validated by Bp/Rp.
Wrong sighash, malformed keys, missing signatures, unknown additions and selective omissions
must not become clean. Do not add any manufacturer exemption or diagnose missing Foundation files.
B. Retain ordered-field evidence: zero-based before/after positions for every recorded field,
per-map retained-key relative-order observations, a fieldOrderChanged map count, and explicit
comparison basis when version conversion uses a locally reconstructed same-version PSBT.
Compare common-key relative sequences, not raw added-signature membership, to avoid calling
normal additions reordering. Record full positions including added/removed keys. Pure ordering
changes are informational, not proof of leakage or a reason to reject an otherwise valid signature.
An informational line remains in existing returned-file technical details, not a new green badge.
The absence of observed reordering does not exclude other arrangement or hidden channels.
C. One shared outcome function classifies a completed summary as matched (reference match with
expected/unchanged/not-applicable file status), review, or differed. Missing file status is review,
not an invented clean observation. A repeated txid preserves the worst observed outcome:
differed > review > matched; later clean responses cannot erase prior findings. The immutable
journal remains sole state authority; current report projection includes metadata before commit.
Session summary, guided status, exported snapshots and UI use the same outcome rules. Additive
review and count-policy fields explain the changed matched-count semantics. Incomplete attempts
remain outside completed distinct counts and remain separately recorded. Prior files are not migrated.
D. Limit unexpected-field rendering to 32 rows and technical keys to 128 hex characters plus an
ellipsis; key truncation must not create duplicate DOM identities. The full immutable evidence,
counts and warnings are untouched. Explicit shown/total wording explains that Save result contains
all details. Lazy user disclosure is not permission to hide the existence of any finding.
E. Retire automatic browser-agent status registration. No agent API is accessed, no replacement
agent controller/toggle is added. Existing internal inspect() remains for UI/tests. This reduces
an unsolicited surface, but cannot constrain an untrusted browser reading the page.
F. Preserve vendor bytes in this scoped remediation. Record the inert modulepreload polyfill and
Alpine unsafe-eval dependency as deferred vendor-refresh/CSP-build work. Test no modulepreload
links are present and offline CSP is unchanged; do not claim no network primitive in the bundle.
G. Correct the reported geometry harness wait to require a visible nonzero rendered box, without
extending runtime or interaction deadlines. Audit similar box() helpers and change only visible
geometry assertions. Controlled delayed-show and never-visible fixtures must distinguish setup
readiness from actual rendered readiness. Bounded waits are test synchronization, not app retries.
H. Record exact installed qualification Python package versions, transitive dependencies and
native tool versions. An explicit environment stage checks them before candidate tests and reports
missing dependencies as unavailable-environment, not a candidate failure. No automatic installs.
Publish EXPECTED-OUTPUT.json in the source package, outside build inputs, with exact HTML bytes,
hash, build-input identity and version; one offline verifier consumes it. This avoids a self-hash
cycle. The sidecar, source manifest and archive are frozen together before acceptance.
I. Preserve audit-reported upstream differential evidence in DEPENDENCIES.json with attribution,
input-audit hash, no supplied raw corpus, and upstreamAuthenticated=false. Rerun supplied BIP84
vectors locally. Do not relabel report claims as reproduced upstream measurements.

## Architecture, modules, trust and ownership
Trusted core stays: src/04-bitcoin.js and the existing reference self-test, metadata inventory,
prepared test, immutable evidence and TbwSessionJournal. Changes are scoped to metadata policy,
public summary utilities/journal projections, application presentation getters and bootstrap.
No second verifier, parser, journal, nonce source, signing method, state store or retry owner.
Metadata is computed from exact returned bytes only after the established semantic verification.
UI caps are read-only projections, never a limit on what is assessed or exported.
Help, demo, agent capability and evidence display remain optional; their absence cannot weaken
core checks. Agent registration is removed, not moved onto an installation-critical path.
Current permissions/CSP/camera owner/randomness are unchanged. No remote scripts, fonts, network
calls, seed persistence, external account changes, software installation or publisher signing.
Build.py is the sole assembler, archive.py the sole source packer and qualify.py the sole job plan.
The added output-verification operation verifies rather than rebuilding or rewriting artifacts.
No live/public active pointer is changed; the handoff has one unambiguous application at its root.

## State, contracts, recovery, upgrade, retirement
Journal inspect/plan/apply/verify/status/rollback remain authoritative. Pure metadata and summary
functions have deterministic input/output contracts; no artificial mutable controller is added.
All failures remain terminal under existing policy; signature/file finding semantics change only
as specified in A/B/C. No automatic camera reacquisition, retry, downgrade or device approval.
Browser reload starts a fresh disposable wallet. No seed/session crash resume or cross-version
adoption is introduced. Save evidence before closing/replacing wallets. Rollback means opening
an explicitly chosen, reviewed older release in a fresh context; it cannot undo a device signature.
No OS installer, bootloader, Bitcoin/Fulcrum services, storage ownership, or recovery boot exists
in this standalone page, so those hardware/service simulations are not applicable.
Retired: contradictory reduced+sighash exclusion; unchecked order completeness phrasing; optimistic
matched summaries; unlimited metadata DOM projection; unsolicited agent registration; reactive-only
geometry readiness; unidentified environment failure; source-only output-hash ambiguity.
Vendor refresh, CSP framework migration, Taproot, new hardware profiles and UI redesign are deferred.

## Qualification and freeze
First reproduce baseline defects, then unit/contracts/integration/fault tests, exact-HTML browser
simulations (including max hostile fields, delayed visibility, metadata review export), independent
reference/structure calculations, source preservation, lifecycle/reload/rollback and archive tests.
Existing 99-job plan is authoritative; the audit's 83-job count is not assumed to cover it.
Retained tests only change for explicit semantics, version, visibility synchronization and exact
historical source projections. Current-runtime tests always execute new bytes, never projected code.
Freeze uniquely named HTML and source archive plus SHA256 before acceptance. Extract freshly and
rerun ALL canonical jobs. Do not alter source/tests/archive during acceptance. Any blocker creates
another candidate and complete restart. Record failures, discarded runs, timeouts and unavailable
engines separately. Hardware/optics/native browser/OS, publisher authentication, vendor provenance,
independent organizational review and Foundation response investigation remain external gates.
