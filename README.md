# Exact Primal-Dual Certificates for a Two-Bidder, Two-Item Auction

**Research preprint; not yet externally peer reviewed.**

This package specifies one final mechanism and one unrestricted upper
certificate for two additive bidders, two items and four independent
uniform values on `[0,1]`. The mechanism is measurable, pointwise DSIC,
ex-post IR and jointly feasible, with utility averaged over its internal
randomization. The optimal mechanism and a matching upper bound remain **open**.

## Certified result

The exact revenue is characterized by the sixteen-face integral formula
in the manuscript, with certified enclosure

```
0.876514341027067549900397423113 <= R_tau <= 0.876514355424052828335888359874
```

The final rational upper satisfies

```
OPT <= U < 0.882351585488796576205586892264
```

The gap enclosure is

```
0.005837230064743747869698532390 <= U - R_tau <= 0.005837244461729026305189469151
```

Thus **gap < 0.005837245 < 0.01**, and the mechanism earns more than
**99.3384%** of unrestricted randomized DSIC optimal revenue. The revenue
interval's midpoint or endpoint is not substituted for its exact integral
characterization. Exact rational upper components and outward-rounded
enclosures are specified by the [final manifest](certificate/reserve_parameter/manifest.json).

## Mechanism and theoretical content

The manuscript defines the seed mechanism directly by its base, Q and E
conditional menus, including lotteries, region boundaries and a joint tie
rule. At reserve `tau = 83/10000`, apply `T_tau(t) = max((t-tau)/(1-tau),0)`
coordinatewise, select the seed's complete joint allocation at that profile,
and charge `(1-tau) p_i^*(T_tau v) + tau sum_j x_ij^*(T_tau v)`.

- Zero-value exclusion at every selected tie makes the transform globally
  DSIC and IR; both bidders use the same transformed profile, ensuring capacity.
- The transform transfers ownership on a whole certified box. Its revenue
  includes all sixteen faces because clamping creates atoms at zero.
- Conditional supports pay the opposing virtual field, and translated IC
  corrections are aggregated on shared endpoint cells before taking a common
  itemwise maximum. The resulting bound covers the unrestricted randomized class.
- Exact integration remainders are distinguished from changes to the actual
  capacity measure and from the mechanism's incentive and capacity slacks.

The chosen mechanism, numerical bounds and certificate are specific to this
instance. The analytic transform has the stated general seed hypotheses;
no universal convergence or finite-menu optimality claim is made.

## Reading the paper

[Manuscript PDF](manuscript/manuscript.pdf) and [LaTeX source](manuscript/manuscript.tex).
The main text follows the final argument: model and theorem, complete
mechanism, exact revenue, common capacity certificate, verification and
remaining gap. Three appendices supply menu compatibility and seed revenue,
the radial/stream proof and coefficients, and certified integral components.
The general reserve proposition explicitly assumes a Borel seed with bounded
payments and zero-value exclusion. These hypotheses ensure measurability and
integrability after clamping. The selected seed satisfies them.

## Certificate map

Stable source directory names are retained so existing hashes and mathematical
replays remain valid. They are file identifiers, not steps readers must follow
to reconstruct the final mechanism.

| Mathematical component | Location |
|---|---|
| Selected reserve parameter, exact family checks and rational-report mechanism | certificate/reserve_parameter/ |
| Frozen face bounds, coupled IC and opposing-excess certificates | `certificate/v5_primal_dual/` |
| Complete seed menus and all-real compatibility proof | `certificate/coordinated_primal_dual/source/V4_6_1_1_lower_bound/`; `verifier/refined_candidate.py` and `research_log/refined_structure_audit.md` |
| Seed revenue by independent full integrals | Same source directory; `research_log/refined_revenue_audit.md`, with the independent audit material in the coordinated package |
| Reusable conditional density, low-square sign bound, sparse cycles and exact `B20`/`Delta1024` components | `certificate/coordinated_primal_dual/source/V4_6_2_upper/` |
| Rational stream coefficients and core polynomial construction | `certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/` |
| Shared-cell master certificate | `certificate/v5_primal_dual/source/V4_8A_frozen_primal/certificate/master_certificate.json` |
| Pointwise opposing-field splice proof | `certificate/v5_primal_dual/source/V5_gap_closure/research_log/global_duality.md` |
| Exact face calculator | `certificate/v5_primal_dual/source/V5_gap_closure/verifier/primal_face_integrals.py` |

The reserve-family optimum is uniquely in (0.008297,0.008299), and the entire
fixed-seed family has revenue below 0.87651436. This is not an unrestricted
upper bound. The selected simple rational is not claimed to be family-optimal.

The driver also verifies the frozen dependency packages, including
`certificate/joint_residual_screening_lower_bound/`. Their presence does not
introduce additional headline results into the paper.

The [verification guide](verification/README.md) identifies the final mechanism,
the executable checks and their independence boundaries.

The mathematical record is `certificate/reserve_parameter/manifest.json`.
Its content hash is printed in the manuscript.

## External comparison

Jiang, Parkes and Wang print a continuous upper certificate of `0.8919` and
approximately `0.876` GemNet revenue for this instance ([Tables 2 and 3](https://arxiv.org/html/2606.10112v1#S5)).
Our final upper improves the printed upper certificate. The external dual
array is not replayed here, and the rounded GemNet revenue does not certify
a ranking against its unrounded value.

## Reproduction

Use Python 3.10 or newer with NumPy, and pdfLaTeX with BibTeX (or the
documented Tectonic fallback). From the package root:

```powershell
python -E -s -B -X utf8 verification/reproduce_all.py
```

To save a transcript, add `--transcript verification/generated/reproduction.txt`.
This optional flag writes a temporary log; the canonical command above needs no
transcript file.

Use `--checks math` for mathematical replay alone, or `--checks release` for
text, metadata, compilation and hash consistency alone.
The default complete run checks text and compilation before long calculations.

This runs the complete certificate dependency chain, the final mathematical
assembly, manuscript and metadata consistency, a clean temporary-directory build and complete SHA-256 coverage.
Do not use `-O`, `-OO` or `PYTHONOPTIMIZE`: proof kernels contain executable
assertions and the supported driver rejects optimized mode.

The upper opposing-excess traversal trusts IEEE binary64 round-to-nearest
semantics and outward expansion using NumPy `nextafter`. Its full tree has a
primary replay and bounded independent cross-checks, not a second independently
implemented full tree. Other independence boundaries are stated in the paper.
See [ENVIRONMENT.md](ENVIRONMENT.md) for runtime details.

For compilation alone, with pdfLaTeX and BibTeX on `PATH`:

```powershell
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
```

Until a DOI or arXiv identifier is assigned, use the provisional citation in
`CITATION.cff`.

## Data, code, and materials availability

The public project repository is
[Baymax-ray/two-bidder-two-item-dsic-certificates](https://github.com/Baymax-ray/two-bidder-two-item-dsic-certificates).
The accompanying release archive contains the exact certificate data,
verification code, transcripts, environment information, and SHA-256 manifests.
The research workspace retains discovery-only experiments; they are not needed
by the reader-facing proof entrypoints.

## AI-assisted tools declaration

This manuscript was developed with the assistance of OpenAI GPT-5.6 Sol and OpenAI Codex.
The tool assisted with mathematical exploration, numerical candidate
generation, implementation and debugging of certificate and verification
code, and drafting and revision of the manuscript. Separately scoped
AI-assisted audits checked the new proofs, source implementations and exact
arithmetic. These are internal checks, not external peer review. AI-generated suggestions
and numerical search outputs were not treated as proofs; the stated results
are supported by the analytic arguments and exact certificates described
here. The author retains responsibility for the content, correctness, and
final presentation of this work.

## License

The manuscript, bibliography, certificate data, transcripts, and other
textual materials are licensed under CC BY 4.0; see `LICENSE`. Python software
is licensed under the MIT License; see `LICENSE-SOFTWARE`.

## Author

Jiarui Fang  
Boston University, Boston, Massachusetts, USA  
Email: baymin@bu.edu  
ORCID: [0009-0006-9100-0445](https://orcid.org/0009-0006-9100-0445)
