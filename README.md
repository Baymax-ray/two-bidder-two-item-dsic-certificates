# Exact rational stream-dual bounds for a two-bidder, two-item auction

**Research preprint; not yet peer reviewed.**

This archive studies two additive bidders and two heterogeneous items with all
four values independent and uniform on `[0,1]`. Mechanisms may be randomized
and must be pointwise dominant-strategy incentive compatible (DSIC), ex-post
individually rational, and ex-post feasible.

The main result is the exact global upper bound

$$
\mathrm{OPT}\le
\frac{3715139591287203}{4194304000000000}
=0.8857583025186545848846435546875.
$$

It is certified by an explicit 32-parameter rational continuous stream-dual
witness and a deterministic nonuniform tensor-Bernstein verifier with a
depth-21 base tree and two selective local refinement levels. A separately
implemented non-importing replay obtains the same integer accumulator, box
counts, and complete dyadic coverage. As a secondary result, an explicit
deterministic layered menu mechanism has exact revenue

$$
\frac{83962078694672281756033}{96000000000000000000000}
=0.8746049864028362682920104166\ldots .
$$

The remaining exact gap is
`34262987107793868572569/3072000000000000000000000`, approximately
`0.01115331611581831659`. The deterministic mechanism therefore earns at least
**98.7408% of the unrestricted optimal revenue**, because its exact revenue
divided by the exact upper certificate exceeds `0.987408`. The unrestricted
optimum remains open.

The upper proof separates analytic weak duality, rational witness feasibility,
and finite exact envelope certification. The lower construction uses
deletion containment to preserve simultaneous feasibility as menus change;
opponent-conditioned taxation alone supplies each bidder's DSIC.

## External benchmarks and our improvements

The closest directly comparable external result located in our
[bounded literature audit](audit/literature_novelty_audit.md) is the strict
continuous DSIC upper certificate `0.8919` reported by Jiang, Parkes, and
Wang for this instance. The same paper reports revenue approximately `0.876`
for GemNet's fully strategyproof mechanism. Both numbers are **external
benchmarks**: `0.8919` is their rigorous continuous upper bound, while
`0.876` is their reported computational revenue for an exactly strategyproof
primal mechanism, not an exact rational certificate produced or replayed here.

Both endpoints improve this archive's preceding release. The quantitative
improvement over the external benchmark is the upper bound. Its certificate
has a separate full implementation replay, sharing the rational manifest and
Bernstein enclosure principle. For the lower mechanism, one exact polytope
verifier certifies the base revenue, and separate replays recompute the added
revenue layers while sharing that base value; there is no second from-scratch
integration of the complete base mechanism.
The new upper bound lowers the external `0.8919` benchmark by the exact amount
`25760146312797/4194304000000000`, approximately `0.006141697481345415`, and
lowers this archive's preceding active exact upper bound
`18588262788621/20971520000000` by
`2512966436997/4194304000000000`, approximately `0.000599137887238741`.
The new lower mechanism improves this archive's preceding exact lower bound
`26237753173862063/30000000000000000` by
`422846104560052011/32000000000000000000000`, approximately
`0.000013213940767501625`. It does not improve on the reported GemNet revenue
`0.876`; its distinct contribution is an explicit layered mechanism with exact
symbolic revenue, pointwise boundary rules, and independent replays of the
additional revenue layers.

## Repository layout

- `manuscript/`: self-contained LaTeX source, bibliography, and release PDF.
- `certificate/continuous_stream_degree4_two_level_nonuniform_upper_bound/`:
  active rational upper-bound manifest, polynomial construction, formal
  verifier, non-importing replay, and deterministic transcripts.
- `certificate/continuous_stream_degree4_nonuniform_upper_bound/`,
  `certificate/continuous_stream_upper_bound/`, and
  `certificate/independent_stream_upper_bound/`: superseded but retained upper
  certificates and independent audit.
- `certificate/ama_lower_bound/`: exact rational base-mechanism verifier.
- `certificate/refined_item_containment_bundle_pivot_lower_bound/`: active
  exact lower certificate with eight item-containment cells and complete
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

Requirements are Python 3.10 or newer, NumPy, `pdflatex`, and `bibtex`. The
recorded release used Python 3.10.16 and NumPy 2.0.1. Install the pinned Python
dependency if needed:

```powershell
python -m pip install -r requirements.txt
```

From the archive root, run the complete publication-facing replay:

```powershell
python -B verification\reproduce_all.py
```

The command reruns the base and complete lower-certificate dependency chain,
the formal two-level nonuniform upper-bound verifier, every non-importing
active replay, a clean temporary-directory manuscript compilation, exact
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

This manuscript was completed with the assistance of OpenAI GPT-5.6 Sol.
The tool assisted with mathematical exploration, numerical candidate
generation, implementation and debugging of certificate and verification
code, and drafting and revision of the manuscript. AI-generated suggestions
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
