# Alignment change / regression traceability

| Request | Change | Evidence |
|---|---|---|
| Same right edge in every workspace | Navigation auto-start margin retains trailing edge when stepper is hidden | Seven widths, each Test/Advanced/Session, stable wallet/transaction snapshot |
| Text below words on left | Single seed-instructions block moved below mnemonic list | 12/24 words, normal/expanded, mobile/desktop, doubled text/spacing |
| QR button on right | QR action row outside canvas and quiet zone, at its right edge | Geometry, unique refs, canvas pixel equality and real QR-pixel decoding |
| Consistent related actions | Scoped trailing-edge action rows; responsive full-width mobile remains | Scan/import/paste, PSBT exports, result/evidence and Back controls |
| No reliability regression | All 29 runtime JS units unchanged, original binding set and canvas attrs identical | Static hashes/binding inventories and entire retained software suite |

DOM order of controls is not reversed; no labels/warnings/fields are removed. The decorative
scan icon previously attached to the instruction prose is retired. Semantic instructions
and QR controls each occur once. New seed-layout-expanded uses existing presentation state.
