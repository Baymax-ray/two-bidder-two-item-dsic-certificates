# Second corrected portable replay

Author-side validation; this is not an independent reviewer report.

**Result: FAIL**

- Exit code: 1.
- Elapsed: 0.628 seconds.
- Completed entrypoints: 0/46; expected sequence matches: False.
- Final marker observed: False (`COORDINATED_PRIMAL_DUAL_CERTIFICATE_PASS 46 entrypoints`).
- Package source identity: 162 files before / 162 after; unchanged: True.
- Final bound source/dependency identities: PASS.
- Independent exact endpoint reconciliation: PASS.
- Separate stdout and stderr are retained; stderr empty: False.
- UTC interval: 2026-09-06T06:45:42.445915+00:00 to 2026-09-06T06:45:43.152378+00:00.
- Distinct temporary root: `D:\文档\ChatGPT\AI4MATH\output\output\two_bidder_two_item_full_dsic_exact_auction\V4_6_1_1_V4_6_2_archive_audit\second_corrected_replay\temp_root_20260906T064542_b1ed6fd7`.
- Process-specific TEMP/TMP used Windows extended paths; the global environment was unchanged.

## Endpoint reconciliation

- lower_enclosure: [0.876464164471798049944906113027, 0.876464164471798049944906113028].
- upper_enclosure: [0.882923053258716969260626799854, 0.882923053258716969260626799855].
- gap_enclosure: [0.006458888786918919315720686827, 0.006458888786918919315720686828].
- ratio_enclosure: [0.992684652685100617902519468374, 0.992684652685100617902519468375].
- Strict gap < 1/100 and ratio > 992684/1000000: PASS.
- The radical bounds were recomputed with integer square roots and exact rational arithmetic at 60 decimal places.

## Source identity

- Wrapper SHA-256 before and after: `c105843778d48cb59e27901351fabbd55f3197ec6fcb635717dc083970e3331f` / `c105843778d48cb59e27901351fabbd55f3197ec6fcb635717dc083970e3331f`.
- Manifest SHA-256 before and after: `06a44df714427fa269e2acbd0c31b9f78d48dea9ff91e3909a2b39124fda4303` / `06a44df714427fa269e2acbd0c31b9f78d48dea9ff91e3909a2b39124fda4303`.
- Full inventories: `before_sha256.json`, `after_sha256.json`, `before_SHA256SUMS`, `after_SHA256SUMS`.
- Run evidence: `environment.json`, `stdout.txt`, `stderr.txt`, `validation_report.json`.

Validation establishes this finite frozen certificate replay and stated endpoint bracket; it does not establish optimality, convergence, or hypotheses beyond those of the certificate.
