# Reproduction environment

The exact lower-bound and rational IC checks use Python's arbitrary-precision
integers, `Fraction`, and integer-square-root enclosures. The stream and V5
continuous-support verifiers also require NumPy. The final reserve bracket leaves
the unrestricted optimum and a matching certificate open.

Recorded release environment:

- Windows 11 and PowerShell;
- Python 3.10.16;
- NumPy 2.0.1;
- signed 64-bit NumPy integer arrays, with explicit bounds checked by the relevant
  upper-bound verifiers;
- IEEE-754 binary64 round-to-nearest basic arithmetic and correctly directed
  `numpy.nextafter`, with 52 explicit mantissa bits and epsilon `2**-52`;
- a TeX build tool on `PATH`: either both `pdflatex` and `bibtex` from a
  TeX Live-compatible distribution, or Tectonic.

The final V5 manuscript build was verified with `pdflatex` and `bibtex`
from TinyTeX/TeX Live 2026. Put the current installation's binary directory
on `PATH` so both tools are found. The V5 audit also
verified official Tectonic 0.17.0 for Windows as a fallback while those tools
were absent from `PATH`. The Tectonic executable's SHA-256 was
`99ffcfdbf1ebf8bdda9e791942e3d06aedb12463fddc33f07de6f5211c8bf08d`;
the official release ZIP's SHA-256 was
`f61ce51f0b0ade1015b7de7ef368541c5424e9756ecbd0d7af97d6d48030845f`.
These identify the observed audit runtime; no executable is bundled with
this source archive.

If `pdflatex` and `bibtex` are not both found, the public runner uses
`tectonic --keep-logs --keep-intermediates --outdir BUILD manuscript.tex`
in its clean temporary build directory. Tectonic runs BibTeX and the required
TeX passes automatically. Its first run may download TeX dependencies;
`TECTONIC_CACHE_DIR` can select an existing writable cache. The audit used a
cache outside the publication archive. The final log is checked for
unresolved references or citations before the generated PDF is accepted.

Python 3.10 or newer is required. Run proof entrypoints with
`python -B -X utf8`; optimized modes (`-O`, `-OO`, or a nonzero
`PYTHONOPTIMIZE`) are unsupported because assertions are part of the proof
checks. The exact checks rely on Python's integer and rational semantics and
NumPy's checked signed `int64` arithmetic.

The V5 support-splice certificate additionally brackets each rational-to-float
conversion and expands every bounding binary64 operation outward with
`nextafter`. Its Bernstein subdivision bounds use outward rounding; rational
box volumes, checked dyadic integer accumulation, and integer-square-root
brackets complete the accepted enclosure. These floating-point semantics are
explicit trusted assumptions. Floating discovery estimates and grid samples
do not establish the continuous bound.

The public runner retains the historical certificate groups and the 46-entry
coordinated predecessor replay, then verifies the inherited portable upper/face component, its exact assembly,
and the final reserve parameter and implementation. Portable replays materialize source trees in a
temporary directory; a short writable `TEMP`/`TMP` path avoids Windows path
length failures. Continuous tree traversals can take several minutes. Wall
time and memory use are environmental, not theorem inputs.

The LaTeX source uses the standard `article` class and the packages
`geometry`, `amsmath`, `amssymb`, `amsthm`, `booktabs`, `array`, `hyperref`,
and `natbib`.

The final selected reserve is 83/10000. Its standard-library rational checker
and exact rational-report implementation are under certificate/reserve_parameter/.
The publication driver separates mathematical replay (--checks math) from
release consistency (--checks release); the default runs both, with the clean
TeX build checked before long mathematical replays.

The publication runner and portable upper/face wrapper clear ambient Python
import overrides for subprocesses. Direct Python children use `-E -s`; legacy
descendants inherit `PYTHONNOUSERSITE=1`. The portable runtime probe records
`sys.executable`, Python and NumPy versions, import flags and the resolved paths
of NumPy, its loaded multiarray extension and core arithmetic modules. These
paths identify the observed trusted runtime and do not turn installed third-party
code into a source-certified or hermetic dependency.
