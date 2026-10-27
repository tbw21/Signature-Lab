# Signature Lab v0.20.12-rc13 UI repair: frozen scope

## Requirement and acceptance
- The landing heading says "Test your signing device" and explains, in the same short two-sentence introduction, that the tool checks device-returned signatures AND signed transaction details against expected results using a disposable wallet. It must not claim firmware certification.
- Preserve the prominent disposable-wallet protection, exact orange wheel identity, existing SeedQR and manual entry, fingerprint confirmation, verification result and evidence, supported signature policies, guided session, and light/dark toggle.
- The "Deliberate edge case" notice is visible only when the actual current transaction's reactive scenarioId is `boundary`. A normal/custom scenario must not show it. Do not override Alpine's display control using `!important`.
- Help answer content must occupy substantially all of its own accordion width; center the full Help column for comfortable reading rather than leaving 40% of a panel blank. All FAQ ids, headings, groups, and contents navigation remain.
- The settings action uses a simple inline sliders SVG and is aligned to the light/dark icon; the existing Settings drawer and its handlers remain.
- No em dash introduced into user-visible strings.

## Core and boundaries
- Trusted modules: all `src/*` except `src/page.html` and `src/style.css`; `vendor/*`; `build.py`, `archive.py`, and `sources.json`. All must remain byte-identical to RC12.
- Permitted new candidate inputs: `src/page.html`, `src/style.css`, `release.json`, and the corresponding `source-lock.json`; generated expected-output manifest, informational documentation, a scoped UI smoke test, and package manifests.
- There is exactly one Alpine coordinator, one transaction/verification pipeline, one camera lifecycle, one session journal, and one theme state. No new controller, persisted wallet data, network operation, key export, or signing operation.
- The only display state for the edge-case notice is the existing `scenarioId` getter. CSS remains a visual concern.
- Rollback: use untouched RC12 preview bytes. Never mutate a frozen candidate or auto-downgrade an existing test. Reload behavior is unchanged: a new temporary wallet is created in this tab; a return to Home alone does not reset it.
- No installer, privileged component, boot/recovery change, or optional module was introduced. Existing Advanced, Help, Session, QR, file and paste modes are retained.

## Qualification boundary
- RC13 is a **development UI preview**. The full canonical campaign, genuine native `file://` and HTTPS browser-origin acceptance, publisher authentication, independent security audit, signer/hardware acceptance, and release approval are separate and incomplete gates.
- The source and handoff archive must be frozen before any campaign is called release acceptance. Failed gates disqualify those frozen bytes; corrections require a new candidate.
