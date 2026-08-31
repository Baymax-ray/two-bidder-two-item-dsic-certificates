# Publication verification

`reproduce_all.py` is the release orchestrator. It reruns the exact affine
base, retained lower predecessors, twenty-band refinement, bundle-pivot
extension, and active item-containment lower certificate, including every
non-importing lower replay. It also reruns the formal two-level nonuniform
upper certificate and its non-importing full replay, checks theorem/README
consistency, builds the manuscript in a clean temporary directory, and verifies
the root SHA-256 manifest.

The lower replays independently recompute added revenue layers, not a second
from-scratch integral of the base mechanism. They share the exact base
revenue certified by the single affine-polytope verifier. Finite differences
are consistency checks; analytic menu formulas and exact price-region checks
supply the degree bounds that justify Boole quadrature.

The upper replay is independent at the implementation level: it shares the
rational manifest and Bernstein enclosure principle with the formal verifier.
The analytic weak-duality theorem is a separate manuscript argument. The
computational trusted base includes Python integers, `fractions.Fraction`,
checked NumPy integer operations, JSON parsing, SHA-256, and file I/O.

The supported entry point checks Python 3.10 or newer and rejects optimized
execution using an explicit runtime condition, returning a nonzero exit code
before running any certificate. Retained kernels use executable assertions,
so direct invocations must also omit `-O`, `-OO`, and `PYTHONOPTIMIZE`.
This restriction is not a claim that the kernels themselves are safe under
optimization. The source-consistency check also verifies the exact inequality
behind the manuscript's rounded-down 98.7408% revenue guarantee.

`make_hashes.py` creates `../SHA256SUMS`; `verify_hashes.py` requires exact
coverage of every stable file. Generated clean-run transcripts under
`generated/` and temporary LaTeX build products are intentionally excluded
from the root manifest. The release PDF and all frozen certificate transcripts
are included.
