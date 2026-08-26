# Reproduction environment

The trusted lower-bound verifiers use only the Python standard library. The
stream verifiers require NumPy.

Recorded release environment:

- Windows 11 and PowerShell;
- Python 3.10.16;
- NumPy 2.0.1;
- signed 64-bit NumPy integer arrays, with explicit bounds checked by both
  upper-bound verifiers;
- `pdflatex` and `bibtex` from a TeX Live-compatible distribution.

Python 3.10 or newer is required. The exact certificate outputs are
deterministic across platforms satisfying Python's integer semantics and
NumPy's signed `int64` semantics. Wall time and memory use are environmental,
not theorem inputs.

The LaTeX source uses the standard `article` class and the packages
`geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `hyperref`,
and `natbib`.
