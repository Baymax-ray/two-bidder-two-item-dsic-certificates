# Final proof and artifact audit

Release audit date: 30 August 2026. Internal-review clarifications updated
3 September 2026. Historical full-traversal results below are not a claim of
a new full-depth run on the revision date.

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
   distributional-divergence assertion at a boundary corner. Classical
   divergence is asserted only on the two open triangles, hence almost
   everywhere; continuity makes their diagonal boundary fluxes cancel.
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
bundle-pivot cells using exact rational arithmetic; separate scalar replays
apply exact Boole quadrature with analytic polynomial degree bounds and
finite-difference consistency checks. The active checker
hash-binds that chain, verifies all eight item-containment price regimes and
deletion margins, and integrates their symbolic gains. Its non-importing
replay instead reconstructs exact demand polygons and independently obtains
the eight-row gain, then adds the sealed predecessor revenue to obtain
`83962078694672281756033/96000000000000000000000`. All lower-layer replays
share the base revenue from the single affine-polytope verifier. Hash bindings
identify the dependency files; they do not supply a second independent
integration of the complete base mechanism.

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

## Internal pre-review revision, 3 September 2026

This is an author-internal change tracker, not a reviewer-facing response or
a journal decision. All six requested clarifications were adopted without
changing the theorem endpoints, frozen coefficients, or mechanism parameters.

| Supplied comments | Adopted change | Location |
| --- | --- | --- |
| R1-m1, R2-m2 | Label the sealed upper-package gap as historical and give the active release gap separately. | Active upper README |
| R1-m2, R2-M1 | State the shared single base-revenue verifier and the independent scope of the added-gain replays. | Contributions, Exact revenue, Reproducibility, root README, CITATION.cff |
| R1-m3, R3-m2 | Test the bundle-pivot region before defining the normalized coordinate; state the positive denominator bound. | The entry-surcharge mechanism |
| R2-m1 | Derive quadrature validity from the analytic menu formula and whole-row price regime; describe differences only as consistency checks. | Exact revenue, Reproducibility, lower READMEs, active replay diagnostics |
| R3-m1 | Require both price triples to satisfy the menu-revenue lemma and state the nonnegative-fee cap. | Exact revenue |
| R3-m3 | Restrict classical divergence to the two open triangles and explain cancellation of diagonal flux. | A rational continuous stream certificate |

The shared-base concern was classified Minor by Reviewer 1 and Major,
Blocking No by Reviewer 2. This revision resolves the overstatement by
restricting the claim, not by claiming a new independent base integration.
The manuscript and citation date, AI-use scope and author responsibility, and
public repository URL were also updated. The historical literature-search
date is retained because this revision does not repeat that search.

Revision verification passed all ten lower-certificate commands, including
the affine base and each primary and additional-gain replay. Exact regression
checks reproduced the supplied price-regime and finite-difference
counterexamples, the excluded zero-denominator report, and the diagonal
one-sided derivatives. Every mathematical manifest payload equals the
pre-review Git version after ignoring dependency-hash fields. An AST comparison
confirmed that the active replay changed only comments and diagnostic strings.
The revised 13-page PDF compiled without warnings, passed exact-endpoint,
date, declaration and hyperlink checks, and was visually inspected on every
page. No full depth-21-to-23 upper traversal, new external certificate replay,
or exhaustive novelty search was performed in this revision.

The subsequent file-location clarification (follow-up R3-m1) was also adopted
in Section 5. The active manifest contains eight item-containment rows; the
twenty Z/S rows and 41 positive bundle-pivot rows reside in its hash-bound
predecessor manifests. Both predecessor paths are now listed explicitly in
the manuscript. Their locations and row counts were checked directly; no
certificate data or verification code changed in this follow-up.

## Exposition revision after further internal review, 3 September 2026

The supplied review was a static assessment, not a new verifier run or an
external acceptance decision. This revision preserves the eight-section
framework and the frozen endpoints while making the proof dependencies
explicit. It does not introduce a new mechanism, witness, or search result.

Adopted changes:

- The abstract and main theorem highlight the deterministic revenue guarantee
  of at least 98.7408% of unrestricted optimal revenue. Exact arithmetic gives
  `L/U = 2686786518229513016193056/2721049505337306884765625`, strictly greater
  than `0.987408`. The release source-consistency check now verifies this
  inequality and the presence of the guarantee in the manuscript and README.
- The upper proof is separated into Stream weak duality, Rational witness
  feasibility, and Certified envelope statements. The analytic theorem
  retains origin utility, the given measurable subgradient selection,
  weak Green integration, and the pointwise itemwise support bound.
- A named Deletion containment lemma precedes the menu parameters. The item
  supports explicitly ensure that the opponent's low coordinate is unique.
- Exact revenue now explains rational demand polygons, analytic degree
  bounds for Boole quadrature, and telescoping gains on overlapping
  predecessor supports. A compact table records each layer and replay scope.
- The trusted computational components and the shared mathematical principle
  and input data of the two upper implementations are explicit. Repeated
  defensive scope statements were reduced; the restricted weak-dual scope
  remains stated where it matters.

Suggestions not adopted verbatim:

- Origin normalization is unnecessary: the proof retains the nonpositive
  origin term and justifies its integrability by the Lipschitz bound.
- The review's GemNet value `0.878` was not substituted. Jiang--Parkes--Wang
  version 1, Table 2 and Table 3 were checked and support the existing reported
  benchmarks `0.8919` and `0.876`, respectively.
- The existing supported reproduction entry point already rejects optimized
  Python through an explicit runtime condition. Frozen assertion-based
  kernels were not rewritten as part of prose revision. The restriction on
  direct kernel execution is now stated in the manuscript and verification
  documentation. No duplicate reproduction entry point was added.
- No separate-branch counterexample, unverified completeness claim, new
  figure, or reviewer-facing response package was imported into this revision.

Verification performed for this revision:

- All ten lower verification/replay commands passed, including the base
  polytope integration and every added-gain layer.
- All 32 manuscript coefficients match the active upper manifest; exact
  polynomial checks verified zero divergence, boundary tangency, and item
  exchange. Both upper implementations agreed on all four chart pairs,
  Bernstein root arrays, and the depth-8 base plus two refinement levels,
  visiting 4,206 nodes in total.
- The release entry point rejected `-O`, `-OO`, and `PYTHONOPTIMIZE=1` with
  exit status 1 before launching certificate kernels. In-memory changes to
  degree, basis order, and coefficient count were rejected by both upper
  manifest loaders (six checks); no certificate files were modified.
- The theorem/README/manifest/declaration check passed. The revised 15-page
  PDF compiled without warnings and was visually inspected on every page.
- Root SHA-256 coverage passed for all 103 stable files. Comparison with the
  pre-revision hash list confirmed that every certificate file was unchanged;
  only manuscript, citation, explanatory, audit, and source-consistency files
  changed in this revision.

The full depth-21-to-23 upper traversal was not rerun. These bounded checks
are not a fresh full-endpoint recertification or an independent analytic
peer review. The exact residual gap remains
`34262987107793868572569/3072000000000000000000000`.
