# RC13 reviewer finding disposition in RC14 draft

| Finding | Disposition | Evidence | Remaining limitation |
|---|---|---|---|
| 1 Light result/transaction text | Remediated visually | Computed Chromium light-theme contrast: result heading, explanation, evidence heading, scenario label >=5.39:1; repeat link and limitation also darkened | Physical signer output rendering not yet tested |
| 2 Match tinted like warning | Remediated | Match uses a restrained green surface; caution amber; mismatch red | Screen-reader result semantics unchanged |
| 3 Misleading UI-only provenance | Documented correctly | RC14 changes template, CSS, build projection, release metadata and tests. RC13/RC14 retain RC13 application JS. Theme storage/step transitions changed before RC13, versus earlier rc3 | Does not imply rc3 and RC14 runtime identical |
| 4 83 old browser/copy jobs | OPEN, not falsely passed | New focused six-condition browser contract plus surviving crypto/BBQr/camera/session runs | Full 139 historical jobs require porting/requalification; historical identity assertions intentionally remain blocked |
| 5 Triple 1-2-3 | Remediated | Removed "What happens next?" sidebar numbering, preserved top stepper and local setup substeps | Side Help card preserved |
| 6 Repeated wallet safety | Remediated | Keep landing safety panel and one setup banner; subtitle and seed instructions focus on actions | No real-wallet usage remains prohibited |
| 7 Stale Help path | Remediated | "Settings, then Session history" | None known |
| 8 Hidden Session/Advanced | Remediated | Visible Settings label, drawer contains full button labels | None known |
| 9 Wrong unsigned claim | Remediated | Compile-time notice derived exclusively from release.json status/authentication | Publisher signature NOT authenticated for this preview |
| 10 Duplicate step-2 headline | Remediated | "Review and sign the test transaction" | None known |
| 11 Official website lost | Remediated | Explicit HTTPS website link in footer, independent of brand/home button | External opening still user initiated |
| Minor MIT spelling | Remediated | MIT license | None |
| Minor arrow spacing | Remediated | Margin between "guide" and arrow | None |
| Minor New test wallet placement | Remediated | Separate row in setup toolbar | At narrow width it returns to left edge and does not overflow |
| Minor fingerprint button wrapping | Remediated | Shorter one-icon action fits single line at 1440px | Narrow view may wrap where needed |
| Minor 390px wordmark wrapping | Remediated | Width-responsive single-line wordmark; tested Chromium 390px | Other fonts/browser engines not fully tested |
