# Final proof and artifact audit

Audit date: 30 August 2026.

## Frozen theorem endpoints

- Exact deterministic lower bound:
  `83962078694672281756033/96000000000000000000000`.
- Exact continuous stream-dual upper bound:
  `3715139591287203/4194304000000000`.
- Exact gap:
  `34262987107793868572569/3072000000000000000000000`.

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
   common-depth normalization for fixed, retained, and refined boxes is checked
   by both implementations.
7. The twenty-band and bundle-pivot lower layers add an opponent-dependent
   common fee to all nonempty menu options. Each bidder therefore keeps the
   predecessor bundle or opts out.
8. Each item-containment row changes prices from `(A,B,C)` to
   `(A+delta,B,C+delta)` and verifies `0<delta<A+B-C`. The changed singleton
   cannot switch across items, a bundle buyer can move only to a subset, and
   an opt-out cannot enter. This completes the pointwise DSIC, ex-post-IR, and
   deletion-feasibility argument, including all tie and boundary cases.

No unresolved item in this audit blocks the stated lower or upper theorem.

## Computational proof audit

The trusted formal upper verifier reconstructs the 32 frozen rational
coefficients, all four chart pairs, and the depth-21 base plus selective
depth-22 and depth-23 traversals. It reproduces accumulator
`3715139591287203`, 404,804 boxes fixed before the unresolved depth-21 leaves,
462,796 unresolved base leaves, 391,618 first-level refinements, 609,951
second-level refinements, 3,738,334 visited nodes, maximum error radius 181,
and coverage `33554432/33554432`.

The non-importing upper replay imports neither the formal verifier nor its
polynomial module. It independently reconstructs the polynomial, Bernstein,
subdivision, winner, refinement, and coverage arithmetic and reproduces every
reported count and the exact upper fraction.

The exact base lower verifier reconstructs the affine/pivot cells. Sealed
predecessor verifiers then integrate twenty common-fee rows and 41 positive
bundle-pivot cells using exact rational arithmetic; independent scalar replays
check polynomial degrees and apply exact Boole quadrature. The active checker
hash-binds that chain, verifies all eight item-containment price regimes and
deletion margins, and integrates their symbolic gains. Its non-importing
replay instead reconstructs exact demand polygons and independently obtains
`83962078694672281756033/96000000000000000000000`.

Discovery-only floating-point files are outside the proof path.

## Release consistency audit

The release orchestrator checks the two theorem fractions against the active
two-level upper and final combined lower manifests, verifies that the external
`0.8919` and `0.876` benchmarks are present but not labeled as our
certificates, checks the AI-assisted-tools declaration and author metadata,
compiles the manuscript from a clean temporary directory, and verifies
complete SHA-256 coverage of stable release files. The release PDF is
regenerated from the updated source and checked against the frozen certificate
values.
