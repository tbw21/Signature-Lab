# v0.15.2-rc1 correction matrix

| Finding | Correction | Regression evidence |
|---|---|---|
| Frame exceptions all labelled checksum failure | Separate known Bytewords encoding/checksum rejection from internal decoder faults | Published vector, independent Python/zlib cases, internal-exception injection |
| A single damaged camera observation terminates acquisition | Bounded pre-admission rejection, visible counts; 8 consecutive/24 total cap | No identity/progress mutation, caps, work/text limits, explicit restart; synthetic actual QR pixels |
| Corruption must never be accepted | Complete-message checksum, identity, geometry, duplicate/equation and signature rules unchanged | Retained negative suite plus new camera-context terminal cases |
| Finite paste/file imports must account for all supplied text | No relaxation for finite input; default session remains strict | Corrupt prefix/middle/tail, mixed and conflicting tails |
| Signature-only PSBT reduction creates spurious support-field alarm | Narrow uniform reduced-envelope recognition, successful semantic verification still mandatory | v0/v2 partial/final reduced responses; modified/missing/wrong signatures rejected |
| Unknown/altered fields must not be hidden by cleanup policy | No device-name allowlist, partial reductions and added fields remain review | Global/input/output proprietary markers, wrong output path/script, selective omission |
| Green combined panel for unresolved metadata | Amber overall result plus explanatory heading and tracker notice | UI, keyboard details, immutable report.overallStatus and guided halt |
| Failures not useful for investigation | Public diagnostic export and per-result rejected-frame transport counts | Download success/failure, no raw QR or local seed, record consistency |
| Avoid regression to old attachment | Use latest UX source, preserve unaffected modules and core hashes | Exact baseline rebuild; token-preservation; retained UI/QR/session/regression suites |

The exact user response is unavailable. Structural reduced-response tests are synthetic,
not a finding that every SeedSigner/COLDCARD version emits that shape. This is a field
accounting policy, not proof against metadata-removal choices or other covert channels.
