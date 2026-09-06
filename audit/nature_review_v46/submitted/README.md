# Exact primal-dual certificates for a two-bidder, two-item auction

**Research preprint; not yet peer reviewed.**

This archive studies two additive bidders and two heterogeneous items with
four independent uniform values on `[0,1]`. Mechanisms may be randomized
and satisfy pointwise DSIC, ex-post IR and ex-post feasibility.

The new explicit randomized mechanism has exactly specified revenue

$$
0.8758198541484224553460<R_J<0.8758198541484224553461.
$$

Together with the retained unrestricted upper certificate,

$$
R_J\le\mathrm{OPT}\le
\frac{3715139591287203}{4194304000000000}
=0.8857583025186545848846435546875.
$$

The certified gap is **strictly below 0.01**:

$$
0<U-R_J<0.0099384483702321295386<\frac1{100}.
$$

The mechanism earns at least **98.8779% of unrestricted optimal revenue**.
Its exact revenue is an explicitly defined reference integral plus rational,
radical and logarithmic increments; decimals here are rational enclosures.
The optimal auction and a matching common upper certificate remain open.

The theoretical additions are:

- **Full randomized residual screening.** Explicit capacity-price measures
  solve the conditional problem at a diagonal capacity hole and a lottery
  junction. Competitors may have arbitrary allocation ranges.
- **Information-rent constraints in the support.** Exact nonnegative slack
  identities combine volume prices, singular report-line prices, convex
  utility traces and IR. Residual capacity is treated pointwise, including
  priced null-volume lines.
- **Profitable joint reallocation.** Binding support conditions guide
  complete changes to both bidders' menus. A coupled singleton/bundle
  response and a compensated lottery-price cut transfer ownership while
  preserving pointwise DSIC and feasibility. All induced revenue effects
  are integrated over the entire affected report regions.

These extend the retained stream weak-duality and exact tensor-Bernstein
upper proof. Conditional optimality is explicitly separated from global
auction optimality: a two-sided variation strictly improves a reference
whose conditional lottery menus were already optimal at their old residual.

## External benchmarks and our improvements

The closest directly comparable external result located in our
[bounded literature audit](audit/literature_novelty_audit.md) is the strict
continuous DSIC upper certificate `0.8919` reported by Jiang, Parkes, and
Wang for this instance. The same paper reports revenue approximately `0.876`
for GemNet's fully strategyproof mechanism. Both numbers are **external
benchmarks**: `0.8919` is their rigorous continuous upper bound, while
`0.876` is their reported computational revenue for an exactly strategyproof
primal mechanism, not an exact rational certificate produced or replayed here.

The stream upper remains unchanged in this update. It improves the external
`0.8919` bound by the exact amount `25760146312797/4194304000000000`.
The new lower mechanism improves this archive's retained deterministic
revenue `83962078694672281756033/96000000000000000000000`
(approximately `0.8746049864028362682920`) by approximately
`0.001214867745586187`. It does not improve on the reported GemNet revenue
`0.876`. Its contribution is a complete mechanism with exact accounting,
full-class conditional theorems and proof-guided joint allocation changes.

The old stream upper has a separate full implementation replay. The new
lower additions have fresh independent menu, dual and revenue audits.
These reconstruct the new polynomial/radical/logarithmic contributions,
while retaining the exact historical reference integral explicitly. Neither
a hash nor an added-gain replay is claimed to be a second from-scratch
integration of every historical base layer.

## Repository layout

- `manuscript/`: LaTeX source, the residual-screening theory supplement,
  bibliography and release PDF.
- `certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/`:
  active rational upper-bound manifest, polynomial construction, formal
  verifier, non-importing replay, and deterministic transcripts.
- `certificate/continuous_stream_degree4_nonuniform_upper_bound/`,
  `certificate/continuous_stream_upper_bound/`, and
  `certificate/independent_stream_upper_bound/`: superseded but retained upper
  certificates and independent audit.
- `certificate/ama_lower_bound/`: exact rational base-mechanism verifier.
- `certificate/joint_residual_screening_lower_bound/`: active randomized lower
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
- `audit/`: final literature/novelty audit and proof-artifact ledger.
- `provenance/`: bounded final-sprint report and clearly segregated
  discovery-only numerical experiments.

Only `certificate/` and the analytic arguments in `manuscript/` belong to the
trusted proof path. Files under `provenance/discovery_only/` record how
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
the portable new lower certificate and its independent audits, the formal
two-level upper verifier and non-importing replay, a clean manuscript build, exact
theorem-value consistency checks, and release-hash verification. The two
upper traversals are the runtime-dominant steps; wall time is
machine-dependent.

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
