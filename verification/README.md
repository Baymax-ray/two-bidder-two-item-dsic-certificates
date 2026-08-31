# Publication verification

`reproduce_all.py` is the release orchestrator. It reruns the exact affine
base, retained lower predecessors, twenty-band refinement, bundle-pivot
extension, and active item-containment lower certificate, including every
non-importing lower replay. It also reruns the formal two-level nonuniform
upper certificate and its non-importing full replay, checks theorem/README
consistency, builds the manuscript in a clean temporary directory, and verifies
the root SHA-256 manifest.

`make_hashes.py` creates `../SHA256SUMS`; `verify_hashes.py` requires exact
coverage of every stable file. Generated clean-run transcripts under
`generated/` and temporary LaTeX build products are intentionally excluded
from the root manifest. The release PDF and all frozen certificate transcripts
are included.
