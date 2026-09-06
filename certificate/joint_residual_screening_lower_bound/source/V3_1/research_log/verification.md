# V3.1 verification record

The completed trial was checked on 2026-09-05 with CPython 3.10.16, using `python -B -X utf8` without optimization. This is an execution record, not a saved raw terminal transcript.

## Exact replay

The following command completed successfully after the mathematical code and certificates were finalized:

```powershell
python -B -X utf8 output/output/two_bidder_two_item_full_dsic_exact_auction/V3_1/verifier/run_all.py
```

Its final result was:

```text
V3_1_ALL_EXACT_REPLAYS_PASS: 17 mathematical replays and 3 preservation checks including dependencies
```

The runner includes the full V4/V3 dependency suite and five new mathematical replays: actual residual geometry, the universal screening certificate, the complete candidate and primary revenue expression, the closed-region audit, and the independent revenue evaluation. Normal execution compares the saved exact certificates without writing. The scripts reject optimized Python execution.

The closed-region audit checked 462 named rational boundary cases and three outside-region continuation cases. These are implementation checks accompanying the analytic proof for all real reports; they are not a finite sample proof of continuum feasibility. The candidate replay also checks a polynomial identity at 60 exact rational nodes, with separate degree bounds `(3,2,4)`. Polynomial interpolation justifies that identity check. These nodes are not a finite type approximation to the auction problem.

The independent revenue replay uses dictionary polynomials, dyadic radical enclosures, and a binomial remainder. It does not call the primary candidate revenue function or its logarithm evaluator. It independently confirms the factor for changing one bidder in both item orientations, the V4 baseline, the strict gain, the area of `Q`, and its integrated inner optimum. Its resulting revenue enclosure is

```text
0.875243586975954394119020 <= R_V3.1 <= 0.875243586975954394119021
```

## Analytic scope and discovery boundary

The machine replays verify exact algebra, certified enclosures, specified boundary cases, and implementation consistency. The universal DSIC envelope, the capacity-measure gap identity for arbitrary randomized mechanisms, and its application at every actual residual in the closed region `Q` rest on the written proofs and independent analytic audits. They have not been formalized in a proof assistant.

The optional SciPy single-lottery probe is preserved as discovery history and is excluded from the exact runner. Its reported zero gain has no role in the optimality proof. No floating optimizer or finite type grid enters the certificate.

The matching support concerns the inner revenue integrated over `Q`. It does not solve the inner contribution on `Q^c`, certify bidder 1's outer optimum, or match the inherited unrestricted auction upper bound. The inherited upper bound was not newly fully recertified in this trial.

## Preservation and file identity

The preservation replay passed for all 811 stable identities in the pre-trial outer manifest. The sole replaced navigation file, `CURRENT_PHASE.md`, is preserved byte-for-byte as `certificate/pre_V3_1_CURRENT_PHASE.md`. The previous manifest is preserved as `certificate/pre_V3_1_SHA256SUMS`. V3, V4, earlier research packages, and the closed archive remain unchanged.

The V3.1 and outer `SHA256SUMS` files cover their respective stable inventories and can be checked with the two manifest commands in the README. Manifests establish file identity and coverage, not the mathematical claims. The inherited checker excludes its own manifest, designated LaTeX build/QA directories, Python caches, and bytecode.
