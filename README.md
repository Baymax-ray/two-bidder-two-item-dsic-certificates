# Exact primal-dual certificates for a two-bidder, two-item auction

**Research preprint; not yet peer reviewed.**

For two additive bidders, two items and four independent uniform values on
`[0,1]`, the selected V4.6.1.1 mechanism is pointwise DSIC, ex-post IR,
measurable and jointly feasible, with exact revenue

$$
R_*=
\frac{35791404252341621852527735747861637}{42525000000000000000000000000000000}
+\frac{31}{1215}\sqrt2
-\frac{15059524650320123}{8305664062500000000000}\sqrt{493894}.
$$

The independently certified interval is

$$
0.876464164471798049944906113027<R_*
<0.876464164471798049944906113028.
$$

The V4.6.2 upper covers the **unrestricted randomized DSIC class**:

$$
R_*\le\mathrm{OPT}\le U_*<0.882923053259,
$$

where the explicit rational certificate is

$$
U_*=
\frac{231831916327659047}{262144000000000000}
-\Delta_{1024}-\frac{81}{10^{10}}.
$$

The full exact rational subtraction and endpoint are in
[the active manifest](certificate/coordinated_primal_dual/manifest.json).
The certified gap is **below 0.006459, hence below 0.01**:

$$
0.006458888786918919315720686827<U_*-R_*
<0.006458888786918919315720686828.
$$

The mechanism earns **more than 99.2684% of unrestricted optimal revenue**.
The optimal auction and a matching certificate remain open. A fresh exact
lottery-box test proves that the present common price does not match the
selected mechanism.

The theoretical advances are:

- **Complete joint exchange.** A monotone threshold with a jump and its
  generalized-inverse plateau change ownership on a positive-volume region.
  The mechanism specifies both menus and joint selection for every report,
  including ties. Three continuous revenue integrations recover the same
  algebraic coefficients; alternative experiments are not added together.
- **Incentive restrictions implied by occupied regions.** Utility traces
  yield full randomized conditional screening certificates on Q, E and an
  occupied wing. Their union covers 64.1627% of opponent-report space.
  This is a map of conditional problems solved at actual residual capacity,
  not a percentage of the global gap closed. The E/W rent elimination does
  not supply a support for arbitrary capacity changes.
- **Strictly less total common capacity price.** A
  universal conditional identity, an opposing virtual-value sign certificate
  and four sparse long-range IC cycles decrease its total mass while
  preserving both unrestricted charged inequalities. The original stream
  maximum already gives zero charged values; their existence alone is not
  the advance. An exact gap identity separates screening,
  unused capacity, virtual allocation and IC/IR slack from numerical
  enclosure remainders. Solving the charged values alone does not establish
  an equality auction.

These are explicit instance-specific constructions and identities. Convex
utility, transport duality and complementary slackness are prior foundations;
we make no first-in-literature or general convergence claim.

## External benchmarks and our improvements

Jiang, Parkes and Wang report a continuous upper bound `0.8919` in Table 2
and GemNet revenue approximately `0.876` in Table 3. We rechecked these
printed values in [their source](https://arxiv.org/html/2606.10112v1#S5).
The new local upper improves the printed external upper by more than
`0.008976946741`. The new exact revenue exceeds the printed `0.876`, but
that rounded report alone cannot establish superiority to GemNet's
unrounded revenue. We did not replay its mechanism or underlying dual array.

The retained stream endpoint is
`3715139591287203/4194304000000000 = 0.8857583025186545848846435546875`.
The new upper improves it by approximately `0.002835249259937616`.
Of this decrease, approximately `0.00138972521893` tightens the enclosure
of the same stream integral, `0.00144551594101` comes from conditional
support replacement, and exactly `0.0000000081` comes from the four IC
cycles. The cycles demonstrate additional admissible incentive directions;
their current numerical contribution is small.
The previous V4.6 lower was in
`(0.8758198541484224553460, 0.8758198541484224553461)` and the retained
fully deterministic lower is
`83962078694672281756033/96000000000000000000000`.
These remain reproducible historical results. The active lower exceeds
V4.6.1 by more than `0.0000085`.

The new [independent audit](audit/V4611_V462_RELEASE_AUDIT.md) reconstructs
all-real compatibility arguments, the full algebraic revenue and the common
support, and repeats both complete upper traversals. Source identity checks
are reported separately from mathematical replays. The new lower does not
rely on merely adding an audited increment to an unevaluated historical
reference integral.

A [three-report internal self-review and revision](audit/nature_review_v4611_v462/README.md)
corrected a temporary-path metadata defect, calibrated the theoretical
contribution and clarified componentwise replay independence. Both complete
corrected portable runs passed from distinct temporary roots; frozen
pre-revision reports remain available alongside the author corrections.

## Repository layout

- `certificate/coordinated_primal_dual/`: active paired endpoints, portable
  source closure, both complete new upper traversals and fresh independent
  structure, full-revenue and support audits.
- `manuscript/`: LaTeX source, the residual-screening theory and stable
  mechanism/revenue specification,
  bibliography and release PDF.
- `certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/`:
  retained rational upper-bound manifest, polynomial construction, formal
  verifier, non-importing replay, and deterministic transcripts.
- `certificate/continuous_stream_degree4_nonuniform_upper_bound/`,
  `certificate/continuous_stream_upper_bound/`, and
  `certificate/independent_stream_upper_bound/`: superseded but retained upper
  certificates and independent audit.
- `certificate/ama_lower_bound/`: exact rational base-mechanism verifier.
- `certificate/joint_residual_screening_lower_bound/`: retained V4.6 randomized lower
  mechanism, portable source closure, exact revenue and conditional supports,
  fresh independent audits and source bindings.
- `certificate/refined_item_containment_bundle_pivot_lower_bound/`: retained
  deterministic lower certificate with eight item-containment cells and complete
  SHA-256 bindings to its predecessor chain.
- `certificate/piecewise_surcharge_bundle_pivot_lower_bound/` and
  `certificate/piecewise_surcharge_twenty_band_lower_bound/`: independently
  replayed 41-cell bundle-pivot and twenty-band predecessors.
- `certificate/piecewise_surcharge_lower_bound/`: retained exact ten-band
  predecessor, non-importing replay, and hash binding to the base certificate.
- `certificate/menu_surcharge_lower_bound/`: superseded two-rectangle lower
  certificate, retained as a reproducible predecessor.
- `verification/`: publication-level orchestrator, hash tools, release
  transcript, and theorem-to-certificate consistency checks.
- `audit/`: independent proof/revenue audits, fresh full upper replays,
  claim-to-evidence ledger and the three-report internal Nature-style
  self-assessment with post-review synthesis and revision record.
- `provenance/`: bounded final-sprint report and clearly segregated
  discovery-only numerical experiments.

The proof path consists of the analytic arguments in `manuscript/`, the
exact kernels in `certificate/`, and the explicitly invoked supplementary
audit checks in `audit/`. Files under `provenance/discovery_only/` record how
witnesses were found or why alternatives stalled; sampled or floating-point
values there are not theorem claims.

## Reproduction

Requirements are Python 3.10 or newer, NumPy for the upper traversal,
`pdflatex`, and `bibtex`. The new lower package uses Python standard-library
exact arithmetic; the original upper release environment is retained in
ENVIRONMENT.md. Install the pinned Python
dependency if needed:

```powershell
python -m pip install -r requirements.txt
```

From the archive root, run the complete publication-facing replay:

```powershell
python -B verification\reproduce_all.py
```

The command reruns the base and complete lower-certificate dependency chain,
the retained V4.6 lower, the active coordinated certificate with both new
complete upper traversals and independent audits, a clean manuscript build, exact
theorem-value consistency checks, and release-hash verification. The two
upper traversals are the runtime-dominant steps; wall time is
machine-dependent.

The two complete upper traversals independently implement the stream
majorant `B20`. The conditional subtraction has one complete `1024`
partition accumulation, plus an independent reconstruction of all averaged
coefficients, classification cross-checks through size `64` and selected
cell integrals. That second check reuses the primary classifier and
integral tables; it is not a second full subtraction accumulation. The IC
cycles have separate whole-box sign and exact decrement checks.

The entry point explicitly rejects optimized Python execution. Do not use
`-O`, `-OO`, or `PYTHONOPTIMIZE` for direct certificate commands: retained
proof kernels use executable assertions. The supported entry point fails with
a nonzero exit status before launching those kernels in optimized mode.

Individual proof checks can be run from their certificate directories using
the commands documented in their local `README.md` files. To compile only the
paper:

```powershell
cd manuscript
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
bibtex manuscript
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
pdflatex -interaction=nonstopmode -halt-on-error manuscript.tex
```

## Exact status and citation

The archive proves a rigorous interval, not an exact solution of the open
optimization problem. Until a DOI or arXiv identifier is assigned, use the
provisional citation in `CITATION.cff`.

## Data, code, and materials availability

The public project repository is
[Baymax-ray/two-bidder-two-item-dsic-certificates](https://github.com/Baymax-ray/two-bidder-two-item-dsic-certificates).
The accompanying release archive contains the exact certificate data,
verification code, transcripts, environment information, and SHA-256 manifests.
Discovery-only experiments are separate from the trusted proof artifacts.

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
