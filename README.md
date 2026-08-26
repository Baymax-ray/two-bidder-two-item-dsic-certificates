# Exact rational stream-dual bounds for a two-bidder, two-item auction

**Research preprint; not yet peer reviewed.**

This archive studies two additive bidders and two heterogeneous items with all
four values independent and uniform on `[0,1]`. Mechanisms may be randomized
and must be pointwise dominant-strategy incentive compatible (DSIC), ex-post
individually rational, and ex-post feasible.

The main result is the exact global upper bound

\[
\operatorname{OPT}\le
\frac{930318295428931}{1048576000000000}
=0.88722066443341350555419921875.
\]

It is certified by an explicit 32-parameter rational continuous stream-dual
witness and a deterministic adaptive tensor-Bernstein verifier with base
depth 20 and common final depth 21. A separately
implemented full replay obtains the same integer accumulator and box counts.
As a secondary result, an explicit deterministic menu mechanism has exact
revenue

\[
\frac{26232788323031183}{30000000000000000}
=0.8744262774343727\ldots .
\]

These endpoints do **not** meet. The unrestricted continuous DSIC optimum
remains open.

## Repository layout

- `manuscript/`: self-contained LaTeX source, bibliography, and release PDF.
- `certificate/continuous_stream_upper_bound/`: trusted rational upper-bound
  manifest, polynomial construction, formal verifier, and deterministic
  transcript; all stable files are covered by the root release hashes.
- `certificate/independent_stream_upper_bound/`: independent arithmetic replay
  and exact shallow enclosure audit.
- `certificate/ama_lower_bound/`: exact rational base-mechanism verifier.
- `certificate/menu_surcharge_lower_bound/`: exact surcharge improvement and
  hash binding to the base certificate.
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

The command reruns both lower-bound verifiers, the formal adaptive upper-bound
verifier, the independent shallow Fraction audit, the independent full
adaptive replay, a clean temporary-directory manuscript compilation, exact
theorem-value consistency checks, and release-hash verification. On the
recorded machine, the two full traversals together took about 22 minutes;
wall time is machine-dependent.

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

## AI-assisted tools declaration

This manuscript was completed with the assistance of OpenAI GPT-5.6 Sol.

## License

The manuscript, bibliography, certificate data, transcripts, and other
textual materials are licensed under CC BY 4.0; see `LICENSE`. Python software
is licensed under the MIT License; see `LICENSE-SOFTWARE`.

## Author

Jiarui Fang  
Boston University, Boston, Massachusetts, USA  
Email: baymin@bu.edu  
ORCID: [0009-0006-9100-0445](https://orcid.org/0009-0006-9100-0445)
