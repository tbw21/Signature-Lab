# RC30 scoped retirement — DEVELOPMENT ONLY

## Freeze and acceptance contract

* Baseline: immutable RC28 standalone HTML and original source, overlaid with reviewed RC29 test-only migration. Historical evidence must remain byte-identical.
* Single coordinator: existing `src/20-application.js` and existing `openWorkspace`; no second router or ledger.
* Authoritative state: existing application state, `release.json` for release status, `source-lock.json` for build inputs, `EXPECTED-OUTPUT.json` for built HTML identity.
* Privilege: offline browser page, no new persistence, network permission or elevated capabilities. Optional Help/Advanced/Session continue through the existing coordinator.
* Lifecycle: reload starts a fresh disposable wallet. No automatic retries, upgrades, background tasks, new boot/recovery paths, or device-signing assumptions. Rollback to a *separately approved, hash-verified* candidate only.
* Explicit retirement: the permanently hidden `nav.workspace-nav` Test/Advanced/Session buttons, the hidden `workspace-alert` badge and their CSS. Do not remove session-state alerts still shown in the visible tracker and session page.
* Focus recovery: after ending a guided session, focus the visible `#tbw-settings > summary` rather than the retired hidden `sessionNav` control.

## Release criteria

1. Build locked from the 29 original module paths; 28 runtime/vendor units must remain byte-identical to RC28, with the one-line focus change in `src/20-application.js` separately reviewed.
2. Remove the dead navigation only when the visible Settings drawer still reaches Advanced and Session and the Back to test control returns properly across 320/390/1440 widths.
3. No lost camera, evidence, signing, wallet, QR or privacy capability; check app-state stability, absence of network requests, CSP, and no error messages.
4. Preserve original historical tests as evidence. Migrate direct obsolete selector expectations to visible controls without deleting security assertions.
5. Verify CSS grammar, JS syntax, source locks, manifest, clean rebuild and tamper rejection. Full canonical 139-job campaign and native/hardware/publisher acceptance still required for release.

## Historical material not eligible for deletion

The nested `source/` snapshot, frozen historical fixtures, baseline HTML, past qualification reports and old pinned test scripts are **evidence**, not active runtime modules. Removing them from provenance would undermine earlier conclusions. Archive separately only after every archived hash, document reference and release contract has been requalified. Do not remove signing, Bitcoin, import, QR, camera or vendor modules without executable reachability and failure-path evidence.

## Qualification grade

DEVELOPMENT / NO-GO. This scope does not attest hardware, publisher signing, or a complete 139-job run.
