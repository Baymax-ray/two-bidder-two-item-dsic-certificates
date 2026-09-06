# Second corrected portable replay

Author-side validation; this is not an independent reviewer report.

**Result: PASS**

- Exit code: 0.
- Elapsed: 604.843 seconds.
- Completed entrypoints: 46/46; expected sequence matches: True.
- Final marker observed: True (`COORDINATED_PRIMAL_DUAL_CERTIFICATE_PASS 46 entrypoints`).
- Package source identity: 162 files before / 162 after; unchanged: True.
- Final bound source/dependency identities: PASS.
- Independent exact endpoint reconciliation: PASS.
- Separate stdout and stderr are retained; stderr empty: True.
- UTC interval: 2026-09-06T06:47:36.225930+00:00 to 2026-09-06T06:57:41.169891+00:00.
- Distinct temporary root: `C:\Users\FangJ\AppData\Local\Temp\dsic-second-corrected-803724c3`.
- Process-specific TEMP/TMP used a distinct ordinary short temporary root; the global environment was unchanged.

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

The initial launch is preserved in `attempt1_environment_failure/`: it stopped before entrypoint 1 with Windows error 267 because the staged working directory was too long. The corrected run above used a short ordinary temporary root and passed all 46 entrypoints without changes to proof sources.

Observed fresh staged mirror: `C:\Users\FangJ\AppData\Local\Temp\dsic-second-corrected-803724c3\dsic-pair-kt_as0b8`.
