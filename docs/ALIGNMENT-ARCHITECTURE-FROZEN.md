# 0.16.2-rc1: alignment refinement, architecture frozen before implementation

## Exact basis and scope
Baseline is the published TBW-Signature-Lab-v0.16.1-rc1.html (SHA-256
a8199a60de4268be0fdd0cce68b48264e150ae789759087938c57655558c05f9) and its source ZIP
(2ade8c8453f275585986964ac47414f0a2541ca12988de8fb60c95cf2535d32e).
The user requested consistent right-aligned action groups and instructions left-aligned
under the seed words. No new features, verification rules, camera policies or exports.

## Requirements / acceptance
A1. Workspace navigation remains anchored to the right in Test, Advanced and Session;
    hiding the test-only stepper must not move it to the left. Mobile retains full-width,
    equal-sized usable segments; labels and keyboard order are unchanged.
A2. Seed-loading heading and instructions sit directly below the words, with the same left
    edge. This holds for 12/24 words, narrow screens and QR enlargement. No duplicated copy.
A3. Enlarge/Reduce QR remains next to the QR and aligned with its right edge, outside the
    quiet zone. QR/fingerprint/word state, rendering dimensions and encoding are unchanged.
A4. Panel action rows end at their content area's right edge; buttons may wrap or fill width
    on small screens. Field controls remain associated with their labels. No reversed DOM
    order or indiscriminate floating of every control.
A5. No clipping/overlap/sideways page scrolling at 320, 360, 390, 438, 768 and 1440 CSS px;
    enlarged text and keyboard focus remain visible. Normal/enlarged QR, all three workspaces,
    and result/advanced actions must be exercised.
A6. Every application and vendor JS file is byte-identical to baseline. Only release identity,
    template, stylesheet, documentation and tests/build-test declarations may change.
A7. Full retained applicable suite plus alignment regressions runs on exact frozen bytes.
    Two clean rebuilds reproduce HTML; deterministic repacking reproduces source ZIP.

## Architecture and trust boundary
Existing module boundaries retained. Template/CSS control presentation only. One prepared
transaction, one camera owner, one QR decoder, one verifier, one immutable result, one journal.
Read-only seed loading instructions move in the DOM; canvas and controls keep single refs.
No second controllers, policy copies, key derivation, dependencies or network permissions.
Optional Advanced/Session views remain the existing projections over that authoritative state.

## Ownership, privileges and state
The operator owns the browser tab and controls all camera permission, imports, exports and
signer approval. No additional privilege, installation, storage or outbound connection.
No settings or secrets are persisted. The active HTML is the only active release pointer;
older immutable downloads are archives, never runtime fallbacks. release.json remains the
sole source version; source-lock records authoritative assembly inputs.

## Lifecycle / rollback / recovery
Normal changes of workspace/enlargement only change existing presentation state.
Existing terminal failures, explicit start/end semantics and no auto-reacquisition retained.
Reload starts fresh; Back/Forward must not start capture. Save evidence before closing.
Upgrade/rollback: close current page, open uniquely named immutable HTML, create a fresh
disposable wallet. Browser code cannot undo a signature produced by the device.
OS boot, services, installed-data migration and recovery-boot are not applicable.
Physical power loss, real optics, platform permissions and supported device/browser acceptance
are external gates, not replaced by DOM/synthetic-media tests.

## Explicitly retired presentation
Right-column seed instruction block; seed enlargement control mixed with left-side prose;
workspace strip left-jumping when stepper hides; inconsistent leading-edge action rows.
No cryptographic, import, export or safety rule is retired.

## Candidate discipline
Development is mutable and failures documented. Freeze uniquely identified HTML/source ZIP
and SHA-256 before acceptance. Never patch that candidate during acceptance. A blocker
requires a new identifier and qualification from the beginning. Report tests vs simulations,
unavailable tools/origins, real hardware and external provenance separately.
