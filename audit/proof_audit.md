# Final proof and artifact audit

Audit date: 26 August 2026.

## Frozen theorem endpoints

- Exact deterministic lower bound:
  `26232788323031183/30000000000000000`.
- Exact continuous stream-dual upper bound:
  `930318295428931/1048576000000000`.
- Exact gap:
  `3144348548884251989/245760000000000000000`.

The endpoints are unequal. The unrestricted optimum remains open.

## Analytic proof audit

Status: **PASS**, with the following publication-facing issues resolved.

1. The mechanism class is stated as jointly measurable and integrable, so the
   conditional payment slices and Fubini step are legitimate.
2. Pointwise DSIC supplies a convex truthful utility and almost-everywhere
   gradient allocation; ex-post IR supplies the sign of the origin utility.
3. The singular radial field is handled on a punctured square. The limiting
   corner flux is retained explicitly, avoiding an unsupported bare
   distributional-divergence assertion at a boundary corner.
4. The stream correction is polynomial, divergence-free in own type, and has
   zero normal trace. Weak Green integration therefore preserves the revenue
   pairing on almost every opponent slice.
5. Ex-post item feasibility is applied only after summing the two bidder field
   pairings. The itemwise positive maximum is thus a valid relaxation for
   arbitrary randomized feasible allocations.
6. Each chart polynomial and competitor difference is constructed exactly.
   Directed fixed-point rounding encloses every Bernstein control, and the
   common-depth normalization for fixed, held, and split boxes is proved in
   the manuscript and checked by both implementations.

No unresolved item in this audit blocks the stated lower or upper theorem.

## Computational proof audit

The trusted formal verifier reconstructs the 32 rational coefficients, all
four chart pairs, and the adaptive depth-20-plus-one traversal. It checks the
manifest and arithmetic bounds and reproduces accumulator
`930318295428931`.

The clean-room verifier imports neither the formal verifier nor its polynomial
module. Its full replay reproduces the accumulator, refinement counts, axis
counts, and coverage `8388608/8388608`. Its paired-Fraction shallow mode
performs 3,087,315 enclosure checks and 444 charge checks. A separate
same-code scale-`10^8` run gives
`18606431629403/20971520000000`, so the improvement over the prior active
certificate is not created by scale-`10^9` rounding.

The exact lower-bound programs independently reconstruct the affine/pivot
cells and the surcharge revenue polynomial. Discovery-only floating-point
files are outside the proof path.

## Release consistency audit

The release orchestrator checks the two theorem fractions against their
manifests, verifies that the AI-assisted-tools declaration occurs exactly once
in both the manuscript and README, checks the author email and ORCID, compiles
the manuscript from a clean temporary directory, and verifies complete
SHA-256 coverage of stable release files. The final PDF is additionally
text-extracted to compare its theorem values with the frozen certificates and
rendered page by page for visual inspection.
