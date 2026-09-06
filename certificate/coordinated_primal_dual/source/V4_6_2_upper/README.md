# V4.6.2 — upper-bound branch

**New unrestricted upper bound: OPT <= 0.882923053259.**
The exact unrounded rational certificate is approximately
0.8829230532587169692606. The parallel V4.6.1 lower branch now gives revenue
approximately 0.8764556138363258521462, leaving a combined gap of about
0.0064674394223911. The gap remains open. The frozen upper ledger retains
its original V4.6 comparison; the current comparison is in
[the cross-branch certificate](certificate/current_bound_comparison.json).

Read [REPORT.md](REPORT.md) for the result, exact decomposition, remaining
obstructions, and limitations. The [upper ledger](certificate/upper_ledger.json)
contains 16 strictly decreasing rational upper certificates.

The three contributions are:

1. [Continuous Bernstein majorant](flow_proof.md), independently replayed
   through all 1,351,220 depth-20 tree nodes.
2. [Reusable conditional screening support](research_log/conditional_global_splice.md),
   converted to a common whole-auction capacity measure.
3. [Sparse long-range IC cycles](research_log/sparse_cycle.md), with exact
   continuous-envelope descent on complete report boxes.

The final [combined certificate](research_log/combined_certificate.md)
solves both unrestricted charged screening problems at zero and displays
all four gap components. It does not match the lower mechanism.

From the auction output directory:

```powershell
python -B -X utf8 V4_6_2_upper/verifier/run_all.py
python -B -X utf8 V4_6_2_upper/verifier/verify_manifest.py
```

The default full replay includes two deep integrations and takes several
minutes. `--skip-deep` runs the other exact checks, explicitly reporting
that the two deep integrations were skipped in that invocation. Default
verifiers are read-only; `--write` is reserved for certificate generation.
See [VERIFICATION.md](VERIFICATION.md) for the actual execution record.
