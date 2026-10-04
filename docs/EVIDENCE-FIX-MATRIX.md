# Evidence upgrade requirements and evidence map

| Requirement | Implementation | Qualification |
|---|---|---|
| Preserve previous signed responses without a new journal | Optional attachments in session-journal.js | evidence-retention, evidence-browser |
| Bound data, no silent eviction, honest gaps | 16 MiB / 256 attachments, terminal fault; optional 256 capture slots | limit/failure tests; replay tampering |
| Keep main design and core verifier unchanged | Session disclosure and shared notice only | evidence-static, retained UI/crypto |
| Diagnostic-only default, explicit original-response choice | allowlisted coordinator projection, existing saver | privacy and browser-download tests |
| Independent file-policy replay | existing tools/replay_evidence.py, v3-only original-byte reconstruction | metadata-fixtures and metadata-replay |
| Actual available-browser critical workflow | existing tests/origins.py, file and loopback navigation | separate passed/failed/unavailable rows |
| Prove selected defects are caught | isolated temporary source mutants and clean controls | deliberate-defects.cjs |
| Avoid camera telemetry blocking core records | 256 optional slots independent of 2000 core slot budget | capture capacity and event tests |
| Dependent-source refresh | investigated, not implemented; no vendor edit | DEPENDENCY-REFRESH-GATE.md |

All tests are software/synthetic unless explicitly marked hardware evidence. Independent Python code is
implementation diversity, not independent organizational approval. Read exact run reports, not this map,
for completed counts. No extra passed case is inferred from a fixture, screenshot or subassertion.
