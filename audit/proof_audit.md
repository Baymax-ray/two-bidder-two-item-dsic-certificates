# Final proof and artifact audit

Audit date: 27 August 2026.

## Frozen theorem endpoints

- Exact deterministic lower bound:
  `26237753173862063/30000000000000000`.
- Exact continuous stream-dual upper bound:
  `18588262788621/20971520000000`.
- Exact gap:
  `1445765276937161827/122880000000000000000`.

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
7. The ten-band lower rule adds an opponent-dependent common fee to all
   nonempty menu options. Each bidder therefore keeps the base bundle or opts
   out, preserving pointwise DSIC, ex-post IR, and ex-post feasibility.

No unresolved item in this audit blocks the stated lower or upper theorem.

## Computational proof audit

The trusted formal upper verifier reconstructs the 32 frozen rational
coefficients, all four chart pairs, and the depth-21 base plus selective
depth-22 traversal. It reproduces accumulator `1858826278862100`, 404,804
fixed-winner-or-zero boxes, 462,796 unresolved base leaves, 391,618 refined
leaves, 71,178 retained leaves, 1,735,196 visited boxes, maximum error radius
165, and coverage `16777216/16777216`.

The non-importing upper replay imports neither the formal verifier nor its
polynomial module. It independently reconstructs the polynomial, Bernstein,
subdivision, winner, refinement, and coverage arithmetic and reproduces every
reported count and the exact upper fraction.

The exact base lower verifier reconstructs the affine/pivot cells. The active
symbolic surcharge verifier checks every band vertex and integrates all ten
rational bands. A separate non-importing replay uses scalar
`fractions.Fraction` arithmetic, fifth-difference degree checks, and exact
five-point Boole quadrature. Both reproduce
`26237753173862063/30000000000000000`.

Discovery-only floating-point files are outside the proof path.

## Release consistency audit

The release orchestrator checks the two theorem fractions against their active
manifests, verifies that the external `0.8919` and `0.876` benchmarks are
present but not labeled as our certificates, checks the AI-assisted-tools
declaration and author metadata, compiles the manuscript from a clean temporary
directory, and verifies complete SHA-256 coverage of stable release files. The
release PDF is regenerated from the updated source and checked against the
frozen certificate values.
